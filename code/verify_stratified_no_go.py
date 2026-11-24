#!/usr/bin/env python3
"""Exact no-solver finite-cohort audit of high-first MS2D site prioritization.

Input: public Al-Karak numerical table, 115 rows, 114 complete, 8 metals, four field readings.
Output: exhaustive k=1..46 Pareto-conforming 23-target, group-matched random
       advantages and chemical cutoff-tie envelope; 114 leave-one-out audits.
No numerical optimizer, probabilistic approximation, or hidden raw data is used.

Conditional on historic site values, source land-use labels, high-first Pareto
consistency, top-23 recorded targets, and within-group random reference.
"""
import csv, hashlib, json, math, sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data'/'AlKarak_2009_Matched_SiteMeasurements_115.csv'
SHA='597e61b5bdeb8b4193f2bf9766fe055bd1787f9a756a89241d99cea65afece1a'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA,'input source differs from audited public data'
ALL=list(csv.DictReader(SOURCE.open(newline='',encoding='utf-8')))
ROWS=[r for r in ALL if r['primary_cohort']=='1']
assert len(ALL)==115 and len(ROWS)==114 and len(ALL[0])==56
METALS=('Zn','Ni','Cu','Cr','Cd','Mn','Pb','Co')

def masks(rows):
    n=len(rows); X=[tuple(int(r[f'field_read_{j}']) for j in range(1,5)) for r in rows]
    pred=[0]*n
    for i in range(n):
        for j in range(n):
            if i!=j and all(X[i][d]>=X[j][d] for d in range(4)) and any(X[i][d]>X[j][d] for d in range(4)):
                pred[j] |= 1<<i
    return pred

def chem_targets(rows,t=23):
    n=len(rows);H=[];B=[];Q=[]
    for metal in METALS:
        c=[F(r[metal+'_recorded']) for r in rows]
        cut=sorted(c,reverse=True)[t-1]
        h=[i for i,x in enumerate(c) if x>cut];b=[i for i,x in enumerate(c) if x==cut]
        H.append(sum(1<<i for i in h));B.append(b);Q.append(t-len(h))
        assert 0<=Q[-1]<=len(b)
    return H,B,Q

