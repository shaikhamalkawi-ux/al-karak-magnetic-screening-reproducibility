#!/usr/bin/env python3
"""Independent brute-force tests on synthetic data, plus invalid-input tests."""
from pathlib import Path
from fractions import Fraction
import itertools,json
import numpy as np
from exact_budget_audit import evaluate,complete_tie_groups
ROOT=Path(__file__).resolve().parents[1]

def orders(s):
    o,gs=complete_tie_groups(np.asarray(s))
    return [np.array(sum((list(q) for q in pp),[])) for pp in itertools.product(*(itertools.permutations(o[a:b]) for a,b in gs))]

def targets_direct(y,t):
    # Independent formulation: enumerate every size-t set, retain those consistent
    # with top-t ordering. Do not reuse enumerate_targets or complete_paths.
    choices=[]
    for v in itertools.combinations(range(len(y)),t):
        z=set(v);other=[i for i in range(len(y)) if i not in z]
        if min(y[i] for i in v)>=max(y[i] for i in other):choices.append(v)
    return choices

def brute(y,f,l,t,L,U,wclass):
    fo=orders(f);lo=orders(l);low=[];high=[]
    for selected in targets_direct(y,t):
        h=np.zeros(len(y),dtype=int);h[list(selected)]=1
        F=np.array([np.cumsum(h[o]) for o in fo]);B=np.array([np.cumsum(h[o]) for o in lo])
        for end in (range(L,U+1) if wclass=='nonincreasing' else [U]):
            if wclass=='arbitrary':
                for k in range(L,U+1):
                    low.append(Fraction(int(B[:,k-1].min()-F[:,k-1].max())))
                    high.append(Fraction(int(B[:,k-1].max()-F[:,k-1].min())))
            else:
                m=end-L+1
                low.append(Fraction(int(B[:,L-1:end].sum(1).min()-F[:,L-1:end].sum(1).max()),m))
                high.append(Fraction(int(B[:,L-1:end].sum(1).max()-F[:,L-1:end].sum(1).min()),m))
    return min(low),max(high)

def main():
    rng=np.random.default_rng(872910);checks=0;datasets=0;targets=0
    designs=[]
    for n in [4,5,6]:
        for _ in range(10):
            y=rng.integers(-1,4,n).tolist();f=rng.integers(-1,3,n).tolist();l=rng.integers(-1,3,n).tolist();t=int(rng.integers(1,n));designs.append((y,f,l,t))
    designs += [([1]*5,[1]*5,[1]*5,2),([1,1,0,0,0],[5,4,3,2,1],[1,2,3,4,5],2)]
    for y,f,l,t in designs:
        a=evaluate(y,f,l,t);n=len(y);datasets+=1;targets+=len(targets_direct(y,t))
        for L,U in [(1,n),(2,n),(1,2),(n,n)]:
            for wc in ['uniform','nonincreasing','arbitrary']:
                got=a.bounds(L,U,wc);want=brute(y,f,l,t,L,U,wc)
                assert (Fraction(got['lower']),Fraction(got['upper']))==want,(datasets,L,U,wc,got,want)
                checks+=1
        fixed=a.weighted(1,[Fraction(1,n)]*n);uniform=a.bounds(1,n)
        assert (fixed['lower'],fixed['upper'])==(uniform['lower'],uniform['upper']);checks+=1
        # Resolved-rank rank-sum identity must use the same tie resolution.
        for h in targets_direct(y,t):
            for of in orders(f)[:3]:
                for ol in orders(l)[:3]:
                    hf=np.isin(of,h).astype(int);hl=np.isin(ol,h).astype(int)
                    def auc_binary(binary):
                        # Number of negative records appearing after each positive.
                        return Fraction(sum(int((binary[i+1:]==0).sum()) for i in range(n) if binary[i]),t*(n-t))
                    integral=int(np.cumsum(hl).sum()-np.cumsum(hf).sum())
                    assert integral==t*(n-t)*(auc_binary(hl)-auc_binary(hf));checks+=1
    malformed=[lambda:evaluate([1,2],[1,float('nan')],[1,2],1),lambda:evaluate([1,2],[1,2],[1,2],0),lambda:evaluate([1,2],[1,2],[1,2],2),lambda:evaluate([1,2],[1,2,3],[1,2],1),lambda:evaluate([1,2],[1,2],[1,2],True),lambda:evaluate([1,2],[1,2],[1,2],1).bounds(0,2),lambda:evaluate([1,2],[1,2],[1,2],1).bounds(1,3),lambda:evaluate([1,2],[1,2],[1,2],1).bounds(1,1.5),lambda:evaluate([1,2],[1,2],[1,2],1).weighted(1,[-1,2]),lambda:evaluate([1,2],[1,2],[1,2],1).weighted(1,[0.2,0.2]),lambda:evaluate([1,1,1,1],[1,2,3,4],[4,3,2,1],2,limit=2)]
    invalid=0
    for f in malformed:
        try:f()
        except ValueError:invalid+=1
        else:raise AssertionError('Malformed input was not rejected')
    result={'synthetic_datasets':datasets,'independently_enumerated_target_sets':targets,'exact_arithmetic_checks':checks,'invalid_inputs_rejected':invalid,'status':'PASS','scope':'Software logic only; no field validation'}
    (ROOT/'qa').mkdir(exist_ok=True);(ROOT/'qa/synthetic_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
