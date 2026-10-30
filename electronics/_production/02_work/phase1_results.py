"""Summarize structural/native evidence and historical manufacturing geometry."""
from phase1_audit import *
import zipfile

def native_nets(p):
    n=parse(p.read_text())
    return {one(x,'name')[1]: sorted((one(y,'ref')[1],one(y,'pin')[1]) for y in children(x,'node')) for x in children(one(n,'nets'),'net')}

def canonical(n):
    n=copy.deepcopy(n)
    if n[0]=='kicad_pcb':
        for f in children(n,'footprint'):
            if ref(f,True).startswith('D'):
                f[:]=[x for x in f if not (isinstance(x,list) and x[0]=='property' and x[1] in ['Manufacturer','MPN','LCSC','AssemblyStatus'])]
                for t in children(f,'fp_text'):
                    if t[1]=='value':t[2]='LED_IDENTITY'
    else:
        for l in children(n,'lib_symbols'):
            l[:]=[x for x in l if not (isinstance(x,list) and x[0]=='symbol' and x[1] in ['LED:SK6812','Saiboard_LED:SKC6812RGBW-WS'])]
        for s in children(n,'symbol'):
            if ref(s).startswith('D'):
                s[:]=[x for x in s if not (isinstance(x,list) and x[0]=='property' and x[1] in ['Manufacturer','MPN','LCSC','AssemblyStatus'])]
                one(s,'lib_id')[1]='LED_LIBRARY'
                for prop in children(s,'property'):
                    if prop[1] in ['Value','Datasheet']:prop[2]='LED_IDENTITY'
        for si in children(n,'symbol_instances'):
            for path in children(si,'path'):
                if one(path,'reference','')[1].startswith('D'):one(path,'value')[1]='LED_IDENTITY'
    return n

def allpins(symbol):
    pins=[]
    for sub in children(symbol,'symbol'):
        for pin in children(sub,'pin'):
            pins.append({'number':one(pin,'number')[1],'name':one(pin,'name')[1],'type':pin[1], 'at':one(pin,'at')[1:],'length':one(pin,'length')[1:]})
    return sorted(pins,key=lambda x:x['number'])

results={}
for d in DESIGNS:
    row={}
    for family,root in [('original',A/'copies'/'original'),('updated',A/'copies'/'updated'/'kicad_files')]:
        out=A/'native'/family/d
        erc=json.loads((out/'erc.json').read_text()); drc=json.loads((out/'drc.json').read_text())
        groups={'erc':[v for sheet in erc['sheets'] for v in sheet['violations']], 'drc':drc['violations'],'unconnected':drc['unconnected_items'],'parity':drc['schematic_parity']}
        summary={key:{'total':len(vals),'severity':dict(collections.Counter(v['severity'] for v in vals)), 'types':dict(collections.Counter(v['type'] for v in vals))} for key,vals in groups.items()}
        pcb=parse((root/d/(d+'.kicad_pcb')).read_text()); sch=parse((root/d/(d+'.kicad_sch')).read_text())
        nets=native_nets(out/'netlist.net')
        boardnets=collections.defaultdict(set)
        for f in children(pcb,'footprint'):
            for pad in children(f,'pad'):
                net=one(pad,'net')
                if net and net[1]!='0': boardnets[net[2]].add((ref(f,True),pad[1]))
        sn={tuple(v):name for name,v in nets.items()}
        pn={tuple(sorted(v)):name for name,v in boardnets.items()}
        shared=set().union(*map(set,sn)) & set().union(*map(set,pn))
        sm={node:frozenset(set(group)&shared) for group in sn for node in group if node in shared}
        pm={node:frozenset(set(group)&shared) for group in pn for node in group if node in shared}
        mismatches=[{'node':list(node),'schematic_group':sorted(sm[node]),'pcb_group':sorted(pm[node])} for node in sorted(shared) if sm[node]!=pm[node]]
        missingpcb=sorted(set().union(*map(set,sn))-set().union(*map(set,pn)))
        missingsch=sorted(set().union(*map(set,pn))-set().union(*map(set,sn)))
        aliases=[{'schematic':sn[g],'pcb':pn[g],'pins':list(g)} for g in sn.keys()&pn.keys() if sn[g]!=pn[g]]
        row[family]={'checks':summary,'net_count':len(nets),'shared_pin_count':len(shared),'connectivity_mismatch_pins':mismatches,'schematic_net_nodes_missing_from_pcb_nets':missingpcb,'pcb_net_nodes_missing_from_schematic_nets':missingsch,'same_membership_net_aliases':aliases}
        row[family]['led_symbol_pins']=allpins(next(x for x in children(one(sch,'lib_symbols'),'symbol') if x[1] in ['LED:SK6812','Saiboard_LED:SKC6812RGBW-WS']))
        if family=='original': origpcb,origsch,orignets=pcb,sch,nets
        else:
            row['pcb_equal_after_declared_identity_changes']=canonical(origpcb)==canonical(pcb)
            row['sch_equal_after_declared_identity_changes']=canonical(origsch)==canonical(sch)
            row['native_net_names_and_nodes_equal']=orignets==nets
    results[d]=row
