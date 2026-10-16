import pandas as pd, numpy as np
p=pd.read_parquet('pbp_shots_typed.parquet'); f=pd.read_parquet('frame_trk.parquet')
p['pid']=p.pid.astype(int)
T=['rim','paint','mid','c3','atb3','trans','pitp','ml_mid','3pt']
agg={}
for t in T:
    p[f'{t}_a']=p[f't_{t}'].astype(int); p[f'{t}_m']=(p[f't_{t}']&p.made).astype(int); p[f'{t}_3m']=(p[f't_{t}']&p.made&p.is3).astype(int)
cols=[c for t in T for c in (f'{t}_a',f'{t}_m',f'{t}_3m')]
g=p.groupby(['gid','pid'])[cols+['is3']].sum().reset_index().rename(columns={'is3':'pbp_3pa'})
g['pbp_fga']=p.groupby(['gid','pid']).size().values
f=f.merge(g,left_on=['GAME_ID','PLAYER_ID'],right_on=['gid','pid'],how='left')
pbp_games=set(p.gid.unique())
f['pbp_ok']=f.GAME_ID.isin(pbp_games)
for c in cols+['pbp_3pa','pbp_fga']: f.loc[f.pbp_ok&f[c].isna(),c]=0
ok=f[f.pbp_ok]
print('pbp games',len(pbp_games),'player-games with pbp',f.pbp_ok.sum(), f.groupby('season').pbp_ok.mean().round(3).to_dict())
print('FGA match box (exact)',(ok.pbp_fga==ok.FGA).mean().round(4),'mean abs diff',(ok.pbp_fga-ok.FGA).abs().mean().round(3))
print('3PA match box',(ok.pbp_3pa==ok.FG3A).mean().round(4))
print('tracking cs+pu<=FGA rows', ((f.cs_fga+f.pu_fga)<=f.FGA)[f.trk_ok].mean().round(4))
f.to_parquet('frame_shots.parquet')
