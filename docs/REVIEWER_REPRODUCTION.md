# Reviewer replay for the Al-Karak screening paper

**Current manuscript:** EP14R4 (submission candidate, 24 November 2026), retaining the EP14R3 decision calculations with an openly released site-level numerical dataset. Full numerical site-level field, laboratory and chemistry values are openly available in data/AlKarak_2009_Matched_SiteMeasurements_115.csv (115 rows, of which 114 are chemistry-complete). For fixed data and code, use [commit a3d2a2f9](https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility/tree/a3d2a2f9ffa04da3f951211d9f59e046b3424eba). See [source replay certificate](SITE_LEVEL_REPLAY_CERTIFICATE.md).

**Repository:** https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility

The five previously published aggregate-only tables are preserved byte-for-byte. In addition the full historical **site-level numerical values for analysis** (including original sample IDs, four field readings, laboratory magnetism and recorded chemistry) are now openly released in data/. A second verifier rebuilds the aggregate tables directly from those site measurements. Detailed GPS/landmark remarks are excluded from public release for residential privacy.

## Public source-level numerical replay

On Python 3.10 or later:

```bash
python -m pip install -r requirements.txt
python run_checks.py
python code/verify_source_free.py --root derived
python code/replay_reported_aggregates.py --root derived
python code/reproduce_from_site_measurements.py
python code/verify_ep14r3_novelty.py
```

The generic code checks (synthetic inputs) verify exact tie handling, budget preferences, and invalid input rejection. The **aggregate-data** checks independently recompute, from the publicly released frozen tables:

- The 16 metal-by-budget (`8 metals × k={23,46}`) random-reference records, including exact hypergeometric probability calculations and their interval bounds.
- The 114-budget × 16-aggregation zinc comparison matrix (1,824 pointwise rows).
- The 3 chemical-target sizes × 16 field-reading aggregations × 5 budget choices (240 decision records); exact cross-checks for point budgets 23 and 46 against the pointwise matrix.
- The historical fixed-target zinc results: at `t=23, k=23` field retrieves 7 sites and laboratory retrieves 4; at `k=46` field retrieves 8 and laboratory 11–12 under exact tie sensitivity.
- For the 16 recorded aggregation variants, the summed lab-minus-field outcome over `k=1..46`: `t=23` is field-favoring (limits −53 to −5), `t=12` is unresolved (−34 to +30) and `t=35` is laboratory-favoring (+30 to +67). These are *ranges across the reported configurations*, not confidence intervals.
- The pooled eight-metal random-reference distribution using a 9-bin site-overlap **histogram only**, with a group-count dynamic program and exact expectation/quantiles/tails.

The original aggregate-only replay executes **2,537 deterministic checks**, the EP14R3 checker verifies 114 budget corridor rows and 16 policy rows, and the new direct site-level replay reconstructs all seven published result files byte-for-byte. The synthetic-code tests execute **904 arithmetic comparisons**, reject **11 intentionally malformed inputs**, and use **32 synthetic datasets**. GitHub Actions executes the aggregate replay and the synthetic tests after each change to the repository.

## Source-file inventory

| File | Contents and scope |
|---|---|
| `derived/metal_random_reference_t23.csv` | 8 metals × two fixed assay budgets, exact random-reference fractions |
| `derived/zinc_primary_16rule_pointwise_check.csv` | Zinc lab-minus-field exact-tie bounds for 16 field-reading rules and budgets 1–114 |
| `derived/zinc_target_sensitivity_16rules.csv` | Three chemical-target sizes, five decision windows, and 16 aggregation rules |
| `derived/nominal_overlap_histogram.csv` | Aggregated counts of sites with 0–8 high-metal memberships (no site identities) |
| `derived/nominal_eight_metal_dependent_random_reference.csv` | Exact pooled eight-metal reference probabilities and quantiles |
| `derived/Zinc_AllRule_Budget_Envelope.csv` | EP14R3 derived 114-budget preference certificate |
| `derived/Zinc_Reweighting_16Rules_Certificate.csv` | EP14R3 derived 16-rule reweighting certificate |

`derived/SHA256SUMS.txt` records the archive hashes so the released files can be independently checked with `sha256sum -c derived/SHA256SUMS.txt` (from the repository root). On Windows, one can use `Get-FileHash` and compare to the manifest.

## Limits of the site-level numerical replay

Public numerical site records now permit exact reconstruction of all seven summary tables. The code still cannot independently certify the original ICP-MS calibration, verify each historical sample's below-detection threshold or establish population-level and prospective screening accuracy. GPS/landmark notes are omitted to avoid revealing residential locations. The previously reported aggregate arithmetic and synthetic tests remain available.

The original five aggregate CSVs remain frozen; the MDPI manuscript and supplement PDFs are maintained in the separate submission package.


## Full numerical input

The direct input used by the new `python code/reproduce_from_site_measurements.py` script is `data/AlKarak_2009_Matched_SiteMeasurements_115.csv` (115 rows; 114 analysed). The original, aggregate-only CSV files remain in `derived/`. This site-level release is the relevant starting point for an independent calculation audit. See `data/DATA_DICTIONARY.md` for the instrument support and historical presentation/source discrepancy.
