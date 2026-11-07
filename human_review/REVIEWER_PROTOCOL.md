# Prospective blinded human coding protocol (NOT EXECUTED)

**Purpose**: prepare an auditable independent human check of the report-level G0–G6 evidence coding; the original 19×7 matrix remains frozen. This file does not claim that independent human coding has occurred.

Two human reviewers should independently inspect original source material, not the already filled `data/selected_study_gate_matrix_19.csv` (do not provide the baseline table until the first pass is submitted). A blinded coordinator should prepare and timestamp two identical copies of `BLIND_HUMAN_CODING_TEMPLATE_19.csv`. A DOI or paper URL is not sufficient by itself to admit a source-only statement: cite a table, figure, page or direct section.

## Gate definitions and coding options

- **G0 — task provenance**: authentic HE learners, actual assessed task, original response/document.
- **G1 — reference standard**: actual rubric or grading system, human/multiple-rater reference and grade scale.
- **G2 — clean-score evidence**: source-reported comparison/error/calibration/discrimination and human reference uncertainty at the source unit.
- **G3 — grade decision evidence**: exact bands, thresholds or actual mark contribution; distinguish retrospective band comparison from released university award in text.
- **G4 — answer-side attack effect**: student-controlled instruction within an assessed artifact, holding the task/rubric/model sufficiently fixed; distinguish attack attempt from measured model response shift.
- **G5 — defended clean work**: paired clean and attacked performance under a protection mechanism, with applicable reference controls, not merely fewer successful attacks.
- **G6 — recourse outcome**: type of flag, simulated substitution, official request, changed mark, and whether final correction was independently adjudicated; only full matched corrected-award evidence could justify a complete correction claim.

For each gate code exactly one: `O` (source-observed scoped endpoint), `P` (partial proxy), `NR` (not reported/tested), `NA` (design inapplicable), `U` (cannot verify at accessible source depth). Every `O`/`P` requires a page/table locator and a bounded interpretation. Do not substitute absence of reporting for absence of practice.

## Proposed workflow (future, no human results yet)

1. Independently examine all 19 originals, record `G0`–`G6` plus evidence locators and a submission timestamp. Record full-text inaccessible cases as `U` where appropriate.
2. Seal two individual coding files before sharing any previous classifications. Preserve pre-adjudication raw agreement; compute overall and by-gate confusion matrices and an unweighted Cohen kappa where denominators and categories are meaningful. Avoid interpreting κ when extreme prevalence/NA makes it uninformative.
3. Adjudicate disagreements one by one against the original source. Record an explicit reason and any retained HOLD. Do not invent unanimity or call arbitration independent blind coding.
4. Compare to the frozen original matrix as a separate **post-unblinding** analysis. If evidence leads to revisions, record a versioned evidence-change table; do not overwrite the original 19×7 baseline silently.

**Status:** `NOT_EXECUTED`; no independent human screen, inter-rater reliability, adjudicated coding table or final source-eligibility universe is claimed by the public release.
