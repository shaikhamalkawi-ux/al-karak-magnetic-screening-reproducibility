# Public data and verification boundary

The original Al-Karak soil chemistry and magnetic records remain **restricted**. This repository does **not** distribute sample identifiers, original source worksheets, site-specific values, coordinates, field notes, or investigator communications.

With project-team permission for this aggregate-only release, the repository now includes five **frozen, source-free, derived aggregate tables** in `derived/`, generic exact budget/tie handling code, synthetic examples, and reviewer verification scripts. The aggregate CSVs were not recalculated or revised for this release: their bytes match the scientific working package of 29 October 2026.

A reviewer can check **2,537 exact aggregate arithmetic and internal consistency conditions** with `python code/verify_source_free.py --root derived`, plus the headline comparisons using `python code/replay_reported_aggregates.py`. Public tests also include **904 synthetic arithmetic checks**. These are not independent reproduction of historical raw-data extraction, laboratory calibration or sample-specific limits of detection.

The public material provides numerical transparency at the **aggregate-results level**. Re-running the complete retrospective study from the original site-level cohort still requires custodian-approved data access. The limited release of these summary aggregates is not a general raw-data licence. Additional site-level source records may be requested through the corresponding author Marianne Tarun (mtarun@hct.ac.ae). Availability is considered on request and remains subject to prior authorization by the source custodians and applicable data-sharing conditions; requests are not automatically approved.

See `docs/REVIEWER_REPRODUCTION.md` for commands, specific claims, file scope and audit limitations.

## EP14R2 availability statement and scope

All files **currently approved for public release** are provided in this GitHub repository, including five aggregate-only derived CSVs, generic analysis and verification scripts, and synthetic test examples. Additional original site-level data are **not** included in that public release and may be requested through the corresponding author only subject to custodian approval. These two access categories must not be conflated. See [EP14R2 data access and verification map](docs/EP14R2_DATA_ACCESS_AND_VERIFICATION.md).

No individual historical sample ID, location, laboratory value, raw worksheet, or proprietary calibration record was added in this documentation update. The public aggregates cannot reproduce the upstream raw-data merge and original calibration.
