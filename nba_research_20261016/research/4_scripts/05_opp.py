# Opponent leg as of date: volume per 100, eFG allowed, ranks; ML composite
import pandas as pd, numpy as np
f=pd.read_parquet('frame_shots.parquet'); tg=pd.read_parquet('teamgames.parquet')
TYPES={ # key: (att, made, made3, source)
 'cs3':('cs3_a','cs3_m','cs3_m','trk'),'pu3':('pu3_a','pu3_m','pu3_m','trk'),'pu2':('pu2_a','pu2_m',None,'trk'),
 'lt10':('lt10_a','lt10_m',None,'trk'),'wo':('wo_a','wo_m','wo_3m','trk'),
 'rim':('rim_a','rim_m',None,'pbp'),'paint':('paint_a','paint_m',None,'pbp'),'mid':('mid_a','mid_m',None,'pbp'),
 'c3':('c3_a','c3_m','c3_m','pbp'),'atb3':('atb3_a','atb3_m','atb3_m','pbp'),'trans':('trans_a','trans_m','trans_3m','pbp'),
 'ftr':('FTA',None,None,'box')}
ML={'ml_cs':('cs_a','cs_m','trk','l7s'),'ml_pu':('pu_a','pu_m','trk','l7s'),'ml_lt10':('lt10_a','lt10_m','trk','l7s'),
    'ml_pitp':('pitp_a','pitp_m','pbp','s'),'ml_mid':('ml_mid_a','ml_mid_m','pbp','s'),'ml_3pt':('3pt_a','3pt_m','pbp','s')}
f['one']=1
# team-game offense sums; availability flags
cols=sorted({c for v in TYPES.values() for c in v[:3] if c}|{c for v in ML.values() for c in v[:2]})
f['trk_bad']=~f.trk_ok
g=f.groupby(['season','GAME_ID','TEAM_ID','OPP_ID','date']).agg({**{c:'sum' for c in cols},'trk_bad':'max','pbp_ok':'min','POSS':'first','FGA':'sum'}).reset_index()
f['FGA_trk']=f.FGA.where(f.trk_ok,0)
fa=f.groupby(['season','GAME_ID','TEAM_ID']).FGA_trk.sum().values
share=fa/g.FGA.replace(0,np.nan).values
tcols=[c for c in cols if c.startswith(('cs','pu','lt10','wo'))]
g['trk_cover']=share
sc=np.where(share>=0.7,1/np.where(share>0,share,1),np.nan)
for c in tcols: g[c]=g[c]*sc
print('team-games with tracking cover <0.7:',(share<0.7).sum(),'scaled (cover<1):',(share<1).sum())
g.loc[~g.pbp_ok.astype(bool),[c for c in cols if c.split('_')[0] in('rim','paint','mid','c3','atb3','trans','pitp','ml','3pt')]]=np.nan
print('team-games',len(g),'trk missing',g.cs3_a.isna().sum(),'pbp missing',g.rim_a.isna().sum())
g=g.sort_values(['TEAM_ID','date'])
# offense prior rates for adjustment
def prior_rate(df,keycol,num,den):
    df=df.sort_values('date'); ok=df[num].notna()
    cn=df[num].where(ok,0).groupby([df.season,df[keycol]]).cumsum()-df[num].where(ok,0)
    cd=df[den].where(ok,0).groupby([df.season,df[keycol]]).cumsum()-df[den].where(ok,0)
    cg=ok.astype(int).groupby([df.season,df[keycol]]).cumsum()-ok.astype(int)
    return cn,cd,cg
out=[]
dates=f[['season','date']].drop_duplicates()
teams=g.TEAM_ID.unique()
grid=dates.merge(pd.DataFrame({'TEAM_ID':teams}),how='cross')  # defense team x date
res=grid.copy()
d=g.copy()  # rows = offense team's game; defense = OPP_ID
d['def']=d.OPP_ID
def asof(d,val_cols,win=None):
    # for each defense team and date D: sums over its games with date < D (season-to-date or last win available)
    rows=[]
    for (s,t),x in d.groupby(['season','def']):
        x=x.sort_values('date')
        dd=grid[(grid.season==s)&(grid.TEAM_ID==t)][['season','date','TEAM_ID']].sort_values('date')
        for vc in val_cols: pass
        rows.append((s,t,x,dd))
    return rows
