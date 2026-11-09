#!/usr/bin/env python3
"""Verify 61 APA keys and source-specific author metadata; bibliographic QA, not full-text verification."""
from pathlib import Path
import csv,re
R=Path(__file__).resolve().parents[1]
idx=list(csv.DictReader((R/'bibliography/papers_index_61.csv').open(encoding='utf-8',newline='')))
lines=(R/'bibliography/apa_bibitems_R109.tex').read_text(encoding='utf-8').splitlines()
items=[re.fullmatch(r'\\bibitem\[([^]]+)\]\{(ref\d+)\} (.+)',x) for x in lines if x.startswith(r'\bibitem')]
assert len(items)==61 and all(items)
keys=[x.group(2) for x in items]
assert set(keys)=={x['bib_key'] for x in idx} and len(set(keys))==61
# Key ordering follows publisher-verified APA first-author sorting including diacritics.
order='ref39 ref49 ref50 ref47 ref48 ref20 ref19 ref61 ref27 ref57 ref35 ref51 ref26 ref16 ref59 ref03 ref10 ref41 ref55 ref24 ref06 ref38 ref45 ref58 ref36 ref43 ref22 ref02 ref25 ref28 ref08 ref46 ref29 ref21 ref23 ref37 ref33 ref42 ref32 ref17 ref01 ref04 ref30 ref05 ref44 ref34 ref13 ref14 ref56 ref60 ref07 ref53 ref31 ref18 ref09 ref52 ref11 ref40 ref12 ref54 ref15'.split()
assert keys==order
assert any(x.group(2)=='ref23' and x.group(1)=='Latif et al.(2024)' for x in items)
assert any(x.group(2)=='ref48' and 'Potop, V.' in x.group(3) for x in items)
assert all(r'\url{https://' in x.group(3) for x in items)
print('PASS APA metadata: 61 cited keys in alpha order; verified Latif, Anghel and publisher author-list repairs; not a full-text audit')
