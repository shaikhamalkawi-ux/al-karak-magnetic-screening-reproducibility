# Public data and verification boundary

The original Al-Karak soil chemistry and magnetic records remain **restricted**. This repository does **not** distribute sample identifiers, original source worksheets, site-specific values, coordinates, field notes, or investigator communications.

With project-team permission for this aggregate-only release, the repository now includes five **frozen, source-free, derived aggregate tables** in `derived/`, generic exact budget/tie handling code, synthetic examples, and reviewer verification scripts. The aggregate CSVs were not recalculated or revised for this release: their bytes match the scientific working package of 29 October 2026.

A reviewer can check **2,537 exact aggregate arithmetic and internal consistency conditions** with `python code/verify_source_free.py --root derived`, plus the headline comparisons using `python code/replay_reported_aggregates.py`. Public tests also include **904 synthetic arithmetic checks**. These are not independent reproduction of historical raw-data extraction, laboratory calibration or sample-specific limits of detection.

The public material provides numerical transparency at the **aggregate-results level**. Re-running the complete retrospective study from the original site-level cohort still requires custodian-approved data access. The limited release of these summary aggregates is not a general raw-data licence. Contact the corresponding author Marianne Tarun (mtarun@hct.ac.ae) for access requests, subject to custodial approval.

See `docs/REVIEWER_REPRODUCTION.md` for commands, specific claims, file scope and audit limitations.
