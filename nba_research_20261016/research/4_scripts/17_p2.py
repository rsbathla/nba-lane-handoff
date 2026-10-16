import pandas as pd, numpy as np
exec(open('16_sweep.py').read().split("names=list(C)")[0].replace("f=f[f.qual].reset_index(drop=True)","f=f.reset_index(drop=True)"))
# add lock-time / in-game separately
lock={'A9_started':f.A9_started.astype(float).values,'C8_spread_move_toward':f.C8_spread_move_toward.astype(float).values}
for t in ['top','middle','bottom']: lock[f'C7_itt_close_t={t}']=np.where(f.C7_itt_close_t=='n/a',np.nan,(f.C7_itt_close_t==t).astype(float))
CUT=pd.Timestamp('2026-01-15')
f['win']=np.where(f.date<CUT,'build','read')
b=f[f.win=='build']; q=b.groupby('PLAYER_ID').dk.quantile(0.75); n=b.groupby('PLAYER_ID').size()
f['thr']=f.PLAYER_ID.map(q); f['nb']=f.PLAYER_ID.map(n).fillna(0)
f=f[f.nb>=20].copy(); keep=f.index.values
f['up']=f.dk>=f.thr
print('players',f.PLAYER_ID.nunique(),'build games',(f.win=='build').sum(),'read games',(f.win=='read').sum(),'read upside rate',f[f.win=='read'].up.mean().round(3))
allc={**C,**lock}
pooled=[]; per=[]
for name,arr in allc.items():
    v=pd.Series(np.asarray(arr,dtype=float)[keep],index=f.index)
    x=f[['PLAYER_ID','win','up']].assign(c=v); x=x[x.c.notna()]; x['pres']=x.c==1
    g=x.groupby(['win','pres']).up.agg(['size','mean']).unstack('pres')
    for w in ['build','read']:
        try: pooled.append({'cond':name,'win':w,'n_p':g.loc[w,('size',True)],'rate_p':g.loc[w,('mean',True)],'rate_a':g.loc[w,('mean',False)]})
        except KeyError: pass
    h=x.groupby(['PLAYER_ID','win','pres']).up.agg(['size','sum']).unstack(['win','pres'])
    h.columns=[f'{a}_{w}_{"p" if p else "a"}' for a,w,p in h.columns]; h=h.fillna(0); h['cond']=name; per.append(h.reset_index())
P=pd.DataFrame(pooled); P['diff']=(P.rate_p-P.rate_a)*100
PW=P.pivot_table(index='cond',columns='win',values=['n_p','diff']); PW.columns=[f'{a}_{b}' for a,b in PW.columns]; PW=PW.reset_index()
PW['lock_or_ingame']=PW.cond.isin(lock.keys())
PW['same_sign']=np.sign(PW.diff_build)==np.sign(PW.diff_read)
PW.to_csv('p2_pooled.csv',index=False)
Q=pd.concat(per,ignore_index=True)
for w in ['build','read']:
    for s in ['p','a']:
        for a in ['size','sum']:
            c=f'{a}_{w}_{s}'
            if c not in Q: Q[c]=0
Q['d_build']=(Q.sum_build_p/Q.size_build_p.replace(0,np.nan)-Q.sum_build_a/Q.size_build_a.replace(0,np.nan))*100
Q['d_read']=(Q.sum_read_p/Q.size_read_p.replace(0,np.nan)-Q.sum_read_a/Q.size_read_a.replace(0,np.nan))*100
ok=(Q.size_build_p>=10)&(Q.size_build_a>=10)&(Q.size_read_p>=5)&(Q.size_read_a>=5)
Q=Q[ok].copy(); Q['layer']=Q.cond.str[0]; Q.loc[Q.cond.isin(lock.keys()),'layer']='lock-time'
Q.to_parquet('p2_perplayer.parquet')
res=[]
for L,g in list(Q.groupby('layer'))+[('all pregame',Q[Q.layer!='lock-time'])]:
    bl=g[g.d_build>=10]; bn=g[g.d_build<=-10]
    res.append({'layer':L,'rows':len(g),'build leads':len(bl),'leads positive in read':round((bl.d_read>0).mean(),3),'build negatives':len(bn),'negatives positive in read':round((bn.d_read>0).mean(),3),'corr build-read':round(g.d_build.corr(g.d_read),3)})
R=pd.DataFrame(res); R.to_csv('p2_perplayer_summary.csv',index=False); print(R.to_string())
x=PW[~PW.lock_or_ingame]; print('pooled pregame conditions',len(x),'same sign',x.same_sign.sum(), '| build |diff|>=3:',(x.diff_build.abs()>=3).sum(),'of which same sign',x[x.diff_build.abs()>=3].same_sign.sum())
print(PW.sort_values('diff_build',ascending=False).head(25).round(2).to_string())
