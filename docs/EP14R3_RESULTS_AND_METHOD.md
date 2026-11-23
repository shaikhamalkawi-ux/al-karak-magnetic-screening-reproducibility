# EP14R3: evidence and historical chemical-method clarification

**Research:** *Prioritizing Soil Sites When Chemical Testing Is Limited: A Tie-Aware Decision Audit of Field and Laboratory Magnetic Rankings in Al-Karak, Jordan*. Historical cohort 114 matched sites, eight acid-extractable metals, 16 declared field-score aggregations.

For the 23 top-ranked *recorded zinc* sites define D(k) = recovered target count under laboratory MS2B minus count under field MS2D:

- **Every k=19–32:** field strictly preferred across all 16 field rules and recorded ties, with differences within [−3,−1].
- **Every k=41–100:** laboratory strictly preferred, with differences within [+1,+9].
- All 114 budgets: 24 strictly field, 64 strictly lab, 5 exactly equal and 21 unresolved.
- At k=23, field/lab retrieve 7/4; at k=46, 8/(11–12).
- On the **same budgets k=27–46**: uniform weights 1/20 imply exact lab-minus-field expected-recovery range **[3/20,5/4]**. Weights 31/50 on k=27 and 1/50 on each k=28–46 give conservative range **[−57/50,−7/50]**. Both profiles are nonincreasing and assign positive probability to every budget.
- Across the uniform-to-point-mass mixture each admissible complete tie/rule state has one preference transition, conservatively within **[3/43,23/43]**.

All statements are conditional, post hoc, finite-cohort arithmetic checks. They are not a general new theorem, future performance, or independent field validation. Two aggregate-only results files under `derived/` encode the 114-point corridor and 16-rule policy calculation; run `python code/verify_ep14r3_novelty.py` to check them against the original five frozen public aggregate CSVs.

## AAS versus ICP-MS

The original final project-report **abstract** contains a graphite-furnace AAS description, but its detailed **Section 3.2.6** explicitly names **PerkinElmer ELAN 9000 ICP-MS** at Prince Faisal Center, Mu'tah University, and describes element-specific analyses and replicates. The independently published primary account of the same campaign by El-Hasan and Lataifeh (2013), *Environmental Earth Sciences* 69, 2299–2310 ([DOI:10.1007/s12665-012-2058-4](https://doi.org/10.1007/s12665-012-2058-4)), identifies the same instrument and 2 M nitric-acid extraction. Thus **ICP-MS** is the supported technique for the current article, while the early abstract discrepancy remains acknowledged in the supplement.

The identification does not independently validate the raw output unit, all laboratory dilutions or the historical factor 1,250. All historical site-level numerical observations and original sample IDs supporting the EP14R3 rankings are now publicly released in data/AlKarak_2009_Matched_SiteMeasurements_115.csv; source-level code reproduces all seven derived tables. Precise GPS and household-location remarks are omitted because they are not used in these calculations. Original archival workbook binary files and the MDPI-specific article/ supplement PDFs are not part of this public dataset.
