# Every shot type x every opponent split: does the split raise HIS attempts / makes / share of that type vs his own average?
# Descriptive counts only; both seasons side by side; baseline = his season-to-date mean over earlier games (5+ earlier games).
import pandas as pd, numpy as np
f=pd.read_parquet('frame_abcd.parquet'); f=f[f.qual].sort_values(['PLAYER_ID','date']).reset_index(drop=True)
PB={'rim','paint','mid','c3','atb3','trans','ml_pitp','ml_mid','ml_3pt'}
NAME={'cs3':'catch-and-shoot 3','pu3':'pull-up 3','pu2':'pull-up 2','lt10':'under 10 ft','wo':'wide open','rim':'rim (0-3 ft)','paint':'short paint (3-10 ft)','mid':'mid-range 2','c3':'corner 3','atb3':'above-break 3','trans':'transition','ftr':'free throws (FTA)',
      'ml_cs':'ML catch-and-shoot (all)','ml_pu':'ML pull-up (all)','ml_lt10':'ML under 10 ft','ml_pitp':'ML paint','ml_mid':'ML mid','ml_3pt':'ML 3PT'}
T={k:(f'{k}_a',f'{k}_m',f'leg_{k}',[f'{k}_{m}_{w}_rk' for m in ['vol','eff','voladj','effadj'] for w in ['szn','l10']]) for k in ['cs3','pu3','pu2','lt10','wo','rim','paint','mid','c3','atb3','trans']}
T['ftr']=('FTA','FTM','leg_ftr',[f'ftr_{m}_{w}_rk' for m in ['vol','voladj'] for w in ['szn','l10']])
for k,a in [('ml_cs','cs'),('ml_pu','pu'),('ml_lt10','lt10'),('ml_pitp','pitp'),('ml_mid','ml_mid'),('ml_3pt','3pt')]:
    T[k]=(f'{a}_a',f'{a}_m',f'leg_{k}',[f'{k}_rk'])
SPLIT=lambda c: c.replace(c.split('_rk')[0].rsplit('_',2)[0]+'_','',1).replace('_rk','') if not c.startswith('ml_') or c.count('_')>2 and not c.endswith('_rk') else c
def splitname(k,c):
    if c==f'{k}_rk': return 'Matchup Lab composite'
    s=c[len(k)+1:-3]; m,w=s.split('_'); return {'vol':'volume allowed','eff':'efficiency allowed','voladj':'volume allowed, opp-adjusted','effadj':'efficiency allowed, opp-adjusted'}[m]+(', season' if w=='szn' else ', last 10')
