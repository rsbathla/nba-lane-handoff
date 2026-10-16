import pandas as pd, numpy as np, unicodedata, re
p=pd.read_parquet('pbp_shots_raw.parquet'); f=pd.read_parquet('frame_trk.parquet')
for c in ['shot_distance','original_x','original_y','el','gtime']: p[c]=pd.to_numeric(p[c],errors='coerce')
def norm(s): s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower(); s=re.sub(r'[^a-z ]','',s); s=re.sub(r'\b(jr|sr|ii|iii|iv)\b','',s); return ' '.join(s.split())
# player ids
p['pid']=np.nan
m=p.season=='2025-26'; p.loc[m,'pid']=pd.to_numeric(p.loc[m,'player'].str.split('/').str[0],errors='coerce')
p['pname']=np.where(m,p.player.str.split('/').str[1],p.player)
roster=f[['GAME_ID','PLAYER_ID','PLAYER_NAME']].copy(); roster['k']=roster.PLAYER_NAME.map(norm)
p['k']=p.pname.map(norm); p['gid']=p.gid.str.zfill(10)
mm=p[~m].merge(roster,left_on=['gid','k'],right_on=['GAME_ID','k'],how='left')
p.loc[~m,'pid']=mm.PLAYER_ID.values
print('unmatched shots by season', p[p.pid.isna()].groupby('season').size().to_dict())
print(p[p.pid.isna()&~m].pname.value_counts().head(15).to_dict())
p.to_parquet('pbp_shots_ids.parquet')
alias={'Alexandre Sarr':1642259,'Carlton Carrington':1642267,'Cui Yongxi':1642385}
miss=p.pid.isna(); p.loc[miss,'pid']=p.loc[miss,'pname'].map(alias)
print('still unmatched',p.pid.isna().sum())
# classify
is3=p.description.str.contains('3PT',case=False,na=False)|p.type.str.contains('3pt',case=False,na=False)
p['is3']=is3; p['made']=p.result=='made'
x=p.original_x; y=p.original_y
m26=p.season=='2025-26'
# basket-relative coordinates in feet: depth (along court from basket), lateral
depth=np.where(m26, np.where(x<50, x*0.94-5.25, (100-x)*0.94-5.25), y/10)
lat=np.where(m26, (y-50)*0.5, x/10)
p['depth']=depth; p['lat']=lat
d=np.where(m26,np.floor(p.shot_distance+0.5),p.shot_distance)
p['t_rim']=(~is3)&(d<=3); p['t_paint']=(~is3)&(d>3)&(d<=10); p['t_mid']=(~is3)&(d>10)
p['t_c3']=is3&(p.depth<=9.0); p['t_atb3']=is3&~p.t_c3
p['t_pitp']=(~is3)&(np.abs(p.lat)<=8)&(p.depth<=19-5.25)
p['t_ml_mid']=(~is3)&~p.t_pitp; p['t_3pt']=is3
p['t_trans']=(p.gteam==p.team)&((p.el-p.gtime)<=6)
# checks
for s,g in p.groupby('season'):
    print(s,'3PA share',g.is3.mean().round(3),'corner share of 3PA',g[g.is3].t_c3.mean().round(3),'rim',g.t_rim.mean().round(3),'pitp',g.t_pitp.mean().round(3),'trans',g.t_trans.mean().round(3))
g=p[m26]; fb=g[['qualifiers1','qualifiers2','qualifiers3','qualifiers4']].eq('fastbreak').any(axis=1)
print('2025-26 transition proxy vs fastbreak qualifier: proxy rate',g.t_trans.mean().round(3),'fb rate',fb.mean().round(3),'agreement',(g.t_trans==fb).mean().round(3),'P(fb|proxy)',fb[g.t_trans].mean().round(3),'P(proxy|fb)',g.t_trans[fb].mean().round(3))
pitp_q=g[['qualifiers1','qualifiers2','qualifiers3']].eq('pointsinthepaint').any(axis=1)
print('made 2s: pitp geometric vs qualifier agreement',(g[g.made&~g.is3].t_pitp==pitp_q[g.made&~g.is3]).mean().round(3))
p.to_parquet('pbp_shots_typed.parquet')
