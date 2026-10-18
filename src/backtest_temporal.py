#!/usr/bin/env python3
"""Rolling-origin historical backtest for a transparent Poisson baseline."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, math, random
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

def paired_bootstrap(rows, model_keys, base_keys, target, multiclass_mode=False, reps=2000, seed=20261018):
    """Paired bootstrap CI for model-minus-baseline Brier/log-loss; negative favors model."""
    if len(rows)<2:
        return {'n':len(rows),'reps':0,'note':'Insufficient sample'}
    def losses(r, keys):
        ps=[max(1e-12,min(1-1e-12,float(r[k]))) for k in keys]
        if multiclass_mode:
            y=int(r[target])
            return sum((p-(i==y)**2) for i,p in enumerate(ps)), -math.log(ps[y])
        p=ps[0]; y=int(r[target])
        return (p-y)**2, -(y*math.log(p)+(1-y)*math.log(1-p))
    pairs=[(losses(r,model_keys),losses(r,base_keys)) for r in rows]
    obs_b=sum(a[0]-b[0] for a,b in pairs)/len(pairs)
    obs_l=sum(a[1]-b[1] for a,b in pairs)/len(pairs)
    rng=random.Random(seed+len(rows)+sum(ord(ch) for ch in target))
    boot_b=[]; boot_l=[]; n=len(pairs)
    for _ in range(reps):
        sample=[pairs[rng.randrange(n)] for _ in range(n)]
        boot_b.append(sum(a[0]-b[0] for a,b in sample)/n)
        boot_l.append(sum(a[1]-b[1] for a,b in sample)/n)
    boot_b.sort(); boot_l.sort()
    lo=int(0.025*reps); hi=min(reps-1,int(0.975*reps))
    return {'n':n,'reps':reps,'brier_delta_model_minus_baseline':round(obs_b,8),
      'brier_delta_95ci':[round(boot_b[lo],8),round(boot_b[hi],8)],
      'logloss_delta_model_minus_baseline':round(obs_l,8),
      'logloss_delta_95ci':[round(boot_l[lo],8),round(boot_l[hi],8)],
      'interpretation':'Negative favors Poisson; CI entirely below zero suggests evidence of lower loss under this bootstrap.'}

def calibration_bins(rows,pkey,ykey):
    bins=[]
    for lo in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
        subset=[r for r in rows if lo <= float(r[pkey]) < lo+0.1 or (lo==0.9 and float(r[pkey])==1.0)]
        bins.append({'range':f'{lo:.1f}-{lo+0.1:.1f}','n':len(subset),
          'mean_probability':round(sum(float(r[pkey]) for r in subset)/len(subset),6) if subset else None,
          'observed_rate':round(sum(int(r[ykey]) for r in subset)/len(subset),6) if subset else None})
    return bins

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
            # Baseline probabilities use only prior matches in this league.
            prior_n=max(1,len(league_old))
            base_home=(sum(1 for x in league_old if x['hg']>x['ag'])+1)/(prior_n+3)
            base_draw=(sum(1 for x in league_old if x['hg']==x['ag'])+1)/(prior_n+3)
            base_away=(sum(1 for x in league_old if x['hg']<x['ag'])+1)/(prior_n+3)
            base_total=base_home+base_draw+base_away
            base_1x2=[base_home/base_total,base_draw/base_total,base_away/base_total]
            base_over=(sum(1 for x in league_old if x['hg']+x['ag']>=2)+1)/(prior_n+2)
            base_under=(sum(1 for x in league_old if x['hg']+x['ag']<=3)+1)/(prior_n+2)
            base_btts=(sum(1 for x in league_old if x['hg']>0 and x['ag']>0)+1)/(prior_n+2)
            rows.append({'date':g['date'],'league':g['league'],'home':g['home'],'away':g['away'],'actual_1x2':0 if g['hg']>g['ag'] else 1 if g['hg']==g['ag'] else 2,'p_home':p[0],'p_draw':p[1],'p_away':p[2],'p_over15':b['over15'],'y_over15':int(g['hg']+g['ag']>=2),'p_under35':b['under35'],'y_under35':int(g['hg']+g['ag']<=3),'p_btts':b['btts'],'y_btts':int(g['hg']>0 and g['ag']>0),
              'base_home':base_1x2[0],'base_draw':base_1x2[1],'base_away':base_1x2[2],
              'base_over15':base_over,'base_under35':base_under,'base_btts':base_btts,
              'season':g['season'],'prior_home_n':len(hh),'prior_away_n':len(aa)})
        hist[(g['league'],g['home'])].append({'date':g['date'],'home':g['home'],'hg':g['hg'],'ag':g['ag']})
        hist[(g['league'],g['away'])].append({'date':g['date'],'home':g['home'],'hg':g['hg'],'ag':g['ag']})
    result={'generated_utc':datetime.now(timezone.utc).isoformat(),'seasons':list(SEASONS),'leagues':list(LEAGUES),'method':'Rolling origin; only earlier completed fixtures; last 10 matches per team; minimum 5 prior matches; shrinkage toward league mean.','raw_completed_matches':len(games),'evaluated_matches':len(rows),'skipped_insufficient_history':skipped,'source_manifest':sources,'source_errors':errors,'metrics':{'1x2':multiclass(rows,['p_home','p_draw','p_away'],'actual_1x2'),'over_1_5':binary(rows,'p_over15','y_over15'),'under_3_5':binary(rows,'p_under35','y_under35'),'btts_yes':binary(rows,'p_btts','y_btts')},
      'baseline_metrics':{'1x2':multiclass(rows,['base_home','base_draw','base_away'],'actual_1x2'),'over_1_5':binary(rows,'base_over15','y_over15'),'under_3_5':binary(rows,'base_under35','y_under35'),'btts_yes':binary(rows,'base_btts','y_btts')},
      'paired_bootstrap_95ci':{
        '1x2':paired_bootstrap(rows,['p_home','p_draw','p_away'],['base_home','base_draw','base_away'],'actual_1x2',True),
        'over_1_5':paired_bootstrap(rows,['p_over15'],['base_over15'],'y_over15'),
        'under_3_5':paired_bootstrap(rows,['p_under35'],['base_under35'],'y_under35'),
        'btts_yes':paired_bootstrap(rows,['p_btts'],['base_btts'],'y_btts')},
      'calibration':{'over_1_5':calibration_bins(rows,'p_over15','y_over15'),'under_3_5':calibration_bins(rows,'p_under35','y_under35'),'btts_yes':calibration_bins(rows,'p_btts','y_btts')},
      'by_league_season':{},
      'limitations':['Exploratory baseline; no odds or ROI claims.','Source coverage varies and is listed explicitly.','The special two-goal-lead market lacks historical goal-timeline data and is not validated by this backtest.']}
    for league in LEAGUES:
        for season in SEASONS:
            subset=[r for r in rows if r['league']==league and r['season']==season]
            if subset:
                result['by_league_season'][f'{league} {season}']={
                  'n':len(subset),
                  '1x2':multiclass(subset,['p_home','p_draw','p_away'],'actual_1x2'),
                  '1x2_baseline':multiclass(subset,['base_home','base_draw','base_away'],'actual_1x2'),
                  'over_1_5':binary(subset,'p_over15','y_over15'),
                  'over_1_5_baseline':binary(subset,'base_over15','y_over15'),
                  'under_3_5':binary(subset,'p_under35','y_under35'),
                  'under_3_5_baseline':binary(subset,'base_under35','y_under35'),
                  'btts_yes':binary(subset,'p_btts','y_btts'),
                  'btts_yes_baseline':binary(subset,'base_btts','y_btts')}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    met=result['metrics']; md=['# Backtest temporal — Poisson exploratorio','',f"Generado UTC: {result['generated_utc']}",'','**No es una prueba de rentabilidad.** Solo se evalúan partidos con al menos cinco partidos previos por equipo.','',f"- Partidos completos cargados: {len(games)}",f"- Partidos evaluados: {len(rows)}",f"- Omitidos por historial insuficiente: {skipped}",f"- Errores de descarga: {len(errors)}",'','| Mercado | N | Brier | Log loss | Exactitud / comparación |','|---|---:|---:|---:|---|']
    a=met['1x2']; md.append(f"| 1X2 | {a['n']} | {a['brier']} | {a['log_loss']} | Exactitud {a['accuracy']} |")
    for k,label in [('over_1_5','Over 1.5'),('under_3_5','Under 3.5'),('btts_yes','Ambos marcan')]:
        x=met[k]; md.append(f"| {label} | {x['n']} | {x['brier']} | {x['log_loss']} | Media {x['mean_probability']}; observada {x['observed_rate']} |")
    md+=['','## Comparación contra baseline histórico de liga (menor es mejor para Brier/log loss)','',
      '| Mercado | Poisson Brier | Baseline Brier | Poisson log loss | Baseline log loss |','|---|---:|---:|---:|---:|']
    for key,label in [('1x2','1X2'),('over_1_5','Over 1.5'),('under_3_5','Under 3.5'),('btts_yes','Ambos marcan')]:
        pm=met[key]; bm=result['baseline_metrics'][key]
        md.append(f"| {label} | {pm['brier']} | {bm['brier']} | {pm['log_loss']} | {bm['log_loss']} |")
    md+=['','## Incertidumbre: bootstrap pareado del diferencial de pérdida','',
      '2.000 remuestreos pareados de partidos. Diferencia = Poisson menos baseline; negativo favorece Poisson. IC 95% completamente negativo sugiere menor pérdida en esta muestra, no rentabilidad.','',
      '| Mercado | Delta Brier | IC 95% | Delta log loss | IC 95% |','|---|---:|---|---:|---|']
    for key,label in [('1x2','1X2'),('over_1_5','Over 1.5'),('under_3_5','Under 3.5'),('btts_yes','Ambos marcan')]:
        z=result['paired_bootstrap_95ci'][key]
        md.append(f"| {label} | {z['brier_delta_model_minus_baseline']} | {z['brier_delta_95ci']} | {z['logloss_delta_model_minus_baseline']} | {z['logloss_delta_95ci']} |")
    md+=['','## Calibración por rangos de probabilidad','',
      'Cada fila compara la probabilidad media pronosticada con la frecuencia observada; los rangos pequeños deben interpretarse con su N.','',
      '| Mercado | Rango | N | Prob. media | Frecuencia observada |','|---|---|---:|---:|---:|']
    for key,label in [('over_1_5','Over 1.5'),('under_3_5','Under 3.5'),('btts_yes','Ambos marcan')]:
        for b in result['calibration'][key]:
            if b['n']: md.append(f"| {label} | {b['range']} | {b['n']} | {b['mean_probability']} | {b['observed_rate']} |")
    md+=['','## Rendimiento por liga y temporada','',
      '| Liga-temporada | N | 1X2 Brier modelo/base | Over1.5 Brier modelo/base | Under3.5 Brier modelo/base | BTTS Brier modelo/base |','|---|---:|---:|---:|---:|---:|']
    for name,x in result['by_league_season'].items():
        md.append(f"| {name} | {x['n']} | {x['1x2']['brier']}/{x['1x2_baseline']['brier']} | {x['over_1_5']['brier']}/{x['over_1_5_baseline']['brier']} | {x['under_3_5']['brier']}/{x['under_3_5_baseline']['brier']} | {x['btts_yes']['brier']}/{x['btts_yes_baseline']['brier']} |")
    md+=['','## Fuentes','', '| Liga | Temporada | Estado | Partidos del archivo | URL |','|---|---|---|---:|---|']
    for s in sources: md.append(f"| {s['league']} | {s['season']} | {s['status']} | {s.get('matches_in_file','—')} | {s['url']} |")
    md+=['','## Limitaciones','']+['- '+x for x in result['limitations']]
    REPORT.write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps({'raw_completed_matches':len(games),'evaluated_matches':len(rows),'skipped':skipped,'errors':len(errors),'metrics':met},ensure_ascii=False))

if __name__=='__main__': main()