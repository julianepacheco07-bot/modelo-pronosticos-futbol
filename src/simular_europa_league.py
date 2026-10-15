#!/usr/bin/env python3
"""Exploratory pre-match Europa League simulation, with strict historical cutoff."""
from pathlib import Path
from datetime import date, datetime, timezone
import hashlib, json, math, requests, unicodedata, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"simulacion"/"simulacion_europa_league_2026-10-15.json"
TARGET=date(2026,10,15)
SEASONS=("2023-24","2024-25","2025-26")
LEAGUES={"Premier League":"en.1","LaLiga":"es.1","Serie A":"it.1","Bundesliga":"de.1","Ligue 1":"fr.1","Eredivisie":"nl.1","Primeira Liga":"pt.1","Belgian First Division":"be.1","Austrian Bundesliga":"at.1","Greek Super League":"gr.1","Scottish Premiership":"sco.1","Danish Superliga":"dk.1","Swiss Super League":"ch.1","Swedish Allsvenskan":"se.1","Norwegian Eliteserien":"no.1","Finnish Veikkausliiga":"fi.1","Turkish Super Lig":"tr.1","Polish Ekstraklasa":"pl.1","Croatian HNL":"hr.1","Hungarian NB I":"hu.1","Romanian Liga I":"ro.1"}
FIXTURES=[
("Sparta Praha","Lillestrøm"),("AZ Alkmaar","Hapoel Beer-Sheva"),("Salzburg","Milan"),
("Lech Poznań","Leverkusen"),("Celje","Omonia"),("Lyon","Crystal Palace"),
("Union SG","Real Sociedad"),("Torreense","Sunderland"),("Benfica","Celtic"),
("Bournemouth","Sturm Graz"),("Celta Vigo","Juventus"),("Dinamo Zagreb","Anderlecht"),
("Ferencváros","Viktoria Plzeň"),("Hoffenheim","Beşiktaş"),("Jagiellonia","Ararat-Armenia"),
("Marseille","Olympiacos"),("NEC Nijmegen","Levski Sofia"),("Rennes","OFI Crete")]
ALIASES={"bayer leverkusen":"leverkusen","bayer 04 leverkusen":"leverkusen","ac milan":"milan",
"olympique lyonnais":"lyon","rc celta de vigo":"celta vigo","real sociedad de futbol":"real sociedad","sparta praha":"sparta prague","sparta prague":"sparta prague","besiktas":"beşiktaş","viktoria plzen":"viktoria plzeň","n.e.c. nijmegen":"nec nijmegen","nec":"nec nijmegen","hapoel beer sheva":"hapoel beer-sheva"}
def norm(s):
    s=unicodedata.normalize("NFKD",str(s)).encode("ascii","ignore").decode("ascii").lower()
    s=re.sub(r"\b(fc|cf|afc|sc|fk|sk|ac|as|club)\b"," ",s)
    s=re.sub(r"[^a-z0-9]+"," ",s).strip()
    s=re.sub(r"\s+"," ",s)
    aliases={"bayer 04 leverkusen":"leverkusen","bayer leverkusen":"leverkusen","ac milan":"milan",
    "olympique lyonnais":"lyon","rc celta de vigo":"celta vigo","real sociedad de futbol":"real sociedad",
    "sparta praha":"sparta prague","besiktas":"besiktas","viktoria plzen":"viktoria plzen",
    "n e c nijmegen":"nec nijmegen","nec":"nec nijmegen","hapoel beer sheva":"hapoel beer sheva",
    "union saint gilloise":"union sg","ferencvarosi":"ferencvaros","ferencvaros budapest":"ferencvaros",
    "celta":"celta vigo","of i crete":"ofi crete","az":"az alkmaar"}
    return aliases.get(s,s)
def pois(lam,n=12):
    p=[math.exp(-lam)]
    for k in range(1,n+1): p.append(p[-1]*lam/k)
    z=sum(p); return [v/z for v in p]
def match_probs(lh,la):
    h,a=pois(lh),pois(la); p=[0.,0.,0.]; over=under=btts=0.
    for i,x in enumerate(h):
        for j,y in enumerate(a):
            q=x*y
            p[0 if i>j else 1 if i==j else 2]+=q
            if i+j>=2: over+=q
            if i+j<=3: under+=q
            if i>0 and j>0: btts+=q
    z=sum(p)
    return {"home_win":p[0]/z,"draw":p[1]/z,"away_win":p[2]/z,"over_1_5":over,"under_3_5":under,"btts_yes":btts}
