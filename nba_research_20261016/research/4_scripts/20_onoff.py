import pandas as pd, numpy as np, glob, re, unicodedata
R='/home/claude/nba/raw/'
f=pd.read_parquet('frame.parquet')[['GAME_ID','PLAYER_ID','PLAYER_NAME','TEAM_ID','TEAM_ABBREVIATION','season','date']]
def norm(s): s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower(); s=re.sub(r'[^a-z ]','',s); s=re.sub(r'\b(jr|sr|ii|iii|iv)\b','',s); return ' '.join(s.split())
alias={'alexandre sarr':'alex sarr','carlton carrington':'bub carrington','cui yongxi':'cui cui'}
f['k']=f.PLAYER_NAME.map(norm)
ros={g:x for g,x in f.groupby('GAME_ID')}
def secs(x):
    p=x.fillna('0:00:00').str.split(':',expand=True).astype(float); return p[0]*3600+p[1]*60+p[2]
out=[]; bad=0
for season,folder in [('2024-25','pbp_2425'),('2025-26','pbp_2526')]:
    for fn in sorted(glob.glob(R+f'bdb/{folder}/[[]20*')):
        gid=re.search(r'-(\d{10})-',fn).group(1)
        if not gid.startswith('002') or gid not in ros: continue
        d=pd.read_csv(fn,dtype=str,low_memory=False)
        r=ros[gid]; kmap=dict(zip(r.k,r.PLAYER_ID)); tmap=dict(zip(r.PLAYER_ID,r.TEAM_ID))
        def pid(name):
            k=norm(name); k=alias.get(k,k); return kmap.get(k)
        cols=['a1','a2','a3','a4','a5','h1','h2','h3','h4','h5']
        names=pd.unique(d[cols].values.ravel()); names=[n for n in names if isinstance(n,str)]
        ids={n:pid(n) for n in names}
        if any(v is None for v in ids.values()): bad+=1
        plist=[p for p in set(ids.values()) if p is not None]; idx={p:i for i,p in enumerate(plist)}
        n=len(plist); Rr=len(d)
        O=np.zeros((Rr,n))
        for c in cols:
            v=d[c].map(ids)
            for i,p in enumerate(v):
                if p is not None and p==p: O[i,idx[p]]=1
        el=secs(d.elapsed).values; per=d.period.values
        dur=np.zeros(Rr); 
        for i in range(Rr-1):
            if per[i]==per[i+1]: dur[i]=max(el[i+1]-el[i],0)
        # plays by player
        Pl=np.zeros((Rr,n))
        ev=d.event_type.values
        actor=d.player.astype(str).str.split('/').str[-1] if season=='2025-26' else d.player
        for i in range(Rr):
            if ev[i] in('shot','free throw','turnover'):
                p=pid(actor.iloc[i]) if isinstance(actor.iloc[i],str) else None
                if p is None or p not in idx: continue
                w=1.0 if ev[i]!='free throw' else 0.44
                if ev[i]=='turnover' and 'team' in str(actor.iloc[i]).lower(): continue
                Pl[i,idx[p]]+=w
        team=np.array([tmap.get(p) for p in plist])
        for T in set(team):
            m=team==T; Ot=O[:,m]; Pt=Pl[:,m]; tp=Pt.sum(axis=1)
            mins=(Ot*dur[:,None]).T@Ot/60      # [P,X] minutes with both on
            minsP=(Ot*dur[:,None]).sum(axis=0)/60
            plays_on=Pt.T@Ot                  # P's plays with X on (P on implied)
            playsP=Pt.sum(axis=0)
            tp_on=(Ot*tp[:,None]).T@Ot         # team plays with P on and X on
            tpP=(Ot*tp[:,None]).sum(axis=0)
            pl=np.array(plist)[m]
            for a in range(len(pl)):
                for b in range(len(pl)):
                    if a==b: continue
                    out.append((gid,season,T,pl[a],pl[b],mins[a,b],minsP[a]-mins[a,b],plays_on[a,b],playsP[a]-plays_on[a,b],tp_on[a,b],tpP[a]-tp_on[a,b]))
    print(season,'done; games with unmapped lineup names',bad)
o=pd.DataFrame(out,columns=['GAME_ID','season','TEAM_ID','P','X','min_on','min_off','pl_on','pl_off','tp_on','tp_off'])
o.to_parquet('onoff_pairs.parquet'); print(o.shape)
