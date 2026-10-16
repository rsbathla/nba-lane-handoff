import pandas as pd, numpy as np, sys
D=pd.Timestamp(sys.argv[1] if len(sys.argv)>1 else '2026-03-18'); GID=sys.argv[2] if len(sys.argv)>2 else '0022501007'
OUT=f'/mnt/project-files/nba/p3_live/template_{D.date()}/'
f=pd.read_parquet('frame_abcd.parquet'); tg=pd.read_parquet('teamgames.parquet'); B=pd.read_pickle('/tmp/board.pkl')
st=pd.read_parquet('opp_state.parquet'); rk=pd.read_parquet('opp_ranks.parquet'); P2=pd.read_csv('p2_pooled.csv').set_index('cond')
g=f[f.GAME_ID==GID]; teams=g.drop_duplicates('TEAM_ID')[['TEAM_ID','TEAM_ABBREVIATION','OPP_ID','OPP','home','open_spread','open_total','close_spread','close_total','itt_open']]
season=g.season.iloc[0]
TYPES={'cs3':'C&S 3','pu3':'Pull-up 3','pu2':'Pull-up 2','lt10':'Under 10 ft','wo':'Wide open','rim':'Rim','paint':'Short paint','mid':'Mid-range','c3':'Corner 3','atb3':'Above-break 3','trans':'Transition','ftr':'FT rate'}
acol={'cs3':'cs3_a','pu3':'pu3_a','pu2':'pu2_a','lt10':'lt10_a','wo':'wo_a','rim':'rim_a','paint':'paint_a','mid':'mid_a','c3':'c3_a','atb3':'atb3_a','trans':'trans_a','ftr':'FTA'}
# team offense rates per 100 as of D (earlier games this season), ranks 30 = most
o=f[(f.season==season)&(f.date<D)]
tgo=o.groupby(['GAME_ID','TEAM_ID']).agg(**{k:(c,'sum') for k,c in acol.items()},POSS=('POSS','first')).reset_index()
off=tgo.groupby('TEAM_ID').sum(numeric_only=True); 
for k in acol: off[k]=off[k]/off.POSS*100
offr=off[list(acol)].rank(method='max')
# team ratings as of D
t=tg[(tg.season==season)&(tg.date<D)]; tr=t.groupby('TEAM_ID').apply(lambda x: pd.Series({'ORtg':np.average(x.OFF_RATING,weights=x.POSS),'DRtg':np.average(x.DEF_RATING,weights=x.POSS),'Pace':x.PACE.mean(),'G':len(x)}),include_groups=False)
trk=pd.DataFrame({'ORtg_rk':tr.ORtg.rank(ascending=False,method='min'),'DRtg_rk':tr.DRtg.rank(method='max'),'Pace_rk':tr.Pace.rank(ascending=False,method='min')})  # ORtg 1 = best offense; DRtg 30 = worst defense; pace 1 = fastest
prev=tg[tg.season=='2024-25']; pr=prev.groupby('TEAM_ID').apply(lambda x: pd.Series({'ORtg':np.average(x.OFF_RATING,weights=x.POSS),'DRtg':np.average(x.DEF_RATING,weights=x.POSS),'Pace':x.PACE.mean()}),include_groups=False)
prk=pd.DataFrame({'ORtg_rk':pr.ORtg.rank(ascending=False,method='min'),'DRtg_rk':pr.DRtg.rank(method='max'),'Pace_rk':pr.Pace.rank(ascending=False,method='min')})
dr=rk[(rk.season==season)&(rk.date==D)].set_index('TEAM_ID')
L=[]; A=teams.iloc[0]; H=teams.iloc[1] if teams.iloc[1].home else teams.iloc[0]; A=teams[teams.TEAM_ID!=H.TEAM_ID].iloc[0]
L.append(f"# {A.TEAM_ABBREVIATION} @ {H.TEAM_ABBREVIATION}, {D.date()} (archived template)\n")
L.append("Template for the nightly game report (plan v2 section 6). Everything above the line \"After the fact\" uses only what was known by lock on this date: ranks from earlier games this season, lines from BigDataBall, projected minutes from Ramneik's 18:06 export, and who played 0 minutes (decision 5). League lifts in brackets are the P2 build-window differences (games before 2026-01-15), so no later game informs them. Ranks are of 30; for defense 1 = stingiest and 30 = most generous.\n")
# findings
B=B[B.game.str.contains(A.TEAM_ABBREVIATION)&B.game.str.contains(H.TEAM_ABBREVIATION)]
def itt(r): return r.open_total/2-r.open_spread/2
L.append("## Findings\n")
fl=[]
for T,O in [(A,H),(H,A)]:
    ab=B[B.team==T.TEAM_ABBREVIATION]['rotation teammates out (played 0 min; 15+ mpg)'].iloc[0]
    fl.append(f"- **{T.TEAM_ABBREVIATION}**: opening spread {T.open_spread:+.1f}, implied total {itt(T):.1f}. Rotation players out: {ab or 'none'}. Opponent {O.TEAM_ABBREVIATION} defense is {int(trk.DRtg_rk[O.TEAM_ID])}/30 by DRtg.")
