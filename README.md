# LLM Grading Evidence Audit — Project 99b

**Public source-to-claim audit and reproducibility materials** for the author-review study *When LLM Grades Become University Decisions: A Source-Critical Review of Grading Validity, Attacks, and Appeals*.

**Current source snapshot: R141-EP1 (22 November 2026)**. The scientific baseline remains the R141 manuscript; EP1 is a typesetting/language/figure-readability revision only. The paper is **NOT SUBMITTED, NOT PEER REVIEWED, NOT ACCEPTED**. The repository does not host the submission-template manuscript or any original third-party scholarly PDFs. See [MANUSCRIPT_STATUS.md](MANUSCRIPT_STATUS.md).

## Current public-source inventory

- The original **19 selected reports × seven G0–G6 questions = 133 fixed source-to-claim annotations** in `data/`. Their gate labels are descriptive evidence availability, not quality/safety scores.
- A source-preserved **111-entry bibliography snapshot**: [metadata CSV](bibliography/source_identity_index_R141_EP1_111.csv) and [author-review bibitems](bibliography/apa_bibitems_R141_EP1_111.tex). The earlier [61-item locator index](bibliography/papers_index_61.csv) is retained as historical metadata, **not** a complete R141 literature list.
- All **10 figures used in the author-review version** as source-exact PNGs under [figures/r141_ep1](figures/r141_ep1), with SVG versions for the five new figures. Figure inventory numbering is archival, not journal figure numbering.
- Frozen **aggregate-only inputs** [FIGURE_R140_AGGREGATE_ONLY.json](data/FIGURE_R140_AGGREGATE_ONLY.json) and [figure renderer](scripts/build_R140_new_figures.py) for the five added figures. These files produce graphics from previously checked counts, **not** a fresh raw-data replay.
- Historical Cruz source-file [replay script](scripts/replay_cruz_grade_pairs.py), source checksum, published-count checks, event overlay and the published-summary controls from the earlier repository version. The original grade-pair Excel workbook is obtained separately from Zenodo v2; no raw student pairs are redistributed.
- Source fingerprints and public-file SHA-256 values in [the manifest](provenance/R141_EP1_public_source_sync_manifest.json).

## How to verify

For the inherited source registers and published-summary checks (Python 3.11+ standard library):

```bash
python qa/run_all.py
```

For the new public-source inventory (metadata and exact archived aggregates, **not** empirical model reproduction):

```bash
python qa/verify_r141_ep1_public_snapshot.py
```

To regenerate the five aggregate-only figures, install optional plotting dependencies from `requirements-figures.txt` and run `python scripts/build_R140_new_figures.py`. The original source-exact images are kept unchanged in the versioned figure directory; numerical content is frozen.

To rerun the Cruz grade-pair checks from the official separate workbook, follow [CRUZ_REPLAY.md](CRUZ_REPLAY.md). An automated synthetic parser smoke test is **not** a substitute for that source-file replay.

## Interpretation and rights

The panel was selected retrospectively and is **not a systematic literature census or an estimate of university-wide grading errors**. A measured score gap is not necessarily an issued university award, and a review request is not independently established correction. Read [CLAIM_BOUNDARIES.md](CLAIM_BOUNDARIES.md).

**No third-party publisher PDFs, protected student response texts, private student scores, credentials, unapproved author manuscript, or MDPI journal-template PDFs are uploaded.** Public visibility is not an open-source reuse grant. Research funding/declarations, author/rights approvals, GitHub license and a permanent repository DOI remain subject to author review; see [LICENSE_STATUS.md](LICENSE_STATUS.md).

For published empirical results, cite the **original investigators** and DOI. For this working code collection, use [CITATION_GUIDANCE.md](CITATION_GUIDANCE.md) and a **specific commit SHA**; do not present a GitHub URL as an archival DOI.
