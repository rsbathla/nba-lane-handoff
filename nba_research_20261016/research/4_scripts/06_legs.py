import pandas as pd, numpy as np
f=pd.read_parquet('frame_shots.parquet'); rk=pd.read_parquet('opp_ranks.parquet')
f=f.sort_values(['PLAYER_ID','date']).reset_index(drop=True)
LEG={'cs3':('cs3_a','trk'),'pu3':('pu3_a','trk'),'pu2':('pu2_a','trk'),'lt10':('lt10_a','trk'),'wo':('wo_a','trk'),
 'rim':('rim_a','pbp'),'paint':('paint_a','pbp'),'mid':('mid_a','pbp'),'c3':('c3_a','pbp'),'atb3':('atb3_a','pbp'),'trans':('trans_a','pbp'),'ftr':('FTA','box'),
 'ml_cs':('cs_a','trk'),'ml_pu':('pu_a','trk'),'ml_lt10':('lt10_a','trk'),'ml_pitp':('pitp_a','pbp'),'ml_mid':('ml_mid_a','pbp'),'ml_3pt':('3pt_a','pbp')}
avail={'trk':f.trk_ok.values,'pbp':f.pbp_ok.values.astype(bool),'box':np.ones(len(f),bool)}
seasons=['2024-25','2025-26']
dates=f[['season','date']].drop_duplicates().sort_values('date')
# per player per season cumulative state, evaluated (a) at each of his games (prior) and (b) at every league date (for tertiles)
recs=[]; at_games={}
for k,(col,src) in list(LEG.items())+[('usage',('usage','box'))]:
    ok=avail[src]&f[col].notna().values
    num=np.where(ok,f[col].fillna(0).values,0.0)
    den=np.where(ok,(f.FGA.values if k!='usage' else 1.0),0.0)
    f['_n']=num; f['_d']=den; f['_g']=ok.astype(int)
    grp=f.groupby(['PLAYER_ID','season'])
    cn=grp._n.cumsum()-f._n; cd=grp._d.cumsum()-f._d; cg=grp._g.cumsum()-f._g
    tot=grp[['_n','_d','_g']].sum().reset_index()
    prev=tot.copy(); prev['season']=prev.season.map({'2024-25':'2025-26'}); prev=prev.dropna(subset=['season'])
    pm=f[['PLAYER_ID','season']].merge(prev,on=['PLAYER_ID','season'],how='left')
    share=np.where((cg>=5)&(cd>0),cn/np.where(cd>0,cd,1),np.nan)
    fb=(cg<5)&(pm._g.fillna(0).values>=10)&(pm._d.fillna(0).values>0)
    share=np.where(fb,pm._n.values/np.where(pm._d.fillna(0).values>0,pm._d.values,1),share)
    f[f'sh_{k}']=share
    # inclusive state after this game (used only for later dates' cutoffs)
    cni=cn+f._n; cdi=cd+f._d; cgi=cg+f._g
    si=np.where((cgi>=5)&(cdi>0),cni/np.where(cdi>0,cdi,1),np.nan)
    fbi=(cgi<5)&(pm._g.fillna(0).values>=10)&(pm._d.fillna(0).values>0)
    f[f'shi_{k}']=np.where(fbi,pm._n.values/np.where(pm._d.fillna(0).values>0,pm._d.values,1),si)
f=f.drop(columns=['_n','_d','_g'])
# tertile cutoffs per position group per date: among all players' as-of shares on that date
# player state at league dates = his share entering his next game after D; approximate by last-known prior state via merge_asof on his games
cut=[]
for s in seasons:
    fs=f[f.season==s][['PLAYER_ID','date','posg']+[c for c in f if c.startswith('shi_')]].sort_values('date')
    ds=dates[dates.season==s].date
    for D in ds:
        # everyone's state as of D: inclusive state after his last game strictly before D (past games only)
        st=fs[fs.date<D].drop_duplicates('PLAYER_ID',keep='last')
        q=st.groupby('posg')[[c for c in st if c.startswith('shi_')]].quantile(2/3)
        q.columns=[c.replace('shi_','sh_') for c in q.columns]
        q['date']=D; q['season']=s; cut.append(q.reset_index())
cut=pd.concat(cut)
f=f.merge(cut,on=['season','date','posg'],how='left',suffixes=('','_cut'))
for k in LEG:
    if k.startswith('ml_'): f[f'leg_{k}']=np.where(f[f'sh_{k}'].notna(),f[f'sh_{k}']>=0.20,np.nan)
    else: f[f'leg_{k}']=np.where(f[f'sh_{k}'].notna()&f[f'sh_{k}_cut'].notna(),f[f'sh_{k}']>=f[f'sh_{k}_cut'],np.nan)
# usage tier
uq=[]
for s in seasons:
    fs=f[f.season==s][['PLAYER_ID','date','posg','shi_usage']].sort_values('date')
    for D in dates[dates.season==s].date:
        st=fs[fs.date<D].drop_duplicates('PLAYER_ID',keep='last')
        if st.empty: continue
        q=st.groupby('posg').shi_usage.quantile([1/3,2/3]).unstack(); q.columns=['u33','u67']; q['date']=D; q['season']=s; uq.append(q.reset_index())
f=f.merge(pd.concat(uq),on=['season','date','posg'],how='left')
f['usage_tier']=np.select([f.sh_usage>=f.u67,f.sh_usage>=f.u33,f.sh_usage<f.u33],['top','middle','bottom'],default='n/a')
# opponent ranks
rk2=rk.rename(columns={'TEAM_ID':'OPP_ID'}).drop(columns=['n_games'])
f=f.merge(rk2,on=['season','date','OPP_ID'],how='left')
# upside
q=f.groupby('PLAYER_ID').dk.quantile(0.75); n=f.groupby('PLAYER_ID').size()
f['p75']=f.PLAYER_ID.map(q); f['ngames']=f.PLAYER_ID.map(n); f['qual']=f.ngames>=20
f['upside']=f.dk>=f.p75
f['pbp_window']=~((f.season=='2024-25')&(f.date>pd.Timestamp('2025-03-24')))
f.to_parquet('frame_e.parquet')
print('qualifying players',f[f.qual].PLAYER_ID.nunique(),'games',f.qual.sum(),'upside share',f[f.qual].upside.mean().round(3))
print('leg availability', {k:round(float(pd.Series(f[f'leg_{k}']).notna().mean()),3) for k in LEG})
print('leg strong share', {k:round(float(pd.Series(f[f'leg_{k}']).mean()),3) for k in LEG})
print(f.usage_tier.value_counts().to_dict())
