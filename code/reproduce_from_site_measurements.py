#!/usr/bin/env python3
"""Rebuild the five original aggregate certificates and EP14R3 decision tables.

Source: the openly released historical numerical site matrix (115 rows; 114 admitted).
Uses Python standard library only. Reproduces recorded-value rankings rather than
claiming independent validation of absolute concentrations or equipment calibration.
"""
from __future__ import annotations
import csv
import hashlib
import itertools
import math
from fractions import Fraction as F
from pathlib import Path
from collections import Counter, defaultdict

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'AlKarak_2009_Matched_SiteMeasurements_115.csv'
DERIVED=ROOT/'derived'
ORDER=['Zn','Ni','Cu','Cr','Cd','Mn','Pb','Co']
RULES={
'mean_1':(0,), 'mean_2':(1,), 'mean_3':(2,), 'mean_4':(3,),
'mean_12':(0,1),'mean_13':(0,2),'mean_14':(0,3),
'mean_23':(1,2),'mean_24':(1,3),'mean_34':(2,3),
'mean_123':(0,1,2),'mean_124':(0,1,3),'mean_134':(0,2,3),
'mean_234':(1,2,3),'mean_1234':(0,1,2,3),
'median4':None,
}
HEAD_POINT='aggregation,k,point_min,point_max'
HEAD_TARGET='target_size_t,aggregation,decision,lower,upper,classification,chemical_target_allocations'
HEAD_RANDOM='metal,k,N,target_t,field_min,field_max,lab_min,lab_max,uniform_random_expectation,field_tail_upper_at_min,field_tail_lower_at_max,lab_tail_upper_at_min,lab_tail_lower_at_max'
HEAD_HIST='num_high_metals_per_site,number_of_sites'
HEAD_DEP='k,N,num_metals,nominal_top_t_each,field_nominal_incidence,lab_nominal_incidence,uniform_expectation,exact_null_quantile_2p5,exact_null_median,exact_null_quantile_97p5,Pr_random_LE_field,Pr_random_GE_lab'


def lines(rows):return ('\n'.join(rows)+'\n').encode('utf-8')
def fmt_frac(a,b):return str(F(a,b))
def read_rows():
    with DATA.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==115 and len({int(r['sample_id']) for r in rows})==115
    selected=[r for r in rows if r['primary_cohort']=='1']
    assert len(selected)==114 and sum(r['primary_cohort']=='0' for r in rows)==1
    assert all(r['Zn_recorded'] and r['AC_LF_per_g'] for r in selected)
    assert all(abs(sum(float(r[f'field_read_{i}']) for i in (1,2,3,4))/4-float(r['field_mean_4calc']))<1e-9 for r in selected)
    assert all(abs(float(r['AC_LF_raw'])/float(r['AC_mass_g'])-float(r['AC_LF_per_g']))<1e-9 for r in selected)
    return selected

def rule_scores(rows):
    scores={}
    for rule,cols in RULES.items():
        vals={}
        for r in rows:
            x=[float(r[f'field_read_{i}']) for i in range(1,5)]
            if cols is None:
                s=sorted(x);value=(s[1]+s[2])/2
            else:value=sum(x[i] for i in cols)/len(cols)
            vals[int(r['sample_id'])]=value
        scores[rule]=vals
    return scores

def alloc_targets(rows,metal,t):
    vals={int(r['sample_id']):float(r[metal+'_recorded']) for r in rows}
    threshold=sorted(vals.values(),reverse=True)[t-1]
    above={i for i,v in vals.items() if v>threshold}
    boundary=sorted(i for i,v in vals.items() if v==threshold)
    count=t-len(above)
    if math.comb(len(boundary),count)>10000:
        raise ValueError('Too many chemical cutoff assignments; no approximation')
    return [above|set(combo) for combo in itertools.combinations(boundary,count)]

