#!/usr/bin/env python3
"""Source-observation consistency checks ONLY. No model experiments or student data."""
import json
from pathlib import Path
humble={
    "attempt_1":{"trials":9,"changed_and_undisclosed":0,"grade_changed":0},
    "attempt_2":{"trials":9,"changed_and_undisclosed":0,"grade_changed":9},
    "attempt_3":{"trials":9,"changed_and_undisclosed":9,"grade_changed":9},
    "attempt_4":{"trials":9,"changed_and_undisclosed":0,"grade_changed":0},
    "attempt_5":{"trials":18,"changed_and_undisclosed":17,"grade_changed":17},
}
assert sum(v["trials"] for v in humble.values())==54
assert humble["attempt_2"]["grade_changed"]==9
assert humble["attempt_2"]["changed_and_undisclosed"]==0
assert all(v["changed_and_undisclosed"]<=v["grade_changed"]<=v["trials"] for v in humble.values())
assert sum(v["changed_and_undisclosed"] for v in humble.values())==26
assert sum(v["grade_changed"] for v in humble.values())==35
data={"source":"Humble (2026) original publisher article pp.8-12 Table 2; Attempt 2 narrative",
  "unit":"trial repetitions from a single synthetic submission; no independent students",
  "observed_counts_by_attempt":humble,
  "non_pooled_descriptive_checks":{"total_trial_repetitions":54,"grade_changes_in_examined_trials":35,"grade_changes_without_output_disclosure":26},
  "note":"Trial totals are arithmetic QA only, NOT prevalence or inferential ASR estimators; designs non-interchangeable",
  "chiang_boundary":"47% self-reported attempt among consenting survey respondents; no independent attack-success validation",
  "corrected_official_awards":"not established"}
Path(__file__).with_name('A20_attack_endpoint_replay.json').write_text(json.dumps(data,indent=2)+'\n')
print('A20 endpoint arithmetic QA PASS: Humble attack2 changed=9, concealed=0; 54 nonindependent repetitions')
