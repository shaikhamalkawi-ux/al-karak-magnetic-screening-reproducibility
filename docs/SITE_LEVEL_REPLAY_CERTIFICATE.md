# Full numerical source-to-aggregate replay certificate

**Public source:** `data/AlKarak_2009_Matched_SiteMeasurements_115.csv`; 115 source rows with 56 columns; 114 admitted complete-case records; one source ID 150 missing matched chemistry and excluded from all published ranking calculations.

**Public procedure:** `python code/reproduce_from_site_measurements.py` (Python standard library only). Reconstructs ranking and tie envelopes independently from the public four-reading MS2D and AC MS2B sample values and the 14 element-specific source values.

**Executed on the source-reviewed local numerical CSV:** 7 out of 7 aggregate tables reproduced with **byte-for-byte identity and matching SHA-256**.

| Published aggregate | SHA-256 |
|---|---|
| `derived/zinc_primary_16rule_pointwise_check.csv` | `01dbeb5feb3ce91cecea7452ecc1a49866f0d89a71a9767d665bfd5d86f21f4d` |
| `derived/zinc_target_sensitivity_16rules.csv` | `ed8edf732497263f410116d629c3281472530419ac0b048957880ac3ceb25af7` |
| `derived/metal_random_reference_t23.csv` | `b45fbdd6323166703f6a00bd9e5e7e785b59675027358ec896327995093bf22f` |
| `derived/nominal_overlap_histogram.csv` | `b3d331eb5704548fc205a11934747e99523c8cff19bc96ec6d939e2f92f5dfb3` |
| `derived/nominal_eight_metal_dependent_random_reference.csv` | `ea567e6f258b6373a47f98379653ece03dff1adfc42bcccb1e5a727b2f5a63ae` |
| `derived/Zinc_AllRule_Budget_Envelope.csv` | `af53d564fe1c528bfdd385a143c41ef8fd0cc4278004c54615de662820a795d8` |
| `derived/Zinc_Reweighting_16Rules_Certificate.csv` | `a382d726702af9cffece2832e365a366b0aca0af297f7965e2bc3cfbab8f7be7` |

The reconstructed outcomes include all-rule zinc strict field support 19–32, strict laboratory support 41–100, and sign-changing budget reweighting over identical support 27–46. The output includes eight-metal individual random reference probabilities and exact dependence-preserving multi-metal random calculations.

This is **complete numerical replay from a public site-level table**, but not an independent remeasurement or validation of the historical sampling network, original absolute chemical calibration, nor a prospective environmental field trial. Those boundaries remain unchanged.
