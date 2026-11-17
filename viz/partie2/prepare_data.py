"""Partie 2 : délais de mise en service des sites DCC vs promesse des 24 mois.

Principe : chaque site garde son `numero_site` d'un fichier trimestriel à l'autre.
Le premier trimestre où `sites_mes == 1` donne la période de mise en service :
entre la fin du trimestre précédent et la fin de ce trimestre.
On compare cet intervalle à la date de l'arrêté + 24 mois :
  - "a_temps"   : mis en service au plus tard à la fin du trimestre, et c'est <= 24 mois
  - "en_retard" : même au début de l'intervalle, on dépassait déjà 24 mois
  - "incertain" : l'échéance tombe dans le trimestre de mise en service
Les sites déjà en service dans le 1er fichier (2022 T1) n'ont pas de date connue.

Usage : python viz/partie2/prepare_data.py   (depuis la racine du projet)
"""
import json
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DCC = HERE.parent.parent / "data" / "dispositif_couverture_ciblee"
OUT = HERE / "data.js"
OPS = {"20801": "Orange", "20810": "SFR", "20815": "Free", "20820": "Bouygues Telecom"}
DELAI = 24  # mois


def fin_trimestre(annee, t):
    return pd.Timestamp(year=annee, month=3 * t, day=1) + pd.offsets.MonthEnd(0)


def mois(a, b):
    return (b - a).days / 30.4375


# --- 1. premier trimestre "en service" pour chaque site ---
fichiers = sorted(DCC.glob("*/*_sites.csv"))
trimestres, premier = [], {}
for i, f in enumerate(fichiers):
    a, t = map(int, re.match(r"(\d{4})_T(\d)", f.name).groups())
    trimestres.append({"label": f"{a} T{t}", "fin": fin_trimestre(a, t)})
    df = pd.read_csv(f, sep=";", dtype=str)
    for s in df.loc[df["sites_mes"] == "1", "numero_site"]:
        premier.setdefault(s, i)

# --- 2. état actuel (dernier fichier) ---
df = pd.read_csv(fichiers[-1], sep=";", dtype=str)
df["pub"] = pd.to_datetime(df["date_publication_arrete"], errors="coerce", format="mixed", dayfirst=True)
for c in ("x_lambert_93", "y_lambert_93"):
    df[c] = pd.to_numeric(df[c].str.replace(",", "."), errors="coerce")
fin_obs = trimestres[-1]["fin"]

sites = []
for r in df.itertuples():
    q = premier.get(r.numero_site)
    echeance = r.pub + pd.DateOffset(months=DELAI) if pd.notna(r.pub) else None
    s = {
        "id": r.numero_site,
        "zone": r.nom_de_la_zone if isinstance(r.nom_de_la_zone, str) else None,
        "dep": r.departement,
        "op": OPS.get(r.op_leader, "Non déterminé"),
        "arrete": r.pub.strftime("%Y-%m-%d") if pd.notna(r.pub) else None,
        "x": None if pd.isna(r.x_lambert_93) else int(r.x_lambert_93),
        "y": None if pd.isna(r.y_lambert_93) else int(r.y_lambert_93),
        "q": q,  # index du trimestre de 1re mise en service (None = pas encore)
    }
    if echeance is None:
        s["statut"] = "inconnu"
    elif q is None:  # pas encore en service
        s["attente_mois"] = round(mois(r.pub, fin_obs), 1)
        s["statut"] = "attente_retard" if fin_obs > echeance else "attente_dans_delai"
    elif q == 0:
        s["statut"] = "avant_2022"
    else:
        debut, fin = trimestres[q - 1]["fin"], trimestres[q]["fin"]
        s["delai_min"] = round(max(0, mois(r.pub, debut)), 1)
        s["delai_max"] = round(mois(r.pub, fin), 1)
        s["statut"] = "a_temps" if fin <= echeance else ("en_retard" if debut > echeance else "incertain")
    sites.append(s)

out = {
    "trimestres": [t["label"] for t in trimestres],
    "delai_promis": DELAI,
    "sites": sites,
}
OUT.write_text("window.DATA2 = " + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")

st = pd.Series([s["statut"] for s in sites]).value_counts()
print(f"OK -> {OUT} ({OUT.stat().st_size // 1024} Ko)")
print(st.to_string())
