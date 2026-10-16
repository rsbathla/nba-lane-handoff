import pandas as pd, numpy as np
P=pd.read_csv('pooled_overall.csv'); C=pd.read_csv('controls.csv'); w=pd.read_parquet('players_wide.parquet')
names={'cs3':'Catch-and-shoot 3','pu3':'Pull-up 3','pu2':'Pull-up 2','lt10':'Under 10 ft','wo':'Wide open','rim':'Rim 0-3 ft','paint':'Short paint 3-10 ft','mid':'Mid-range','c3':'Corner 3','atb3':'Above-break 3','trans':'Transition (proxy)','ftr':'Free-throw rate',
 'ml_cs':'ML C&S','ml_pu':'ML Pull Up','ml_lt10':'ML <10ft','ml_pitp':'ML PITP','ml_mid':'ML Mid','ml_3pt':'ML 3PT'}
def cell(r,s):
    return f"{int(r[f'up_present_{s}'])}/{int(r[f'n_present_{s}'])} = {r[f'rate_p_{s}']*100:.1f}% vs {r[f'rate_a_{s}']*100:.1f}% (**{r[f'diff_{s}']:+.1f}**)"
lines=[]
def table(cond_map,title):
    lines.append(f'\n### {title}\n')
    lines.append('| Shot type | Condition | 2024-25: upside when present (rate) vs absent | 2025-26: same |')
    lines.append('|---|---|---|---|')
    for t in names:
        for c,lab in cond_map.items():
            r=P[(P.type==t)&(P.cond==c)&(P.kind=='opp')]
            if len(r)==0: continue
            r=r.iloc[0]; lines.append(f'| {names[t]} | {lab} | {cell(r,"2024-25")} | {cell(r,"2025-26")} |')
table({'vol_szn_b5':'Volume allowed, bottom 5','eff_szn_b5':'eFG allowed, bottom 5','ml_b5':'ML rank 26-30'},'Table 1. Opponent leg alone, bottom 5 (all qualifying players pooled)')
table({'vol_szn_b10':'Volume allowed, bottom 10','eff_szn_b10':'eFG allowed, bottom 10','ml_b10':'ML rank 21-30'},'Table 2. Opponent leg alone, bottom 10')
# controls
def d(t):
    if isinstance(t,str): t=eval(t.replace('np.float64',''))
    return f'{t[3]:+.1f}' if t else ''
lines.append('\n### Table 3. Does the match to his shot type add anything? (difference in points, 2024-25 / 2025-26)\n')
lines.append('| Shot type | Condition | All players | Players who lean on the type | Players who do not | Only games vs defenses outside DRtg bottom 10 | Share of these games also vs a DRtg bottom-10 defense |')
lines.append('|---|---|---|---|---|---|---|')
for _,r in C.iterrows():
    lines.append(f"| {names[r.type]} | {r.cond.replace('_szn','').replace('_',' ')} | {d(r.all_24)} / {d(r.all_25)} | {d(r.leans_24)} / {d(r.leans_25)} | {d(r.not_leans_24)} / {d(r.not_leans_25)} | {d(r.vs_non_weak_D_24)} / {d(r.vs_non_weak_D_25)} | {r.share_also_DRtg_b10:.0%} |")
# carry-over
e=w[(w.n_present_24>=5)&(w.n_present_25>=5)&(w.n_absent_24>=5)&(w.n_absent_25>=5)]
hd=e[e.cond.isin(['vol_szn_b5','vol_szn_b10','eff_szn_b5','eff_szn_b10','ml_b5','ml_b10'])]
lines.append('\n### Table 4. Do per-player reads carry from 2024-25 into 2025-26?\n')
lines.append('| Rows | Group by 2024-25 difference | Rows | Positive again in 2025-26 | Mean 2025-26 difference |'); lines.append('|---|---|---|---|---|')
for kind,lab in [('opp','Opponent leg alone'),('cross','Cross (leans on it AND opponent bottom)')]:
    x=hd[hd.kind==kind]
    for g,m in [('+10 or more',x.diff_pts_24>=10),('-10 to +10',x.diff_pts_24.abs()<10),('-10 or less',x.diff_pts_24<=-10)]:
        y=x[m]; lines.append(f'| {lab} | {g} | {len(y):,} | {(y.diff_pts_25>0).mean():.1%} | {y.diff_pts_25.mean():+.1f} |')
st=hd[hd.kind=='opp'].status.value_counts()
lines.append(f"\nPer-player headline opponent rows with enough games both seasons: {int(st.sum()-st.get('too few games',0)):,}. Lead both seasons: {st.get('lead',0):,}. Negative both seasons: {st.get('negative both seasons',0):,}. Flat: {st.get('flat',0):,}. Reversed: {st.get('reversed',0):,}. Too few games: {st.get('too few games',0):,}.")
open('/home/claude/nba/build/report_tables.md','w').write('\n'.join(lines))
print('\n'.join(lines)[:3000])
