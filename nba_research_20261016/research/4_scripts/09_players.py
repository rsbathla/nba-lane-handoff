import pandas as pd, numpy as np
r=pd.read_parquet('counts_long.parquet')
idx=['PLAYER_ID','player','posg','games','p75','usage_top','usage_middle','usage_bottom','type','cond','kind']
w=r.pivot_table(index=idx,columns='season',values=['n_present','up_present','n_absent','up_absent','diff_pts'],aggfunc='first').reset_index()
w.columns=['_'.join([c for c in col if c]).replace('2024-25','24').replace('2025-26','25') for col in w.columns]
for c in ['n_present_24','n_present_25','up_present_24','up_present_25','n_absent_24','n_absent_25','up_absent_24','up_absent_25']: w[c]=w[c].fillna(0).astype(int)
d1,d2=w.diff_pts_24,w.diff_pts_25
enough=(w.n_present_24>=5)&(w.n_present_25>=5)&(w.n_absent_24>=5)&(w.n_absent_25>=5)
w['status']=np.select([
  ~enough,
  (d1>0)&(d2>0)&~((d1.abs()<=5)&(d2.abs()<=5)),
  (d1.abs()<=5)&(d2.abs()<=5),
  (d1<0)&(d2<0),
  d1*d2<0],
  ['too few games','lead','flat','negative both seasons','reversed'],default='other')
w['small']=enough&((w.n_present_24<10)|(w.n_present_25<10))
w['lead_strength']=np.where(w.status=='lead',np.minimum(d1,d2),np.nan)
# cross vs leg-alone and vs opp-alone for same player/type/cond
leg=w[w.kind=='leg'][['PLAYER_ID','type','diff_pts_24','diff_pts_25','n_present_24','n_present_25','n_absent_24','n_absent_25']].rename(columns=lambda c: c if c in('PLAYER_ID','type') else 'leg_'+c)
opp=w[w.kind=='opp'][['PLAYER_ID','type','cond','diff_pts_24','diff_pts_25']].rename(columns={'diff_pts_24':'opp_d24','diff_pts_25':'opp_d25'})
w=w.merge(leg,on=['PLAYER_ID','type'],how='left').merge(opp,on=['PLAYER_ID','type','cond'],how='left')
# leg always present (or never): leg alone not defined
w['leg_degenerate']=(w.leg_n_absent_24<5)|(w.leg_n_absent_25<5)|(w.leg_n_present_24<5)|(w.leg_n_present_25<5)
cx=w.kind=='cross'
beats_leg=(w.diff_pts_24>w.leg_diff_pts_24)&(w.diff_pts_25>w.leg_diff_pts_25)
w['cross_note']=np.where(cx&(w.status=='lead'),np.where(w.leg_degenerate,'player leg present nearly every game (cross = opponent leg for him)',np.where(beats_leg,'beats his leg alone','player leg restated')),'')
w.to_parquet('players_wide.parquet')
fam=w.groupby(['kind']).size()
print('family sizes',fam.to_dict())
print(w.groupby(['kind','status']).size().unstack(fill_value=0))
hd=w[w.cond.isin(['vol_szn_b5','vol_szn_b10','eff_szn_b5','eff_szn_b10','ml_b5','ml_b10'])&(w.kind=='opp')]
print('headline opp rows',len(hd)); print(hd.status.value_counts().to_dict())
# reference: if no relation, how often would "lead" happen by chance? compare to share of negative-both
