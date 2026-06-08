---
description: Principes de modélisation numérique dans l'ingénierie des ressources en eau, couvrant les équations Navier-Stokes, la sélection des modèles 1D/2D/3D, la configuration des mailles, l'étalonnage et les pièges communs de modélisation.
---

# Principes

```{admonition} Theory chapter under development
:class: tip

Nous travaillons sur une section théorique plus exhaustive sur la modélisation numérique des rivières et des réservoirs. D'ici là, veuillez utiliser notre {ref}`glossary` pour des explications détaillées de termes techniques qui pourraient ne pas être claires.
```

Les modèles numériques dans l'ingénierie des ressources en eau approximativement le mouvement des fluides à travers les solutions itératives de {term}`Navier-Stokes equations` et leur approximation statistique avec les équations {term}`Reynolds-averaged Navier-Stokes <RANS>`. Le rôle des modèles numériques devient de plus en plus important lorsqu'on peut distinguer les modèles en fonction de leurs hypothèses de simplification (p. ex. pour les dimensions ou les caractéristiques des fluides). Les modèles purement hydrodynamiques simulent le mouvement de l'eau et ont une grande précision pour simuler les phénomènes d'écoulement, mais des défis majeurs demeurent pour la modélisation morphodynamique. Alors que la modélisation unidimensionnelle (**1d** moyenne de section) est lentement abandonnée pour son incapacité à tenir compte des phénomènes d'écoulement complexes dans les rivières naturelles, les modèles bidimensionnels (**2d**) et tridimensionnels (**3d**) deviennent de plus en plus populaires. Néanmoins, les choix de modèles et la compréhension des modèles numériques posent des défis. Dans ce contexte, {cite:t}`mosselman_five_2016` souligne cinq problèmes communs et généralisés dans la création et l'interprétation de modèles numériques. Ces cinq erreurs sont:

1. Préparation : Les modèles unidimensionnels (1d), bidimensionnels (2d) et tridimensionnels (3d) nécessitent des données d'entrée similaires (série de flux, relation étape-décharge, rugosité, modèle d'élévation numérique, tailles de grain). Ce qui varie, c'est le calcul (3d > 2d > 1d) et l'étalonnage (1d > 2d > 3d).
2. Configuration de la grille : Les limites du modèle doivent être suffisamment éloignées de la zone d'intérêt. Une limite d'entrée ne devrait être que le long du lit de rivière mouillé en permanence et les 1 à 2 % le plus en amont du lit de chenal modélisé devraient avoir une contrainte non-érosive attribuée aux cellules. Dans le cas contraire, le modèle peut être instable en raison de la vitesse et des taux d'érosion localement très élevés près de la limite d'entrée.
3. Configuration du modèle: Lisez et comprenez comment les fermetures de turbulence sont mises en œuvre dans le modèle pour définir de façon réaliste les paramètres du modèle utilisés pour la fermeture de turbulence et produire un modèle stable.
4. Validation/post-traitement des modèles: Mauvaise confiance dans les modèles numériques mal validés: Chaque modèle nécessite des données de validation, ce qui implique un travail sur le terrain épuisant et à forte intensité de main-d'oeuvre.
5. Interprétation du modèle : La direction du transport des sédiments et des vecteurs d'écoulement de l'eau diffère principalement.

Ce chapitre présente des logiciels open-access et open-source avec de nombreux tutoriels sur les données pré-traitement (geo) spatialement explicites, la mise en place de fichiers de contrôle de modèles, les modèles d'exécution et post-traitement. Des tutoriels sont disponibles dans ce livre électronique pour les logiciels suivants:

* **BASEMENT (accès libre)**<br> Le tutoriel {ref}`chpt-basement` introduit la modélisation hydrodynamique 2d avec le modèle numérique de Zurich (Suisse) *BASEMENT* 3.x, qui a été principalement développé avec des tests de référence sur **les rivières et cours d'eau de montagne**.
* **TELEMAC (open source)**<br>Open TELEMAC-MASCARET est une suite logicielle puissante pour une grande variété de **rivières, lacs et même deltas de l'océan**.
  * Obtenez un aperçu des fichiers et des options de modèle dans la section {ref}`TELEMAC introduction <chpt-telemac>`.
  * Le tutoriel {ref}`chpt-telemac2d` introduit la modélisation hydrodynamique 2d avec des fichiers de géométrie standard *SLF* (selafin).
  * Le tutoriel {ref}`chpt-telemac3d` introduit la modélisation hydrodynamique 3d (didacticiel exploratoire).
* **OpenFOAM** représente un autre outil de modélisation puissant, qui ** est recommandé pour modéliser les interactions flow-structure**, et ce livre électronique fournit une introduction de base par [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/) dans le {ref}`OpenFOAM section <chpt-openfoam>`. De plus, le tutoriel du développeur d'OpenFOAM [3 semaines](https://wiki.openfoam.com/index.php?title=%223_weeks%22_series) est un bon début dans la modélisation d'OpenFOAM pour les doctorants ou les ingénieurs. Sur {ref}`Debian Linux / Ubuntu / Mint <linux-install>`, de préférence installer OpenFOAM à partir du [Ubuntu depositary](https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian#ubuntu).

(calibration)=
## Étalonnage et validation

Un modèle numérique peut fournir de bonnes données, ce qui n'est pas significatif à moins qu'un modèle ne soit étalonné et validé. Il y a trois possibilités de le faire.

1. L'étalonnage numérique évalue la stabilité de la simulation elle-même. Les paramètres concernés sont par exemple l'état {term}`CFL` (Courant-Friedrichs-Lewy) ou d'autres paramètres hydrauliques. Un étalonnage numérique peut prendre du temps et nécessite des connaissances spécialisées pour juger de la validité des paramètres.
1. Étalonnage hydraulique (et validation), qui compare les niveaux de surface d'eau modélisés, les vitesses d'écoulement ou la contrainte de cisaillement du lit avec les données d'observation.
1. L'étalonnage et la validation morphologiques comparent les taux de changement de terrain simulés avec ceux observés (sans objet ici parce qu'ils n'ont pas été appliqués dans le modèle).

```{admonition} The Difference between Calibration and Validation
**La calibration** est l'adaptation itérative d'une simulation à la réalité en utilisant des données de mesure (observation) dans le but de minimiser l'erreur entre les résultats modélisés et observés. **Validation** n'évalue que la bonté (ou l'erreur) du modèle sans l'adapter lui-même.
```

Ce livre électronique fournit des conseils pour l'étalonnage des modèles (paramètres) dans les sections TELEMAC sur {ref}`hydrodynamics <tm2d-calibration>` et {ref}`morphodynamics <gaia-calibration>`.

## Que faire avec les résultats du modèle numérique?

Une fois le modèle étalonné, il peut être utilisé pour simuler des hydrographies d'inondation afin d'évaluer la stabilité des caractéristiques de l'ingénierie fluviale et du paysage fluvial ou de la zone d'inondation. De plus, la qualité de l'habitat des espèces de poissons ciblées](https://pubs.er.usgs.gov/publication/70121265) peut être évaluée, par exemple, en fonction de la profondeur de l'eau, de la vitesse du débit et de la taille du grain (et d'autres paramètres). Il existe même des logiciels spéciaux pour exécuter ces tâches, comme [CASiMiR](http://www.casimir-software.de/ENG/index_eng.html) (commercial) ou [River Architect](https://riverarchitect.github.io).