L+=fl
neg=dr.loc[H.TEAM_ID,'pu3_vol_szn_rk'], dr.loc[A.TEAM_ID,'pu3_vol_szn_rk']
L.append(f"- Pull-up 3 volume allowed: {H.TEAM_ABBREVIATION} {int(neg[0])}/30, {A.TEAM_ABBREVIATION} {int(neg[1])}/30. Bottom 5 here is a **negative** league read (P2 build {P2.loc['E_pu3_vol_b5','diff_build']:+.1f}).")
L.append("\n## Game story\n")
L.append(f"Opening total {A.open_total:.1f} (closing {A.close_total:.1f}); {A.TEAM_ABBREVIATION} {A.open_spread:+.1f} opening, {A.close_spread:+.1f} closing. Pace: {A.TEAM_ABBREVIATION} {int(trk.Pace_rk[A.TEAM_ID])}/30, {H.TEAM_ABBREVIATION} {int(trk.Pace_rk[H.TEAM_ID])}/30 (1 = fastest). Lines and pace set the scoring level of the game; in the study they did not change which players beat their own top quarter (implied team total thirds within 1.3 points both seasons).\n")
L.append("## Team identity (as of this date; 2024-25 full season alongside)\n")
L.append("| | "+A.TEAM_ABBREVIATION+" | "+H.TEAM_ABBREVIATION+" |"); L.append("|---|---|---|")
for c,lab in [('ORtg_rk','Offensive rating rank (1 = best)'),('DRtg_rk','Defensive rating rank (30 = most generous)'),('Pace_rk','Pace rank (1 = fastest)')]:
    L.append(f"| {lab} | {int(trk[c][A.TEAM_ID])} (2024-25: {int(prk[c][A.TEAM_ID])}) | {int(trk[c][H.TEAM_ID])} (2024-25: {int(prk[c][H.TEAM_ID])}) |")
L.append(f"| Record of games so far | {int(tr.G[A.TEAM_ID])} games | {int(tr.G[H.TEAM_ID])} games |")
L.append("\n## Who wins each collision (shot type: offense volume rank vs the other side's volume allowed rank, both of 30, 30 = most)\n")
L.append("| Shot type | "+A.TEAM_ABBREVIATION+" offense | "+H.TEAM_ABBREVIATION+" allows | "+H.TEAM_ABBREVIATION+" offense | "+A.TEAM_ABBREVIATION+" allows | Read |"); L.append("|---|---|---|---|---|---|")
for k,lab in TYPES.items():
    ao,hd,ho,ad=offr.loc[A.TEAM_ID,k],dr.loc[H.TEAM_ID,f'{k}_vol_szn_rk'],offr.loc[H.TEAM_ID,k],dr.loc[A.TEAM_ID,f'{k}_vol_szn_rk']
    reads=[]
    for T,ov,dv,O in [(A,ao,hd,H),(H,ho,ad,A)]:
        if ov>=21 and dv>=21: reads.append(f"{T.TEAM_ABBREVIATION} strength into {O.TEAM_ABBREVIATION} weakness"+(" (a negative read league-wide)" if k=='pu3' else ""))
        elif ov>=21 and dv<=5: reads.append(f"{T.TEAM_ABBREVIATION} strength into {O.TEAM_ABBREVIATION} strength")
    L.append(f"| {lab} | {int(ao)} | {int(hd)} | {int(ho)} | {int(ad)} | {'; '.join(reads) or '-'} |")