def build(d,spec):
    # spec: list of (name, num, den, availcol)
    outs=[]
    for (s,t),x in d.groupby(['season','def']):
        x=x.sort_values('date').reset_index(drop=True)
        dd=grid[(grid.season==s)&(grid.TEAM_ID==t)][['season','date','TEAM_ID']].sort_values('date').reset_index(drop=True)
        r=dd.copy()
        idx=np.searchsorted(x.date.values,dd.date.values,side='left')  # number of games strictly before D
        r['n_games']=idx
        for name,num,den,av in spec:
            ok=x[av].notna().values
            nv=np.where(ok,x[num].fillna(0).values,0); dv=np.where(ok,x[den].fillna(0).values,0)
            cn=np.concatenate([[0],np.cumsum(nv)]); cd=np.concatenate([[0],np.cumsum(dv)]); cg=np.concatenate([[0],np.cumsum(ok)])
            r[f'{name}_szn']=np.where(cd[idx]>0,cn[idx]/np.where(cd[idx]>0,cd[idx],1),np.nan)
            r[f'{name}_szn_n']=cg[idx]
            # last 10 / last 7 available games
            okpos=np.where(ok)[0]
            for W in (10,7):
                vals=[];
                for i in idx:
                    pos=okpos[okpos<i][-W:]
                    vals.append(nv[pos].sum()/dv[pos].sum() if len(pos)==W and dv[pos].sum()>0 else np.nan)
                r[f'{name}_l{W}']=vals
        outs.append(r)
    return pd.concat(outs)
spec=[]
for k,(a,m,m3,src) in TYPES.items():
    spec.append((f'{k}_vol',a,'POSS',a))
    if m is not None:
        d[f'{k}_pts']=d[m]+(0.5*d[m3] if m3 else 0)
        spec.append((f'{k}_eff',f'{k}_pts',a,a))
for k,(a,m,src,w) in ML.items():
    spec.append((f'{k}_fgpct',m,a,a)); spec.append((f'{k}_fgapg',a,'one',a))
d['one']=1
# adjusted: offense game rate minus offense prior season rate
adj=[]
d=d.sort_values('date')
for k,(a,m,m3,src) in TYPES.items():
    d[f'{k}_rate']=d[a]/d.POSS*100
    cn,cd,cg=prior_rate(d,'TEAM_ID',a,'POSS'); pr=cn/cd.replace(0,np.nan)*100
    d[f'{k}_voladj_d']=np.where(cg>=5,d[f'{k}_rate']-pr,np.nan); d[f'{k}_voladj_one']=np.where(cg>=5,1.0,np.nan)
    spec.append((f'{k}_voladj',f'{k}_voladj_d',f'{k}_voladj_one',f'{k}_voladj_d'))
    if m is not None:
        cn,cd,cg=prior_rate(d,'TEAM_ID',f'{k}_pts',a); pe=cn/cd.replace(0,np.nan)
        d[f'{k}_effadj_d']=np.where((cg>=5)&(d[a]>0),d[f'{k}_pts']/d[a].replace(0,np.nan)-pe,np.nan); d[f'{k}_effadj_one']=np.where(~np.isnan(d[f'{k}_effadj_d']),1.0,np.nan)
        spec.append((f'{k}_effadj',f'{k}_effadj_d',f'{k}_effadj_one',f'{k}_effadj_d'))
st=build(d,spec)
# ranks: 1 = stingiest (lowest), 30 = most allowed; only teams with >=10 games
st['elig']=st.n_games>=10
rk=st[['season','date','TEAM_ID','n_games']].copy()
for k in TYPES:
    for meas in ['vol','eff','voladj','effadj']:
        for win in ['szn','l10']:
            c=f'{k}_{meas}_{win}'
            if c not in st: continue
            rk[f'{k}_{meas}_{win}_rk']=st[c].groupby([st.season,st.date]).rank(method='max').where(st.elig)
for k,(a,m,src,w) in ML.items():
    parts=[]
    for c in ([f'{k}_fgpct_l7',f'{k}_fgapg_l7'] if w=='l7s' else [])+[f'{k}_fgpct_szn',f'{k}_fgapg_szn']:
        parts.append(st[c].groupby([st.season,st.date]).rank(method='max'))
    comp=pd.concat(parts,axis=1).mean(axis=1,skipna=False)
    rk[f'{k}_rk']=comp.groupby([st.season,st.date]).rank(method='max').where(st.elig)
st.to_parquet('opp_state.parquet'); rk.to_parquet('opp_ranks.parquet')
print(rk.shape); print(rk[rk.n_games>=10].filter(like='_rk').notna().mean().round(3).sort_values().head(10).to_dict())
