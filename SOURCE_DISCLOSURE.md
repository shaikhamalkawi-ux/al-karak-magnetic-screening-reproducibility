# Public availability of the Al-Karak numerical source dataset

The complete numerical measurements used for the EP14R3 within-cohort ranking analysis are **publicly available** at [data/AlKarak_2009_Matched_SiteMeasurements_115.csv](data/AlKarak_2009_Matched_SiteMeasurements_115.csv). The data file contains 115 historical site records; 114 have matched magnetic and chemical values and form the analysed cohort. Each record includes four field MS2D readings, laboratory magnetic measurements with mass normalizations, original numbered sample IDs, recorded chemistry values (including the eight primary and additional studied elements), and an inclusion flag.

The independent Python [source-replay program](code/reproduce_from_site_measurements.py) reconstructs all five original frozen aggregate CSVs plus the two additional EP14R3 aggregate certificates **byte-for-byte** from the site measurements. Original aggregate tables and their hashes have not been altered. The public GitHub release includes a data dictionary, code, examples, source-check documentation and QA.

Historical location field notes include references to identifiable residences; precise GPS and free-text location descriptions are not copied into the public numerical file. These are not inputs to the manuscript's retrieval calculations.

This public release enables direct numerical reproduction without requesting data from the corresponding author. It is not independent authentication of original analytical instrument exports, laboratory detection limits, the historic concentration-unit conversion or a new field validation. The final project's detailed chemistry methods and the 2013 published article report PerkinElmer ELAN 9000 ICP-MS; an earlier report abstract mentions AAS.

The full MDPI manuscript and supplementary PDF, including the journal LaTeX template, are held in the separate editorial submission package and are not published in this repository.

## EP14R6 source-to-policy-class evidence

The same publicly released 115 historical site rows (114 included in the ranked analysis) now additionally reproduce the strict high-first four-reading field-class audit using `code/verify_stratified_no_go.py`, and a separate within-site order-statistic sensitivity using `code/verify_sorted_readings_no_go.py`. Outputs are in `results/` and a verified source-provenance note is in `docs/EP14R6_POLICY_AND_PROVENANCE.md`. No chemical calibration or new sites were inferred. The original five plus two aggregate-source tables are byte-identical to the previous release. The research manuscript/MDPI template remain outside this public repository.
