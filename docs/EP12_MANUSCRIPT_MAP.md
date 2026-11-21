# EP12 manuscript-to-public-repository verification map

**As of 22 November 2026.** The manuscript is under author review and is not reported as accepted or published.

**Title:** Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan

**Repository:** https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility

| Manuscript finding or method | Public file | Verification scope |
| --- | --- | --- |
| 114 admitted matched sites, 8 metals, primary top-23 target | `derived/metal_random_reference_t23.csv` | Aggregate fields and reported denominators; not source-level joins |
| Zinc recovery (at k=23: field 7, lab 4; k=46: field 8, lab 11–12) | `derived/metal_random_reference_t23.csv` | `python code/replay_reported_aggregates.py --root derived` |
| Zinc target-size and 16 field-aggregation-rule comparisons | `derived/zinc_target_sensitivity_16rules.csv`; `derived/zinc_primary_16rule_pointwise_check.csv` | Exact aggregate checks, not independent source regeneration |
| Metal-by-budget random-site reference | `derived/metal_random_reference_t23.csv` | Exact finite-population hypergeometric arithmetic |
| Eight-metal dependent random benchmark | `derived/nominal_overlap_histogram.csv`; `derived/nominal_eight_metal_dependent_random_reference.csv` | Aggregate group-count dynamic programming |
| General exact tie-aware finite-budget method | `code/exact_budget_audit.py`; `code/test_exact_budget_audit.py`; `examples/` | Synthetic algorithm tests |

From the repository root, run:

```bash
python -m pip install -r requirements.txt
python run_checks.py
python code/verify_source_free.py --root derived
python code/replay_reported_aggregates.py --root derived
sha256sum -c derived/SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt
```

**Public data and code permissions:** The existing five aggregate CSVs and generic code were publicly released with the documented project-team permission. They are unchanged by this editorial synchronization. Neither the 114 site-level records nor raw chemistry, magnetic measurements, sample IDs, coordinates, or site notes are public or redistributable from this release.

**Not supplied:** `Supplementary_Data_Exact_Certificates.zip` has not been identified in the inspected EP12 submission package or the current public repository. Claims of its presence must be corrected in the manuscript until the exact archive and release permission can be verified. The public source-free verifier already exists at `code/verify_source_free.py`, but it does not substitute for an unreleased broader certificate archive.

The public materials permit verification of selected mathematical and aggregate results; they do not independently reproduce original laboratory/field data collection, upstream source processing, absolute calibration, or prospective generalization. There is no repository DOI yet.
