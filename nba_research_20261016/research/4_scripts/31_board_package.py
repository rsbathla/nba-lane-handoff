# Package the team-board data (same data the Claude Design canvas loads) as CSVs + JSON + README in one zip.
# Usage: 31_board_package.py <full json from 29 FULL_JSON> <design json from 30> <out dir>
import json,csv,sys,os,zipfile
F=json.load(open(sys.argv[1])); S=json.load(open(sys.argv[2])); O=sys.argv[3]; os.makedirs(O,exist_ok=True)
T=F['teams']; order=[t['code'] for t in S['teams']]
def w(name,cols,rows):
    with open(os.path.join(O,name),'w',newline='',encoding='utf-8') as f:
        c=csv.writer(f); c.writerow(cols); c.writerows(rows)
    return len(rows)
n={}
n['teams.csv']=w('teams.csv',['team','name','opening_night_game','players_in_preseason','posts','the_read','preview','availability'],
  [[t,T[t]['name'],T[t].get('game') or '',sum(1 for p in T[t]['players'] if p.get('gp')),len(st['posts']),' | '.join(T[t].get('notes',[])),st['preview'],st['availability']] for t,st in zip(order,S['teams'])])
n['players.csv']=w('players.csv',['team','player','nba_person_id','named_in_post','pre_gp','pre_mpg','pre_starts','pre_box_games','pre_usg','gp_2025_26','mpg_2025_26','start_pct_2025_26','usg_2025_26'],
  [[t,p['name'],p['pid'],int(bool(p.get('named'))),p.get('gp') or 0,p.get('mpg'),p.get('starts'),p.get('box'),p.get('usg'),p.get('gp25'),p.get('mpg25'),p.get('st25'),p.get('usg25')] for t in order for p in T[t]['players']])
n['player_games.csv']=w('player_games.csv',['team','player','nba_person_id','date','opp','minutes','started','usg'],
  [[t,p['name'],p['pid'],'2026-'+g['d'],g['opp'],g.get('min'),int(bool(g.get('s'))),g.get('u')] for t in order for p in T[t]['players'] for g in p.get('games',[])])
n['posts.csv']=w('posts.csv',['team','date_utc','kind','author','handle','topic','source','url','text','quoted_text'],
  [[st['code'],i['date'],i['k'],i['author'],i.get('handle',''),i.get('topic',''),i['src'],i.get('url',''),i['text'],i.get('quoted','')] for st in S['teams'] for i in st['posts']])
json.dump(S,open(os.path.join(O,'nba_teams.json'),'w'),ensure_ascii=False,indent=1)
open(os.path.join(O,'README.md'),'w').write(f"""# NBA preseason team board data

Built {F['built']}. Preseason box scores run through {F['box_through']}; X posts through 2026-10-15. This is the same data as the team board and the Claude Design canvas.

## Files
- **teams.csv**: 30 rows, opening-night teams first. Includes the opening-night game, the read (notes joined by " | "), the preview and availability.
- **players.csv**: {n['players.csv']} rows, one per player per team. Players are included if they played in preseason, averaged 12+ minutes in 2025-26, or are named in a post. Fields: preseason games, MPG, starts out of games with a box score, usage %, and the same for 2025-26 (start % instead of starts).
- **player_games.csv**: {n['player_games.csv']} rows, one per player per preseason game: minutes, started (1/0), usage %.
- **posts.csv**: {n['posts.csv']} rows. kind = analyst / beat (lineups and beat) / coach (coach quotes). source = Read in your Chrome, Your bookmark, Web search, Quote relay, or Codex summary. Multi-team analyst notes are cut to each team's section.
- **nba_teams.json**: the nested file the canvas loads (display-ready strings).

## Notes
- Usage is the box formula 100·(FGA+0.44·FTA+TOV)·(team MIN/5)/(MIN·team possessions), minutes-weighted across games.
- Post dates are UTC, so an evening ET post shows the next day.
- Posts are opinions and reports, not confirmed roles. Thunder Dan, Adam Stock and Besbris are only partly covered because X stops loading author searches after about 9 posts.
- Descriptive counts only; nothing here is a projection.
""")
z=os.path.join(os.path.dirname(O.rstrip('/')),'nba_board_data_20261016.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(os.listdir(O)): zf.write(os.path.join(O,f),'nba_board_data_20261016/'+f)
print(n,z,os.path.getsize(z))
