#!/usr/bin/env python3
"""Deterministic public-safe checks. No private datasets or API credentials required."""
from __future__ import annotations
import csv, json, pathlib, collections, hashlib, sys
root=pathlib.Path(__file__).resolve().parents[1] / 'data'
read=lambda n:list(csv.DictReader((root/n).open(encoding='utf-8-sig',newline='')))
b=read('selected_study_gate_matrix_19.csv')
s=read('selected_source_register_19.csv')
x=read('selected_19_archive_origin_crosswalk.csv')
e=read('endpoint_event_overlay_19.csv')
c=read('saez_framework_crosswalk_7.csv')
assert len(b)==len(s)==len(e)==19 and len(x)==19
assert [a['ID'] for a in b]==[a['ID'] for a in e]==[a['ID'] for a in s]==[f'SG{k:02d}' for k in range(1,20)]
assert len(set(a['ID'] for a in e))==19
assert all(e[i]['G3_original']==b[i]['G3'] and e[i]['G6_original']==b[i]['G6'] for i in range(19))
assert collections.Counter(z['G3'] for z in b)=={'P':10,'O':4,'NR':4,'NA':1}
assert collections.Counter(z['G6'] for z in b)=={'NR':12,'P':6,'NA':1}
assert sum(1 for z in b for k in range(7) if z[f'G{k}'] in ('O','P','NR','NA','U'))==133
assert len(c)==7
assert all(z['Coding_status']=='SINGLE_ANALYST_INTERPRETIVE_OVERLAY_UNVALIDATED' for z in e)
assert set(z['ID'] for z in e if z['G6_observed_event'] in ['FLAG_ROUTING_ONLY','SIMULATED_HUMAN_SCORE_SUBSTITUTION','REFERENCE_DEPENDENT_DISCREPANCY_TRIGGER','OBSERVED_APPEAL_LINKED_MARK_REVISIONS','OBSERVED_STUDENT_REVIEW_REQUESTS'])=={'SG02','SG03','SG04','SG09','SG17','SG18'}
assert set(z['ID'] for z in e if z['G3_original']=='O' and z['G3_observed_event']=='RETROSPECTIVE_GRADE_BAND')=={'SG05','SG07','SG14'}
assert not any('VERIFIED_CORRECTION' in z['G6_observed_event'] for z in e)
print('PASS: 19 identities, unchanged 133 G0–G6 cells, 7 Saez framework components, 6 G6 partial-event types, single-analyst limitations')
