# TransitProof

A standalone GenLayer Intelligent Contract for **shipment condition assessment** using committed dispatch and arrival photographs, transaction-authenticated custody checkpoints and independent multimodal validator evaluation.

One shipment per deployment. No frontend, external wallet connection, escrow, payouts or liability determination. Deploy and interact using GenLayer Studio's built-in accounts.

## What it does

Locks the shipment serial, parties, dispatch photo hash, handling text and deadlines. The fixed three acceptance conditions are intact packaging, no visible physical damage, and correct serial-numbered item. Each custody transfer requires a proposal from the outgoing custodian and a countersignature by the incoming custodian. The arrival photo hash is committed by the carrier and acknowledged by the recipient before inspection submission.

After inspection closes, the contract checks uploaded photo bytes against both commitments. The leader and validators independently inspect those same images with `gl.nondet.exec_prompt(images=..., response_format='json')`. A custom `gl.vm.run_nondet_unsafe` validator compares all three normalized observations, rejecting malformed responses and disagreements. The verdict is derived deterministically, never chosen by a privileged caller.

| Observation | Result |
| --- | --- |
| Arrival identity clearly differs | `ITEM_MISMATCH` |
| Packaging or physical condition fails | `DAMAGED` |
| All three conditions positively supported | `ACCEPTED` |
| Any unresolved condition, with no demonstrated failure | `INCONCLUSIVE` |

Identity mismatch takes precedence over damage. All condition observations remain visible in the assessment. Every assessment has `responsibility: NOT_DETERMINED` and `authenticity: NOT_ESTABLISHED`.

## Run checks

Python 3.12+; no dependencies required for the local behavior suite:

```sh
python -m unittest discover -s tests -v
python -m py_compile contracts/transit_proof.py examples/prepare_photos.py
```

The tests execute the actual contract source with a small mocked GenLayer host. They cover roles, custody order, deadlines, immutable commitments, byte/hash binding, response schema, all verdicts, missing-evidence timeouts, finalization and independent-validator disagreement. They do **not** emulate GenVM storage, network consensus, signatures or real image understanding. See [deployment status](docs/DEPLOYMENT.md) for observed live verification.

## Deploy and demonstrate

See [the complete Studio walkthrough](docs/DEMO.md). Import `contracts/transit_proof.py` into [GenLayer Studio](https://studio.genlayer.com), select a built-in account, and deploy with **no constructor arguments** in Normal (Full Consensus) mode. Use test GEN from the Studio faucet if needed. Select separate built-in shipper, carrier and recipient accounts for a meaningful provenance demo. The contract permits the same address in multiple roles for a solo demonstration; that does not provide independent witnesses.

```sh
python examples/prepare_photos.py dispatch.jpg arrival.jpg --output photo-arguments.json
```

Use real photos that you have permission to publish. Each image must show the item, packaging and a legible serial; use a collage if needed, but retain original evidence externally. Photos are limited to 350,000 base64 characters each (about 262 KB of bytes). The helper hashes original bytes, not base64 text. Evidence entered in transaction calldata is public. The contract stores hashes and records, not base64 images, in its own state.

## API

| Function | Authorized caller and purpose |
| --- | --- |
| `register_shipment` | Deployer, once; locks agreement |
| `record_checkpoint` | Shipper proposes DISPATCH; carrier proposes ARRIVAL |
| `acknowledge_checkpoint` | Carrier accepts DISPATCH; recipient accepts ARRIVAL |
| `submit_delivery` | Recipient, once during inspection; binds receipt to acknowledged arrival hash |
| `raise_dispute` | Any shipment party during inspection; one per address, maximum three |
| `verify_delivery` | Any party after inspection; committed photo bytes and real AI consensus |
| `finalize_delivery` | Anyone after review delay, or after missing-receipt timeout |
| `get_shipment` | Anyone; complete JSON agreement, custody history, disputes, assessment and audit |

## Boundaries

- Transaction signatures authenticate submitting accounts; there is no arbitrary detached-signature verifier. Countersignatures acknowledge the already committed checkpoint.
- Hashes establish byte integrity, not camera provenance, truth, time of capture or genuine possession. A signature does not prove a photographed condition is real.
- `ACCEPTED` is an assessment of visible conditions in authenticated submissions, not a guarantee of authenticity or hidden condition. Ambiguity or insufficient views must yield `UNKNOWN` observations.
- Dispute attachment hashes are audit commitments only. Their contents are not fetched or visually evaluated in this MVP; reasons are untrusted statements.
- Handling text gives interpretive context to three fixed conditions. This MVP does not evaluate sensor temperature, hidden damage, arbitrary additional conditions, or liability.
- Submitted delivery evidence is immutable. Disputes close before evaluation, so all validators evaluate one frozen record. A failed consensus transaction can be retried with the same committed images; no privileged verdict override exists.
- The application review delay is **not protocol finality**. Consumers must wait for successful network execution and protocol finalization of relevant writes. Protocol appeals remain separate from `raise_dispute`.
- The timeout path records `INCONCLUSIVE`, never automatic acceptance. It is available when no timely receipt exists. A receipt with unavailable AI remains pending; the application does not invent a consensus result.
- Fixed bounds keep the audit small; no amendment, shipment reuse, custody correction, upgrade or adjudicated compensation flow is provided.

## References

- [Image processing](https://docs.genlayer.com/developers/intelligent-contracts/features/image-processing)
- [Transaction context and deterministic time](https://docs.genlayer.com/developers/intelligent-contracts/features/transaction-context)
- [Non-determinism](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)
- [GenLayer Studio](https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio)

MIT licensed. Experimental testnet software; see [security and threat model](docs/SECURITY.md).
