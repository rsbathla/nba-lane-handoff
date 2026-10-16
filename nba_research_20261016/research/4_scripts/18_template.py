import pandas as pd, numpy as np, unicodedata, re, sys
D=pd.Timestamp(sys.argv[1] if len(sys.argv)>1 else '2026-03-18'); FEAT=sys.argv[2] if len(sys.argv)>2 else '0022501007'
OUT=f'/mnt/project-files/nba/p3_live/template_{D.date()}/'
f=pd.read_parquet('frame_abcd.parquet'); st=pd.read_parquet('opp_state.parquet'); rk=pd.read_parquet('opp_ranks.parquet'); tg=pd.read_parquet('teamgames.parquet')
P2=pd.read_csv('p2_pooled.csv').set_index('cond')  # build window = before 2026-01-15 (valid evidence for a March date)
ab=tg.drop_duplicates('TEAM_ID').set_index('TEAM_ID').TEAM_ABBREVIATION
names=f.drop_duplicates('PLAYER_ID').set_index('PLAYER_ID').PLAYER_NAME
s=f[f.date==D].copy()
# upside line from earlier games only
prior=f[f.date<D]; ps=prior[prior.season==s.season.iloc[0]]; g=ps.groupby(['TEAM_ID','PLAYER_ID']).MIN.agg(['mean','size']); mpg=g[g['size']>=5]['mean'].to_dict(); q=prior.groupby('PLAYER_ID').dk.quantile(0.75); n=prior.groupby('PLAYER_ID').size()
s['line']=s.PLAYER_ID.map(q); s['n_prior']=s.PLAYER_ID.map(n).fillna(0)
# projections (pregame export)
def norm(x): x=unicodedata.normalize('NFKD',str(x)).encode('ascii','ignore').decode().lower(); x=re.sub(r'[^a-z ]','',x); x=re.sub(r'\b(jr|sr|ii|iii|iv)\b','',x); return ' '.join(x.split())
pj=pd.read_csv('/home/claude/nba/raw/projections/NBA DFS Projections - 2026-03-18T180646.523.csv'); pj['k']=pj.Player.map(norm)
pj=pj.drop_duplicates('k').set_index('k')
s['proj_min']=s.PLAYER_NAME.map(norm).map(pj.Minutes)
lift=lambda c: (f"{P2.loc[c,'diff_build']:+.1f}" if c in P2.index else '')
TN={'cs3':'C&S 3','pu3':'pull-up 3','pu2':'pull-up 2','lt10':'under 10 ft','wo':'wide-open','rim':'rim','paint':'short paint','mid':'mid-range','c3':'corner 3','atb3':'above-break 3','trans':'transition','ftr':'FT rate'}
def lines(r):
    L=[]
    out=[ f"{names.get(p,str(p))} ({mpg.get((r.TEAM_ID,p),0):.0f} mpg)" for p in list(r.absent) if p!=r.PLAYER_ID and mpg.get((r.TEAM_ID,p),0)>=15] if r.absent is not None else []
    for c,lab in [('B4_samepos_starter_out','same-position starter out'),('B2_top_ast_out','top playmaker out'),('B1_top_usg_out','top-usage teammate out'),('B3_start_c_out','starting center out'),('B5_two_rotation_out','2+ rotation teammates out')]:
        if r[c]==1: L.append(f"{lab} ({lift(c)})")
    if r.A9_started==1: L.append(f"starting (lock-time, {lift('A9_started') or '+12.6'})")
    if r.A4_min_l10_t=='top': L.append(f"prior-10 minutes top third ({lift('A4_min_l10_t=top')})")
    if r.A4_min_l10_t=='bottom': L.append(f"NEG prior-10 minutes bottom third ({lift('A4_min_l10_t=bottom')})")
    if r.D1_drtg_rk>=26: L.append(f"opp DRtg {int(r.D1_drtg_rk)}/30 ({lift('D1_drtg_rk_b5')})")
    if r.D3_dvpadj_rk>=21: L.append(f"opp DvP adj at {r.posg} {int(r.D3_dvpadj_rk)}/30 ({lift('D3_dvpadj_rk_b10')})")
    # v2 (approved 2026-10-15 after VOLUME_ALL_SPLITS): raw volume allowed and Matchup Lab only; efficiency splits dropped
    MIX={'rim','paint','ftr'}
    for k,t in TN.items():
        if k=='pu3' or r.get(f'leg_{k}')!=1: continue
        c=f'{k}_vol_szn_rk'
        if c in r and r[c]>=26:
            v=P2.loc[f'E_{k}_vol_b5','diff_build'] if f'E_{k}_vol_b5' in P2.index else 0
            kind='shot-mix shift' if k in MIX else 'more shots overall'
            L.append(f"tiebreak: leans {t}; opp allows {int(r[c])}/30 ({kind}, {v:+.1f})")
    for k,t in [('ml_cs','C&S'),('ml_pu','pull-up'),('ml_lt10','under 10 ft'),('ml_pitp','paint'),('ml_mid','mid'),('ml_3pt','3PT')]:
        c=f'{k}_rk'
        if r.get(f'leg_{k}')==1 and c in r and r[c]>=26:
            L.append(f"tiebreak: Matchup Lab {t} {int(r[c])}/30 ({lift(f'E_{k}_b5')})")
    if r.get('pu3_vol_szn_rk',0)>=26: L.append(f"NEG opp allows pull-up 3s {int(r.pu3_vol_szn_rk)}/30 ({lift('E_pu3_vol_b5')})")
    return L, out
rows=[]
for _,r in s.sort_values(['TEAM_ABBREVIATION','sal_dk'],ascending=[True,False]).iterrows():
    L,out=lines(r)
    rows.append({'game':r.MATCHUP,'player':r.PLAYER_NAME,'team':r.TEAM_ABBREVIATION,'opp':r.OPP,'pos':r.posg,'dk_salary':r.sal_dk,'proj_min (18:06 export)':r.proj_min,
      'started (lock)':'Y' if r.A9_started==1 else 'N','usage tier':r.A1_usg_szn_t,'prior-10 min tier':r.A4_min_l10_t,'upside line (own top quarter, earlier games)':round(r.line,1) if r.n_prior>=20 else 'n<20',
      'rotation teammates out (played 0 min; 15+ mpg)':', '.join(sorted(out)) if out else '','pregame lines (league lift, pts)':' | '.join(L),
      'AFTER THE FACT: minutes':round(r.MIN,1),'AFTER THE FACT: DK':r.dk,'AFTER THE FACT: upside':('yes' if r.dk>=r.line else 'no') if r.n_prior>=20 else ''})
B=pd.DataFrame(rows); B.to_csv(OUT+'board.csv',index=False)
print('board rows',len(B))
# hit rates by line presence, after the fact (descriptive only)
B['has_absence']=B['pregame lines (league lift, pts)'].str.contains(r'out \(')
x=B[B['AFTER THE FACT: upside']!='']
print(x.groupby('has_absence')['AFTER THE FACT: upside'].apply(lambda z:(z=='yes').mean()).round(3).to_dict(), x.groupby('has_absence').size().to_dict())
B.to_pickle('/tmp/board.pkl')
