#!/usr/bin/env python3
"""Finite-cohort exact budget-retrieval audit; not a predictor or new theorem.

Scores must be finite and directed so that larger scores are selected first.
Chemical ties at the top-t cutoff and all exact score ties are admitted.
The same target set and complete rank resolution apply across a budget window.
Uniform, arbitrary, or nonincreasing budget probabilities are distinct estimands.
Protected input records are never emitted by this module's command-line interface.
"""
from __future__ import annotations
import argparse, csv, itertools, json, math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence
import numpy as np

def direction(lo: Fraction | int, hi: Fraction | int) -> str:
    return 'LAB' if lo > 0 else 'FIELD' if hi < 0 else 'EXACT_EQUAL' if lo == hi == 0 else 'UNRESOLVED'

def finite_vector(x: Sequence[float], name: str) -> np.ndarray:
    a=np.asarray(x,dtype=float)
    if a.ndim!=1 or len(a)<2 or not np.isfinite(a).all():
        raise ValueError(f'{name}: expected a finite one-dimensional array with at least two entries')
    return a

def complete_tie_groups(score: np.ndarray) -> tuple[np.ndarray,list[tuple[int,int]]]:
    order=np.argsort(-score,kind='stable')
    ends=np.r_[0,1+np.flatnonzero(score[order][1:]!=score[order][:-1]),len(score)]
    return order,list(zip(ends[:-1].tolist(),ends[1:].tolist()))

def enumerate_targets(chem: np.ndarray,t: int,limit: int=100000) -> np.ndarray:
    if isinstance(t,bool) or not isinstance(t,(int,np.integer)) or not 1<=t<len(chem):
        raise ValueError('t must be an integer in 1..n-1')
    cutoff=np.sort(chem)[-t];above=np.flatnonzero(chem>cutoff);at=np.flatnonzero(chem==cutoff)
    choose=t-len(above);count=math.comb(len(at),choose)
    if count>limit:
        raise ValueError(f'{count} cutoff allocations exceed the explicit enumeration limit {limit}; no approximation made')
    H=np.zeros((count,len(chem)),dtype=np.int8);H[:,above]=1
    for i,c in enumerate(itertools.combinations(at,choose)):H[i,list(c)]=1
    return H

def complete_paths(score: np.ndarray,H: np.ndarray) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    """For each fixed H, extremal complete tie resolutions, valid for every k."""
    order,groups=complete_tie_groups(score)
    low=np.zeros((len(H),len(score)),dtype=np.int32);high=np.zeros_like(low)
    for a,b in groups:
        positives=H[:,order[a:b]].sum(1)
        positions=np.arange(b-a)[None,:]
        # Negatives first minimizes all prefixes; positives first maximizes them.
        low[:,a:b]=(positions >= ((b-a)-positives[:,None]))
        high[:,a:b]=(positions < positives[:,None])
    nominal=np.cumsum(H[:,order],axis=1,dtype=np.int32)
    return np.cumsum(low,axis=1),np.cumsum(high,axis=1),nominal

def rational_auc(score: np.ndarray,H: np.ndarray) -> list[Fraction]:
    result=[]
    for h in H:
        p=score[h.astype(bool)];q=score[~h.astype(bool)]
        wins=int((p[:,None]>q).sum());ties=int((p[:,None]==q).sum())
        result.append(Fraction(2*wins+ties,2*len(p)*len(q)))
    return result

