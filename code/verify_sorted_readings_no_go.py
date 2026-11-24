#!/usr/bin/env python3
"""Exact k=23 permutation-invariant MS2D reading-order robustness audit.

Input: the same immutable 115-row public source; 114 included sites.
For each site, sort the four readings, then require every strict order-statistic
superior to precede a selected dominated site. Exhaustively enumerate all
upward-closed k=23 sets and maximize field-minus-land-use-matched random
expected eight-metal target incidence over compatible recorded cutoff ties.
No optimizer, geolocation, external calibration, or unreviewed data is used.
"""
import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data'/'AlKarak_2009_Matched_SiteMeasurements_115.csv'
EXPECTED_SHA = '597e61b5bdeb8b4193f2bf9766fe055bd1787f9a756a89241d99cea65afece1a'
METALS = ('Zn','Ni','Cu','Cr','Cd','Mn','Pb','Co')


def run():
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == EXPECTED_SHA, 'Source file identity changed'
    with DATA.open(encoding='utf-8',newline='') as f:
        all_rows=list(csv.DictReader(f))
    rows=[r for r in all_rows if r['primary_cohort']=='1']
    assert len(all_rows)==115 and len(rows)==114 and len(all_rows[0])==56
    n=len(rows)
    X=[tuple(sorted(int(r[f'field_read_{d}']) for d in range(1,5))) for r in rows]
    P=[]
    for i in range(n):
        s=frozenset(j for j in range(n) if i!=j and
            all(X[j][d]>=X[i][d] for d in range(4)) and
            any(X[j][d]>X[i][d] for d in range(4)))
        P.append(s)
    assert sum(len(s) for s in P)==5778
    level={frozenset()}
    for k in range(1,24):
        level={S|{i} for S in level for i in range(n) if i not in S and P[i] <= S}
    assert len(level)==11
    groups=Counter(r['historical_land_use'] for r in rows)
    labels=[r['historical_land_use'] for r in rows]
    targets=[]
    for m in METALS:
        a=[F(r[f'{m}_recorded']) for r in rows]
        cutoff=sorted(a,reverse=True)[22]
        high=frozenset(i for i,v in enumerate(a) if v>cutoff)
        tied=frozenset(i for i,v in enumerate(a) if v==cutoff)
        remain=23-len(high)
        assert 0<=remain<=len(tied)
        targets.append((high,tied,remain))
    best=None; best_ids=None; best_F=None; best_B=None
    for S in level:
        n_by_group=Counter(labels[i] for i in S)
        f={g:F(n_by_group[g],groups[g]) for g in groups}
        diff=F(0); hits=0; reference=F(0)
        for hi,tie,t in targets:
            # Field and random reference must use the same chemical target.
            chosen=frozenset(sorted(tie,key=lambda i:(int(i in S)-f[labels[i]],i),reverse=True)[:t])
            T=hi|chosen
            h=sum(i in S for i in T)
            b=sum((f[labels[i]] for i in T),F(0))
            hits+=h;reference+=b;diff+=h-b
        assert diff==hits-reference
        if best is None or diff>best:
            best=diff;best_ids=sorted(int(rows[i]['sample_id']) for i in S);best_F=hits;best_B=reference
    assert best==F(-6,1), (best,best_ids,best_F,best_B)
    cert={
        'research_version':'EP14R6',
        'source_sha256':EXPECTED_SHA,
        'site_records':114,
        'sorted_four_reading_strict_dominance_pairs':5778,
        'k':23,'top_t_per_metal':23,'metals':list(METALS),
        'permutation_invariant_admissible_sets':11,
        'maximum_field_minus_stratified_random_excess':str(best),
        'witness_source_ids':best_ids,
        'witness_metal_site_incidences':best_F,
        'witness_random_expected_incidences':str(best_B),
        'interpretation':'One finite-cohort sensitivity certificate under order-statistic strict high-first precedence; not an external calibration or policy-validation claim.'
    }
    expected_path=ROOT/'results/SORTED_FIELD_READING_ORDER_CERTIFICATE.json'
    expected=json.loads(expected_path.read_text()) if expected_path.exists() else None
    if expected is not None:
        assert expected==cert, 'Stored permutation-invariant certificate differs from exact public-data replay'
    else:
        expected_path.write_text(json.dumps(cert,indent=2,ensure_ascii=False)+'\n')
    print('PASS sorted four-replicate invariant: 5778 ordered pairs, 11 k23 sets, max excess -6')
    print('WITNESS selected site ids:',','.join(map(str,best_ids)))
    print('WITNESS field incidences=',best_F,'matched-random expectation=',best_B)

if __name__=='__main__':run()
