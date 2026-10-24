"""Lossless, review-gated IW story extraction and same-branch merge (standard library).

plan SOURCE --world WORLD --session NAME --branch NAME > plan.json
build PLAN... --output NEW_DIRECTORY [--partial]

Plans propose line boundaries; mark reviewed=true only after reviewing them.
Native text has unescaped delimiters, so inferred boundaries are not authoritative.
Build validates hashes and explicit spans, rejects conflicts, and writes a fresh
atomic output directory. It never overwrites a prior extraction or source file.
"""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,tempfile

HEADINGS={'Action':'action','Outcome':'outcome','Secret Information':'secretInfo','Tracked Items':'trackedItems','Hidden Tracked Items':'hiddenTrackedItems'}
ORDER={v:i for i,v in enumerate(HEADINGS.values())}
MARKER=re.compile(r'^-- Turn ([1-9][0-9]*) --$')

def digest(data):return hashlib.sha256(data).hexdigest()
def load_source(path):
    raw=Path(path).read_bytes()
    text=raw.decode('utf-8-sig')
    lines=text.replace('\r\n','\n').replace('\r','\n').split('\n')
    if lines and lines[-1]=='':lines.pop()
    return raw,lines
def text_span(lines,start,end):return '\n'.join(lines[start-1:end])
def check_span(start,end,low,high):
    if type(start)!=int or type(end)!=int or not low<=start<=end<=high:
        raise ValueError('Invalid or out-of-range line span')

def propose(path,names,session,branch):
    if not session or not branch:raise ValueError('Explicit session and branch are required')
    if len(set(names))!=len(names):raise ValueError('Duplicate tracker Names require manually resolved boundaries')
    raw,lines=load_source(path)
    markers=[(i+1,int(m[1])) for i,line in enumerate(lines) if (m:=MARKER.fullmatch(line))]
    if not markers:raise ValueError('No turn markers found')
    turns=[];issues=[]
    for idx,(start,number) in enumerate(markers):
        end=markers[idx+1][0]-1 if idx+1<len(markers) else len(lines)
        hits=[(i+1,HEADINGS[lines[i]]) for i in range(start,end-1) if lines[i] in HEADINGS and re.fullmatch('-{4,}',lines[i+1])]
        sections=[]
        for j,(header,kind) in enumerate(hits):
            stop=hits[j+1][0]-1 if j+1<len(hits) else end
            sec={'kind':kind,'headerLine':header,'endLine':stop}
            if kind in ('trackedItems','hiddenTrackedItems'):
                found=[(k+1,lines[k][:-1]) for k in range(header+1,stop) if lines[k].endswith(':') and lines[k][:-1] in names]
                sec['trackers']=[{'name':name,'startLine':pos,'endLine':found[n+1][0]-1 if n+1<len(found) else stop} for n,(pos,name) in enumerate(found)]
                if len({name for _,name in found})!=len(found):issues.append('Duplicate possible tracker header at turn '+str(number))
                if not found and any(x.strip() for x in lines[header+1:stop]):issues.append('Unresolved tracker section at turn '+str(number))
            sections.append(sec)
        kinds=[s['kind'] for s in sections]
        if kinds!=sorted(set(kinds),key=lambda k:ORDER[k]) or 'outcome' not in kinds:issues.append('Ambiguous/missing section boundaries at turn '+str(number))
        turns.append({'number':number,'startLine':start,'endLine':end,'sections':sections})
    nums=[t['number'] for t in turns]
    if nums!=list(range(nums[0],nums[0]+len(nums))):issues.append('Nonconsecutive or duplicate proposed turn markers')
    return {'version':1,'session':session,'branch':branch,'reviewed':False,'path':str(Path(path).resolve()),'sha256':digest(raw),'trackerNames':list(names),'turns':turns,'reviewIssues':issues,'boundaryNotice':'Unescaped text can imitate turn, section or tracker headings. Review and correct spans; reviewed=true is an operator assertion, not inferred certainty.'}

