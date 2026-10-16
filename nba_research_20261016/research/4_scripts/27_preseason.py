# Preseason 2026 player table: games / minutes from the latest NBA.com leaguegamelog (P, preseason), starts from boxscoreadvancedv3
# (a non-empty position = starter; minutes from the boxscore, decimal), union of Codex's 10-13 pull and Ramneik's daily pipeline captures. Usage: 27_preseason.py <leaguegamelog json> <out csv> <adv json dirs...>
import json,glob,sys,pandas as pd
LOG,OUT=sys.argv[1],sys.argv[2]; dirs=sys.argv[3:]
d=json.load(open(LOG))['resultSets'][0]; g=pd.DataFrame(d['rowSet'],columns=d['headers'])
g=g[g.GAME_ID.str.startswith('001')]
st={}; mins={}
for dd in dirs:
    for fn in glob.glob(dd+'/*.json'):
        if '00126' not in fn: continue
        b=json.load(open(fn)).get('boxScoreAdvanced')
        if not b: continue
        for side in ['homeTeam','awayTeam']:
            for p in b[side]['players']:
                st[(b['gameId'],p['personId'])]=int(bool(p.get('position')))
                m=p['statistics'].get('minutes') or '0:00'; mm,ss=(m.split(':')+['0'])[:2]; mins[(b['gameId'],p['personId'])]=float(mm)+float(ss)/60
g['MIN_LOG']=g.MIN; g['MIN']=[mins.get((a,b),m) for a,b,m in zip(g.GAME_ID,g.PLAYER_ID,g.MIN_LOG)]
print('negative log minutes',g[g.MIN_LOG<0][['PLAYER_NAME','GAME_ID','MIN_LOG','MIN']].to_dict('records'))
g.loc[g.MIN<0,'MIN']=float('nan')  # NBA.com log glitch (Mark Williams 0012600054 = -4)
g['start']=[st.get((a,b)) for a,b in zip(g.GAME_ID,g.PLAYER_ID)]
cov=g.drop_duplicates('GAME_ID'); print('log games',len(cov),'with boxscore',int(cov.start.notna().sum()) if False else g.groupby('GAME_ID').start.apply(lambda z:z.notna().any()).sum(),'last date',g.GAME_DATE.max())
t=g.groupby('PLAYER_ID').agg(pre_gp=('GAME_ID','size'),pre_mpg=('MIN','mean'),pre_starts=('start','sum'),pre_box=('start','count'),team=('TEAM_ABBREVIATION','last'),name=('PLAYER_NAME','last'))
t['starter_rate']=t.pre_starts/t.pre_box.where(t.pre_box>0)
t.index.name='pid'; t.reset_index().to_csv(OUT,index=False); print(len(t))
