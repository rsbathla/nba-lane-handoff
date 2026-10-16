import pandas as pd, numpy as np, json, gzip, glob, re
R='/home/claude/nba/raw/'
f=pd.read_parquet('frame_e2.parquet')  # all player-games (qual and not)
fe=pd.read_parquet('frame_e.parquet'); f=fe.merge(f[['GAME_ID','PLAYER_ID','drtg_rk']],on=['GAME_ID','PLAYER_ID'],how='left')
tg=pd.read_parquet('teamgames.parquet')
f=f.sort_values(['PLAYER_ID','date']).reset_index(drop=True)
seasons=['2024-25','2025-26']
dates=f[['season','date']].drop_duplicates().sort_values('date')
def asof_player(num,den=None,minprior=5,fallback=True):
    """season-to-date ratio from earlier games; prev-season fallback when <5 earlier games and >=10 prev games"""
    n=pd.Series(num,index=f.index).fillna(0.0); ok=pd.Series(num,index=f.index).notna()
    d=pd.Series(1.0 if den is None else den,index=f.index).where(ok,0.0).fillna(0.0); n=n.where(ok,0.0)
    g=[f.PLAYER_ID,f.season]
    cn=n.groupby(g).cumsum()-n; cd=d.groupby(g).cumsum()-d; cg=ok.astype(int).groupby(g).cumsum()-ok.astype(int)
    v=np.where((cg>=minprior)&(cd>0),cn/cd.where(cd>0,1),np.nan)
    if fallback:
        t=pd.DataFrame({'p':f.PLAYER_ID,'s':f.season,'n':n,'d':d,'g':ok.astype(int)}).groupby(['p','s']).sum().reset_index()
        t['s']=t.s.map({'2024-25':'2025-26'}); t=t.dropna()
        m=f[['PLAYER_ID','season']].merge(t,left_on=['PLAYER_ID','season'],right_on=['p','s'],how='left')
        fb=(cg.values<minprior)&(m.g.fillna(0).values>=10)&(m.d.fillna(0).values>0)
        v=np.where(fb,m.n.values/np.where(m.d.fillna(0).values>0,m.d.values,1),v)
    return v
def lastk(x,k=10,minprior=5):
    s=pd.Series(x,index=f.index); r=s.groupby([f.PLAYER_ID,f.season]).transform(lambda z: z.shift(1).rolling(k,min_periods=minprior).mean()); return r.values
def tertile(col):
    """top/middle/bottom third within posg on date, cutoffs from every player's state entering his next game on/after the date"""
    out=np.full(len(f),'n/a',dtype=object); cuts=[]
    for s in seasons:
        fs=f[f.season==s][['PLAYER_ID','date','posg',col]].sort_values('date')
        for D in dates[dates.season==s].date:
            st=fs[fs.date<D].drop_duplicates('PLAYER_ID',keep='last')  # past only: entering state of his last game before D
            if st.empty: continue
            q=st.groupby('posg')[col].quantile([1/3,2/3]).unstack(); q.columns=['lo','hi']; q['date']=D; q['season']=s; cuts.append(q.reset_index())
    c=pd.concat(cuts); m=f[['season','date','posg',col]].merge(c,on=['season','date','posg'],how='left')
    v=m[col]; out=np.select([v>=m.hi,v>=m.lo,v<m.lo],['top','middle','bottom'],default='n/a'); return out
# ---------- Layer A
f['usg']=f.usage
f['A1_usg_szn']=asof_player(f.usg); f['A2_usg_l10']=lastk(f.usg)
f['A3_min_szn']=asof_player(f.MIN); f['A4_min_l10']=lastk(f.MIN)
team=f.groupby(['GAME_ID','TEAM_ID'])[['FGA','AST']].transform('sum')
f['A5_fgash_szn']=asof_player(f.FGA,team.FGA); f['A6_astsh_szn']=asof_player(f.AST,team.AST)
# passing / rebounding daily
pas=[];reb=[]
for s in seasons:
    for fn in glob.glob(R+f'intake/nba_official_20261013/{s}/*_Player_Passing.json.gz'):
        dt=re.search(r'(\d{4}-\d\d-\d\d)',fn).group(1); d=json.load(gzip.open(fn))['resultSets'][0]; x=pd.DataFrame(d['rowSet'],columns=d['headers']); x['date']=dt; pas.append(x[['PLAYER_ID','date','POTENTIAL_AST']])
    for fn in glob.glob(R+f'intake/nba_official_20261013/{s}/*_Player_Rebounding.json.gz'):
        dt=re.search(r'(\d{4}-\d\d-\d\d)',fn).group(1); d=json.load(gzip.open(fn))['resultSets'][0]; x=pd.DataFrame(d['rowSet'],columns=d['headers']); x['date']=dt; reb.append(x[['PLAYER_ID','date','REB_CHANCES']])
