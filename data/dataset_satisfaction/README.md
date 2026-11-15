# Dataset : Satisfaction client des opérateurs télécoms français

Extrait de : **ARCEP, Observatoire de la satisfaction client, édition 2026** (chiffres 2025)
Enquête réalisée par l'institut CSA, questionnaire en ligne, 23 septembre - 10 octobre 2025,
échantillon de 4 029 consommateurs de 18 ans et plus.
Source PDF : https://www.arcep.fr/fileadmin/cru-1769533491/user_upload/observatoire/satisfaction-client/fevrier-2026/observatoire-satisfaction-client_edition2026_fev2026.pdf

## Fichiers

### 1. satisfaction_generale.csv (58 lignes)
Note moyenne de satisfaction (0 à 10) par opérateur et par année, 2021-2025.
- `marche` : mobile | internet_fixe | consolide (mobile + fixe, publié depuis 2024)
- `operateur` : Bouygues Telecom, Free, Orange, SFR, Ensemble (moyenne marché)
- `annee` : 2021 à 2025
- `note_sur_10`

Pages sources : 9 (mobile), 61 (FAI), 116 (consolidé).

### 2. distribution_notes_2025.csv (15 lignes)
Répartition des répondants par tranche de note, mesure 2025.
- `pct_notes_9_10`, `pct_notes_6_8`, `pct_notes_0_5` : % de répondants

### 3. problemes_rencontres.csv (45 lignes)
% d'abonnés déclarant avoir rencontré un problème au cours des 12 derniers mois.
- `type_probleme` : au_moins_un_probleme, fraudes_appels_indesirables, qualite_de_service,
  surfacturation_contractuel, souscription, autres, et pour le fixe les déclinaisons
  fibre / ADSL
- `pct_2025` : mesure 2025
- `pct_2024` : mesure 2024 quand publiée dans le rapport (vide sinon)

Pages sources : 14-17 (mobile), 64-72 (FAI).

### 4. service_client_mobile_2025.csv (16 lignes)
Satisfaction détaillée du service client mobile par critère (note sur 10), mesure 2025.
Base : abonnés ayant contacté leur service client suite à un problème.
- `critere` : accueil, attente_disponibilite, continuite_parcours, pertinence_reponses

Page source : 35.

## Notes méthodologiques
- Les données sont des agrégats nationaux déclaratifs (sondage), pas des mesures techniques.
- "Ensemble" = moyenne de l'ensemble des opérateurs du marché.
- Les chiffres ont été relevés manuellement depuis les graphiques du rapport PDF
  (vérifiés visuellement page par page) ; précision : celle affichée dans le rapport.
- Pour les mesures techniques (débits, couverture), croiser avec les données
  ARCEP "Mon Réseau Mobile" et ANFR (open data).

## Licence
Données publiques ARCEP. Mentionner la source dans toute réutilisation :
"ARCEP, Observatoire de la satisfaction client, édition 2026 (enquête CSA)".
