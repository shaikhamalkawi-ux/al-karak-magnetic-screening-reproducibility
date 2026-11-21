# Al-Karak magnetic screening — reviewer code and aggregate-only replay

This public repository supports the paper **Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan**.

**Public reviewer link:** https://github.com/shaikhamalkawi-ux/al-karak-magnetic-screening-reproducibility

## Reproduce the publicly checkable results

Python 3.10 or later:

```bash
python -m pip install -r requirements.txt
python run_checks.py
python code/verify_source_free.py --root derived
python code/replay_reported_aggregates.py --root derived
```

The `derived/` directory now contains five *frozen aggregate-only* CSVs from the historical-cohort reanalysis, released with project-team permission. From these, an external reviewer can independently verify **2,537 internal arithmetic/aggregate consistency checks** and the explicitly reported zinc target-size/budget comparisons. Synthetic-code tests add **904 exhaustive small-problem comparisons** and **11 invalid input rejections**. The tests are automatically run in GitHub Actions.

For an exact list of outputs checked, commands, and limitations, see **[Reviewer reproduction instructions](docs/REVIEWER_REPRODUCTION.md)** and [Data disclosure](SOURCE_DISCLOSURE.md).

## Public files

- `code/exact_budget_audit.py` — generic exact tie-aware, finite-cohort budget comparisons.
- `code/test_exact_budget_audit.py` — independent small synthetic tests.
- `code/verify_source_free.py` — exact checks of the released aggregate tables, including random-reference identities.
- `code/replay_reported_aggregates.py` — replay and verify selected headline comparisons from released aggregates.
- `derived/*.csv` — five **aggregate-only** historical outputs, with no individual site records.
- `examples/` — explicitly fictional seven-record example and expected outputs.
- `.github/workflows/verify.yml` — automatic public test execution.

## Important limitation

**Neither the 114 matched Al-Karak site-level records nor original lab/field readings or locations are public.** Aggregate replay is meaningfully more informative than synthetic-code testing alone, but is not complete source-to-publication reproduction. To reproduce the historical data acquisition, matching and measurements, a reviewer would need separately authorized access to original custodial records. Please contact corresponding author **Marianne Tarun (mtarun@hct.ac.ae)** for a request, subject to source-custodian approval.

This public release does **not** authenticate the 1250 spreadsheet processing factor, original soil mg/kg conversions, site-specific detection limits, or prospective instrument superiority. See `SOURCE_DISCLOSURE.md` for scope.

## Citation and software permissions

Please cite the journal article if published. The repository has **no minted DOI**. The public tables are provided for scholarly verification; no public redistribution right in raw data is granted. Any further software licence should be explicitly approved by the project team.

## Alignment with the current manuscript (22 November 2026)

The current **EP12 author-review manuscript** is titled **Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan**. The repository is the public code-and-aggregate release cited in its Data Availability Statement and Supplement. It is not a journal publication or a complete release of the historical site-level data.

The **five frozen CSV files in `derived/` are the only public historical-data outputs here**. They remain byte-for-byte unchanged during this synchronization, as do all analysis and test scripts. The public checks verify internal arithmetic and selected claims from aggregates, not original site measurements or prospective performance. See the [EP12 verification map](docs/EP12_MANUSCRIPT_MAP.md).

A separately named comprehensive certificates archive is **not included** in this public release. It should not be described as an available attachment until an exact authorized copy is archived and verified. The repository has no DOI; the EP12 manuscript is still under author review.
