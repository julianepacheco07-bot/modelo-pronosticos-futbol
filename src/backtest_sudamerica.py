#!/usr/bin/env python3
"""Rolling backtest de goles para Colombia, Brasil y Argentina (OpenFootball CC0).
Uso: python src/backtest_sudamerica.py. No calcula ROI ni recomienda apuestas."""
import hashlib, json, math, re
from datetime import datetime
from pathlib import Path
import requests
import pandas as pd

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"/"south_america"
OUT=ROOT/"backtest_sudamerica_resultados.json"
BASE="https://raw.githubusercontent.com/openfootball/south-america/master"
SOURCES={
 "Colombia Primera A":[f"colombia/{y}_co1.txt" for y in (2023,2024,2025)],
 "Brazil Serie A":[f"brazil/{y}_br1.txt" for y in (2023,2024,2025)],
 "Argentina Primera":[f"argentina/{y}_ar1.txt" for y in (2023,2024,2025)]}
DATE=re.compile(r"^\s{2,}([A-Z][a-z]{2})\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
MATCH=re.compile(r"^\s{4,}(?:\d{1,2}:\d{2}\s+)?(.+?)\s+v\s+(.+?)\s+(\d+)\s*-\s*(\d+)(?:\s+\([^)]*\))?\s*$")
MONTHS={m:i for i,m in enumerate(["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]) if m}

def parse_txt(txt,league,season):
 rows=[]; year=int(season); month=day=None
 for line in txt.splitlines():
  d=DATE.match(line)
  if d:
   _,mon,dd,yy=d.groups(); year=int(yy) if yy else year; month=MONTHS[mon]; day=int(dd); continue
  m=MATCH.match(line)
  if not m or month is None: continue
  home,away,hg,ag=m.groups()
  try: date=datetime(year,month,day).date().isoformat()
  except ValueError: continue
  rows.append(dict(league=league,season=str(season),date=date,home=home.strip(),away=away.strip(),hg=int(hg),ag=int(ag)))
 return rows

def load():
 DATA.mkdir(parents=True,exist_ok=True); rows=[]; manifest=[]
 for league,paths in SOURCES.items():
  for rel in paths:
   url=f"{BASE}/{rel}"; resp=requests.get(url,timeout=40); resp.raise_for_status(); raw=resp.content
   (DATA/rel.replace("/","__")).write_bytes(raw)
   season=Path(rel).name.split("_")[0]; parsed=parse_txt(raw.decode("utf-8-sig"),league,season)
   if len(parsed)<100: raise RuntimeError(f"Formato/cobertura inesperado en {rel}: {len(parsed)} partidos")
   rows+=parsed; manifest.append({"url":url,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"matches_parsed":len(parsed)})
 if len(manifest) != sum(len(v) for v in SOURCES.values()):
  raise RuntimeError(f"Cobertura incompleta: {len(manifest)} fuentes recuperadas de {sum(len(v) for v in SOURCES.values())}.")
 raw_df=pd.DataFrame(rows)
 raw_df["date"]=pd.to_datetime(raw_df.date,errors="coerce")
 raw_df=raw_df.dropna(subset=["date"])
 # Remove exact duplicates, then exclude fixtures with contradictory final scores.
 key=["league","date","home","away"]
 exact_dups=int(raw_df.duplicated(key+["hg","ag"]).sum())
 raw_df=raw_df.drop_duplicates(key+["hg","ag"])
 score_counts=raw_df.groupby(key,dropna=False)[["hg","ag"]].apply(lambda g: len(g.drop_duplicates()))
 conflicted_keys=set(score_counts[score_counts>1].index.tolist())
 if conflicted_keys:
  tuples=pd.MultiIndex.from_frame(raw_df[key])
  conflict_index=pd.MultiIndex.from_tuples(list(conflicted_keys),names=key)
  raw_df=raw_df.loc[~tuples.isin(conflict_index)].copy()
 df=raw_df.sort_values(["league","date","home","away"]).reset_index(drop=True)
 return df,manifest,{"exact_duplicates_removed":exact_dups,"conflicting_fixtures_excluded":len(conflicted_keys)}

def poisson(lam,n=12):
 p=[math.exp(-lam)]
 for k in range(1,n+1): p.append(p[-1]*lam/k)
 z=sum(p); return [x/z for x in p]

def predict(hist,match):
 h=hist[(hist.home==match.home)|(hist.away==match.home)].tail(5)
 a=hist[(hist.home==match.away)|(hist.away==match.away)].tail(5)
 if len(h)<5 or len(a)<5 or len(hist)<30:return None
 def rates(g,team):
  gf=[];ga=[]
  for r in g.itertuples():
   gf.append(r.hg if r.home==team else r.ag); ga.append(r.ag if r.home==team else r.hg)
  return sum(gf)/len(gf),sum(ga)/len(ga)
 hgf,hga=rates(h,match.home); agf,aga=rates(a,match.away)
 avgh=max(.2,hist.hg.mean()); avga=max(.2,hist.ag.mean())
 lh=.65*(hgf/avgh)*(aga/avga)*avgh+.35*avgh
 la=.65*(agf/avga)*(hga/avgh)*avga+.35*avga
 lh=max(.15,min(3.5,lh)); la=max(.15,min(3.5,la)); ph=poisson(lh);pa=poisson(la)
 return {"lambda_home":round(lh,4),"lambda_away":round(la,4),
 "p_over_1_5":round(1-ph[0]*pa[0]-ph[1]*pa[0]-ph[0]*pa[1],6),
 "p_under_3_5":round(sum(ph[i]*pa[j] for i in range(13) for j in range(13) if i+j<=3),6),
 "p_btts_yes":round((1-ph[0])*(1-pa[0]),6)}

def score(p,y):
 p=min(1-1e-12,max(1e-12,p)); return (p-y)**2,-(y*math.log(p)+(1-y)*math.log(1-p))

def run():
 df,manifest,cleaning=load(); preds=[]; skipped=0
 for m in df.itertuples():
  hist=df[(df.league==m.league)&(df.date<m.date)]
  p=predict(hist,m)
  if p is None: skipped+=1; continue
  actual={"over_1_5":int(m.hg+m.ag>=2),"under_3_5":int(m.hg+m.ag<=3),"btts_yes":int(m.hg>0 and m.ag>0)}
  row={"league":m.league,"season":m.season,"date":m.date.date().isoformat(),"home":m.home,"away":m.away,**p,
       "actual_over_1_5":actual["over_1_5"],"actual_under_3_5":actual["under_3_5"],"actual_btts_yes":actual["btts_yes"],
       "history_n":len(hist)}
  # Leakage-safe reference: market prevalence from strictly earlier matches in this league.
  for market,yk in [("over_1_5","actual_over_1_5"),("under_3_5","actual_under_3_5"),("btts_yes","actual_btts_yes")]:
   if len(hist):
    outcomes=[int((r.hg+r.ag>=2) if market=="over_1_5" else ((r.hg+r.ag<=3) if market=="under_3_5" else (r.hg>0 and r.ag>0))) for r in hist.itertuples()]
    row[f"baseline_{market}"]=sum(outcomes)/len(outcomes)
   else: row[f"baseline_{market}"]=None
  preds.append(row)
 if not preds: raise RuntimeError("Sin predicciones; revisar formato de fechas y fuentes.")
 market_defs=[("over_1_5","p_over_1_5","actual_over_1_5"),("under_3_5","p_under_3_5","actual_under_3_5"),("btts_yes","p_btts_yes","actual_btts_yes")]
 def calc_metrics(rows,scope_name):
  out=[]
  for market,pk,yk in market_defs:
   valid=[r for r in rows if r.get(pk) is not None and r.get(yk) is not None]
   if not valid: continue
   sc=[score(float(r[pk]),int(r[yk])) for r in valid]
   brier=sum(v[0] for v in sc)/len(sc); logloss=sum(v[1] for v in sc)/len(sc)
   base=[score(float(r[f"baseline_{market}"]),int(r[yk])) for r in valid if r.get(f"baseline_{market}") is not None]
   base_brier=sum(v[0] for v in base)/len(base) if base else None
   out.append({"scope":scope_name,"market":market,"n":len(sc),"brier":round(brier,6),"logloss":round(logloss,6),
    "accuracy_at_0_5":round(sum((float(r[pk])>=.5)==bool(r[yk]) for r in valid)/len(valid),6),
    "baseline_brier":round(base_brier,6) if base_brier is not None else None,
    "baseline_logloss":round(sum(v[1] for v in base)/len(base),6) if base else None,
    "brier_skill_vs_historical_prevalence":round(1-brier/base_brier,6) if base_brier and base_brier>0 else None})
  return out
 metrics=calc_metrics(preds,"Global")
 grouped_metrics=[]
 for league in sorted({r["league"] for r in preds}):
  for season in sorted({r["season"] for r in preds if r["league"]==league}):
   subset=[r for r in preds if r["league"]==league and r["season"]==season]
   grouped_metrics.extend(calc_metrics(subset,f"{league} | {season}"))
 # Reliability table in fixed bins; expose observed frequencies and counts.
 calibration=[]
 for market,pk,yk in market_defs:
  for lo in [0,.1,.2,.3,.4,.5,.6,.7,.8,.9]:
   hi=lo+.1
   subset=[r for r in preds if lo <= float(r[pk]) < hi or (hi==1.0 and float(r[pk])<=1.0 and float(r[pk])>=lo)]
   if subset:
    calibration.append({"market":market,"bin_low":lo,"bin_high":hi,"n":len(subset),
      "mean_predicted":round(sum(float(r[pk]) for r in subset)/len(subset),6),
      "observed_rate":round(sum(int(r[yk]) for r in subset)/len(subset),6)})
 report={"created_utc":datetime.utcnow().isoformat(timespec="seconds")+"Z","source":"OpenFootball South America, CC0",
  "leagues":list(SOURCES),"seasons":[2023,2024,2025],"manifest":manifest,"matches_loaded":len(df),"cleaning":cleaning,
  "predictions_scored":len(preds),"skipped_insufficient_history":skipped,"metrics":metrics,"metrics_by_league_season":grouped_metrics,
  "calibration_bins":calibration,
  "limitations":["Poisson de forma reciente; no calibrado para apuestas.","Sin cuotas ni ROI: no afirma rentabilidad.",
  "Predicciones usan solo partidos estrictamente anteriores a la fecha objetivo.",
  "Baseline de prevalencia usa solo partidos anteriores de la misma liga; el skill es predictivo, no financiero.",
  "Resultados por liga-temporada pueden tener muestras pequeñas; revisar N antes de interpretar."],"predictions":preds}
 OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("matches_loaded","predictions_scored","skipped_insufficient_history","metrics")},ensure_ascii=False,indent=2))
 print("Informe:",OUT)

if __name__=="__main__": run()
