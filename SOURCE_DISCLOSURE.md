# Public availability of the Al-Karak numerical source dataset

The complete numerical measurements used for the EP14R3 within-cohort ranking analysis are **publicly available** at [data/AlKarak_2009_Matched_SiteMeasurements_115.csv](data/AlKarak_2009_Matched_SiteMeasurements_115.csv). The data file contains 115 historical site records; 114 have matched magnetic and chemical values and form the analysed cohort. Each record includes four field MS2D readings, laboratory magnetic measurements with mass normalizations, original numbered sample IDs, recorded chemistry values (including the eight primary and additional studied elements), and an inclusion flag.

The independent Python [source-replay program](code/reproduce_from_site_measurements.py) reconstructs all five original frozen aggregate CSVs plus the two additional EP14R3 aggregate certificates **byte-for-byte** from the site measurements. Original aggregate tables and their hashes have not been altered. The public GitHub release includes a data dictionary, code, examples, source-check documentation and QA.

Historical location field notes include references to identifiable residences; precise GPS and free-text location descriptions are not copied into the public numerical file. These are not inputs to the manuscript's retrieval calculations.

This public release enables direct numerical reproduction without requesting data from the corresponding author. It is not independent authentication of original analytical instrument exports, laboratory detection limits, the historic concentration-unit conversion or a new field validation. The final project's detailed chemistry methods and the 2013 published article report PerkinElmer ELAN 9000 ICP-MS; an earlier report abstract mentions AAS.

The full MDPI manuscript and supplementary PDF, including the journal LaTeX template, are held in the separate editorial submission package and are not published in this repository.