def extract(plan):
    if plan.get('reviewed') is not True:raise ValueError('Review line boundaries and set reviewed=true before extraction')
    if not isinstance(plan.get('session'),str) or not plan['session'].strip() or not isinstance(plan.get('branch'),str) or not plan['branch'].strip():raise ValueError('Explicit nonempty session and branch required')
    if plan.get('reviewIssues'):raise ValueError('Resolve reviewIssues and clear them after reviewing the layout')
    raw,lines=load_source(plan['path'])
    if digest(raw)!=plan.get('sha256'):raise ValueError('Source SHA256 mismatch; regenerate/review plan')
    turns=plan.get('turns',[])
    if not isinstance(turns,list) or not turns:raise ValueError('Plan needs explicit turn spans')
    parsed=[];last_end=None;last_num=None
    names=plan.get('trackerNames',[])
    if not isinstance(names,list) or not all(isinstance(n,str) and n for n in names) or len(names)!=len(set(names)):raise ValueError('Tracker Names must be unique nonempty strings')
    for turn in turns:
        n=turn['number'];start=turn['startLine'];end=turn['endLine']
        check_span(start,end,1,len(lines))
        if type(n)!=int or n<1 or lines[start-1]!=f'-- Turn {n} --':raise ValueError('Turn marker does not match approved span')
        if last_end is not None and (start!=last_end+1 or n!=last_num+1):raise ValueError('Turn spans must be contiguous and sequential within a source')
        last_end,last_num=end,n
        sections=turn['sections'];kinds=[s['kind'] for s in sections]
        if 'outcome' not in kinds or any(k not in ORDER for k in kinds) or kinds!=sorted(set(kinds),key=lambda k:ORDER[k]):raise ValueError('Invalid/duplicate section sequence')
        data={'number':n,'sections':{},'trackedItems':{},'hiddenTrackedItems':{}}
        prev=start
        for idx,sec in enumerate(sections):
            h,e=sec['headerLine'],sec['endLine'];check_span(h,e,start+1,end)
            expected_end=sections[idx+1]['headerLine']-1 if idx+1<len(sections) else end
            if h<=prev or e!=expected_end:raise ValueError('Overlapping or incomplete section spans')
            if idx==0 and any(x.strip() for x in lines[start:h-1]):raise ValueError('Unclassified text before first section')
            label=next(k for k,v in HEADINGS.items() if v==sec['kind'])
            if lines[h-1]!=label or h>=e or not re.fullmatch('-{4,}',lines[h]):raise ValueError('Section header does not match approved span')
            prev=e
            body=text_span(lines,h+2,e) if h+2<=e else ''
            data['sections'][sec['kind']]=body
            if sec['kind'] in ('trackedItems','hiddenTrackedItems'):
                ts=sec.get('trackers',[]);previous=h+1
                for j,item in enumerate(ts):
                    a,b=item['startLine'],item['endLine'];name=item['name'];check_span(a,b,h+2,e)
                    boundary=ts[j+1]['startLine']-1 if j+1<len(ts) else e
                    if a<=previous or b!=boundary or name not in names or lines[a-1]!=name+':' or name in data[sec['kind']]:raise ValueError('Invalid/duplicate tracker boundary')
                    if j==0 and any(x.strip() for x in lines[h+1:a-1]):raise ValueError('Unclassified tracker text before first Name')
                    data[sec['kind']][name]=text_span(lines,a+1,b) if a<b else ''
                    previous=b
                if not ts and body.strip():raise ValueError('Unresolved tracker section; provide reviewed Name boundaries')
        if set(data['trackedItems']) & set(data['hiddenTrackedItems']):raise ValueError('Same tracker Name in visible and hidden sections is ambiguous')
        data['content']=text_span(lines,start,end).rstrip('\n')
        data['contentSha256']=digest(data['content'].encode('utf8'))
        data['provenance']=[{'sourceSha256':digest(raw),'path':str(Path(plan['path']).resolve()),'lineRange':[start,end]}]
        parsed.append(data)
    if last_end!=len(lines):raise ValueError('Unclassified text after final turn span')
    return parsed

def merge(plans,partial=False):
    if not plans:raise ValueError('No sources')
    identity={(p.get('session'),p.get('branch')) for p in plans}
    if len(identity)!=1:raise ValueError('Different sessions/branches cannot be merged; select a branch explicitly')
    merged={}
    for plan in plans:
        for turn in extract(plan):
            n=turn['number']
            if n in merged:
                old=merged[n]
                # Identical text is insufficient if operators approved different parsing.
                if any(old[k]!=turn[k] for k in ('content','sections','trackedItems','hiddenTrackedItems')):raise ValueError(f'Conflicting turn {n}; choose/reconcile a branch before merging. No timestamp winner.')
                old['provenance'].extend(turn['provenance'])
            else:merged[n]=turn
    nums=sorted(merged)
    if nums!=list(range(nums[0],nums[-1]+1)) or (not partial and nums[0]!=1):raise ValueError('History has gaps or missing initial turns; partial only permits a contiguous later range')
    for t in merged.values():t['provenance']=sorted({json.dumps(p,sort_keys=True):p for p in t['provenance']}.values(),key=lambda p:(p['sourceSha256'],p['lineRange'],p['path']))
    session,branch=next(iter(identity))
    return {'session':session,'branch':branch,'partial':bool(partial),'boundaryAssurance':'operator-reviewed; text format is unescaped','turns':[merged[n] for n in nums]}

