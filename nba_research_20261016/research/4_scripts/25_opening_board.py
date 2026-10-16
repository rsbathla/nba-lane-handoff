# Opening-night (and early-season) board: last season's numbers for players and opponents, team changes flagged,
# absences from the latest injury report (status Out) because no 0-minute record exists before tipoff.
# Usage: python3 25_opening_board.py <date> <dk_slate.parquet> <injuries.parquet> <schedule.parquet> [preseason projections csv]
# v2 (review 2026-10-15): injury names keyed from the slate's name_key; pull-up-3 NEG for everyone (as template); tips from schedule;
# roles by last-season position, most starts over 2024-26 (preseason starts break ties); assist share minutes-weighted; usage tier = plain mean (A1).
import pandas as pd, numpy as np, sys, os, unicodedata, re
D=sys.argv[1]; SLATE=sys.argv[2]; INJ=sys.argv[3]; SCHED=sys.argv[4]
PRE=sys.argv[5] if len(sys.argv)>5 else '/home/claude/nba/raw/dfs/nba/analytics/data/preseason_baseline_2026/projections_all_rostered.csv'
RAW='/home/claude/nba/raw/dfs/nba/analytics/data/'
OUT=f'/mnt/project-files/nba/p3_live/{D}/'; os.makedirs(OUT,exist_ok=True)
def norm(x): x=unicodedata.normalize('NFKD',str(x)).encode('ascii','ignore').decode().lower(); x=re.sub(r'[^a-z ]','',x); x=re.sub(r'\b(jr|sr|ii|iii|iv)\b','',x); return ' '.join(x.split())
f=pd.read_parquet('frame_abcd.parquet'); tg=pd.read_parquet('teamgames.parquet'); rk=pd.read_parquet('opp_ranks.parquet')
P2=pd.read_csv('p2_pooled.csv').set_index('cond'); lift=lambda c: (f"{P2.loc[c,'diff_build']:+.1f}" if c in P2.index else '')
abbr=tg.drop_duplicates('TEAM_ID').set_index('TEAM_ID').TEAM_ABBREVIATION; tid=pd.Series(abbr.index,index=abbr.values)
L=f[f.season=='2025-26'].copy()
sl=pd.read_parquet(SLATE); sl=sl[sl.game_type=='classic'].copy()
sl['pid']=sl.person_id; sl['posg']=sl.position_dk.str.split('/').str[0]
inj=pd.read_parquet(INJ); out_keys=set(inj[inj.status=='Out'].name_key.map(norm)); dtd=set(inj[inj.status!='Out'].name_key.map(norm))
pre=pd.read_csv(PRE).set_index('pid')
sch=pd.read_parquet(SCHED); sch=sch[sch.date==D]; tip=dict(zip(sch.home,sch.tip_et.str[11:16]))|dict(zip(sch.away,sch.tip_et.str[11:16]))
# ---- player facts from 2025-26 (all his games, any team)
g=L.groupby('PLAYER_ID')
pf=pd.DataFrame({'gp25':g.size(),'mpg25':g.MIN.mean(),'starts25':g.started.sum(),'team25':g.TEAM_ID.last().map(abbr),
   'usg25':g.usage.mean(),
   'usgw25':(L.usage*L.MIN).groupby(L.PLAYER_ID).sum()/L.MIN.where(L.usage.notna()).groupby(L.PLAYER_ID).sum()})
L['astsh']=L.AST/L.groupby(['GAME_ID','TEAM_ID']).AST.transform('sum').replace(0,np.nan)
pf['astw25']=(L.astsh*L.MIN).groupby(L.PLAYER_ID).sum()/L.MIN.where(L.astsh.notna()).groupby(L.PLAYER_ID).sum()
pf['starts2']=f.groupby('PLAYER_ID').started.sum()
pf['start_rate25']=pf.starts25/pf.gp25
q=f.groupby('PLAYER_ID').dk.quantile(0.75); n=f.groupby('PLAYER_ID').size()
# shot-type shares 2025-26 (10+ games)
TN={'cs3':'C&S 3','pu2':'pull-up 2','lt10':'under 10 ft','wo':'wide-open','rim':'rim','paint':'short paint','mid':'mid-range','c3':'corner 3','atb3':'above-break 3','trans':'transition','ftr':'FT rate'}
MIX={'rim','paint','ftr'}
for k in list(TN)+['pu3']:
    a='FTA' if k=='ftr' else f'{k}_a'
    pf[f'sh_{k}']=L[a].groupby(L.PLAYER_ID).sum()/L.FGA.where(L[a].notna()).groupby(L.PLAYER_ID).sum()