g=[f.PLAYER_ID,f.season]
f['tier']=f.A1_usg_szn_t.where(f.A1_usg_szn_t!='n/a')
out=[]; rep=[]
for k,(ac,mc,leg,rks) in T.items():
    a=f[ac].astype(float); mk=f[mc].astype(float); ok=a.notna()&mk.notna()&f.FGA.notna()
    if k in PB: ok&=f.pbp_window.astype(bool)
    den=f.FGA.astype(float)
    n=ok.astype(int); cn=n.groupby(g).cumsum()-n
    def prior(v):
        v=v.where(ok).fillna(0); return (v.groupby(g).cumsum()-v)
    base=(prior(a)/cn.replace(0,np.nan)).where(cn>=5); bm=(prior(mk)/cn.replace(0,np.nan)).where(cn>=5)
    bsh=(prior(a)/prior(den).replace(0,np.nan)).where(cn>=5)
    D=pd.DataFrame({'season':f.season,'pid':f.PLAYER_ID,'posg':f.posg,'tier':f.tier,'strong':f[leg]==1,
        'd_att':a-base,'d_mk':mk-bm,'d_sh':(a/den.replace(0,np.nan)-bsh)*100,'above':(a>base).astype(float),'up':f.upside.astype(float)})
    v=ok&base.notna()
    for rc in rks:
        if rc not in f: continue
        rk=f[rc]; sn=splitname(k,rc)
        for cut,lo in [('bottom 5',26),('bottom 10',21)]:
            x=D[v&rk.notna()].copy(); x['pres']=rk[x.index]>=lo; x['stingy']=rk[x.index]<=5
            for grp,mask in [('all players',None),('strong in the type',x.strong),('not strong',~x.strong)]+[(f'pos {p}',x.posg==p) for p in ['PG','SG','SF','PF','C']]+[(f'usage {t}',x.tier==t) for t in ['top','middle','bottom']]:
                y=x if mask is None else x[mask]
                for s,z in y.groupby('season'):
                    p=z[z.pres]; q=z[~z.pres]; st=z[z.stingy]
                    if len(p)<30 or len(q)<30: continue
                    out.append({'type':NAME[k],'key':k,'opponent split':sn,'cut':cut,'players':grp,'season':s,'games present':len(p),'games other':len(q),
                        'att vs own avg present':p.d_att.mean(),'att vs own avg other':q.d_att.mean(),'att vs own avg stingiest 5':st.d_att.mean() if len(st) else np.nan,
                        'att lift':p.d_att.mean()-q.d_att.mean(),'makes lift':p.d_mk.mean()-q.d_mk.mean(),'share lift (pts)':p.d_sh.mean()-q.d_sh.mean(),
                        'nights above own avg present %':p.above.mean()*100,'nights above own avg other %':q.above.mean()*100,
                        'upside present %':p.up.mean()*100,'upside other %':q.up.mean()*100,'upside lift':(p.up.mean()-q.up.mean())*100})
            if cut=='bottom 10':
                y=x[x.strong]; pp=y.groupby(['pid','season','pres']).d_att.agg(['mean','size']).unstack('pres')
                if ('size',True) in pp and ('size',False) in pp:
                    pp=pp[(pp[('size',True)]>=5)&(pp[('size',False)]>=5)]
                    dd=(pp[('mean',True)]-pp[('mean',False)]).unstack('season').dropna()
                    if dd.shape[1]==2 and len(dd)>=10:
                        c0,c1=dd.columns
                        rep.append({'type':NAME[k],'opponent split':sn,'strong players 5+/5+ both seasons':len(dd),'more both seasons':int(((dd[c0]>0)&(dd[c1]>0)).sum()),'fewer both':int(((dd[c0]<0)&(dd[c1]<0)).sum()),'mixed':int((dd[c0]*dd[c1]<=0).sum()),'size corr 24-25 vs 25-26':dd[c0].corr(dd[c1])})
R=pd.DataFrame(out); P=pd.DataFrame(rep)
W=R.pivot_table(index=['type','key','opponent split','cut','players'],columns='season',values=['att lift','makes lift','share lift (pts)','upside lift','games present','att vs own avg stingiest 5']).reset_index()
W.columns=[f'{a} {b}'.strip() for a,b in W.columns]
def verdict(r):
    a,b=r['att lift 2024-25'],r['att lift 2025-26']
    if pd.isna(a) or pd.isna(b): return 'n/a'
    if a>0 and b>0: return 'more attempts both seasons'
    if a<0 and b<0: return 'fewer attempts both seasons'
    return 'mixed'
W['volume read']=W.apply(verdict,axis=1); W['att lift smaller season']=np.where(W['volume read']=='more attempts both seasons',W[['att lift 2024-25','att lift 2025-26']].min(axis=1),np.nan)
O='/mnt/project-files/nba/p1_historical/layer_e/volume_check/'
R.round(3).to_csv(O+'volume_all_long.csv.gz',index=False,compression='gzip'); W.round(3).to_csv(O+'volume_all_wide.csv',index=False); P.round(3).to_csv(O+'volume_all_per_player_repeat.csv',index=False)
W.to_pickle('/tmp/volW.pkl'); P.to_pickle('/tmp/volP.pkl')
print(len(R),len(W)); print(W['volume read'].value_counts())
