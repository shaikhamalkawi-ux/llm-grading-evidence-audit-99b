#!/usr/bin/env python3
"""Check R141-EP1 public-source completeness; NOT a new grading experiment.

No dependencies beyond Python 3.9 standard library; verify exact archived labels and
figures and metadata. This is not a full empirical data replay.
"""
from pathlib import Path
from collections import Counter
import csv, json, hashlib
ROOT = Path(__file__).resolve().parent.parent
record = json.loads((ROOT/'data/FIGURE_R140_AGGREGATE_ONLY.json').read_text())
assert record['N1_floden']['discordant'] == [12,19,21,17,6]
assert sum(record['N1_floden']['discordant']) == 75
assert sum(record['N2_human_score_diff']['frequency']) == 1000
assert sum(i * x for i,x in enumerate(record['N2_human_score_diff']['frequency'])) == 1827
assert len(record['N3_matrix']['status_rows']) == 19
assert all(len(row) == 7 for row in record['N3_matrix']['status_rows'])
assert Counter(v for row in record['N3_matrix']['status_rows'] for v in row) == Counter({'O':46,'P':34,'NR':46,'NA':6,'U':1})
assert record['N4_cruz']['counts'] == [[236,66],[29,31]]
assert record['N5_human_thresholds']['total'] == [213,224,249,249,232,196]
with (ROOT/'bibliography/source_identity_index_R141_EP1_111.csv').open(newline='',encoding='utf-8') as f:
    items=list(csv.DictReader(f))
assert len(items) == len({row['citation_key'] for row in items}) == 111
imgs=sorted((ROOT/'figures/r141_ep1').glob('Figure*.png'))
assert len(imgs)==10
assert all(p.stat().st_size > 1000 for p in imgs)
for i in range(1,6):
    assert len(list((ROOT/'figures/r141_ep1/source_svg').glob(f'N{i}_*.svg'))) == 1
manifest=json.loads((ROOT/'provenance/R141_EP1_public_source_sync_manifest.json').read_text())
for name, expected in manifest['public_file_sha256'].items():
    p=ROOT/name
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==expected, name
print(f"PASS: R141-EP1 public snapshot: {len(imgs)} figures, {len(items)} references, 19x7 gates, manifest {len(manifest['public_file_sha256'])} assets")
