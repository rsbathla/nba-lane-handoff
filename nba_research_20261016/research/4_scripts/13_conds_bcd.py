import pandas as pd, numpy as np
R='/home/claude/nba/raw/'
f=pd.read_parquet('frame_a.parquet'); tg=pd.read_parquet('teamgames.parquet')
# ---------- Layer B: absences ("played 0 minutes")
ap=f[['season','PLAYER_ID','TEAM_ID','date','GAME_ID','A1_usg_szn','A6_astsh_szn','A3_min_szn','started','posg']].copy()
games=tg[['season','GAME_ID','TEAM_ID','date']].drop_duplicates()
# player-team spans: for each player, sequence of appearances; out for team game if appeared for team before and next appearance (any team) is for this team (or none)
ap=ap.sort_values(['PLAYER_ID','date'])
recs=[]
for (pid,s),x in ap.groupby(['PLAYER_ID','season']):
    x=x.reset_index(drop=True)
    for i in range(len(x)):
        t=x.TEAM_ID[i]; d0=x.date[i]
        nxt=x.iloc[i+1] if i+1<len(x) else None
        if nxt is not None and nxt.TEAM_ID!=t: d1=nxt.date; end_excl=True
        elif nxt is not None: d1=nxt.date; end_excl=True
        else: d1=pd.Timestamp('2100-01-01'); end_excl=True
        recs.append((pid,s,t,d0,d1, nxt is None or nxt.TEAM_ID==t))
sp=pd.DataFrame(recs,columns=['PLAYER_ID','season','TEAM_ID','d0','d1','same_next'])
sp=sp[sp.same_next]
# team games strictly between d0 and d1 are absences
gm=games.merge(sp,on=['season','TEAM_ID'])
out=gm[(gm.date>gm.d0)&(gm.date<gm.d1)][['season','GAME_ID','TEAM_ID','date','PLAYER_ID']]
print('absence rows',len(out))
# attach absentee's as-of state at that date: last known season-to-date values (from his most recent game before date)
st=f[['PLAYER_ID','season','date','A1_usg_szn','A6_astsh_szn','A3_min_szn','usage','AST','MIN','started','posg']].sort_values('date')
# cumulative incl his game (state after game) for use on later dates
st=st.copy(); g=[st.PLAYER_ID,st.season]
st['n']=st.groupby(['PLAYER_ID','season']).cumcount()+1
st['usg_cum']=st.usage.fillna(0).groupby(g).cumsum()/st.n; st['min_cum']=st.MIN.groupby(g).cumsum()/st.n
st['starts_cum']=st.started.fillna(0).groupby(g).cumsum()
out=pd.merge_asof(out.sort_values('date'),st[['PLAYER_ID','season','date','n','usg_cum','min_cum','starts_cum','posg']].rename(columns={'date':'sdate'}).sort_values('sdate'),left_on='date',right_on='sdate',by=['PLAYER_ID','season'],allow_exact_matches=False)
# team roles as of date, among players who appeared for the team earlier: top usage (5+ games), top assist share, most starts at C, most starts at each posg
f2=f[['season','TEAM_ID','date','PLAYER_ID','usage','AST','started','posg','MIN']].copy()
tm_ast=f2.groupby(['season','TEAM_ID','date']).AST.transform('sum'); f2['astsh']=f2.AST/tm_ast.replace(0,np.nan)
# v1.2 (review D3/D4): usage and assist share weighted by minutes; usage/assist roles need 15+ mpg;
# players whose latest appearance before D (any team) was for another team are dropped from the team's roles; start ties broken by minutes
f2['umin']=f2.usage*f2.MIN; f2['amin']=f2.astsh*f2.MIN
f2['umin_ok']=f2.MIN.where(f2.usage.notna(),0); f2['amin_ok']=f2.MIN.where(f2.astsh.notna(),0)
lastteam=f[['season','PLAYER_ID','date','TEAM_ID']].sort_values('date')
roles=[]
for (s,t),x in f2.groupby(['season','TEAM_ID']):
    x=x.sort_values('date'); ds=sorted(x.date.unique()); lt=lastteam[lastteam.season==s]
    for D in ds:
        y=x[x.date<D]
        if y.empty: continue
        cur=lt[(lt.date<D)&lt.PLAYER_ID.isin(y.PLAYER_ID.unique())].drop_duplicates('PLAYER_ID',keep='last')
        stay=set(cur[cur.TEAM_ID==t].PLAYER_ID); y=y[y.PLAYER_ID.isin(stay)]
        if y.empty: continue
        a=y.groupby('PLAYER_ID').agg(n=('usage','size'),umin=('umin','sum'),uw=('umin_ok','sum'),amin=('amin','sum'),aw=('amin_ok','sum'),starts=('started','sum'),posg=('posg','first'),mn=('MIN','mean'),mt=('MIN','sum'))
        a['usg']=a.umin/a.uw.replace(0,np.nan); a['ast']=a.amin/a.aw.replace(0,np.nan)
        e=a[a.n>=5]; e15=e[e.mn>=15]
        r={'season':s,'TEAM_ID':t,'date':D}
        r['top_usg']=e15.usg.idxmax() if e15.usg.notna().any() else np.nan
        r['top_ast']=e15.ast.idxmax() if e15.ast.notna().any() else np.nan
        def topstart(c): return c.sort_values(['starts','mt'],ascending=False).index[0] if len(c) else np.nan
        r['start_c']=topstart(a[(a.posg=='C')&(a.starts>0)])
        for pg in ['PG','SG','SF','PF','C']:
            r[f'start_{pg}']=topstart(a[(a.posg==pg)&(a.starts>0)])
        r['rotation']=list(e[e.mn>=20].index); r['high_usg']=list(e15[e15.usg>=25].index)
        roles.append(r)
