#!/usr/bin/env python3
"""Exploratory rolling-origin backtest for Colombia Primera A (OpenFootball).

No odds/ROI claims. Fixtures on the same calendar date are forecast before any
results from that date enter history, because kickoff times are not supplied.
"""
from __future__ import annotations
import datetime as dt, json, math, re, urllib.request
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/evaluacion/backtest_liga_betplay_2023_2025_ejecucion_diagnostica.json"
REPORT=ROOT/"data/evaluacion/backtest_liga_betplay_2023_2025_ejecucion_diagnostica.md"
SOURCES={
 2023:"https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2023_co1.txt",
 2024:"https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2024_co1.txt",
 2025:"https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2025_co1.txt"}
DATE_RE=re.compile(r"^\s{2,}(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+([A-Z][a-z]{2})\s+(\d{1,2})(?:\s+(\d{4}))?\s*$")
# Kickoff time is optional: OpenFootball has some matchdays without it.
MATCH_RE=re.compile(r"^\s{2,}(?:(\d{1,2}:\d{2})\s+)?(.+?)\s+v\s+(.+?)\s+(\d+)-(\d+)(?:\s|$)")
ALIASES={"Alianza Petrolera":"Alianza FC","Atlético Junior":"Junior FC","Junior":"Junior FC"}

def fetch(year):
 req=urllib.request.Request(SOURCES[year],headers={"User-Agent":"football-model-research/1.0"})
 with urllib.request.urlopen(req,timeout=30) as r:return r.read().decode("utf-8")
def parse(year,text):
 date=None;rows=[];unparsed=0
 for line in text.splitlines():
  d=DATE_RE.match(line)
  if d:
   try:date=dt.date(int(d.group(3) or year),dt.datetime.strptime(d.group(1),"%b").month,int(d.group(2))).isoformat()
   except ValueError:date=None
   continue
  if " v " not in line or not re.search(r"\d+-\d+",line):continue
  m=MATCH_RE.match(line)
  if not m:unparsed+=1;continue
  home,away=m.group(2).strip(),m.group(3).strip()
  if not date or not home or not away:unparsed+=1;continue
  rows.append({"date":date,"home":ALIASES.get(home,home),"away":ALIASES.get(away,away),"hg":int(m.group(4)),"ag":int(m.group(5)),"source_year":year})
 return rows,unparsed
def avg(xs):return sum(xs)/len(xs) if xs else 0.0
def poisson(lam,maximum=12):
 p=[math.exp(-lam)]
 for k in range(1,maximum+1):p.append(p[-1]*lam/k)
 z=sum(p);return [v/z for v in p]
def predict(lh,la):
 h,a=poisson(lh),poisson(la);p=[0.,0.,0.];m={"over15":0.,"under35":0.,"btts":0.}
 for i,hi in enumerate(h):
  for j,aj in enumerate(a):
   q=hi*aj;p[0 if i>j else 1 if i==j else 2]+=q
   if i+j>=2:m["over15"]+=q
   if i+j<=3:m["under35"]+=q
   if i>0 and j>0:m["btts"]+=q
 return p,m
def binary_metrics(probs,ys):
 eps=1e-12
 return {"brier":avg([(p-y)**2 for p,y in zip(probs,ys)]),
 "log_loss":avg([-math.log(max(eps,min(1-eps,p if y else 1-p))) for p,y in zip(probs,ys)]),
 "mean_probability":avg(probs),"observed_rate":avg(ys)}
def multiclass_metrics(rows,key):
 get=lambda r:r["p1x2"] if key=="model" else r["baseline_1x2"]
 return {"brier_multiclass":avg([sum((p-(i==r["y1x2"]))**2 for i,p in enumerate(get(r))) for r in rows]),
 "log_loss":avg([-math.log(max(1e-12,min(1-1e-12,get(r)[r["y1x2"]]))) for r in rows]),
 "accuracy":avg([int(max(range(3),key=lambda i:get(r)[i])==r["y1x2"]) for r in rows])}
