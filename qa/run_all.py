#!/usr/bin/env python3
"""One-command public reproduction. No network, third-party packages, or student data."""
from __future__ import annotations
from pathlib import Path
import csv,hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
entries=[
 'qa/verify_release.py',
 'qa/verify_cruz_replay.py',
 'scripts/replay_1000_matrix.py',
 'scripts/replay_kerwat_reference_baselines.py',
 'scripts/replay_yang_paired_summary.py',
 'scripts/verify_a40_azad_appeal.py',
 'scripts/verify_attack_endpoint_identity.py',
 'scripts/verify_evalhack_cross_table.py',
]
for ent in entries:
  p=ROOT/ent
  r=subprocess.run([sys.executable,str(p)],cwd=ROOT,capture_output=True,text=True)
  if r.returncode:
    print(f'FAIL {ent} ({r.returncode})\n{r.stdout}\n{r.stderr}',file=sys.stderr)
    sys.exit(r.returncode)
  print(f'PASS {ent}')
# 61 exact bibliographic keys / source locators, no third-party PDF binary.
idx=list(csv.DictReader((ROOT/'bibliography/papers_index_61.csv').open(newline='',encoding='utf-8')))
assert len(idx)==61 and len(set(z['bib_key'] for z in idx))==61
assert all(z['source_url'].startswith('https://') and z['PDF_rehosted']=='NO' for z in idx)
assert not list(ROOT.rglob('*.pdf'))
# Integrity manifest for files which are not computed outputs.
manifest=json.loads((ROOT/'qa/sha256_manifest.json').read_text(encoding='utf-8'))
for path,digest in manifest.items():
  pp=ROOT/path
  assert pp.exists(), path
  assert hashlib.sha256(pp.read_bytes()).hexdigest()==digest, path
print(f'PASS metadata locators={len(idx)}, integrity manifest={len(manifest)}, no copyrighted PDFs packaged')
print('PASS ALL R108 public-safe checks (published-summary arithmetic and descriptive source records)')
