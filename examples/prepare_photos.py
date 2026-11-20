"""Prepare real, consented JPEG/PNG evidence for Studio. Does not upload files."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('dispatch', type=Path)
parser.add_argument('arrival', type=Path)
parser.add_argument('--output', type=Path, default=Path('photo-arguments.json'))
args = parser.parse_args()
result = {}
for name in ('dispatch', 'arrival'):
    raw = getattr(args, name).read_bytes()
    encoded = base64.b64encode(raw).decode()
    if len(encoded) > 350000:
        parser.error(f'{name}: resize photo to under 262 KB')
    result[name + '_sha256'] = hashlib.sha256(raw).hexdigest()
    result[name + '_photo_base64'] = encoded
args.output.write_text(json.dumps(result, indent=2))
print(f'Prepared {args.output}; photos and transaction inputs will be public if submitted.')
