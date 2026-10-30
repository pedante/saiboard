"""Read-only structural audit; creates isolated copies and evidence, never a baseline."""
from pathlib import Path
import collections
import copy
import csv
import hashlib
import json
import math
import re
import shutil

P = Path(__file__).resolve().parents[1]
S = P / '00_original_snapshot'
A = P / '01_audit' / 'phase1'
A.mkdir(exist_ok=True)
DESIGNS = ['11x3', '8x3', '3x8', '8x8']

def parse(text):
    stack, root = [], []
    current = root
    for m in re.finditer(r'\s+|;[^\n]*|\(|\)|"(?:\\.|[^"\\])*"|[^\s()"]+', text):
        t = m.group()
        if t.isspace() or t.startswith(';'):
            continue
        if t == '(':
            child = []
            current.append(child)
            stack.append(current)
            current = child
        elif t == ')':
            assert stack, 'Unbalanced closing parenthesis'
            current = stack.pop()
        else:
            current.append(re.sub(r'\\(["\\nrt])', lambda x: {'n':'\n','r':'\r','t':'\t'}.get(x[1],x[1]),t[1:-1]) if t.startswith('"') else t)
    assert not stack and len(root) == 1
    return root[0]

def children(n, key):
    return [x for x in n if isinstance(x,list) and x and x[0] == key]

def one(n, key, default=None):
    v = children(n,key)
    return v[0] if v else ([key,default] if default is not None else [])

def props(n):
    return {x[1]:x[2] for x in children(n,'property')}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def dump(name, data):
    (A/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def ref(n, pcb=False):
    return next((x[2] for x in children(n,'fp_text') if x[1]=='reference'),'') if pcb else props(n).get('Reference','')

def footprint(n):
    return {'reference':ref(n,True),'value':next((x[2] for x in children(n,'fp_text') if x[1]=='value'),''), 'footprint':n[1], 'properties':props(n),'at':one(n,'at')[1:],'layer':one(n,'layer')[1:], 'pads':[{ 'number':x[1], 'net':one(x,'net')[1:], 'at':one(x,'at')[1:], 'size':one(x,'size')[1:], 'drill':one(x,'drill')[1:]} for x in children(n,'pad')]}

def board_geometry(n):
    edges=[x for x in n if isinstance(x,list) and one(x,'layer', '')[1:] == ['Edge.Cuts']]
    points=[]
    for e in edges:
        for k in ['start','end','mid','center']:
            v=one(e,k)
            if len(v)>=3: points.append([float(v[1]),float(v[2])])
    # shortcut: only straight outlines are supported; add analytic extents if curved sources appear.
    assert all(e[0] in ['gr_line','gr_rect'] for e in edges), 'Curved outline requires analytic extents'
    bbox=[min(x[0] for x in points),min(x[1] for x in points),max(x[0] for x in points),max(x[1] for x in points)]
    layers=[x[1] for x in one(n,'layers')[1:] if isinstance(x,list) and x[1].endswith('.Cu')]
    holes=[]
    for f in children(n,'footprint'):
        at=one(f,'at'); fx,fy=map(float,at[1:3]); angle=math.radians(float(at[3]) if len(at)>3 else 0)
        for pad in children(f,'pad'):
            drill=one(pad,'drill')
            if not drill: continue
            xy=one(pad,'at'); x,y=map(float,xy[1:3])
            # KiCad PCB screen-coordinate rotation.
            holes.append({'reference':ref(f,True),'pad':pad[1],'type':pad[2],'drill':drill[1:],'x':round(fx+x*math.cos(angle)+y*math.sin(angle),6),'y':round(fy-x*math.sin(angle)+y*math.cos(angle),6)})
    holes += [{'reference':'via','type':'via','drill':one(v,'drill')[1:],'x':float(one(v,'at')[1]),'y':float(one(v,'at')[2])} for v in children(n,'via')]
    return {'outline_bbox_mm':bbox,'outline_size_mm':[round(bbox[2]-bbox[0],6),round(bbox[3]-bbox[1],6)],'layers':layers,'layer_count':len(layers),'outline_segments':len(edges),'holes':holes,'drill_count':len(holes),'thickness_field':one(one(n,'general'),'thickness')[1:]}

def compare_fields(a,b):
    return {k:{'before':a.get(k),'after':b.get(k)} for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)}

assert parse('(a (b "x\\"y") (c 1))') == ['a',['b','x"y'],['c','1']]
assert parse('(a ; comment\n (b "µF"))') == ['a',['b','µF']]

