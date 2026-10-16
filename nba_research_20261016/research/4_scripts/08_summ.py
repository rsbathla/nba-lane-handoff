import pandas as pd, numpy as np
r=pd.read_parquet('counts_long.parquet')
k=['type','cond','kind','season']
def pool(df,by):
    g=df.groupby(by)[['n_present','up_present','n_absent','up_absent']].sum().reset_index()
    g['rate_p']=g.up_present/g.n_present; g['rate_a']=g.up_absent/g.n_absent; g['diff']=(g.rate_p-g.rate_a)*100
    return g
P=pool(r,k); PP=pool(r,k+['posg'])
w=P.pivot_table(index=['type','cond','kind'],columns='season',values=['n_present','up_present','n_absent','up_absent','rate_p','rate_a','diff']).reset_index()
w.columns=['_'.join([c for c in col if c]) for col in w.columns]
w.to_csv('pooled_overall.csv',index=False); PP.to_csv('pooled_by_position.csv',index=False)
h=w[w.cond.isin(['player_leg','vol_szn_b5','vol_szn_b10','eff_szn_b5','eff_szn_b10','ml_b5','ml_b10'])]
pd.set_option('display.width',250)
print(h[['type','cond','kind','n_present_2024-25','rate_p_2024-25','rate_a_2024-25','diff_2024-25','n_present_2025-26','rate_p_2025-26','rate_a_2025-26','diff_2025-26']].round(3).to_string())
