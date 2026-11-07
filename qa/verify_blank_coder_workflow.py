#!/usr/bin/env python3
"""Verify prospective blank human reviewer materials without claiming review occurred."""
from pathlib import Path
import csv
root=Path(__file__).resolve().parents[1]
read=lambda n:list(csv.DictReader((root/n).open(newline='',encoding='utf-8-sig')))
frozen=read('data/selected_study_gate_matrix_19.csv')
blind=read('human_review/BLIND_HUMAN_CODING_TEMPLATE_19.csv')
adj=read('human_review/ADJUDICATION_TEMPLATE_133.csv')
assert len(blind)==len(frozen)==19
assert len(adj)==19*7
assert [z['ID'] for z in blind]==[z['ID'] for z in frozen]
assert all(z['G'+str(g)]=='' for z in blind for g in range(7))
assert all(z['source_pages_or_table_locators']=='' and z['coder_comments']=='' for z in blind)
assert all(z['status']=='PENDING_HUMAN_REVIEW' and not z['adjudicated_state'] for z in adj)
assert {(z['ID'],z['gate']) for z in adj}=={(z['ID'],'G'+str(g)) for z in frozen for g in range(7)}
print('PASS: prospective human reviewer blank, 19 cases, 133 adjudication cells, 0 invented human assessments')
