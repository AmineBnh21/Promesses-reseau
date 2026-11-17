"""Agrège les CSV de data/ en un seul fichier viz/data.js (window.DATA = {...}).

Usage : python viz/prepare_data.py   (depuis la racine du projet)
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = Path(__file__).resolve().parent / "data.js"

OPS = {"20801": "Orange", "20810": "SFR", "20815": "Free", "20820": "Bouygues Telecom"}


def read_jalerte(name):
    path = DATA / "jalerte_opendata_bilanannuel" / name
    for enc in ("utf-8", "cp1252"):
        try:
            df = pd.read_csv(path, sep=";", encoding=enc)
            break
        except UnicodeDecodeError:
            continue
    df.columns = [c.strip() for c in df.columns]
    return df


# ---------- DCC : évolution trimestrielle ----------
dcc_timeline = []
last_sites = None
for f in sorted((DATA / "dispositif_couverture_ciblee").glob("*/*_sites.csv")):
    m = re.match(r"(\d{4})_T(\d)", f.name)
    df = pd.read_csv(f, sep=";", decimal=",", dtype={"insee_dep": str, "op_leader": str})
    num = lambda c: pd.to_numeric(df[c], errors="coerce").fillna(0)
    dcc_timeline.append({
        "trimestre": f"{m[1]} T{m[2]}",
        "demandes": int(num("sites_demandes").sum()),
        "mis_en_service": int(num("sites_mes").sum()),
        "a_6_mois": int(num("sites_6_mois").sum()),
        "a_6_24_mois": int(num("sites_6_24_mois").sum()),
        "attente": int(num("sites_attente_deploiement").sum()),
    })
    last_sites, last_label = df, f"{m[1]} T{m[2]}"

df = last_sites
df["statut"] = "autre"
df.loc[pd.to_numeric(df["sites_attente_deploiement"], errors="coerce") == 1, "statut"] = "attente"
df.loc[pd.to_numeric(df["sites_6_24_mois"], errors="coerce") == 1, "statut"] = "6-24 mois"
df.loc[pd.to_numeric(df["sites_6_mois"], errors="coerce") == 1, "statut"] = "< 6 mois"
df.loc[pd.to_numeric(df["sites_mes"], errors="coerce") == 1, "statut"] = "en service"
for c in ("x_lambert_93", "y_lambert_93"):
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "."), errors="coerce")
# NB : seuls les sites en service ont des coordonnées dans les fichiers ARCEP
geo = df.dropna(subset=["x_lambert_93", "y_lambert_93"])
dcc_points = [
    [int(x), int(y), d]
    for x, y, d in zip(geo["x_lambert_93"], geo["y_lambert_93"], geo["departement"])
]

dep = (
    df.groupby("departement")
    .agg(
        total=("statut", "size"),
        en_service=("statut", lambda s: int((s == "en service").sum())),
        a_venir=("statut", lambda s: int((s != "en service").sum())),
    )
    .reset_index()
    .sort_values("a_venir", ascending=False)
)
dcc_dep = dep.to_dict("records")

leader = df["op_leader"].map(OPS).fillna("Non déterminé").value_counts()
dcc_leader = [{"operateur": k, "sites": int(v)} for k, v in leader.items()]

# ---------- Satisfaction ----------
sat = pd.read_csv(DATA / "dataset_satisfaction" / "satisfaction_generale.csv")
pb = pd.read_csv(DATA / "dataset_satisfaction" / "problemes_rencontres.csv")

# ---------- J'alerte ----------
fixe_mobile = read_jalerte("2.1.0_repartition_marche_fixe_mobile_2022_2025.csv")
fixe_mobile.columns = ["annee", "fixe", "mobile"]

themes_mob = read_jalerte("2.1.2.b_repartition_theme_principal_2022_2025_mobile_grandpublic.csv")
themes_mob = themes_mob.rename(columns={themes_mob.columns[0]: "annee"})

hex_df = read_jalerte("2.1.2.a_densite_alertes_france_2025_mobile_grandpublic.csv")
# Grille hexagonale régulière (hexagones "flat-top", rayon ~8 660 m). Les hexagones
# côtiers sont découpés par le trait de côte : on recale leur barycentre sur la grille
# pour ne garder qu'un centre (x, y) par cellule, le navigateur redessine l'hexagone.
R = 8660.254
X0, Y0 = 648966.13, 6864046.0
hexes = []
for dens, pop, geom in zip(hex_df.iloc[:, 0], hex_df["Population"], hex_df["geometry"]):
    nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", geom)]
    cx, cy = sum(nums[0::2]) / len(nums[0::2]), sum(nums[1::2]) / len(nums[1::2])
    col = round((cx - X0) / (1.5 * R))
    off = 7500 if col % 2 else 0
    row = round((cy - Y0 - off) / 15000)
    hexes.append([round(X0 + col * 1.5 * R), round(Y0 + off + row * 15000), float(dens), int(pop)])

out = {
    "dcc": {
        "timeline": dcc_timeline,
        "dernier_trimestre": last_label,
        "points": dcc_points,
        "departements": dcc_dep,
        "leaders": dcc_leader,
    },
    "satisfaction": sat.to_dict("records"),
    "problemes": pb.astype(object).where(pd.notna(pb), None).to_dict("records"),
    "jalerte": {
        "fixe_mobile": fixe_mobile.to_dict("records"),
        "themes_mobile": themes_mob.to_dict("records"),
        "densite_mobile_2025": hexes,
    },
}

OUT.write_text("window.DATA = " + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size // 1024} Ko), {len(dcc_points)} sites, {len(hexes)} hexagones")