roles=pd.DataFrame(roles)
absent=out.groupby(['GAME_ID','TEAM_ID']).PLAYER_ID.apply(set).rename('absent').reset_index()
f=f.merge(roles,on=['season','TEAM_ID','date'],how='left').merge(absent,on=['GAME_ID','TEAM_ID'],how='left')
f['absent']=f.absent.apply(lambda s: s if isinstance(s,set) else set())
def isout(pidcol): return np.array([ (p==p) and (p!=me) and (p in ab) for p,me,ab in zip(f[pidcol],f.PLAYER_ID,f.absent)],dtype=float)
avail=f.top_usg.notna()
f['B1_top_usg_out']=np.where(avail&(f.top_usg!=f.PLAYER_ID),isout('top_usg'),np.nan)
f['B2_top_ast_out']=np.where(f.top_ast.notna()&(f.top_ast!=f.PLAYER_ID),isout('top_ast'),np.nan)
f['B3_start_c_out']=np.where(f.start_c.notna()&(f.start_c!=f.PLAYER_ID),isout('start_c'),np.nan)
samepos=np.array([r.get(f'start_{p}') if isinstance(p,str) else np.nan for r,p in zip(f[[f'start_{x}' for x in ['PG','SG','SF','PF','C']]].rename(columns=lambda c:c).to_dict('records'),f.posg)])
f['_samepos']=samepos
f['B4_samepos_starter_out']=np.where(pd.notna(samepos)&(samepos!=f.PLAYER_ID),isout('_samepos'),np.nan)
f['B5_two_rotation_out']=[ (np.nan if not isinstance(rot,list) else float(len([p for p in rot if p in ab and p!=me])>=2)) for rot,ab,me in zip(f.rotation,f.absent,f.PLAYER_ID)]
f['B6_25usg_out']=[ (np.nan if not isinstance(h,list) else float(len([p for p in h if p in ab and p!=me])>=1)) for h,ab,me in zip(f.high_usg,f.absent,f.PLAYER_ID)]
f['n_absent']=f.absent.apply(len)
print('B rates',{c:round(float(np.nanmean(f[c])),3) for c in ['B1_top_usg_out','B2_top_ast_out','B3_start_c_out','B4_samepos_starter_out','B5_two_rotation_out','B6_25usg_out']})
# ---------- Layer C: lines
def tfeed(fn):
    d=pd.read_excel(fn,sheet_name=0,header=None,skiprows=1)
    d=d.iloc[:,[1,2,3,4,36,37,38,39,40,41,44,45,46,51,52]]
    d.columns=['GAME_ID','date','team','venue','rest','s1','s2','s3','s4','s5','open_odds','open_spread','open_total','close_spread','close_total']
    d=d[d.GAME_ID.notna()]; d['GAME_ID']=d.GAME_ID.astype(str).str.zfill(10); return d