def rank_paths(scores,target):
    groups=defaultdict(list)
    for sid,value in scores.items():groups[value].append(sid)
    minstep=[];maxstep=[]
    for score in sorted(groups,reverse=True):
        group=groups[score];positive=sum(sid in target for sid in group);n=len(group)
        minstep.extend([0]*(n-positive)+[1]*positive)
        maxstep.extend([1]*positive+[0]*(n-positive))
    return list(itertools.accumulate(minstep)),list(itertools.accumulate(maxstep))

def make_profiles(rows,metal,t,field_scores,lab_scores):
    H=alloc_targets(rows,metal,t)
    labpaths=[rank_paths(lab_scores,h) for h in H]
    result={}
    for rule,field in field_scores.items():
        lows=[];highs=[]
        for idx,h in enumerate(H):
            fl,fu=rank_paths(field,h);ll,lu=labpaths[idx]
            lows.append([ll[k]-fu[k] for k in range(114)])
            highs.append([lu[k]-fl[k] for k in range(114)])
        result[rule]={'low':[min(a[k] for a in lows) for k in range(114)],
                      'high':[max(a[k] for a in highs) for k in range(114)],
                      'compatible_low':lows,'compatible_high':highs}
    return result,len(H)

def label(lo,hi):
    return 'LAB' if lo>0 else 'FIELD' if hi<0 else 'EXACT_EQUAL' if lo==hi==0 else 'UNRESOLVED'

def count_bounds(scores,H,k):
    lo=[];hi=[]
    for h in H:
        a,b=rank_paths(scores,h);lo.append(a[k-1]);hi.append(b[k-1])
    return min(lo),max(hi)

def hyper_upper(n,t,k,s):
    return F(sum(math.comb(t,j)*math.comb(n-t,k-j) for j in range(max(0,k-(n-t)),min(k,t)+1) if j>=s),math.comb(n,k))

def quantile(dist,den,p):
    total=0
    for s,c in sorted(dist.items()):
        total+=c
        if F(total,den)>=p:return s
    raise AssertionError('unreachable quantile')

def subset_distribution(hist,k):
    dp=[{} for _ in range(k+1)];dp[0][0]=1;seen=0
    for elem,n in sorted(hist.items()):
        for _ in range(n):
            for j in range(min(k-1,seen),-1,-1):
                for s,nways in list(dp[j].items()):
                    dp[j+1][s+elem]=dp[j+1].get(s+elem,0)+nways
            seen+=1
    den=math.comb(seen,k)
    assert sum(dp[k].values())==den
    return dp[k],den

def nominal_sites(scores,k):return sorted(scores,key=lambda i:(-scores[i],i))[:k]

