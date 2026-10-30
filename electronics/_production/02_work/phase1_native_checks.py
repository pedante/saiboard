"""Native checks on isolated audit copies, with before/after source hash guards."""
from phase1_audit import *
import subprocess
import time

CLI=['/usr/bin/flatpak','run','--command=kicad-cli','org.kicad.KiCad']
N=A/'native'
N.mkdir(exist_ok=True)
sources=[p for p in (A/'copies').rglob('*') if p.is_file() and (p.suffix in ['.kicad_sch','.kicad_pcb','.kicad_pro','.kicad_sym'] or p.name=='sym-lib-table')]
before={str(p):sha(p) for p in sources}
records=[]
for family,root in [('original',A/'copies'/'original'),('updated',A/'copies'/'updated'/'kicad_files')]:
    for d in DESIGNS:
        out=N/family/d
        out.mkdir(parents=True,exist_ok=True)
        for kind,args in [('erc',['sch','erc','--format','json','--severity-all','--exit-code-violations','-o',str(out/'erc.json'),str(root/d/(d+'.kicad_sch'))]),('drc',['pcb','drc','--format','json','--severity-all','--schematic-parity','--exit-code-violations','-o',str(out/'drc.json'),str(root/d/(d+'.kicad_pcb'))]),('netlist',['sch','export','netlist','-o',str(out/'netlist.net'),str(root/d/(d+'.kicad_sch'))])]:
            command=CLI+args
            assert not any(x in command for x in ['--save-board','upgrade','--refill-zones'])
            assert Path(command[-1]).is_relative_to(A/'copies')
            t=time.time()
            try:
                r=subprocess.run(command,capture_output=True,text=True,timeout=240,cwd=out)
                record={'family':family,'design':d,'kind':kind,'command':command,'returncode':r.returncode,'seconds':round(time.time()-t,2),'stdout':r.stdout,'stderr':r.stderr}
            except subprocess.TimeoutExpired as e:
                record={'family':family,'design':d,'kind':kind,'command':command,'error':'timeout','seconds':round(time.time()-t,2)}
            (out/(kind+'_command.json')).write_text(json.dumps(record,indent=2)+'\n')
            records.append(record)
            print(f'{family} {d} {kind}: {record.get("returncode",record.get("error"))}',flush=True)
after={str(p):sha(p) for p in sources}
assert before==after,'CLI changed an input design copy'
with (P/'01_audit'/'SOURCE_INVENTORY.csv').open() as f:
    for row in csv.DictReader(f):
        assert sha(S/row['path'])==row['sha256'],row['path']
        assert sha(P.parent/row['path'])==row['sha256'],row['path']
dump('NATIVE_RUNS.json',{'version':'10.0.7','records':records,'copy_design_hashes_unchanged':True,'original_and_snapshot_hashes_unchanged':True,'copy_design_hashes':before,'zones':'stored fills; no refill requested','native_source_upgrade_or_save':False})
