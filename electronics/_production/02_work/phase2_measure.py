"""Source geometry and metadata measurements, without writing EDA inputs."""
from phase1_audit import *
import html
import itertools

BASE=P/'02_work/baseline/kicad_files'
OUT=P/'01_audit/phase2'

def fpvalue(f):
    return next(x[2] for x in children(f,'fp_text') if x[1]=='value')

def transform(f,x,y):
    at=one(f,'at');angle=math.radians(float(at[3]) if len(at)>3 else 0)
    return float(at[1])+x*math.cos(angle)+y*math.sin(angle),float(at[2])-x*math.sin(angle)+y*math.cos(angle)

def padbox(f,p):
    at=one(p,'at');x,y=transform(f,*map(float,at[1:3]));sx,sy=map(float,one(p,'size')[1:3])
    angle=float(at[3]) if len(at)>3 else 0
    assert abs(angle/90-round(angle/90))<1e-8, 'nonorthogonal pad requires polygon distance'
    if round(angle/90)%2:sx,sy=sy,sx
    return [x-sx/2,y-sy/2,x+sx/2,y+sy/2]

def boxgap(a,b):
    return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))

assert boxgap([0,0,1,1],[2,0,3,1])==1
assert transform(['f',['at','10','20','90']],1,0)==(10,19)

