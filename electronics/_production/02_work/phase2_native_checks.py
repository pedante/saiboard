"""Read-only native checks; JLC screening settings exist only in audit copies."""
from phase1_audit import *
import subprocess
import time

BASE = P/'02_work/baseline'
OUT = P/'01_audit/phase2'
CLI = ['/usr/bin/flatpak', 'run', '--command=kicad-cli', 'org.kicad.KiCad']
OUT.mkdir(exist_ok=True)
baseline_hashes = {str(p.relative_to(BASE)): sha(p) for p in BASE.rglob('*') if p.is_file()}
records, settings_log = [], []
for mode in ['baseline', 'jlc_screen']:
    root = OUT/'copies'/mode
    if not root.exists():
        shutil.copytree(BASE/'kicad_files', root)
    if mode == 'jlc_screen':
        for d in DESIGNS:
            f = root/d/(d+'.kicad_pro')
            j = json.loads(f.read_text())
            rules = j['board']['design_settings']['rules']
            changes = {'min_text_height': 1.0, 'min_text_thickness': 0.15,
                       'min_silk_clearance': 0.15, 'solder_mask_min_width': 0.13,
                       'solder_mask_to_copper_clearance': 0.09}
            settings_log.append({'design':d, 'before':{k:rules.get(k) for k in changes}, 'after':changes})
            rules.update(changes)
            # Keep the original stricter copper/hole constraints; do not waive violations.
            f.write_text(json.dumps(j, indent=2)+'\n')
    inputs = {str(p):sha(p) for p in root.rglob('*') if p.is_file() and p.suffix in ['.kicad_pcb','.kicad_sch','.kicad_pro']}
    for d in DESIGNS:
        out = OUT/'native'/mode/d
        out.mkdir(parents=True, exist_ok=True)
        jobs = [('drc', ['pcb','drc','--format','json','--severity-all','--all-track-errors','--schematic-parity','--exit-code-violations','-o',str(out/'drc.json'),str(root/d/(d+'.kicad_pcb'))])]
        if mode == 'baseline':
            jobs += [('erc', ['sch','erc','--format','json','--severity-all','--exit-code-violations','-o',str(out/'erc.json'),str(root/d/(d+'.kicad_sch'))]),
                     ('netlist', ['sch','export','netlist','-o',str(out/'netlist.net'),str(root/d/(d+'.kicad_sch'))])]
        for kind,args in jobs:
            command = CLI+args
            assert not any(x in command for x in ['--save-board','upgrade','--refill-zones'])
            assert Path(command[-1]).is_relative_to(OUT/'copies')
            log = out/(kind+'_command.json')
            if mode == 'baseline' and log.exists():
                previous = json.loads(log.read_text())
                if previous['returncode'] in [0,5]:
                    records.append(previous)
                    continue
            start=time.time()
            r=subprocess.run(command, capture_output=True, text=True, timeout=240, cwd=out)
            row={'mode':mode,'design':d,'kind':kind,'command':command,'returncode':r.returncode,
                 'seconds':round(time.time()-start,2),'stdout':r.stdout,'stderr':r.stderr}
            (out/(kind+'_command.json')).write_text(json.dumps(row,indent=2)+'\n')
            records.append(row)
            print(mode,d,kind,r.returncode,flush=True)
            assert r.returncode in [0,5], row
    assert all(sha(Path(p)) == h for p,h in inputs.items()), 'native check changed an audit input'
assert baseline_hashes == {str(p.relative_to(BASE)):sha(p) for p in BASE.rglob('*') if p.is_file()}
for row in csv.DictReader((P/'01_audit/SOURCE_INVENTORY.csv').open()):
    assert sha(S/row['path']) == sha(P.parent/row['path']) == row['sha256']
(OUT/'NATIVE_RUNS.json').write_text(json.dumps({'date':'2026-10-29','records':records,
    'audit_setting_changes':settings_log,'baseline_hashes':baseline_hashes,
    'all_design_inputs_unchanged':True,'original_and_snapshot_hashes_unchanged':True,
    'zones':'stored fills; no refill/save/upgrade','generated_preferences':'KiCad created .kicad_prl files in audit copies only; no input design changed.',
    'screening_note':'Existing copper/hole rules retained; mask .13 covers all listed 1oz colors, legend 1mm follows capabilities table.'},indent=2)+'\n')
