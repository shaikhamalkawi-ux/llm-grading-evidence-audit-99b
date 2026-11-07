# LLM Grading Evidence Audit — Project 99b

**Public reproducibility and source-to-claim evidence files** for the author-review manuscript *When LLM Grades Become University Decisions: Evidence Boundaries for Scoring, Attacks, and Appeals* (target journal: *Education Sciences*, MDPI). 

**Status as of 8 November 2026:** scientific author-review; not submitted or accepted. This repository is public for inspection. A permanent archived version/DOI and reuse licences have not yet been author-approved. See [LICENSE_STATUS.md](LICENSE_STATUS.md). This project is **not** an independent human-screened systematic review, a PRISMA census, a field-wide performance estimate, or a deployment test.

## What is actually reproducible here?

- The fixed purposive **19 report identities × 7 G0–G6 reporting gates = 133 cells** and exact source identities; neither study quality nor a university grading safety score.
- A **single-analyst descriptive event-type overlay** distinguishing G3 retrospective grade comparison from deployed LLM-mark use; and G6 review flag / simulation / instructor-referenced trigger / observed appeal-linked mark change / request. **No independently blinded coding or reliability estimate** is claimed.
- Six small, standalone standard-library published-summary arithmetic scripts: EvalHack fixed-routing conditional ceiling, Kerwat restricted-label controls, Yang rounded paired-summary sensitivity, Azad appeals, Humble attack-endpoint semantics, and EvalHack cross-table comparability. These are **not** new LLM grading experiments or original student-level replications.
- A **seven-row source-scoped framework crosswalk** to Saez et al. (2026); complementary questions, **not a demonstrated outperforming framework**.
- A [61-item bibliographic locator index](bibliography/papers_index_61.csv) with authoritative DOI/publisher URLs and the [source-preserved bibliography](bibliography/references_source_preserved.bib). Third-party articles are linked, **not redistributed**.

## Reproduce with Python 3.11+ (no external Python dependencies)

```bash
python qa/run_all.py
```

This prints a per-script `PASS` or fails with a nonzero code. Outputs are deterministic descriptive checks generated from published summary counts. For substantive scientific interpretation, read [CLAIM_BOUNDARIES.md](CLAIM_BOUNDARIES.md) before citing any number.

## Repository files

`data/`: public-safe 19-source register, G0–G6 matrix, A66 archival provenance crosswalk, R106 event overlay, seven-component prior-art crosswalk and event-summary JSON.

`scripts/`: six executed source-specific arithmetic checks plus one published-count Kerwat JSON input; each uses only Python's standard library.

`bibliography/`: 61 source locators and the frozen source-preserved BibTeX notes; no copyrighted article PDFs or protected student responses.

`qa/`: one-command executable verification, blank-review checks, and a SHA-256 manifest check.

`human_review/`: prospective **blank** dual-coder and adjudication templates (not executed; no human reliability statistics fabricated).

## Interpretation and citation

Use the exact source citation for the original empirical study. This repository contains an **audit of published evidence**, not a substitute for reading that study. For the 99b manuscript, an author-approved article citation and repository DOI are **pending**. GitHub alone is not a versioned archival DOI; an immutable release/Zenodo deposit may be prepared after author approval.

Repository URL: https://github.com/shaikhamalkawi-ux/llm-grading-evidence-audit-99b
