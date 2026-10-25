#!/usr/bin/env python3
"""Publish a validated, standalone bundle containing only allowlisted static files."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile


def build(public, personal, destination, outfit):
    merged = json.loads(subprocess.check_output(
        [str(outfit), 'catalog', '--source', str(public), '--personal', str(personal), '--json'],
        stderr=subprocess.PIPE))
    origins = {}
    for prefix, root in [('public', public), ('personal', personal)]:
        data = json.loads((root / 'outfit.yaml').read_text())
        for item in data.get('dotfiles', []):
            origins[item['id']] = (prefix, root)
    files = {}
    for item in merged.get('dotfiles', []):
        prefix, root = origins[item['id']]
        source = root / item['source']
        if not source.resolve().is_relative_to(root.resolve()):
            raise ValueError('Dotfile source escapes its bundle')
        item['source'] = prefix + '/' + item['source']
        files[item['source']] = source.read_bytes()
    merged['name'] = 'John personal profiles (standalone public bundle)'
    files['outfit.yaml'] = (json.dumps(merged, indent=2) + '\n').encode()
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as archive:
        for name, contents in sorted(files.items()):
            info = tarfile.TarInfo(name)
            info.size, info.mode, info.mtime = len(contents), 0o600, 0
            archive.addfile(info, io.BytesIO(contents))
    with destination.open('wb') as output:
        with gzip.GzipFile(fileobj=output, mode='wb', mtime=0, filename='') as compressed:
            compressed.write(stream.getvalue())
    return hashlib.sha256(destination.read_bytes()).hexdigest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public', type=Path, required=True)
    parser.add_argument('--outfit', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', type=Path, default=Path('dist'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    filename = f'outfit-personal_{args.version}.tar.gz'
    digest = build(args.public, Path(__file__).resolve().parents[1], args.output / filename,
                   args.outfit.resolve())
    (args.output / 'SHA256SUMS').write_text(digest + '  ' + filename + '\n')
    print(digest, filename)
