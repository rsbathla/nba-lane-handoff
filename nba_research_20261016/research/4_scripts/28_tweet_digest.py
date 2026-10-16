# NBA preseason tweets + team previews digest: Ramneik's saved X bookmarks (Codex team-guide capture, 10-14), Full Court Press coach/beat relays,
# and the guide's NBA.com preview / media-day notes, each set beside what the preseason box shows for the players named (through the latest log).
# Usage: 28_tweet_digest.py <guide dir> <leaguegamelog_P json> <roster parquet> <out md> <adv json dirs...>
import json,glob,re,sys,unicodedata,pandas as pd,numpy as np
GD,LOG,ROS,OUT,XP=sys.argv[1:6]; dirs=sys.argv[6:]
FR='/mnt/project-files/nba/p1_historical/layer_e/build/data/frame_abcd.parquet'
OPEN=['BOS','DET','NYK','PHI','OKC','SAS']
def norm(s): return re.sub(r'[^a-z ]',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
# preseason log -> per player-game box usage (same formula as the frame's usg)
d=json.load(open(LOG))['resultSets'][0]; g=pd.DataFrame(d['rowSet'],columns=d['headers']); g=g[g.GAME_ID.str.startswith('001')]
st={}; bm={}
for dd in dirs:
    for fn in [x for x in glob.glob(dd+'/*.json') if 'boxscoreadvancedv3' in x or '/adv_2026-27_' in x]:
        b=json.load(open(fn)).get('boxScoreAdvanced')
        if not b or not b['gameId'].startswith('001'): continue
        for side in ['homeTeam','awayTeam']:
            for p in b[side]['players']:
                st[(b['gameId'],p['personId'])]=int(bool(p.get('position')))
                m=p['statistics'].get('minutes') or '0:00'; mm,ss=(m.split(':')+['0'])[:2]; bm[(b['gameId'],p['personId'])]=float(mm)+float(ss)/60
g['MIN']=[bm.get((a,b),m) for a,b,m in zip(g.GAME_ID,g.PLAYER_ID,g.MIN)]
g.loc[g.MIN<0,'MIN']=np.nan  # NBA.com log glitch (Mark Williams 0012600054 = -4)
g['poss']=g.FGA+0.44*g.FTA+g.TOV
t=g.groupby(['GAME_ID','TEAM_ID']).agg(tmin=('MIN','sum'),tposs=('poss','sum')).reset_index()
g=g.merge(t,on=['GAME_ID','TEAM_ID'])
g['usg']=np.where(g.MIN>0,100*g.poss*(g.tmin/5)/(g.MIN*g.tposs),np.nan)
g['start']=[st.get((a,b)) for a,b in zip(g.GAME_ID,g.PLAYER_ID)]
g=g.sort_values('GAME_DATE'); LAST=g.GAME_DATE.max()
# last season (2025-26), all teams
f=pd.read_parquet(FR,columns=['season','PLAYER_ID','MIN','usg','started']); f=f[f.season=='2025-26']
f['mu']=f.MIN*f.usg
L=f.groupby('PLAYER_ID').agg(gp25=('MIN','size'),mpg25=('MIN','mean'),st25=('started','mean'),mu=('mu','sum'),m=('MIN','sum'))
L['usg25']=L.mu/L.m
R=pd.read_parquet(ROS); R['ln']=R.PLAYER_LAST_NAME.map(lambda s:norm(re.sub(r'\b(Jr|Sr|II|III|IV)\.?$','',s.strip())).strip())
R['fn']=R.PLAYER_FIRST_NAME.map(lambda s:norm(s).strip())
def pline(pid,name):
    x=g[g.PLAYER_ID==pid]; l=L.loc[pid] if pid in L.index else None
    if len(x):
        mins=x.MIN.fillna(0); u=(x.usg*mins).sum()/mins[x.usg.notna()].sum() if mins[x.usg.notna()].sum()>0 else np.nan
        box=x.start.notna().sum(); sr=f"{int(x.start.sum())}/{box}" if box else 'n/a'
        pg=', '.join(f"{r.GAME_DATE[5:].replace('-','/')} {r.MATCHUP[-3:]} {r.MIN:.0f}m{' S' if r.start==1 else ''} {r.usg:.0f}%" if pd.notna(r.MIN) else f"{r.GAME_DATE[5:]} min n/a" for r in x.itertuples())
        pre=f"{len(x)} | {mins.mean():.1f} | {sr} | {u:.1f}" if pd.notna(u) else f"{len(x)} | {mins.mean():.1f} | {sr} | n/a"
    else: pre,pg='0 | — | — | —','no preseason game through '+LAST
    ls=f"{int(l.gp25)} | {l.mpg25:.1f} | {l.st25:.0%} | {l.usg25:.1f}" if l is not None else 'none | | |'
    return f"| {name} | {pre} | {ls} | {pg} |"
def named(team,text):
    tx=' '+norm(text)+' '; r=R[R.TEAM_ABBREVIATION==team]; out=[]
    for x in r.itertuples():
        full=f' {norm(x.player).strip()} ' in tx
        lnhit=f' {x.ln} ' in tx; amb=(r.ln==x.ln).sum()>1
        fnhit=len(x.fn)>=5 and (r.fn==x.fn).sum()==1 and x.fn not in set(r.ln) and f' {x.fn} ' in tx and x.fn not in ('jalen','jaylen','kevin','james','marcus')
        if full or (lnhit and not amb) or fnhit: out.append((x.PERSON_ID,x.player))
        elif lnhit and amb: out.append((x.PERSON_ID,x.player+' (shared surname; may not be the one meant)'))
    return out
# sources
B=json.load(open(GD+'/BOOKMARKS.json')); Q=json.load(open(GD+'/QUOTE_OVERLAY.json')); src={s['id']:s for s in B['sources']}
page=open(GD+'/PAGE.md').read()
names={k:v for k,v in zip(g.TEAM_NAME,g.TEAM_ABBREVIATION) if v in set(R.TEAM_ABBREVIATION)}
secs={}
for blk in re.split(r'\n(?=# )',page):
    m=re.match(r'# (.+)\n',blk)
    if not m or m.group(1) not in names: continue
    body=blk.split('\n## ')[0]; secs[names[m.group(1)]]={k:(re.search(r'\*\*'+k+r'\.\*\*\s*(.+)',body) or [None,None])[1] for k in ['Dated availability','Current evidence and source conflicts']}
XPOSTS=[]
def fmt(p,team=True):
    tag={'bookmark':' · your bookmark'}.get(p.get('source'),'') or (' · read in your Chrome' if p.get('via')=='chrome' else '')
    head=f"- {p['date_utc'][:10]} **{p['author']}** (@{p['handle']}){', '+p['topic'] if team else ''}{tag} [post]({p['url']})"
    t=p['text'].strip(); q=p.get('quoted_text')
    body='\n'.join('  > '+l if l.strip() else '  >' for l in t.split('\n'))
    if q: body+='\n  >\n'+'\n'.join('  > *Quoting:* '+l if i==0 else '  > '+l for i,l in enumerate(q.strip().split('\n')))
    if p.get('text_truncated'): body+='\n  > *(cut off; the full post would not load)*'
    return head+'\n'+body
XJ=json.load(open(XP)); XPOSTS=XJ['posts']; ARTS=XJ.get('articles',[])
CONF={c['teams'][0]:c['issue'] for c in B['conflicts']}
SRCS=', '.join(f"{x['author']} {x['event_date']} '{x['title']}'" for x in B['sources'])
md=[f"# NBA preseason tweets and team previews, checked against the box score\n",
f"Built 2026-10-15 for Ramneik by `layer_e/build/28_tweet_digest.py`. Box-score numbers run through **{LAST}** (NBA.com preseason log + every saved advanced boxscore).\n",
"## Verdict\n",
open(sys.argv[0].replace("28_tweet_digest.py","28_verdict.md")).read(),
"## What is in here, and what is not\n",
f"- **X:** {len(XPOSTS)} posts dated 2026-09-25 to 2026-10-15. {sum(p.get('via')=='chrome' for p in XPOSTS)} were read directly in your Chrome on 2026-10-15 (full text, marked 'read in your Chrome'): your NBA bookmarks back to 09-25 plus X searches since 10-01 (preseason usage, preseason notes, starting lineups, the opening-night teams, and Thunder Dan, Adam Stock, Myguyknowsaguy, Besbris, Engleman). The rest came from web search of x.com, where the text is what the search shows (long posts cut off with ...). Dates come from the post ID in UTC, so an evening ET post shows the next day. X stops loading author searches after about 9 posts, so Thunder Dan, Adam Stock and Besbris are only partly covered; a team with few posts is a gap in coverage, not a quiet team.",
f"- **Codex's 10-14 bookmark notes:** Codex's team guide summarized 4 of your bookmarked posts ({SRCS}) into {len(B['team_annotations'])} team notes across {len({a['team'] for a in B['team_annotations']})} teams. They are shown as 'Codex's notes on your bookmarks'; the full posts are in the X sections.",
f"- **Coach and beat-writer quotes:** {len(Q['notes'])} Full Court Press (@fcpnba) relays dated 10-09 to 10-14. These are relays of quotes, not transcripts; the clips were not checked.",
"- **Team previews:** NBA.com's 2026-27 season previews (09-22) and media-day / news items, as summarized per team in Codex's guide. These are Codex's summaries with links, not my reading of the articles.",
"- **The box score columns are mine**, from the raw NBA.com data, not from the posts. Usage is the box formula (shots + 0.44 FT + turnovers, per team possession on the floor), minutes-weighted, the same formula as the research frame. S = started. Preseason samples are 1 to 5 games and starters often rested, so a usage number here is a pointer, not a role.",
"- Every post is an analyst's opinion, not a role confirmation. Category-league draft opinions (Siakam, Jalen Williams, Young's efficiency) don't say anything about DK points.\n",
"Columns in each table: preseason games | mpg | starts / games with a boxscore | usage % ; 2025-26 games | mpg | start rate | usage % ; then every preseason game (date, opponent, minutes, S if started, usage).\n"]
H="| Player | Pre G | Pre MPG | Pre starts | Pre USG % | 25-26 G | 25-26 MPG | 25-26 start % | 25-26 USG % | Preseason games |\n|---|---|---|---|---|---|---|---|---|---|"
teams=OPEN+sorted(set(names.values())-set(OPEN))
def team_block(tm):
    out=[]; ids=[]
    bk=[a for a in B['team_annotations'] if a['team']==tm]; qs=[q for q in Q['notes'] if q['team']==tm]; s=secs.get(tm,{})
    full=[k for k,v in names.items() if v==tm][0]
    out.append(f"### {full} ({tm}){' — opening night' if tm in OPEN else ''}\n")
    if bk:
        out.append("**Codex's notes on your bookmarks (10-14):**\n")
        for a in bk:
            sc=src[a['source_id']]; out.append(f"- **{sc['author']}** ({sc['event_date']} games): {a['claim']} [post]({sc['url']})"); ids+=named(tm,a['claim'])
        if tm in CONF: out.append(f"- *Analysts disagree:* {CONF[tm]}")
        out.append('')
    xs=sorted([p for p in XPOSTS if p['team']==tm],key=lambda p:p['date_utc'])
    if xs:
        out.append(f"**On X ({len(xs)} posts, camp and preseason):**\n")
        for p in xs:
            out.append(fmt(p)); ids+=named(tm,p['text']+' '+' '.join(p.get('players',[])))
        out.append('')
    if qs:
        out.append("**Coach / beat quotes (Full Court Press relays):**\n")
        for q in qs:
            out.append(f"- {q['source_date'].replace('Observed ','')}: {q['claim']} [post]({q['source_url']})"); ids+=named(tm,q['claim'])
        out.append('')
    if s.get('Current evidence and source conflicts'):
        out.append(f"**Preview and news (Codex summary of NBA.com / team reports):** {s['Current evidence and source conflicts']}\n"); ids+=named(tm,s['Current evidence and source conflicts'])
    if s.get('Dated availability'):
        out.append(f"**Availability as of 10-14 (Codex):** {s['Dated availability']}\n"); ids+=named(tm,s['Dated availability'])
    seen=[]; best={}
    for pid,nm in ids:
        if pid not in best or '(shared surname' in best[pid]: best[pid]=nm
    for pid,nm in ids:
        if (pid,best[pid]) not in seen: seen.append((pid,best[pid]))
    if seen:
        out.append("**What the box score shows for the players named above:**\n"); out.append(H)
        for pid,nm in seen: out.append(pline(pid,nm))
        out.append('')
    return out,len(bk)+len(qs),len(seen)
cnt={}
md.append("## Opening-night teams (Oct 20)\n")
for tm in OPEN:
    o,n,k=team_block(tm); md+=o; cnt[tm]=(n,k)
mx=[p for p in XPOSTS if p['team']=='MULTI']
if mx or ARTS:
    md.append("## Across teams (analysts and roundups)\n")
    for p in sorted(mx,key=lambda p:p['date_utc']): md.append(fmt(p,False))
    for a in ARTS: md.append(f"- Article: [{a['title']}]({a['url']}){' ('+a['date']+')' if a.get('date') else ''}: {a.get('summary','')}")
    md.append('')
md.append("## Teams with bookmarks, X posts or coach quotes\n")
rest=[tm for tm in teams[6:] if any(a['team']==tm for a in B['team_annotations']) or any(q['team']==tm for q in Q['notes']) or any(p['team']==tm for p in XPOSTS)]
for tm in rest:
    o,n,k=team_block(tm); md+=o; cnt[tm]=(n,k)
md.append("## Other teams: preview and news only (no posts found)\n")
for tm in [t for t in teams[6:] if t not in rest]:
    o,n,k=team_block(tm); md+=o; cnt[tm]=(n,k)
open(OUT,'w').write('\n'.join(md)+'\n')
print('teams',len(cnt),'with posts',sum(1 for v in cnt.values() if v[0]),'players named',sum(v[1] for v in cnt.values()),'last',LAST)
missing=[tm for tm in teams if tm not in secs]; print('no guide section',missing)
# optional: JSON for the team dashboard (29_dashboard.py)
import os
if os.environ.get('DASH_JSON'):
    def prow(pid,name):
        x=g[g.PLAYER_ID==pid]; l=L.loc[pid] if pid in L.index else None; r={'name':name,'pid':int(pid)}
        if len(x):
            mins=x.MIN.fillna(0); w=mins[x.usg.notna()].sum()
            r.update(gp=len(x),mpg=round(float(mins.mean()),1),starts=int(x.start.sum()) if x.start.notna().any() else None,box=int(x.start.notna().sum()),
                     usg=round(float((x.usg*mins).sum()/w),1) if w>0 else None,
                     games=[{'d':rr.GAME_DATE[5:],'opp':rr.MATCHUP[-3:],'min':None if pd.isna(rr.MIN) else round(float(rr.MIN)),'s':rr.start==1,'u':None if pd.isna(rr.usg) else round(float(rr.usg))} for rr in x.itertuples()])
        else: r.update(gp=0)
        if l is not None: r.update(gp25=int(l.gp25),mpg25=round(float(l.mpg25),1),st25=round(float(l.st25)*100),usg25=round(float(l.usg25),1))
        return r
    D={'built':'2026-10-15','box_through':LAST,'open':OPEN,'teams':{},'multi':[p for p in XPOSTS if p['team']=='MULTI'],'articles':ARTS}
    for tm in sorted(set(names.values())):
        full=[k for k,v in names.items() if v==tm][0]; ids=[]
        bk=[dict(a,**{k:src[a['source_id']][k] for k in ('author','url','event_date')}) for a in B['team_annotations'] if a['team']==tm]
        qs=[q for q in Q['notes'] if q['team']==tm]; xs=sorted([p for p in XPOSTS if p['team']==tm],key=lambda p:p['date_utc'],reverse=True); s=secs.get(tm,{})
        for a in bk: ids+=named(tm,a['claim'])
        for q in qs: ids+=named(tm,q['claim'])
        for p in xs: ids+=named(tm,p['text']+' '+' '.join(p.get('players',[])))
        for k in ('Current evidence and source conflicts','Dated availability'):
            if s.get(k): ids+=named(tm,s[k])
        mentioned={pid for pid,_ in ids}
        roster=R[R.TEAM_ABBREVIATION==tm]; rows=[]
        for x in roster.itertuples():
            r=prow(x.PERSON_ID,x.player); r['named']=x.PERSON_ID in mentioned
            if r['gp']>0 or r.get('mpg25',0)>=12 or r['named']: rows.append(r)
        rows.sort(key=lambda r:(-(r.get('mpg') or 0),-(r.get('mpg25') or 0)))
        D['teams'][tm]={'name':full,'bookmarks':bk,'conflict':CONF.get(tm),'relays':qs,'posts':xs,'preview':s.get('Current evidence and source conflicts'),'availability':s.get('Dated availability'),'players':rows}
    json.dump(D,open(os.environ['DASH_JSON'],'w'),ensure_ascii=False,default=lambda o:o.item() if hasattr(o,'item') else str(o))
    print('dash json',len(D['teams']))
