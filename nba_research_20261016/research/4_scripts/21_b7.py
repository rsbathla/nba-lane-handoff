import pandas as pd, numpy as np
o=pd.read_parquet('onoff_pairs.parquet'); fr=pd.read_parquet('frame.parquet')[['GAME_ID','PLAYER_ID','MIN','FGA','FTA','TOV','date']]
g=o.groupby(['GAME_ID','P']).first().reset_index(); g['m']=g.min_on+g.min_off; g['pl']=g.pl_on+g.pl_off
v=g.merge(fr,left_on=['GAME_ID','P'],right_on=['GAME_ID','PLAYER_ID'])
print('minutes corr',round(v.m.corr(v.MIN),4),'mean abs diff',round((v.m-v.MIN).abs().mean(),2),'| plays corr',round(v.pl.corr(v.FGA+0.44*v.FTA+v.TOV),4))
o=o.merge(fr[['GAME_ID','date']].drop_duplicates(),on='GAME_ID')
f=pd.read_parquet('frame_abcd.parquet'); f=f[f.qual].copy()
# prior on/off for (P, X=top_usg) over earlier games this season, same team
o=o.sort_values('date')
key=['season','TEAM_ID','P','X']
for c in ['min_on','min_off','pl_on','pl_off','tp_on','tp_off']: o['c_'+c]=o.groupby(key)[c].cumsum()
cum=o[key+['date']+['c_'+c for c in ['min_on','min_off','pl_on','pl_off','tp_on','tp_off']]]
x=f[['GAME_ID','PLAYER_ID','TEAM_ID','season','date','top_usg','B1_top_usg_out','upside','pbp_window']].dropna(subset=['top_usg']).copy()
x['top_usg']=x.top_usg.astype(int); x=x.sort_values('date')
m=pd.merge_asof(x,cum.rename(columns={'P':'PLAYER_ID','X':'top_usg'}).sort_values('date'),on='date',by=['season','TEAM_ID','PLAYER_ID','top_usg'],allow_exact_matches=False)
m['sh_on']=m.c_pl_on/m.c_tp_on*100; m['sh_off']=m.c_pl_off/m.c_tp_off*100
ok=(m.c_min_on>=100)&(m.c_min_off>=100)&m.pbp_window
m['B7']=np.where(ok,(m.sh_off-m.sh_on)>=3,np.nan)
y=m[(m.B1_top_usg_out==1)&m.B7.notna()]
for s,g in y.groupby('season'):
    p=g[g.B7==1]; a=g[g.B7==0]
    print(s,'nights top-usage teammate out with prior on/off',len(g),'| B7 present',f'{int(p.upside.sum())}/{len(p)} = {p.upside.mean()*100:.1f}%','absent',f'{int(a.upside.sum())}/{len(a)} = {a.upside.mean()*100:.1f}%','diff',round((p.upside.mean()-a.upside.mean())*100,1))
# reference: B1 nights overall vs not
m.to_parquet('b7.parquet')
