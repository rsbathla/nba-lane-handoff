import pandas as pd, numpy as np
f=pd.read_parquet('frame_e.parquet'); f=f[f.qual].copy(); tg=pd.read_parquet('teamgames.parquet')
# opponent DRtg season-to-date as of date (points allowed per 100 poss), rank 30 = worst
tg=tg.sort_values('date'); tg['pa']=tg.DEF_RATING*tg.POSS/100
rows=[]
for (s,t),x in tg.groupby(['season','TEAM_ID']):
    x=x.sort_values('date'); cpa=np.concatenate([[0],x.pa.cumsum()]); cp=np.concatenate([[0],x.POSS.cumsum()])
    ds=f[f.season==s].date.drop_duplicates().sort_values().values
    i=np.searchsorted(x.date.values,ds,side='left')
    rows.append(pd.DataFrame({'season':s,'date':ds,'OPP_ID':t,'n':i,'drtg':np.where(cp[i]>0,cpa[i]/np.where(cp[i]>0,cp[i],1)*100,np.nan)}))
dr=pd.concat(rows)
dr['drtg_rk']=dr.groupby(['season','date']).drtg.rank(method='max').where(dr.n>=10)
f=f.merge(dr[['season','date','OPP_ID','drtg_rk']],on=['season','date','OPP_ID'],how='left')
def diff(df,c):
    df=df[c.notna()] if False else df
    out={}
    for s,x in df.groupby('season'):
        p=x[x._c==1]; a=x[x._c==0]
        out[s]=(len(p),round(p.upside.mean()*100,1),round(a.upside.mean()*100,1),round((p.upside.mean()-a.upside.mean())*100,1))
    return out
res=[]
f['_c']=np.where(f.drtg_rk.notna(),(f.drtg_rk>=26).astype(float),np.nan)
x=f[f._c.notna()]
print('Opponent DRtg bottom 5 (general weakness):',diff(x,None))
f['_c']=np.where(f.drtg_rk.notna(),(f.drtg_rk>=21).astype(float),np.nan); x=f[f._c.notna()]
print('Opponent DRtg bottom 10:',diff(x,None))
PB=['rim','paint','mid','c3','atb3','trans','ml_pitp','ml_mid','ml_3pt']
heads=[(k,c) for k in ['cs3','pu3','pu2','lt10','wo','rim','paint','mid','c3','atb3','trans','ftr'] for c in ['vol_szn','eff_szn'] if not (k=='ftr' and c=='eff_szn')]+[(k,'ml') for k in ['ml_cs','ml_pu','ml_lt10','ml_pitp','ml_mid','ml_3pt']]
for k,c in heads:
    rc=f'{k}_rk' if c=='ml' else f'{k}_{c}_rk'
    for cut,th in [('b5',26),('b10',21)]:
        y=f.copy()
        if k in PB: y=y[y.pbp_window]
        y=y[y[rc].notna()&y[f'leg_{k}'].notna()&y.drtg_rk.notna()]
        y['_c']=(y[rc]>=th).astype(float)
        both=diff(y,None)
        lg=diff(y[y[f'leg_{k}']==1],None); nl=diff(y[y[f'leg_{k}']==0],None)
        # funnel net of general weakness: only games vs opponents NOT in DRtg bottom 10
        nd=diff(y[y.drtg_rk<21],None)
        overlap=((y[rc]>=th)&(y.drtg_rk>=21)).sum()/max((y[rc]>=th).sum(),1)
        res.append(dict(type=k,cond=c+'_'+cut,
            all_24=both.get('2024-25'),all_25=both.get('2025-26'),
            leans_24=lg.get('2024-25'),leans_25=lg.get('2025-26'),
            not_leans_24=nl.get('2024-25'),not_leans_25=nl.get('2025-26'),
            vs_non_weak_D_24=nd.get('2024-25'),vs_non_weak_D_25=nd.get('2025-26'),share_also_DRtg_b10=round(overlap,2)))
R=pd.DataFrame(res); R.to_csv('controls.csv',index=False)
pd.set_option('display.width',300); pd.set_option('display.max_colwidth',30)
def d(t): return t[3] if isinstance(t,tuple) else None
S=pd.DataFrame({'type':R.type,'cond':R.cond,'all':R.all_24.map(d).astype(str)+' / '+R.all_25.map(d).astype(str),
 'leans':R.leans_24.map(d).astype(str)+' / '+R.leans_25.map(d).astype(str),'not_leans':R.not_leans_24.map(d).astype(str)+' / '+R.not_leans_25.map(d).astype(str),
 'vs_nonweak_D':R.vs_non_weak_D_24.map(d).astype(str)+' / '+R.vs_non_weak_D_25.map(d).astype(str),'overlap_DRtg_b10':R.share_also_DRtg_b10})
print(S.to_string())
f.to_parquet('frame_e2.parquet')
