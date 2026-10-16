# Per player-game shot-type attempts/makes from tracking and play-by-play
import pandas as pd, numpy as np, glob, json, gzip, re
R='/home/claude/nba/raw/'; A=R+'dfs/nba/analytics/data/research_v2/'
f=pd.read_parquet('frame.parquet')
# ---- tracking
t=[pd.read_csv(A+'tracking_corrected_2024-25.csv'),pd.read_csv(A+'tracking_corrected_2025-26.csv')]
bf=[]
for fn in glob.glob(R+'intake/nba_shot_backfill_20261013/2024-25/*.json.gz'):
    dt,tag=re.search(r'(\d{4}-\d\d-\d\d)_(\w+)\.json',fn).groups()
    d=json.load(gzip.open(fn))['resultSets'][0]; x=pd.DataFrame(d['rowSet'],columns=d['headers'])
    bf.append(pd.DataFrame({'date':dt,'tag':tag,'nba_pid':x.PLAYER_ID,'fgm':x.FGM,'fga':x.FGA,'fg3m':x.FG3M,'fg3a':x.FG3A}))
bf=pd.concat(bf); t=pd.concat(t)
t=pd.concat([t,bf[pd.to_datetime(bf.date)>pd.to_datetime(t[t.date<'2025-07-01'].date.max())]])
t['date']=pd.to_datetime(t.date)
print('tracking rows',len(t), t.groupby(t.date.dt.year).size().to_dict())
w=t.pivot_table(index=['nba_pid','date'],columns='tag',values=['fga','fgm','fg3a','fg3m'],aggfunc='sum')
w.columns=[f'{tag}_{v}' for v,tag in w.columns]; w=w.reset_index()
tr_dates=set(t.date.unique())
f=f.merge(w,left_on=['PLAYER_ID','date'],right_on=['nba_pid','date'],how='left')
# date covered by tracking => missing row means 0 attempts
cov=f.date.isin(tr_dates)
tc=[c for c in w.columns if c[:3] in('cs_','pu_','lt1','wo_','vti')]
for c in tc: f.loc[cov&f[c].isna(),c]=0
# quarantine
for q in ['tracking_quarantine_2024.csv','tracking_quarantine_2025.csv']:
    qq=pd.read_csv(A+q); qq['gid']=qq.gid.astype(str).str.zfill(10)
    bad=f.set_index(['GAME_ID','PLAYER_ID']).index.isin(pd.MultiIndex.from_arrays([qq.gid,qq.pid]))
    f.loc[bad,tc]=np.nan
f['trk_ok']=f['cs_fga'].notna()
# tracking sanity: types cannot exceed FGA
print('tracking ok share',f.trk_ok.mean().round(4), 'cs>FGA',(f.cs_fga>f.FGA).sum(), 'pu>FGA',(f.pu_fga>f.FGA).sum())
f['cs3_a']=f.cs_fg3a; f['cs3_m']=f.cs_fg3m
f['pu3_a']=f.pu_fg3a; f['pu3_m']=f.pu_fg3m
f['pu2_a']=f.pu_fga-f.pu_fg3a; f['pu2_m']=f.pu_fgm-f.pu_fg3m
f['lt10_a']=f.lt10_fga; f['lt10_m']=f.lt10_fgm
f['wo_a']=f.wo_fga; f['wo_m']=f.wo_fgm; f['wo_3m']=f.wo_fg3m
f['cs_a']=f.cs_fga; f['cs_m']=f.cs_fgm; f['pu_a']=f.pu_fga; f['pu_m']=f.pu_fgm
# ---- play-by-play
def secs(x):
    p=x.fillna('0:00:00').str.split(':',expand=True).astype(float); return p[0]*3600+p[1]*60+p[2]
rows=[]
for season,folder in [('2024-25','pbp_2425'),('2025-26','pbp_2526')]:
    for fn in sorted(glob.glob(R+f'bdb/{folder}/[[]20*')):
        gid=re.search(r'\](\d+)-',fn.replace(']-',']')).group(1) if False else re.search(r'-(\d{10})-',fn).group(1)
        if not gid.startswith('002'): continue
        d=pd.read_csv(fn,dtype=str,low_memory=False).reset_index(drop=True)
        d['el']=secs(d.elapsed)
        teams=[x for x in d.loc[d.event_type=='shot','team'].dropna().unique()]
        gteam=[None]*len(d); gtime=[np.nan]*len(d)
        per=None; lt=None; gt=np.nan; miss_team=None
        for i,(p_,et,tm,res,el) in enumerate(zip(d.period,d.event_type,d.team,d.result,d.el)):
            if p_!=per: per=p_; lt=None; gt=np.nan; miss_team=None
            if et=='shot':
                gteam[i]=lt; gtime[i]=gt
                miss_team = tm if res=='missed' else None
            elif et=='free throw':
                miss_team = tm if res=='missed' else None
            elif et=='rebound':
                if miss_team is not None and isinstance(tm,str) and tm!=miss_team: lt,gt=tm,el
                miss_team=None
            elif et=='turnover' and isinstance(tm,str):
                o=[x for x in teams if x!=tm]
                if o: lt,gt=o[0],el
                miss_team=None
        d['gteam']=gteam; d['gtime']=gtime
        s=d[d.event_type=='shot'].copy(); s['gid']=gid; s['season']=season
        keep=['gid','season','date','team','player','result','type','shot_distance','original_x','original_y','description','el','gteam','gtime','period']
        for q in ['qualifiers1','qualifiers2','qualifiers3','qualifiers4','area_detail']:
            if q in s: keep.append(q)
        rows.append(s[keep])
    print(season,'pbp parsed',len(rows))
p=pd.concat(rows,ignore_index=True)
p.to_parquet('pbp_shots_raw.parquet'); f.to_parquet('frame_trk.parquet')
print('shots',len(p), p.groupby('season').size().to_dict())
