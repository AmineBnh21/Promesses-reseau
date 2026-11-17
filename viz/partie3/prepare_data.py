"""Partie 3 : vues liées par département (carte cliquable, zoom, détail à la demande).

Entrées
  - data/dispositif_couverture_ciblee/*/*_sites.csv   (relevés trimestriels DCC)
  - data/jalerte_opendata_bilanannuel/2.1.2.a_repartition_...  (nb d'alertes mobiles 2025 par hexagone)
  - viz/partie3/geo/departements.geojson    (contours simplifiés, github.com/gregoiredavid/france-geojson)
  - viz/partie3/geo/communes_population.json (population des communes, geo.api.gouv.fr)

Traitements
  - délai de mise en service de chaque site (même méthode que la partie 2)
  - conversion Lambert-93 -> WGS84 (formules IGN, sans dépendance externe)
  - rattachement des sites et des hexagones J'alerte à un département par point-dans-polygone
  - population et alertes mobiles par département (somme des hexagones dont le centre tombe dedans)

Usage : python viz/partie3/prepare_data.py   (depuis la racine du projet)
"""
import json
import math
import re
from pathlib import Path

import pandas as pd
from matplotlib.path import Path as MplPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DCC = ROOT / "data" / "dispositif_couverture_ciblee"
JALERTE = ROOT / "data" / "jalerte_opendata_bilanannuel" / "2.1.2.a_repartition_alertes_france_2025_mobile_grandpublic.csv"
GEO = HERE / "geo" / "departements.geojson"
POP = HERE / "geo" / "communes_population.json"  # https://geo.api.gouv.fr/communes?fields=codeDepartement,population
OUT = HERE / "data.js"
OPS = {"20801": "Orange", "20810": "SFR", "20815": "Free", "20820": "Bouygues Telecom"}
DELAI = 24


# ---------- Lambert-93 -> WGS84 (IGN, note ALG0004) ----------
N, C, XS, YS = 0.7256077650532670, 11754255.426096, 700000.0, 12655612.049876
E, LON0 = 0.0818191910428158, math.radians(3)


def l93_to_wgs84(x, y):
    dx, dy = x - XS, YS - y
    r = math.hypot(dx, dy)
    lon = LON0 + math.atan2(dx, dy) / N
    lat_iso = -math.log(r / C) / N
    phi = 2 * math.atan(math.exp(lat_iso)) - math.pi / 2
    for _ in range(10):
        es = E * math.sin(phi)
        phi = 2 * math.atan(((1 + es) / (1 - es)) ** (E / 2) * math.exp(lat_iso)) - math.pi / 2
    return round(math.degrees(lon), 4), round(math.degrees(phi), 4)


# ---------- départements ----------
geo = json.loads(GEO.read_text(encoding="utf-8"))
paths = []  # (code, MplPath)


def ring_area(ring):
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:]))


def prep_ring(ring, exterior):
    ring = [[round(x, 4), round(y, 4)] for x, y in ring]
    # d3-geo attend des anneaux extérieurs dans le sens horaire (inverse de la RFC 7946)
    if (ring_area(ring) > 0) == exterior:
        ring = ring[::-1]
    return ring


