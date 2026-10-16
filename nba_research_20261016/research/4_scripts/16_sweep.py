import pandas as pd, numpy as np
f=pd.read_parquet('frame_abcd.parquet'); f=f[f.qual].reset_index(drop=True)
C={}
for col in ['A2_usg_l10_t'  # v1.2 (review D7): A1 tier is the cell, not a condition
           ,'A3_min_szn_t','A4_min_l10_t','A5_fgash_szn_t','A6_astsh_szn_t','A7_potast_szn_t','A8_rebch_szn_t','A12_sal_t','C1_itt_open_t','C3_total_open_t']:
    for t in ['top','middle','bottom']: C[f'{col}={t}']=np.where(f[col]=='n/a',np.nan,(f[col]==t).astype(float))
for v in ['fav8+','close','dog8+']: C[f'C2_spread_open={v}']=np.where(f.C2_spread_open=='n/a',np.nan,(f.C2_spread_open==v).astype(float))
for c in ['A10_started3of5','A11_rotation_5to9','B1_top_usg_out','B2_top_ast_out','B3_start_c_out','B4_samepos_starter_out','B5_two_rotation_out','B6_25usg_out','C4_both_fast','C5_b2b','C6_home']: C[c]=f[c].astype(float).values
for c in ['D1_drtg_rk','D2_dvp_rk','D3_dvpadj_rk','D4_orb_rk','D5_tov_rk','D6a_rim_eff_rk','D6b_blk_rk','D7_fta_rk']:
    v=f[c]; C[c+'_b5']=np.where(v.notna(),(v>=26).astype(float),np.nan); C[c+'_b10']=np.where(v.notna(),(v>=21).astype(float),np.nan)
PB={'rim','paint','mid','c3','atb3','trans','ml_pitp','ml_mid','ml_3pt'}
for k in ['cs3','pu3','pu2','lt10','wo','rim','paint','mid','c3','atb3','trans','ftr']:
    for m in ['vol','eff']:
        c=f'{k}_{m}_szn_rk'
        if c not in f: continue
        for cut,th in [('b5',26),('b10',21)]:
            v=f[c].where(f.pbp_window if k in PB else pd.Series(True,index=f.index)); C[f'E_{k}_{m}_{cut}']=np.where(v.notna(),(v>=th).astype(float),np.nan)
    v=f[f'leg_{k}'].astype(float).where(f.pbp_window if k in PB else pd.Series(True,index=f.index)); C[f'E_leg_{k}']=v.values
for k in ['ml_cs','ml_pu','ml_lt10','ml_pitp','ml_mid','ml_3pt']:
    v=f[f'{k}_rk'].where(f.pbp_window if k in PB else pd.Series(True,index=f.index))
    for cut,th in [('b5',26),('b10',21)]: C[f'E_{k}_{cut}']=np.where(v.notna(),(v>=th).astype(float),np.nan)
names=list(C); X=np.column_stack([C[n] for n in names]).astype(float)
M=~np.isnan(X); X1=np.where(M,X,0.0); u=f.upside.values.astype(float)
print('conditions',len(names))
rows=[]
for (s,tier,pos),idx in f.groupby(['season','A1_usg_szn_t','posg']).groups.items():
    if tier=='n/a': continue
    i=np.asarray(idx); x=X1[i]; m=M[i].astype(float); uu=u[i][:,None]
    pres=x.T@x; up_pres=(x*uu).T@x; avail=m.T@m; up_avail=(m*uu).T@m
    # pair availability for absent: both available minus present
    ab=avail-pres; up_ab=up_avail-up_pres
    # v1.2 (review D2): 2x2 groups among games where both conditions are available
    xm=x.T@m; up_xm=(x*uu).T@m
    n10=xm-pres; n01=xm.T-pres; n00=avail-pres-n10-n01
    u10=up_xm-up_pres; u01=up_xm.T-up_pres; u00=up_avail-up_pres-u10-u01
    iu=np.triu_indices(len(names),0)
    rows.append(pd.DataFrame({'season':s,'tier':tier,'pos':pos,'i':iu[0],'j':iu[1],'n_p':pres[iu],'u_p':up_pres[iu],'n_a':ab[iu],'u_a':up_ab[iu],
        'n10':n10[iu],'u10':u10[iu],'n01':n01[iu],'u01':u01[iu],'n00':n00[iu],'u00':u00[iu]}))