def publish(plans,destination,partial=False):
    dest=Path(destination).resolve()
    if dest.exists():raise ValueError('Output must be a new directory; existing extractions are never overwritten')
    result=merge(plans,partial)
    if not dest.parent.is_dir():raise ValueError('Output parent must exist')
    stage=Path(tempfile.mkdtemp(prefix='.iw-story-',dir=dest.parent))
    # The only cleanup target is this tool-created sibling staging directory.
    assert stage.parent==dest.parent and stage.name.startswith('.iw-story-')
    try:
        src=stage/'sources';src.mkdir();records=[]
        for p in sorted(plans,key=lambda p:(p['sha256'],p['path'])):
            raw=Path(p['path']).read_bytes()
            if digest(raw)!=p['sha256']:raise ValueError('Source changed during publication')
            name='sources/'+p['sha256']+'.txt';(stage/name).write_bytes(raw)
        (stage/'reviewed-plans.json').write_text(json.dumps(plans,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
        (stage/'story.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
        for p in sorted(stage.rglob('*')):
            if p.is_file():records.append({'path':p.relative_to(stage).as_posix(),'sha256':digest(p.read_bytes())})
        manifest={'version':1,'session':result['session'],'branch':result['branch'],'partial':result['partial'],'files':records}
        (stage/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
        for rec in records:
            if digest((stage/rec['path']).read_bytes())!=rec['sha256']:raise ValueError('Staging integrity failure')
        # Same-volume rename publishes the complete directory; it cannot replace a nonempty prior extraction.
        if dest.exists():raise ValueError('Output appeared during publication')
        stage.rename(dest)
    finally:
        if stage.exists():shutil.rmtree(stage)
    return manifest

def verify_archive(directory):
    root=Path(directory).resolve()
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf8'))
    seen=set()
    for entry in manifest['files']:
        name=entry['path']
        if not isinstance(name,str) or name in seen:raise ValueError('Duplicate or invalid manifest path')
        path=(root/name).resolve()
        if Path(name).is_absolute() or not path.is_relative_to(root) or path==root:raise ValueError('Unsafe manifest path')
        if digest(path.read_bytes())!=entry['sha256']:raise ValueError('Archive hash mismatch: '+name)
        seen.add(name)
    if not {'story.json','reviewed-plans.json'}<=seen:raise ValueError('Missing required archive entries')
    story=json.loads((root/'story.json').read_text(encoding='utf8'))
    if any(story.get(k)!=manifest.get(k) for k in ('session','branch','partial')):raise ValueError('Archive identity mismatch')
    return {'session':story['session'],'branch':story['branch'],'partial':story['partial'],'turns':len(story['turns']),'verifiedFiles':len(seen),'note':'Only manifest-listed files were read; unlisted directory contents are not extraction output.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('plan');p.add_argument('source',type=Path);p.add_argument('--world',type=Path,required=True);p.add_argument('--session',required=True);p.add_argument('--branch',required=True)
    b=sub.add_parser('build');b.add_argument('plans',nargs='+',type=Path);b.add_argument('--output',required=True,type=Path);b.add_argument('--partial',action='store_true')
    v=sub.add_parser('verify');v.add_argument('directory',type=Path)
    a=parser.parse_args()
    try:
        if a.command=='plan':
            w=json.loads(a.world.read_text(encoding='utf-8-sig'));out=propose(a.source,[t['name'] for t in w.get('trackedItems',[])],a.session,a.branch)
        elif a.command=='build':out=publish([json.loads(p.read_text(encoding='utf-8-sig')) for p in a.plans],a.output,a.partial)
        else:out=verify_archive(a.directory)
    except (ValueError,KeyError,TypeError,OSError) as e:parser.exit(2,str(e)+'\n')
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
