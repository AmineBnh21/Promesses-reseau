# Dispositif de Couverture Ciblée (DCC)
---

## :bar_chart: Présentation des données

Le dispositif de couverture ciblée fait partie des obligations du *New Deal* mobile. Il a pour objectif d’assurer la couverture de 5 000 zones par chacun des quatre opérateurs : Bouygues Telecom, Free Mobile, Orange et SFR. Le ministre chargé des communications électroniques signe chaque année une ou plusieurs listes des zones à couvrir sur les conseils d’équipes projets locales travaillant pour les collectivités territoriales.

Chaque **arrêté** contient une liste de **zones à couvrir**. Les zones à couvrir sont materialisées par un ensemble de **points d'intérêt** (POI) qui devront être couverts dans un délai de 24 mois maximum par les opérateurs désignés. Pour chaque zones à couvir, un certain nombre de **sites** sont anticipés.

[Plus d'informations sur le New Deal mobile](https://www.arcep.fr/cartes-et-donnees/suivi-du-new-deal-mobile.html).

## :notebook: Descriptif des données 

### :round_pushpin: Fichier : Points d'intérêt

Ce fichier liste l'ensemble des points identifiés par les pouvoirs publics en France métropolitaine dans le cadre du dispositif de couverture ciblée. Plusieurs points peuvent appartenir à la même "zone" (`numero_zone_unique`). Les opérateurs devront construire un ou plusieurs sites pour apporter de la couverture sur la zone identifiée (`nb_sites_demandes_total_zone`).

Les coordonnées des 300 premiers points d'intérêts ne figurent pas dans les arrêtés et ont été recalculés à titre indicatif pour donner une information sur la zone à couvrir, mais ne constituent pas la zone.

Les données de points d'intérêt sont rassemblées dans un fichier global (ex : `2022_T3_dcc_Metropole_POI.csv`).

**Caractéristiques générales :**

|||
| ----------------- | ----------------------------------------------------------------- |
| Format	 		| csv 																|
| Séparateur	 	| ;							 										|
| Décimale		 	| ,							 										|
| Encodage	 		| UTF-8 															|
| Type de géométrie	| point (x;y)														|
| Système de coordonnées géographiques | RGF93 / Lambert-93 (EPSG:2154)					|
| Source			| arrêtés / opérateurs 												|

*Pour afficher les fichiers csv avec les bons accents dans le logiciel Microsoft Excel, il est possible d’exécuter l’Assistant importation de texte en remplaçant l’extension de nom de fichier `.csv` par `.txt` avant de l’ouvrir. Vous pourrez alors sélectionner l’encodage UTF-8.*

**Description des champs :**

| Nom du champ				| Description																	|  Format	|              
| ------------------------- | ----------------------------------------------------------------------------- | ----------| 
| `id_point`                | Identifiant du point d'intérêt par ordre de publication au JORF 				| Entier	|
| `num_arrete`              | Numéro de l'arrêté dans lequel le point d'intérêt à couvrir (POI) est défini	| Texte		|
| `date_publication_arrete` | Date de publication au JORF de l'arrêté dans lequel le POI est défini 		| Date ("jj/mm/aaaa")		|
| `id_dossier`              | Numéro de dossier unique auquel le POI est rattaché, correspondant à une zone à couvrir par un ou plusieurs sites par les mêmes opérateurs | Entier | 
| `nom_dossier`             | Nom du dossier unique auquel le POI est rattaché, correspondant à une zone à couvrir par un ou plusieurs sites par les mêmes opérateurs | Texte | 
| `nb_sites_dossier`        | Nombre de sites nécessaires pour couvrir l'ensemble des POI du dossier		| Texte		|
| `code_insee`              | Code INSEE de la commune où se trouve le POI (Code Officiel Géographique de l'année courante)				| Texte 	|
| `nom_commune`             | Nom de la commune dans laquelle se situe le POI (Code Officiel Géographique de l'année courante)			| Texte		|
| `departement`             | Nom du département dans lequel se situe le POI (Code Officiel Géographique de l'année courante) 			| Texte		|
| `insee_dep`               | Code INSEE du département dans lequel se trouve le POI (Code Officiel Géographique de l'année courante) 	| Texte		|
| `region`                  | Nom de la région dans laquelle se trouve le POI (Code Officiel Géographique de l'année courante) 			| Texte		|
| `x_lambert_93`            | Coordonnée x du point dans le système de projection en vigueur 				| Décimal	|
| `y_lambert_93`            | Coordonnée y du point dans le système de projection en vigueur 				| Décimal	|
| `20801`                   | `1` si l'opérateur Orange est désigné pour couvrir ce point, `0` sinon		| Booléen 	|
| `20810`                   | `1` si l'opérateur SFR est désigné pour couvrir ce point, `0` sinon 			| Booléen 	|
| `20815`                   | `1` si l'opérateur Free Mobile est désigné pour couvrir ce point, `0` sinon	| Booléen 	|
| `20820`                   | `1` si l'opérateur Bouygues Telecom est désigné pour couvrir ce point, `0` sinon| Booléen 	|
| `origine_zone`            | Identifiant de la zone figurant dans l'arrêté (ou nom de l'ancien programme si bascule du POI dans le DCC) | Texte	|
| `origine_coordonnes`      | Selon les arrêtés, les coordonnées géographiques des POI peuvent figurer dans les arrêtés (arrete) ou ont été définies par l'Arcep quand elles ne figurent pas dans les arretes, au niveau du chef-lieu de la commune ('Arcep chef-lieu') ou d'un autre lieu de peuplement ('Arcep autre') | Texte
| `num_zone_arrete`         | Identifiant de la zone arrêtée et dans laquelle se situe le POI				| Entier	|
| `nom_point_arrete`        | Nom du point arrêté (si disponible)											| Texte		|
| `identifiant_site`        | Identifiant du site figurant dans l'arrêté et devant permettre la couverture du POI (si disponible)| Texte |
| `lien_arrete`             | Lien vers l'arrêté publié au JORF 											| Texte		|

**Emprise :**

France métropolitaine.

### :tokyo_tower: Fichier : Sites

Ce fichier liste l'ensemble des sites permettant la couverture des zones identifiées par les pouvoirs publics en France métropolitaine dans le cadre du dispositif de couverture ciblée. Afin de faciliter le retraitement des données, les services de l'Arcep ont attribué un numéro unique à chacun des sites (`numero_site`). Plusieurs sites peuvent appartenir à une même zone identifiée par les pouvoirs publics (`nom_de_la_zone`). Lorsque les emplacements des sites sont identifiés, leur nom, ainsi que leurs coordonnées géographiques sont renseignés.

Les données de sites sont distribuées dans un fichier global (ex : `2022_T3_dcc_Metropole_sites.csv`).
-
**Caractéristiques générales :**

|||
| ----------------- | ----------------------------------------------------------------- |
| Format	 		| csv 																|
| Séparateur	 	| ;							 										|
| Décimale		 	| ,							 										|
| Encodage	 		| UTF-8 															|
| Type de géométrie	| point (x;y)														|
| Système de coordonnées géographiques | RGF93 / Lambert-93 (EPSG:2154)					|
| Source			| arrêtés / opérateurs 												|

**Sites et sites physiques :**

La colonne `site physique` indique si le site nécessite un nouveau point haut ('1') ou, dans le cas où d'autres opérateurs ont déjà été nommés préalablement dans le dispositif de couverture ciblée, si le site peut être mutualisé avec les sites existants ('0') dans le cadre du DCC - le numéro du site mutualisé est indiqué dans la colonne `numero_site_physique`. Pour avoir le nombre total de sites mis en service : filtrer les données sur `sites_mes=1` et `site physique=1`.
Pour obtenir le nombre de site mis en service par opérateur : filtrer les données sur `sites_mes=1` et comptabiliser les données de la colonne de chaque opérateur.

**Description des champs :**

| Nom du champ				  | Description																		|  Format	|              
| --------------------------- | ------------------------------------------------------------------------------- | --------- | 
| `num_arrete`                | Numéro de l'arrêté dans lequel le site est demandé 								| Texte		|				
| `date_publication_arrete`   | Date de publication au JORF de l'arrêté dans lequel le site est défini 			| Date ("jj/mm/aaaa")|
| `numero_site`			      | Identifiant unique du site														| Entier	|
| `nom_site_operateurs`       | Identifiant unique désignant le site s'il est partagé par plusieurs opérateurs 	| Texte		|
| `site_physique`             |`1` si le site est demandé pour la première fois dans un arrêté, `0` si le site a déjà été demandé dans un arrêté précédent | Booléen |
| `numero_site_physique`      | Identificant unique désigant le site physique									| Entier	|
| `nom_site_arrete`           | Nom du site figurant dans l'arrêté 												| Texte		|
| `id_dossier`                | Numéro de dossier unique auquel le site est rattaché, correspondant à une zone à couvrir par un ou plusieurs sites par les mêmes opérateurs | Entier |
| `nom_de_la_zone`            | Nom de la zone à couvrir par un ou plusieurs sites 								| Texte		|
| `region`                    | Nom de la région dans laquelle se situe la zone à couvrir (Code Officiel Géographique de l'année courante)			| Texte 	|
| `departement`               | Nom du département dans lequel se situe la zone à couvrir (Code Officiel Géographique de l'année courante) 			| Texte 	|
| `insee_dep`                 | Code INSEE du département dans lequel se situe la zone à couvrir (Code Officiel Géographique de l'année courante)	| Texte 	|
| `x_lambert_93`              | Coordonnée x du point dans le système de projection en vigueur					| Décimal 	|
| `y_lambert_93`              | Coordonnée y du point dans le système de projection en vigueur					| Décimal 	|
| `20801`                     | `1` si l'opérateur Orange est désigné pour couvrir la zone, `0` sinon    		| Booléen	|
| `20810`                     | `1` si l'opérateur SFR est désigné pour couvrir la zone, `0` sinon   			| Booléen	|
| `20815`                     | `1` si l'opérateur Free Mobile est désigné pour couvrir la zone, `0` sinon   	| Booléen	|
| `20820`                     | `1` si l'opérateur Bouygues Telecom est désigné pour couvrir la zone, `0` sinon | Booléen	|
| `op_leader`                 | Identifiant (MCC MNC) de l'opérateur leader sur le site ou `0` si l'opérateur leader n'a pas encore été déterminée | Texte 	|
| `sites_demandes`            | `1` si le site figure dans l'arrêté, `0` sinon									| Booléen	|
| `sites_mes`                 | `1` si le site est mis en service, `0` sinon 									| Booléen	|
| `sites_6_mois`              | `1` si le site est à déployer dans les six mois, `0` sinon						| Booléen	|
| `sites_6_24_mois`           | `1` si le site est à déployer entre six et vingt-quatre mois, `0` sinon 		| Booléen	|
| `sites_attente_deploiement` | `1` si le site est un autre site en attente de déploiement, `0` sinon			| Booléen	|
| `origine_zone`              | Identifiant de la zone figurant dans l'arrêté (ou nom de l'ancien programme si bascule du site dans le DCC)			| Texte 	|
| `num_zone_arrete`           | Identifiant de la zone arrêtée et dans laquelle se situe le site  				| Entier	|


Les champs `sites_mes`, `sites_6_mois`, `sites_6_24_mois`, et `sites_attente_deploiement` sont mutuellement exclusifs.

Certains sites sont partagés par plusieurs départements : dans ce cas, les champs `region`, `departement` et `insee_dep` contienne les noms ou codes de chaque territoire concerné séparés par " / ".

**Emprise :**

France métropolitaine.

### Liste des arrêtés publiés sur Legifrance

+ [**Arrêté du 4 juillet 2018** définissant la liste des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2018 (id : JORFTEXT000037161874)](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000037161874)
+ [**Arrêté du 21 décembre 2018** définissant la liste complémentaire des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2018 (id : JORFTEXT000037852630)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037852630)
+ [**Arrêté du 21 mars 2019** définissant la première liste des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2019 (id : JORFTEXT00003825776)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000038257761)
+ [**Arrêté du 12 juillet 2019** définissant la deuxième liste des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2019 (id : JORFTEXT000038777456)](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000038777456)
+ [**Arrêté du 23 décembre 2019** définissant la troisième liste des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2019 (id : JORFTEXT000039684846)](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000039684846)
+ [**Arrêté du 23 décembre 2019** définissant la quatrième liste des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2019 (id : JORFTEXT000039682947)](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000039682947)
+ [**Arrêté du 27 mai 2020** définissant la première liste des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2020 (id : JORFTEXT000041939050)](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000041939050)
+ [**Arrêté du 21 août 2020** définissant la deuxième liste des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2020 (id : JORFTEXT000042271635)](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000042271635)
+ [**Arrêté du 1er octobre 2020** modifiant les listes des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour les années 2018 et 2019 (id : JORFTEXT000042407499)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042407499)
+ [**Arrêté du 1er octobre 2020** définissant une liste complémentaire de nouvelles zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2020 (id : JORFTEXT000042407491)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042407491)
+ [**Arrêté du 17 décembre 2020** définissant la troisième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2020 (id : JORFTEXT000042738867)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042738867)
+ [**Arrêté du 17 décembre 2020** définissant la première liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2021 (id : JORFTEXT000042738859)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000042738859)
+ [**Arrêté du 9 avril 2021** définissant la deuxième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2021 (id : JORFTEXT000043386176)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043386176)
+ [**Arrêté du 27 septembre 2021** modifiant les listes des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour les années 2018, 2019, 2020 et 2021 (id : JORFTEXT000044162896)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044162896)
+ [**Arrêté du 27 septembre 2021** définissant une liste complémentaire de nouvelles zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2021 (id : JORFTEXT000044162888)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044162888)
+ [**Arrêté du 21 décembre 2021** définissant la troisième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2021 (id : JORFTEXT000044813553)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000044813553)
+ [**Arrêté du 1er février 2022** définissant la première liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2022 (id : JORFTEXT000045174650)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045174650)
+ [**Arrêté du 21 juin 2022** définissant la deuxième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2022 (id : JORFTEXT000045963073)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045963073)
+ [**Arrêté du 24 octobre 2022** modifiant les listes des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour les années 2018, 2019, 2020, 2021 et 2022 (id : JORFTEXT000046496400)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046496400)
+ [**Arrêté du 24 octobre 2022** définissant une liste complémentaire de nouvelles zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2022 (id : JORFTEXT000046496419)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046496419)
+ [**Arrêté du 23 décembre 2022** définissant la troisième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2022 (id : JORFTEXT000046836685)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046836685)
+ [**Arrêté du 23 décembre 2022** définissant la première liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2023 (id : JORFTEXT000046836677)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000046836677)
+ [**Arrêté du 31 juillet 2023** définissant la deuxième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2023 (id : JORFTEXT000047931261)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000047931261)
+ [**Arrêté du 28 novembre 2023** modifiant les listes des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour les années 2018, 2019, 2020, 2021, 2022 et 2023 (id : JORFTEXT000048571774)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000048571774)
+ [**Arrêté du 28 novembre 2023** définissant une liste complémentaire de nouvelles zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2023 (id : JORFTEXT000048571794)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000048571794)
+ [**Arrêté du 26 décembre 2023** définissant la troisième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2023 (id : JORFTEXT000048706412)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000048706412)
+ [**Arrêté du 27 juin 2024** définissant la deuxième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2024 (id : JORFTEXT000049989616)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000049989616)
+ [**Arrêté du 20 novembre 2024** modifiant les listes des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour les années 2018, 2019, 2020, 2021, 2022, 2023 et 2024 (id : JORFTEXT000050667916)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000050667916)
+ [**Arrêté du 23 décembre 2024** définissant la troisième liste de zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2024 (id : JORFTEXT000050822812)](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000050822812)
+ [**Arrêté du 3 février 2026** définissant une liste de nouvelles zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2026 (id : JORFTEXT000053465032)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053465032)
+ [**Arrêté du 25 mars 2026** définissant une liste complémentaire de nouvelles zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour l'année 2026 (id : JORFTEXT000053734214)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053734214)
+ [**Arrêté du 25 mars 2026** modifiant les listes des zones à couvrir par les opérateurs de radiocommunications mobiles au titre du dispositif de couverture ciblée pour les années 2019, 2020, 2021, 2022, 2023 et 2024 (id JORFTEXT000053734132)](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053734132)



## :card_file_box: Organisation des publications

### :palm_tree: Arborescence 

Les fichiers de données sont rangés par trimestre de publication :
```
📂dispositif_couverture_ciblee
 ┣ 📂2022_T2
 ┣ 📂2022_T3
 ┃ ┣ 📜2022_T2_dcc_Metropole_POI.csv
 ┃ ┣ 📜2022_T2_dcc_Metropole_sites.csv
 ┣ 📂...
 ┣ 📂last
 ┗ 📜documentation_dcc.md
 ```

### :running_man: Fréquences de publication

| Nom du fichier                         | Fréquence de publication    		  |
| -------------------------------------- | ---------------------------------- |
| XXXX_TX_dcc_POI                        | Trimestrielle (T1,T2,T3,T4)        |
| XXXX_TX_dcc_sites                      | Trimestrielle (T1,T2,T3,T4)        |


