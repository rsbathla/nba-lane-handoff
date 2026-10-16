import pandas as pd, numpy as np
f=pd.read_parquet('frame_abc.parquet'); tg=pd.read_parquet('teamgames.parquet'); rk=pd.read_parquet('opp_ranks.parquet')
# DvP: DK points by posg allowed per game by each defense; adjusted: minus players' own season-to-date avg
f=f.sort_values(['PLAYER_ID','date'])
g=[f.PLAYER_ID,f.season]; n=f.groupby(['PLAYER_ID','season']).cumcount()
f['dk_szn_prior']=(f.dk.groupby(g).cumsum()-f.dk)/n.replace(0,np.nan)
f['dk_resid']=np.where(n>=5,f.dk-f.dk_szn_prior,np.nan)
dv=f.groupby(['season','GAME_ID','OPP_ID','date','posg']).agg(dk=('dk','sum'),res=('dk_resid','sum'),nres=('dk_resid','count')).reset_index()
rows=[]
for (s,t,pg),x in dv.groupby(['season','OPP_ID','posg']):
    x=x.sort_values('date'); cd=np.concatenate([[0],x.dk.cumsum()]); cr=np.concatenate([[0],x.res.cumsum()]); cn=np.concatenate([[0],x.nres.cumsum()])
    ds=np.sort(f[(f.season==s)].date.unique()); i=np.searchsorted(x.date.values,ds,side='left')
    rows.append(pd.DataFrame({'season':s,'date':ds,'OPP_ID':t,'posg':pg,'n':i,'dvp':np.where(i>=1,cd[i]/np.maximum(i,1),np.nan),'dvp_adj':np.where((i>=1)&(cn[i]>0),cr[i]/np.maximum(cn[i],1),np.nan)}))
dvp=pd.concat(rows)
dvp['D2_dvp_rk']=dvp.groupby(['season','date','posg']).dvp.rank(method='max').where(dvp.n>=10); dvp['D3_dvpadj_rk']=dvp.groupby(['season','date','posg']).dvp_adj.rank(method='max').where(dvp.n>=10)
f=f.merge(dvp[['season','date','OPP_ID','posg','D2_dvp_rk','D3_dvpadj_rk']],on=['season','date','OPP_ID','posg'],how='left')
# team defensive aggregates from opponent box: OREB% allowed, TOV forced per 100, blocks per 100, using player box sums
tb=f.groupby(['season','GAME_ID','TEAM_ID','OPP_ID','date']).agg(OREB=('OREB','sum'),DREB=('DREB','sum'),TOV=('TOV','sum'),BLK=('BLK','sum'),POSS=('POSS','first')).reset_index()
o=tb[['GAME_ID','TEAM_ID','DREB','BLK']].rename(columns={'TEAM_ID':'OPP_ID','DREB':'def_dreb','BLK':'def_blk'})
tb=tb.merge(o,on=['GAME_ID','OPP_ID'])  # offense row with defense's DREB/BLK
rows=[]
for (s,t),x in tb.groupby(['season','OPP_ID']):
    x=x.sort_values('date'); c=lambda v: np.concatenate([[0],np.cumsum(v)])
    ore,dre,tov,blk,pos=c(x.OREB.values),c(x.def_dreb.values),c(x.TOV.values),c(x.def_blk.values),c(x.POSS.values)
    ds=np.sort(f[f.season==s].date.unique()); i=np.searchsorted(x.date.values,ds,side='left'); ok=i>=1
    rows.append(pd.DataFrame({'season':s,'date':ds,'OPP_ID':t,'n':i,'orb_allowed':np.where(ok,ore[i]/np.maximum(ore[i]+dre[i],1),np.nan),'tov_forced':np.where(ok,tov[i]/np.maximum(pos[i],1)*100,np.nan),'blk100':np.where(ok,blk[i]/np.maximum(pos[i],1)*100,np.nan)}))
td=pd.concat(rows)
td['D4_orb_rk']=td.groupby(['season','date']).orb_allowed.rank(method='max').where(td.n>=10)           # 30 = allows most offensive rebounds
td['D5_tov_rk']=td.groupby(['season','date']).tov_forced.rank(ascending=False,method='max').where(td.n>=10)  # 30 = forces fewest
td['D6b_blk_rk']=td.groupby(['season','date']).blk100.rank(ascending=False,method='max').where(td.n>=10)     # 30 = fewest blocks
f=f.merge(td[['season','date','OPP_ID','D4_orb_rk','D5_tov_rk','D6b_blk_rk']],on=['season','date','OPP_ID'],how='left')
f['D1_drtg_rk']=f.drtg_rk; f['D6a_rim_eff_rk']=f.rim_eff_szn_rk; f['D7_fta_rk']=f.ftr_vol_szn_rk
f.to_parquet('frame_abcd.parquet')
for c in ['D1_drtg_rk','D2_dvp_rk','D3_dvpadj_rk','D4_orb_rk','D5_tov_rk','D6a_rim_eff_rk','D6b_blk_rk','D7_fta_rk']: print(c, round(f[c].notna().mean(),3))
