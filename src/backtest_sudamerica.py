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
 df=pd.DataFrame(rows).drop_duplicates(["league","date","home","away","hg","ag"])
 df["date"]=pd.to_datetime(df.date,errors="coerce"); df=df.dropna(subset=["date"]).sort_values(["league","date"]).reset_index(drop=True)
 return df,manifest

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
 df,manifest=load(); preds=[]; skipped=0
 for m in df.itertuples():
  hist=df[(df.league==m.league)&(df.date<m.date)]
  p=predict(hist,m)
  if p is None: skipped+=1; continue
  preds.append({"league":m.league,"season":m.season,"date":m.date.date().isoformat(),"home":m.home,"away":m.away,
   **p,"actual_over_1_5":int(m.hg+m.ag>=2),"actual_under_3_5":int(m.hg+m.ag<=3),"actual_btts_yes":int(m.hg>0 and m.ag>0)})
 if not preds: raise RuntimeError("Sin predicciones; revisar formato de fechas y fuentes.")
 metrics=[]
 for market,pk,yk in [("over_1_5","p_over_1_5","actual_over_1_5"),("under_3_5","p_under_3_5","actual_under_3_5"),("btts_yes","p_btts_yes","actual_btts_yes")]:
  sc=[score(x[pk],x[yk]) for x in preds]
  metrics.append({"market":market,"n":len(sc),"brier":round(sum(x[0] for x in sc)/len(sc),6),"logloss":round(sum(x[1] for x in sc)/len(sc),6),
   "accuracy_at_0_5":round(sum((p[pk]>=.5)==bool(p[yk]) for p in preds)/len(preds),6)})
 report={"created_utc":datetime.utcnow().isoformat(timespec="seconds")+"Z","source":"OpenFootball South America, CC0",
  "leagues":list(SOURCES),"seasons":[2023,2024,2025],"manifest":manifest,"matches_loaded":len(df),
  "predictions_scored":len(preds),"skipped_insufficient_history":skipped,"metrics":metrics,
  "limitations":["Baseline de forma reciente + Poisson; no calibrado para apuestas.","Sin cuotas ni ROI: no afirma rentabilidad.",
  "Predicciones usan solo partidos anteriores a la fecha objetivo.","Cobertura depende de los archivos públicos de origen."],"predictions":preds}
 OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({k:report[k] for k in ("matches_loaded","predictions_scored","skipped_insufficient_history","metrics")},ensure_ascii=False,indent=2))
 print("Informe:",OUT)

if __name__=="__main__": run()
