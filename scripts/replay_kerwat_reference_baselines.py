#!/usr/bin/env python3
"""Replay no-text grade-band controls from published aggregate label counts.

No student essays, empirical ordering, model outputs, APIs, randomization or
sampling inference are used. All calculated control metrics use exact fractions.
Run without arguments to write the two deterministic aggregate output files.
"""
from __future__ import annotations
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def constant_metrics(counts: dict[int, int], prediction: int,
                     positive: int = 3, negative: int = 2) -> dict[str, Fraction]:
    """Metrics of one fixed grade against aggregate ordered reference counts."""
    if (not counts or any(type(k) is not int or type(v) is not int or v < 0
                          for k, v in counts.items()) or type(prediction) is not int):
        raise ValueError("Grade keys and prediction must be integers; counts must be nonnegative integers")
    n = sum(counts.values())
    if n <= 0:
        raise ValueError("Reference population cannot be empty")
    out = {
        "exact_agreement": Fraction(counts.get(prediction, 0), n),
        "within_one_band": Fraction(sum(v for k, v in counts.items()
                                         if abs(prediction-k) <= 1), n),
        "mae_grade_bands": Fraction(sum(abs(prediction-k)*v for k, v in counts.items()), n),
        "signed_bias_grade_bands": Fraction(sum((prediction-k)*v for k, v in counts.items()), n),
    }
    # Binary metrics only for an exactly two-class reference and in-support prediction.
    support = {k for k, v in counts.items() if v > 0}
    if support == {positive, negative} and prediction in support:
        out["distinction_sensitivity"] = Fraction(prediction == positive)
        out["merit_recall"] = Fraction(prediction == negative)
        out["balanced_accuracy_two_classes"] = (out["distinction_sensitivity"]+out["merit_recall"])/2
    return out


def self_test() -> dict[str, int | str]:
    cases = 0
    # Exhaust all positive count pairs for three adjacent grade pairs, both constants.
    for a in range(3):
        for n_a in range(1, 21):
            for n_b in range(1, 21):
                for pred in (a, a+1):
                    m = constant_metrics({a:n_a, a+1:n_b}, pred, a+1, a)
                    assert m["within_one_band"] == 1
                    assert 0 <= m["exact_agreement"] <= 1
                    assert m["mae_grade_bands"] == 1-m["exact_agreement"]
                    assert m["balanced_accuracy_two_classes"] == Fraction(1,2)
                    cases += 1
    # The unit-tolerance result must not be generalized to a full four-grade spectrum.
    assert constant_metrics({0:1,1:1,2:1,3:1},2)["within_one_band"] == Fraction(3,4)
    assert constant_metrics({2:70,3:44},2)["exact_agreement"] == Fraction(35,57)
    assert constant_metrics({2:70,3:44},2)["mae_grade_bands"] == Fraction(22,57)
    assert constant_metrics({2:70,3:44},3)["signed_bias_grade_bands"] == Fraction(35,57)
    rejected = 0
    for bad in ({}, {2:0}, {2:-1,3:2}, {2:1.5}, {2:True}):
        try:
            constant_metrics(bad,2)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Invalid count input was not rejected")
    return {"status":"PASS", "adjacent_support_cases":cases,
            "four_spectrum_counterexample":1, "fixed_count_checks":3,
            "invalid_inputs_rejected":rejected}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inputs", type=Path, default=Path(__file__).with_name("kerwat_published_inputs.json"))
    ap.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = ap.parse_args()
    raw = args.inputs.read_bytes()
    data = json.loads(raw)
    values = data["grade_values"]
    counts = {values[label]:n for label,n in data["reference_counts"].items()}
    if sum(counts.values()) != data["n_essays"]:
        raise ValueError("Published total and grade-count sum differ")
    if counts != {0:0,1:0,2:70,3:44} or values != {"Fail":0,"Pass":1,"Merit":2,"Distinction":3}:
        raise ValueError("The locked source marginals/scale differ from this analysis record")
    tests = self_test()
    controls = {}
    csv_rows = []
    for label in ("Merit", "Distinction"):
        metrics = constant_metrics(counts, values[label])
        controls[label] = {name:{"fraction":str(v), "decimal":float(v)}
                           for name,v in metrics.items()}
        csv_rows.append({"constant_grade":label, **{k:float(v) for k,v in metrics.items()}})
    result = {
        "source_doi":data["doi"], "input_sha256":hashlib.sha256(raw).hexdigest(),
        "count_unit":data["count_unit"], "reference_counts":data["reference_counts"],
        "n_essays":data["n_essays"], "controls":controls,
        "source_reported_best_configuration":data["reported_best_configuration"],
        "descriptive_differences_only":{
            "constant_Merit_minus_reported_best_exact_percentage_points":
                float(Fraction(70,114)*100 - Fraction("54.4")),
            "constant_Merit_minus_reported_best_within_one_percentage_points":1.8,
            "reported_best_mae_minus_constant_Merit_mae_grade_bands":
                float(Fraction("0.474")-Fraction(44,114)),
            "limitation":"Differences use rounded source values; no paired significance claim, confidence interval or model row reconstruction"
        },
        "interpretation":"Both no-text constants attain unit-tolerance agreement of one only because all observed reference grades are two adjacent bands. Constant Merit has zero Distinction sensitivity; the source best model reports 43.2 percent. These controls are diagnostics, not recommended grading policies.",
        "tests":tests,
        "analysis_status":data["analysis_status"],
        "prohibited_inferences":data["prohibited_inferences"]
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/"kerwat_reference_baseline_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    with (args.output_dir/"kerwat_reference_baselines.csv").open("w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0])); w.writeheader(); w.writerows(csv_rows)
    print(json.dumps(result,indent=2,ensure_ascii=False))


if __name__ == "__main__":
    main()
