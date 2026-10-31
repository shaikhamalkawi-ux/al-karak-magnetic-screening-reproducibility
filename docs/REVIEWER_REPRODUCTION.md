# Reviewer replay for the Al-Karak retrospective screening paper

**Repository:** https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility

This release contains five **aggregate-only derived tables** preserved byte-for-byte from the frozen research outputs of 29 October 2026. They contain *no site identifiers, coordinates, original chemistry or magnetic readings, sampling maps, or sample-level rows*.

## What you can check with no permission or original data

On Python 3.10 or later:

```bash
python -m pip install -r requirements.txt
python run_checks.py
python code/verify_source_free.py --root derived
python code/replay_reported_aggregates.py --root derived
```

The generic code checks (synthetic inputs) verify exact tie handling, budget preferences, and invalid input rejection. The **aggregate-data** checks independently recompute, from the publicly released frozen tables:

- The 16 metal-by-budget (`8 metals × k={23,46}`) random-reference records, including exact hypergeometric probability calculations and their interval bounds.
- The 114-budget × 16-aggregation zinc comparison matrix (1,824 pointwise rows).
- The 3 chemical-target sizes × 16 field-reading aggregations × 5 budget choices (240 decision records); exact cross-checks for point budgets 23 and 46 against the pointwise matrix.
- The historical fixed-target zinc results: at `t=23, k=23` field retrieves 7 sites and laboratory retrieves 4; at `k=46` field retrieves 8 and laboratory 11–12 under exact tie sensitivity.
- For the 16 recorded aggregation variants, the summed lab-minus-field outcome over `k=1..46`: `t=23` is field-favoring (limits −53 to −5), `t=12` is unresolved (−34 to +30) and `t=35` is laboratory-favoring (+30 to +67). These are *ranges across the reported configurations*, not confidence intervals.
- The pooled eight-metal random-reference distribution using a 9-bin site-overlap **histogram only**, with a group-count dynamic program and exact expectation/quantiles/tails.

A complete aggregate-only replay executes **2,537 deterministic checks**. The synthetic-code tests execute **904 arithmetic comparisons**, reject **11 intentionally malformed inputs**, and use **32 synthetic datasets**. GitHub Actions executes the aggregate replay and the synthetic tests after each change to the repository.

## Source-file inventory

| File | Contents and scope |
|---|---|
| `derived/metal_random_reference_t23.csv` | 8 metals × two fixed assay budgets, exact random-reference fractions |
| `derived/zinc_primary_16rule_pointwise_check.csv` | Zinc lab-minus-field exact-tie bounds for 16 field-reading rules and budgets 1–114 |
| `derived/zinc_target_sensitivity_16rules.csv` | Three chemical-target sizes, five decision windows, and 16 aggregation rules |
| `derived/nominal_overlap_histogram.csv` | Aggregated counts of sites with 0–8 high-metal memberships (no site identities) |
| `derived/nominal_eight_metal_dependent_random_reference.csv` | Exact pooled eight-metal reference probabilities and quantiles |

`derived/SHA256SUMS.txt` records the archive hashes so the released files can be independently checked with `sha256sum -c derived/SHA256SUMS.txt` (from the repository root). On Windows, one can use `Get-FileHash` and compare to the manifest.

## What this does **not** reproduce

The five tables are outputs of a historical analysis, not the underlying 114-site raw records. Public replay checks table-to-table consistency, exact arithmetic, and specific reported numerical comparisons, but **cannot independently regenerate the site-level data joins, chemical/magnetic source readings, calibration factors, original sampling timestamps, or the complete upstream analysis from raw measurements**. It must not be cited as an independent laboratory replication or prospective screening validation.

Original restricted records remain with the project data custodians. Requests for controlled source-level review go through the corresponding author, **Marianne Tarun (mtarun@hct.ac.ae)**, subject to the custodians' access decision. No approval of *raw data* redistribution is implied by releasing these aggregates.

No paper, supplementary PDF, or scientific result was modified as part of this reviewer-data release.
