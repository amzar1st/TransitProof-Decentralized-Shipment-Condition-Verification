"""Dependency-free behavior tests. GenVM host is mocked, not a network simulator."""
import importlib.util
import sys
import types
import unittest
from pathlib import Path
import hashlib
import base64

class UserError(Exception):
    pass

class Address(str):
    def __new__(cls, value):
        if len(value) != 42 or not value.startswith('0x'):
            raise ValueError('address')
        int(value[2:], 16)
        return str.__new__(cls, value.lower())

class Return:
    def __init__(self, value):
        self.calldata = value

A, B, C, X = [Address('0x' + x * 40) for x in '1234']
identity = lambda fn: fn
fake = types.ModuleType('genlayer')
gl = types.SimpleNamespace(Contract=object, message=types.SimpleNamespace(sender_address=A),
    public=types.SimpleNamespace(write=identity, view=identity),
    vm=types.SimpleNamespace(UserError=UserError, Return=Return), nondet=types.SimpleNamespace())
fake.gl, fake.Address = gl, Address
sys.modules['genlayer'] = fake
spec = importlib.util.spec_from_file_location('contract', Path(__file__).parents[1] / 'contracts/transit_proof.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
RAW = b'\x89PNG\r\n\x1a\nfixture-only-not-a-real-image'
ENC = base64.b64encode(RAW).decode()
HASH = hashlib.sha256(RAW).hexdigest()

class TransitTests(unittest.TestCase):
    def setUp(self):
        self.clock = 1000
        m.now = lambda: self.clock
        gl.message.sender_address = A
        self.c = m.TransitProof()
        self.c.register_shipment('TP-1', B, C, 'SN-42', HASH, 'Keep dry; fragile', 2000, 60, 60)
        self.output = dict(packaging='PASS', physical='PASS', identity='PASS')
        gl.nondet.exec_prompt = lambda *a, **kw: self.output.copy()
        gl.vm.run_nondet_unsafe = self.consensus

    def consensus(self, leader, validator):
        proposed = leader()
        if not validator(Return(proposed)):
            raise UserError('Consensus disagreement')
        return proposed

    def load(self):
        import json
        return json.loads(self.c.get_shipment())

    def custody(self):
        self.c.record_checkpoint('DISPATCH', HASH, 'Packed')
        gl.message.sender_address = B
        self.c.acknowledge_checkpoint()
        self.c.record_checkpoint('ARRIVAL', HASH, 'Delivered')
        gl.message.sender_address = C
        self.c.acknowledge_checkpoint()

    def delivered(self):
        self.custody()
        self.c.submit_delivery(HASH, 'Received for inspection')
        self.clock = 1061

    def test_happy_path_and_finality(self):
        self.delivered()
        self.c.verify_delivery(ENC, ENC)
        self.assertEqual(self.load()['assessment']['verdict'], 'ACCEPTED')
        with self.assertRaises(UserError): self.c.finalize_delivery()
        self.clock = 1122
        gl.message.sender_address = X
        self.c.finalize_delivery()
        self.assertEqual(self.load()['state'], 'FINALIZED')
        with self.assertRaises(UserError): self.c.finalize_delivery()

    def test_roles_and_countersignatures(self):
        gl.message.sender_address = X
        with self.assertRaises(UserError): self.c.record_checkpoint('DISPATCH', HASH, 'x')
        gl.message.sender_address = A
        self.c.record_checkpoint('DISPATCH', HASH, 'x')
        with self.assertRaises(UserError): self.c.acknowledge_checkpoint()
        with self.assertRaises(UserError): self.c.record_checkpoint('ARRIVAL', HASH, 'x')

    def test_hash_binding(self):
        self.delivered()
        with self.assertRaises(UserError): self.c.verify_delivery(base64.b64encode(RAW+b'x').decode(), ENC)

    def test_all_verdicts(self):
        for obs, expected in [({'packaging':'FAIL','physical':'UNKNOWN','identity':'PASS'},'DAMAGED'),
                              ({'packaging':'FAIL','physical':'FAIL','identity':'FAIL'},'ITEM_MISMATCH'),
                              ({'packaging':'PASS','physical':'UNKNOWN','identity':'PASS'},'INCONCLUSIVE')]:
            self.assertEqual(m.verdict(obs), expected)

    def test_schema_rejects_extra_and_invalid(self):
        for value in [None, {}, {'packaging':'PASS','physical':'PASS','identity':'HACK'}, {**self.output,'verdict':'ACCEPTED'}]:
            with self.assertRaises(UserError): m.normalize(value)

    def test_dispute_freeze_and_immutability(self):
        self.custody()
        self.c.raise_dispute('Wet packaging', HASH)
        with self.assertRaises(UserError): self.c.raise_dispute('again', HASH)
        self.c.submit_delivery(HASH, 'Wet')
        with self.assertRaises(UserError): self.c.submit_delivery(HASH, 'Changed')
        with self.assertRaises(UserError): self.c.verify_delivery(ENC, ENC)
        self.clock = 1061
        with self.assertRaises(UserError): self.c.raise_dispute('late', HASH)
        with self.assertRaises(UserError): self.c.finalize_delivery()

    def test_timeout_without_receipt(self):
        self.clock = 2001
        self.c.finalize_delivery()
        self.assertEqual(self.load()['assessment']['verdict'], 'INCONCLUSIVE')

    def test_timeout_after_arrival(self):
        self.custody()
        self.clock = 1061
        self.c.finalize_delivery()
        self.assertEqual(self.load()['assessment']['responsibility'], 'NOT_DETERMINED')

    def test_locked_agreement(self):
        with self.assertRaises(UserError): self.c.register_shipment('new', B, C, 'x', HASH, 'x', 2000, 60, 60)

    def test_independent_validator_rejects_disagreement(self):
        self.delivered()
        def disagree(leader, validator):
            proposed = leader()
            self.output['identity'] = 'UNKNOWN'
            self.assertFalse(validator(Return(proposed)))
            raise UserError('Consensus disagreement')
        gl.vm.run_nondet_unsafe = disagree
        with self.assertRaises(UserError): self.c.verify_delivery(ENC, ENC)
        self.assertEqual(self.load()['state'], 'INSPECTION')

    def test_invalid_image_encoding_and_size(self):
        for encoded in ['!', '', 'a' * 350001, base64.b64encode(b'not image').decode()]:
            with self.assertRaises(Exception): m.photo(encoded, HASH)

    def test_late_checkpoint(self):
        self.clock = 2001
        with self.assertRaises(UserError): self.c.record_checkpoint('DISPATCH', HASH, 'late')

if __name__ == '__main__':
    unittest.main()
