# Al-Karak soil magnetic screening — open numerical data and reproduction

This repository supports the pre-submission article *Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan* (current author-review version EP14R6; original paired-budget decision-results baseline EP14R3, source-level public data release EP14R4, and high-first feasibility analysis EP14R5; 25 November 2026).


**Immutable analysis-data snapshot:** [commit `a3d2a2f9ffa04da3f951211d9f59e046b3424eba`](https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility/tree/a3d2a2f9ffa04da3f951211d9f59e046b3424eba). The pinned source-data commit contains the open numerical observations; it predates the subsequently added high-first policy-class code in EP14R6. The EP14R3 paired-budget results and seven source-replayed tables have not changed. This Git commit is a fixed reproducibility reference, not a Zenodo DOI.

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
python code/verify_stratified_no_go.py
python code/verify_sorted_readings_no_go.py
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

## EP14R6: High-first feasibility certificate (new relative to original paired-budget audit)

The fully public Python-standard-library verifier `code/verify_stratified_no_go.py` checks **5,209 strict four-reading ordered dominance pairs**, **90 admissible 23-site sets**, and a maximum **−55/14** eight-metal target incidence excess versus each selected set's source-activity-composition-matched random expected count. The six-/four-group strict negative corridor covers budgets **18–36** and ends at budget 37. A **separate** test `code/verify_sorted_readings_no_go.py` first sorts the four field readings within each site to avoid arbitrary replicate-label alignment, and certifies **5,778** strict order-statistic pairs, **11** admissible 23-site sets, and a maximum **−6**. This sorted test imposes more precedence constraints and thus examines a **smaller, stricter** high-first class; it is not a claim about all magnetic-screening algorithms. These tests are historical and post hoc, not independent field validation or an economic comparison.

The 2011 project final report identifies the **Scientific Research Support Fund (SRSF), grant S/2/02/2008**, and dates sampling **July–September 2009**; the 2013 published original study dates the same field campaign **June–August 2009**. The exact month window is unresolved in the documents, so the author-review manuscript calls it the 2009 campaign and discloses both. HCT APC support does not alter original historical grant attribution.

[Reproducible R6 certificate, exact numbers and boundaries](docs/EP14R6_POLICY_AND_PROVENANCE.md) · [Original source-data SHA snapshot](https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility/tree/a3d2a2f9ffa04da3f951211d9f59e046b3424eba).