pf['posg25']=L.groupby('PLAYER_ID').posg.last()
# ---- slate join
s=sl.merge(pf,left_on='pid',right_index=True,how='left')
s['posr']=s.posg25.fillna(s.posg)  # last-season position (as in the study), DK primary if none
s['line']=s.pid.map(q); s['n_hist']=s.pid.map(n).fillna(0)
s['new_team']=np.where(s.team25.notna()&(s.team25!=s.team),'NEW TEAM (was '+s.team25.fillna('')+')',np.where(s.gp25.isna(),'no 2025-26 games',''))
s['pre_gp']=s.pid.map(pre.pre_gp); s['pre_mpg']=s.pid.map(pre.pre_mpg); s['pre_start_rate']=s.pid.map(pre.starter_rate)
# usage tier at DK position among all 2025-26 players with 5+ games (last season)
base=pf[pf.gp25>=5]
def tier(v,pos,col):
    x=base[base.posg25==pos][col].dropna()
    if pd.isna(v) or len(x)<10: return 'n/a'
    lo,hi=x.quantile([1/3,2/3]); return 'top' if v>=hi else ('middle' if v>=lo else 'bottom')
s['usage tier (2025-26)']=[tier(v,p,'usg25') for v,p in zip(s.usg25,s.posr)]
for k in list(TN)+['pu3']:
    s[f'leg_{k}']=[(tier(v,p,f'sh_{k}')=='top') if gp>=10 else False for v,p,gp in zip(s[f'sh_{k}'],s.posr,s.gp25.fillna(0))]
# ---- team roles on CURRENT rosters from last-season numbers (v1.2 rules: minutes-weighted, 15+ mpg, 5+ games)
s['key']=s.name_key.map(norm)
s['out']=s.key.isin(out_keys); s['dtd']=s.key.isin(dtd)
roles={}
for t,x in s.groupby('team'):
    y=x[(x.gp25>=5)]
    e15=y[y.mpg25>=15]
    r={'top_usg':e15.sort_values('usgw25',ascending=False).pid.iloc[0] if len(e15) else None}
    # assist share of his team's assists in his games, minutes-weighted (v1.2); shares from last season's team
    r['top_ast']=e15.sort_values('astw25',ascending=False).pid.iloc[0] if len(e15) and e15.astw25.notna().any() else None
    x2=x.assign(pre_st=((x.pre_gp>=2)&(x.pre_start_rate>=0.5)).astype(int),starts2=x.starts2.fillna(0))
    for pg in ['PG','SG','SF','PF','C']:
        c=x2[(x2.posr==pg)&((x2.starts2>0)|(x2.pre_st==1))].sort_values(['starts2','pre_st','mpg25'],ascending=False); r[pg]=c.pid.iloc[0] if len(c) else None
    r['rotation']=set(y[y.mpg25>=20].pid); r['high_usg']=set(e15[e15.usgw25>=25].pid)
    roles[t]=r
nm=s.set_index('pid').dk_player
def absence_lines(r):
    R=roles[r.team]; outs=set(s[(s.team==r.team)&s.out].pid)-{r.pid}; Lx=[]
    def o(p): return p is not None and p!=r.pid and p in outs
    if o(R.get(r.posr)): Lx.append(f"same-position starter out: {nm[R[r.posr]]} ({lift('B4_samepos_starter_out')})")
    if o(R['top_ast']): Lx.append(f"top playmaker out: {nm[R['top_ast']]} ({lift('B2_top_ast_out')})")
    if o(R['top_usg']): Lx.append(f"top-usage teammate out: {nm[R['top_usg']]} ({lift('B1_top_usg_out')})")
    if o(R.get('C')): Lx.append(f"starting center out: {nm[R['C']]} ({lift('B3_start_c_out')})")
    if len((R['rotation']-{r.pid})&outs)>=2: Lx.append(f"2+ rotation teammates out ({lift('B5_two_rotation_out')})")
    return Lx
