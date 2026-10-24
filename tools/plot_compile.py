"""Compile a literal-Scenario prerequisite DAG into a new IW world. No runtime inference."""
from __future__ import annotations
import argparse,copy,hashlib,json,re
from pathlib import Path


def analyze(plan):
    if not isinstance(plan,dict) or not isinstance(plan.get('nodes'),list) or not plan['nodes']:
        raise ValueError('Plan needs a nonempty nodes list')
    if set(plan)-{'title','nodes'}:raise ValueError('Unknown plan field')
    if not isinstance(plan.get('title'),str) or not plan['title'].strip():raise ValueError('Plan needs a title')
    nodes=plan['nodes']; by={}
    for n in nodes:
        if not isinstance(n,dict) or set(n)-{'id','name','scenario','requires','award'}:raise ValueError('Unknown node field or invalid node')
        key=n.get('id')
        if not isinstance(key,str) or not re.fullmatch('[a-z][a-z0-9_]*',key):raise ValueError('Node id must be a lowercase identifier')
        if key == 'score':raise ValueError('score is reserved')
        if key in by:raise ValueError('Duplicate node id: '+key)
        if any(not isinstance(n.get(k),str) or not n[k].strip() for k in ('name','scenario')):raise ValueError('Each node needs Name and literal Scenario')
        if any(x in n['scenario'] for x in ('<<','<=','<#')):raise ValueError('Dynamic Scenarios are outside this compiler contract')
        deps=n.get('requires',[])
        if not isinstance(deps,list) or any(not isinstance(d,str) for d in deps) or len(set(deps))!=len(deps):raise ValueError('requires must contain unique node ids')
        award=n.get('award',0)
        if type(award)!=int or award<0:raise ValueError('award must be a nonnegative integer')
        by[key]=n
    for key,n in by.items():
        for d in n.get('requires',[]):
            if d not in by:raise ValueError('Unknown prerequisite '+d+' on '+key)
    pending=list(by);order=[]
    while pending:
        ready=[k for k in pending if all(d in order for d in by[k].get('requires',[]))]
        if not ready:raise ValueError('Cyclic prerequisites: '+', '.join(pending))
        order.extend(ready);pending=[k for k in pending if k not in ready]
    groups={}
    for n in nodes:groups.setdefault(n['scenario'],[]).append(n['name'])
    return {'order':order,'structurallyReachable':order,'roots':[k for k in order if not by[k].get('requires')],
            'sharedScenarios':{s:n for s,n in groups.items() if len(n)>1},
            'scope':'All-of prerequisite connectivity only. Scenario recognition, timing, character knowledge and narrative satisfiability are not proved. Shared Scenarios may complete several nodes in the same turn.'}


def identity(kind,key):return hashlib.sha256((kind+':'+key).encode()).hexdigest()[:18]


def compile_world(plan,template):
    report=analyze(plan);w=copy.deepcopy(template)
    # Always a fresh scaffold, never merge over an existing authored world.
    if template.get('trackedItems') or template.get('triggerEvents'):raise ValueError('Template must have no trackers or triggers')
    w.update(title=plan['title'],description='A literal-Scenario prerequisite graph.',background='A courier works through the objectives below.',
             instructions='Follow the declared objectives. Treat Plot progress as authoritative; do not invent rewards.',
             firstInput='Describe the opening situation and the available objectives.',mature=False,nsfw=False,
             conditions=list(dict.fromkeys(n['scenario'] for n in plan['nodes'])),trackedItems=[],triggerEvents=[])
    nodes={n['id']:n for n in plan['nodes']}
    initial='score: 0\n'+'\n'.join(k+': 0' for k in report['order'])
    # Reserve the score key so completion cannot alias the award total.
    if 'score' in nodes:raise ValueError('score is reserved')
    w['trackedItems']=[dict(id=identity('tracker','plot'),name='Plot progress',variableName='plot',positionInList=0,
         dataType='yaml',visibility='everyone',description='Completion flags and awarded score. Script-owned.',
         initialValue=initial,initialValueBasedOnPC='same',autoUpdate=False,updateInstructions='',enforceFormat=False)]
    for k in report['order']:
        n=nodes[k];guard=' and '.join(['$plot.'+k+' = 0']+['$plot.'+d+' = 1' for d in n.get('requires',[])])
        script='if '+guard+'\n    $plot.score += '+str(n.get('award',0))+'\n    $plot.'+k+' = 1'
        w['triggerEvents'].append(dict(id=identity('trigger',k),name=n['name'],advancedLogic=False,
            triggerOnStartOfGame=False,triggerMidGame=False,canTriggerMoreThanOnce=True,
            triggerConditions=[dict(id=identity('event',k),category='condition',type='triggerOnEvent',data=n['scenario']),
                               dict(id=identity('guard',k),category='condition',type='triggerOnPawScript',data=guard)],
            triggerEffects=[dict(id=identity('commit',k),type='effectRunScript',data=script)]))
    report['triggerOrder']=[nodes[k]['name'] for k in report['order']]
    return w,report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        plan=json.loads(a.plan.read_text(encoding='utf-8-sig'))
        template=json.loads((Path(__file__).resolve().parent.parent/'World-Template.json').read_text(encoding='utf8'))
        w,r=compile_world(plan,template)
        if a.output:
            from validate_iw_export import validate
            schema=json.loads(Path(__file__).with_name('iw-export.schema.json').read_text(encoding='utf8'))
            findings=validate(w,schema)
            if any(f['severity']=='error' for f in findings):raise ValueError(json.dumps(findings))
            with a.output.open('x',encoding='utf8') as f:json.dump(w,f,ensure_ascii=False,indent=2)
            r['validation']=findings
        print(json.dumps(r,indent=2,ensure_ascii=False))
    except (ValueError,OSError,KeyError,TypeError) as e:p.exit(2,str(e)+'\n')
if __name__=='__main__':main()
