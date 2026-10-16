# Ramneik's challenge (2026-10-15): does a generous shot-type defense raise HIS attempts of that type, vs his own prior average?
# Descriptive counts only. Baseline = his season-to-date mean from earlier games (5+ earlier games). Both seasons side by side.
import pandas as pd, numpy as np
f=pd.read_parquet('frame_abcd.parquet'); f=f[f.qual].sort_values(['PLAYER_ID','date']).reset_index(drop=True)
TR=['cs3','pu3','pu2','lt10','wo']; PB=['rim','paint','mid','c3','atb3','trans']
types=[k for k in TR+PB if f'{k}_a' in f and f'{k}_vol_szn_rk' in f]
g=[f.PLAYER_ID,f.season]
rows=[]; prow=[]
for k in types:
    a=f[f'{k}_a'].astype(float)
    ok=a.notna()&f.FGA.notna()
    if k in PB: ok&=f.pbp_window.astype(bool)
    a=a.where(ok); sh=(a/f.FGA.replace(0,np.nan)).where(ok)
    n=ok.astype(int); cn=n.groupby(g).cumsum()-n
    ca=a.fillna(0).groupby(g).cumsum()-a.fillna(0); cf=f.FGA.where(ok).fillna(0).groupby(g).cumsum()-f.FGA.where(ok).fillna(0)
    base=(ca/cn.replace(0,np.nan)).where(cn>=5); bsh=(ca/cf.replace(0,np.nan)).where(cn>=5)
    rk=f[f'{k}_vol_szn_rk']
    for cond,th in [('bottom 5 (26-30)',26),('bottom 10 (21-30)',21)]:
        for legname,legmask in [('all players',pd.Series(True,index=f.index)),('strong in the type',f[f'leg_{k}']==1)]:
            x=pd.DataFrame({'season':f.season,'pres':rk>=th,'rk':rk,'a':a,'base':base,'sh':sh,'bsh':bsh,'up':f.upside,'pid':f.PLAYER_ID})[legmask & ok & base.notna() & rk.notna()]
            x['more']=x.a>x.base; x['more_sh']=x.sh>x.bsh; x['d']=x.a-x.base; x['dsh']=(x.sh-x.bsh)*100
            for s,y in x.groupby('season'):
                p=y[y.pres]; q=y[~y.pres]; st=y[y.rk<=5]
                rows.append({'type':k,'defense':cond,'players':legname,'season':s,
                  'games present':len(p),'games other':len(q),
                  'att vs own avg, present':round(p.d.mean(),2),'att vs own avg, other':round(q.d.mean(),2),'att vs own avg, stingiest 5':round(st.d.mean(),2),
                  'share of his FGA vs own (pts), present':round(p.dsh.mean(),1),'share vs own, other':round(q.dsh.mean(),1),
                  'nights above own avg, present':f"{int(p.more.sum())}/{len(p)} = {p.more.mean()*100:.1f}%",'nights above own avg, other':f"{int(q.more.sum())}/{len(q)} = {q.more.mean()*100:.1f}%",
                  'upside when above own avg':f"{int(y[y.more].up.sum())}/{int(y.more.sum())} = {y[y.more].up.mean()*100:.1f}%",'upside when not':f"{int(y[~y.more].up.sum())}/{int((~y.more).sum())} = {y[~y.more].up.mean()*100:.1f}%",
                  'upside present & above own avg':f"{y[y.pres&y.more].up.mean()*100:.1f}%",'upside present & not above':f"{y[y.pres&~y.more].up.mean()*100:.1f}%"})
            if cond.startswith('bottom 10') and legname=='strong in the type':
                pp=x.groupby(['pid','season','pres']).d.agg(['mean','size']).unstack('pres')
                pp=pp[(pp[('size',True)]>=5)&(pp[('size',False)]>=5)]
                dd=(pp[('mean',True)]-pp[('mean',False)]).unstack('season').dropna()
                if dd.shape[1]==2:
                    c=dd.columns
                    prow.append({'type':k,'players with 5+/5+ games both seasons':len(dd),'more attempts vs bottom 10 in both seasons':int(((dd[c[0]]>0)&(dd[c[1]]>0)).sum()),'fewer in both':int(((dd[c[0]]<0)&(dd[c[1]]<0)).sum()),'mixed':int((dd[c[0]]*dd[c[1]]<=0).sum()),'corr season1 vs season2':round(dd[c[0]].corr(dd[c[1]]),3)})
R=pd.DataFrame(rows); P=pd.DataFrame(prow)
O='/mnt/project-files/nba/p1_historical/layer_e/volume_check/'
R.to_csv(O+'volume_by_type.csv',index=False); P.to_csv(O+'volume_per_player_repeat.csv',index=False)
pd.set_option('display.width',300); pd.set_option('display.max_columns',30)
print(R[(R.defense.str.startswith('bottom 10'))][['type','players','season','games present','att vs own avg, present','att vs own avg, other','att vs own avg, stingiest 5','share of his FGA vs own (pts), present','share vs own, other','nights above own avg, present','nights above own avg, other']].to_string())
print(R[(R.defense.str.startswith('bottom 10'))&(R.players=='strong in the type')][['type','season','upside when above own avg','upside when not','upside present & above own avg','upside present & not above']].to_string())
print(P.to_string())
