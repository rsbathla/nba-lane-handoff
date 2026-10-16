import pandas as pd, numpy as np
w=pd.read_parquet('players_wide.parquet')
H=['vol_szn_b5','vol_szn_b10','eff_szn_b5','eff_szn_b10','ml_b5','ml_b10']
names={'cs3':'Catch-and-shoot 3','pu3':'Pull-up 3','pu2':'Pull-up 2','lt10':'Under 10 ft','wo':'Wide open','rim':'Rim (0-3 ft)','paint':'Short paint (3-10 ft)','mid':'Mid-range','c3':'Corner 3','atb3':'Above-the-break 3','trans':'Transition (proxy)','ftr':'Free-throw rate',
 'ml_cs':'Matchup Lab C&S','ml_pu':'Matchup Lab Pull Up','ml_lt10':'Matchup Lab <10ft','ml_pitp':'Matchup Lab PITP','ml_mid':'Matchup Lab Mid','ml_3pt':'Matchup Lab 3PT'}
cl={'vol_szn_b5':'Volume allowed, bottom 5','vol_szn_b10':'Volume allowed, bottom 10','eff_szn_b5':'eFG allowed, bottom 5','eff_szn_b10':'eFG allowed, bottom 10','ml_b5':'Matchup Lab rank 26-30','ml_b10':'Matchup Lab rank 21-30','player_leg':'He leans on this type'}
x=w[(w.cond.isin(H)&w.kind.isin(['opp','cross']))|(w.kind=='leg')].copy()
x['shot_type']=x.type.map(names); x['condition']=x.cond.map(cl).fillna(x.cond)
x.loc[x.kind=='cross','condition']='He leans on it AND '+x.loc[x.kind=='cross','condition']
x['row']=x.kind.map({'opp':'opponent leg alone','leg':'player leg alone','cross':'cross'})
for s in ['24','25']:
    x[f'present_{s}']=[f'{u}/{n}' for u,n in zip(x[f'up_present_{s}'],x[f'n_present_{s}'])]
    x[f'absent_{s}']=[f'{u}/{n}' for u,n in zip(x[f'up_absent_{s}'],x[f'n_absent_{s}'])]
x['usage_tier_mix']=('top '+(x.usage_top*100).round().astype(int).astype(str)+'% / mid '+(x.usage_middle*100).round().astype(int).astype(str)+'% / bottom '+(x.usage_bottom*100).round().astype(int).astype(str)+'%')
out=x[['player','posg','games','p75','usage_tier_mix','shot_type','row','condition','present_24','absent_24','diff_pts_24','present_25','absent_25','diff_pts_25','status','small','cross_note']].rename(columns={'posg':'pos','p75':'upside_line_dk','present_24':'2024-25 upside when present','absent_24':'2024-25 upside when absent','diff_pts_24':'2024-25 diff (pts)','present_25':'2025-26 upside when present','absent_25':'2025-26 upside when absent','diff_pts_25':'2025-26 diff (pts)'})
out['2024-25 diff (pts)']=out['2024-25 diff (pts)'].round(1); out['2025-26 diff (pts)']=out['2025-26 diff (pts)'].round(1); out['upside_line_dk']=out.upside_line_dk.round(2)
out=out.sort_values(['player','shot_type','row','condition'])
D='/mnt/project-files/nba/p1_historical/layer_e/'
out.to_csv(D+'layer_e_per_player.csv',index=False)
L=out[(out.status=='lead')&(out.row!='player leg alone')&~out.small]
L=L.assign(ls=np.minimum(L['2024-25 diff (pts)'],L['2025-26 diff (pts)'])).sort_values('ls',ascending=False).drop(columns='ls')
L.to_csv(D+'layer_e_leads.csv',index=False); print('leads',len(L))
T=L[L.row=='opponent leg alone'].head(15)
rows=['| Player | Shot type | Condition | 2024-25 present / absent | 2025-26 present / absent |','|---|---|---|---|---|']
for _,r in T.iterrows(): rows.append(f"| {r.player} ({r.pos}) | {r.shot_type} | {r.condition} | {r['2024-25 upside when present']} vs {r['2024-25 upside when absent']} | {r['2025-26 upside when present']} vs {r['2025-26 upside when absent']} |")
open('leads_table.md','w').write('\n'.join(rows))
st=w[w.cond.isin(H)&(w.kind=='opp')].status.value_counts(); print(st.to_dict(), 'family opp',(w.kind=='opp').sum(),'cross',(w.kind=='cross').sum(),'leg',(w.kind=='leg').sum())
