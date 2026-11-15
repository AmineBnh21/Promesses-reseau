Architecture en 2 étages :

Étage 1 : pipeline de préparation (Python/pandas, hors ligne)

Tu télécharges TOUS les snapshots ANFR (2017→2026, un par trimestre ou par mois), tous les fichiers ARCEP, tous les bilans J’alerte
Tu nettoies et tu croises tout dans un notebook
Tu exportes des fichiers optimisés pour le site (JSON/CSV par niveau de zoom)

Ça, c’est un vrai travail de data engineering, et c’est valorisé dans le barème « réalisation technique ». Rien n’est perdu : toutes les analyses se font sur les données complètes.

Étage 2 : la visu D3 avec drill-down (exploration à plusieurs niveaux)

Niveau France : évolution 2017→2026 par opérateur (courbes, bump chart) ; données agrégées mais calculées sur tout
Niveau département : clic sur la carte → détail du département, évolution locale, comparaison des 4 opérateurs
Niveau commune/site : zoom → les antennes individuelles s’affichent (position, techno, date de mise en service). Là tu montres la donnée brute, mais seulement celle de la zone visible

C’est exactement le principe « Overview first, zoom and filter, details on demand » (Shneiderman), la règle d’or qu’on attend dans un cours de dataviz. Le jury adorera que tu la cites.

Pourquoi ça ne dégrade rien :

La carte des ~110 000 sites complets peut s’afficher en entier avec du canvas ou un hexbin (regroupement hexagonal) : visuellement riche, performant
La timeline utilise tous les snapshots : tu peux faire une animation du déploiement 2017→2026, site par site qui s’allume sur la carte. C’est spectaculaire en soutenance et ça utilise 100 % des données
Les signalements et la satisfaction restent annuels parce que c’est leur granularité native, pas une réduction de ta part

Le seul vrai arbitrage : charger 10 ans × 110 000 sites d’un coup dans le navigateur (~500 Mo) ne marchera pas. Donc tu découpes en fichiers par année ou par département, chargés à la demande. L’utilisateur a accès à tout, jamais tout en même temps. C’est invisible pour lui et c’est ce que fait n’importe quel site pro (y compris monreseaumobile.arcep.fr).