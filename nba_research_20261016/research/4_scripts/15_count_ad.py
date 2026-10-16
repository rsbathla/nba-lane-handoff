import pandas as pd, numpy as np
f=pd.read_parquet('frame_abcd.parquet'); f=f[f.qual].copy().reset_index(drop=True)
C={}  # name -> (layer, label, array of 1/0/nan)
def tier(col,layer,lab):
    v=f[col]
    for t in ['top','middle','bottom']:
        C[f'{col}={t}']=(layer,lab,np.where(v=='n/a',np.nan,(v==t).astype(float)))
for col,lab in [('A1_usg_szn_t','usage rate, season-to-date'),('A2_usg_l10_t','usage rate, prior 10'),('A3_min_szn_t','minutes, season-to-date'),('A4_min_l10_t','minutes, prior 10'),('A5_fgash_szn_t','FGA share of team'),('A6_astsh_szn_t','assist share of team'),('A7_potast_szn_t','potential assists'),('A8_rebch_szn_t','rebound chances'),('A12_sal_t','DK salary on the slate')]:
    tier(col,'A pregame',lab)
C['A9_started']=('A lock-time','started (confirmed lineup)',f.A9_started.values)
C['A10_started3of5']=('A pregame','started 3+ of prior 5',f.A10_started3of5.values)
C['A11_rotation_5to9']=('A pregame','5th-9th man by minutes',f.A11_rotation_5to9.astype(float).values)
for c,l in [('B1_top_usg_out','top-usage teammate out'),('B2_top_ast_out','top-assist teammate out'),('B3_start_c_out','starting center out'),('B4_samepos_starter_out','same-position starter out'),('B5_two_rotation_out','2+ rotation teammates out'),('B6_25usg_out','a 25%+ usage teammate out')]:
    C[c]=('B pregame (0-minute rule)',l,f[c].astype(float).values)
for col,lab,lay in [('C1_itt_open_t','opening implied team total','C pregame'),('C3_total_open_t','opening game total','C pregame'),('C7_itt_close_t','closing implied team total','C lock-time')]:
    tier(col,lay,lab)
for v in ['fav8+','close','dog8+']: C[f'C2_spread_open={v}']=('C pregame',f'opening spread {v}',np.where(f.C2_spread_open=='n/a',np.nan,(f.C2_spread_open==v).astype(float)))
C['C4_both_fast']=('C pregame','both teams top-10 pace',f.C4_both_fast.astype(float).values)
C['C5_b2b']=('C pregame','back-to-back',f.C5_b2b.astype(float).values)
C['C6_home']=('C pregame','home',f.C6_home.astype(float).values)
C['C8_spread_move_toward']=('C lock-time','spread moved 1.5+ toward his team',f.C8_spread_move_toward.astype(float).values)
C['C8_total_up3']=('C lock-time','total moved up 3+',f.C8_total_up3.astype(float).values)
for c,l in [('C9_blowout15','final margin 15+'),('C10_ot','overtime'),('C11_5fouls','5+ fouls'),('IG_min_above_med','minutes above his median'),('IG_usg_above_med','usage above his median'),('IG_fga_above_med','FGA above his median'),('IG_dkpm_above_med','DK per minute above his median')]:
    C[c]=('in-game',l,f[c].astype(float).values)
for c,l in [('D1_drtg_rk','defensive rating'),('D2_dvp_rk','DK points allowed to his position'),('D3_dvpadj_rk','DvP opponent-adjusted'),('D4_orb_rk','offensive rebounds allowed'),('D5_tov_rk','turnovers forced (fewest)'),('D6a_rim_eff_rk','rim eFG allowed'),('D6b_blk_rk','blocks (fewest)'),('D7_fta_rk','FTA allowed per 100')]:
    v=f[c]
    C[c+'_b5']=('D pregame',l+', bottom 5',np.where(v.notna(),(v>=26).astype(float),np.nan))
    C[c+'_b10']=('D pregame',l+', bottom 10',np.where(v.notna(),(v>=21).astype(float),np.nan))
base=f[['PLAYER_ID','PLAYER_NAME','posg','season','upside','A1_usg_szn_t']].copy()
recs=[]; pool=[]
for k,(layer,lab,arr) in C.items():
    x=base.copy(); x['c']=np.asarray(arr,dtype=float); x=x[x.c.notna()]; x['pres']=x.c==1
    g=x.groupby(['PLAYER_ID','season','pres']).upside.agg(['size','sum']).unstack('pres',fill_value=0)
    g.columns=[f'{a}_{"p" if b else "a"}' for a,b in g.columns]
    for c in ['size_p','sum_p','size_a','sum_a']:
        if c not in g: g[c]=0
    g=g.reset_index(); g['cond']=k; g['layer']=layer; g['label']=lab; recs.append(g)
    for by in [['season'],['season','posg'],['season','A1_usg_szn_t']]:
        q=x.groupby(by+['pres']).upside.agg(['size','sum']).unstack('pres',fill_value=0); q.columns=[f'{a}_{"p" if b else "a"}' for a,b in q.columns]
        q=q.reset_index(); q['cond']=k; q['layer']=layer; q['label']=lab; q['by']='+'.join(by); pool.append(q)
r=pd.concat(recs,ignore_index=True).rename(columns={'size_p':'n_present','sum_p':'up_present','size_a':'n_absent','sum_a':'up_absent'})
r['diff_pts']=(r.up_present/r.n_present.replace(0,np.nan)-r.up_absent/r.n_absent.replace(0,np.nan))*100
P=pd.concat(pool,ignore_index=True).rename(columns={'size_p':'n_present','sum_p':'up_present','size_a':'n_absent','sum_a':'up_absent'})
P['rate_p']=P.up_present/P.n_present; P['rate_a']=P.up_absent/P.n_absent; P['diff_pts']=(P.rate_p-P.rate_a)*100
r.to_parquet('counts_ad_long.parquet'); P.to_csv('pooled_ad.csv',index=False)
o=P[P.by=='season'].pivot_table(index=['layer','cond','label'],columns='season',values=['n_present','rate_p','rate_a','diff_pts']).round(3)
o.columns=[f'{a}_{b}' for a,b in o.columns]; pd.set_option('display.width',250)
print(o.reset_index()[['layer','label','cond','n_present_2024-25','rate_p_2024-25','rate_a_2024-25','diff_pts_2024-25','n_present_2025-26','rate_p_2025-26','rate_a_2025-26','diff_pts_2025-26']].to_string())
