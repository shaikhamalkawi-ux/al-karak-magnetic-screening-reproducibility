# Al-Karak magnetic soil screening — source-free verification

This public repository supports the pre-submission manuscript **Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan** (research version EP14R3, 23 November 2026).

## Research outcomes

Among 114 matched historical sites, using the top-23 *recorded zinc* target, the field MS2D ranking is strictly preferred at every budget k=19–32 and laboratory MS2B at every k=41–100, across 16 field aggregation rules and recorded-value ties. On the same feasible budget support k=27–46, two strictly positive, nonincreasing probability policies yield opposite laboratory-minus-field preferences. A conservative mixture-switching weight lies in [3/43,23/43].

These are post hoc, finite-cohort diagnostic results, not new mathematical theory, prospective performance, or operating-cost evidence. [Read the exact bounds and archival source-method comparison](docs/EP14R3_RESULTS_AND_METHOD.md).

## Run tests

```bash
python -m pip install -r requirements.txt
python run_checks.py
python code/verify_source_free.py --root derived
python code/replay_reported_aggregates.py --root derived
python code/verify_ep14r3_novelty.py
sha256sum -c derived/SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt
```

The original **five frozen aggregate-only CSVs** have not changed. This update adds **two derived aggregate-only EP14R3 certificates** and a verifier; the established public checks cover 2,537 arithmetic/consistency conditions and 904 synthetic checks with 11 invalid-input rejections.

No individual site-level readings, sample IDs, coordinates, chemical workbooks or calibration exports are public. Source-level requests go through corresponding author Marianne Tarun (mtarun@hct.ac.ae), subject to the applicable conditions.

The historical final-report abstract mentions AAS; its detailed methods and the 2013 peer-reviewed study instead identify **PerkinElmer ELAN 9000 ICP-MS**. This supports the instrument designation but does not independently certify absolute concentration conversion.

The journal-specific MDPI LaTeX template and pre-submission manuscript/supplement PDFs are maintained in the separate submission package, not posted to this repository. The paper is not submitted and no repository DOI or general software licence is asserted.

[Source and rights boundary](SOURCE_DISCLOSURE.md) · [EP14R3 evidence](docs/EP14R3_RESULTS_AND_METHOD.md) · [Reviewer reproduction](docs/REVIEWER_REPRODUCTION.md)
