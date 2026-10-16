# Regenerates the layers A-D report tables (1-5) and CSV outputs from the current build files (review D1)
import pandas as pd, numpy as np
OUT='/mnt/project-files/nba/p1_historical/layers_a_d/'
P=pd.read_csv('pooled_ad.csv')
S=['2024-25','2025-26']
def cell(r): return f"{int(r.up_present)}/{int(r.n_present)} = {r.rate_p*100:.1f}% vs {r.rate_a*100:.1f}% (**{r.diff_pts:+.1f}**)"
md=[]
# Table 1
t=P[P.by=='season']
order=list(dict.fromkeys(t.cond))
md.append('## Table 1. Every A-D condition, pooled (upside when present vs absent)\n\n| Layer | Condition | 2024-25 upside when present vs absent | 2025-26 |\n|---|---|---|---|')
for c in order:
    x=t[t.cond==c].set_index('season')
    if not all(s in x.index for s in S): continue
    lab=x.label.iloc[0]
    if '=' in c and not lab.endswith(c.split('=')[1]): lab=f"{lab} = {c.split('=')[1]}"
    md.append(f"| {x.layer.iloc[0]} | {lab} | {cell(x.loc[S[0]])} | {cell(x.loc[S[1]])} |")
# Table 2
T2=[('A9_started','started (confirmed lineup)'),('B1_top_usg_out','top-usage teammate out'),('B2_top_ast_out','top-assist teammate out'),('B4_samepos_starter_out','same-position starter out'),('B5_two_rotation_out','2+ rotation teammates out'),('D1_drtg_rk_b5','defensive rating, bottom 5'),('D3_dvpadj_rk_b5','DvP opponent-adjusted, bottom 5'),('C1_itt_open_t=top','opening implied team total = top'),('C4_both_fast','both teams top-10 pace')]
t2=P[P.by=='season+A1_usg_szn_t']
md.append('\n## Table 2. Inside usage tiers (season-to-date usage, top / middle / bottom third at his position)\n\n| Condition | Usage tier | 2024-25 diff (present games) | 2025-26 diff (present games) |\n|---|---|---|---|')
for c,l in T2:
    for tier in ['top','middle','bottom']:
        x=t2[(t2.cond==c)&(t2.A1_usg_szn_t==tier)].set_index('season')
        md.append(f"| {l} | {tier} | {x.loc[S[0]].diff_pts:+.1f} ({int(x.loc[S[0]].n_present):,}) | {x.loc[S[1]].diff_pts:+.1f} ({int(x.loc[S[1]].n_present):,}) |")
# Sweep outputs and Table 3
pr=pd.read_parquet('sweep_pairs.parquet'); ok=pr.read
rd=pr[ok].copy()
rd['interaction_2024']=rd.inter_2024; rd['interaction_2025']=rd.inter_2025
rd.drop(columns=[c for c in rd.columns if c.startswith('inter_')]).to_csv(OUT+'sweep_all_readable_cells.csv.gz',index=False,compression='gzip')
L=rd[rd.status=='cross lead'].sort_values('margin',ascending=False)
L2=pd.DataFrame({'usage tier':L.tier,'pos':L.pos,'condition 1':L.cond_i,'condition 2':L.cond_j,
  '2024-25 present games':L.n_p_2024,'2024-25 cross diff':L.diff_2024.round(1),'2024-25 cond 1 alone':L.i_d24.round(1),'2024-25 cond 2 alone':L.j_d24.round(1),
  '2025-26 present games':L.n_p_2025,'2025-26 cross diff':L.diff_2025.round(1),'2025-26 cond 1 alone':L.i_d25.round(1),'2025-26 cond 2 alone':L.j_d25.round(1),
  'margin over better leg':L.margin.round(1),'interaction vs additive 2024-25':L.inter_2024.round(1),'interaction vs additive 2025-26':L.inter_2025.round(1)})
L2.to_csv(OUT+'sweep_cross_leads.csv',index=False)
nc=len(set(pr.cond_i)|set(pr.cond_j)); npairs=pr[['i','j']].drop_duplicates().shape[0]
md.append(f"\n## Table 3. The sweep's largest cross leads with 100+ present games in each season\n\nFull list: `sweep_cross_leads.csv` ({len(L):,} rows); every readable cell: `sweep_all_readable_cells.csv.gz`. Family: {nc} pregame conditions, {npairs:,} pairs, 15 usage-tier x position groups ({int(ok.sum()):,} readable cells).\n\n| Usage tier | Pos | Condition 1 | Condition 2 | 2024-25 cross (n) / leg 1 / leg 2 | 2025-26 cross (n) / leg 1 / leg 2 |\n|---|---|---|---|---|---|")
for _,r in L[(L.n_p_2024>=100)&(L.n_p_2025>=100)].head(15).iterrows():
    md.append(f"| {r.tier} | {r.pos} | {r.cond_i} | {r.cond_j} | {r.diff_2024:+.1f} ({int(r.n_p_2024)}) / {r.i_d24:+.1f} / {r.j_d24:+.1f} | {r.diff_2025:+.1f} ({int(r.n_p_2025)}) / {r.i_d25:+.1f} / {r.j_d25:+.1f} |")
