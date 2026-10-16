import pandas as pd, numpy as np
f=pd.read_parquet('frame_e.parquet'); f=f[f.qual].copy()
TR=['cs3','pu3','pu2','lt10','wo']; PB=['rim','paint','mid','c3','atb3','trans']; TYPES=TR+PB+['ftr']
MLT=['ml_cs','ml_pu','ml_lt10','ml_pitp','ml_mid','ml_3pt']
def conds(k):
    out={}
    for meas in ['vol','eff','voladj','effadj']:
        for win in ['szn','l10']:
            c=f'{k}_{meas}_{win}_rk'
            if c in f: 
                for cut,th in [('b5',26),('b10',21)]:
                    out[f'{meas}_{win}_{cut}']=np.where(f[c].notna(),f[c]>=th,np.nan)
    return out
def mlconds(k):
    c=f'{k}_rk'; return {'ml_b5':np.where(f[c].notna(),f[c]>=26,np.nan),'ml_b10':np.where(f[c].notna(),f[c]>=21,np.nan)}
recs=[]
base=f[['PLAYER_ID','PLAYER_NAME','posg','season','upside','pbp_window']].reset_index(drop=True)
def add(typ,cname,kind,flag):
    x=base.copy(); x['c']=np.asarray(flag,dtype=float)
    if typ in PB or typ in('ml_pitp','ml_mid','ml_3pt'): x.loc[~x.pbp_window,'c']=np.nan
    x=x[x.c.notna()]; x['pres']=x.c==1
    g=x.groupby(['PLAYER_ID','season','pres']).upside.agg(['size','sum']).unstack('pres',fill_value=0)
    g.columns=[f'{a}_{"p" if b else "a"}' for a,b in g.columns]
    for c in ['size_p','sum_p','size_a','sum_a']:
        if c not in g: g[c]=0
    g=g.reset_index(); g['type']=typ; g['cond']=cname; g['kind']=kind
    recs.append(g)
for k in TYPES+MLT:
    leg=f[f'leg_{k}'].values
    add(k,'player_leg','leg',leg)
    cs=mlconds(k) if k in MLT else conds(k)
    for cn,cv in cs.items():
        add(k,cn,'opp',cv)
        cr=np.where(np.isnan(leg.astype(float))|np.isnan(cv),np.nan,(leg==1)&(cv==1))
        add(k,cn,'cross',cr)
r=pd.concat(recs,ignore_index=True)
r=r.rename(columns={'size_p':'n_present','sum_p':'up_present','size_a':'n_absent','sum_a':'up_absent'})
r['rate_present']=r.up_present/r.n_present.replace(0,np.nan); r['rate_absent']=r.up_absent/r.n_absent.replace(0,np.nan)
r['diff_pts']=(r.rate_present-r.rate_absent)*100
info=f.groupby('PLAYER_ID').agg(player=('PLAYER_NAME','last'),posg=('posg','first'),games=('dk','size'),p75=('p75','first'))
ut=f.groupby('PLAYER_ID').usage_tier.value_counts(normalize=True).unstack(fill_value=0)
info=info.join(ut.add_prefix('usage_')); 
r=r.merge(info,left_on='PLAYER_ID',right_index=True)
r.to_parquet('counts_long.parquet')
print(r.shape, r.groupby(['kind']).size().to_dict())
