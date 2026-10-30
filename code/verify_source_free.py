#!/usr/bin/env python3
"""Source-free verifier for private derived aggregates. No site-level records needed."""
from __future__ import annotations
import argparse,csv,itertools,json,math
from fractions import Fraction as Q
from pathlib import Path
from collections import Counter,defaultdict

def read(path):
 with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def hg(n,t,k,a):
 return Q(sum(math.comb(t,j)*math.comb(n-t,k-j) for j in range(a,min(t,k)+1) if 0<=k-j<=n-t),math.comb(n,k))
def grp_dp(hist,k):
 """Group-count expansion ∏_w (1+x*y^w)^multiplicity, independent from sequential DP."""
 cur={(0,0):1}
 for w,c in sorted(hist.items()):
  next=dict()
  for (t,s),v in cur.items():
   for j in range(0,min(c,k-t)+1):
    key=(t+j,s+j*w)
    next[key]=next.get(key,0)+v*math.comb(c,j)
  cur=next
 return {score:v for (chosen,score),v in cur.items() if chosen==k}
def cls(l,u):return 'LAB' if l>0 else 'FIELD' if u<0 else 'EXACT_EQUAL' if l==u==0 else 'UNRESOLVED'
def verify(root):
 rows=read(root/'zinc_target_sensitivity_16rules.csv')
 assert len(rows)==240
 assert {int(r['target_size_t']) for r in rows}=={12,23,35}
 assert len({r['aggregation'] for r in rows})==16
 assert len({r['decision'] for r in rows})==5
 assert len(set((r['target_size_t'],r['aggregation'],r['decision']) for r in rows))==240
 checks=Counter()
 for r in rows:
  l,u=int(r['lower']),int(r['upper']);assert l<=u
  assert r['classification']==cls(l,u)
  checks['zinc_bounds_sign']+=1
 primary=read(root/'zinc_primary_16rule_pointwise_check.csv');assert len(primary)==1824
 assert len(set((r['aggregation'],r['k']) for r in primary))==1824
 pr={(r['aggregation'],int(r['k'])):r for r in primary}
 for r in rows:
  if r['target_size_t']=='23' and r['decision'] in ('point23','point46'):
   k=23 if r['decision']=='point23' else 46
   p=pr[(r['aggregation'],k)]
   assert (p['point_min'],p['point_max'])==(r['lower'],r['upper'])
   checks['primary_point_crosscheck']+=1
 for p in primary:
  assert 1<=int(p['k'])<=114
  assert int(p['point_min'])<=int(p['point_max'])
  checks['primary_bounds']+=1
 mrows=read(root/'metal_random_reference_t23.csv')
 assert len(mrows)==16 and len(set((r['metal'],r['k']) for r in mrows))==16
 for r in mrows:
  n,t,k=map(int,(r['N'],r['target_t'],r['k']))
  assert (n,t)==(114,23) and k in [23,46]
  assert Q(r['uniform_random_expectation'])==Q(k*t,n)
  for p,field in [('field','field'),('lab','lab')]:
   lo=int(r[p+'_min']);hi=int(r[p+'_max'])
   assert 0<=lo<=hi<=min(k,t)
   assert Q(r[p+'_tail_upper_at_min'])==hg(n,t,k,lo)
   assert Q(r[p+'_tail_lower_at_max'])==hg(n,t,k,hi)
   assert Q(r[p+'_tail_upper_at_min'])>=Q(r[p+'_tail_lower_at_max'])
   checks['hypergeom_bounds']+=1
 hist={int(r['num_high_metals_per_site']):int(r['number_of_sites']) for r in read(root/'nominal_overlap_histogram.csv')}
 assert sum(hist.values())==114 and sum(w*c for w,c in hist.items())==184
 checks['nominal_overlap_identity']+=1
 pool=read(root/'nominal_eight_metal_dependent_random_reference.csv')
 assert len(pool)==2
 for r in pool:
  k=int(r['k']);assert k in [23,46]
  dist=grp_dp(hist,k);den=math.comb(114,k);assert sum(dist.values())==den
  assert Q(r['uniform_expectation'])==Q(k*184,114)
  F=int(r['field_nominal_incidence']);L=int(r['lab_nominal_incidence'])
  assert Q(r['Pr_random_LE_field'])==Q(sum(v for s,v in dist.items() if s<=F),den)
  assert Q(r['Pr_random_GE_lab'])==Q(sum(v for s,v in dist.items() if s>=L),den)
  sorted_dist=sorted(dist.items());acc=0;q={}
  for s,c in sorted_dist:
   acc+=c
   for quant in (Q(1,40),Q(1,2),Q(39,40)):
    if quant not in q and Q(acc,den)>=quant:q[quant]=s
  assert [int(r[x]) for x in ('exact_null_quantile_2p5','exact_null_median','exact_null_quantile_97p5')]==[q[x] for x in (Q(1,40),Q(1,2),Q(39,40))]
  checks['pooled_multimetal_group_dp']+=1
 # Independent exhaustive toy tests: site-specific DP vs all subsets.
 for ws in ([0,1,2,3],[0,0,1,3,3],[1,1,1,2,2,4],[0,1,1,4,5,5,5]):
  for k in range(len(ws)+1):
   dp=grp_dp(Counter(ws),k)
   brute=Counter(sum(q) for q in itertools.combinations(ws,k))
   assert dp==dict(brute)
   checks['small_bruteforce_dp']+=1
 # deterministic hypergeom probability mass identity at small dimensions
 for n in range(4,12):
  for t in range(1,n):
   for k in range(1,n):
    sum_mass=sum(Q(math.comb(t,j)*math.comb(n-t,k-j),math.comb(n,k)) for j in range(max(0,k-(n-t)),min(t,k)+1))
    assert sum_mass==1
    checks['hypergeom_mass_identity']+=1
 return {'status':'PASS','checks':dict(checks),'total_checks':sum(checks.values()),'privacy_boundary':'Only aggregate tables and synthetic tests inspected; does not reauthenticate historical source records.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path);a=p.parse_args()
 r=verify(a.root)
 if a.out:a.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r,indent=2))
