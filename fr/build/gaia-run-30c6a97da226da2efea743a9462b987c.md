---
description: Guide pour l'exécution des simulations morphodynamiques TELEMAC-GAIA et l'analyse des résultats du transport des sédiments, y compris la charge en lit, la charge en suspension et les sorties d'évolution du lit.
---

(gaia-run)=
# Cours et analyse

## Cours Gaia

Assurez-vous que le dossier de simulation (par exemple `/gaia2d-tutorial/`) contient au moins les fichiers suivants (ou similaires, selon le cas de simulation) :

* Un maillage informatique, par exemple, sous la forme de [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* Un fichier de définitions des limites hydrodynamiques, par exemple, sous la forme de [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* Une définition des limites Gaia, par exemple, sous la forme de [boundarys-gaia.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries-gaia.cli).
* A results file of a Telemac2d/3d simulation for a hotstart initialization, for example, for 35 m$^3$/s in the form of [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) (result of the {ref}`dry-initialized steady run <tm2d-init-dry>` ending at `t=15000`).
* Un fichier de direction Telemac2d, comme [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* Un fichier de direction Gaia, comme [gaia-morphodynamique.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).

````{dropdown} Expand to review the Gaia steering file **gaia-morphodynamics.cas**
```fortran
/------------------------------------------------------------------/
/ Gaia in TELEMAC
/ GAIA STEERING FILE
/ file name: gaia-morphodynamics.cas
/
/------------------------------------------------------------------/
/                    COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE : qgismesh.slf
RESULTS FILE : rGaia-steady2d.slf
VARIABLES FOR GRAPHIC PRINTOUTS : B,E,M,MU,N,P,QSBL,TOB
MASS-BALANCE : YES
/
/ NUMERICAL OPTIONS
/------------------------------------------------------------------/
FINITE VOLUMES : NO
/------------------------------------------------------------------/
/
/------------------------------------------------------------------/
/ RIVERBED COMPOSITION
/------------------------------------------------------------------/
/
/ SEDIMENT
CLASSES TYPE OF SEDIMENT : NCO;NCO;NCO / CO-cohesive or NCO-non-cohesive
CLASSES SEDIMENT DIAMETERS : 0.0005;0.02;0.1 / in m
CLASSES SEDIMENT DENSITY : 2680;2680;2680 / in kg per m3
/
/ RIVERBED LAYERS - manual section 3.2.1
ACTIVE LAYER THICKNESS : 0.3 / multiple of D90 - default is 10000
NUMBER OF LAYERS FOR INITIAL STRATIFICATION : 3 / default is 1
LAYERS INITIAL THICKNESS : 1.5 / m - default is 100
/
/------------------------------------------------------------------/
/ BEDLOAD
/------------------------------------------------------------------/
/
/ BOUNDARIES
PRESCRIBED SOLID DISCHARGES : 10.;0.
/
BED LOAD FOR ALL SANDS : YES / deactivate with NO
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1 / MPM - see table for more
CLASSES SHIELDS PARAMETERS : 0.047;0.047;0.047
MPM COEFFICIENT : 8
/
/ BEDLOAD DIRECTION - manual sec. 3.1.4-3.1.7
SLOPE EFFECT : YES / default is YES - set to NO to disable
FORMULA FOR DEVIATION : 1 / use 2 for talmon-1995 approach
FORMULA FOR SLOPE EFFECT : 1 / default is 1 (koch-flokstra) change to 2 for soulsby
BETA : 1.3 / only with koch-flokstra - default is 1.3
/
/ SECONDARY CURRENTS - manual sec. 3.1.7
SECONDARY CURRENTS : YES / default is NO
SECONDARY CURRENTS ALPHA COEFFICIENT : 0.8 / default is 1.
/
/ FRICTION
SKIN FRICTION CORRECTION : 1 / set 0 to disable correction in shallow waters
RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER : 3. / default is 3.
/
/------------------------------------------------------------------/
/ SUSPENDED LOAD
/------------------------------------------------------------------/
/
SUSPENSION FOR ALL SANDS : YES / deactivate with NO
/
SUSPENSION TRANSPORT FORMULA FOR ALL SANDS : 1
/
/ NUMERICAL PARAMETERS
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14
/
/ ADDITIONAL SEDIMENT - manual section 4.2
CLASSES SETTLING VELOCITIES : -9;-9;-9 / use Gaia defaults
CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION : 1000;1000;1000 / N per m2
LAYERS PARTHENIADES CONSTANT : 1.E-03 / in kg per m2 per s - default is 1.E-03
```
````

Avec ces fichiers disponibles, ouvrez *Terminal*, allez dans le dossier de configuration TELEMAC (p. ex. `~/telemac/v9.0.0/configs/`), et chargez l'environnement (p. ex. `pysource.openmpi.sh` - utilisez la même chose que pour compiler TELEMAC).

```
cd ~/telemac/v9.0.0/configs
source pysource.openmpi.sh
```

```{admonition} Environment loading varies by installation
:class: note, dropdown

La commande exacte pour charger l'environnement TELEMAC dépend de votre configuration d'installation. Les variations courantes sont les suivantes :

* **Installation standard**: `source pysource.openmpi.sh` ou `source pysource.gfortran.sh`
* **Intel compilers**: `source pysource.intel.sh`
* ** Configurations personnalisées**: Consultez votre dossier `configs/` pour obtenir les fichiers `pysource.*.sh`

Si vous rencontrez des erreurs de chargement de module, vérifiez que toutes les dépendances requises (Python, MPI, compilateurs) sont correctement installées et configurées. Consultez le {ref}`TELEMAC installation guide <modular-install>` pour le dépannage.
```

Avec l'environnement TELEMAC chargé, passez au répertoire où vit la simulation TELEMAC Gaia (par exemple, `/home/telemac/v9.0.0/mysimulations/gaia2d-tutorial/`) et lancez le fichier `*.cas` en l'appelant avec le script **telemac2d.py** (il saura automatiquement qu'il doit utiliser Gaia quand il lit la ligne `COUPLING WITH : 'GAIA'`).

```
cd ~/telemac/v9.0.0/mysimulations/gaia2d-tutorial/
telemac2d.py steady2d-gaia.cas
```

````{admonition} Speed up with parallel computing
Avec {ref}`parallelism <tm-system-wide-opts>` activé, accélérer le calcul en utilisant plusieurs cœurs à travers le drapeau `--ncsize=N`. Par exemple, la ligne suivante exécute la simulation sur `N=4` cores:

```
telemac2d.py steady2d-gaia.cas --ncsize=4
```

**Lignes directrices pour la sélection `ncsize`:**
* Commencez par `ncsize` égal au nombre de cœurs CPU physiques (pas les hyperfils)
* Pour les petites mailles (< 10 000 nœuds), les frais généraux de parallélisation peuvent dépasser les avantages.
* Pour les grands maillages (> 100 000 nœuds), des accélérations significatives sont possibles.
* Surveiller l'utilisation du processeur pendant les runs pour optimiser `ncsize` pour votre système

**Drapeaux utiles supplémentaires:**
* `--nctile=N`: Nombre de sous-domaines pour la décomposition du domaine (par défaut égale `ncsize`)
* `--ncnode=N`: Nombre de nœuds de calcul pour les essais en grappe
* `-s` ou `--sortie`: Ré-exécuter seulement l'étape de fusion (utile si la simulation terminée mais la fusion a échoué)
* `-c` ou `--compileonly`: Compilez uniquement les fichiers de Fortran sans exécuter
* `--clean`: Supprimer les fichiers temporaires avant de commencer
````

```{admonition} Common runtime errors and solutions
:class: warning, dropdown

**Erreur : "ARRÊT DE L'APPEL - TAILLE DE L'ARRIÈRE"**
* Cause : Affectation insuffisante de la mémoire pour le maillage ou les variables
* Solution: Réduire la taille du maillage ou augmenter la mémoire disponible; vérifier les problèmes de qualité du maillage

**Erreur: "DÉPTE D'EAU NÉGATIVE"**
* Cause : Instabilités numériques, souvent à partir d'un pas trop long ou d'un maillage de mauvaise qualité
* Solution : Réduire `TIME STEP`, activer `TREATMENT OF NEGATIVE DEPTHS : 2`, améliorer la qualité du maillage dans les zones problématiques

**Erreur : « SOLIDE NON CONVERGE »**
* Cause: Le résolveur linéaire n'a pas atteint le critère de convergence
* Solution : Augmenter `MAXIMUM NUMBER OF ITERATIONS FOR SOLVER`, se détendre `SOLVER ACCURACY`, ou vérifier les conditions limites

**Erreur: «EXCEPTION DE POINTS DE FLOCATION»**
* Cause : Division par zéro ou débordement, souvent à partir de très petites profondeurs d'eau
* Solution : Augmenter `MINIMAL VALUE OF THE WATER HEIGHT`, vérifier les conditions initiales

** Spécifique à la gaie: "CONCENTRATION NÉGATIVE"**
* Cause: Instabilités numériques dans le système d'advection
* Solution : Utiliser le schéma `14` ou `15` pour les sédiments en suspension, réduire le temps, vérifier les conditions limites pour la charge en suspension
```

Un calcul réussi devrait se terminer par les lignes (ou similaires) suivantes dans *Terminal*:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                             1  HOURS
                             4  MINUTES
                            34  SECONDS
... merging separated result files

... handling result files
       moving: r2dsteady-gaia.slf
       moving: rGaia-steady2d.slf
       moving: r-control-sections.txt
... deleting working dir

My work is done
```

TELEMAC écrira les fichiers *r2dsteady-gaia.slf*, *rGaia-steady2d.slf* et *r-control-sections.txt* dans le dossier de simulation. Ces fichiers de résultats sont également disponibles dans le dépôt de modélisation de ce eBook pour accomplir le tutoriel post-traitement:

* [Télécharger r2dsteady-gaia.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady-gaia.slf) (résultats hydrodynamiques)
* [Télécharger rGaia-steady2d.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/rGaia-steady2d.slf) (résultats morphodynamiques)
* [Télécharger r-control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r-control-sections.txt) (flux de section de contrôle)

```{admonition} Understanding the output files
:class: note

**r2dsteady-gaia.slf** contient les variables hydrodynamiques définies dans le fichier de direction Telemac2d (p. ex. vitesse, profondeur de l'eau, élévation libre de la surface). Ceux-ci sont calculés par Telemac2d avec la rétroaction d'évolution du lit de Gaia.

**rGaia-steady2d.slf** contient les variables morphodynamiques définies dans le fichier de direction de Gaia (p. ex. élévation du fond, taux de transport de la charge de lit, concentrations de sédiments). Les variables correspondent au mot clé **VARIABLES POUR PRINTOUTS GRAPHIQUES** à `gaia-morphodynamics.cas`.

**r-control-sections.txt** contient des séries chronologiques de flux sur les sections de contrôle définies. Chaque ligne représente une étape temporelle avec des colonnes pour le flux intégré de chaque section.
```

## Traitement après

### Flux de section de contrôle

Le {ref}`control sections <tm-control-sections>` permet d'avoir des idées sur l'adaptation correcte du flux aux limites amont et aval (préciser Q seulement). {numref}`Figure %s <gaia-hydrograph>` montre les débits modélisés où les courbes *Inflow boundary* et *Outflow boundary* convergent après environ 10000 pas de temps. Notez que le graphique montre des nombres absolus alors que la sortie originale dans *r-control-sections.txt* est négative en raison de l'ordre des définitions de nœuds dans *control-sections.txt*. L'initialisation {ref}`hotstart <gaia-hotstart>` fait que les flux fluctuent autour du flux prescrit de 35 m$^{3}$/s dès le début. L'augmentation du débit *Extrait boundary* vers la fin de la simulation peut être attribuée à l'érosion des sédiments et au type de limite en aval du flux libre (`544-4`).

```{figure} ../../img/telemac/gaia-hydrograph.png
:alt: result flow discharge telemac2d morphodynamic gaia inflow outflow control sections
:name: gaia-hydrograph

Les flux simulés sur les sections de contrôle *Inflow boundary* en amont et *Outflow boundary* en aval.
```

```{admonition} How to distinguish water fluxes at inflow and outflow control sections from sediment transport rates?
Avec les deux {ref}`boundary files for Telemac2d and Gaia <gaia-bc>`, il est possible d'utiliser différents types de limites dans les fichiers de pilotage hydrodynamique (*steady2d-gaia.cas*) et morphodynamique (*gaia-morphodynamique.cas*). Ainsi, les flux de volume d'eau peuvent être prescrits à l'entrée et les sections de sortie à travers `455`-type limites (précisées Q seulement) dans les fichiers de direction hydrodynamique et/ou limites. Par exemple, avec `455`-type en amont et en aval des limites hydrodynamiques, adapter le mot-clé **PRESCRIBED FLOWRATES** à `35.;35` dans le fichier de direction hydrodynamique (*steady2d-gaia.cas*) sans changer la limite morphodynamique (Gaia) et les fichiers de direction.
```

```{admonition} Sediment mass balance verification
:class: tip
Pour vérifier la conservation de la masse de sédiments, activez `MASS-BALANCE : YES` dans le fichier de direction de Gaia. La sortie de l'inventaire comprendra des renseignements sur le bilan massique des sédiments à chaque période d'impression :

* ** Masse initiale**: Masse totale des sédiments au début de la simulation
* ** Masse finale**: Masse totale des sédiments à l'étape actuelle
* **Flux de masse**: Sédiment entrant ou sortant par les frontières
* **Erreur**: Erreur relative du bilan massique (devrait être < 1% pour les simulations bien configurées)

Les erreurs importantes du bilan massique (> 5 %) indiquent des problèmes potentiels liés aux conditions limites, aux schémas d'advection ou aux instabilités numériques.
```

### Visualisation avec QGIS

Les résultats de la simulation Gaia peuvent être visualisés et des instantanés de temps exportés vers des formats raster (par exemple, {term}`GeoTIFF`) ou shapefile en utilisant le plugin PostTelemac dans QGIS de la même manière que dans le {ref}`steady2d tutorial <tm2d-post-export>`. La dernière version de QGIS permet en outre le chargement d'un fichier maillé Selafin (résultats) (ici: *r2dsteady-gaia.slf*) en tant que couche maillé QGIS, qui peut ensuite être visualisé dans le port de vue et exporté vers une vidéo avec le plugin Crayfish. À cette fin, ** lancer QGIS**, ** mettre le {ref}`project CRS <qgis-project>` à EPSG:25833** (ETRS89 / zone UTM 33N), et enregistrer le nouveau projet dans le dossier `gaia2d-tutorial/` (ou où jamais les fichiers de simulation Gaia vivent). Dans le panneau **Browser** de QGIS, trouvez le dossier **Project Home**, élargissez-le et faites glisser-déposer les deux mailles de résultats de simulation (*r2dsteady-gaia.slf* et *rGaia-steady2d.slf*) vers le panneau **Layers**.

Double-cliquez sur *r2dsteady-gaia.slf* ou *rGaia-steady2d.slf* pour ouvrir leurs propriétés de la couche **Mesh**, puis allez à l'onglet **Source** pour basculer les paramètres hydrodynamiques (p. ex. *profondeur d'eau* ou *fluidrate scalaire m2s*) ou morphodynamiques Gaia (p. ex. *qs bedload kg(ms*)) respectivement, à différents moments. {numref}`Figure %s <qgis-gaia-mesh-properties>` montre la fenêtre des propriétés des calques QGIS maillage de la simulation *rGaia-steady2d.slf* résultats géométrie où les cases rouges mettent en évidence les étapes pour basculer les variables de sortie et les temps de visualisation. En outre, l'onglet **Symbologie** fournit des options pour les échelles de couleur de valeur ou les représentations vectorielles (par exemple, pour les vecteurs de vitesse dans *r2dsteady-gaia.slf*).

```{figure} ../../img/telemac/qgis-gaia-mesh-properties.png
:alt: qgis telemac2d gaia morphodynamics solid discharge bedload results slf
:name: qgis-gaia-mesh-properties

La fenêtre maillage Propriétés du calque avec l'onglet Source pour sélectionner les variables de sortie Gaia. La capture d'écran indique les étapes de visualisation de *qs bedload* à la fin de la simulation (boîtes rouges). De plus, les gammes de couleurs des tracés peuvent être adaptées dans l'onglet Symbologie (boîte rouge cassée).
```

```{admonition} rGaia-steady2d.slf (results file) not correctly showing in QGIS
:class: error, dropdown

Le fichier de résultats `rGaia-steady2d.slf` n'apparaît-il pas dans QGIS? Assurez-vous de l'importer avec sa géoréférence correcte: **EPSG:25833** (ETRS 89 / zone UTM 33N). Si le maillage apparaît au mauvais endroit ou avec une géométrie déformée, vérifiez que:

1. Le projet Système de coordonnées correspond au filet Système de coordonnées (EPSG:25833)
2. La reprojection à la volée est activée si un projet différent est utilisé Système de coordonnées
3. Le fichier géométrique d'origine a utilisé le bon système de référence de coordonnées

Pour définir le calque Système de coordonnées manuellement : Faites un clic droit sur le calque → **Fixez Système de coordonnées** → **Fixez Système de coordonnées...** → recherchez EPSG:25833.
```

Notez que seuls les paramètres définis avec les **VARIABLES POUR PRINTOUTS GRAPHIQUES** dans les fichiers de pilotage hydrodynamique ({ref}`steady2d-gaia.cas <tm2d-gen>`) et morphodynamique ({ref}`gaia-morphodynamics.cas <gaia-gen>`) peuvent être tracés dans QGIS.

```{admonition} Key Gaia output variables for visualization
:class: tip
Les variables suivantes sont particulièrement utiles pour l'analyse des simulations morphodynamiques :

| Variable | Description | Unit |
|----------|-------------|------|
| `B` | Bottom elevation | m |
| `E` | Bottom evolution (change from initial) | m |
| `QSBL` | Bedload transport rate (per unit width) | kg/(m·s) |
| `QS` | Total solid discharge | kg/s |
| `TOB` | Bed shear stress | N/m² |
| `MU` | Skin friction correction factor | - |
| `CS*` | Suspended sediment concentration (per class) | g/l |
| `ES*` | Layer thickness (per layer) | m |
| `A*`, `R*` | Sediment class fractions in active layer | - |

Inclure ceux-ci dans **VARIABLES POUR PRINTOUTS GRAPHIQUES** pour permettre la visualisation.
```

Pour exporter une vidéo des résultats de simulation, utilisez le plugin *Crayfish* :

* Dans QGIS, assurez-vous que le plugin Crayfish est installé (appelez le {ref}`QGIS instructions <qgis-tbx-install>`).
* Dans le panneau **Layer**, sélectionnez **rGaia-steady2d** (ou *r2dsteady-gaia*).
* Avec *rGaia-steady2d* (ou *r2dsteady-gaia*) sélectionné, allez à **Mesh** (menu déroulant supérieur) > **Crayfish** > **Exporter l'animation ...** (si le calque n'est pas surligné, un message d'erreur apparaît : *Veuillez sélectionner un calque Mesh pour exporter*).
* Dans la fenêtre **Export Animation**, allez dans l'onglet **General** et définissez un nom de fichier de sortie en cliquant sur le bouton **...** (par exemple, `velocity-video.avi`).
* Adaptation facultative des paramètres *Layout* et *Video*.
* Cliquez sur **OK** pour démarrer l'export vidéo.

Pour la première fois qu'une vidéo est exportée, Crayfish devra définir un encodeur vidéo **FFmpeg** et guider l'installation (si nécessaire). Suivez les instructions et recommencez à exporter la vidéo. La vidéo suivante a été exportée avec Crayfish pour visualiser les vecteurs de vitesse:

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/jFgwiAsElH0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Video: Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Notez comment les vecteurs de vitesse évoluent au fil du temps et que des vitesses d'écoulement élevées se produisent aux rampes/sills dans la section de la rivière (p. ex., les deux maxima transversal proches de la limite amont ou le maximum transversal près de la limite aval). En conséquence, le transport des charges de lit aux rampes devrait également être prononcé. La vidéo suivante montre *qs bedload* pour vérifier si le modèle a obtenu le lien physique entre la vitesse d'écoulement et la charge de lit droite.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/BUaqvWZ_AVk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Video: Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Après avoir regardé la vidéo, on peut conclure que la relation entre les vitesses d'écoulement et la charge de lit est approximativement correcte, mais le modèle peut nécessiter une certaine correction en adaptant {ref}`magnitude and direction parameters <gaia-dir>`. La section suivante illustre par exemple comment la solidité physique du modèle peut être analysée et améliorée.


(bl-plausability)=
## Plausibilité

Les résultats ci-dessus montrent des charges de lit en état d'équilibre et des charges suspendues dans une section de rivière blindée à un débit bas de 35 m$^{3}$/s. La comparaison de la vitesse d'écoulement et des vidéos de transport des sédiments suggère que les taux de transport des sédiments les plus élevés se produisent là où la vitesse d'écoulement est élevée. Trois classes de taille des sédiments ont été définies dans le {ref}`Basic Setup of Gaia <gaia-sed>` avec un diamètre moyen de 0,0005 m, 0,02 m et 0,1 m. La simulation prévoit que seule la classe de granulométrie la plus fine se déplacera au débit de base (p. ex. dans la sortie de console pendant la simulation). Cette classe de sédiments fins de 0,5 mm de diamètre (sable) est transportée sous forme de lit et en suspension sans effet mesurable sur l'élévation du lit. On peut donc supposer que le modèle est essentiellement raisonnable physiquement, en particulier si l'on considère qu'on ne modélise presque pas l'élévation du lit de rivière malgré le pic de transport local des sédiments fins. Néanmoins, pour vérifier la plausibilité physique d'un modèle morphodynamique, il faut simuler des décharges plus élevées (inondations). Ensuite, les grains plus grossiers de 0,02 m (grave) et de 0,1 m (cobble) devraient aussi se déplacer.

```{admonition} A physical plausibility check is not a model validation
La vérification de plausibilité physique sert à vérifier si les résultats de simulation sont physiquement sains. Les résultats physiques non significatifs seraient, par exemple, lorsque la profondeur de l'eau augmente de façon permanente dans une simulation régulière, lorsque l'eau coule au-dessus des plaines inondables au débit de base ou quitte le modèle à des nœuds limites non définis, ou lorsque aucun sédiment ne se déplace à un débit élevé (p. ex., une crue de 100 ans) sur un lit de rivière alluvial. La validation du modèle intervient après l'étalonnage (voir la section suivante).
```

Aussi la profondeur de l'eau, la vitesse du débit (vecteurs) et {term}`Topographic change` devraient être analysées (en QGIS ou BlueKenue) puisque Gaia modifie les élévations du lit de rivière. Par exemple, si le modèle prédit {term}`Topographic change` sous la forme d'une érosion profonde de 10 m au débit de base, les définitions de mots clés pour le {ref}`riverbed <gaia-active-lyr>` devraient être révisées. De même, les paramètres hydro-morphodynamiquement pertinents tels que {ref}`friction <c-friction>`, ou {ref}`direction and magnitude (bedload) <gaia-dir>` correcteurs doivent être vérifiés.

```{admonition} Plausibility checklist for morphodynamic simulations
:class: tip

Avant de procéder à l'étalonnage, vérifier ce qui suit:

**Hydrodynamique:**
- [ ] Les profondeurs d'eau sont physiquement raisonnables (pas de profondeur négative, pas d'inondation irréaliste)
- [ ] Les vitesses de débit correspondent aux plages prévues pour la décharge
- [ ] Le bilan massique des entrées et sorties est fermé (sections de contrôle)
- [ ] Aucune oscillation ou instabilité fallacieuse dans le champ de vitesse

**Morphodynamique:**
- [ ] Le transport des sédiments se produit lorsque la contrainte de cisaillement dépasse les valeurs critiques
- [ ] La direction de la charge de lit s'harmonise avec la direction du flux principal (avec les écarts attendus dans les courbes)
- [ ] L'amplitude de l'évolution du lit est plausible (pas de trous de 10 m au débit de base)
- [ ] Le bilan massique des sédiments est fermé (vérifiez la sortie du bilan massique de Gaia)
- [ ] Seules les classes mobiles de sédiments se déplacent (fractions grossières stables à faible débit)

** Charge suspendue (si activée):**
- [ ] Les concentrations se situent dans des fourchettes physiquement raisonnables (habituellement < 10 g/l pour les rivières)
- [ ] La distribution verticale suit le profil Rouse attendu (pour les simulations 3D)
- [ ] Le dépôt se produit dans les zones à faible vitesse
- [ ] Aucune concentration négative
```

Lorsqu'un modèle est finalement et approximativement significatif physiquement, le modèle peut être {ref}`calibrated <bl-calibration>` avec des données d'observation. La section suivante fournit une liste de mots-clés qui peuvent être utilisés pour étalonner {term}`Bedload` et/ou {term}`Suspended load` simulations avec Gaia.


(gaia-calibration)=
## Étalonnage

```{dropdown} Recall: How to calibrate?
L'étalonnage implique l'adaptation par étapes des paramètres d'entrée du modèle afin d'obtenir le meilleur ajustement (statistique) possible des données modélisées et mesurées. Dans le processus d'étalonnage du modèle, un seul paramètre doit être modifié à la fois par des écarts de 10 à 20 % par rapport à sa valeur par défaut. Par exemple, si la valeur par défaut est `BETA : 1.3`, l'étalonnage peut être testé pour `BETA : 1.2`, puis `BETA : 1.1`, et ainsi de suite, pour finalement savoir quelle valeur pour **BETA** apporte les résultats du modèle le plus proche des données d'observation.

De plus, une analyse de sensibilité compare les modifications progressives de plusieurs paramètres (toujours un à la fois) et leurs effets sur les résultats du modèle. Par exemple, si une variation de 10 % de **BETA** donne une variation de 5 % de la profondeur globale de l'eau alors qu'une variation de 10 % d'un coefficient de frottement donne une variation de 20 % de la profondeur globale de l'eau, on peut conclure que la sensibilité du modèle par rapport au coefficient de frottement est plus élevée que par rapport à **BETA**. Toutefois, ces conclusions exigent des considérations minutieuses dans les modèles multiparamétriques et complexes des écosystèmes fluviaux.
```

Cette section suppose que le modèle est déjà étalonné hydrodynamiquement (par exemple, en ce qui concerne le frottement) comme décrit dans le {ref}`steady modeling section <tm2d-calibration>`. Gaia peut ensuite être utilisé pour modéliser un hydrographe d'inondation avec un {ref}`unsteady (quasi-steady) simulation <chpt-unsteady>`. Le calibrage exige que les mesures de l'élévation du lit de rivière avant et après l'inondation soient disponibles (c.-à-d. une carte {term}`Topographic change`).

```{admonition} Calibration data requirements
:class: note

Les données d'étalonnage idéales pour les modèles morphodynamiques comprennent:
* **Pré-événement Modèle numérique de terrain (MNT)**: bathymétrie/topographie à haute résolution avant l'événement modélisé
* **Après l'événement Modèle numérique de terrain (MNT)**: Bathymétrie/topographie haute résolution après l'événement modelé
* **Hydrographe**: Série chronologique de décharges pendant l'événement
* ** Concentrations de sédiments en suspension**: Séries chronologiques SSC mesurées aux stations de mesure (si disponibles)
* **Mesures de la charge utile**: Données de l'échantillonneur ou du piège (rares mais précieuses)

La différence entre les Modèle numérique de terrain (MNT) pré- et post-événement donne la carte **topographique de changement** (ou DoD - Modèle numérique de terrain (MNT) de Différence), qui sert de cible d'étalonnage primaire pour les modèles morphodynamiques.
```

(bl-calibration)=
### Paramètres d'étalonnage de la charge de lit

La liste suivante de paramètres peut être envisagée pour l'étalonnage de la charge en lit dans Gaia:

* **Representative roughness length** $k'_{s}$ (cf. Equation {eq}`eq-cf-skin`) with the keyword **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER** $\alpha_{ks}$ (default: $\alpha_{ks}$=`3.`). Note that this keyword is a multiplier of the mean grain diameter $D_{50}$; thus: $k'_{s}= \alpha_{ks} \cdot D_{50}$ (goes into Equation {eq}`eq-cf-skin`):
  * Pour utiliser ce paramètre d'étalonnage, assurez-vous que `SKIN FRICTION CORRECTION : 1`.
  * On dune-form sand riverbeds, start with $\alpha_{ks}$=`37.` {cite:p}`mendoza2017`.
  * In alternating bar riverbeds, start with $\alpha_{ks}$=`3.6` {cite:p}`mendoza2017`.
  * Augmenter $\alpha_{ks}$ augmente la friction cutanée et donc les taux de transport de la charge de lit.

* Pour les modèles basés sur la formule {ref}`Meyer-Peter and Müller <gaia-mpm>` (c.-à-d. utilisant un {term}`Shields parameter` pour le mouvement des sédiments naissants), le mot-clé **CLASSES PARAMETERS** peut être modifié :
  * Si l'érosion est surestimée, augmenter **CLASSES PARAMÈTRES**.
  * Si l'érosion est sous-estimée, réduisez les paramètres **.
  * Portée typique : 0,03-0,06 pour les sédiments uniformes, jusqu'à 0,07 pour les lits blindés.

* Le **MPM COEFFICIENT** peut être ajusté (par défaut: `8`):
  * Valeur originale de Meyer-Peter et Müller: `8`
  * Correction de Wong-Parker pour les lits d'avion: `3.97` (avec `CLASSES SHIELDS PARAMETERS : 0.0495`)
  * Réduire pour diminuer les taux globaux de transport de la charge de lit.

* Avec la correction de pente activée et en utilisant les formules de correction {cite:t}`koch1980`, adapter le mot-clé **BETA** de l'équation {eq}`eq-qb-corr` (par défaut est `BETA : 1.3`):
  * Si l'érosion dans les sections courbes du chenal est surestimée, diminuer **BETA**.
  * Si l'érosion dans les sections courbes du chenal est sous-estimée, augmenter **BETA**.
  * Plage typique: 1.0-2.0.

* Pour ajuster le profil de dépôt et d'érosion dans les courbes (riverbends), activer le mot-clé **CURRENTS SECONDAIRES** et modifier la valeur **CURRENTS SECONDAIRES ALPHA COEFFICIENT** (cf. {ref}`Secondary Currents <gaia-secondary>`):
  * Par défaut : `1.0` (lit mou)
  * Pour les lits difficiles: `0.75`
  * Influe sur l'intensité du flux hélicoïdal et donc sur la redistribution latérale des sédiments.

* Le mot clé **HIDING FACTOR FORMULA** (pour les sédiments multiclasses) contrôle la façon dont les particules plus fines sont cachées par les particules plus grossières:
  * `0`: facteur de cache constant (**default**), qui exige que les valeurs par classe soient données avec le mot clé **CLASSES HIDING FACTOR**
  * `1`: Formule Egiazaroff
  * `2`: Formule Ashida & Michiue
  * `4`: formule Karim, Holly & Yang
  * Influe sur la mobilité relative des différentes classes de sédiments.

```{admonition} Recommended calibration sequence for bedload
:class: tip

1. **Première** : Étalonnage de la magnitude globale du transport à l'aide de **CLASSES PARAMÈTRES** ou **MPM COEFFICIENT**
2. **Deuxième**: Régler la distribution spatiale en utilisant **BETA** et **CURRENTS SECONDAIRES ALPHA COEFFICIENT**
3. **Troisième** : Tune fine utilisant **RATIO ENTRE LA FRICTION DE LA SKIN ET LE DIAMÈTRE MEAN**
4. ** Dernier** : Régler les effets de cache/exposition pour les modèles multiclasses en utilisant **HIDING FACTOR FORMULA**

Comparer le changement topographique simulé avec le DoD mesuré (Modèle numérique de terrain (MNT) of Difference) à l'aide de mesures statistiques telles que le RMSE, l'efficacité Nash-Sutcliffe ou la cote Brier Skill Score.
```

### Paramètres d'étalonnage de charge suspendus

La liste suivante de paramètres peut être prise en compte pour l'étalonnage du transport en suspension et du profil d'érosion des dépôts à Gaia:

* **{ref}`CLASSES SETTLING VELOCITIES <gaia-sl-sed>`** :
  - Réduire pour augmenter la longueur du transport et réduire les taux de dépôt
  - Augmentation pour raccourcir les trajectoires de transport et améliorer les dépôts
  - Réglez à `-9` pour utiliser le calcul automatique de Gaia en fonction de la taille du grain

* **{ref}`CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION <gaia-sl-sed>`** :
  - Réduire pour maintenir les sédiments en suspension plus longtemps (déposition seulement à des contraintes de cisaillement plus faibles)
  - Augmentation pour permettre le dépôt à des contraintes de cisaillement plus élevées
  - Par défaut `1000` N/m2 désactive efficacement le seuil de dépôt

* **LAYERS PARTHENIADES CONSTANT** (constante du taux d'érosion $M$):
  - Augmentation des taux d ' érosion
  - Réduire les taux d'érosion
  - Gamme typique: 1.E-04 à 1.E-02 kg/(m2·s)

* **LAYERS STRESS DE CRITIQUE D'ÉROSION DU MUD**:
  - Augmentation pour réduire l'érosion (seuil plus élevé)
  - Diminution pour accroître l'érosion (seuil inférieur)
  - Variables avec consolidation des sédiments; plage typique: 0,01-1,0 N/m2

* ** COEFFICIENT POUR LA DIFFUSION DES SEDIMENTS SUPPLÉMENTAIRES** (ou s'appuyer sur le modèle de turbulence; par défaut `1.E-6` m2/s):
  - Des valeurs plus élevées augmentent la propagation latérale des sédiments en suspension
  - Les valeurs inférieures concentrent les panaches de sédiments

```{admonition} Recommended calibration sequence for suspended load
:class: tip

1. **Première** : Correspondance des concentrations de sédiments en suspension aux stations de mesure en ajustant **LAYERS PARTHENIADES CONSTANT** (érosion) et **CLASSES FIXANT DES VÉLOCITÉS** (déposition)
2. **Deuxième**: Ajuster **LAYERS CRITIQUE ÉROSION FEUILLE DU MUD** pour contrôler l'origine de l'érosion
3. **Troisième** : Tune fine ** CLASSES STRESS CRITIQUE POUR DÉPOSITION DE MUD** pour correspondre aux profils de dépôt
4. **Dernier**: Ajuster ** COEFFICIENT POUR LA DIFFUSION DES SEDIMENTS SUSPENDUS** si l'étalement du panache apparaît incorrect

Comparer les séries chronologiques SSC simulées avec les mesures utilisant l'efficacité RMSE ou Nash-Sutcliffe.
```

**Et ensuite?**
: Le modèle étalonné devra également être validé. La validation nécessite un autre ensemble de mesures de l'altitude du lit de rivière avant et après une autre inondation (c.-à-d. une autre carte spécifique à l'événement {term}`Topographic change`). Hélas, les cartes {term}`Topographic change` sont chères et il est rare d'avoir au moins trois {term}`DEM`s de différents points dans le temps pour une section de rivière, ce qui permettrait la création de deux cartes {term}`Topographic change`. Pour cette raison, l'ensemble de données d'étalonnage est souvent divisé en pratique. Par exemple, les 2/3 d'une carte {term}`Topographic change` peuvent être utilisés pour l'étalonnage des modèles et les 1/3 pour la validation des modèles. Toutefois, ce partage fait que les deux ensembles de données ne sont pas statistiquement indépendants et que les chiffres de qualité de validation seront biaisés.

```{admonition} Model validation approaches
:class: note

Lorsque des ensembles de données de validation indépendants ne sont pas disponibles, il convient d'examiner:

* **Diffusion spatiale**: Étalonnage sur la partie amont, validation en aval (ou vice versa)
* **Scission temporaire**: Étalonnage sur la première moitié de l'événement, valider sur la seconde moitié
* ** Validation par défaut**: fractionnement en k des données disponibles
* **Validation fondée sur les procédés**: Vérifier que le modèle reproduit correctement les comportements physiques connus (p. ex. formation de barres de point dans les méandres, séquences de riffles de pool)
* ** Analyse de sensibilité**: Documenter la réponse du modèle aux variations de paramètres pour caractériser l'incertitude

Toujours signaler les limites de validation de manière transparente lors de la publication ou de l'application des résultats du modèle.
```