def strata(rows,variant):
    orig=[r['historical_land_use'] for r in rows]
    if variant=='six':labels=orig
    elif variant=='four':labels=[x.split(';')[0] for x in orig]
    elif variant=='three':labels=['Agricultral' if x=='Agricultral' else 'Resident' if x=='Resident' else 'HighActivity' for x in orig]
    elif variant=='two':labels=['Agricultral' if x=='Agricultral' else 'Other' for x in orig]
    elif variant=='global':labels=['All']*len(rows)
    else:raise ValueError(variant)
    names=sorted(set(labels));group_masks=[sum(1<<i for i,x in enumerate(labels) if x==g) for g in names]
    sz=[p.bit_count() for p in group_masks];scale=math.lcm(*sz)
    gx={g:i for i,g in enumerate(names)}
    return {'names':names,'mask':group_masks,'size':sz,'scale':scale,'group':[gx[g] for g in labels], 'weight':[scale//v for v in sz]}

def objective(mask,grp,H,B,Q):
    """Return (scaled exact best excess over group-matched random, achievable hits)
    optimizing each metal's cutoff ties *consistently* across both sides at fixed mask.
    """
    counts=[(mask&m).bit_count() for m in grp['mask']]
    coefs=[counts[j]*grp['weight'][j] for j in range(len(counts))]
    scale=grp['scale'];g=grp['group']
    if 'high_group_counts' not in grp:
        grp['high_group_counts']=[[(hh&gm).bit_count() for gm in grp['mask']] for hh in H]
    high_group=grp['high_group_counts']
    excess=0;hits=0
    for m in range(8):
        h=H[m];nh=(mask&h).bit_count();hits+=nh
        excess+=nh*scale-sum(coefs[gg]*high_group[m][gg] for gg in range(len(counts)))
        bv=sorted([((scale if (mask>>j)&1 else 0)-coefs[g[j]],j) for j in B[m]],reverse=True)
        excess+=sum(val for val,j in bv[:Q[m]])
        hits+=sum((mask>>j)&1 for val,j in bv[:Q[m]])
    return excess,hits

def max_optimistic_hits(mask,H,B,Q):
    return sum((mask&H[m]).bit_count()+min(Q[m],sum((mask>>j)&1 for j in B[m])) for m in range(8))

def ideals_at(pred,kmax):
    level={0};n=len(pred)
    for k in range(1,kmax+1):
        nxt=set()
        for s in level:
            for j in range(n):
                bit=1<<j
                if not(s&bit) and not(pred[j]&~s):nxt.add(s|bit)
        level=nxt
        yield k,level

def maximum(level,grp,H,B,Q):
    opt=-10**40;site_mask=None;hits=None
    for s in level:
        d,f=objective(s,grp,H,B,Q)
        if d>opt:opt=d;site_mask=s;hits=f
    return opt,site_mask,hits

def run_main():
    pred=masks(ROWS); assert sum(x.bit_count() for x in pred)==5209
    H,B,Q=chem_targets(ROWS);sigs={key:strata(ROWS,key) for key in ['six','four','three','two','global']}
    ids=[int(r['sample_id']) for r in ROWS]
    budget_rows=[];at23={}
    for k,level in ideals_at(pred,46):
        r={'budget_k':k,'admissible_site_sets':len(level),'max_global_hits':max(max_optimistic_hits(s,H,B,Q) for s in level),'global_expected_fraction':str(F(8*k*23,len(ROWS)))}
        for key in ['six','four','three']:
            d,s,f=maximum(level,sigs[key],H,B,Q)
            r[key]={'best_excess':str(F(d,sigs[key]['scale'])),'best_excess_numerator':d,'denominator':sigs[key]['scale'],'positive_possible':d>0,'strict_no_go':d<0}
            if k==23:at23[key]={'max_excess':str(F(d,sigs[key]['scale'])),'count_ideals':len(level),'witness_sample_ids':[ids[i] for i in range(len(ROWS)) if s>>i&1], 'witness_F':f}
        if k==23:
            assert len(level)==90
            for key in ['two','global']:
                d,s,f=maximum(level,sigs[key],H,B,Q)
                at23[key]={'max_excess':str(F(d,sigs[key]['scale'])),'witness_F':f}
        budget_rows.append(r)
    expected_at23={'six':'-55/14','four':'-1241/322','three':'-985/266','two':'-351/40','global':'-748/57'}
    assert all(at23[k]['max_excess']==v for k,v in expected_at23.items()),at23
    assert all(budget_rows[i-1]['six']['strict_no_go'] and budget_rows[i-1]['four']['strict_no_go'] for i in range(18,37))
    assert all(budget_rows[i-1]['three']['strict_no_go'] for i in range(19,40))
    assert budget_rows[36]['six']['best_excess']=='2/3' and budget_rows[35]['six']['best_excess']=='-1/3'
    # Check one and two exceptions, including source-only witnesses from two independent MILP studies.
    wit1=[8, 21, 31, 44, 45, 46, 55, 56, 57, 58, 64, 69, 75, 76, 77, 88, 91, 93, 105, 106, 111, 112, 141]
    wit2=[8, 19, 21, 44, 46, 55, 56, 57, 58, 64, 69, 73, 75, 77, 88, 91, 93, 103, 105, 106, 112, 140, 141]
    id_index={sid:i for i,sid in enumerate(ids)}
    def evaluate_witness(w):
        s=sum(1<<id_index[i] for i in w)
        exceptions=sum(bool(pred[i]&~s) for i in range(len(ROWS)) if (s>>i)&1)
        d,h=objective(s,sigs['six'],H,B,Q)
        return {'max_excess_vs_stratified_random':str(F(d,sigs['six']['scale'])),'optimistic_hit_count':max_optimistic_hits(s,H,B,Q),'achieving_same_target_hits':h,'strict_priority_exception_count':exceptions}
    ex1=evaluate_witness(wit1);ex2=evaluate_witness(wit2)
    assert ex1['strict_priority_exception_count']==1 and ex1['max_excess_vs_stratified_random']=='45/14'
    assert ex2['strict_priority_exception_count']==2 and ex2['optimistic_hit_count']==38
    individually=[]
    for m in range(8):
        eligibleH=sum(1 for i in range(len(ROWS)) if (H[m]>>i)&1 and pred[i].bit_count()+1<=23)
        eligibleB=sum(1 for j in B[m] if pred[j].bit_count()+1<=23)
        individually.append(eligibleH+min(Q[m],eligibleB))
    assert individually==[7,5,4,1,3,1,3,1]
    assert sum(individually)+8 < F(8*23*23,114) # single exception is insufficient to exceed global chance
    # Delete one site and re-run the exact finite-class test, each time recomputing all chemical top23 targets.
    loo=[]
    for omit in range(len(ROWS)):
        r=ROWS[:omit]+ROWS[omit+1:];pred2=masks(r);H2,B2,Q2=chem_targets(r);g2=strata(r,'six')
        last=None
        for k,lev in ideals_at(pred2,23):
            if k==23:last=lev
        d,s,h=maximum(last,g2,H2,B2,Q2)
        loo.append({'excluded_sample_id':ids[omit],'best_excess_fraction':str(F(d,g2['scale'])),'negative':d<0,'number_of_ideals':len(last)})
    assert len(loo)==114 and all(z['negative'] for z in loo)
    cert={'research_status':'EP14R5 manuscript integration candidate; public numerical source is unchanged','source_sha256':SHA,'sites':114,'source_rows':115,'chemical_metals':list(METALS),'target_size':23,'field4_dominance_pairs':5209,
          'at_budget23':at23,'global_random_hits_expectation':str(F(8*23*23,114)),
          'strict_no_go_corridors':{'six_and_four':'k=18..36','six_four_three_common':'k=19..36','three':'k=19..39'},
          'stratified_no_go_loo_count':sum(x['negative'] for x in loo),'loo_maximum_excess':max((F(x['best_excess_fraction']) for x in loo),default=F(0)).__str__(),
          'exceptions':{'one_site_witness':ex1,'two_site_witness':ex2,'per_metal_individual_eligibility_bound':individually,'one_exception_simple_upper':sum(individually)+8,'minimum_exceptions_to_exceed_stratified_expected':1,'minimum_exceptions_to_exceed_global_uniform_expected':2},
          'claim_boundary':'These exact results are historical-cohort and goal conditional. No external validation, causal or costs claims; no assertion that one or two exceptions are identifiable without knowing chemistry.'}
    out=ROOT/'results';out.mkdir(exist_ok=True)
    (out/'EXACT_STRATIFIED_NO_GO_CERTIFICATE.json').write_text(json.dumps(cert,indent=2,ensure_ascii=False)+'\n')
    (out/'ALL_BUDGET_EXACT_SWEEP.json').write_text(json.dumps(budget_rows,indent=2,ensure_ascii=False)+'\n')
    (out/'LEAVE_ONE_OUT_EXACT.json').write_text(json.dumps(loo,indent=2,ensure_ascii=False)+'\n')
    print('PASS: 90 exact k23 ideals, strict stratified no-go -55/14; 19-budget corridor k18..36; 114/114 leave-one-out; 1/2 exception counterexamples.')
    return cert

if __name__=='__main__':run_main()
