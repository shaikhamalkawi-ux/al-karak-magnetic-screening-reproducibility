#!/usr/bin/env python3
"""Public reviewer checks that require no original observations or derived tables."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
commands = [
    [sys.executable,'code/test_exact_budget_audit.py'],
    [sys.executable,'code/exact_budget_audit.py','--input','examples/SYNTHETIC_seven_records.csv','--target','3','--start','1','--end','4','--weights','uniform'],
    [sys.executable,'code/exact_budget_audit.py','--input','examples/SYNTHETIC_seven_records.csv','--target','3','--start','4','--end','4','--weights','uniform']
]
for i, cmd in enumerate(commands):
    res = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
    data = json.loads(res.stdout)
    if i==0:
        assert data.get('exact_arithmetic_checks')==904, data
        assert data.get('invalid_inputs_rejected')==11, data
    elif i==1:
        assert data.get('lower')=='-1/4', data
    else:
        assert data.get('lower')=='1', data
    print('PASS:', ' '.join(cmd[1:]))
print('PUBLIC SYNTHETIC REVIEWER CHECKS PASS')
