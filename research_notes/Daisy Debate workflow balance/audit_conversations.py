import glob,json,collections,datetime,re,pathlib
out=pathlib.Path(__file__).parent
inventory=[]; extracted=[]
def txt(c):
 if isinstance(c,str):return c
 if isinstance(c,list):return '\n'.join(x.get('text','') for x in c if isinstance(x,dict))
 return ''
def date(t):
 try:return datetime.datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()
 except:return None
files=[('claude',f) for f in glob.glob('/Users/jono/.claude/projects/*/**/*.jsonl',recursive=True)]
files += [('codex',f) for f in glob.glob('/Users/jono/.codex/sessions/**/*.jsonl',recursive=True)]
for provider,f in files:
 rows=[]
 for n,line in enumerate(open(f),1):
  try:rows.append((n,json.loads(line)))
  except:pass
 cwd=''; sid=''; imported=False
 if provider=='codex':
  meta=next((d['payload'] for _,d in rows if d.get('type')=='session_meta'),{})
  cwd=meta.get('cwd','');sid=meta.get('id',''); imported=any('external-import' in str(d.get('payload',{}).get('turn_id','')) for _,d in rows)
 else:
  cwd=next((d.get('cwd','') for _,d in rows if '/dev/daisydebate' in d.get('cwd','') or '/dev/pagespace' in d.get('cwd','')),next((d.get('cwd','') for _,d in rows if d.get('cwd')),''));sid=next((d.get('sessionId') for _,d in rows if d.get('sessionId')),'')
 project='daisydebate' if 'daisydebate' in cwd or (provider=='claude' and 'daisydebate' in f) else 'pagespace' if 'pagespace' in cwd or (provider=='claude' and 'pagespace' in f) else ''
 # Include external cwd only if actual user/assistant messages explicitly refer to repo; flag as mixed rather than silently count.
 if not project:continue
 tools=collections.Counter(); usage=collections.Counter(); messages=[]; timestamps=[]; compact=0; last_total={}; first_baseline={}; seen=set(); types=collections.Counter()
 for n,d in rows:
  types[d.get('type','')]+=1
  t=d.get('timestamp');ts=date(t or '')
  if ts:timestamps.append(ts)
  role=''; content='';calls=[]
  if provider=='claude':
   if d.get('type')=='system' and d.get('subtype')=='compact_boundary':compact+=1
   m=d.get('message',{});role=m.get('role','');content=txt(m.get('content'))
   calls=[(x.get('name',''),x.get('input',{})) for x in m.get('content',[]) if isinstance(x,dict) and x.get('type')=='tool_use'] if isinstance(m.get('content'),list) else []
   mid=m.get('id')
   if m.get('usage') and mid not in seen:
    seen.add(mid)
    for k,v in m['usage'].items():
     if isinstance(v,(int,float)):usage[k]+=v
  else:
   p=d.get('payload',{})
   if d.get('type')=='compacted' or p.get('type')=='context_compacted':compact+=1
   if d.get('type')=='response_item':
    if p.get('type')=='message':role=p.get('role','');content=txt(p.get('content'))
    elif p.get('type') in ('function_call','custom_tool_call'):
     arg=p.get('arguments',p.get('input',''))
     try:arg=json.loads(arg)
     except:pass
     calls=[(p.get('name',''),arg)]
   if d.get('type')=='event_msg' and p.get('type')=='token_count':
    info=p.get('info') or {}
    if info.get('total_token_usage'):
     if not last_total:
      first_baseline={k:v-info.get('last_token_usage',{}).get(k,0) for k,v in info['total_token_usage'].items()}
     last_total=info['total_token_usage']
  for name,arg in calls:
   tools[name]+=1
   messages.append({'line':n,'time':t,'role':'tool_call','name':name,'text':json.dumps(arg,ensure_ascii=False)})
  if content and role in ('user','assistant'):messages.append({'line':n,'time':t,'role':role,'text':content})
 if provider=='codex':usage.update({k:v-first_baseline.get(k,0) for k,v in last_total.items()})
 intervals=[b-a for a,b in zip(timestamps,timestamps[1:]) if b>=a]
 row={'provider':provider,'project':project,'path':f,'session_id':sid,'cwd':cwd,'external_import':imported,'forked_from_id':meta.get('forked_from_id') if provider=='codex' else None,'inherited_token_baseline':first_baseline,'records':len(rows),'message_count':len([m for m in messages if m['role']!='tool_call']),'tool_calls':sum(tools.values()),'tools':dict(tools),'compactions':compact,'usage':dict(usage),'start':datetime.datetime.fromtimestamp(min(timestamps),datetime.timezone.utc).isoformat() if timestamps else None,'end':datetime.datetime.fromtimestamp(max(timestamps),datetime.timezone.utc).isoformat() if timestamps else None,'span_seconds':max(timestamps)-min(timestamps) if timestamps else 0,'bounded_interevent_seconds_5min':sum(min(x,300) for x in intervals),'long_gaps_gt5min':sum(x>300 for x in intervals),'record_types':dict(types)}
 inventory.append(row)
 extracted.append({'meta':row,'messages':messages})
(out/'conversation_inventory.json').write_text(json.dumps(inventory,indent=2))
# This derived corpus preserves source references; local use only, do not publish raw content.
(out/'conversation_metrics.json').write_text(json.dumps({'groups':[{ 'provider':provider,'project':project,'files':len(g),'tool_calls':sum(x['tool_calls'] for x in g),'compactions':sum(x['compactions'] for x in g),'usage':dict(sum((collections.Counter(x['usage']) for x in g),collections.Counter()))} for provider in ('claude','codex') for project in ('daisydebate','pagespace') if (g:=[x for x in inventory if x['provider']==provider and x['project']==project])]},indent=2))
pathlib.Path('/private/tmp/daisy-conversation-extract.json').write_text(json.dumps(extracted))
print((out/'conversation_metrics.json').read_text())
print('FILES',len(inventory),'MESSAGES',sum(len(x['messages']) for x in extracted))
