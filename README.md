# Al-Karak magnetic screening — reviewer code and synthetic examples

This public repository supports the paper **Magnetic Soil-Screening Preferences Depend on Chemical Targets and Assay-Budget Range: A Source-Audited Al-Karak Reanalysis**.

**Public reviewer link:** https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility

## What is public

- Generic finite-cohort, exact-tie, assay-budget retrieval code (`code/exact_budget_audit.py`).
- Independent brute-force tests using **synthetic** datasets (`code/test_exact_budget_audit.py`).
- One explicitly fictional seven-record example and expected outputs (`examples/`).
- A source-free checker (`code/verify_source_free.py`) that can evaluate *separately authorized* aggregate inputs; those inputs are **not included** in the public repository.

**No observed Al-Karak site-level data, sample identifiers, coordinates, chemistry or magnetic measurements, original spreadsheets, investigator emails, or unapproved derived aggregate tables are published here.**

## Run the public tests

Python 3.10+ is required.

```bash
python -m pip install -r requirements.txt
python run_checks.py
```

The public checks confirm **904 synthetic exact-arithmetic comparisons**, **11 expected invalid-input rejections**, and both seven-record example cases. The GitHub Actions workflow runs the same commands on new commits. These checks establish only internal software behavior—not the correctness of the historical measurements or an independent regeneration of the cohort-specific paper results.

The seven-record example illustrates that a uniform budget window and one fixed budget can favor different ranking workflows. It is *not* an Al-Karak observation.

## Public scope versus restricted cohort

The original Al-Karak campaign has 115 magnetic sample records and a restricted 114-site matched primary-chemistry subset. Site-level data and some aggregate-derived verification records remain held by the original custodians. A reader may request access through the corresponding author, **Marianne Tarun (mtarun@hct.ac.ae)**, subject to the original data custodians' permission. Access is not guaranteed, and the public files cannot independently regenerate all cohort-specific numbers in the paper.

To verify privately admitted aggregate tables, an authorized researcher can provide the correct inputs to:

```bash
python code/verify_source_free.py --root /path/to/approved/derived
```

The repository deliberately does not include a `derived/` directory. It also does not claim to certify raw chemical unit conversions, sample-specific detection limits, absolute regulatory concentrations, prospective sensor performance, or instrument superiority.

## Citation and license

Please cite the associated journal article if published. This repository currently has **no minted DOI**. The original research data are not licensed for redistribution. No general software reuse license is asserted without author approval.
