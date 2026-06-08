---
description: Introduction au couplage de l'hydrodynamique TELEMAC avec la morphodynamique GAIA pour simuler la charge de lit et le transport des sédiments en suspension dans les rivières, les lacs et les estuaires.
---

# Introduction et couplage

```{admonition} Requirements
Ce tutoriel est conçu pour ** modélistes avancés** et avant de plonger dans ce tutoriel assurez-vous de ** compléter les tutoriels {ref}`TELEMAC pre-processing <slf-prepro-tm>` et {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>`**.

Le cas présenté dans ce tutoriel a été établi avec le logiciel suivant:
* {ref}`Notepad++ <npp>` éditeur de texte (tout autre éditeur de texte fera tout aussi bien).
* TELEMAC v9.0.0 ({ref}`stand-alone installation <modular-install>`) - les versions antérieures peuvent ne pas reconnaître certains des mots clés utilisés dans ce livre électronique.
* {ref}`QGIS <qgis-install>`.
* Debian Linux / Ubuntu 24.04 (en savoir plus sur {ref}`software chapter <chpt-vm-linux>`).
```

## Terminologie
Une simulation hydromorphodynamique implique la modélisation de processus axés sur le ruissellement **{term}`Sediment transport`**. Les sections précédentes de ce livre électronique se concentrent sur l'hydrodynamique définie comme *l'étude des liquides en mouvement* et cette section se concentre sur **morphodynamique** définie comme **l'étude des changements liés au temps dans les formes des lits alluviaux et leurs processus sous-jacents**.

(gaia-seditrans)=
## Modes de transport des sédiments

TELEMAC has a dedicated module called Gaia for modeling morphodynamics. Gaia enables modeling sediment transport and morphological evolution (i.e., {term}`Topographic change`) in rivers, lakes, and estuaries. It comes with particular routines to consider a spatio-temporal variation of grain sizes, grading curves, and riverbed layering for simulating sediment transport in the form of **{term}`Bedload` (coarse sediment)** and/or **{term}`Suspended load` (fine sediment)**. {term}`Bedload` is calculated by solving semi-empiric equations, such as the {cite:t}`meyer-peter_formulas_1948` formula (read more later in this tutorial). {term}`Suspended load` is modeled by solving the {term}`Advection`-{term}`Diffusion` equations (typically, the {term}`RANS` form), which require closures for sediment erosion and deposition fluxes. {numref}`Figure %s <bl-vs-sl>` qualitatively illustrates the two basic modes of sediment transport in the form of suspended load and bedload. Whether a particle is transported in suspension or as bedload can also be determined by calculating of the {term}`Rouse number`.

```{figure} https://github.com/Ecohydraulics/media/raw/main/png/sediment-transport.png
:alt: sediment transport bedload suspended load
:name: bl-vs-sl