if __name__ == '__main__':
    result, component_rows = {}, []
    for family, rel in [('original','kicad_files'),('updated','updated_components_SKC6812RGBW-WS')]:
        dest=A/'copies'/family
        if not dest.exists(): shutil.copytree(S/rel,dest)
        for f in dest.rglob('*'):
            if f.is_file(): f.chmod(0o644)
        # Original source root is already kicad_files; candidate root includes libraries.
    for d in DESIGNS:
        versions={}
        for family, root in [('original',A/'copies'/'original'),('updated',A/'copies'/'updated'/'kicad_files')]:
            pcb=parse((root/d/(d+'.kicad_pcb')).read_text())
            sch=parse((root/d/(d+'.kicad_sch')).read_text())
            fs=children(pcb,'footprint'); syms=children(sch,'symbol')
            pcb_refs=[ref(x,True) for x in fs]; sch_refs=[ref(x) for x in syms if not ref(x).startswith('#') and one(x,'on_board','yes')[1]=='yes']
            versions[family]={'pcb':pcb,'sch':sch,'footprints':{ref(x,True):x for x in fs},'symbols':{ref(x):x for x in syms},'geometry':board_geometry(pcb), 'consistency':{'footprint_count':len(fs),'schematic_nonpower_onboard_count':len(sch_refs),'duplicate_pcb_refs':[k for k,v in collections.Counter(pcb_refs).items() if v>1],'duplicate_sch_refs':[k for k,v in collections.Counter(sch_refs).items() if v>1],'pcb_only_refs':sorted(set(pcb_refs)-set(sch_refs)),'sch_only_refs':sorted(set(sch_refs)-set(pcb_refs)), 'unassigned_footprints':[ref(x) for x in syms if ref(x) in sch_refs and not props(x).get('Footprint')]}}
        a,b=versions['original'],versions['updated']
        diffs=[]
        for r in sorted(set(a['symbols'])|set(b['symbols'])|set(a['footprints'])|set(b['footprints'])):
            sc={};pc={}
            if r in a['symbols'] and r in b['symbols']:
                sa,sb=a['symbols'][r],b['symbols'][r]
                sc=compare_fields({**props(sa),'lib_id':one(sa,'lib_id')[1:]},{**props(sb),'lib_id':one(sb,'lib_id')[1:]})
            elif r in a['symbols'] or r in b['symbols']:sc={'presence_changed':True}
            if r in a['footprints'] and r in b['footprints']:pc=compare_fields(footprint(a['footprints'][r]),footprint(b['footprints'][r]))
            elif r in a['footprints'] or r in b['footprints']:pc={'presence_changed':True}
            changed=bool(sc or pc)
            component_rows.append({'design':d,'reference':r,'changed':changed,'classification':'intentional component update' if changed and r.startswith('D') else ('unexplained' if changed else 'unchanged'),'schematic_diff':sc,'pcb_diff':pc})
            if changed:diffs.append(component_rows[-1])
        pcb_other_a=[x for x in a['pcb'] if not isinstance(x,list) or x[0]!='footprint']
        pcb_other_b=[x for x in b['pcb'] if not isinstance(x,list) or x[0]!='footprint']
        sch_other_a=[x for x in a['sch'] if not isinstance(x,list) or x[0] not in ['symbol','lib_symbols']]
        sch_other_b=[x for x in b['sch'] if not isinstance(x,list) or x[0] not in ['symbol','lib_symbols']]
        result[d]={'component_differences':diffs,'noncomponent_pcb_tree_equal':pcb_other_a==pcb_other_b,'noncomponent_sch_tree_equal':sch_other_a==sch_other_b,'geometry_equal':a['geometry']==b['geometry'],'versions':{k:{'geometry':v['geometry'],'consistency':v['consistency'],'pcb_format':one(v['pcb'],'version')[1],'sch_format':one(v['sch'],'version')[1]} for k,v in versions.items()}}
        for family,v in versions.items():
            dump(f'{d}_{family}_components.json',{'pcb':[footprint(x) for x in v['footprints'].values()], 'schematic':[{'reference':r,**props(x),'lib_id':one(x,'lib_id')[1:],'uuid':one(x,'uuid')[1:]} for r,x in v['symbols'].items()]})
    dump('STRUCTURAL_DIFF.json',result)
    dump('COMPONENT_DIFF.json',component_rows)
    with (A/'COMPONENT_DIFF.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(component_rows[0])); w.writeheader();w.writerows([{**r,'schematic_diff':json.dumps(r['schematic_diff']),'pcb_diff':json.dumps(r['pcb_diff'])} for r in component_rows])
    for d,v in result.items():print(d,json.dumps({'changed_components':len(v['component_differences']),'pcb_noncomponent_equal':v['noncomponent_pcb_tree_equal'],'sch_noncomponent_equal':v['noncomponent_sch_tree_equal'],'geometry_equal':v['geometry_equal'],'consistency':{k:x['consistency'] for k,x in v['versions'].items()},'geometry':{k:x['geometry']['outline_size_mm'] for k,x in v['versions'].items()}}))
