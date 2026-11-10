"""
Self-check for Mahmoud OS v2.1.x planning package consistency.
Reads the CSV as single source of truth and validates that the blueprint,
priority matrix and changelog stay synchronized.
Run: python plans/mahmoud-os-v2.1-selfcheck.py
"""
from pathlib import Path
import csv
import re
from collections import defaultdict

PLANS_DIR = Path(__file__).parent
MATRIX = PLANS_DIR / 'mahmoud-os-requirements-matrix-v2.1.2.csv'
BLUEPRINT = PLANS_DIR / 'mahmoud-os-master-blueprint-v2.1.2.md'
PRIORITY = PLANS_DIR / 'mahmoud-os-feature-priority-v2.1.2.md'
CHANGELOG = PLANS_DIR / 'mahmoud-os-v2.1.2-changelog.md'

def main():
    rows = list(csv.DictReader(MATRIX.read_text(encoding='utf-8').splitlines()))
    r_rows = [r for r in rows if r['req_id'].startswith('R')]
    s_rows = [r for r in rows if r['req_id'].startswith('S')]
    ftr_rows = [r for r in rows if r['req_id'].startswith('FTR')]

    checks = []

    def ids_contiguous(items, prefix):
        nums = sorted(int(x[len(prefix):]) for x in (r['req_id'] for r in items))
        return [f'{prefix}{n}' for n in range(1, max(nums)+1) if n not in nums]

    checks.append(('R IDs contiguous', not ids_contiguous(r_rows, 'R')))
    checks.append(('S IDs contiguous', not ids_contiguous(s_rows, 'S')))
    checks.append(('FTR IDs contiguous', not ids_contiguous(ftr_rows, 'FTR')))
    checks.append(('Total rows = 100', len(rows) == 100))

    all_f = {f'F{n:02d}' for n in range(1, 51)}
    covered = {r['f_id'] for r in rows}
    checks.append(('All F01-F50 covered', all_f <= covered))

    f_class = defaultdict(set)
    for r in rows:
        if r['release'] == 'Future':
            f_class[r['f_id']].add('Future')
        elif r['req_id'].startswith('R') and r['req_id'] in ('R063','R064','R065','R066'):
            f_class[r['f_id']].add('DeferredRequired')
    conflicts = [fid for fid, cls in f_class.items() if 'DeferredRequired' in cls and 'Future' in cls]
    checks.append(('No deferred required outcome also Future', not conflicts))

    first_rel = [r for r in r_rows if r['release'] in ('P0', 'P0-P4', 'P1-P4')]
    comp_rel = [r for r in r_rows if r['release'].startswith(('P5', 'P8', 'P10'))]
    checks.append(('First release ends at R038', max(int(r['req_id'][1:]) for r in first_rel) == 38))
    checks.append(('Complete product ends at R066', max(int(r['req_id'][1:]) for r in comp_rel) == 66))

    bp = BLUEPRINT.read_text(encoding='utf-8')
    checks.append(('BP no stale R001-R034', 'R001–R034' not in bp and 'R001-R034' not in bp))
    checks.append(('BP no stale R001-R047', 'R001–R047' not in bp and 'R001-R047' not in bp))
    checks.append(('BP no stale R001-R051', 'R001–R051' not in bp and 'R001-R051' not in bp))
    checks.append(('BP complete product R001-R066', 'R001–R066' in bp))
    checks.append(('BP no Hermes=R037', not re.search(r'Hermes[^\n]{0,80}R037', bp)))
    checks.append(('BP P01 first-use approved-pinned-baseline',
                   '`P01-IDENTITY.md#proposed-first-use-command-and-service-policy-authority` (approved-pinned-baseline)' in bp))
    checks.append(('BP P12 cache approved-pinned-baseline',
                   '`P12-MODELS.md#proposed-cache-completeness-and-derived-admission` (approved-pinned-baseline)' in bp))
    checks.append(('BP P13 citation approved-pinned-baseline',
                   '`P13-EVALUATIONS.md#proposed-citation-verification-before-repair` (approved-pinned-baseline)' in bp))

    pm = PRIORITY.read_text(encoding='utf-8')
    checks.append(('PM first release R001-R038', 'R001–R038' in pm))
    checks.append(('PM complete product R039-R066', 'R039–R066' in pm))
    checks.append(('PM no stale R001-R034', 'R001–R034' not in pm and 'R001-R034' not in pm))
    checks.append(('PM no stale R001-R047', 'R001–R047' not in pm and 'R001-R047' not in pm))
    checks.append(('PM no stale R001-R051', 'R001–R051' not in pm and 'R001-R051' not in pm))
    checks.append(('PM no Hermes=R037', not re.search(r'Hermes[^\n]{0,80}R037', pm)))
    checks.append(('PM R038 = F04 discovery', '| R038 | **Discovery questions' in pm))
    checks.append(('PM R040 = Hermes', '| R040 | **Hermes Self-Improvement Review' in pm))
    checks.append(('PM R063-R066 required outcomes', '| R063 | **Credits' in pm and '| R066 | **Support desk' in pm))

    log = CHANGELOG.read_text(encoding='utf-8')
    checks.append(('Changelog v2.1.4 entry', 'v2.1.4 consistency synchronization' in log))
    checks.append(('Changelog 50/50 coverage', '50/50' in log or '50 canonical' in log))
    checks.append(('Changelog R063-R066', 'R063–R066' in log or 'R063-R066' in log))

    failures = []
    for name, ok in checks:
        print(f'{"PASS" if ok else "FAIL"}: {name}')
        if not ok:
            failures.append(name)

    print(f'\nTotal: {len(checks)}, FAIL: {len(failures)}')
    if failures:
        print('Failures:', failures)
        raise SystemExit(1)

if __name__ == '__main__':
    main()
