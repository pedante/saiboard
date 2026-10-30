"""Verify Phase 3 evidence coverage and immutable inputs; never write EDA files."""
from pathlib import Path
import csv
import hashlib
import json
import os
import re
from urllib.parse import unquote
from phase1_audit import P, DESIGNS, parse, children, one

A = P / '01_audit/phase3'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


inventory = list(csv.DictReader((P / '01_audit/SOURCE_INVENTORY.csv').open()))
assert len(inventory) == 117
for row in inventory:
    for root in (P.parent, P / '00_original_snapshot'):
        assert digest(root / row['path']) == row['sha256'], (root, row['path'])
original_paths = set()
for root, dirs, files in os.walk(P.parent):
    dirs[:] = [d for d in dirs if Path(root) / d != P]
    original_paths.update(str((Path(root) / f).relative_to(P.parent)) for f in files)
assert original_paths == {row['path'] for row in inventory}, 'Original file set changed'

chg4 = json.loads((P / '01_audit/CHG-004/VERIFICATION.json').read_text())
assert chg4['status'] == 'Applied-provisional'
assert chg4['complete_tree_equal_after_reversing_allowed_fields']
baseline_files = chg4['baseline_files']
assert len(baseline_files) == 27
for row in baseline_files:
    original_copy = P / '02_work/baseline_before_CHG004' / row['path']
    working = P / '02_work/baseline' / row['path']
    assert digest(original_copy) == row['sha256'], original_copy
    assert not original_copy.stat().st_mode & 0o222, original_copy
    assert digest(working) == row['baseline_sha256'], working
for directory in ('baseline', 'baseline_before_CHG004'):
    root = P / '02_work' / directory
    assert {str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()} == {
        row['path'] for row in baseline_files
    }, directory

guard = json.loads((A / 'INPUT_GUARD.json').read_text())
for name, expected in guard['hashes'].items():
    assert digest(Path(name)) == expected, name
mechanical = json.loads((A / 'MECHANICAL_READONLY.json').read_text())
for row in mechanical:
    assert digest(P.parent.parent / row['path']) == row['sha256'], row['path']

groups = json.loads((A / 'PROCUREMENT_GROUPS.json').read_text())
observations = json.loads((A / 'SOURCING_OBSERVATIONS.json').read_text())
assert [g['id'] for g in groups] == [r['id'] for r in observations]
assert len(groups) == 20
references = [(x['design'], x['reference']) for g in groups for x in g['instances']]
assert len(references) == len(set(references)) == 582
per_design = {}
for design in DESIGNS:
    native = parse((P / f'01_audit/phase2/native/baseline/{design}/netlist.net').read_text())
    expected = {one(c, 'ref')[1] for c in children(one(native, 'components'), 'comp')}
    actual = {r for d, r in references if d == design}
    assert actual == expected, (design, actual ^ expected)
    per_design[design] = len(actual)
assert per_design == {'11x3': 165, '8x3': 114, '3x8': 89, '8x8': 214}
assert groups[0]['quantity'] == 145
assert [len(groups[0]['designators'][d]) for d in DESIGNS] == [33, 24, 24, 64]
holes = json.loads((A / 'MECHANICAL_REFERENCE_EXCLUSIONS.json').read_text())
assert sum(map(len, holes.values())) == 20
assert all({'exclude_from_bom', 'exclude_from_pos_files'} <= set(x['attributes'])
           for entries in holes.values() for x in entries)
assert not any((P / '03_output').iterdir()), 'Production output is no longer empty'

audit = (A / 'PHASE3_AUDIT.md').read_text()
assert set(re.findall(r'\| (U-\d{3}) \|', audit)) == {f'U-{i:03}' for i in range(1, 31)}
proposals = (A / 'CHANGE_PROPOSALS.md').read_text()
assert set(re.findall(r'\| (CHG-\d{3}) /', proposals)) == {f'CHG-{i:03}' for i in range(7, 28)}
report = (P / 'docs/PRODUCTION_PREP_REPORT.md').read_text()
assert len(re.findall(r'^## [1-9]\. ', report, re.M)) == 9
assert all(f'CHG-{i:03}' in report for i in range(1, 28))
assert all(f'F-{i:03}' in report for i in range(1, 30))
links = 0
docs = [P / 'docs/PRODUCTION_PREP_REPORT.md', *A.glob('*.md')]
for doc in docs:
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', doc.read_text()):
        if re.match(r'^[a-z]+:', target) or target.startswith('#'):
            continue
        linked = (doc.parent / unquote(target.split('#')[0])).resolve()
        if linked == A / 'FINAL_VERIFICATION.json':
            continue  # This successful check writes that result below.
        assert linked.is_file(), (doc, linked)
        links += 1

result = {
    'date': '2026-10-29', 'phase': 3,
    'status': 'Review package complete; qualification incomplete; stopped at gate',
    'CHG-004_status': 'Applied-provisional; equivalence not verified',
    'original_files_checked': len(inventory),
    'original_and_snapshot_hashes_unchanged': True,
    'original_file_set_unchanged': True,
    'baseline_files_checked': len(baseline_files),
    'baseline_hashes_identical_to_CHG004_approved_result': True,
    'pristine_backup_hashes_and_read_only_flags_verified': True,
    'only_CHG004_fields_differ_from_originals': True,
    'phase3_guard_files_checked': len(guard['hashes']),
    'mechanical_files_checked': len(mechanical),
    'mechanical_hashes_unchanged': True,
    'bom_instances': len(references), 'bom_groups': len(groups),
    'bom_designators_equal_native_netlists': per_design,
    'original_LED_count': 145, 'provisional_LED_count': 145, 'uncovered_LEDs': [],
    'mechanical_bom_and_position_exclusions_verified': 20,
    'unverified_register_items': 30, 'new_fix_proposals': 21,
    'report_local_links_checked': links,
    'no_design_change_or_refill_in_phase3': True,
    'native_checks': 'Unchanged Phase2 inputs/results; no redundant rerun',
    'production_output_empty': True,
    'release': 'BLOCKED; no manufacturing release, order or upload'
}
(A / 'FINAL_VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