L.append("\nThe study found these collisions move upside nights by about 2-4 points and mostly track overall defense, so they are tiebreaks (layer E report).\n")
L.append("## Players\n")
# per-player own splits from earlier games
conds={'B1_top_usg_out':'top-usage teammate out','B2_top_ast_out':'top playmaker out','B4_samepos_starter_out':'same-position starter out','B5_two_rotation_out':'2+ rotation out','A9_started':'started','C5_b2b':'back-to-back','C6_home':'home','D1_drtg_rk_b10':'opp DRtg bottom 10','D3_dvpadj_rk_b10':'opp DvP adj bottom 10'}
fx=f[f.date<D].copy(); fx['D1_drtg_rk_b10']=np.where(fx.D1_drtg_rk.notna(),(fx.D1_drtg_rk>=21).astype(float),np.nan); fx['D3_dvpadj_rk_b10']=np.where(fx.D3_dvpadj_rk.notna(),(fx.D3_dvpadj_rk>=21).astype(float),np.nan)
for _,r in B.sort_values(['team','dk_salary'],ascending=[True,False]).iterrows():
    if not (r['proj_min (18:06 export)']>=15): continue
    pid=f[(f.GAME_ID==GID)&(f.PLAYER_NAME==r.player)].PLAYER_ID.iloc[0]
    h=fx[fx.PLAYER_ID==pid]; line=r['upside line (own top quarter, earlier games)']
    sp=[]
    if isinstance(line,(int,float)):
        h=h.assign(up=h.dk>=line)
        for c,lab in conds.items():
            v=h[c].astype(float); p=h[v==1]; a=h[v==0]
            if len(p)>=8 and len(a)>=8: sp.append((lab,p.up.sum(),len(p),a.up.sum(),len(a),(p.up.mean()-a.up.mean())*100))
    lines=r['pregame lines (league lift, pts)']; pos=[x for x in lines.split(' | ') if x and not x.startswith('NEG')]; negs=[x for x in lines.split(' | ') if x.startswith('NEG')]
    import re as _re
    def lv(x):
        m=_re.findall(r'\(([+-]\d+\.\d)\)',x) or _re.findall(r'([+-]\d+\.\d)\)',x); return float(m[-1]) if m else 0.0
    best=max(pos,key=lv) if pos else None; worst=min(negs,key=lv) if negs else None
    verdict=(f"strongest pregame line is {best.split(' (')[0] if '(' in best else best} ({lv(best):+.1f} league-wide)" if best else "no positive pregame line")+(f"; main caution: {worst.replace('NEG ','').split(' (')[0]} ({lv(worst):+.1f})" if worst else "")
    L.append(f"### {r.player} ({r.team} {r.pos}, ${int(r.dk_salary):,}, projected {r['proj_min (18:06 export)']} min)\n")
    L.append(f"**Verdict:** {verdict[0].upper()+verdict[1:]}. Upside line {line} DK (his own top quarter from earlier games). Usage tier: {r['usage tier']}; prior-10 minutes: {r['prior-10 min tier']}; started: {r['started (lock)']}.\n")
    L.append("Upside checklist (each line with its league lift in points, not added up): " + ('; '.join(pos) if pos else 'none') + ('. Negatives: '+'; '.join(negs) if negs else '') + '.\n')
    if sp:
        b=max(sp,key=lambda z:z[5]); w=min(sp,key=lambda z:z[5])
        L.append(f"His own splits, earlier games (these did not carry forward as a group in P2): best **{b[0]}** {b[1]}/{b[2]} vs {b[3]}/{b[4]} ({b[5]:+.0f}{', small' if min(b[2],b[4])<10 else ''}); strongest negative **{w[0]}** {w[1]}/{w[2]} vs {w[3]}/{w[4]} ({w[5]:+.0f}{', small' if min(w[2],w[4])<10 else ''}).\n")
L.append("---\n## After the fact (not used above)\n")
L.append("| Player | Minutes | DK | Upside line | Upside? |"); L.append("|---|---|---|---|---|")
for _,r in B.sort_values('AFTER THE FACT: DK',ascending=False).iterrows():
    L.append(f"| {r.player} | {r['AFTER THE FACT: minutes']} | {r['AFTER THE FACT: DK']} | {r['upside line (own top quarter, earlier games)']} | {r['AFTER THE FACT: upside']} |")
open(OUT+f'GAME_{A.TEAM_ABBREVIATION}_at_{H.TEAM_ABBREVIATION}.md','w').write('\n'.join(L))
print('\n'.join(L)[:6000])
