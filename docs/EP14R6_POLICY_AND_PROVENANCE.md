# EP14R6: High-first screening audit, four-replicate ordering, and historical source reconciliation

**Article:** *Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan*.

**State:** EP14R6 editorial and source-provenance closure built from the EP14R5 integrated author-review baseline (25 November 2026). The scientific manuscript and journal template are **not** in this public repository; the journal has **not** been sent this version. Coauthor sign-off on the newly integrated science remains an author-side action.

## Why the added audit matters

The original paired MS2D versus MS2B site-retrieval and tie/assay-budget results remain unchanged. An additional post-hoc **negative feasibility certificate** asks whether any selected-site list in a declared **strict high-first** field policy class can beat the expectation of a stratified random comparator with the same historical activity-label composition. It counts eight metal-target incidences, *not* distinct locations, chemical mass, risk exceedances, economic savings, or future performance.

The class respects precedence when a site's four recorded field readings are all at least as high as another site's, with at least one strictly higher. Historical numerical site-level records (115 rows, 114 included) are public in `data/`.

- Labeled-record columns: 5,209 strict ordered pairs; 90 feasible 23-site sets; exact best excess **−55/14**.
- For the historical six-group or four-group activity composition matching, the best possible excess is negative for **all k=18–36** (target top-23 for each of 8 metals). The six-group maximum becomes **+2/3 at k=37**; this only refutes a universal negative bound, not a prospective effectiveness result.
- Leave one site out: **114/114** held the six-group k23 bound negative, with target redefined within the remaining cohort. Not 114 independent field surveys.
- **Permutation-invariant sensitivity:** Sorting the four local MS2D replicates within each site, then comparing their order statistics, yields **5,778 strict pairs, 11 feasible 23-site sets and best excess −6**, independently recomputed with a second Python program. The order-statistic precedence class is stricter (it contains more pairwise precedence constraints) and thus **smaller** than the original labeled-column selection class. It checks robustness to arbitrary within-site replicate labels; it is **not** an independent calibration or proof about every magnetic-screening rule.

## Inspect and reproduce

From the repository root, Python 3.10+ standard library is enough:

```bash
python code/verify_stratified_no_go.py
python code/verify_sorted_readings_no_go.py
python code/reproduce_from_site_measurements.py
sha256sum -c SHA256SUMS.txt
```

The published `results/` JSONs and Figure 8 CSV are frozen output snapshots. The scripts verify their arithmetic from the publicly released numerical observations. The verifier's proof compares a selected list with the **expectation** of its own activity-composition-matched random design, using one compatible chemical-target tie assignment on both sides. No dataset has been replaced or rounded to obtain these conclusions.

## Historical source differences (reported, not silently repaired)

The original *Environmental Magnetism: Urban Environmental Pollution Monitoring and Assessment Using Magnetic Proxies* final project report (2011, investigators M. S. Lataifeh and T. El-Hasan) identifies **Scientific Research Support Fund (SRSF)**, grant **S/2/02/2008**, for the original project. It reports **July–September 2009** sampling. The later peer-reviewed 2013 article (El-Hasan and Lataifeh, *Environmental Earth Sciences* 69:2299–2310; DOI [10.1007/s12665-012-2058-4](https://doi.org/10.1007/s12665-012-2058-4)) reports **June–August 2009**. The record available here does not independently establish one definitive three-month window. We therefore identify the campaign by **year (2009)** and disclose the unresolved month discrepancy in the manuscript Supplement. This does not involve a time-series analysis.

The project's detailed methods and 2013 publication identify **PerkinElmer ELAN 9000 ICP-MS** for chemical testing, while the original report abstract mentions AAS. Source-supported instrument terminology is not a reconstructed calibration chain; the historical reported unit and dilution history have not been independently certified.

## Explicit limitations

- The strict high-first class does **not** include all historical 16 field-aggregation rules under arbitrary tie breaking, or inverse/nonmonotone/spatially stratified algorithms.
- The four original readings were local replicates, not four documented co-registered geographic directions; column-index matching across sites is an *analytic* sensitivity assumption, not physical alignment evidence.
- Six source activity labels include tiny mixed groups and an original spelling variation; coarsenings reduce dependence on those categories but do not establish ecological or causal validity.
- The target definitions and relevant budget window were explored post hoc in the historical dataset; any external transfer claim requires a genuinely new test campaign.

**Historical numerical data snapshot:** [Git commit a3d2a2f9ffa04da3f951211d9f59e046b3424eba](https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility/tree/a3d2a2f9ffa04da3f951211d9f59e046b3424eba); no Zenodo DOI is claimed. The current (later) code commit can be pinned separately for full EP14R6 replay.