@dataclass
class Audit:
    low: np.ndarray
    high: np.ndarray
    nominal: np.ndarray
    target_count: int
    auc: list[Fraction]
    field_auc: list[Fraction]
    lab_auc: list[Fraction]
    @property
    def n(self)->int:return self.low.shape[1]
    @property
    def allocations(self)->int:return self.low.shape[0]
    def bounds(self,start:int,end:int,weight_class:str='uniform')->dict:
        if isinstance(start,bool) or isinstance(end,bool) or not isinstance(start,(int,np.integer)) or not isinstance(end,(int,np.integer)) or not 1<=start<=end<=self.n:
            raise ValueError('Budget bounds must satisfy 1 <= start <= end <= n')
        a=self.low[:,start-1:end];b=self.high[:,start-1:end];m=end-start+1
        if weight_class=='uniform':
            lo=Fraction(int(a.sum(1).min()),m);hi=Fraction(int(b.sum(1).max()),m)
            jlo=jhi=end
        elif weight_class=='nonincreasing':
            pa=np.cumsum(a,axis=1);pb=np.cumsum(b,axis=1)
            ls=[Fraction(int(pa[:,j].min()),j+1) for j in range(m)]
            us=[Fraction(int(pb[:,j].max()),j+1) for j in range(m)]
            lo=min(ls);hi=max(us);jlo=start+ls.index(lo);jhi=start+us.index(hi)
        elif weight_class=='arbitrary':
            lo=Fraction(int(a.min()));hi=Fraction(int(b.max()))
            jlo=start+int(np.unravel_index(np.argmin(a),a.shape)[1]);jhi=start+int(np.unravel_index(np.argmax(b),b.shape)[1])
        else:raise ValueError('weight_class must be uniform, nonincreasing or arbitrary')
        return dict(start=start,end=end,weight_class=weight_class,lower=str(lo),upper=str(hi),direction=direction(lo,hi),lower_extreme_end=jlo,upper_extreme_end=jhi)
    def weighted(self,start:int,weights:Sequence[int|float|str])->dict:
        w=[Fraction(str(v)) for v in weights]
        if not w or any(x<0 for x in w) or sum(w)!=1:
            raise ValueError('Weights must be nonnegative and sum exactly to one; rational strings such as 1/3 are accepted')
        end=start+len(w)-1
        if isinstance(start,bool) or not isinstance(start,(int,np.integer)) or not 1<=start<=end<=self.n:raise ValueError('Invalid weighted window')
        def ev(v):return sum((int(x)*p for x,p in zip(v,w)),Fraction(0))
        lo=min(ev(v) for v in self.low[:,start-1:end]);hi=max(ev(v) for v in self.high[:,start-1:end])
        return dict(start=start,end=end,weight_class='user_fixed',lower=str(lo),upper=str(hi),direction=direction(lo,hi))

def evaluate(chemical:Sequence[float],field:Sequence[float],lab:Sequence[float],t:int,limit:int=100000)->Audit:
    chemical=finite_vector(chemical,'chemical');field=finite_vector(field,'field');lab=finite_vector(lab,'lab')
    if not len(chemical)==len(field)==len(lab):raise ValueError('All three input vectors must have identical length')
    H=enumerate_targets(chemical,t,limit)
    fl,fu,fn=complete_paths(field,H);ll,lu,ln=complete_paths(lab,H)
    af=rational_auc(field,H);al=rational_auc(lab,H)
    return Audit(ll-fu,lu-fl,ln-fn,t,[l-f for f,l in zip(af,al)],af,al)

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--chemical',default='chemical');p.add_argument('--field',default='field');p.add_argument('--lab',default='lab')
    p.add_argument('--target',type=int,required=True);p.add_argument('--start',type=int,required=True);p.add_argument('--end',type=int,required=True)
    p.add_argument('--weights',choices=['uniform','nonincreasing','arbitrary'],default='uniform');p.add_argument('--output',type=Path)
    a=p.parse_args()
    with a.input.open(encoding='utf-8-sig',newline='') as f:r=list(csv.DictReader(f))
    try:
        audit=evaluate([float(x[a.chemical]) for x in r],[float(x[a.field]) for x in r],[float(x[a.lab]) for x in r],a.target)
        result=audit.bounds(a.start,a.end,a.weights)
    except (KeyError,ValueError,TypeError) as e:p.error(str(e))
    result.update(n=audit.n,t=a.target,chemical_cutoff_allocations=audit.allocations,statistic='expected lab-minus-field recorded-high-site recovery over the stated budget class',scope='Finite input cohort; exact recorded-value ties only. Not confidence bounds, calibration, future accuracy, measured cost or release authorization.')
    text=json.dumps(result,indent=2)
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text+'\n',encoding='utf8')
    print(text)
if __name__=='__main__':main()