def main():
    games=[]; source_manifest=[]
    for league,code in LEAGUES.items():
        for season in SEASONS:
            url=f"https://raw.githubusercontent.com/openfootball/football.json/master/{season}/{code}.json"
            try:
                resp=requests.get(url,timeout=25)
                if resp.status_code==404:
                    source_manifest.append({"league":league,"season":season,"url":url,"status":"no disponible"})
                    continue
                resp.raise_for_status()
            except requests.RequestException as exc:
                source_manifest.append({"league":league,"season":season,"url":url,"status":"error","detail":str(exc)[:180]})
                continue
            raw=resp.content; source_manifest.append({"league":league,"season":season,"url":url,"status":"ok","sha256":hashlib.sha256(raw).hexdigest()})
            obj=resp.json(); items=obj.get("matches",[]) if isinstance(obj,dict) else obj
            for m in items:
                sc=m.get("score",{}); sc=sc.get("ft") if isinstance(sc,dict) else sc
                if not isinstance(sc,list) or len(sc)!=2 or sc[0] is None or sc[1] is None: continue
                try: d=date.fromisoformat(str(m.get("date",""))[:10])
                except ValueError: continue
                if d>=TARGET: continue
                games.append({"date":d,"home":norm(str(m.get("team1",""))),"away":norm(str(m.get("team2",""))),
                              "hg":int(sc[0]),"ag":int(sc[1]),"league":league})
    output=[]
    for home,away in FIXTURES:
        hname,aname=norm(home),norm(away)
        hist_h=sorted([g for g in games if hname in (g["home"],g["away"])],key=lambda x:x["date"])[-10:]
        hist_a=sorted([g for g in games if aname in (g["home"],g["away"])],key=lambda x:x["date"])[-10:]
        rec={"date":TARGET.isoformat(),"competition":"UEFA Europa League","home":home,"away":away,
             "cutoff":"2026-10-15 00:00 UTC (solo resultados anteriores; sin datos del partido objetivo)",
             "odds":{"Betano":None,"other_bookmakers":None},"model":"Poisson exploratorio, hasta 10 partidos previos en 21 ligas y jornada 1 UEFA; mínimo 1 por equipo; estimaciones de baja confianza",
             "decision":"ANALISIS_INSUFICIENTE"}
        if len(hist_h)>=1 and len(hist_a)>=1:
            def rates(hist,team):
                gf=[];ga=[]
                for g in hist:
                    ishome=g["home"]==team
                    gf.append(g["hg"] if ishome else g["ag"]); ga.append(g["ag"] if ishome else g["hg"])
                return sum(gf)/len(gf),sum(ga)/len(ga)
            hgf,hga=rates(hist_h,hname); agf,aga=rates(hist_a,aname)
            # Suavizado de baja confianza: prior de 4 partidos equivalentes basado en los marcadores cargados.
            all_scores=[v for g in games for v in (g["hg"],g["ag"])]
            prior=sum(all_scores)/len(all_scores) if all_scores else 1.35
            def shrink(x,n,k=4): return (x*n+prior*k)/(n+k)
            hgf,hga=shrink(hgf,len(hist_h)),shrink(hga,len(hist_h))
            agf,aga=shrink(agf,len(hist_a)),shrink(aga,len(hist_a))
            lh=max(.15,(hgf+aga)/2); la=max(.15,(agf+hga)/2)
            rec.update({"lambda_home":round(lh,4),"lambda_away":round(la,4),
              "history":{"home_n":len(hist_h),"away_n":len(hist_a),"confidence":"BAJA" if min(len(hist_h),len(hist_a))<5 else "LIMITADA",
              "home_last_match":max(g["date"] for g in hist_h).isoformat(),
              "away_last_match":max(g["date"] for g in hist_a).isoformat()},
              "probabilities":{k:round(v,4) for k,v in match_probs(lh,la).items()},
              "decision":"REFERENCIA_EXPLORATORIA; NO ES MODELO VALIDADO PARA EUROPA LEAGUE",
              "limitations":"Estimación exploratoria no validada para Europa League; no incorpora alineaciones, lesiones, noticias ni cuotas verificadas. Incertidumbre alta con muestras cortas."})
        else:
            rec["reason"]="Sin historial previo identificable para uno o ambos equipos; no se imputa ni inventa probabilidad."
        output.append(rec)
    payload={"generated_utc":datetime.now(timezone.utc).isoformat(),"target_date":TARGET.isoformat(),
      "matches_requested":len(FIXTURES),"estimated":sum("probabilities" in x for x in output),
      "insufficient":sum("probabilities" not in x for x in output),"sources":source_manifest,"matches":output,"probability_caveat":"Estimaciones con menos de cinco partidos por equipo son de baja confianza; no constituyen recomendación automática de apuesta."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:payload[k] for k in ("generated_utc","target_date","matches_requested","estimated","insufficient")},ensure_ascii=False))
    print("OUTPUT="+str(OUT))
if __name__=="__main__": main()
