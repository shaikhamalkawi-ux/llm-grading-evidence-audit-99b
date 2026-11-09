# Reproduce the Cruz et al. (2026) case-specific grade-pair check

The original article is **Cruz, da Silva & Mamede (2026)**, *Computers and Education Open*, DOI [10.1016/j.caeo.2026.100411](https://doi.org/10.1016/j.caeo.2026.100411). The authors' official dataset is [Zenodo record 21823096 (v2)](https://doi.org/10.5281/zenodo.21823096), published 6 August 2026. Download the file **`Grading_Metrics_AI_vs_Instructor.xlsx`** from the official record. This is a third-party research dataset and is **not** repackaged in this repository.

Expected source checksum: `MD5 045dc7549d0c5cfb0ef888cbfd99c038`; `SHA-256 881f2151e3ca70685f042dfda06b1c41e925e5c4b87e9ea4a59f7bf6d6bcac0a`.

Run (Python 3.11+, standard library only):

```bash
python scripts/replay_cruz_grade_pairs.py --workbook /path/to/Grading_Metrics_AI_vs_Instructor.xlsx --output /tmp/cruz_replay_output.json
```

The script **fails closed** for source-checksum mismatch, schema mismatch, case-count mismatch or metric discrepancies against the locked R31 source replay. It reads two aggregate grade fields (`GRADE_PROFESSOR`, `GRADE_GPT`) from six sheets and computes MAE, signed AI minus instructor bias, within-0.5-point count and ICC(A,1) two-way absolute single-measure. Cross-sheet ID reuse is identified but no source IDs are exported. A trigger **strictly greater than 0.8** is checked; no source records happen to equal exactly 0.8, so `>0.8` and `>=0.8` both give 11 for this file. This strict definition matches the official authors' `run_all_stats.py` in Zenodo v2.

The published derived output can be inspected at [`results/cruz_replay_aggregate_only.json`](results/cruz_replay_aggregate_only.json). Its figures were **actually recalculated locally from the checksum-pinned original workbook**, not inferred from an article table. The automated CI runs a synthetic, explicitly nonempirical parser/ICC software test and validates the retained aggregate output; for scientific row-level replay, the user must download the source from Zenodo and run the command above. The CI check is therefore not misrepresented as a full dataset rerun.

**Scientific boundary:** 362 submissions from a reported 66 course students are not 362 independent learners. Official grades remained with the instructor; the 0.8-point discrepancy trigger requires the teacher's own score, and there are no institutional grade amendments in this file. The printed ICC is a descriptive pooled point estimate, with no new student-cluster uncertainty estimate. Do not treat this as a multi-institution generalization, correction rate, causal effect or new LLM experiment.
