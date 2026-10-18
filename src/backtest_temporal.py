#!/usr/bin/env python3
"""Rolling-origin historical backtest for a transparent Poisson baseline."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, math
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'evaluacion'/'backtest_temporal_2023_2026.json'
REPORT=ROOT/'data'/'evaluacion'/'backtest_temporal_2023_2026.md'
SEASONS=('2023-24','2024-25','2025-26')
LEAGUES={'Premier League':'en.1','LaLiga':'es.1','Serie A':'it.1','Bundesliga':'de.1','Ligue 1':'fr.1'}
MIN_PRIOR=5; MAX_PRIOR=10; PRIOR_STRENGTH=4.0

def pois(lam,n=12):
    p=[math.exp(-lam)]
    for k in range(1,n+1): p.append(p[-1]*lam/k)
    z=sum(p); return [x/z for x in p]

def markets(lh,la):
    hp,ap=pois(lh),pois(la); result=[0.0,0.0,0.0]; over=under=btts=0.0
    for i,pi in enumerate(hp):
        for j,pj in enumerate(ap):
            q=pi*pj; result[0 if i>j else 1 if i==j else 2]+=q
            if i+j>=2: over+=q
            if i+j<=3: under+=q
            if i>0 and j>0: btts+=q
    z=sum(result)
    return [x/z for x in result], {'over15':over,'under35':under,'btts':btts}

def multiclass(rows,keys,target):
    n=len(rows)
    if not n: return {'n':0,'brier':None,'log_loss':None,'accuracy':None}
    bs=ll=acc=0.0
    for r in rows:
        y=int(r[target]); ps=[max(1e-12,min(1-1e-12,float(r[k]))) for k in keys]
        bs+=sum((p-(i==y))**2 for i,p in enumerate(ps)); ll-=math.log(ps[y])
        acc+=int(max(range(len(ps)),key=lambda i:ps[i])==y)
    return {'n':n,'brier':round(bs/n,6),'log_loss':round(ll/n,6),'accuracy':round(acc/n,6)}

def binary(rows,pkey,ykey):
    n=len(rows)
    if not n: return {'n':0,'brier':None,'log_loss':None,'mean_probability':None,'observed_rate':None}
    bs=ll=sp=sy=0.0
    for r in rows:
        p=max(1e-12,min(1-1e-12,float(r[pkey]))); y=int(r[ykey])
        bs+=(p-y)**2; ll-=y*math.log(p)+(1-y)*math.log(1-p); sp+=p; sy+=y
    return {'n':n,'brier':round(bs/n,6),'log_loss':round(ll/n,6),'mean_probability':round(sp/n,6),'observed_rate':round(sy/n,6)}

def main():
    games=[]; sources=[]; errors=[]
    for league,code in LEAGUES.items():
        for season in SEASONS:
            url=f'https://raw.githubusercontent.com/openfootball/football.json/master/{season}/{code}.json'
            try:
                res=requests.get(url,timeout=30)
                if res.status_code==404: sources.append({'league':league,'season':season,'status':'404','url':url}); continue
                res.raise_for_status(); raw=res.content; obj=res.json()
                items=obj.get('matches',[]) if isinstance(obj,dict) else obj
                sources.append({'league':league,'season':season,'status':'ok','matches_in_file':len(items),'url':url,'sha256':hashlib.sha256(raw).hexdigest()})
                for m in items:
                    score=m.get('score',{}); ft=score.get('ft') if isinstance(score,dict) else score
                    if not isinstance(ft,list) or len(ft)!=2 or ft[0] is None or ft[1] is None: continue
                    d=str(m.get('date',''))[:10]
                    try: datetime.strptime(d,'%Y-%m-%d')
                    except ValueError: continue
                    games.append({'date':d,'league':league,'season':season,'home':str(m.get('team1','')).strip(),'away':str(m.get('team2','')).strip(),'hg':int(ft[0]),'ag':int(ft[1])})
            except Exception as e: errors.append({'league':league,'season':season,'url':url,'error':str(e)[:200]})
    games.sort(key=lambda x:(x['date'],x['league'],x['home'],x['away']))
    dedup=[]; seen=set()
    for g in games:
        key=(g['date'],g['league'],g['home'],g['away'],g['hg'],g['ag'])
        if key not in seen: seen.add(key); dedup.append(g)
    games=dedup; hist=defaultdict(list); rows=[]; skipped=0
    for g in games:
        hh=hist[(g['league'],g['home'])][-MAX_PRIOR:]; aa=hist[(g['league'],g['away'])][-MAX_PRIOR:]
        if len(hh)<MIN_PRIOR or len(aa)<MIN_PRIOR: skipped+=1
        else:
            league_old=[x for x in games if x['league']==g['league'] and x['date']<g['date']]
            prior=sum(x['hg']+x['ag'] for x in league_old)/max(1,2*len(league_old))
            hgf=sum(x['hg'] if x['home']==g['home'] else x['ag'] for x in hh)/len(hh)
            hga=sum(x['ag'] if x['home']==g['home'] else x['hg'] for x in hh)/len(hh)
            agf=sum(x['hg'] if x['home']==g['away'] else x['ag'] for x in aa)/len(aa)
            aga=sum(x['ag'] if x['home']==g['away'] else x['hg'] for x in aa)/len(aa)
            hgf=(hgf*len(hh)+prior*PRIOR_STRENGTH)/(len(hh)+PRIOR_STRENGTH); hga=(hga*len(hh)+prior*PRIOR_STRENGTH)/(len(hh)+PRIOR_STRENGTH)
            agf=(agf*len(aa)+prior*PRIOR_STRENGTH)/(len(aa)+PRIOR_STRENGTH); aga=(aga*len(aa)+prior*PRIOR_STRENGTH)/(len(aa)+PRIOR_STRENGTH)
            p,b=markets(max(.05,(hgf+aga)/2),max(.05,(agf+hga)/2))
            rows.append({'date':g['date'],'league':g['league'],'home':g['home'],'away':g['away'],'actual_1x2':0 if g['hg']>g['ag'] else 1 if g['hg']==g['ag'] else 2,'p_home':p[0],'p_draw':p[1],'p_away':p[2],'p_over15':b['over15'],'y_over15':int(g['hg']+g['ag']>=2),'p_under35':b['under35'],'y_under35':int(g['hg']+g['ag']<=3),'p_btts':b['btts'],'y_btts':int(g['hg']>0 and g['ag']>0),'prior_home_n':len(hh),'prior_away_n':len(aa)})
        hist[(g['league'],g['home'])].append({'date':g['date'],'home':g['home'],'hg':g['hg'],'ag':g['ag']})
        hist[(g['league'],g['away'])].append({'date':g['date'],'home':g['home'],'hg':g['hg'],'ag':g['ag']})
    result={'generated_utc':datetime.now(timezone.utc).isoformat(),'seasons':list(SEASONS),'leagues':list(LEAGUES),'method':'Rolling origin; only earlier completed fixtures; last 10 matches per team; minimum 5 prior matches; shrinkage toward league mean.','raw_completed_matches':len(games),'evaluated_matches':len(rows),'skipped_insufficient_history':skipped,'source_manifest':sources,'source_errors':errors,'metrics':{'1x2':multiclass(rows,['p_home','p_draw','p_away'],'actual_1x2'),'over_1_5':binary(rows,'p_over15','y_over15'),'under_3_5':binary(rows,'p_under35','y_under35'),'btts_yes':binary(rows,'p_btts','y_btts')},'limitations':['Exploratory baseline; no odds or ROI claims.','Source coverage varies and is listed explicitly.','The special two-goal-lead market lacks historical goal-timeline data and is not validated by this backtest.']}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    met=result['metrics']; md=['# Backtest temporal — Poisson exploratorio','',f"Generado UTC: {result['generated_utc']}",'','**No es una prueba de rentabilidad.** Solo se evalúan partidos con al menos cinco partidos previos por equipo.','',f"- Partidos completos cargados: {len(games)}",f"- Partidos evaluados: {len(rows)}",f"- Omitidos por historial insuficiente: {skipped}",f"- Errores de descarga: {len(errors)}",'','| Mercado | N | Brier | Log loss | Exactitud / comparación |','|---|---:|---:|---:|---|']
    a=met['1x2']; md.append(f"| 1X2 | {a['n']} | {a['brier']} | {a['log_loss']} | Exactitud {a['accuracy']} |")
    for k,label in [('over_1_5','Over 1.5'),('under_3_5','Under 3.5'),('btts_yes','Ambos marcan')]:
        x=met[k]; md.append(f"| {label} | {x['n']} | {x['brier']} | {x['log_loss']} | Media {x['mean_probability']}; observada {x['observed_rate']} |")
    md+=['','## Fuentes','', '| Liga | Temporada | Estado | Partidos del archivo | URL |','|---|---|---|---:|---|']
    for s in sources: md.append(f"| {s['league']} | {s['season']} | {s['status']} | {s.get('matches_in_file','—')} | {s['url']} |")
    md+=['','## Limitaciones','']+['- '+x for x in result['limitations']]
    REPORT.write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({'raw_completed_matches':len(games),'evaluated_matches':len(rows),'skipped':skipped,'errors':len(errors),'metrics':met},ensure_ascii=False))

if __name__=='__main__': main()