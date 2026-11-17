# Promesses réseau

Les réseaux mobiles en France sur les 5 dernières années : ce que les opérateurs ont promis, ce qu'ils ont livré, et ce qu'en pensent les utilisateurs.

Le fil rouge est le **New Deal mobile (2018)** : à travers le *Dispositif de couverture ciblée* (DCC), l'État désigne par arrêté des zones à couvrir, et les opérateurs ont **24 mois** pour y mettre un site en service. Les données permettent de vérifier si cette promesse est tenue, et de la confronter aux signalements et à la satisfaction des clients.

## Lancer les visualisations

Les pages sont statiques : il suffit d'ouvrir le fichier `index.html` dans un navigateur (double-clic, pas besoin de serveur). Une connexion internet est nécessaire pour charger D3.js depuis le CDN.

| Page | Contenu |
|---|---|
| [`viz/index.html`](viz/index.html) | **Partie 1, premier coup d'œil** : évolution du DCC, cartes des sites et des alertes, satisfaction, problèmes rencontrés, signalements J'alerte |
| [`viz/partie2/index.html`](viz/partie2/index.html) | **Partie 2, la promesse des 24 mois est-elle tenue ?** : délais réels de mise en service, sites en attente, animation du déploiement trimestre par trimestre |
| [`viz/partie3/index.html`](viz/partie3/index.html) | **Partie 3, département par département** : carte cliquable avec zoom, nuage alertes / sites, détail du département sélectionné |

Si les données changent, régénérer le fichier `data.js` de chaque partie (depuis la racine du projet) :

```bash
python viz/prepare_data.py
python viz/partie2/prepare_data.py
python viz/partie3/prepare_data.py
```

Dépendances Python : `pandas` et `matplotlib` (utilisé seulement pour les tests point-dans-polygone de la partie 3).

## Architecture

Le projet suit une architecture en 2 étages :

1. **Préparation des données (Python / pandas, hors ligne)** : chaque `prepare_data.py` lit les CSV bruts de `data/`, nettoie, croise et agrège, puis exporte un `data.js` compact (`window.DATA = {...}`) que la page charge directement.
2. **Visualisation (D3.js v7)** : une page HTML autonome par partie, avec infobulles au survol, filtres et vues liées.

Le parcours suit le principe de Shneiderman, *« Overview first, zoom and filter, then details on demand »* : vue nationale, puis filtre par opérateur et par département, puis détail site par site.

```
data/
  dispositif_couverture_ciblee/   relevés trimestriels DCC 2022 T1 → 2026 T2 (sites + points d'intérêt)
  jalerte_opendata_bilanannuel/   bilans annuels J'alerte l'Arcep 2022 → 2025
  dataset_satisfaction/           observatoire de la satisfaction client (Arcep / CSA, édition 2026)
viz/
  index.html, prepare_data.py     partie 1
  partie2/                        partie 2
  partie3/                        partie 3
    geo/                          contours des départements + population des communes
```

## Données

| Source | Contenu | Granularité |
|---|---|---|
| [Arcep, Dispositif de couverture ciblée](https://www.arcep.fr/cartes-et-donnees/suivi-du-new-deal-mobile.html) | Sites demandés par arrêté, statut de déploiement, opérateur leader, coordonnées (Lambert-93) | Trimestrielle, par site. Voir [`documentation_dcc.md`](data/dispositif_couverture_ciblee/documentation_dcc.md) |
| Arcep, J'alerte l'Arcep (bilans annuels) | Signalements des utilisateurs par marché, thème, et sur une maille hexagonale | Annuelle |
| Arcep / CSA, Observatoire de la satisfaction client | Notes de satisfaction par opérateur, problèmes rencontrés | Annuelle. Voir [`README`](data/dataset_satisfaction/README.md) |
| [france-geojson](https://github.com/gregoiredavid/france-geojson) | Contours simplifiés des départements | `viz/partie3/geo/` |
| [geo.api.gouv.fr](https://geo.api.gouv.fr/communes?fields=codeDepartement,population&format=json) | Population des communes, sommée par département | `viz/partie3/geo/` |

## Premiers résultats

- **5 352 sites** demandés au titre du DCC au 2026 T2, dont **83 %** en service.
- Parmi les 3 173 sites mis en service depuis 2022 T2 : **39 % livrés en retard** de façon certaine, 27 % à temps, 34 % incertains (date connue au trimestre près).
- Le délai médian est de **24 mois** : une grande partie des sites est livrée juste au moment de l'échéance.
- **252 sites** ne sont toujours pas en service alors que les 24 mois sont dépassés, certains depuis **78 mois**.
- Les quatre opérateurs sont proches : de 37 % (Bouygues Telecom) à 41 % (SFR) de sites livrés en retard.
- Les alertes mobiles J'alerte ont fortement augmenté en 2025 (7 430, contre 5 915 en 2024), portées par le thème « déploiement des réseaux ».

## Méthode et limites

- **Date de mise en service** : chaque site garde son `numero_site` d'un relevé trimestriel à l'autre. Le premier relevé où `sites_mes = 1` donne le trimestre de mise en service.
- **À temps / incertain / en retard** : on compare ce trimestre à la date de l'arrêté + 24 mois. *À temps* si même la fin du trimestre reste sous l'échéance, *en retard* si même son début la dépasse, *incertain* sinon.
- Les **1 284 sites déjà en service en 2022 T1** n'ont pas de date connue : ils sont exclus des délais.
- Les 24 mois sont comptés depuis la publication de l'arrêté ; d'éventuels **reports** accordés aux opérateurs ne sont pas pris en compte.
- Les **sites non livrés n'ont pas de coordonnées** publiées : ils n'apparaissent pas sur les cartes, seulement dans les tableaux et les comptages.
- **Alertes par département** : 6 389 alertes mobiles sont localisées sur les 7 430 du bilan 2025, dont 5 903 rattachées à un département (selon le centre de chaque hexagone).
- Conversion **Lambert-93 → WGS84** réalisée dans le script (formules IGN), sans dépendance externe.

## Feuille de route

### Idées principales
- [x] Couverture ciblée vs réelle : nombre de sites installés (parties 1 à 3)
- [x] Satisfaction des clients : profil des plaintes, signalements J'alerte (partie 1)
- [x] Promesses tenues ou non : délais de mise en service vs 24 mois (parties 2 et 3)
- [ ] Qualité du réseau dans le temps (campagnes de mesures de l'Arcep)
- [ ] Temps de réparation des lignes
- [ ] Causes des incidents

### Prochaines étapes envisagées
- [ ] Antennes ANFR (2017 → 2026) : course à la 4G/5G par opérateur, animation du déploiement
- [ ] Couverture théorique vs réelle de la 4G/5G (cartes « Mon réseau mobile » vs mesures)
- [ ] Zones blanches / grises
- [ ] Population INSEE au niveau commune pour un zoom plus fin

### Autres idées à incorporer ou non
- Course au déploiement de la 5G
- Conséquences du New Deal de 2018
- Expériences personnelles
- Achat de cartes SIM
- ADSL et fibre
