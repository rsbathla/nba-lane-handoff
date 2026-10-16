# Compact team data for the Claude Design canvas ("NBA Preseason Team Board"), from the processed JSON 29_dashboard.py writes with FULL_JSON set.
# Usage: 30_design_data.py <full json> <out json>
import json,re,sys
D=json.load(open(sys.argv[1])); OUT=sys.argv[2]
T=D['teams']; OPEN=D['open']
f1=lambda v:'—' if v is None else f'{v:.1f}'
def link_text(s): return re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',r'\1',s or '')
def items(x):
    out=[]
    for p in x['analyst']: out.append(dict(k='analyst',date=p['date_utc'],author=p['author'],handle=p.get('handle'),url=p.get('url'),text=p['text'],src='Read in your Chrome' if p.get('via')=='chrome' else 'Web search',topic=(x['name'].split(' ')[-1]+' section of a multi-team post') if p.get('excerpt') else 'Analyst post'))
    for p in x['posts']:
        k='coach' if ('coach' in (p.get('topic') or '') or p.get('handle')=='fcpnba') else ('analyst' if p.get('source')=='bookmark' else 'beat')
        src='Your bookmark' if p.get('source')=='bookmark' else ('Read in your Chrome' if p.get('via')=='chrome' else 'Web search')
        out.append(dict(k=k,date=p['date_utc'],author=p['author'],handle=p.get('handle'),url=p.get('url'),text=p['text'],quoted=p.get('quoted_text'),src=src,topic=p.get('topic') or ''))
    for q in x['relays']: out.append(dict(k='coach',date=((re.search(r'\d{4}-\d{2}-\d{2}',q.get('source_date') or '') or [None])[0] if re.search(r'\d{4}-\d{2}-\d{2}',q.get('source_date') or '') else '2026-10-14'),author='Full Court Press relay',handle='fcpnba',url=q.get('source_url'),text=q['claim'],src='Quote relay',topic='Coach / beat quote'))
    for b in x['bookmarks']: out.append(dict(k='analyst',date=b['event_date'],author=b['author'],handle=None,url=b.get('url'),text=b['claim'],src='Codex summary',topic=f"Codex note on your bookmark ({b['event_date']} games)"))
    out.sort(key=lambda i:i['date'],reverse=True)
    for i in out:
        i['date']=i['date'][:10]
        for k in [k for k,v in i.items() if v in (None,'')]: del i[k]
    return out
def players(x):
    rows=[]
    for p in x['players']:
        d=(p['usg']-p['usg25']) if p.get('gp') and p.get('usg') is not None and p.get('usg25') is not None else None
        rows.append(dict(name=p['name'],named=bool(p.get('named')),gp=p.get('gp') or 0,
            mpg=f1(p['mpg']) if p.get('gp') else '—',st=(f"{p['starts']}/{p['box']}" if p.get('box') else 'n/a') if p.get('gp') else '—',
            usg=f1(p['usg']) if p.get('gp') else '—',dlt=(None if d is None or abs(d)<3 else ('+' if d>0 else '')+f'{d:.0f}'),up=bool(d and d>0),
            gp25='—' if p.get('gp25') is None else p['gp25'],mpg25=f1(p.get('mpg25')),st25='—' if p.get('st25') is None else f"{p['st25']}%",usg25=f1(p.get('usg25')),
            games=[dict(t=f"{g['d'].replace('-','/')} {g['opp']} {g['min'] if g.get('min') is not None else '?'}m {g['u'] if g.get('u') is not None else '–'}%",s=bool(g.get('s'))) for g in p.get('games',[])] if p.get('gp') else []))
    return rows
order=OPEN+sorted([t for t in T if t not in OPEN],key=lambda t:T[t]['name'])
teams=[]
for t in order:
    x=T[t]; it=items(x)
    teams.append(dict(code=t,name=x['name'],game=x.get('game'),opening=t in OPEN,notes=x.get('notes',[]),players=players(x),posts=it,
        preview=link_text(x.get('preview')),availability=link_text(x.get('availability')),conflict=x.get('conflict'),
        played=sum(1 for p in x['players'] if p.get('gp'))))
out=dict(built=D['built'],box_through=D['box_through'],teams=teams)
json.dump(out,open(OUT,'w'),ensure_ascii=False,separators=(',',':'))
print('teams',len(teams),'posts',sum(len(t['posts']) for t in teams),'bytes',len(json.dumps(out,ensure_ascii=False,separators=(',',':')).encode()))