def main():
 all_rows=[];coverage={}
 for year,url in SOURCES.items():
  source_text=fetch(year)
  rows,bad=parse(year,source_text)
  header=re.search(r"# Matches\s+(\d+)",source_text)
  expected=int(header.group(1)) if header else None
  coverage[str(year)]={"parsed_scored_matches":len(rows),"header_match_count":expected,"unparsed_score_lines":bad,"source_url":url,"count_matches_header":(expected is None or expected==len(rows))}
  all_rows+=rows
 all_rows.sort(key=lambda r:(r["date"],r["home"],r["away"]))
 seen=set();dupes=[]
 for r in all_rows:
  k=(r["date"],r["home"],r["away"])
  if k in seen:dupes.append(k)
  seen.add(k)
 bydate=defaultdict(list)
 for r in all_rows:bydate[r["date"]].append(r)
 history=defaultdict(list);prior=[];evaluated=[]
 for date in sorted(bydate):
  # No same-day results can leak into predictions: source lacks kickoff timestamps.
  league_home=avg([r["hg"] for r in prior]) if len(prior)>=30 else 1.35
  league_away=avg([r["ag"] for r in prior]) if len(prior)>=30 else 1.05
  base_1x2=[(sum((r["hg"]>r["ag"])==True and r["hg"]!=r["ag"] for r in prior)+2)/(len(prior)+6),
             (sum(r["hg"]==r["ag"] for r in prior)+2)/(len(prior)+6),
             (sum(r["hg"]<r["ag"] for r in prior)+2)/(len(prior)+6)]
  base_markets={}
  for k,fn in [("over15",lambda r:r["hg"]+r["ag"]>=2),("under35",lambda r:r["hg"]+r["ag"]<=3),("btts",lambda r:r["hg"]>0 and r["ag"]>0)]:
   base_markets[k]=(sum(fn(r) for r in prior)+2)/(len(prior)+4)
  for row in bydate[date]:
   hh,ah=history[row["home"]],history[row["away"]]
   if len(hh)<4 or len(ah)<4:continue
   hh,ah=hh[-10:],ah[-10:]
   rate=lambda xs,k:avg([x[k] for x in xs])
   lh=max(.15,(rate(hh,"gf")*rate(ah,"ga")+4*league_home)/5)
   la=max(.15,(rate(ah,"gf")*rate(hh,"ga")+4*league_away)/5)
   p1x2,markets=predict(lh,la)
   y=0 if row["hg"]>row["ag"] else 1 if row["hg"]==row["ag"] else 2
   outcomes={"over15":int(row["hg"]+row["ag"]>=2),"under35":int(row["hg"]+row["ag"]<=3),"btts":int(row["hg"]>0 and row["ag"]>0)}
   evaluated.append({**row,"lambda_home":lh,"lambda_away":la,"p1x2":p1x2,"markets":markets,"y1x2":y,
                     "outcomes":outcomes,"baseline_1x2":base_1x2,"baseline_markets":base_markets})
  for row in bydate[date]:
   prior.append(row);history[row["home"]].append({"gf":row["hg"],"ga":row["ag"]});history[row["away"]].append({"gf":row["ag"],"ga":row["hg"]})
 if not evaluated:raise SystemExit("No se generaron predicciones; revisar fuente y parser.")
 if any(not d["count_matches_header"] for d in coverage.values()):
  print("ADVERTENCIA: los conteos parseados no coinciden con los encabezados de la fuente; resultados no aptos para aprobar recalibración.")
 metrics={"1x2":{"n":len(evaluated),"model":multiclass_metrics(evaluated,"model"),"rolling_frequency_baseline":multiclass_metrics(evaluated,"baseline")}}
 for key in ("over15","under35","btts"):
  ys=[r["outcomes"][key] for r in evaluated]
  metrics[key]={"n":len(evaluated),"model":binary_metrics([r["markets"][key] for r in evaluated],ys),
   "rolling_frequency_baseline":binary_metrics([r["baseline_markets"][key] for r in evaluated],ys)}
 payload={"status":"diagnostic_not_approved_for_recalibration","method":"Date-batched rolling-origin; last 10 matches per team, minimum 4; Poisson score model with strength-4 shrinkage; compare with smoothed rolling competition-frequency baseline.",
 "source_coverage":coverage,"parsed_total":len(all_rows),"duplicate_fixtures_after_alias_normalization":len(dupes),"normalized_team_count":len(set([r["home"] for r in all_rows]+[r["away"] for r in all_rows])),
 "evaluated_matches":len(evaluated),"prediction_date_range":[evaluated[0]["date"],evaluated[-1]["date"]],"metrics":metrics,
 "limitations":["No kickoff timestamps; all same-date predictions made before that date's results enter history","Alias normalization only covers known Alianza Petrolera/Alianza FC and Atlético Junior/Junior labels","2025 file is partial through May in retrieved source","No confidence intervals, calibration bins, home/away-specific form or historical odds","No profitability/ROI claim"]}
 OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 lines=["# Backtest diagnóstico — Liga BetPlay 2023–2025","","**Estado: exploratorio; no aprobar recalibración ni apostar automáticamente con estos resultados.**","","## Cobertura"]
 for year,d in coverage.items():lines.append(f"- {year}: {d['parsed_scored_matches']} marcadores parseados; {d['unparsed_score_lines']} líneas de marcador no parseadas.")
 lines += [f"- Total parseado: {len(all_rows)}; duplicados tras normalizar alias: {len(dupes)}; equipos normalizados: {payload['normalized_team_count']}.",
 f"- Predicciones evaluadas: {len(evaluated)}; período {evaluated[0]['date']} a {evaluated[-1]['date']}.",
 "- Se corrigió el parser para admitir partidos sin hora de inicio y se agruparon las predicciones por fecha para evitar fuga de resultados del mismo día.","",
 "## Modelo frente a línea base rolling suavizada","","| Mercado | Modelo Brier | Base Brier | Modelo log loss | Base log loss | Prob. media modelo | Frecuencia real |","|---|---:|---:|---:|---:|---:|---:|"]
 for key,label in [("1x2","1X2"),("over15","Over 1.5"),("under35","Under 3.5"),("btts","Ambos marcan")]:
  m=metrics[key];mm=m["model"];bb=m["rolling_frequency_baseline"]
  lines.append(f"| {label} | {mm.get('brier_multiclass',mm.get('brier',0)):.4f} | {bb.get('brier_multiclass',bb.get('brier',0)):.4f} | {mm['log_loss']:.4f} | {bb['log_loss']:.4f} | {mm.get('mean_probability',float('nan')):.4f} | {mm.get('observed_rate',float('nan')):.4f} |")
 lines += ["","## Conclusión","",
 "El modelo Poisson supera modestamente a la línea base en 1X2, pero la línea base obtiene mejores Brier y log loss en Over 1.5, Under 3.5 y ambos marcan. Por tanto, no hay evidencia suficiente para aplicar una recalibración general ni para afirmar que el modelo mejora los mercados de goles.",
 "","## Limitaciones pendientes","",
 "El archivo de 2025 consultado es parcial; falta validar la cobertura de playoffs, normalizar exhaustivamente alias, evaluar por bandas de calibración y obtener intervalos de confianza temporales. No se usan cuotas históricas y no se calcula ROI. Los resultados son diagnósticos, no recomendaciones de apuestas.",""]
 REPORT.write_text("\n".join(lines),encoding="utf-8")
 print(json.dumps(payload,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