# ---- opponents: 2025-26 final state (as of each team's last game date in the build)
last=rk[rk.season=='2025-26'].sort_values('date').groupby('TEAM_ID').tail(1).set_index('TEAM_ID')
dr=L.sort_values('date').groupby('OPP_ID').tail(1).set_index('OPP_ID').D1_drtg_rk
dvp=L.sort_values('date').groupby(['OPP_ID','posg']).D3_dvpadj_rk.last()
rows=[]
s['tip']=s.team.map(tip)
for _,r in s.sort_values(['tip','team','salary'],ascending=[True,True,False]).iterrows():
    o=tid.get(r.opp); Lx=absence_lines(r)
    if pd.notna(r.pre_start_rate) and r.pre_gp>=2 and r.pre_start_rate>=0.5: Lx.append(f"started {r.pre_start_rate:.0%} of preseason games (confirm at lock; started {lift('A9_started') or '+12.6'})")
    d1=dr.get(o); dv=dvp.get((o,r.posr))
    if pd.notna(d1) and d1>=26: Lx.append(f"opp DRtg {int(d1)}/30 last season ({lift('D1_drtg_rk_b5')})")
    if pd.notna(dv) and dv>=21: Lx.append(f"opp DvP adj at {r.posr} {int(dv)}/30 last season ({lift('D3_dvpadj_rk_b10')})")
    for k,t in TN.items():
        c=f'{k}_vol_szn_rk'
        if r[f'leg_{k}'] and o in last.index and c in last and last.loc[o,c]>=26:
            v=P2.loc[f'E_{k}_vol_b5','diff_build'] if f'E_{k}_vol_b5' in P2.index else 0
            Lx.append(f"{'NEG ' if v<0 else ''}tiebreak: leans {t}; opp allowed {int(last.loc[o,c])}/30 last season ({'shot-mix shift' if k in MIX else 'more shots overall'}, {v:+.1f})")
    if o in last.index and last.loc[o,'pu3_vol_szn_rk']>=26: Lx.append(f"NEG opp allowed pull-up 3s {int(last.loc[o,'pu3_vol_szn_rk'])}/30 last season ({lift('E_pu3_vol_b5')})")
    tm_out=[f"{nm[p]} ({s.set_index('pid').mpg25.get(p,0):.0f} mpg last season)" for p in s[(s.team==r.team)&s.out].pid if p!=r.pid]
    rows.append({'game':f"{r.team} {'vs' if r.home==1 else '@'} {r.opp}",'tip (ET)':tip.get(r.team,''),'player':r.dk_player,'team':r.team,'opp':r.opp,'pos':r.position_dk,'dk_salary':r.salary,
      'injury report':'OUT' if r.out else ('day-to-day' if r.dtd else ''),'team change':r.new_team,
      'preseason games / mpg / start rate':(f"{int(r.pre_gp)} / {r.pre_mpg:.1f} / {r.pre_start_rate:.0%}" if pd.notna(r.pre_gp) and r.pre_gp>0 else 'no preseason'),
      'last season: games / mpg / start rate':(f"{int(r.gp25)} / {r.mpg25:.1f} / {r.start_rate25:.0%}" if pd.notna(r.gp25) else 'none'),
      'usage tier (last season, at his position)':r['usage tier (2025-26)'],
      'upside line (own top quarter, 2024-26)':round(r.line,1) if r.n_hist>=20 else 'n<20',
      'teammates OUT on injury report':', '.join(tm_out),'pregame lines (league lift, pts)':' | '.join(Lx)})
B=pd.DataFrame(rows); B.to_csv(OUT+'board.csv',index=False)
inj_src=os.path.basename(INJ); sl_src=os.path.basename(SLATE)
print('board rows',len(B),'out',int(s.out.sum()),'new team',int((s.new_team.str.startswith('NEW')).sum()),'no history',int((s.n_hist<20).sum()))
print('sources',sl_src,inj_src)
for t,r in roles.items(): print(t,{k:(nm.get(v) if not isinstance(v,set) else len(v)) for k,v in r.items()})
print('dtd',list(s[s.dtd].dk_player))
B.to_pickle('/tmp/open_board.pkl'); s.to_pickle('/tmp/open_s.pkl')
