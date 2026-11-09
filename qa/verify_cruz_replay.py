#!/usr/bin/env python3
"""Test Cruz public replay parser on synthetic OOXML; compare public aggregate fingerprint.

This is software QA, not reanalysis of human student data. Full source replay must
be run separately with the original, checksum-pinned Zenodo v2 workbook.
"""
from __future__ import annotations
import importlib.util
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.sax.saxutils import escape
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'scripts'/'replay_cruz_grade_pairs.py'
spec = importlib.util.spec_from_file_location('cruzreplay', SRC)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

N = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'

def doc_rows(k, count):
    s = ['<row r="1"><c r="A1" t="inlineStr"><is><t>ID</t></is></c>'
         '<c r="B1" t="inlineStr"><is><t>GRADE_PROFESSOR</t></is></c>'
         '<c r="C1" t="inlineStr"><is><t>GRADE_GPT</t></is></c></row>']
    for i in range(1, count+1):
        label = f'DUP_{i}' if k in (1,2) and i in (1,2,3) else f'case{k}_synthetic_{i}'
        prof = 2.75+((i+2*k)%7)*0.125
        ai = prof + ((i+k)%5-2)*0.125
        s.append(f'<row r="{i+1}"><c r="A{i+1}" t="inlineStr"><is><t>{escape(label)}</t></is></c>'
                 f'<c r="B{i+1}"><v>{prof}</v></c><c r="C{i+1}"><v>{ai}</v></c></row>')
    return '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+''.join(s)+'</sheetData></worksheet>'

with TemporaryDirectory() as tmp:
    p = Path(tmp)/'synthetic_test_only.xlsx'
    with ZipFile(p,'w') as z:
        book = '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
        book += ''.join(f'<sheet name="case{k}" sheetId="{k}" r:id="rId{k}"/>' for k in range(1,7))
        book += '</sheets></workbook>'
        z.writestr('xl/workbook.xml',book)
        rel='<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        rel+=''.join(f'<Relationship Id="rId{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{k}.xml"/>' for k in range(1,7))
        rel+='</Relationships>'
        z.writestr('xl/_rels/workbook.xml.rels',rel)
        for k,count in enumerate(mod.EXPECTED_CASE_COUNTS,1):
            z.writestr(f'xl/worksheets/sheet{k}.xml',doc_rows(k,count))
    pairs, cases, dups=mod.read_pairs(p)
    assert len(pairs)==362 and list(cases.values())==mod.EXPECTED_CASE_COUNTS
    assert len(dups)==3 and set(dups)=={'DUP_1','DUP_2','DUP_3'}
    o=mod.calculate(pairs)
    assert o['n_paired_submissions']==362 and math.isfinite(o['icc_2_1_absolute_agreement'])

results=json.loads((ROOT/'results/cruz_replay_aggregate_only.json').read_text())
assert results['source_md5']==mod.MD5 and results['source_sha256']==mod.SHA256
assert results['status']=='PASS_SOURCE_V2_DESCRIPTIVE_REPLAY'
mod.validate_reported(results['metrics'])
assert results['case_counts']=={f'case{k}':cnt for k,cnt in enumerate(mod.EXPECTED_CASE_COUNTS,1)}
assert results['repeated_labels_across_sheets_count']==3
print('PASS: synthetic .xlsx parser/ICC test; authentic Zenodo-v2 aggregate output fingerprint verified; original row-level workbook NOT packaged')
