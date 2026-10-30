"""Read source/audit data; write Phase 3 evidence only, never EDA files."""
from pathlib import Path
import collections
import hashlib
import json
import re
import zipfile
from phase1_audit import P, DESIGNS, parse, children, one, ref

A = P / '01_audit/phase3'
B = P / '02_work/baseline'
ROOT = P.parent.parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(name, obj):
    (A / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

guard = {str(f): digest(f) for folder in [ROOT/'board', B, P/'00_original_snapshot'] for f in folder.rglob('*') if f.is_file()}
groups = {}
for item in json.loads((A/'SOURCE_BOM_GROUPS.json').read_text()):
    key = item['footprint'] if item['footprint'].startswith(('Connector_', 'TerminalBlock_')) else item['value']
    g = groups.setdefault(key, {'source_values': [], 'footprint': item['footprint'], 'instances': []})
    g['source_values'].append(item['value'])
    g['instances'].extend(item['instances'])
for i, (key, g) in enumerate(groups.items(), 1):
    g['id'] = f'BOM-{i:02d}'
    g['quantity'] = len(g['instances'])
    g['designators'] = {d: sorted([x['reference'] for x in g['instances'] if x['design']==d], key=lambda s: (re.sub(r'\d','',s), int(re.search(r'\d+',s)[0]))) for d in DESIGNS}
assert sum(g['quantity'] for g in groups.values()) == 582
assert len({(x['design'],x['reference']) for g in groups.values() for x in g['instances']}) == 582
dump('PROCUREMENT_GROUPS.json', list(groups.values()))

native, mechanical_refs, power, zones = {}, {}, {}, {}
for d in DESIGNS:
    n = parse((P/f'01_audit/phase2/native/baseline/{d}/netlist.net').read_text())
    nets = {one(x,'name')[1]: [[one(y,'ref')[1],one(y,'pin')[1],one(y,'pinfunction','')[1]] for y in children(x,'node')] for x in children(one(n,'nets'),'net')}
    native[d] = {name: nodes for name,nodes in nets.items() if name in ['P','P3.3','GND'] or re.match(r'^(PQ\d+|Q\d+|Net-\(Q\d+-B\))$',name)}
    pcb = parse((B/f'kicad_files/{d}/{d}.kicad_pcb').read_text())
    mechanical_refs[d] = [{'reference':ref(f,True),'uuid':one(f,'tstamp','')[1], 'attributes':one(f,'attr')[1:]} for f in children(pcb,'footprint') if f[1].startswith('MountingHole:')]
    assert all({'exclude_from_bom','exclude_from_pos_files'} <= set(f['attributes']) for f in mechanical_refs[d])
    netids = {x[1]:x[2] for x in children(pcb,'net')}
    power[d] = dict(collections.Counter((netids.get(one(s,'net')[1]),one(s,'layer')[1],one(s,'width')[1]) for s in children(pcb,'segment') if netids.get(one(s,'net')[1]) in ['P','P3.3','GND']))
    power[d] = [{'net':k[0],'layer':k[1],'width_mm':float(k[2]),'segments':v} for k,v in power[d].items()]
    zones[d] = [{'uuid':one(z,'tstamp','')[1],'net':one(z,'net_name','')[1], 'layer':one(z,'layer','')[1], 'priority':one(z,'priority','0')[1], 'boundary':children(z,'polygon')} for z in children(pcb,'zone')]
dump('NATIVE_POWER_AND_RESISTOR_NETS.json',native)
dump('MECHANICAL_REFERENCE_EXCLUSIONS.json',mechanical_refs)
dump('POWER_TRACK_WIDTHS.json',power)
dump('ZONE_BOUNDARIES.json',zones)

mechanical=[]
for folder in [ROOT/'board', ROOT/'electronics/3d_prints']:
    for f in sorted(folder.rglob('*')):
        if not f.is_file(): continue
        entry={'path':str(f.relative_to(ROOT)), 'bytes':f.stat().st_size,'sha256':digest(f)}
        if f.suffix=='.dxf':
            lines=f.read_text().splitlines(); assert len(lines)%2==0
            pairs=list(zip(lines[::2],lines[1::2]))
            start=pairs.index(('2','ENTITIES')); end=next(i for i in range(start+1,len(pairs)) if pairs[i]==('0','ENDSEC'))
            ps=pairs[start+1:end]
            entry['entities']=dict(collections.Counter(v for c,v in ps if c=='0'))
            entry['z_coordinates']=sorted({float(v) for c,v in ps if c in ['30','31','32','38','39']})
            entry['header_units_code']=pairs[pairs.index(('9','$INSUNITS'))+1][1]
            entry['note']='Planar drawing; no machining depths or PCB-thickness parameter established.'
        elif f.suffix=='.gcode':
            zz=[float(x) for x in re.findall(r'^;Z:([0-9.]+)',f.read_text(),re.M)]
            entry['print_layer_z_mm'] = sorted(set(zz))
        elif f.suffix=='.f3d':
            with zipfile.ZipFile(f) as z:
                entry['archive_members']=len(z.namelist())
                entry['note']='Archive inspected read-only; native binary dimensions/dependencies not decoded. UNVERIFIED.'
        mechanical.append(entry)
dump('MECHANICAL_READONLY.json',mechanical)
assert all(digest(Path(path))==before for path,before in guard.items())
dump('INPUT_GUARD.json',{'date':'2026-10-29','unchanged':True,'hashes':guard})
print(json.dumps({'procurement_groups':len(groups),'instances':582,'mounting_holes':{d:len(v) for d,v in mechanical_refs.items()},'mechanical_files':len(mechanical),'guarded_unchanged':len(guard)},indent=2))