Représentation qualitative de deux modes de transport des sédiments. À gauche : charge en suspension sous forme de particules fines se déplaçant avec le flux en vrac ; à droite : charge en lit sous forme de particules roulant, sautant ou glissant sur le lit de la rivière.
```

On distingue davantage les sédiments très fins, **cohésifs** et les sédiments plus grossiers, **non cohésifs**. En outre, Gaia explique l'évolution du lit à travers une solution itérative du {term}`Exner equation` {cite:p}`exner_uber_1925` pour la conservation de masse.

Le recrutement de sédiments pour le transport de charge en suspension et de charge en lit nécessite un examen détaillé du lit de la rivière, qui sera fourni plus tard dans la section sur la définition de {ref}`the riverbed composition and the active layer <gaia-active-lyr>`.


(tm-coupling)=
## Couplage TELEMAC et Gaia

Le module morphodynamique Gaia peut être interne **couplé** avec les modèles hydrodynamiques Telemac2d (solution du {term}`Shallow water equations`) ou Telemac3d (solution du Reynolds-moyenne {term}`Navier-Stokes (RANS) equations <Navier-Stokes equations>`). Cette section explique les types de couplage Telemac2d/Telemac3d (hydrodynamique) avec Gaia (morphodynamique).

### De Sisyphe à Gaïa

Sisyphe est le module traditionnel de transport des sédiments de TELEMAC, qui a été largement remplacé par le module Gaia plus unifié. Gaia est basé sur le module historique SISYPHE, avec un grand nombre d'améliorations, de corrections et d'optimisations mises en œuvre. Le cadre unifié de Gaia gère efficacement différentes classes de sédiments, des mélanges sable-mud et des dimensions spatiales 2D et 3D. Pour obtenir des spécifications au-delà des caractéristiques présentées ici dans la documentation TELEMAC et le forum TELEMAC, il est utile de connaître le patrimoine SISYPHE. Les routines de SISYPHE sont toujours disponibles dans les versions récentes de TELEMAC via Gaia, mais certains mots-clés nécessitent des ajustements. En savoir plus dans le [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) à l'annexe 8.1 et dans le gaia.dico (`telemac/v9.0.0/sources/gaia/gaia.dico`).

### Couplage Hydrodynamique (Telemac2d/3d) et Morphodynamique (Gaia)

Un modèle numérique hydro-morphodynamique peut être soit entièrement couplé** ou ** découplé**.

Modèle entièrement couplé
: Un modèle entièrement couplé résout l'hydrodynamique {term}`Navier-Stokes equations` en même temps que les équations de transport des sédiments (c.-à-d. l'érosion et les flux de dépôt depuis et vers le lit de la rivière à travers le {term}`Exner equation`). L'élévation du lit (c.-à-d. {term}`Topographic change`) est calculée pour chaque pas de temps, ce qui conduit à ** longtemps de calcul**. En plus du couplage de l'hydrodynamique gravitationnelle (c.-à-d. flux en vrac le long des pentes de la vallée), {term}`Sediment transport`, et {term}`Topographic change`, un modèle peut également être couplé avec l'hydrodynamique des vagues (surface).

* Gamme de demande :* Des processus morphodynamiques rapides, tels que des débits de sédiments hyperconcentrés ou des débits de débris.



Modèle découplé
: Un modèle découplé alterne entre l'hydrodynamique et la morphodynamique (c'est-à-dire le {term}`Exner equation`). Le lit de la rivière est considéré comme fixe lorsque les variables hydrodynamiques sont calculées, puis les changements d'altitude du lit sont calculés séparément en fonction du champ de débit calculé. Cette approche *synchrone* est plus efficace que le couplage complet.

* Gamme de demande :* La plupart des modèles fluviaux, en particulier les modèles lacustres ou océaniques où les échelles de temps morphodynamiques sont beaucoup plus longues que les échelles de temps hydrodynamiques.

Gaia suit l'approche **découplée**. L'étape temporelle utilisée pour le calcul morphodynamique est la même que pour l'hydrodynamique (précisée dans le fichier de direction Telemac2d ou Telemac3d). À chaque étape, l'hydrodynamique est résolue d'abord avec le lit gelé, puis les équations de transport des sédiments et l'évolution du lit (équation Exner) sont résolues sur la base du champ d'écoulement calculé.

```{admonition} Coupling period for wave-current-sediment interactions
:class: note
Lors du couplage de Gaia avec le module d'onde TOMAWAC, une période **de couplage** peut être spécifiée pour contrôler la fréquence de mise à jour des champs d'onde. Cela est pertinent parce que les calculs d'onde peuvent être coûteux et que les conditions d'onde peuvent ne pas changer aussi rapidement que les courants. Pour le couplage Telemac2d/3d-Gaia de base sans ondes, la morphodynamique est calculée à chaque étape du temps hydrodynamique. Pour en savoir plus sur le couplage des vagues à la section 5.1 du [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

### Exigences du dossier pour le couplage Gaia

En plus des fichiers standard de direction Telemac2d, de limites et de mailles géométriques, le couplage hydrodynamique avec Gaia nécessite un nouveau fichier de direction (`*.cas`) qui doit être référencé dans le fichier de direction principal de la simulation. À cette fin, **créer un nouveau dossier pour le tutoriel de Gaia** (par exemple, appelé `/gaia2d-tutorial/`), copier le {ref}`dry-initialized steady2d simulation and results files <tm2d-init-dry>` (ou cloner le [gaia2d-tutorial depository](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/)), et **créer un nouveau fichier de direction de Gaia** (par exemple, appelé `gaia-morphodynamics.cas`). Ainsi, les fichiers suivants devraient vivre dans le dossier de modélisation pour ce tutoriel:

* Le maillage informatique sous la forme de [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* Les définitions des limites sous la forme de [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* Les résultats de l'exécution du modèle 2d stabilisé à l'initialisation sèche pour 35 m$^3$/s sous la forme de [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) ({ref}`dry steady run <tm2d-init-dry>` fining at `T=15000`).
* Un fichier de direction Telemac2d pour ce tutoriel, construit sur le fichier de direction stable2d initialisé à sec et appelé [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* Le nouveau fichier de direction [gaia-morphodynamique.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).

```{admonition} Gaia simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/gaia2d-tutorial/).
```

### Couple Gaia dans le fichier de pilotage hydrodynamique

Pour implémenter programmatiquement le couplage de Gaia avec une simulation Telemac2d/Telemac3d, quelques nouveaux mots clés doivent être définis en plus des mots clés expliqués dans le {ref}`steady2d chapter <telemac2d-steady>`. Le premier mot-clé supplémentaire est la référence pour tout couplage avec le fichier de direction Telemac2d ou Telemac3d:

```fortran
/ steady2d-gaia.cas
COUPLING WITH : 'GAIA'
```

```{admonition} steady2d-gaia.cas is the hydrodynamics (Telemac2d or Telemac3d) steering file
:class: note
Dans ce tutoriel, le fichier de direction hydrodynamique (Telemac2d ou Telemac3d) est appelé [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas) et le fichier de direction morphodynamique (Gaia) est appelé [gaia-morphodynamique.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).
```

En outre, le mot-clé **GAIA STEERING FILE** lie le fichier de pilotage de l'hydrodynamique `gaia-morphodynamics.cas` dans Telemac2d (ou Telemac3d) :

```fortran
/ steady2d-gaia.cas
/ ...
GAIA STEERING FILE : gaia-morphodynamics.cas
```


(gaia-hotstart)=
### Démarrer

Ce tutoriel s'appuie sur les résultats du {ref}`dry-initialized steady2d model <tm2d-init-dry>` parce que les simulations Gaia nécessitent généralement un champ de flux bien développé comme condition initiale (voir le {ref}`above definitions <tm-coupling>`). L'utilisation d'un ancien résultat de simulation pour l'initialisation du modèle s'appelle **hotstart**, ce qui nécessite un fichier de résultats d'une simulation précédente. À cette fin, assurez-vous que le fichier de résultats stable2d initialisé à sec se trouve dans le dossier de simulation ([télécharger r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf)). Ensuite ** définir le démarrage à chaud dans le fichier de direction Telemac2d** avec les mots-clés suivants:


```fortran
/ steady2d-gaia.cas
/ ...
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
```

```{admonition} COMPUTATION CONTINUED is obsolete in TELEMAC v9.0
:class: warning
Depuis TELEMAC v9.0, le mot clé `COMPUTATION CONTINUED` a été supprimé**. L'étape de poursuite est maintenant **activée automatiquement** lorsque `PREVIOUS COMPUTATION FILE` est spécifiée dans le fichier de direction. Il suffit de fournir le fichier de calcul précédent déclenche le comportement hotstart.
```

Le mot clé **INITIAL TEMPS SET TO ZERO** réinitialise le temps de simulation à `0`. Ensuite, assurez-vous que tous les mots-clés ** CONDITIONS INITIALES** sont commentés avec un **/** (à défaut de supprimer ces lignes de stabilisate2d-gaia.cas):

```fortran
/ steady2d-gaia.cas
/ ...
/ INITIAL CONDITIONS - not required (hotstart)
/ ------------------------------------------------------------------
/ INITIAL CONDITIONS : 'ZERO DEPTH' / use ZERO DEPTH to start with dry model conditions
/ INITIAL DEPTH : 0.005 / use INTEGER for speeding up calculations
```

```{admonition} Bottom elevation must be available in the hotstart geometry (SLF)
:class: warning
L'élévation inférieure doit être imprimée dans le fichier de résultats de la simulation utilisée pour le démarrage à chaud. À cette fin, assurez-vous que la liste des valeurs du mot clé **VARIABLES POUR PRINTOUTS GRAPHIQUES** contient `B` comme indiqué dans le {ref}`explanations for the setup of the dry-initialized model <tm2d-init-dry>`.
```

```{admonition} Continuing a Gaia computation (sedimentological hotstart)
:class: tip
Pour poursuivre une simulation de Gaia à partir d'un précédent calcul sédimentologique (c.-à-d. pour redémarrer avec les données existantes sur la composition du lit et les couches), utilisez le mot-clé **DOSSIER DE COMPUTATION SÉDIMENTOLOGIQUE PRÉCÉDENT** dans le fichier de direction de Gaia. Depuis v9.0, spécifier ce fichier active automatiquement la poursuite sans avoir besoin de mot-clé supplémentaire. Le fichier précédent devrait contenir l'élévation du fond (`B`), les épaisseurs de couche (`*ES`), et idéalement les masses de sédiments (`*S*` ou `*M*`) ou les rapports (`*A*`, `*R*`) pour une poursuite appropriée.
```

Le fichier de direction initialisé à sec prescrit les débits et les élévations, ce qui exige ** des modifications dans stability2d-gaia.cas** à ** prescrit Q seulement**. La raison de la prescription Q seulement est qu'avec Gaia, nous voulons modéliser les changements dans les profondeurs d'eau et l'élévation du lit de rivière, ce qui signifie que l'élévation de la surface de l'eau ne doit pas être limitée (c.-à-d. non prescrite) comme condition limite. Ainsi, la configuration des conditions limites pour Gaia nécessite également de légères modifications des fichiers limites (`*.cli`) qui seront expliqués dans la section suivante sur le {ref}`Basic Setup of Gaia <gaia-bc>`. À cette fin, assurez-vous que dans le fichier de pilotage hydrodynamique **seulement le mot-clé de prescription de débit est activé** et que la prescription d'élévation est désactivée (commenter avec `/`):

```fortran
/ steady2d-gaia.cas
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 374.805626;371.33
```

### Sections de contrôle

Les sections de contrôle sont des séquences de nombres de nœuds (ou de coordonnées de nœuds) où TELEMAC résume les flux, par exemple, pour vérifier les bilans massiques des entrées et des sorties. La section de simulation non stable fournit des instructions détaillées pour {ref}`defining control sections <tm-control-sections>` et ce tutoriel réutilise le fichier des sections de contrôle à partir de la simulation non stable (**[télécharger control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/control-sections.txt)**).

````{dropdown} Expand to view the file *control-sections.txt*
```
# control sections steady2d
2 -1
Inflow_boundary
144 32
Outflow_boundary
34 5
```
````

Pour utiliser les sections de commande pour la simulation de Gaia ajouter ce qui suit au fichier de direction **hydrodynamique**:

```
/ steady2d-gaia.cas
/ ...
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
```

Ainsi, le redémarrage de la simulation écrira les flux dans les deux sections de contrôle définies à un fichier appelé *r-control-flows.txt*.

### Résumé de la direction hydrodynamique

Avec les adaptations ci-dessus et en utilisant une durée de simulation de `30000` timesteps (pour observer l'évolution morphodynamique) avec une période d'impression graphique de chaque `5000` timesteps (pour réduire la taille du fichier de sortie), le fichier de direction hydrodynamique final devrait ressembler à ceci:

```fortran
/ steady2d-gaia.cas
/
TITLE : 'gaia2d steady'
/
/ HOTSTART - continuation is automatic when PREVIOUS COMPUTATION FILE is specified (v9.0+)
PREVIOUS COMPUTATION FILE : r2dsteady.slf / here - 35 CMS initialization after t 15000
INITIAL TIME SET TO ZERO : YES / avoid restarting at 15000
/
COUPLING WITH : 'GAIA'
GAIA STEERING FILE : gaia-morphodynamics.cas
/
/ DEFAULTS FROM STEADY2D
/
/------------------------------------------------------------------/
/     COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
RESULTS FILE           : r2dsteady-gaia.slf
/
MASS-BALANCE : YES / activates mass balance printouts - does not enforce mass balance
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
/
/ CONTROL SECTIONS
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
/
/------------------------------------------------------------------/
/     GENERAL PARAMETERS
/------------------------------------------------------------------/
TIME STEP : 1.
NUMBER OF TIME STEPS : 30000
GRAPHIC PRINTOUT PERIOD : 5000
LISTING PRINTOUT PERIOD : 5000
/
/------------------------------------------------------------------/
/     NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/ General solver parameters from section 7.1
DISCRETIZATIONS IN SPACE : 11;11
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
ADVECTION : YES
/
/ FINITE ELEMENT SCHEME PARAMETERS - section 7.2.1 in the manual
/------------------------------------------------------------------
TREATMENT OF THE LINEAR SYSTEM : 2 / default is 2 - use 1 to avoid smoothened results
SCHEME FOR ADVECTION OF VELOCITIES : 14 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 14
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITY : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION OF VELOCITY : 1. / v9p0 default
IMPLICITATION COEFFICIENT OF TRACERS : 0.6 / v9p0 default
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VELOCITY : 1.
MASS-LUMPING ON TRACERS : 1.
/ MASS-LUMPING FOR WEAK CHARACTERISTICS : 1. / enabling leads to weak characteristics
SUPG OPTION : 0;0;2;2  / classic supg for U and V
/
/ SOLVER
/------------------------------------------------------------------
INFORMATION ABOUT SOLVER : YES
SOLVER : 1
/
/ TIDAL FLATS  - see section 7.5
TIDAL FLATS : YES
CONTINUITY CORRECTION : YES / default is NO
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2 / value 2 or 3 is required with tidal flats - default is 1
/
/ MATRIX HANDLING - see section 7.6
MATRIX STORAGE : 3 / default is 3
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
/
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.;35.
/ PRESCRIBED ELEVATIONS : 374.805626;0.
/
/ Type of velocity profile can be 1-constant normal profile (default) and (cli) 4-vector is proportional to root (water depth, only for Q)
VELOCITY PROFILES : 4;1
/
/ INITIAL CONDITIONS - not required (hotstart)
/ ------------------------------------------------------------------
/ INITIAL CONDITIONS : 'ZERO DEPTH' / use ZERO DEPTH to start with dry model conditions
/ INITIAL DEPTH : 0.005 / use INTEGER for speeding up calculations
/
/ STABILITY CONTROLS
/ ------------------------------------------------------------------
PRINTING CUMULATED FLOWRATES : YES
/
/------------------------------------------------------------------/
/     TURBULENCE
/------------------------------------------------------------------/
/
DIFFUSION OF VELOCITY : YES / default is YES
TURBULENCE MODEL : 3
/
&ETA
```