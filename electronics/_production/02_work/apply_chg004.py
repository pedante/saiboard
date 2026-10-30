"""Apply approved provisional LED identity fields; prove all other parsed content identical."""
from phase1_audit import *
import difflib

B=P/'02_work/baseline'
BACK=P/'02_work/baseline_before_CHG004'
E=P/'01_audit/CHG-004'
assert not B.exists() and not BACK.exists(), 'Refusing to overwrite either baseline'
E.mkdir(exist_ok=True)
manifest=json.loads((A/'PROPOSED_BASELINE_MANIFEST.json').read_text())['files']
for row in manifest:
    src=S/row['path'];assert sha(src)==row['sha256']
    for dest in [B,BACK]:
        target=dest/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,target);target.chmod(0o644 if dest==B else 0o444)

def spans(text):
    depth=0;start=None;found=[]
    for m in re.finditer(r'"(?:\\.|[^"\\])*"|;[^\n]*|[()]',text):
        t=m.group()
        if t=='(':
            depth+=1
            if depth==2:start=m.start()
        elif t==')':
            if depth==2:found.append((start,m.end()))
            depth-=1
    assert depth==0
    return found

def replace_field(block,tag,name,new):
    pattern=r'(\('+tag+r' '+re.escape(name)+r' )"(?:\\.|[^"\\])*"'
    result,count=re.subn(pattern,lambda m:m[1]+json.dumps(new,ensure_ascii=False),block,count=1)
    assert count==1,(tag,name)
    return result

assert [parse('(a (b "(") (c 1))'[i:j])[0] for i,j in spans('(a (b "(") (c 1))')]==['b','c']
records=[];diffs=[];coverage={}
fields=['Manufacturer','MPN','LCSC','AssemblyStatus']
for d in DESIGNS:
    counts={}
    for suffix in ['.kicad_sch','.kicad_pcb']:
        rel=Path('kicad_files')/d/(d+suffix);original=(S/rel).read_text()
        candidate=(S/'updated_components_SKC6812RGBW-WS'/rel).read_text()
        pcb=suffix=='.kicad_pcb';tag='footprint' if pcb else 'symbol'
        candidates={ref(parse(candidate[i:j]),pcb):candidate[i:j] for i,j in spans(candidate) if parse(candidate[i:j])[0]==tag}
        edits=[];refs=[]
        for i,j in spans(original):
            block=original[i:j];node=parse(block)
            if node[0]==tag and ref(node,pcb).startswith('D'):
                r=ref(node,pcb);refs.append(r)
                value=next((x[2] for x in children(node,'fp_text') if x[1]=='value'),None) if pcb else props(node)['Value']
                assert value=='SK6812', (d,r,value)
                new=replace_field(block,'fp_text','value','SKC6812RGBW-WS') if pcb else replace_field(block,'property','"Value"','SKC6812RGBW-WS')
                if not pcb:new=replace_field(new,'property','"Datasheet"',props(parse(candidates[r]))['Datasheet'])
                added=[]
                for ci,cj in spans(candidates[r]):
                    prop=parse(candidates[r][ci:cj])
                    if prop[0]=='property' and prop[1] in fields:
                        item=candidates[r][ci:cj]
                        if prop[1]=='AssemblyStatus':item=replace_field(item.replace('(property','(root (property',1)+')','property','"AssemblyStatus"','Applied-provisional - CHG-004; Phase 3 verification required')[6:-1]
                        added.append(item)
                assert len(added)==4
                new=new[:-1]+'\n    '+'\n    '.join(added)+'\n  )'
                edits.append((i,j,new));records.append({'design':d,'file':str(rel),'reference':r,'before':props(node) if not pcb else footprint(node),'after':props(parse(new)) if not pcb else footprint(parse(new))})
            elif node[0]=='symbol_instances':
                changes=[]
                for pi,pj in spans(block):
                    path=parse(block[pi:pj])
                    if one(path,'reference','')[1].startswith('D'):
                        changes.append((pi,pj,replace_field(block[pi:pj],'value','', 'SKC6812RGBW-WS') if False else re.sub(r'\(value "SK6812"\)','(value "SKC6812RGBW-WS")',block[pi:pj])))
                for pi,pj,text in reversed(changes):block=block[:pi]+text+block[pj:]
                edits.append((i,j,block))
        counts[suffix]=refs
        modified=original
        for i,j,text in reversed(edits):modified=modified[:i]+text+modified[j:]
        # Reverse only the allowed field edits to prove no circuit/library/geometry change.
        tree=parse(modified)
        for node in children(tree,tag):
            if ref(node,pcb) in refs:
                node[:]=[x for x in node if not (isinstance(x,list) and x[0]=='property' and x[1] in fields)]
                if pcb:
                    for x in children(node,'fp_text'):
                        if x[1]=='value':x[2]='SK6812'
                else:
                    for x in children(node,'property'):
                        if x[1]=='Value':x[2]='SK6812'
                        if x[1]=='Datasheet':x[2]=props(next(x for x in children(parse(original),'symbol') if ref(x)==ref(node)))['Datasheet']
        for instances in children(tree,'symbol_instances'):
            for node in children(instances,'path'):
                if one(node,'reference','')[1] in refs:one(node,'value')[1]='SK6812'
        assert tree==parse(original), 'STOP: non-identity difference'
        (B/rel).write_text(modified)
        delta=''.join(difflib.unified_diff(original.splitlines(True),modified.splitlines(True),fromfile='original/'+str(rel),tofile='baseline/'+str(rel)))
        (E/(d+suffix+'.diff')).write_text(delta);diffs.append(delta)
    assert counts['.kicad_sch']==counts['.kicad_pcb'] or set(counts['.kicad_sch'])==set(counts['.kicad_pcb'])
    coverage[d]={'original_LED_count':len(counts['.kicad_pcb']),'updated_LED_count':len(counts['.kicad_pcb']),'references':counts['.kicad_pcb'],'uncovered':[]}
assert sum(x['original_LED_count'] for x in coverage.values())==145
for row in manifest:
    assert sha(BACK/row['path'])==row['sha256']
    if Path(row['path']).suffix not in ['.kicad_sch','.kicad_pcb']:assert sha(B/row['path'])==row['sha256']
for path in sorted(BACK.rglob('*'),reverse=True):
    if path.is_dir():path.chmod(0o555)
BACK.chmod(0o555)
(E/'ORIGINAL_TO_BASELINE.diff').write_text(''.join(diffs))
(E/'FIELD_CHANGES.json').write_text(json.dumps(records,indent=2)+'\n')
(E/'VERIFICATION.json').write_text(json.dumps({'change_id':'CHG-004','status':'Applied-provisional','approval_date':'2026-10-29','coverage':coverage,'total_original_LEDs':145,'total_updated_LEDs':145,'uncovered_LEDs':[],'original_embedded_symbols_and_library_ids_preserved':True,'complete_tree_equal_after_reversing_allowed_fields':True,'backup_matches_original_manifest':True,'baseline_files':[{**r,'baseline_sha256':sha(B/r['path'])} for r in manifest]},indent=2)+'\n')
print(json.dumps({'status':'Applied-provisional','coverage':coverage,'diff':'01_audit/CHG-004/ORIGINAL_TO_BASELINE.diff','backup':str(BACK)},indent=2))