tf=pd.concat([tfeed(R+'bdb/03-24-2025-nba-season-team-feed.xlsx'),tfeed(R+'bdb/feeds_2526/05-24-2026-nba-season-team-feed.xlsx')])
tf=tf[tf.GAME_ID.str.startswith('002')].drop_duplicates(['GAME_ID','team'])
for c in ['open_spread','open_total','close_spread','close_total']: tf[c]=pd.to_numeric(tf[c],errors='coerce')
# v1.2 (review D6): map team names to TEAM_ID (learned from home/away games), then merge on (GAME_ID, TEAM_ID) so neutral sites get each team's own line
tf['home']=tf.venue=='H'
tgh=tg[['GAME_ID','TEAM_ID','MATCHUP']].copy(); tgh['home']=tgh.MATCHUP.str.contains('vs.')
nm=tf[tf.venue.isin(['H','R'])].merge(tgh[['GAME_ID','TEAM_ID','home']],on=['GAME_ID','home'])
nm=nm.groupby('team').TEAM_ID.agg(lambda z: z.value_counts().index[0])
tf['TEAM_ID']=tf.team.map(nm); print('unmapped line teams',int(tf.TEAM_ID.isna().sum()),'neutral rows',int((tf.venue=='N').sum()))
tf=tf.dropna(subset=['TEAM_ID']); tf['TEAM_ID']=tf.TEAM_ID.astype(tg.TEAM_ID.dtype)
tf=tf.merge(tgh[['GAME_ID','TEAM_ID']],on=['GAME_ID','TEAM_ID'],how='inner')
print('line rows',len(tf),'games',tf.GAME_ID.nunique(), 'open spread missing',tf.open_spread.isna().mean().round(3))
tf['itt_open']=tf.open_total/2-tf.open_spread/2; tf['itt_close']=tf.close_total/2-tf.close_spread/2
f=f.merge(tf[['GAME_ID','TEAM_ID','open_spread','open_total','close_spread','close_total','itt_open','itt_close']],on=['GAME_ID','TEAM_ID'],how='left')
# tertiles of implied team total on the date (across all teams playing that date in this season-to-date pool)
def date_t(col):
    lo=f.groupby(['season','date'])[col].transform(lambda z: z.quantile(1/3)); hi=f.groupby(['season','date'])[col].transform(lambda z: z.quantile(2/3))
    return np.select([f[col]>=hi,f[col]>=lo,f[col]<lo],['top','middle','bottom'],default='n/a')
# implied total tertile: within season-to-date distribution of all team-games before date (avoid slate-size noise)
def szn_t(col,src):
    out=np.full(len(f),'n/a',dtype=object)
    x=src[['season','date',col]].dropna().sort_values('date')
    for s in ['2024-25','2025-26']:
        xs=x[x.season==s]
        for D in f[f.season==s].date.unique():
            prior=xs[xs.date<D][col]
            if len(prior)<100: continue
            lo,hi=prior.quantile([1/3,2/3]); m=(f.season==s)&(f.date==D)&f[col].notna()
            v=f.loc[m,col]; out[m.values]=np.select([v>=hi,v>=lo],['top','middle'],default='bottom')
    return out
