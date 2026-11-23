# Al-Karak soil magnetic screening — open numerical data and reproduction

This repository supports the pre-submission article *Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan* (journal submission version EP14R4; methods/decision-results baseline EP14R3; public site-level data release 23 November 2026).


**Immutable analysis-data snapshot:** [commit `a3d2a2f9ffa04da3f951211d9f59e046b3424eba`](https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility/tree/a3d2a2f9ffa04da3f951211d9f59e046b3424eba). EP14R4 adds the public site-level numerical replay and revised data-availability description; it does not change the EP14R3 mathematical results. This Git commit is a fixed reproducibility reference, not a Zenodo DOI.

## Fully public numerical site data

- [115 historical field/laboratory site records, including the 114 chemical-complete sites](data/AlKarak_2009_Matched_SiteMeasurements_115.csv): four original field readings per site; laboratory magnetic LF/HF readings and mass for AC, AF, BC and BF fractions; recorded chemical elements and original sample identifiers; and an inclusion flag.
- [Column dictionary and interpretation](data/DATA_DICTIONARY.md).
- [Data reuse terms](data/DATA_LICENSE.md).
- [Full source-level replay code](code/reproduce_from_site_measurements.py), which reconstructs **all seven published numerical aggregate files byte-for-byte** from the public site-level values, including zinc target/budget comparisons, metal random references, dependent multi-metal random distributions and both EP14R3 novelty certificates.
- The earlier `derived/` files and generic synthetic-code tests are retained.

The numerical measurements supporting the research are available for direct download without login or data request. No individual site-level quantitative record used for the ranking analysis is withheld. Historical free-text location descriptions and precise GPS entries are omitted to avoid identifying residences; neither is needed to reproduce the numerical results.

## Reproduce results from site measurements

Python 3.10 or newer:

```bash
python code/reproduce_from_site_measurements.py
python run_checks.py
python code/verify_source_free.py --root derived
python code/replay_reported_aggregates.py --root derived
python code/verify_ep14r3_novelty.py
sha256sum -c SHA256SUMS.txt
sha256sum -c derived/SHA256SUMS.txt
```

**Verification evidence:** 115 location records, 114 admitted chemical-complete records, 56 columns in the public numerical data file, 7/7 full aggregate file matches by SHA-256/byte identity, and GitHub Actions checks. The result is a reproduction from historical *site-level numerical observations*, not an independent repeat of field sampling, verification of the original chemical calibration, or a claim of prospective screening performance.

## Main decision findings

For the top-23 recorded zinc target: field MS2D ranking has a strict all-rule preference at each k=19–32; laboratory MS2B has a strict preference at k=41–100. For identical budget support k=27–46, two positive nonincreasing budget-probability policies reverse the preferred ranking. The conservative transition-weight envelope is [3/43,23/43]. These are conditional post hoc comparisons, not a new general theorem or an assertion of instrument superiority.

## Historical measurement method

The original project report abstract says AAS; its Section 3.2.6 and the peer-reviewed article of El-Hasan and Lataifeh (2013), DOI 10.1007/s12665-012-2058-4, document **PerkinElmer ELAN 9000 ICP-MS**. The current methods follow the detailed report and publication. The original instrument export unit, complete dilution history and historical ×1250 processing factor are not independently metrologically certified.

**The journal-template article and supplementary PDFs are not posted to GitHub.** The research article has not been submitted or accepted.

[Source replay audit](docs/SITE_LEVEL_REPLAY_CERTIFICATE.md) · [Data availability](SOURCE_DISCLOSURE.md) · [EP14R3 analysis](docs/EP14R3_RESULTS_AND_METHOD.md) · [Reviewer instructions](docs/REVIEWER_REPRODUCTION.md)