dump('CONNECTIVITY_AND_CHECKS.json',results)

struct=json.loads((A/'STRUCTURAL_DIFF.json').read_text())
history={}
for d in DESIGNS:
    folder=S/'kicad_files'/d/'gerbers'
    job=json.loads((folder/(d+'-job.gbrjob')).read_text())
    text=(folder/(d+'-Edge_Cuts.gbr')).read_text()
    assert '%MOMM*%' in text and '%FSLAX46Y46*%' in text
    points=[(int(x)/1e6,-int(y)/1e6) for x,y in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',text)]
    bbox=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)]
    drillrows=[]
    counts={}
    for kind in ['PTH','NPTH']:
        t=(folder/(d+'-'+kind+'.drl')).read_text()
        assert 'METRIC' in t and 'G85' not in t and not re.search(r'^R\d',t,re.M)
        tools={m[0]:float(m[1]) for m in re.findall(r'^T(\d+)C([\d.]+)',t,re.M)}
        tool=None
        for line in t.splitlines():
            if re.fullmatch(r'T\d+',line):tool=line[1:]
            xy=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
            if xy:drillrows.append({'kind':kind,'x':float(xy[1]),'y':-float(xy[2]),'diameter':tools[tool]})
        counts[kind]=sum(x['kind']==kind for x in drillrows)
    geom=struct[d]['versions']['original']['geometry']
    def holekey(x): return (round(x['x'],3),round(x['y'],3),round(x['diameter'],3),x['kind'])
    sourceholes=[{'x':x['x'],'y':x['y'],'diameter':float(x['drill'][0]),'kind':'NPTH' if x['type']=='np_thru_hole' else 'PTH'} for x in geom['holes']]
    old=collections.Counter(map(holekey,drillrows));new=collections.Counter(map(holekey,sourceholes))
    remaining=list(sourceholes)
    offsets=[]
    for hole in drillrows:
        candidates=[(math.hypot(hole['x']-x['x'],hole['y']-x['y']),i) for i,x in enumerate(remaining) if hole['kind']==x['kind'] and abs(hole['diameter']-x['diameter'])<1e-6]
        distance,index=min(candidates)
        offsets.append(distance)
        remaining.pop(index)
    with zipfile.ZipFile(folder/'gerber.zip') as z:
        zipmatches={x.filename:sha(folder/Path(x.filename).name)==hashlib.sha256(z.read(x)).hexdigest() for x in z.infolist() if not x.is_dir() and (folder/Path(x.filename).name).is_file()}
    history[d]={'generator':job['Header'],'project_id':job['GeneralSpecs']['ProjectId'],'gerber_outline_bbox_mm':bbox,'gerber_outline_size_mm':[round(bbox[2]-bbox[0],6),round(bbox[3]-bbox[1],6)],'source_outline_bbox_mm':geom['outline_bbox_mm'],'outline_matches':bbox==geom['outline_bbox_mm'],'job_size_mm':job['GeneralSpecs']['Size'],'layer_count':job['GeneralSpecs']['LayerNumber'],'source_layer_count':geom['layer_count'],'drills':counts,'source_drill_count':len(sourceholes),'drill_geometry_matches_0_001mm':old==new,'historical_only_holes':list((old-new).elements()),'source_only_holes':list((new-old).elements()),'zip_loose_matches':zipmatches,'revision_attribution':'UNVERIFIED exact revision: ProjectId.Revision is rev?; outline/layer/drill evidence does not identify an electrical revision. Original and update have identical physical geometry.'}
    history[d]['max_hole_coordinate_distance_mm']=max(offsets)
    history[d]['holes_match_within_0_001mm']=not remaining and max(offsets)<=0.001
dump('HISTORICAL_FAB_COMPARISON.json',history)
for d,row in results.items():
    print(d,json.dumps({k:v for k,v in row.items() if k not in ['original','updated']}))
    for f in ['original','updated']:print(f,json.dumps({'checks':row[f]['checks'],'connectivity_mismatch_pins':len(row[f]['connectivity_mismatch_pins']),'schematic_nodes_missing':len(row[f]['schematic_net_nodes_missing_from_pcb_nets']),'pcb_nodes_missing':len(row[f]['pcb_net_nodes_missing_from_schematic_nets']),'aliases':len(row[f]['same_membership_net_aliases'])}))
    print('historical',json.dumps({k:v for k,v in history[d].items() if k not in ['zip_loose_matches','generator','project_id']}))