def make_outputs(rows):
    scores=rule_scores(rows)
    lab={int(r['sample_id']):float(r['AC_LF_per_g']) for r in rows}
    zinc23,nc=make_profiles(rows,'Zn',23,scores,lab)
    assert nc==3
    p=[HEAD_POINT]
    for rule in RULES:
        for k in range(1,115):p.append(f"{rule},{k},{zinc23[rule]['low'][k-1]},{zinc23[rule]['high'][k-1]}")
    result={'zinc_primary_16rule_pointwise_check.csv':lines(p)}
    ts=[HEAD_TARGET]
    for t in (12,23,35):
        resp,nalloc=make_profiles(rows,'Zn',t,scores,lab)
        for rule in RULES:
            for name,L,U in [('point23',23,23),('point46',46,46),('prefix1_46',1,46),('window23_46',23,46),('window27_46',27,46)]:
                lo=min(sum(x[L-1:U]) for x in resp[rule]['compatible_low'])
                hi=max(sum(x[L-1:U]) for x in resp[rule]['compatible_high'])
                ts.append(f'{t},{rule},{name},{lo},{hi},{label(lo,hi)},{nalloc}')
    result['zinc_target_sensitivity_16rules.csv']=lines(ts)
    random=[HEAD_RANDOM]
    for metal in ORDER:
        H=alloc_targets(rows,metal,23)
        for k in (23,46):
            fl,fu=count_bounds(scores['mean_1234'],H,k)
            ll,lu=count_bounds(lab,H,k)
            random.append(f'{metal},{k},114,23,{fl},{fu},{ll},{lu},{F(23*k,114)},{hyper_upper(114,23,k,fl)},{hyper_upper(114,23,k,fu)},{hyper_upper(114,23,k,ll)},{hyper_upper(114,23,k,lu)}')
    result['metal_random_reference_t23.csv']=lines(random)
    memberships={int(r['sample_id']):0 for r in rows}
    for metal in ORDER:
        chem={int(r['sample_id']):float(r[metal+'_recorded']) for r in rows}
        for sid in nominal_sites(chem,23):memberships[sid]+=1
    hist=Counter(memberships.values())
    result['nominal_overlap_histogram.csv']=lines([HEAD_HIST]+[f'{s},{hist.get(s,0)}' for s in range(9)])
    pooled=[HEAD_DEP]
    for k in (23,46):
        field_total=sum(memberships[i] for i in nominal_sites(scores['mean_1234'],k))
        lab_total=sum(memberships[i] for i in nominal_sites(lab,k))
        distrib,den=subset_distribution(hist,k)
        lo=quantile(distrib,den,F(1,40));med=quantile(distrib,den,F(1,2));hi=quantile(distrib,den,F(39,40))
        left=F(sum(v for s,v in distrib.items() if s<=field_total),den)
        right=F(sum(v for s,v in distrib.items() if s>=lab_total),den)
        pooled.append(f'{k},114,8,23,{field_total},{lab_total},{F(k*sum(memberships.values()),114)},{lo},{med},{hi},{left},{right}')
    result['nominal_eight_metal_dependent_random_reference.csv']=lines(pooled)
    env=['k,all_rule_lower,all_rule_upper,strict_sign']
    counts=dict(FIELD=0,LAB=0,EQUAL=0,UNRESOLVED=0)
    for k in range(1,115):
        lo=min(zinc23[r]['low'][k-1] for r in RULES);hi=max(zinc23[r]['high'][k-1] for r in RULES)
        labl='EQUAL' if lo==hi==0 else 'FIELD' if hi<0 else 'LAB' if lo>0 else 'UNRESOLVED'
        counts[labl]+=1;env.append(f'{k},{lo},{hi},{labl}')
    assert counts==dict(FIELD=24,LAB=64,EQUAL=5,UNRESOLVED=21),counts
    result['Zinc_AllRule_Budget_Envelope.csv']=lines(env)
    policy=['rule,point27_lower,point27_upper,window27_46_lower,window27_46_upper,uniform_bound_lower,uniform_bound_upper,front_loaded_conservative_lower,front_loaded_conservative_upper']
    for rule in RULES:
        x=zinc23[rule];dl=x['low'][26];du=x['high'][26]
        wl=min(sum(y[26:46]) for y in x['compatible_low']);wu=max(sum(y[26:46]) for y in x['compatible_high'])
        policy.append(f'{rule},{dl},{du},{wl},{wu},{F(wl,20)},{F(wu,20)},{F(30*dl+wl,50)},{F(30*du+wu,50)}')
    result['Zinc_Reweighting_16Rules_Certificate.csv']=lines(policy)
    return result,counts


def main():
    rows=read_rows();outputs,counts=make_outputs(rows)
    checked=0
    for name,b in outputs.items():
        target=DERIVED/name
        if target.exists():
            match=target.read_bytes()==b
            assert match,('Published aggregate differs from source replay',name)
            print('BYTE PARITY PASS',name,hashlib.sha256(b).hexdigest())
        else:
            print('UNAVAILABLE FOR BYTE PARITY',name,hashlib.sha256(b).hexdigest())
        checked+=1
    assert checked==7
    print('PASS: 115 public numerical source records; 114 included; 7 reconstructed aggregate files; 16 aggregation rules')
    print('A source replay does not independently certify historic raw instrument units or chemical calibration.')

if __name__=='__main__':main()
