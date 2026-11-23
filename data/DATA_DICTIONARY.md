# Al-Karak 2009 historical numerical measurements — data dictionary

File: `AlKarak_2009_Matched_SiteMeasurements_115.csv`. **115 source site rows** sorted by original source sample ID, of which **114 have complete primary field/laboratory magnetic and chemical values**. The only excluded source site is ID 150, with no matched final chemical record; it is retained with `primary_cohort=0`, never imputed.

| Columns | Meaning |
|---|---|
| `sample_id` | Original historical numerical sample identifier, not a person identifier |
| `primary_cohort` | 1 for the 114 admitted site records; 0 for the unmatched source record |
| `historical_land_use` | Source-reported land-use code; spelling and mixed labels retained |
| `field_read_1` through `field_read_4` | Original four Bartington MS2D field readings per location; do not interpret them as independent sites |
| `field_mean_4calc` | Exact unrounded arithmetic mean of the four field readings, primary MS2D ranking score |
| `field_mean_archived` | Average shown in the original field workbook, retained to document source presentation differences |
| `AC_LF_raw`, `AC_HF_raw`, `AC_mass_g` | Original prepared upper-coarse soil laboratory MS2B recorded low/high-frequency readings and mass |
| `AC_LF_per_g`, `AC_HF_per_g` | Mass-normalized recorded MS2B responses; `AC_LF_per_g` is the **laboratory ranking score** |
| `AF_*`, `BC_*`, `BF_*` | Corresponding upper-fine, lower-coarse, lower-fine recorded LF/HF readings, sample mass and mass-normalized responses |
| `Fe_recorded`, `Zn_recorded`, `Ni_recorded`, `Cu_recorded`, `Cr_recorded`, `Cd_recorded`, `Mn_recorded`, `Pb_recorded`, `Co_recorded` | Original source-reported numerical upper-coarse acid-extractable chemical values; the eight primary non-Fe analytes are Zn, Ni, Cu, Cr, Cd, Mn, Pb and Co |
| `V_recorded`, `Ba_recorded`, `Al_recorded`, `As_recorded`, `Se_recorded` | Additional source-reported chemical columns used only in the bounded exploratory extension |
| `THM_recorded` | Historical source-reported THM field; not assumed equal to the arithmetic sum of displayed analytes |
| `*_presentation` and `field_average_presentation` | Alternative historical presentation fields preserved for discrepancy identification; **not the primary chemical or magnetic ranking inputs** |

**Units and data quality:** Magnetic source columns retain historic instrument readings; mass is recorded in grams. The original field workbook describes its field mean with a `×10⁻⁴` notation, while MS2B sheets have another historical scale notation; the study uses **rankings within each instrument** rather than comparing physical magnitudes. The historic chemical values were presented in the source publication as soil ppm, nominal mg/kg for dry solids, from 2 M nitric acid extraction; absolute units, the raw instrument-export unit and the historical 1,250 processing factor have not been independently metrologically reconstructed. Zero-coded source chemical entries can denote below-detection reporting codes and must **not** be treated as measured zero concentrations.

**Exact source-input selection:** Filtering `primary_cohort=1` gives 114 sites. For every of 16 declared field rules, compute the mean of a nonempty subset of four field readings, or their four-reading median. The MS2B comparator is `AC_LF_per_g`. For each metal, define the top-23 highest recorded chemical values, allowing all boundary ties. The Python replay program constructs complete ranking-tie bounds with a **single compatible chemical target set** across each budget window.

The source files used to assemble these numerical rows were the historical field MS2D, MS2B laboratory fractions and final upper-coarse chemical spreadsheets. Non-numeric source notes, personal-location descriptions and precise GPS coordinates were not required by the paper's numerical analysis and are **not** included in this public table.

For exact regenerated outputs run `python code/reproduce_from_site_measurements.py` from the repo root; outputs must match all seven files in `derived/` without any rounding or tolerance.
