# Per-game summary for the opening-night board (last season's team identity, roster changes, injury report, lines on)
import pandas as pd, numpy as np, sys
D=sys.argv[1]; OUT=f'/mnt/project-files/nba/p3_live/{D}/'
B=pd.read_pickle('/tmp/open_board.pkl'); tg=pd.read_parquet('teamgames.parquet'); rk=pd.read_parquet('opp_ranks.parquet')
t=tg[tg.season=='2025-26'].groupby('TEAM_ABBREVIATION').agg(off=('OFF_RATING','mean'),dfn=('DEF_RATING','mean'),pace=('PACE','mean'))
t['off_rk']=t.off.rank(ascending=False,method='min').astype(int); t['def_rk']=t.dfn.rank(method='max').astype(int); t['pace_rk']=t.pace.rank(ascending=False,method='min').astype(int)
md=[f"# Opening night {D}: game summaries\n\nAll team and player numbers are **last season (2025-26)**. Rosters changed over the summer, so a team's defense rank describes last year's roster. Ranks are of 30: offense and pace 1 = best/fastest, defense 30 = most generous. Absences come from the injury report (status Out), not the 0-minute rule.\n"]
for gname,x in B.groupby('tip (ET)',sort=True):
    for gm,y in x.groupby('game'):
        if 'vs' not in gm: continue
        h,a=y.team.iloc[0],y.opp.iloc[0]
        md.append(f"## {a} @ {h}, {gname} ET\n")
        md.append(f"| | {a} | {h} |\n|---|---|---|")
        md.append(f"| Offensive rating rank, last season | {t.loc[a,'off_rk']} | {t.loc[h,'off_rk']} |")
        md.append(f"| Defensive rating rank, last season | {t.loc[a,'def_rk']} | {t.loc[h,'def_rk']} |")
        md.append(f"| Pace rank, last season | {t.loc[a,'pace_rk']} | {t.loc[h,'pace_rk']} |")
        for tm in [a,h]:
            z=B[B.team==tm]
            nt=z[z['team change'].str.startswith('NEW')]; outs=z[z['injury report']=='OUT']
            md.append(f"\n**{tm}**: new this season: {', '.join(nt.player+' ('+nt['team change'].str.replace('NEW TEAM (','').str.rstrip(')')+')') or 'none on the DK slate'}. Out on the injury report: {', '.join(outs.player) or 'none'}.")
            on=z[z['pregame lines (league lift, pts)']!='']
            for _,r in on.iterrows():
                md.append(f"- {r.player} (${r.dk_salary:,}): {r['pregame lines (league lift, pts)']}")
        md.append('')
open(OUT+'GAMES.md','w').write('\n'.join(md)); print('\n'.join(md)[:3000])