pas=pd.concat(pas); reb=pd.concat(reb); pas['date']=pd.to_datetime(pas.date); reb['date']=pd.to_datetime(reb.date)
pdates=set(pas.date); rdates=set(reb.date)
f=f.merge(pas,on=['PLAYER_ID','date'],how='left').merge(reb,on=['PLAYER_ID','date'],how='left')
f.loc[f.date.isin(pdates)&f.POTENTIAL_AST.isna(),'POTENTIAL_AST']=0; f.loc[f.date.isin(rdates)&f.REB_CHANCES.isna(),'REB_CHANCES']=0
print('passing coverage',f.POTENTIAL_AST.notna().groupby(f.season).mean().round(3).to_dict(),'reb',f.REB_CHANCES.notna().groupby(f.season).mean().round(3).to_dict())
f['A7_potast_szn']=asof_player(f.POTENTIAL_AST); f['A8_rebch_szn']=asof_player(f.REB_CHANCES)
f['started']=(f.starter=='Y').astype(float).where(f.starter.isin(['Y','N']))
f['A9_started']=f.started
f['A10_started3of5']=pd.Series(f.started).groupby([f.PLAYER_ID,f.season]).transform(lambda z: z.shift(1).rolling(5,min_periods=5).sum()).ge(3).astype(float).where(pd.Series(f.started).groupby([f.PLAYER_ID,f.season]).cumcount()>=5)
# rotation spot: rank on team by season-to-date minutes among players who appeared in team's previous game
f['_minszn']=f.A3_min_szn
tgm=f[['season','TEAM_ID','date','PLAYER_ID','_minszn']]
prevgame=tg.sort_values('date')[['season','TEAM_ID','date']].drop_duplicates(); prevgame['prev_date']=prevgame.groupby(['season','TEAM_ID']).date.shift(1)
f=f.merge(prevgame,on=['season','TEAM_ID','date'],how='left')
appeared=f[['TEAM_ID','date','PLAYER_ID']].rename(columns={'date':'prev_date'}); appeared['in_prev']=True
f=f.merge(appeared,on=['TEAM_ID','prev_date','PLAYER_ID'],how='left'); f['in_prev']=f.in_prev.fillna(False).astype(bool)
# v1.2 (review D5): rank every player who appeared in the team's previous game (whether or not he plays tonight)
# by his season-to-date minutes state after that previous game (= his last game before D); prev-season fallback as asof_player
g=[f.PLAYER_ID,f.season]; ncum=f.groupby(['PLAYER_ID','season']).cumcount()+1; mcum=f.MIN.fillna(0).groupby(g).cumsum()/ncum
prevs=f.groupby(['PLAYER_ID','season']).agg(pg=('MIN','size'),pm=('MIN','mean')).reset_index(); prevs['season']=prevs.season.map({'2024-25':'2025-26'}); prevs=prevs.dropna()
after=f[['PLAYER_ID','season','TEAM_ID','date']].assign(ncum=ncum.values,mcum=mcum.values).merge(prevs,on=['PLAYER_ID','season'],how='left')
after['mstate']=np.where(after.ncum>=5,after.mcum,np.where(after.pg.fillna(0)>=10,after.pm,np.nan))
after['A11_rot_rank']=after.groupby(['TEAM_ID','date']).mstate.rank(ascending=False,method='first')
f=f.merge(after[['PLAYER_ID','TEAM_ID','date','A11_rot_rank']].rename(columns={'date':'prev_date'}),on=['PLAYER_ID','TEAM_ID','prev_date'],how='left')
f.loc[~f.in_prev,'A11_rot_rank']=np.nan
f['A11_rotation_5to9']=np.where(f.A11_rot_rank.notna(),f.A11_rot_rank.between(5,9),np.nan)
# salary tertile on the slate date within posg
f['A12_sal']=f.sal_dk
for c in ['A1_usg_szn','A2_usg_l10','A3_min_szn','A4_min_l10','A5_fgash_szn','A6_astsh_szn','A7_potast_szn','A8_rebch_szn']:
    f[c+'_t']=tertile(c)
sq=f.groupby(['season','date','posg']).A12_sal.transform(lambda z: z.quantile(1/3)); sh=f.groupby(['season','date','posg']).A12_sal.transform(lambda z: z.quantile(2/3))
f['A12_sal_t']=np.select([f.A12_sal>=sh,f.A12_sal>=sq,f.A12_sal<sq],['top','middle','bottom'],default='n/a')
# in-game shape
med=f.groupby('PLAYER_ID')[['MIN','usage','FGA']].transform('median')
f['IG_min_above_med']=f.MIN>med.MIN; f['IG_usg_above_med']=f.usage>med.usage; f['IG_fga_above_med']=f.FGA>med.FGA
f['dkpm']=f.dk/f.MIN; f['IG_dkpm_above_med']=f.dkpm>f.groupby('PLAYER_ID').dkpm.transform('median')
f.to_parquet('frame_a.parquet')
print('A done', f.shape)
