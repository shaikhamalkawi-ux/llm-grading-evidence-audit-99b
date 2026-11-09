#!/usr/bin/env python3
"""Reproduce published Cruz et al. (2026) grade-pair descriptive checks.

Input: ORIGINAL (not redistributed) public Zenodo v2 workbook
  https://doi.org/10.5281/zenodo.21823096
  Grading_Metrics_AI_vs_Instructor.xlsx
  expected MD5: 045dc7549d0c5cfb0ef888cbfd99c038

Run: python scripts/replay_cruz_grade_pairs.py --workbook /path/to/Grading_Metrics_AI_vs_Instructor.xlsx

Uses only the Python standard library. Reads the first-row headers and the
GRADE_PROFESSOR / GRADE_GPT score columns of six worksheets. DOES NOT export
student row data or feedback. This is a descriptive replay, NOT an independent
student-level test, causal analysis, or verification of official final awards.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

MD5 = "045dc7549d0c5cfb0ef888cbfd99c038"
SHA256 = "881f2151e3ca70685f042dfda06b1c41e925e5c4b87e9ea4a59f7bf6d6bcac0a"
EXPECTED_CASE_COUNTS = [64, 59, 64, 63, 59, 53]
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PNS = "http://schemas.openxmlformats.org/package/2006/relationships"
TAG = lambda name: f"{{{NS}}}{name}"


def xlsx_worksheets(path: Path):
    with ZipFile(path) as z:
        book = ET.fromstring(z.read("xl/workbook.xml"))
        rel = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        targets = {node.attrib["Id"]: node.attrib["Target"] for node in rel if node.tag == f"{{{PNS}}}Relationship"}
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(TAG("si")):
                shared.append("".join((s.text or "") for s in si.iter(TAG("t"))))
        for sheet in book.findall(f"{TAG('sheets')}/{TAG('sheet')}"):
            name = sheet.attrib["name"]
            if not re.fullmatch(r"case[1-6]", name):
                continue
            rid = sheet.attrib[f"{{{RNS}}}id"]
            target = targets[rid].lstrip("/")
            if not target.startswith("xl/"):
                target = "xl/" + target
            target = target.replace("xl/xl/", "xl/")
            root = ET.fromstring(z.read(target))
            rows = []
            for row in root.findall(f"{TAG('sheetData')}/{TAG('row')}"):
                fields = {}
                for cell in row.findall(TAG("c")):
                    col = re.match(r"[A-Z]+", cell.attrib.get("r", ""))
                    if not col:
                        continue
                    pos = col.group(0)
                    kind = cell.attrib.get("t", "")
                    v = cell.find(TAG("v"))
                    if kind == "inlineStr":
                        inline = cell.find(TAG("is"))
                        val = "".join(x.text or "" for x in inline.iter(TAG("t"))) if inline is not None else ""
                    elif kind == "s":
                        val = shared[int(v.text)] if v is not None and v.text else None
                    elif v is None or v.text is None:
                        val = None
                    elif kind in ("str", "e"):
                        val = v.text
                    else:
                        val = float(v.text)
                    fields[pos] = val
                rows.append(fields)
            yield name, rows


def read_pairs(path: Path):
    pairs = []
    counts = {}
    ids_seen = Counter()
    for name, rows in xlsx_worksheets(path):
        if not rows:
            raise ValueError(f"Empty sheet {name}")
        header = {str(value): col for col, value in rows[0].items() if value is not None}
        for required in ("ID", "GRADE_PROFESSOR", "GRADE_GPT"):
            if required not in header:
                raise ValueError(f"Missing column {required} in {name}")
        count = 0
        for row in rows[1:]:
            p, a = row.get(header["GRADE_PROFESSOR"]), row.get(header["GRADE_GPT"])
            if p is None and a is None:
                continue
            if p is None or a is None:
                raise ValueError(f"Only one grade in {name}, row {count+2}")
            p, a = float(p), float(a)
            if not math.isfinite(p) or not math.isfinite(a):
                raise ValueError(f"Nonfinite grade in {name}")
            label = str(row.get(header["ID"]))
            # Case ID, not bare label, is the row-level key; labels can recur across sheets.
            ids_seen[label] += 1
            pairs.append((p, a))
            count += 1
        counts[name] = count
    if [counts.get(f"case{i}") for i in range(1, 7)] != EXPECTED_CASE_COUNTS:
        raise ValueError(f"Unexpected source case counts: {counts}")
    return pairs, counts, {k: v for k, v in ids_seen.items() if v > 1}


def calculate(pairs):
    n = len(pairs)
    if n < 3:
        raise ValueError("Need >=3 paired rows")
    ps = [p for p, _ in pairs]
    ys = [a for _, a in pairs]
    ds = [a-p for p, a in pairs]
    g = (sum(ps) + sum(ys)) / (2*n)
    ssr = 2*sum(((p+a)/2-g)**2 for p, a in pairs)
    ssc = n*((sum(ps)/n-g)**2+(sum(ys)/n-g)**2)
    sst = sum((x-g)**2 for x in ps+ys)
    sse = sst-ssr-ssc
    msr, msc, mse = ssr/(n-1), ssc, sse/(n-1)
    # ICC(A,1) / two-way absolute agreement, single-measure, two fixed raters.
    icc = (msr-mse)/(msr+mse+(2/n)*(msc-mse))
    return {
        "n_paired_submissions": n,
        "within_half_point": sum(abs(d) <= .5 for d in ds),
        "outside_half_point": sum(abs(d) > .5 for d in ds),
        "at_least_0_8_discrepancy": sum(abs(d) >= .8 for d in ds),
        "greater_than_0_8_discrepancy": sum(abs(d) > .8 for d in ds),
        "mae": sum(abs(d) for d in ds) / n,
        "signed_bias_ai_minus_instructor": sum(ds) / n,
        "icc_2_1_absolute_agreement": icc,
    }


def validate_reported(o):
    expected = {
        "n_paired_submissions": 362,
        "within_half_point": 302,
        "outside_half_point": 60,
        "at_least_0_8_discrepancy": 11,
        "mae": 0.3069751381215469,
        "signed_bias_ai_minus_instructor": -0.1559622467771638,
        "icc_2_1_absolute_agreement": 0.4888536273784712,
    }
    for name, v in expected.items():
        if not math.isclose(o[name], v, rel_tol=1e-10, abs_tol=1e-11):
            raise AssertionError(f"Unexpected {name}: {o[name]} vs {v}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workbook", type=Path, required=True, help="Original Zenodo v2 .xlsx (NOT in this repository)")
    ap.add_argument("--output", type=Path, help="Optional aggregate-only JSON output")
    args = ap.parse_args()
    original = args.workbook.read_bytes()
    sha, md5 = hashlib.sha256(original).hexdigest(), hashlib.md5(original).hexdigest()
    if md5 != MD5 or sha != SHA256:
        raise ValueError("Workbook is NOT the source-locked original Zenodo v2 workbook (MD5/SHA-256 mismatch)")
    pairs, case_counts, repeated = read_pairs(args.workbook)
    m = calculate(pairs)
    validate_reported(m)
    out = {
        "source": "Cruz et al. (2026) original public Zenodo v2 grade-pair workbook",
        "source_doi": "10.5281/zenodo.21823096",
        "source_file": args.workbook.name,
        "source_md5": md5,
        "source_sha256": sha,
        "case_counts": case_counts,
        "repeated_labels_across_sheets_count": len(repeated),
        "repeated_labels_not_exported": True,
        "metrics": m,
        "status": "PASS_SOURCE_V2_DESCRIPTIVE_REPLAY",
        "limits": "Instructor benchmark only; one institution, 66 students and 362 submissions; case-local IDs cannot establish cross-case learner link; grade-threshold review rule requires instructor marks; no corrected official awarded grade result, significance test, or transport claim.",
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