R=pd.concat(rows,ignore_index=True)
R['diff']=(R.u_p/R.n_p.replace(0,np.nan)-R.u_a/R.n_a.replace(0,np.nan))*100
rr=lambda u,n: u/n.replace(0,np.nan)
R['inter']=((rr(R.u_p,R.n_p)-rr(R.u00,R.n00))-(rr(R.u10,R.n10)-rr(R.u00,R.n00))-(rr(R.u01,R.n01)-rr(R.u00,R.n00)))*100
R['n_min4']=R[['n_p','n10','n01','n00']].min(axis=1)
W=R.pivot_table(index=['tier','pos','i','j'],columns='season',values=['n_p','u_p','n_a','u_a','diff','inter','n_min4']).reset_index()
W.columns=[f'{a}_{b[:4]}' if b else a for a,b in W.columns]
single=W[W.i==W.j][['tier','pos','i','diff_2024','diff_2025','n_p_2024','n_p_2025']]
pair=W[W.i!=W.j].copy()
for side in ['i','j']:
    s2=single.rename(columns={'i':side,'diff_2024':f'{side}_d24','diff_2025':f'{side}_d25','n_p_2024':f'{side}_n24','n_p_2025':f'{side}_n25'})
    pair=pair.merge(s2,on=['tier','pos',side],how='left')
ok=(pair.n_p_2024>=30)&(pair.n_p_2025>=30)&(pair.n_a_2024>=30)&(pair.n_a_2025>=30)
pair['read']=ok
best24=np.maximum(pair.i_d24,pair.j_d24); best25=np.maximum(pair.i_d25,pair.j_d25)
pair['margin']=np.minimum(pair.diff_2024-best24,pair.diff_2025-best25)
pair['status']=np.select([~ok,(pair.diff_2024>0)&(pair.diff_2025>0)&(pair.margin>0),(pair.diff_2024>0)&(pair.diff_2025>0),(pair.diff_2024.abs()<=5)&(pair.diff_2025.abs()<=5),pair.diff_2024*pair.diff_2025<0],
  ['too few games','cross lead','positive, restates a leg','flat','reversed'],default='negative both / other')
pair['cond_i']=[names[k] for k in pair.i]; pair['cond_j']=[names[k] for k in pair.j]
single['cond']=[names[k] for k in single.i]
pair.to_parquet('sweep_pairs.parquet'); single.to_parquet('sweep_single.parquet')
print('cells',len(pair),'readable',int(ok.sum())); print(pair[ok].status.value_counts().to_dict())
bothlift=ok&(pair.i_d24>0)&(pair.i_d25>0)&(pair.j_d24>0)&(pair.j_d25>0)
four=bothlift&(pair.n_min4_2024>=30)&(pair.n_min4_2025>=30)
I=pair[four]
print('2x2: both legs lift both seasons',int(bothlift.sum()),'with all four groups 30+ both seasons',len(I),
      'below additive both',int(((I.inter_2024<0)&(I.inter_2025<0)).sum()),'above both',int(((I.inter_2024>0)&(I.inter_2025>0)).sum()),
      'mixed',int((I.inter_2024*I.inter_2025<=0).sum()),'median',round(I.inter_2024.median(),2),round(I.inter_2025.median(),2))
allI=pair[ok&(pair.n_min4_2024>=30)&(pair.n_min4_2025>=30)]
print('2x2 all readable with four groups 30+',len(allI),'below both',int(((allI.inter_2024<0)&(allI.inter_2025<0)).sum()),'above both',int(((allI.inter_2024>0)&(allI.inter_2025>0)).sum()),'median',round(allI.inter_2024.median(),2),round(allI.inter_2025.median(),2))
L=pair[pair.status=='cross lead'].sort_values('margin',ascending=False)
pd.set_option('display.width',250)
print(L.head(30)[['tier','pos','cond_i','cond_j','n_p_2024','diff_2024','i_d24','j_d24','n_p_2025','diff_2025','i_d25','j_d25','margin']].round(1).to_string())
