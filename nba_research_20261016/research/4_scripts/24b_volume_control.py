# Control for 24: under each type's "volume allowed, season, bottom 10" split, does HIS TOTAL FGA (and minutes) rise as much as the type?
import pandas as pd, numpy as np
f=pd.read_parquet('frame_abcd.parquet'); f=f[f.qual].sort_values(['PLAYER_ID','date']).reset_index(drop=True)
g=[f.PLAYER_ID,f.season]; PB={'rim','paint','mid','c3','atb3','trans'}
def dev(col,ok):
    v=f[col].astype(float).where(ok); n=ok.astype(int); cn=n.groupby(g).cumsum()-n; c=v.fillna(0).groupby(g).cumsum()-v.fillna(0)
    return v-(c/cn.replace(0,np.nan)).where(cn>=5)
rows=[]
for k in ['cs3','pu3','pu2','lt10','wo','rim','paint','mid','c3','atb3','trans','ftr']:
    ac='FTA' if k=='ftr' else f'{k}_a'
    ok=f[ac].notna()&f.FGA.notna()
    if k in PB: ok&=f.pbp_window.astype(bool)
    dt=dev(ac,ok); dF=dev('FGA',ok); dM=dev('MIN',ok)
    rk=f[f'{k}_vol_szn_rk']
    for grp,m in [('all players',pd.Series(True,index=f.index)),('strong in the type',f[f'leg_{k}']==1)]:
        x=pd.DataFrame({'season':f.season,'p':rk>=21,'dt':dt,'dF':dF,'dM':dM})[m&ok&rk.notna()&dt.notna()]
        for s,z in x.groupby('season'):
            a=z[z.p][['dt','dF','dM']].mean(); b=z[~z.p][['dt','dF','dM']].mean()
            rows.append({'type':k,'players':grp,'season':s,'type att lift':a['dt']-b['dt'],'total FGA lift':a.dF-b.dF,'minutes lift':a.dM-b.dM})
R=pd.DataFrame(rows); R.round(3).to_csv('/mnt/project-files/nba/p1_historical/layer_e/volume_check/volume_control_total_fga.csv',index=False)
pd.set_option('display.width',200); print(R.round(2).to_string())