# 2x2 interaction summary
bl=ok&(pr.i_d24>0)&(pr.i_d25>0)&(pr.j_d24>0)&(pr.j_d25>0)
four=lambda m: m&(pr.n_min4_2024>=30)&(pr.n_min4_2025>=30)
def summ(m):
    I=pr[four(m)]; return len(I),int(((I.inter_2024<0)&(I.inter_2025<0)).sum()),int(((I.inter_2024>0)&(I.inter_2025>0)).sum()),int((I.inter_2024*I.inter_2025<=0).sum()),I.inter_2024.median(),I.inter_2025.median()
a=summ(bl); b=summ(ok)
md.append(f"\n**Do crosses stack?** Counted as a 2x2 inside each cell (both present / only condition 1 / only condition 2 / neither, each group 30+ games both seasons), interaction = (both - neither) - (only 1 - neither) - (only 2 - neither). Where both legs lift on their own in both seasons ({a[0]:,} cells): below additive in both seasons {a[1]:,}, above additive in both {a[2]:,}, mixed {a[3]:,}; median interaction {a[4]:+.1f} / {a[5]:+.1f} points. All readable cells ({b[0]:,}): below {b[1]:,}, above {b[2]:,}, mixed {b[3]:,}; median {b[4]:+.1f} / {b[5]:+.1f}.")
# Table 4 P2 pooled
PW=pd.read_csv('p2_pooled.csv'); pre=PW[~PW.lock_or_ingame]
T4=pre[pre.diff_build.abs()>=2.5].sort_values('diff_build',ascending=False)
md.append("\n## Table 4. P2 pooled: build window (2024-25 + 2025-26 before Jan 15) vs read window (after Jan 15), conditions with |build diff| >= 2.5\n\nThe upside threshold is frozen from build games only, so the read window's base rate is 30.9% (late-season scoring is higher).\n\n| Condition | Build window diff (present games) | Read window diff (present games) | Same direction |\n|---|---|---|---|")
for _,r in T4.iterrows():
    md.append(f"| {r.cond} | {r.diff_build:+.1f} ({int(r.n_p_build):,}) | {r.diff_read:+.1f} ({int(r.n_p_read):,}) | {'yes' if r.same_sign else '**no**'} |")
b3=pre[pre.diff_build.abs()>=3]
md.append(f"\nAll {len(pre)} pregame conditions: {int(pre.same_sign.sum())} kept their sign ({pre.same_sign.mean()*100:.0f}%). With a build difference of 3+ points: {int(b3.same_sign.sum())} of {len(b3)}.")
# Table 5
R=pd.read_csv('p2_perplayer_summary.csv')
md.append("\n## Table 5. P2 per player: do personal reads carry forward?\n\nA row is one player x condition with 10+ present and 10+ absent build games and 5+ / 5+ read games. A build lead is a build difference of +10 or more; a build negative is -10 or less.\n\n| Layer | Rows | Build leads | Positive again in read | Build negatives | Positive in read | Correlation build vs read |\n|---|---|---|---|---|---|---|")
for _,r in R.iterrows():
    md.append(f"| {r.layer} | {int(r.rows):,} | {int(r['build leads']):,} | {r['leads positive in read']*100:.1f}% | {int(r['build negatives']):,} | {r['negatives positive in read']*100:.1f}% | {r['corr build-read']:.3f} |")
open('ad_report_tables.md','w').write('\n'.join(md)+'\n')
# per-player csv
r=pd.read_parquet('counts_ad_long.parquet'); f=pd.read_parquet('frame_abcd.parquet',columns=['PLAYER_ID','PLAYER_NAME','posg','qual'])
nm=f[f.qual].drop_duplicates('PLAYER_ID').set_index('PLAYER_ID')
r['cnt']=r.up_present.astype(int).astype(str)+'/'+r.n_present.astype(int).astype(str); r['cna']=r.up_absent.astype(int).astype(str)+'/'+r.n_absent.astype(int).astype(str)
w=r.pivot_table(index=['PLAYER_ID','layer','label','cond'],columns='season',values=['cnt','cna','diff_pts'],aggfunc='first').reset_index()
w.columns=[a if not b else f'{b} {a}' for a,b in w.columns]
w.insert(0,'player',w.PLAYER_ID.map(nm.PLAYER_NAME)); w.insert(1,'pos',w.PLAYER_ID.map(nm.posg))
w=w.rename(columns={f'{s} cnt':f'{s} upside when present' for s in S}|{f'{s} cna':f'{s} upside when absent' for s in S}|{f'{s} diff_pts':f'{s} diff (pts)' for s in S})
cols=['player','pos','layer','label','cond']+[f'{s} {k}' for s in S for k in ['upside when present','upside when absent','diff (pts)']]
w[cols].sort_values(['player','cond']).round(1).to_csv(OUT+'layers_a_d_per_player.csv',index=False)
import shutil
for fn in ['pooled_ad.csv']: shutil.copy(fn,OUT+fn)
for fn in ['p2_pooled.csv','p2_perplayer_summary.csv']: shutil.copy(fn,'/mnt/project-files/nba/p2_forward/'+fn)
print('\n'.join(md[-12:]))
q=pd.read_parquet('p2_perplayer.parquet'); q.to_csv('/mnt/project-files/nba/p2_forward/p2_perplayer_rows.csv.gz',index=False,compression='gzip')
