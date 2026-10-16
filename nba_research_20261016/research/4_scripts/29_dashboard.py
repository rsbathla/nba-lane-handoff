# Team dashboard (single HTML page) from the tweets-digest JSON written by 28_tweet_digest.py with DASH_JSON set.
# Splits multi-team analyst notes (Thunder Dan / Adam Stock style team headers) into per-team excerpts.
# Usage: 29_dashboard.py <dash json> <out html>
import json,re,sys,html
D=json.load(open(sys.argv[1])); OUT=sys.argv[2]
AL={'ATL':['hawks'],'BOS':['celtics'],'BKN':['nets'],'CHA':['hornets'],'CHI':['bulls'],'CLE':['cavs','cavaliers'],'DAL':['mavs','mavericks'],
'DEN':['nuggets'],'DET':['pistons'],'GSW':['warriors','dubs'],'HOU':['rockets'],'IND':['pacers'],'LAC':['clippers'],'LAL':['lakers'],'MEM':['grizzlies','grizz'],
'MIA':['heat'],'MIL':['bucks'],'MIN':['wolves','timberwolves'],'NOP':['pels','pelicans'],'NYK':['knicks'],'OKC':['thunder'],'ORL':['magic'],'PHI':['sixers','76ers'],
'PHX':['suns'],'POR':['blazers','trail blazers'],'SAC':['kings'],'SAS':['spurs'],'TOR':['raptors'],'UTA':['jazz'],'WAS':['wizards']}
HDR={a:t for t,v in AL.items() for a in v}
def split_post(p):
    """Return {team: excerpt} for a multi-team post with team-name header lines; {} if it has none."""
    out={}; cur=None; buf=[]
    for line in p['text'].split('\n'):
        k=line.strip().lower().rstrip(':')
        if k in HDR:
            if cur and buf: out.setdefault(cur,[]).extend(buf)
            cur,buf=HDR[k],[]; continue
        if re.match(r'^[A-Za-z0-9 .]+ vs\.? [A-Za-z0-9 .()]+$',line.strip()):
            if cur and buf: out.setdefault(cur,[]).extend(buf)
            cur,buf=None,[]; continue
        if cur: buf.append(line)
    if cur and buf: out.setdefault(cur,[]).extend(buf)
    return {t:'\n'.join(v).strip() for t,v in out.items() if '\n'.join(v).strip()}
def mentions(p):
    t=p['text'].replace('Thunder Dan','').replace('ThunderDan','')
    return {tm for tm,v in AL.items() if any(re.search(r'\b'+re.escape(a)+r'\b',t,re.I) for a in v)}
for tm in D['teams']: D['teams'][tm]['analyst']=[]
for p in D['multi']:
    parts=split_post(p)
    base={k:p[k] for k in ('author','handle','date_utc','url','via','source') if k in p}
    if parts:
        for tm,ex in parts.items(): D['teams'][tm]['analyst'].append(dict(base,text=ex,excerpt=True))
    else:
        for tm in mentions(p): D['teams'][tm]['analyst'].append(dict(base,text=p['text'],excerpt=False))
for tm in D['teams']: D['teams'][tm]['analyst'].sort(key=lambda p:p['date_utc'],reverse=True)
GAMES={'BOS':'BOS @ DET','DET':'BOS @ DET','NYK':'PHI @ NYK','PHI':'PHI @ NYK','OKC':'OKC @ SAS','SAS':'OKC @ SAS'}
# The read for each team: same content as 28_verdict.md, attributed
NOTES={
'SAS':['Mitch Johnson said on 10-08 he is starting Fox, Castle and Harper with Vassell and Wembanyama (Jared Weiss), and that five started on 10-14.',
       'Harris, Keldon Johnson, Kornet and Champagnie were all out that night (Thunder Dan). Champagnie\'s 3-for-3 starts came in games Fox missed.',
       'Neither five has been tested with everyone available. Treat the board\'s Spurs start lines as open until lineups at lock.'],
'OKC':['Mara started 3 of 4 and Stirtz 2 of 4 with Holmgren and Jaylin Williams not playing. Holmgren was out 10-13 with a quad contusion.',
       'Daigneault: the rotation is "fluid night to night." Thunder Dan says Mara and Stirtz are not going to be in the regular-season rotation; Myguyknowsaguy thinks Stirtz could be.',
       'McCain ran 29-30% usage with Mitchell playing and 34% on 10-13 without him.',
       'Daigneault (10-09, via FCPNBA): Stirtz is still learning to play off the ball after being college\'s highest-usage player.'],
'PHI':['Simons, Bona and Barlow have not played (hamstring, foot, back). Nurse had "some hope" for the 10-16 finale.',
       'LeBron: one game, 18 minutes, one shot, 16% usage. Embiid had 8 turnovers in 24 minutes on 10-08 (Adam Stock).',
       'Edgecombe started all 3 games at 23 minutes; Wade\'s and Walker\'s starts came with others out.'],
'NYK':['The regular five started all 3 games they played, at 15 to 22 minutes. Thunder Dan flags Towns\'s assists as a possible hub role.',
       '10-13 vs Toronto was a full rest night (8 regulars did not dress), so that night\'s bench numbers say nothing.'],
'BOS':['White, Walsh, George, Tatum and Mitchell Robinson started the last two games. Queta came off the bench both nights; Mazzulla tried Robinson and Queta together late on 10-14.',
       'Tatum took 19 shots in 26 minutes on 10-10 and runs at 28.8% preseason usage.'],
'DET':['Bickerstaff (10-09, via FCPNBA) sees Ausar Thompson going above 26 minutes, in shorter stretches, with more ball-handling.',
       'Duren played once (10-14): started, 15 minutes, 24 points, 38% usage. Reed\'s 3 games of center minutes came while Duren was out.'],
'LAC':['Strus has a partial plantar fascia tear, re-evaluated in 4 weeks (Shams, 10-05). Wagler started in his place on 10-14.'],
'POR':['Coach Micah Nori said starting Morant and Lillard together "doesn\'t make sense." Scoot Henderson started over Morant on 10-13.'],
'TOR':['Kawhi Leonard sat the first games on a ramp-up plan and was available from 10-13 (17 minutes, started).',
       'FCPNBA (10-11, citing @JLew1050) expects Ja\'Kobe Walter to get 15-20 starts on Kawhi rest nights.'],
'LAL':['Redick: the starting spots beside Dončić, Reaves and Kessler are "nothing definitive yet."'],
'BKN':['Same starting five all preseason (Dëmin, Ellis, Porter Jr., Randle, Sharpe). Thunder Dan expects Porter\'s high-usage role to continue.'],
}
for tm,v in NOTES.items(): D['teams'][tm]['notes']=v
for tm in D['teams']: D['teams'][tm]['game']=GAMES.get(tm)
import os
if os.environ.get('FULL_JSON'): json.dump(D,open(os.environ['FULL_JSON'],'w'),ensure_ascii=False)  # processed data for 30_design_data.py
data=json.dumps(D,ensure_ascii=False).replace('</','<\\/')
tpl=open(sys.argv[0].replace('29_dashboard.py','29_dashboard_template.html')).read()
open(OUT,'w').write(tpl.replace('/*__DATA__*/null',data))
print('teams',len(D['teams']),'analyst excerpts',sum(len(t['analyst']) for t in D['teams'].values()),'bytes',len(data))
