#!/usr/bin/env python3
"""Recompute EP14R3 source-free results using the original public aggregates."""
import csv
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).resolve().parents[1]/"derived"
def read(n):
    with (root/n).open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))
p=read("zinc_primary_16rule_pointwise_check.csv")
t=read("zinc_target_sensitivity_16rules.csv")
env=read("Zinc_AllRule_Budget_Envelope.csv")
policy=read("Zinc_Reweighting_16Rules_Certificate.csv")
rules={r["aggregation"] for r in p}
assert len(p)==1824 and len(t)==240 and len(env)==114 and len(policy)==16 and len(rules)==16
assert {x["rule"] for x in policy}==rules
counts=dict(FIELD=0,LAB=0,EQUAL=0,UNRESOLVED=0)
for k in range(1,115):
    a=[x for x in p if int(x["k"])==k]
    assert len(a)==16 and {x["aggregation"] for x in a}==rules
    lo=min(int(x["point_min"]) for x in a);hi=max(int(x["point_max"]) for x in a)
    label="FIELD" if hi<0 else "LAB" if lo>0 else "EQUAL" if lo==hi==0 else "UNRESOLVED"
    r=env[k-1]
    assert (int(r["k"]),int(r["all_rule_lower"]),int(r["all_rule_upper"]),r["strict_sign"])==(k,lo,hi,label)
    counts[label]+=1
    if 19<=k<=32:assert label=="FIELD"
    if 41<=k<=100:assert label=="LAB"
assert counts==dict(FIELD=24,LAB=64,EQUAL=5,UNRESOLVED=21)
alo=[];ahi=[];blo=[];bhi=[];tl=[];th=[]
for r in policy:
    x=next(z for z in p if z["aggregation"]==r["rule"] and z["k"]=="27")
    y=next(z for z in t if z["aggregation"]==r["rule"] and z["target_size_t"]=="23" and z["decision"]=="window27_46")
    dl,du=int(x["point_min"]),int(x["point_max"]);wl,wu=int(y["lower"]),int(y["upper"])
    truth={"point27_lower":F(dl),"point27_upper":F(du),"window27_46_lower":F(wl),"window27_46_upper":F(wu),
       "uniform_bound_lower":F(wl,20),"uniform_bound_upper":F(wu,20),
       "front_loaded_conservative_lower":F(30*dl+wl,50),"front_loaded_conservative_upper":F(30*du+wu,50)}
    assert all(F(r[key])==v for key,v in truth.items()),r["rule"]
    assert du<0 and wl>0 and 30*du+wu<0
    alo.append(F(wl,20));ahi.append(F(wu,20));blo.append(F(30*dl+wl,50));bhi.append(F(30*du+wu,50))
    tl.append(F(wl,wl-20*dl));th.append(F(wu,wu-20*du))
assert (min(alo),max(ahi),min(blo),max(bhi))==(F(3,20),F(5,4),F(-57,50),F(-7,50))
assert (min(tl),max(th))==(F(3,43),F(23,43))
print("PASS: 114 budgets, 16 field rules, exact fractions and policy reversal")