result={};variants={};gallery=[]
for d in DESIGNS:
    b=parse((BASE/d/(d+'.kicad_pcb')).read_text());s=parse((BASE/d/(d+'.kicad_sch')).read_text())
    syms={ref(x):x for x in children(s,'symbol') if not ref(x).startswith('#')}
    fs=children(b,'footprint');geom=board_geometry(b);outline=geom['outline_bbox_mm']
    boxes=[];pads=[];unassigned=[];mismatches=[];no_fab=[];thin=[];silktext=[]
    for f in fs:
        r=ref(f,True);sym=syms.get(r);v=props(sym).get('Value') if sym else None
        if sym and v!=fpvalue(f):mismatches.append({'reference':r,'schematic':v,'pcb':fpvalue(f)})
        art=[x for x in f if isinstance(x,list) and x[0].startswith('fp_')]
        if not any(one(x,'layer','')[1].endswith('.Fab') for x in art):no_fab.append(r)
        for x in art:
            layer=one(x,'layer','')[1]
            if not layer.endswith('.SilkS'):continue
            if x[0]=='fp_text':
                if 'hide' in x or 'hide' in one(x,'layer'):continue
                font=one(one(x,'effects'),'font');silktext.append({'reference':r,'text':x[2],'size':one(font,'size')[1:],'stroke':one(font,'thickness')[1:]})
            elif one(x,'width') and float(one(x,'width')[1])<.15-1e-9:thin.append({'reference':r,'kind':x[0],'width':float(one(x,'width')[1]),'uuid':one(x,'tstamp')[1:]})
        pad_data=[]
        for pad in children(f,'pad'):
            bounds=padbox(f,pad);layers=one(pad,'layers')[1:];net=one(pad,'net','0')[1:]
            pad_data.append({'number':pad[1],'type':pad[2],'shape':pad[3],'at':one(pad,'at')[1:3],'size':one(pad,'size')[1:],'layers':layers,'pinfunction':one(pad,'pinfunction')[1:]})
            if pad[2]=='np_thru_hole':continue
            if not one(pad,'net'):unassigned.append({'reference':r,'pad':pad[1],'position':transform(f,*map(float,one(pad,'at')[1:3]))})
            boxes.append(('pad '+r+'.'+pad[1],bounds))
            pads.append({'reference':r,'pad':pad[1],'bounds':bounds,'layers':layers,'net':net,'size':list(map(float,one(pad,'size')[1:]))})
        key=json.dumps([v,f[1],pad_data],sort_keys=True)
        if key not in variants:
            vid='FP-%02d'%(len(variants)+1)
            variants[key]={'id':vid,'value':v,'footprint':f[1],'designators':[],'pads':pad_data,'example':d+'/'+r}
            gallery.append((vid,d,r,f))
        variants[key]['designators'].append(d+'/'+r)
    for x in children(b,'segment'):
        sx,sy=map(float,one(x,'start')[1:3]);ex,ey=map(float,one(x,'end')[1:3]);rad=float(one(x,'width')[1])/2
        boxes.append(('track '+one(x,'tstamp')[1],[min(sx,ex)-rad,min(sy,ey)-rad,max(sx,ex)+rad,max(sy,ey)+rad]))
    for x in children(b,'via'):
        px,py=map(float,one(x,'at')[1:3]);rad=float(one(x,'size')[1])/2;boxes.append(('via',[px-rad,py-rad,px+rad,py+rad]))
    for z in children(b,'zone'):
        for poly in children(z,'filled_polygon'):
            pts=[list(map(float,x[1:3])) for x in children(one(poly,'pts'),'xy')]
            boxes.append(('stored zone '+one(z,'net_name','')[1],[min(x[0] for x in pts),min(x[1] for x in pts),max(x[0] for x in pts),max(x[1] for x in pts)]))
    edges=sorted((min(bb[0]-outline[0],bb[1]-outline[1],outline[2]-bb[2],outline[3]-bb[3]),label) for label,bb in boxes)
    holes=geom['holes'];holegaps=[]
    for a,bh in itertools.combinations(holes,2):
        gap=math.hypot(a['x']-bh['x'],a['y']-bh['y'])-(float(a['drill'][0])+float(bh['drill'][0]))/2
        holegaps.append((gap,a,bh))
    padgaps=[]
    for a,bp in itertools.combinations(pads,2):
        if a['net']==bp['net'] or not set(a['layers'])&set(bp['layers'])&{'F.Cu','B.Cu'}:continue
        padgaps.append((boxgap(a['bounds'],bp['bounds']),a['reference']+'.'+a['pad'],bp['reference']+'.'+bp['pad']))
    nets=parse((OUT/'native/baseline'/d/'netlist.net').read_text())
    old=parse((P/'01_audit/phase1/native/original'/d/'netlist.net').read_text())
    assert one(nets,'nets')==one(old,'nets'),d+' native connectivity changed'
    checks={}
    for mode in ['baseline','jlc_screen']:
        j=json.loads((OUT/'native'/mode/d/'drc.json').read_text())
        checks[mode]={k:{'total':len(j[k]),'types':dict(collections.Counter(x['type'] for x in j[k])),'severities':dict(collections.Counter(x['severity'] for x in j[k]))} for k in ['violations','unconnected_items','schematic_parity']}
    erc=json.loads((OUT/'native/baseline'/d/'erc.json').read_text());ev=[v for sh in erc['sheets'] for v in sh['violations']]
    checks['erc']={'types':dict(collections.Counter(v['type'] for v in ev)),'severities':dict(collections.Counter(v['severity'] for v in ev))}
    result[d]={'geometry':geom,'component_sides':dict(collections.Counter(one(f,'layer')[1] for f in fs if ref(f,True) in syms)),
      'direct_value_mismatches':mismatches,'unnumbered_or_unassigned_copper_pads':unassigned,
      'footprints_without_fab_art':no_fab,'thin_silk_graphics':thin,'visible_silk_text':silktext,
      'minimum_track_width':min(float(one(x,'width')[1]) for x in children(b,'segment')),
      'via_size_drill_counts':dict(collections.Counter(str((one(x,'size')[1],one(x,'drill')[1])) for x in children(b,'via'))),
      'minimum_copper_to_outline_bounds_mm':edges[0],'nearest_holes':min(holegaps,key=lambda x:x[0]),
      'minimum_different_net_pad_bounding_box_gap_mm':min(padgaps),'minimum_smd_pad_dimension':min(min(x['size']) for x in pads),
      'mask_expansion_mm':one(one(b,'setup'),'pad_to_mask_clearance')[1:],
      'baseline_native_net_names_and_members_equal_original':True,'checks':checks}
