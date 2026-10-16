# Player-game frame: NBA.com box + DK points + BDB DFS position/usage/starter
import pandas as pd, json, gzip, numpy as np
R='/home/claude/nba/raw/'
def rs(f):
    d=json.load(gzip.open(f)); r=d['resultSets'][0]; return pd.DataFrame(r['rowSet'],columns=r['headers'])
pl=[];tm=[]
for s in ['2024-25','2025-26']:
    p=rs(f'{R}intake/nba_player_logs_20261013/{s}/playergamelogs_Base.json.gz'); p['season']=s; pl.append(p)
    t=rs(f'{R}intake/nba_official_20261013/{s}/teamgamelogs_Advanced.json.gz'); t['season']=s; tm.append(t)
pl=pd.concat(pl); tm=pd.concat(tm)
pl=pl[pl.GAME_ID.str.startswith('002')&(pl.MIN>0)].copy()
tm=tm[tm.GAME_ID.str.startswith('002')].copy()
pl['date']=pd.to_datetime(pl.GAME_DATE).dt.normalize(); tm['date']=pd.to_datetime(tm.GAME_DATE).dt.normalize()
# opponent
opp=tm[['GAME_ID','TEAM_ID','TEAM_ABBREVIATION','POSS','PACE']].rename(columns={'TEAM_ID':'OPP_ID','TEAM_ABBREVIATION':'OPP','POSS':'OPP_POSS','PACE':'OPP_PACE'})
tm2=tm.merge(opp,on='GAME_ID'); tm2=tm2[tm2.TEAM_ID!=tm2.OPP_ID]
pl=pl.merge(tm2[['GAME_ID','TEAM_ID','OPP_ID','OPP','POSS','OPP_POSS']],on=['GAME_ID','TEAM_ID'],how='left')
pl['home']=pl.MATCHUP.str.contains('vs.')
dd=((pl[['PTS','REB','AST','STL','BLK']]>=10).sum(axis=1))
pl['dk']=pl.PTS+0.5*pl.FG3M+1.25*pl.REB+1.5*pl.AST+2*pl.STL+2*pl.BLK-0.5*pl.TOV+np.where(dd>=2,1.5,0)+np.where(dd>=3,3,0)
# BDB DFS feed
def dfs(f):
    d=pd.read_excel(f,sheet_name=0,header=None,skiprows=3)
    d=d.iloc[:,:21]; d.columns=['dataset','GAME_ID','date','PLAYER_ID','player','team','opp','starter','venue','min','usage','rest','pos_dk','pos_fd','pos_yh','sal_dk','sal_fd','sal_yh','dk_bdb','fd_bdb','yh_bdb']
    d=d[d.GAME_ID.notna()]; d['GAME_ID']=d.GAME_ID.astype(str).str.zfill(10); d['PLAYER_ID']=pd.to_numeric(d.PLAYER_ID,errors='coerce'); return d
b=pd.concat([dfs(R+'bdb/06-08-2025-nba-season-dfs-feed.xlsx'),dfs(R+'bdb/feeds_2526/06-05-2026-nba-season-dfs-feed.xlsx')])
b=b[b.GAME_ID.str.startswith('002')].drop_duplicates(['GAME_ID','PLAYER_ID'])
print('bdb dfs rows',len(b), b.dataset.value_counts().to_dict())
pl=pl.merge(b[['GAME_ID','PLAYER_ID','starter','usage','rest','pos_dk','sal_dk','dk_bdb']],on=['GAME_ID','PLAYER_ID'],how='left')
pl['dk_bdb']=pd.to_numeric(pl.dk_bdb,errors='coerce'); pl['usage']=pd.to_numeric(pl.usage,errors='coerce'); pl['sal_dk']=pd.to_numeric(pl.sal_dk,errors='coerce')
pl['pos1']=pl.pos_dk.astype(str).str.split('/').str[0].where(pl.pos_dk.notna())
_pp=pl[pl.pos1.isin(['PG','SG','SF','PF','C'])].sort_values('date')
def _mode(x):
    vc=x.value_counts(); top=vc[vc==vc.max()].index
    return [p for p in x[::-1] if p in top][0]  # ties: position in his most recent game
pg=_pp.groupby('PLAYER_ID').pos1.agg(_mode)
pl['posg']=pl.PLAYER_ID.map(pg)
m=pl.dk_bdb.notna(); diff=(pl.dk-pl.dk_bdb).abs()
print('player-games',len(pl), pl.groupby('season').size().to_dict(), 'bdb matched',m.sum(), 'dk exact(<=0.01)',(diff[m]<=0.01).sum(), 'mismatch',(diff[m]>0.01).sum())
pl.loc[m&(diff>0.01),['season','GAME_ID','PLAYER_NAME','dk','dk_bdb','PTS','REB','AST']].to_csv('dk_mismatches.csv',index=False)
print('missing posg',pl.posg.isna().sum(), 'missing usage',pl.usage.isna().sum())
pl['rest']=pl.rest.astype(str); pl['starter']=pl.starter.astype(str); pl['pos_dk']=pl.pos_dk.astype(str)
pl.to_parquet('frame.parquet'); tm2.to_parquet('teamgames.parquet')
