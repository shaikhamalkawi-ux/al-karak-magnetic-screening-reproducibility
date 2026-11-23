# Al-Karak EP14R2 — Public Data and On-Request Data

**Manuscript status:** author review, not submitted (23 November 2026).
**Repository:** https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility

## Public files available immediately

- `derived/metal_random_reference_t23.csv`: eight-metal-by-budget random-site reference and selected recovery information.
- `derived/zinc_primary_16rule_pointwise_check.csv`: 16 fixed field-score rules, full budget axis, aggregate zinc bounds.
- `derived/zinc_target_sensitivity_16rules.csv`: alternative chemical upper-tail targets, budget-window sensitivity.
- `derived/nominal_overlap_histogram.csv`: aggregated 0–8-metal site-membership histogram, no site identifiers.
- `derived/nominal_eight_metal_dependent_random_reference.csv`: within-cohort dependent random reference.
- `code/` and `run_checks.py`: generic methods, deterministic verifiers, and arithmetic replay.
- `examples/`: synthetic records and expected outcomes; not historical source data.
- `requirements.txt`, `derived/SHA256SUMS.txt`, `SHA256SUMS.txt`, and GitHub Actions workflow: reproducibility metadata and integrity checks.

## Original data available for an authorized request

The source investigators' 114-site soil chemical and field/laboratory magnetic data, individual observations, worksheets, coordinates, site identities, and calibration details are not included here. A request for controlled scientific review can be directed to corresponding author **Marianne Tarun (mtarun@hct.ac.ae)**. Any inspection or transfer requires permission from the historical data custodians and compliance with applicable data-sharing restrictions. **No automatic release or permission for public redistribution is implied.**

## What can be reproduced

From the frozen aggregate files: specified top-tail and budget-based arithmetic, selected zinc tie-aware counts, dependent random-site reference calculations, and synthetic algorithm tests. The public repository **cannot** independently re-create original individual measurements, site joins, assay quality controls, or prospective performance.

## Manuscript language

> Publicly available research materials, including generic analysis and verification code, synthetic examples, and five aggregate-level data tables supporting the reported arithmetic checks, are available at https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility. These materials support reproducibility of the publicly released aggregate calculations but do not contain the original site-level magnetic and chemical measurements or independently reproduce their laboratory calibration. Additional original site-level records may be requested from the corresponding author; access is considered on request and is subject to permission from the historical data custodians and applicable data-sharing conditions. The public repository does not imply unrestricted access to or permission to redistribute the original records.

**No scientific source measurements, code algorithms, or aggregate CSV values were changed for EP14R2.**
