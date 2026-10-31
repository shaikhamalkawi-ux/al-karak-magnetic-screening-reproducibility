#!/usr/bin/env python3
"""Recheck selected published Al-Karak aggregate claims without site-level records.

This script checks the original, frozen derived CSV data, not archived sample
measurements. It cannot regenerate or verify instrument readings or unit
conversions. No original sample IDs, coordinates, or measurements are used.
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from verify_source_free import verify


def rows(path: Path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def replay(root: Path) -> dict:
    assert root.is_dir(), f'Missing derived directory: {root}'
    verification = verify(root)
    assert verification['status'] == 'PASS'
    assert verification['total_checks'] == 2537
    metals = rows(root / 'metal_random_reference_t23.csv')
    zinc = {(r['metal'], int(r['k'])): r for r in metals}
    assert len(metals) == 16 and len({r['metal'] for r in metals}) == 8
    assert {(int(r['N']), int(r['target_t'])) for r in metals} == {(114,23)}
    for k, field, lab in [(23, (7,7), (4,4)), (46,(8,8),(11,12))]:
        row = zinc[('Zn', k)]
        assert (int(row['field_min']),int(row['field_max'])) == field
        assert (int(row['lab_min']),int(row['lab_max'])) == lab
    sensitivity = rows(root / 'zinc_target_sensitivity_16rules.csv')
    aggs = sorted({r['aggregation'] for r in sensitivity})
    assert len(aggs) == 16
    assert len(sensitivity) == 3 * len(aggs) * 5
    assert {int(r['target_size_t']) for r in sensitivity} == {12,23,35}
    assert {r['decision'] for r in sensitivity} == {
        'point23','point46','prefix1_46','window23_46','window27_46'
    }

    def classification(t: int, window: str) -> dict:
        selected = [r for r in sensitivity if int(r['target_size_t']) == t and r['decision']==window]
        assert len(selected) == 16
        counts = Counter(r['classification'] for r in selected)
        return {
            'number_of_aggregation_rules': len(selected),
            'classes': dict(sorted(counts.items())),
            'minimum_reported_lower': min(int(r['lower']) for r in selected),
            'maximum_reported_upper': max(int(r['upper']) for r in selected),
        }

    t23 = classification(23, 'prefix1_46')
    t12 = classification(12, 'prefix1_46')
    t35 = classification(35, 'prefix1_46')
    assert t23['classes'] == {'FIELD':16}
    assert (t23['minimum_reported_lower'],t23['maximum_reported_upper'])==(-53,-5)
    assert t12['classes']=={'UNRESOLVED':16}
    assert (t12['minimum_reported_lower'],t12['maximum_reported_upper'])==(-34,30)
    assert t35['classes']=={'LAB':16}
    assert (t35['minimum_reported_lower'],t35['maximum_reported_upper'])==(30,67)

    primary = rows(root / 'zinc_primary_16rule_pointwise_check.csv')
    assert len(primary)==16*114
    assert set(map(int, (r['k'] for r in primary))) == set(range(1,115))

    return {
        'status':'PASS',
        'basis':'Author-approved public aggregate CSVs only; not source-row reproduction',
        'cohort_size':114,
        'number_of_metal_targets':8,
        'chemical_top_t_primary':23,
        'zinc_t23':{
            'budget_23':{'field_recovered':[7,7],'laboratory_recovered':[4,4]},
            'budget_46':{'field_recovered':[8,8],'laboratory_recovered':[11,12]},
        },
        'aggregation_rules':len(aggs),
        'zinc_prefix_budgets_1_to_46':{
            'chemical_target_12':t12,
            'chemical_target_23':t23,
            'chemical_target_35':t35,
        },
        'replay_checks':verification['total_checks'],
        'replay_breakdown':verification['checks'],
        'scopes_not_verified':['original chemistry','original magnetic readings','sample IDs',
            'site-level rankings or joins','absolute calibration','field validation','raw-data collection'],
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent/'derived')
    p.add_argument('--output', type=Path, default=None)
    args=p.parse_args()
    report=replay(args.root)
    output=json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(output,encoding='utf8')
    print(output,end='')

if __name__=='__main__':main()
