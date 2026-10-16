# Merge the X-search post files (search titles, dated from status IDs), apply checked fixes, write one clean list for 28_tweet_digest.py.
# Usage: 28b_clean_xposts.py <out json> <xposts json files...>
import json,sys,re,datetime
OUT=sys.argv[1]; P=[]; ART=[]
for fn in sorted(sys.argv[2:],key=lambda f:not re.search('chrome|fcpnba',f)):
    j=json.load(open(fn)); pp=(j['posts'] if isinstance(j,dict) else j)
    for p in pp: p['handle']=p['handle'].lstrip('@'); p['via']='chrome' if re.search('chrome|fcpnba',fn) else 'search'
    P+=pp; ART+=(j.get('articles',[]) if isinstance(j,dict) else [])
DROP={'https://x.com/SpectrumSN/status/'}  # prefix: lineup post whose title has no names
out=[]; seen=set()
for p in P:
    u=p['url'].split('?')[0]; p['url']=u
    if u in seen or any(u.startswith(d) and 'SpectrumSN' in u for d in DROP): continue
    if p['handle'].lower()=='baruthaalex' and ('Mock Draft' in p['text'] or 'Sleepers and Breakouts' in p['text']): continue  # category-league drafts, no role info
    sid=int(re.search(r'status/(\d+)',u).group(1)); d=datetime.datetime.fromtimestamp(((sid>>22)+1288834974657)/1000,datetime.UTC)
    if d.date()<datetime.date(2026,9,25): continue
    p['date_utc']=d.strftime('%Y-%m-%dT%H:%MZ')
    if p['handle']=='fcpnba' and "Ja'Kobe Walter" in p['text']: p['team']='TOR'  # roster 10-15: Walter and Kawhi on TOR (the RC tag said LAC)
    if 'Max Strus' in p['text']: p['team']='LAC'  # roster capture 10-15: Strus on LAC
    if p['handle']=='myguyknowsaguy' and p['team']=='MULTI': p['team']='UTA'  # post leads with Peterson / Jazz
    seen.add(u); out.append(p)
    if 'Luka Doncic and Draymond Green are resting' in p['text']: out.append(dict(p,team='LAL' if p['team']=='GSW' else 'GSW'))
json.dump({'posts':out,'articles':ART},open(OUT,'w'),indent=1,ensure_ascii=False)
print(len(P),'->',len(out),'articles',len(ART))
