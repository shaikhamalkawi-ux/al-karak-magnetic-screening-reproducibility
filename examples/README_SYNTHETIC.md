# Artificial example — not Al-Karak data

Every number in SYNTHETIC_seven_records.csv was constructed for software demonstration.
None is an observed historical measurement. There are seven artificial records and three
high-chemical targets. With higher magnetic score selected first, the uniform budget 1–4
mean difference is −1/4, while the known budget k=4 difference is +1 (laboratory minus field).
The example illustrates an already known ranking phenomenon; it is not validation or a new result.

Run the synthetic-example commands from the repository root:

```bash
python code/exact_budget_audit.py --input examples/SYNTHETIC_seven_records.csv --target 3 --start 1 --end 4 --weights uniform
python code/exact_budget_audit.py --input examples/SYNTHETIC_seven_records.csv --target 3 --start 4 --end 4 --weights uniform
```