for f in geo["features"]:
    g, code = f["geometry"], f["properties"]["code"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    polys = [[prep_ring(r, i == 0) for i, r in enumerate(p)] for p in polys]
    f["geometry"] = {"type": "MultiPolygon", "coordinates": polys}
    f["properties"] = {"code": code, "nom": f["properties"]["nom"]}
    for p in polys:
        paths.append((code, MplPath(p[0])))


def dep_of(lon, lat):
    for code, p in paths:
        if p.contains_point((lon, lat)):
            return code
    return None


# ---------- délais (méthode partie 2) ----------
def fin_trimestre(a, t):
    return pd.Timestamp(year=a, month=3 * t, day=1) + pd.offsets.MonthEnd(0)


def mois(a, b):
    return (b - a).days / 30.4375


fichiers = sorted(DCC.glob("*/*_sites.csv"))
trimestres, premier = [], {}
for i, f in enumerate(fichiers):
    a, t = map(int, re.match(r"(\d{4})_T(\d)", f.name).groups())
    trimestres.append({"label": f"{a} T{t}", "fin": fin_trimestre(a, t)})
    d = pd.read_csv(f, sep=";", dtype=str)
    for s in d.loc[d["sites_mes"] == "1", "numero_site"]:
        premier.setdefault(s, i)

df = pd.read_csv(fichiers[-1], sep=";", dtype=str)
df["pub"] = pd.to_datetime(df["date_publication_arrete"], errors="coerce", format="mixed", dayfirst=True)
for c in ("x_lambert_93", "y_lambert_93"):
    df[c] = pd.to_numeric(df[c].str.replace(",", "."), errors="coerce")
fin_obs = trimestres[-1]["fin"]
codes = {f["properties"]["code"] for f in geo["features"]}

sites, hors_dep = [], 0
for r in df.itertuples():
    lon = lat = None
    dep = None
    if pd.notna(r.x_lambert_93):
        lon, lat = l93_to_wgs84(r.x_lambert_93, r.y_lambert_93)
        dep = dep_of(lon, lat)
    if dep is None:  # pas de coordonnées : premier code INSEE cité ("02 / 80" -> "02")
        c = str(r.insee_dep).split("/")[0].strip()
        dep = c if c in codes else None
    hors_dep += dep is None
    q = premier.get(r.numero_site)
    s = {"id": r.numero_site, "zone": r.nom_de_la_zone if isinstance(r.nom_de_la_zone, str) else None,
         "dep": dep, "op": OPS.get(r.op_leader, "Non déterminé"),
         "arrete": r.pub.strftime("%Y-%m-%d") if pd.notna(r.pub) else None, "lon": lon, "lat": lat, "q": q}
    if pd.isna(r.pub):
        s["statut"] = "inconnu"
    else:
        ech = r.pub + pd.DateOffset(months=DELAI)
        if q is None:
            s["attente_mois"] = round(mois(r.pub, fin_obs), 1)
            s["statut"] = "attente_retard" if fin_obs > ech else "attente_dans_delai"
        elif q == 0:
            s["statut"] = "avant_2022"
        else:
            debut, fin = trimestres[q - 1]["fin"], trimestres[q]["fin"]
            s["delai_min"], s["delai_max"] = round(max(0, mois(r.pub, debut)), 1), round(mois(r.pub, fin), 1)
            s["statut"] = "a_temps" if fin <= ech else ("en_retard" if debut > ech else "incertain")
    sites.append(s)

# ---------- J'alerte : alertes mobiles par département ----------
# Fichier "répartition" : nombre d'alertes par hexagone (6 389 alertes localisées sur 7 430 au bilan).
# Chaque hexagone est rattaché au département qui contient son centre (approximation en limite).
h = pd.read_csv(JALERTE, sep=";", encoding="cp1252")
alertes = {}
for n, g in zip(h.iloc[:, 0], h["geometry"]):
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", g)]
    cx, cy = sum(nums[0::2]) / len(nums[0::2]), sum(nums[1::2]) / len(nums[1::2])
    dep = dep_of(*l93_to_wgs84(cx, cy))
    if dep:
        alertes[dep] = alertes.get(dep, 0) + int(n)

# ---------- population officielle (geo.api.gouv.fr, somme des communes) ----------
pop = {}
for c in json.loads(POP.read_text(encoding="utf-8")):
    pop[c["codeDepartement"]] = pop.get(c["codeDepartement"], 0) + (c.get("population") or 0)

deps = {code: {"pop": pop.get(code, 0), "alertes": alertes.get(code, 0)} for code in sorted(codes)}

out = {"trimestres": [t["label"] for t in trimestres], "delai_promis": DELAI,
       "geo": geo, "sites": sites, "deps": deps}
OUT.write_text("window.DATA3 = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size // 1024} Ko) | {len(sites)} sites, {hors_dep} sans département | "
      f"{len(deps)} départements, {sum(d['pop'] for d in deps.values()):,} hab., "
      f"{sum(d['alertes'] for d in deps.values())} alertes mobiles rattachées")
print("Contrôle Lambert-93 -> WGS84 (Paris ~ 2.35, 48.85) :", l93_to_wgs84(652469, 6862035))