(OUT/'MEASUREMENTS.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'FOOTPRINT_VARIANTS.json').write_text(json.dumps(list(variants.values()),indent=2)+'\n')
# Audit illustration uses local footprint coordinates already mirrored in source for back-side footprints.
seen_geometry=set();unique_gallery=[]
for item in gallery:
    f=item[3]
    key=json.dumps([f[1],one(f,'layer')[1:],[(p[1:4],one(p,'at')[1:3],one(p,'size')[1:]) for p in children(f,'pad')]])
    if key not in seen_geometry:
        seen_geometry.add(key);unique_gallery.append(item)
gallery=unique_gallery
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="%d">'%(320*((len(gallery)+3)//4)+70),'<rect width="100%" height="100%" fill="white"/>','<text x="15" y="25" font-size="18">Source footprint audit: copper gold, silk blue, fabrication green; pad numbers overlaid. Not CPL orientation.</text>']
for i,(vid,d,r,f) in enumerate(gallery):
    x=(i%4)*350;y=(i//4)*320+50
    coords=[]
    for p in children(f,'pad'):
        at=one(p,'at');sz=one(p,'size');px,py=map(float,at[1:3]);sx,sy=map(float,sz[1:3]);coords += [(px-sx/2,py-sy/2),(px+sx/2,py+sy/2)]
    mnx=min(c[0] for c in coords)-3;mny=min(c[1] for c in coords)-3;w=max(c[0] for c in coords)-mnx+3;h=max(c[1] for c in coords)-mny+3
    svg.append(f'<text x="{x+10}" y="{y+18}" font-size="14">{vid}: {d}/{r} {html.escape(fpvalue(f))}</text>')
    svg.append(f'<svg x="{x+10}" y="{y+30}" width="330" height="270" viewBox="{mnx} {mny} {w} {h}">')
    for z in f:
        if not isinstance(z,list):continue
        layer=one(z,'layer','')[1];color='#2575c4' if layer.endswith('.SilkS') else '#159457' if layer.endswith('.Fab') else None
        if color and z[0]=='fp_line':
            sx,sy=one(z,'start')[1:3];ex,ey=one(z,'end')[1:3];width=one(z,'width','.1')[1]
            svg.append(f'<path d="M{sx} {sy}L{ex} {ey}" stroke="{color}" stroke-width="{width}" fill="none"/>')
        if color and z[0]=='fp_circle':
            cx,cy=map(float,one(z,'center')[1:3]);ex,ey=map(float,one(z,'end')[1:3]);rr=math.hypot(ex-cx,ey-cy)
            svg.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" stroke="{color}" stroke-width=".15" fill="none"/>')
        if color and z[0]=='fp_text' and z[2] in ['+','-']:
            tx,ty=one(z,'at')[1:3];svg.append(f'<text x="{tx}" y="{ty}" font-size="1" fill="{color}">{z[2]}</text>')
    for pad in children(f,'pad'):
        px,py=map(float,one(pad,'at')[1:3]);sx,sy=map(float,one(pad,'size')[1:3]);rad=float(one(pad,'roundrect_rratio','0')[1])*min(sx,sy)
        if pad[2]=='np_thru_hole':
            svg.append(f'<circle cx="{px}" cy="{py}" r="{float(one(pad,"drill")[1])/2}" stroke="#666" stroke-width=".1" fill="white"/>')
            continue
        svg.append(f'<rect x="{px-sx/2}" y="{py-sy/2}" width="{sx}" height="{sy}" rx="{rad}" fill="#d9ae39"/>')
        svg.append(f'<text x="{px}" y="{py+.12}" text-anchor="middle" font-size=".45">{pad[1]}</text>')
    svg.append('</svg>')
svg.append('</svg>');(OUT/'FOOTPRINT_GALLERY.svg').write_text('\n'.join(svg))
for d,j in result.items():
    print(d, 'value mismatches',len(j['direct_value_mismatches']),'unnetted pads',j['unnumbered_or_unassigned_copper_pads'], 'edge',j['minimum_copper_to_outline_bounds_mm'],'hole gap',round(j['nearest_holes'][0],4),'pad bbox gap',j['minimum_different_net_pad_bounding_box_gap_mm'],'thin graphics',len(j['thin_silk_graphics']))
print('Footprint variants:',len(variants))