src=tf.drop(columns=['date']).merge(tg[['GAME_ID','TEAM_ID','season','date']],on=['GAME_ID','TEAM_ID'])
f['C1_itt_open_t']=szn_t('itt_open',src); f['C3_total_open_t']=szn_t('open_total',src)
f['C7_itt_close_t']=szn_t('itt_close',src)
f['C2_spread_open']=np.select([f.open_spread<=-8,f.open_spread.abs()<=4.5,f.open_spread>=8],['fav8+','close','dog8+'],default=np.where(f.open_spread.isna(),'n/a','other'))
f['C8_spread_move_toward']=np.where(f.open_spread.notna()&f.close_spread.notna(),(f.open_spread-f.close_spread)>=1.5,np.nan)
f['C8_total_up3']=np.where(f.open_total.notna()&f.close_total.notna(),(f.close_total-f.open_total)>=3,np.nan)
# pace both teams top third as of date
tg2=tg.sort_values('date').copy()
pace=[]
for (s,t),x in tg2.groupby(['season','TEAM_ID']):
    x=x.sort_values('date'); cp=np.concatenate([[0],x.PACE.cumsum()]); n=np.arange(len(x)+1)
    ds=np.sort(f[f.season==s].date.unique()); i=np.searchsorted(x.date.values,ds,side='left')
    pace.append(pd.DataFrame({'season':s,'date':ds,'TEAM_ID':t,'n':i,'pace':np.where(i>=1,cp[i]/np.maximum(i,1),np.nan)}))
pace=pd.concat(pace); pace['pace_rk']=pace.groupby(['season','date']).pace.rank(method='max').where(pace.n>=10); pace=pace.drop(columns='n')
f=f.merge(pace.rename(columns={'pace':'own_pace','pace_rk':'own_pace_rk'}),on=['season','date','TEAM_ID'],how='left').merge(pace.rename(columns={'TEAM_ID':'OPP_ID','pace':'opp_pace','pace_rk':'opp_pace_rk'}),on=['season','date','OPP_ID'],how='left')
f['C4_both_fast']=np.where(f.own_pace_rk.notna()&f.opp_pace_rk.notna(),(f.own_pace_rk>=21)&(f.opp_pace_rk>=21),np.nan)
tdates=tg[['season','TEAM_ID','date']].drop_duplicates().sort_values('date'); tdates['prev']=tdates.groupby(['season','TEAM_ID']).date.shift(1)
f=f.merge(tdates,on=['season','TEAM_ID','date'],how='left'); f['C5_b2b']=np.where(f.prev.notna(),(f.date-f.prev).dt.days==1,np.nan)
f['C6_home']=f.home.astype(float)
# in-game
fin=tg[['GAME_ID','TEAM_ID','PLUS_MINUS']] if 'PLUS_MINUS' in tg else None
box=tg[['GAME_ID','TEAM_ID','MIN']].rename(columns={'MIN':'TMIN'})
f=f.merge(box,on=['GAME_ID','TEAM_ID'],how='left')
pts=f.groupby(['GAME_ID','TEAM_ID']).PTS.transform('sum'); f['_tpts']=pts
op=f.groupby(['GAME_ID','TEAM_ID'])._tpts.first().reset_index().rename(columns={'TEAM_ID':'OPP_ID','_tpts':'_opts'})
f=f.merge(op,on=['GAME_ID','OPP_ID'],how='left'); f['margin']=f._tpts-f._opts
f['C9_blowout15']=(f.margin.abs()>=15).astype(float); f['C10_ot']=(f.TMIN>48.5).astype(float); f['C11_5fouls']=(f.PF>=5).astype(float)
f.to_parquet('frame_abc.parquet'); print('BC done',f.shape)
