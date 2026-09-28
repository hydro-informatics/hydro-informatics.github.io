---
description: Simulations numériques hydrodynamiques avec Telemac2d
---

(telemac2d-steady)=
# Stabilité 2d

```{admonition} Requirements
Ce tutoriel est conçu pour ** débutants avancés** et avant de plonger dans ce tutoriel assurez-vous de compléter le {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>`.

Le cas présenté dans ce tutoriel a été établi avec le logiciel suivant:
* un éditeur de texte, comme {ref}`Notepad++ <npp>` (tout autre éditeur de texte fera le travail).
* Télémac v8p2r0 ou plus récent ({ref}`stand-alone installation <modular-install>`).
* {ref}`QGIS <qgis-install>` et le {ref}`PostTelemac plugin <tm-qgis-plugins>`.
* Debian Linux 10 (Buster) / Debian 11 installé sur une machine virtuelle (lisez plus dans le {ref}`software chapter <chpt-vm-linux>`).
```

## Commencez

Cette section s'appuie sur la géométrie de SELAFIN (`*.slf`) et sur les fichiers de conditions limites de Conlim (`*.cli`) qui résultent de la configuration {ref}`TELEMAC pre-processing tutorial <slf-prepro-tm>`. Les deux fichiers peuvent également être téléchargés à partir du dépôt de matériaux supplémentaires de ce livre électronique:

* [Télécharger qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf) (usages **EPSG:32633** - ETRS 89 / UTM zone 33N).
* [Télécharger les limites.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli).

Envisagez de sauvegarder les deux fichiers dans un nouveau dossier, comme `/steady2d-tutorial/` qui contiendra tous les fichiers modèles.

```{admonition} Download simulation files
All simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial/).
```

## Dossier de direction (CAS)

The steering file has the file ending `*.cas` (presumably derived from the French word *cas*, which means *case* in English). The `*.cas` file is the main simulation file with information about references to the two always mandatory files (i.e., the [SELAFIN](https://gdal.org/drivers/vector/selafin.html) `*.slf` geometry and the `*.cli` boundary files) and optional files, as well as definitions of simulation parameters. The steering file can be created or edited with a basic text editor or advanced GUI software such as {ref}`Fudaa PrePro <fudaa>` or {ref}`BlueKenue <bluekenue>`. This tutorial uses a basic text editor (e.g., {ref}`Notepad++ <npp>` on Windows).

```{admonition} Fudaa PrePro
*Fudaa PrePro* est livré avec des descriptions variables qui facilitent la définition des limites, des conditions initiales et des paramètres numériques dans le fichier de direction. Cependant, Fudaa PrePro fait des directions de fichiers selon la plate-forme sur laquelle il est exécuté (c.-à-d. `\` sur Windows et `/` sur Linux) et écrit des chemins absolus vers le fichier `*.cas`, qui nécessite souvent une correction manuelle (par exemple, si Fudaa PrePro est utilisé pour configurer un fichier `*.cas` sur Windows pour exécuter une simulation TELEMAC sur Linux). Pour travailler avec Fudaa PrePro, suivez les instructions de téléchargement dans le {ref}`software chapter <fudaa>`. Pour lancer Fudaa Prepro, ouvrez *Terminal* (Linux) ou *Command Prompt* (Windows) et tapez sur:

* `cd` vers le répertoire d'installation (télécharger) de Fudaa PrePro
* Démarrez l'interface graphique (demande java):
  * *Linux* : `sh supervisor.sh`
  * *Windows*: `supervisor.bat`
```

Pour ce tutoriel, **créer un nouveau fichier texte** dans le même dossier où `qgismesh.slf` et `boundaries.cli` live, et le nommer, par exemple, `steady2d.cas` (par exemple, `/steady2d-tutorial/steady2d.cas`). Les prochaines sections guident à l'aide de définitions de paramètres qui découlent du manuel [Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf). Le fichier de direction final peut être téléchargé à partir du dépôt de matériaux supplémentaires ([téléchargez stabilisate2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

### Aperçu du fichier CAS

La case ci-dessous montre le fichier fourni [steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas) qui peut être utilisé pour exécuter ce tutoriel.

````{admonition} Expand to view the complete .CAS file
:class: note, dropdown

```fortran
/---------------------------------------------------------------------
/ TELEMAC2D
/ STEADY HYDRODYNAMICS TRAINING
/---------------------------------------------------------------------

/ steady2d.cas
/------------------------------------------------------------------/
/			COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
TITLE : '2d steady'
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE            : qgismesh.slf
RESULTS FILE           : r2dsteady.slf
/
MASS-BALANCE : YES / activates mass balance printouts - does not enforce mass balance
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,B,H,S,Q,F / Q enables boundary flux equilibrium controls, B required for gaia (optional)
/
/------------------------------------------------------------------/
/			GENERAL PARAMETERS
/------------------------------------------------------------------/
TIME STEP : 1.
NUMBER OF TIME STEPS : 15000
GRAPHIC PRINTOUT PERIOD : 200
LISTING PRINTOUT PERIOD : 100
/
/------------------------------------------------------------------/
/			NUMERICAL PARAMETERS
/------------------------------------------------------------------/
/ General solver parameters
DISCRETIZATIONS IN SPACE : 11;11
FREE SURFACE GRADIENT COMPATIBILITY : 0.1  / default 1.
ADVECTION : YES
/
/ STABILITY CONTROLS
PRINTING CUMULATED FLOWRATES : YES
/
/ FINITE ELEMENT SCHEME PARAMETERS
/------------------------------------------------------------------
TREATMENT OF THE LINEAR SYSTEM : 2 / default is 2 - use 1 to avoid smoothened results
SCHEME FOR ADVECTION OF VELOCITIES : 14 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 14
IMPLICITATION FOR DEPTH : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR VELOCITY : 0.55 / should be between 0.55 and 0.6
IMPLICITATION FOR DIFFUSION OF VELOCITY : 1. / v8p4 default
IMPLICITATION COEFFICIENT OF TRACERS : 0.6 / v8p4 default
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VELOCITY : 1.
MASS-LUMPING ON TRACERS : 1.
SUPG OPTION : 0;0;2;2 / classic supg for U and V
/
/ SOLVER
/------------------------------------------------------------------
INFORMATION ABOUT SOLVER : YES
SOLVER : 1
MAXIMUM NUMBER OF ITERATIONS FOR SOLVER : 200 / maximum number of iterations when solving the propagation step
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF TRACERS : 60 / tracer diffusion
MAXIMUM NUMBER OF ITERATIONS FOR K AND EPSILON : 50 / diffusion and source terms of k-e
/
/ TIDAL FLATS
TIDAL FLATS : YES
CONTINUITY CORRECTION : YES / default is NO
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2 / value 2 or 3 is required with tidal flats - default is 1
/
/ MATRIX HANDLING
MATRIX STORAGE : 3 / default is 3
/
/ BOUNDARY CONDITIONS
/------------------------------------------------------------------
/
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.; 0.
PRESCRIBED ELEVATIONS : 374.80565;371.33
/
/ Type of velocity profile can be 1-constant normal profile (default) 2-UBOR and VBOR in the boundary conditions file (cli) 3-vector in UBOR in the boundary conditions file (cli) 4-vector is proportional to the root (water depth, only for Q) 5-vector is proportional to the root (virtual water depth), the virtual water depth is obtained from a lower point at the boundary condition (only for Q)
VELOCITY PROFILES : 4;1
/
/ Friction at the bed
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
/ Friction at the boundaries
LAW OF FRICTION ON LATERAL BOUNDARIES : 4 / 4-Manning
ROUGHNESS COEFFICIENT OF BOUNDARIES : 0.03 / Roughness coefficient
/
/ INITIAL CONDITIONS
/ ------------------------------------------------------------------
INITIAL CONDITIONS : 'ZERO DEPTH' / start with dry model conditions
/
/-------------------------------------------------------------------
/			TURBULENCE
/-------------------------------------------------------------------
/
DIFFUSION OF VELOCITY : YES / default is YES
TURBULENCE MODEL : 3
/
&ETA
```

```{admonition} What means &ETA?
:class: note
Le mot-clé `&ETA` en bas du fichier modèle `*.cas` fait imprimer des mots-clés et les valeurs qui leur sont assignées lorsqu'il exécute son algorithme *Damocles*.
```
````

(tm2d-gen)=
### Paramètres généraux

Les paramètres généraux définissent l'environnement de calcul en commençant par un titre de simulation et les liens les plus importants aux deux fichiers d'entrée obligatoires:

* `BOUNDARY CONDITIONS FILE : boundaries.cli` - avec un fichier *MED*, utilisez un fichier limite *BND*
* `GEOMETRY FILE : qgismesh.slf`

Le modèle **output** peut être défini avec les mots clés suivants:

* `RESULTS FILE : r2dsteady.slf` - peut être un fichier *MED* ou un fichier *SLF*
* `VARIABLES FOR GRAPHIC PRINTOUTS` (i.e., paramètres de sortie):
  * `U,V,H,S,Q,F` , pour le flux (`U`: $u$) et latéral (`V`: $v$) vitesses, profondeur de l'eau (`H`: $h$), élévation de la surface de l'eau (`S`: $wse$), décharge/fluxes (`Q`: $Q$), et {term}`Nombre de Froude <Froude number>` (`F`: $Fr$)
  * Autres variables d'intérêt pour les tutoriels dans ce livre électronique : élévation du bas `B` (obligatoire pour {ref}`morphodynamics with Gaia <gaia-basics>`, valeur du type de friction du bas utilisé `W` ({ref}`see below <tm2d-friction>`), et {term}`turbulent kinetic energy <Turbulent kinetic energy>` `K` (exige l'utilisation du $k-\epsilon$ {ref}`turbulence model <tm2d-turbulence>`).
  * The full list of available output variables can be found in the [Telemac2d reference manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac2d/reference/telemac2d_reference_9.0.pdf), section 1.348 (page 92).

Les vitesses (`U` et `V`), la profondeur d'eau (`H`) et le débit (`Q`) sont des variables standard qui devraient être utilisées dans chaque simulation. En particulier, la décharge `Q` est nécessaire pour vérifier quand (stable) s convergent aux limites d'entrée et de sortie. De plus, la décharge `Q` permet de tracer les flux intégrés le long de toute ligne définie par l'utilisateur dans le modèle. La procédure de vérification et d'identification des rejets est décrite dans la section {ref}`discharge verification <verify-steady-tm2d>` de la post-traitement.

Les variables temporelles (`TIME STEP` et `NUMBER OF TIME STEPS`) définissent la longueur de simulation. Les périodes d'impression (`GRAPHIC PRINTOUT PERIOD` et `LISTING PRINTOUT PERIOD`) définissent la fréquence de sortie des résultats. Plus la période d'impression est petite**, plus la simulation sera longue** parce que l'écriture des résultats prend du temps. Les périodes d'impression (fréquences) se rapportent à un multiple du paramètre `TIME STEPS` et doivent être un nombre inférieur à celui de `NUMBER OF TIME STEPS`. Pour en savoir plus sur les paramètres des étapes temporelles, consultez le [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) dans les sections 5 et 12.4.2.

En outre, le paramètre `MASS-BALANCE : YES` affichera des flux de masse et des erreurs dans la région de calcul, qui est un paramètre important pour vérifier la plausibilité du modèle. Notez que ce mot-clé n'autorise que les impressions de bilan de masse et n'impose pas le bilan de masse du modèle, qui doit être réalisé grâce à une configuration de modèle cohérente suivant ce tutoriel et le [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).

````{admonition} Expand to review the GENERAL PARAMETERS used in this tutorial
:class: note, dropdown
```fortran
TITLE : '2d steady flow'
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE : qgismesh.slf
RESULTS FILE : r2dsteady.slf
/
MASS-BALANCE : YES / activates mass balance printouts - does not enforce mass balance
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F / Q enables boundary flux equilibrium controls
/
TIME STEP : 1.
NUMBER OF TIME STEPS : 15000
GRAPHIC PRINTOUT PERIOD : 200
LISTING PRINTOUT PERIOD : 100
```
````

(tm2d-numerical)=
### Paramètres numériques généraux

**Les descriptions suivantes se rapportent à la section 7.1 du [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Telemac2d est livré avec trois solveurs pour approximer la moyenne de profondeur {term}`Équations de Navier-Stokes <Navier-Stokes equations>` (i.e., le {term}`Équations <Shallow water equations>`) {cite:p}`kundu_fluid_2008` (p. 262) qui peut être choisi en ajoutant le mot-clé **EQUATIONS** au fichier `*.cas`:

* `EQUATIONS : SAINT-VENANT FE` est le **default** qui fait que Telemac2d utilise une méthode d'élément fini de Saint-Venant,
* `EQUATIONS : SAINT-VENANT FV` fait Telemac2d utiliser une méthode de volume fini de Saint-Venant, et
* `EQUATIONS : BOUSSINESQ` fait Telemac2d utiliser le {term}`approximation de Boussinesq <Boussinesq approximation>`, qui suppose une densité constante (hypothèse de fluide incroyable) et ne doit pas être confondu avec le {term}`hypothèse de Boussinesq <Boussinesq hypothesis>`.

En outre, un type de discrétisation doit être spécifié avec le mot-clé **DISCRETISATIONS IN SPACE**, qui est une liste de cinq valeurs entières. Les cinq éléments de la liste définissent des schémas de discrétisation spatiale pour (1) la vitesse, (2) la profondeur, (3) les traceurs, (4) $k-\epsilon$ turbulence, et (5) $\tilde{\nu}$ advection (Spalart-Allmaras), respectivement. La longueur minimale de la liste des mots clés est de 2 (pour la vitesse et la profondeur) et tous les autres éléments sont facultatifs. Les éléments de la liste peuvent prendre les valeurs suivantes définissant la discrétisation spatiale:

* `11` (**default**) active la discrétisation triangulaire (linéaire) dans l'espace (c.-à-d. triangles à 3 nœuds),
* `12` active la discrétisation quasi-bulle avec 4 nœuds, et
* `13` active la discrétisation quadratique avec 6 nœuds.

Le manuel [Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) recommande l'utilisation de **la valeur par défaut de `DISCRETIZATIONS IN SPACE : 11;11`** qui attribue une discrétisation linéaire pour la vitesse et la profondeur de l'eau, qui ** est rapide mais potentiellement instable**. L'option `12;11` peut être utilisée pour réduire les instabilités ou les oscillations de surface libres (p. ex., avec des gradients bathymétriques abrupts). L'option `13;11` augmente la précision des résultats, le temps de calcul, l'utilisation de la mémoire, et elle n'est actuellement pas disponible dans Telemac2d.

De plus, le mot-clé **FREE SURFACE GRADIENT** peut être défini pour augmenter la stabilité d'un modèle. Sa valeur par défaut est `1.0`, mais elle peut être réduite près de zéro pour atteindre la stabilité. Les développeurs proposent une valeur minimale de `0.`, mais des résultats plus réalistes peuvent être obtenus en fixant ce mot-clé à un peu plus de zéro (par exemple, `0.1`). Par exemple, la combinaison de mots clés suivante peut réduire les instabilités de surface (également appelées *wiggles* ou *oscillations*):

```fortran
DISCRETIZATIONS IN SPACE : 12;11
FREE SURFACE GRADIENT : 0.1
```

Par défaut {term}`Advection` est activé par le mot clé `ADVECTION : YES` et il peut être désactivé pour des termes particuliers seulement:

```fortran
ADVECTION OF H : NO / deactivates depth advection
ADVECTION OF U AND V : NO / deactivates velocity advection
ADVECTION OF K AND EPSILON : NO / deactivates turbulent energy and dissipation (k-e model) or Spalart-Allmaras advection
ADVECTION OF TRACERS : NO / deactivates tracer advection
```

Le mot-clé **PROPAGATION** (par défaut : `YES`) oriente la simulation de la propagation et des phénomènes connexes. Par exemple, la propagation invalidante (`PROPAGATION : NO`) désactivera également {term}`Diffusion`. L'inverse, lorsque la propagation est activée, {term}`Diffusion` peut être désactivé séparément. En savoir plus sur {term}`Diffusion` à Telemac2d dans la section {ref}`turbulence <tm2d-turbulence>`.

(tm2d-fe)=
### Éléments finis

**Les descriptions suivantes se rapportent à la section 7.2.1 du [Manuel de Télémac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Telemac2d utilise des éléments finis pour les solutions itératives à {term}`Équations <Shallow water equations>`. Le mot clé **TREATMENT DU SYSTÈME LINEAR** permet de remplacer l'ensemble original d'équations (option `1`) impliquées dans le résolveur d'éléments finis de TELEMAC par une équation d'onde généralisée (option `2`**). Le remplacement (c.-à-d. l'utilisation de l'équation d'onde **généralisée**) est réglé à **par défaut depuis v8p2** et diminue le temps de calcul, mais adoucit les résultats. Cette valeur par défaut (`TREATMENT OF THE LINEAR SYSTEM : 2`) active automatiquement la masse pour la profondeur et la vitesse, et implique une diffusion explicite de la vitesse.

```{admonition} Use SCHEME FOR ADVECTION in lieu of TYPE OF ADVECTION
:class: note, dropdown
Le mot-clé **TYPE OF AVECTION** est une liste de quatre entiers qui définissent les schémas d'advection pour (1) les vitesses (à la fois $u$ et $v$), (2) la profondeur d'eau $h$, (3) les traceurs et (4) les turbulences ($k-\epsilon$ ou $\tilde{\nu}$). La valeur prévue pour (2) profondeur est ignorée puisque v6p0 et une liste de deux valeurs est suffisante en l'absence de traceurs (3) et d'un modèle de turbulence spécifique (4). Ainsi, au lieu de `TYPE OF ADVECTION`, le mot-clé `SCHEME FOR ADVECTION OF VELOCITIES` doit être utilisé. La valeur par défaut est `TYPE OF ADVECTION : 1;5;1;1` (où le `5` pour la profondeur d'eau provient d'une ancienne version Telemac2d et ne déclenche pas le schéma PSI). Toutefois, **le [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) indique que le mot-clé TYPE D'ADVECTION sera supprimé dans les versions futures.**
```

Les mots-clés [Telemac2d handbook](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf)] indiquent que les mots-clés suivants scalar **CHEME POUR ADVECTION** s'appliquent au lieu de la liste de type d'ADVECTION bientôt obsolète :

```fortran
SCHEME FOR ADVECTION OF VELOCITIES : 1 / default
SCHEME FOR ADVECTION OF TRACERS : 1 / default
SCHEME FOR ADVECTION OF K-EPSILON : 1 / default
```

Les trois mots clés `SCHEME FOR ADVECTION` scalar peuvent prendre les valeurs suivantes :

* `1` définit une méthode de caractéristiques non-conservatrice de masse (par défaut pour tous),
* `2` définit un schéma semi-implicit et active le schéma Streamline Upwind Petrov Galerkin (SUPG) (lire plus loin),
* `3`, `4`, `13`, et `14` activer le système dit NERD (ces numéros activent différents systèmes en 3d seulement),
* `5` définit un système de distribution PSI de masse (ne pas utiliser avec les plates-formes de marée), et
* `15` définit le plan ERIA de masse qui fonctionne avec les plates-formes de marée.

Les options `4` et `5` exigent que la condition {term}`Nombre de Courant <CFL>` soit inférieure à 1.

````{admonition} Recommended SCHEME OF ADVECTION ... keywords
:class: tip
Le manuel [Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) recommande des combinaisons spécifiques selon le scénario de simulation.

Pour les modèles **sans zones sèches** utiliser:
```fortran
SCHEME FOR ADVECTION OF VELOCITIES : 4 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 4
```

Pour les modèles avec des plats **tidal** utiliser (comme dans ce tutoriel):
```fortran
SCHEME FOR ADVECTION OF VELOCITIES : 14 / alternatively keep 1
SCHEME FOR ADVECTION OF TRACERS : 5
SCHEME FOR ADVECTION OF K-EPSILON : 14
```
````

**Sans aucun SCHEME D'ADVECTION ...** mot clé, le mot clé **SUPG OPTION** (Streamline Upwind Petrov Galerkin) définit si le remontage s'applique et quel type de remontage s'applique. Le **SUPG OPTION** est une liste de quatre entiers, où chaque élément peut prendre l'une des valeurs suivantes:

* `0` désactive le remontage,
* `1` permet de remonter avec un système SUPG classique (recommandé lorsque la condition {term}`Nombre de Courant <CFL>` est inconnue), et
* `2` permet le remontage avec un schéma SUPG modifié, où le remontage est égal à l'état {term}`Nombre de Courant <CFL>` (recommandé lorsque l'état {term}`Nombre de Courant <CFL>` est petit).

Par défaut, `SUPG OPTION : 2;2;2;2`, où

* le premier élément de la liste se réfère à la vitesse du flux (par défaut `2`),
* la seconde à la profondeur de l'eau (par défaut `2` - défini à `0` quand `MATRIX STORAGE : 3`),
* le troisième aux traceurs (par défaut `2`), et
* le dernier (quatrième) au modèle k-epsilon (par défaut `2`).

Notez que le mot clé `SUPG OPTION` ** n'est pas facultatif** pour de nombreuses combinaisons de mots clés et que ce tutoriel utilise `SUPG OPTION : 0;0;2;2`.

**Paramètres d'implicitation** (**IMPLICITATION POUR LA DÉPENSE**, **IMPLICITATION POUR LES VALEURS** et **IMPLICITATION POUR LA DIFFUSION DE LA VÉLOCITÉ**) s'appliquent à la discrétisation temporelle semi-implicite utilisée dans Telemac2d. Pour permettre la compatibilité des versions croisées, les paramètres d'implicitation doivent être définis dans le fichier `*.cas`. Pour **DEPTH** et **VELOCITÉS** utiliser des valeurs entre `0.55` et `0.60` (**default est `0.55` depuis v8p1**); pour **IMPLICITATION POUR LA DIFFUSION DE VÉLOCITÉ** utiliser `1.0` (default).

La valeur par défaut `TREATMENT OF THE LINEAR SYSTEM : 2` implique ce que l'on appelle **mouvement de masse**, ce qui conduit à un lissage des résultats. Des mots-clés et des valeurs de masse spécifiques sont requis pour l'option de contrôle du flux du mot-clé **TREATMENT OF NEGATIVE DEPTHS** et de la valeur par défaut pour le traitement des plates-formes de marée. À cette fin, les mots-clés de masse doivent être définis comme suit:

```fortran
MASS-LUMPING ON H : 1.
MASS-LUMPING ON VELOCITY : 1.
MASS-LUMPING ON TRACERS : 1.
```

En outre, `MASS-LUMPING FOR WEAK CHARACTERISTICS : 1.` peut être défini, ce qui fera Telemac2d en utilisant des caractéristiques faibles (voir ci-dessous). La valeur par défaut de tout mot clé `MASS-LUMPING ...` est `0.` et la valeur maximale est `1.`, ce qui fait diagonale des matrices de masse.

Le mot-clé **OPTION DES CARACTÉRISTIQUES** définit la méthode des caractéristiques qui peuvent prendre un formulaire **fort (par défaut de `1`)** ou **faible (`2`)**. Une forme faible diminue {term}`Diffusion`, est plus conservatrice, et augmente le temps de calcul. Télémac2d passe automatiquement de la forme forte par défaut (`1`) à la forme faible (`2`) lorsque

* le `TYPE OF ADVECTION` est fixé à `1`,
* tout `SCHEME FOR ADVECTION ...` est défini à `1`, ou
* n'importe quel `SCHEME OPTION FOR ADVECTION OF ...` est fixé à `2`.

Aucune de ces options ne doit être utilisée avec des traceurs parce qu'ils ne sont pas de grande conservation.

(steady2d-fv)=
### Volumes finis

La méthode du volume fini est mentionnée ici pour l'exhaustivité et des descriptions détaillées sont disponibles à la section 7.2.2 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf), et l'exemple de malpasset (`telemac/v9.0.0/examples/telemac2d/malpasset/`). Pour activer le schéma de volume fini utiliser:

```fortran
EQUATIONS : 'SAINT-VENANT FV' / the apostrophes are strictly needed here
```


```{admonition} Use finite volumes only with v8p2 or later
Les versions antérieures du résolveur de volume fini de Telemac2d sont buggy, mais depuis les améliorations majeures ont été mises en œuvre avec v8p2, les nouvelles versions fonctionnent stable.
```

La méthode du volume fini implique la définition d'un schéma à travers le mot clé **FINITE VOLUME SCHEME** qui peut prendre l'une des valeurs entières suivantes:

* `0` permet le schéma {cite:t}`roe1981ars`
* `1` est le **default** et permet le schéma cinétique {cite:p}`audusse2000`,
* `3` permet le plan {cite:t}`zokagoa2010` qui est incompatible avec les appartements de marée,
* `4` permet le plan {cite:t}`tchamen1998` pour modéliser le mouillage et le séchage d'une bathymétrie complexe,
* `5` permet le programme Harten Lax Leer-Contact (HLLC) {cite:p}`toro2009a`, et
* `6` permet le flux moyen pondéré (WAF) {cite:p}`ata2012` plan pour lequel le parallélisme n'est pas actuellement implémenté.

Les schémas de volume/éléments finis sont (semi-) explicites et potentiellement sujets à l'instabilité. Pour cette raison, il est recommandé de définir une condition {term}`Nombre de Courant <CFL>` et une étape de temps variable :

```fortran
DESIRED COURANT NUMBER : 0.9
VARIABLE TIME-STEP : YES / default is NO
DURATION : 15000
```

Le mot-clé **DURATION** est requis pour mettre fin à la simulation.

L'étape de temps variable causera des sorties irrégulières de listage, tandis que la fréquence de sortie graphique est écrite en fonction du **TIME STEP**. Notez que **ce tutoriel utilise `VARIABLE TIME-STEP : NO`**.

Le mot-clé **FINITE VOLUME SCHEME TIME ORDER** définit le second ordre de temps, qui est par défaut défini à *Euler explicite* (`1`). Définir l'ordre du schéma temporel à `2` rend Telemac2d en utilisant le schéma Newmark où un coefficient d'intégration peut être utilisé pour modifier le paramètre d'intégration. Notez que `NEWMARK TIME INTEGRATION COEFFICIENT : 1` correspond à *Euler explicite*. Pour implémenter ces options dans le fichier de direction, utilisez les paramètres suivants :

```fortran
FINITE VOLUME SCHEME TIME ORDER : 2 / default is 1 - Euler explicit
NEWMARK TIME INTEGRATION COEFFICIENT : 0.5 / default is 0.5
```

Cependant, d'autres tutoriels et le forum Telemac recommandent d'utiliser les paramètres de schéma suivants pour les volumes finis:

```fortran
FINITE VOLUME SCHEME : 5 / HLLC
FINITE VOLUME SCHEME SPACE ORDER : 1
FINITE VOLUME SCHEME TIME ORDER : 1
```


Les recommandations de mots clés supplémentaires pour le schéma de volume fini sont les suivantes:

```fortran
OPTION FOR THE DIFFUSION OF VELOCITIES : 2 / only option to get mass conservation but can cause problems with tidal flats
SCHEME FOR ADVECTION OF VELOCITIES : 3 / use 3, also for FV - MATRIX STORAGE must be 3
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4 / overrides SUPG OPTION and OPTION FOR CHARACTERISTICS
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2 / increase for higher accuracy and longer computing time, requires SCHEME OF ADVECTION 3,4,5, or 15 and OPTION 2,3,4
TYPE OF SOURCES : 2 / 2=Dirac is the only possibility for mass conservation, the default=1 means linear function and is not mass conservative
CONTINUITY CORRECTION : YES / particularly important when not only discharge but also depth is imposed at boundaries
```

Selon le type d'analyse, les paramètres liés au solveur de **SOLVER**, **SOLVER OPTIONS**, **MAXIMUM NUMÉRO D'ITERATION POUR SOLVER** et **TIDAL FLATS** peuvent également être modifiés. Plus précisément, tous les mots-clés **TIDAL FLAT** deviennent **obsolètes avec le schéma FV**.

(tm2d-solver-pars)=
### Paramètres du solvant numérique

** Les descriptions suivantes se rapportent à la section 7.3.1 du [Manuel de Télémac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Le solveur peut être sélectionné et spécifié avec les mots-clés **SOLVER**, **SOLVER FOR DIFFUSION OF TRACERS** et **SOLVER FOR K-EPSILON MODEL** où les paramètres suivants sont recommandés :

```fortran
SOLVER : 1 / default is 3
SOLVER FOR DIFFUSION OF TRACERS : 1
SOLVER FOR K-EPSILON MODEL : 1
```

Le paramètre **SOLVER** à `1` au lieu de la valeur par défaut de `3` est recommandé avec `TREATMENT OF THE LINEAR SYSTEM : 2` (i.e., la valeur par défaut depuis v8p2) pour les fichiers de direction cohérents et compatibles avec l'arrière.

Every solver keyword can take an integer value between `1` and `8`, where `1`-`6` use conjugate gradient methods:

* `1` définit la méthode du gradient conjugué pour les matrices symétriques,
* `2` définit la méthode résiduelle conjuguée,
* `3` définit le gradient conjugué sur la méthode d'équation normale,
* `4` définit la méthode d'erreur minimale,
* `5` définit la méthode du gradient conjugué carré,
* `6` définit la méthode du gradient biconjugal stabilisé (BICGSTAB),
* `7` définit la méthode *Generalized minimum RESidual* (**GMRES**), et
* `8` définit le résolveur direct de l'Université Yale (YSMP) qui n'est pas compatible avec le parallélisme.

La méthode **GMRES peut être activée avec le schéma d'éléments finis** avec les options de solveur suivantes pour le {term}`Sous-espaces de Krylov <Krylov space>`:

```fortran
SOLVER OPTION : 2 / hydrodynamic propagation
SOLVER OPTION FOR TRACERS DIFFUSION : 2 / tracer diffusion
OPTION FOR THE SOLVER FOR K-EPSILON MODEL : 2 /  k-e or Spalart-Allmaras
```

Les options de solveur varient entre les valeurs de **`2` pour une petite maille** et **`5` pour une grande maille**. Les entiers de `3` ou `4` peuvent être utilisés pour les mailles moyennes. Le [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) recommande d'exécuter des simulations à plusieurs reprises pour trouver une valeur optimale, où des valeurs plus élevées (à proximité de `5`) augmentent le temps nécessaire à une itération mais conduisent à une convergence plus rapide.

(tm2d-accuracy)=
### Précision numérique

**Les descriptions suivantes se rapportent à la section 7.3.2 du [Manuel de Télémac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Les mots-clés de précision font que Telemac2d arrête une itération lorsque deux solutions consécutives pour le même élément varient de moins d'un seuil **ACCURACY**. À cette fin, les seuils de précision par défaut suivants peuvent être modifiés (Telemac2d ignore les paramètres non pertinents):

```fortran
SOLVER ACCURACY : 1.E-4 / propagation steps
ACCURACY FOR DIFFUSION OF TRACERS : 1.E-6 / tracer diffusion
ACCURACY OF K : 1.E-9 / diffusion and source terms of turbulent energy transport
ACCURACY OF EPSILON : 1.E-9 / diffusion and source terms of turbulent dissipation transport
ACCURACY OF SPALART-ALLMARAS : 1.E-9 / diffusion and source terms of the Spalart-Allmaras equation
```

Dans l'expérience, la précision du solveur ne doit pas être supérieure à `1.E-3` (10$^{-3}$). En revanche, de très petites exactitudes entraîneront des temps de calcul plus longs. En plus ou alternativement aux mots-clés de précision, les nombres par défaut suivants d'itérations maximales peuvent être modifiés pour accélérer les calculs:

```fortran
MAXIMUM NUMBER OF ITERATIONS FOR SOLVER : 100 / maximum number of iterations when solving the propagation step
MAXIMUM NUMBER OF ITERATIONS FOR DIFFUSION OF TRACERS : 60 / tracer diffusion
MAXIMUM NUMBER OF ITERATIONS FOR K AND EPSILON : 50 / diffusion and source terms of k-e or Spalart-Allmaras
```

Telemac2d imprimera des messages d'avertissement lorsque la convergence n'a pas pu être atteinte avec la combinaison définie de la précision et du nombre maximal de mots clés d'itération. Les impressions du message d'avertissement peuvent être désactivées avec le mot-clé **INFORMATION À PROPOS DE SOLVER**, mais il n'est pas recommandé de désactiver les avertissements de convergence.

(tm2d-tidal)=
### Plats à marée

**Les descriptions suivantes se réfèrent à la section 7.5 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Le mot-clé **TIDAL FLATS (par défaut: `YES`)** s'applique uniquement au schéma des éléments finis ({ref}`EQUATIONS keyword <tm2d-numerical>`) et peut être ignoré avec {ref}`finite volumes <steady2d-fv>`**. Le terme *tidal* peut être légèrement déroutant parce que les plates-formes de marée peuvent se produire au-delà des régions côtières: Les plates-formes de marée peuvent se produire partout où l'on peut moudre et sécher les cellules de la grille ou lors de transitions d'écoulement (p. ex., lorsque l'eau qui coule rapidement entre dans une zone d'eau souterraine). Le mouillage et le séchage, et les transitions d'écoulement se produisent dans presque tous les environnements plus complexes qu'une flume carrée, et par conséquent, l'activation des plates-formes de marée dans les modèles Telemac2d est fortement recommandée. Bien que l'activation des plates-formes de marée entraîne des temps de calcul plus longs, dans la plupart des cas, un calcul avec des plates-formes de marée fournit des résultats physiquement raisonnables.


Le mot-clé **TIDAL FLATS** est lié à quelques autres mots-clés Telemac2d qui conduisent à la stabilité du modèle et à la signification physique. Les configurations de mots clés suivantes peuvent généralement être appliquées aux cours d'eau et aux canaux (quasi) stables et réels (par opposition aux flumes de laboratoire avec géométries simplifiées):

```fortran
TIDAL FLATS : YES
CONTINUITY CORRECTION : YES / default is NO
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2 / value 2 or 3 is required with tidal flats
```

L'OPTION DE TRAITEMENT DES PLAQUES TIDALES** accepte les valeurs entières entre `1` et `3` pour choisir l'une des options suivantes :

* `1` détecte les plans de marée et corrige le gradient de surface libre.
* `2` supprime les éléments plats de marée en utilisant une table de masquage qui élimine toute contribution des éléments de maille concernés. Cette option peut affecter la conservation de masse du modèle.
* `3` ressemble à `1`, mais ajoute un terme de porosité aux éléments de maille semi-sec. Cela affecte la quantité d'eau dans le modèle, qui équivaut ici à la profondeur intégrale multipliée par la porosité. Un fichier utilisateur Fortran peut être utilisé pour modifier le terme porosité dans le sous-routine `USER_CORPOR`.

Le mot-clé **TREATMENT OF NEGATIVE DEPTHS (par défaut: `1`)** définit une approche pour éliminer les valeurs négatives de profondeur d'eau où les nombres entiers suivants peuvent être utilisés:

* `0` désactive tout traitement des profondeurs d'eau négatives.
* `1` adoucit avec prudence les profondeurs d'eau négatives (**par défaut**).
  * Un mot clé du numéro flottant `THRESHOLD FOR NEGATIVE DEPTHS` (par défaut: `0.`) est disponible uniquement pour cette option.
  * En fixant le seuil à, par exemple, `-0.1`, les profondeurs d'eau négatives (p. ex. -0,05 m) par rapport à -0,1 mètres restent inchangées.
* `2` impose une limite de flux qui assure strictement des profondeurs d'eau positives.
* `3` agit de la même manière que `2`, mais pour le plan ERIA {term}`Advection` (set `SCHEME FOR ADVECTION OF TRACERS` à `4` ou `5`). Cette option est appropriée pour modéliser des traceurs conservateurs.

````{admonition} TIDAL FLATS options require particular keyword combinations
:class: tip
Les mots-clés (voir la section {ref}`finite element parameters <tm2d-fe>`) doivent être définis pour **TRACERS** à LIPS (soit `4` ou `5`), et pour tous les autres à NERD (`13` ou `14`) ou au schéma ERIA (`15`).

Lorsque vous utilisez LIPS (`4` ou `5`) avec NERD (`13` ou `14`) utilisez la combinaison suivante (**utilisée dans ce tutoriel**):
```fortran
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2
```

Lorsque vous utilisez LIPS (`4` ou `5`) avec ERIA (`15`) utilisez la combinaison suivante :
```fortran
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 3
```

Pour en savoir plus sur les combinaisons de paramètres viables ou perturbateurs pour les plates-formes de marée à la section 16.5 du [Télémac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).
````

### Manipulation des matrices

**Les descriptions suivantes se réfèrent à la section 7.6 du [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Telemac2d fournit plusieurs options pour la gestion matricielle qui doivent être mises en place pour certains systèmes de solveur.

Le mot clé **MATRIX STORAGE** peut être défini comme suit:

* `1` pour utiliser le stockage matriciel classique élément par élément.
* `3` pour utiliser le stockage matriciel basé sur le bord (par défaut). Ce paramètre par défaut est requis lorsque tout mot-clé **CHEM POUR L'ADOPTION ...** est défini à `3`, `4`, `5`, `13`, `14` ou `15`, et lorsque tout mot-clé direct **SOLVER** est défini à `8`.

Le mot-clé supplémentaire **MATRIX-VECTOR PRODUCT** peut être utilisé pour changer de méthode de multiplication pour le schéma d'éléments finis. Cependant, la valeur par défaut de `1` (multiplication vectorielle par une matrice non assemblée) ne doit pas être modifiée** car la seule alternative (`2` pour la multiplication matricielle assemblée frontale) n'est pas implémentée pour le parallélisme et la discrétisation quasi bulle.


(tm2d-bounds)=
### Conditions limites

**Les descriptions suivantes des paramètres de frottement se réfèrent à la section 4.2 du [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Mots-clés relatifs aux limites de liquides attribuent des propriétés hydrauliques aux lignes de limites de liquides définies spatialement en amont et en aval dans le fichier Conlim (`*.cli`) {ref}`created with BlueKenue <bk-liquid-bc>`. Cette section présente l'attribution de limites de liquide stables pour un rejet de 35 m$^3$/s. À cette fin, l'état de la limite en amont est fixé à un débit cible constant (*Ouvrir la limite avec Q* prescrite) et l'état de la limite en aval reçoit une affectation {term}`Courbe d'étalonnage <Stage-discharge relation>` (*Ouvrir la limite avec Q et H* prescrits) (appeler {numref}`Fig. %s <bk-bc-types>`). Ainsi, pour exécuter ce tutoriel, ajoutez les mots-clés suivants au fichier de direction (`*.cas`) :

* Le mot-clé `PRESCRIBED FLOWRATES : 35.;0.` assigne un débit de 35 m$^3$/s au bord de la frontière **en amont** et n'impose pas de débit au bord de la frontière **en aval**. La prescription en aval `Q` de 0.0 fait que Telemac2d ignore cette valeur correspondant à la limite en aval (profondeur prescrite seulement).
* Le mot clé `PRESCRIBED ELEVATIONS : 374.80565;371.33` assigne une élévation de la surface de l'eau $wse$ (ou H dans Telemac) en mètres au-dessus du niveau de la mer (m a.s.l.) aux limites **en amont** et **en aval**.

L'ordre des débits prescrits (Q) et des valeurs $wse$ (H) dépend de l'ordre de la définition des limites. Ainsi, le premier élément de liste définit les valeurs pour l'élément en amont et le deuxième élément de liste pour la limite ouverte en aval.

````{admonition} How to find out the order of boundary conditions?
:class: tip
L'ordre des limites ouvertes peut être lu à partir du fichier `*.cli`. La première limite ouverte qui est listée dans le fichier `*.cli` correspond au premier élément de la liste dans n'importe quel mot clé **PRESCRIBED ...**. Un nœud de frontière ouvert dans le fichier `*.cli` est caractérisé par une ligne commençant par quelque chose comme `4 5 5` ou `5 5 5` (i.e., tout sauf `2 2 2`, qui correspond à un noeud de frontière de mur fermé) et BlueKenue marque également les noms de frontières ouvertes aux extrémités de la ligne (après le hashtag). {numref}`Figure %s <boundary-cli>` illustre le fichier [boundarys.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli) utilisé dans ce chapitre où la limite ouverte `upstream` est définie à la ligne 7, avant la définition de la limite ouverte en aval à partir de la ligne 313.

```{figure} ../../img/telemac/boundary-cli.png
:alt: telemac 2d cli boundary conditions order cas steering file prescribed prescription
:name: boundary-cli

Le fichier [boundarys.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli) utilisé dans ce tutoriel commence par la limite en amont définie à la ligne 7. Pour trouver la limite en aval défiler vers le bas jusqu'à la ligne 313.
```
````

Les conditions limites liquides peuvent être attribuées à toute limite ouverte dans le fichier `*.cli`.

````{admonition} External files instead of PRESCRIBED-keywords
:class: note, dropdown
Au lieu d'une liste de nombres semi-colons séparés dans le fichier de direction, les conditions de limite liquide peuvent également être définies avec un fichier de condition de limite liquide au format texte *ASCII*. À cette fin, les mots clés `LIQUID BOUNDARIES FILE` et/ou `STAGE-DISCHARGE CURVES FILE` doivent être définis dans le fichier de direction. Des fichiers externes sont nécessaires pour la simulation des débits quasi instables (p. ex., un hydrographe d'inondation ou des séquences à faible débit pour les conditions d'habitat) et plus de détails peuvent être trouvés aux sections 4.2.5 et 4.2.6 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) ou {ref}`unsteady section in this eBook <chpt-unsteady>`.
````

Un type de profil de vitesse peut être attribué à n'importe quelle limite ouverte prescrite Q (flux) ou U (vitesse) sous la forme d'une liste qui a le même ordre d'éléments que les mots-clés définis ci-dessus **PRESCRIBED ...**. À cette fin, les profils de vitesse en amont et en aval peuvent être définis avec le mot clé **VELOCITY PROFILS** qui accepte les valeurs suivantes:

* `1` est l'option **default** qui définit la direction de la vitesse d'écoulement aux nœuds limites normaux à leurs bords. Cette option attribue une longueur de 1 au vecteur et le multiplie avec un facteur numérique pour obtenir un débit cible.
* `2` lit les profils de vitesse U et V à partir du fichier des conditions limites (`*.cli`) qui sont multipliés par une constante pour obtenir un débit cible.
* `3` impose la direction du vecteur de vitesse normale à la limite et lit la valeur (UBOR) à partir du fichier `*.cli`, qui est ensuite multiplié par une constante pour donner un débit cible.
* `4` impose la direction du vecteur de vitesse normale à la limite et calcule la norme de la valeur proportionnelle à la racine carrée de la profondeur de l'eau. Cette option ne peut être utilisée qu'à l'aide d'une limite ouverte Q* prescrite.
* `5` impose la direction du vecteur de vitesse normale à la limite et calcule la norme de la valeur proportionnelle à la racine carrée d'une profondeur d'eau virtuelle.

La limite amont étant une limite Q* prescrite, ce tutoriel utilise `VELOCITY PROFILES : 4;1` dans le fichier de direction. Pour en savoir plus sur les options pour définir les profils de vitesse à la section 4.2.8 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).


```{admonition} Boundary conditions and mass balance
:class: tip

Les paramètres des conditions limites affectent le bilan massique, qui est un critère crucial pour un modèle numérique sonore. En savoir plus sur la mise en place {ref}`boundary conditions for mass balance <foc-mass-bc>`.
```


(tm2d-init-dry)=
### Conditions initiales

**Les descriptions suivantes se réfèrent à la section 4.1 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Les conditions initiales décrivent l'état du modèle au début d'une simulation. Telemac2d reconnaît les types de conditions initiales suivants, qui peuvent être définies dans le dossier de pilotage avec le mot clé `INITIAL CONDITIONS : 'TYPE'` où `TYPE` peut être l'une des suivantes:

* `ZERO ELEVATION` initialise l'élévation de surface libre à 0 (**par défaut**). Ainsi, les premières profondeurs d'eau correspondent à l'altitude du fond.
* `CONSTANT ELEVATION` initialise l'élévation de surface libre à une valeur définie par un mot-clé **INITIAL ELEVATION** qui a une valeur par défaut de `0.`. Ainsi, les profondeurs d'eau initiales correspondent à la soustraction de l'élévation du fond de l'élévation de la surface de l'eau $wse$. La profondeur initiale de l'eau est fixée à zéro aux noeuds où l'élévation du fond est supérieure à celle définie par le mot-clé **INITIAL ELEVATION**.
* `ZERO DEPTH` initialise la simulation avec `0` (i.e., $wse$ correspond à l'élévation inférieure). Ainsi, le modèle commence par des conditions sèches, semblables à celles du tutoriel {ref}`BASEMENT <basement2d>`.
* `CONSTANT DEPTH` initialise les profondeurs d'eau à une valeur définie par un mot-clé **INITIAL DEPTH** qui a une valeur par défaut de `0.`.
* `TPXO SATELLITE ALTIMETRY` initialise le modèle à l'aide d'informations fournies par une base de données définie par l'utilisateur (par exemple, le [modèle TPXO de l'OSU pour les marées océaniques](http://g.hyyb.org/archive/Tide/TPXO/TPXO_WEB/global.html)). Pour en savoir plus à la section 4.2.12 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) sur la modélisation des systèmes marins.

Pour commencer, définissez la profondeur initiale de l'eau comme 0 avec le mot clé suivant, ce qui signifie que le modèle sera initialisé avec un lit de rivière sec:

```fortran
INITIAL CONDITIONS : 'ZERO DEPTH'
```

La vitesse de simulation peut être significativement augmentée lorsque le modèle a déjà fonctionné une fois à la même décharge (initiale). Le résultat d'une simulation antérieure peut être utilisé pour la condition initiale avec les mots-clés `COMPUTATION CONTINUED : YES` (par défaut `NO`) et `PREVIOUS COMPUTATION FILE : *.slf` (fournir le nom d'un fichier `*.slf`). Ce type d'initialisation du modèle est également appelé *hotstart*. Pour en savoir plus sur les hotstarts dans les sections {ref}`unsteady simulation <tm2d-hotstart>` et {ref}`Gaia <gaia-hotstart>`. Aussi, la section 4.1.3 du [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) fournit des descriptions pour les calculs continus (hotstart).


````{admonition} Wet the model at the beginning

Utilisez un état initial *constante* de l'eau *profondeur* de `1` (entier) pour accélérer les calculs, ce qui correspond à un état de modèle initial complètement inondé (excédent de volume d'eau). Cependant, cette initialisation de type placera également une couche d'eau épaisse de 1 m au-delà des berges de la rivière, où l'eau pourrait ne pas être en mesure de s'écouler. Ainsi, les flaques sont susceptibles de se former longitudinalement le long des limites solides `2 2 2`.

```fortran
INITIAL CONDITIONS : 'CONSTANT DEPTH'
INITIAL DEPTH : 1
```

Dans le cas de simulations delta, une condition initiale définie par `CONSTANT ELEVATION` pourrait être de préférence définie au niveau d'un lac ou d'une mer.
````

(tm2d-friction)=
### Friction (douceur)

**Les descriptions suivantes des paramètres de frottement se rapportent à la section 6.1 du [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Le mot-clé **LAW OF BOTTOM FRICTION** définit un modèle de rugosité pour les limites topographiques, qui peut être défini comme suit:

* `0` sans friction.
* `1` pour l'équation {cite:t}`haaland1983`, qui est une forme implicite de l'équation {cite:t}`colebrook1937` qui s'appuie sur le facteur de frottement de Darcy-Wesbach $f_D$. Cette loi comporte un degré élevé d'incertitude découlant de l'ensemble de données expérimentales de l'auteur original.
* `2` pour la rugosité {cite:t}`chezy_formula_1776` qui peut également être utilisée comme `3` et `4`.
* `3` pour {cite:t}`strickler_beitrage_1923` rugness $k_{st}$ (en savoir plus, par exemple, sur le {ref}` 1d hydraulics exercise <ex-1d-hydraulics>`), qui est l'inverse de $n_m$ (`4`).
* `4` pour {cite:t}`manning_transactions_1891` rugness $n_m$ (en savoir plus, par exemple, sur le {ref}` 1d hydraulics exercise <ex-1d-hydraulics>`), qui est l'inverse de $k_{st}$ (`3`).
* `5` for the {cite:t}`nikuradse_stromungsgesetze_1933` roughness law, which should correspond to 3 $\cdot D_{90}$ according to {cite:t}`vanrijn2019`.
* `6` pour la loi logarithmique du mur pour les flux turbulents. Cette option suppose que la vitesse d'écoulement moyenne est une fonction logarithmique de la distance de la paroi au-delà des couches visqueuses et tampons. L'épaisseur de ces couches est fonction de la longueur de rugosité de la paroi {cite:p}`von_karman_mechanische_1930`.
* `7` pour l'équation {cite:t}`colebrook1937` qui calcule le facteur de frottement de Darcy-Weisbach $f_D$ pour les flux turbulents dans les tuyaux lisses.

En ce qui concerne les applications 2d de ce livre électronique, les modèles de rugosité les plus pertinents sont `3` {cite:p}`strickler_beitrage_1923`, `4` {cite:p}`manning_transactions_1891`, et `6` (loi sur les journaux). La loi {cite:t}`nikuradse_stromungsgesetze_1933` rugness (`5`) est recommandée pour les simulations 3d (voir {ref}`Telemac3d tutorial <chpt-telemac3d-slf>`). La friction est plus généralement appelée avec le coefficient général $c_{f}$, qui a une pertinence particulière pour le transport {term}`charge de fond <Bedload>` (cf. {ref}`morphodynamic calculations with Gaia <c-friction>`).

The **FRICTION COEFFICIENT FOR THE BOTTOM** keyword sets the value for a characteristic roughness coefficient. For instance, when the friction law keyword is set to `3` {cite:p}`strickler_beitrage_1923`, the friction corresponds to the Strickler roughness coefficient $k_{st}$ (in fictive units of m$^{1/3}$ s$^{-1}$). For rough channels (e.g., mountain rivers) $k_{st} \approx 20$ m$^{1/3}$ s$^{-1}$ and for smooth concrete-lined channels $k_{st} \approx 75$ m$^{1/3}$ s$^{-1}$. In fully turbulent flows, the Strickler roughness can be approximated with $k_{st} \approx \frac{26}{D_{90}^{1/6}}$ {cite:p}`meyer-peter_formulas_1948` where $D_{90}$ is the grain diameter of which 90% of the surface grain mixture are finer.
This tutorial features the application of a *Manning* roughness coefficient of $n_m$= 0.03, which is the inverse of $k_{st}$ and implemented with:

```fortran
LAW OF BOTTOM FRICTION : 4 / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
```

````{dropdown} Expand to see exemplary values for Manning roughness
{numref}`Table %s <tab-mannings-n>` liste des valeurs exemplaires pour le coefficient de rugosité de Manning $n_m$ basé sur {cite:t}`usgs1973_n` et {cite:t}`usgs1989_n`.

```{list-table} Exemplary values for Manning roughness for straight uniform channels.
:header-rows: 1
:name: tab-mannings-n

* - Type de surface
  - Diamètre du matériau (10$^{-3}$m)
  - $n_m$ (m$^{-1/3}$s)

* - Béton
  - $-$
  - 0,012-0,018

* - Sol ferme
  - $-$
  - 0,025-0,032

* - Sable grossier
  - 1-2
  - 0,026-0,035

* - Gravel
  - 2-64
  - 0,028-0,035

* - Corbeille
  - 64-256
  - 0,030-0,050

* - Boulder
  - $>$ 256
  - 0,040-0,070
```
````

```{admonition} Friction zones (regional friction values)
:class: tip, dropdown

Pour créer des zones avec des valeurs de friction différentes, jetez un coup d'œil à l'attention sur {ref}`roughness zones <tm-friction-zones>`.
```

En outre, des conditions de rugosité spécifiques doivent être définies pour les limites de liquide (voir {ref}`above <tm2d-bounds>`), qui ne doivent pas être modifiées dans le processus d'étalonnage du modèle plus tard. À cette fin, un **mesuré {term}`Courbe d'étalonnage <Stage-discharge relation>`** est nécessaire pour recalculer l'hydraulique moyenne de section. Pour cela, jetez un œil à la formule {ref}`Python exercise on 1-d hydraulics for solving the Manning-Strickler <ex-1d-hydraulics>`.

```fortran
LAW OF FRICTION ON LATERAL BOUNDARIES : 3 / integer (3 is Strickler)
ROUGHNESS COEFFICIENT OF BOUNDARIES : 33.3 / float inverse of n_m=0.03
```

```{admonition} Differentiate between bottom and boundary friction
:class: important

Ne pas utiliser les deux mots clés définissant le frottement aux limites fera que tout étalonnage de rugosité affecte le bilan massique.
```


(tm2d-turbulence)=
### Turbulence

**Les descriptions suivantes se réfèrent à la section 6.2 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

La turbulence décrit un état apparemment aléatoire et chaotique du mouvement du fluide sous la forme de tourbillons tridimensionnels. La vraie turbulence n'est présente que dans la vorticité 3d et lorsqu'elle se produit, elle domine surtout tous les autres phénomènes de flux par des augmentations de dissipation d'énergie, de traînée, de transfert de chaleur et de mélange {cite:p}`kundu_fluid_2008`. Le phénomène des turbulences est un mystère pour la science depuis longtemps, depuis que des flux turbulents ({term}`read more about the implementation in RANS <RANS>`) ont été observés, mais ne peuvent s'expliquer par les systèmes d'équations linéaires. Aujourd'hui, la turbulence est considérée comme un phénomène aléatoire qui peut être pris en compte dans les équations linéaires, par exemple, en introduisant des paramètres statistiques. Par exemple, lorsque la turbulence s'applique à la moyenne de profondeur {term}`Équations de Navier-Stokes <Navier-Stokes equations>`, une solution numérique pour une quantité (par exemple, vitesse de débit) correspond à $value = \overline{mean value} + value fluctuation'$. À cette fin, il existe une variété d'options pour mettre en œuvre les turbulences dans les modèles numériques {cite:p}`nezu1993`.

Les dimensions horizontales et verticales des tourbillons turbulents peuvent varier considérablement, en particulier dans les cours d'eau et les transitions vers les zones d'aval (plats de marée) où la large dimension horizontale du débit (largeur de rivière $w$) est significativement plus grande que la dimension verticale du débit (profondeur d'eau $h$): $w >> h$. Telemac2d fournit des modèles de turbulences multiples qui peuvent être appliqués aux dimensions verticales et/ou horizontales et définis avec le mot-clé **TURBULENCE MODEL** étant un nombre entier pour l'une des options suivantes:

* `1` pour utiliser un coefficient de viscosité constant (**default**) pour la viscosité turbulente, la viscosité moléculaire et {term}`Diffusion`. Cette option de fermeture ne doit pas être utilisée avec {term}`Courbe d'étalonnage <Stage-discharge relation>` les limites ouvertes (c.-à-d. ne pas utiliser avec Q et H prescrits) {cite:p}`wilson2002`.
* `2` to use the Elder formula for the {term}`Diffusion` coefficient $D$. The Elder turbulence closure also yields small errors for {term}`Courbe d'étalonnage <Stage-discharge relation>` open boundaries (i.e., do not use this option with prescribed Q and H) {cite:p}`wilson2002`.
* `3` to use the $k-\epsilon$ two-equation model solving the {term}`Équations de Navier-Stokes <Navier-Stokes equations>`. The first equation represents a turbulence closure for the {term}`turbulent kinetic energy <Turbulent kinetic energy>` $k$; the second equation is a turbulence closure for the turbulent dissipation $\epsilon$. Both equations express that the sum of change of (I) $k$ and $\epsilon$ in time, and (II) {term}`Advection` transport of $k$ and $\epsilon$ equal the sum of (1) {term}`Diffusion` transport of $k$ and $\epsilon$, (2) the production rate of $k$/$\epsilon$, and (3) the destruction rate of $k$/$\epsilon$ {cite:p}`launder1974`. The $k-\epsilon$ model is a generalization of the mixing length model (see option `5`) and assumes that the turbulent viscosity is isotropic (valid for many river applications, but not for circular-rotating flows or groundwater) {cite:p}`bradshaw1987`. Thus, the $k-\epsilon$ model introduces two additional equations and requires a finer mesh than the constant viscosity option `1`, which leads to a longer computation time. Yet, the $k-\epsilon$ model generally yields accurate results and small errors with {term}`Courbe d'étalonnage <Stage-discharge relation>` open boundaries {cite:p}`wilson2002`. The following default keywords are associated with the $k-\epsilon$ model:
  * `VELOCITY DIFFUSIVITY : 1.E-6` correspondant à la viscosité cinématique $\nu$ de l'eau (10$^{-6}$ m$^2$/s).
  * `TURBULENCE REGIME FOR SOLID BOUNDARIES : 2` **pour les murs bruts** des limites fermées pour appliquer la valeur choisie pour les mots-clés **LAW OF BOTTOM FRICTION** et **ROUGHNESS COEFFICIENT OF BOUNDARIES** (appelez la section {ref}`tm2d-friction`). Pour **smooth murs frontières fermés** set `TURBULENCE REGIME FOR SOLID BOUNDARIES : 1`.
  * `INFORMATION ABOUT K-EPSILON MODEL : YES` permet la sortie de console d'informations sur la solution de fermeture $k-\epsilon$.
* `4` pour utiliser le modèle {cite:t}`smagorinsky1963` (également connu sous le nom de * circulation générale*), qui découle de la modélisation climatique. Il représente une simulation ** grand eddy** (LES, contrairement à {term}`Moyenne de Reynolds <RANS>`). Le modèle {cite:t}`smagorinsky1963` ne tient pas compte de {term}`Diffusion`.
* `5` pour utiliser un modèle de longueur de mélange selon la théorie de Prandtl qu'une quantité de fluide conserve ses propriétés pour une longueur caractéristique avant de se mélanger avec le flux en vrac {cite:p}`bradshaw1974`.
* `6` pour utiliser le modèle {cite:t}`spalart1992` one-equation {term}`Moyenne de Reynolds <RANS>`, qui résout une seule équation de transport pour une viscosité cinématique turbulente modifiée $\tilde{\nu}$, à partir de laquelle la viscosité eddy $\nu_t$ est dérivée par une fonction d'amortissement proche du mur. L'équation de transport pour $\tilde{\nu}$ comprend la convection, {term}`Diffusion`, un terme de production proportionnel au taux de déformation local, et un terme de destruction qui dépend de la distance à la paroi solide la plus proche. Par rapport au modèle $k-\epsilon$, Spalart-Allmaras est plus léger (une équation au lieu de deux), mais le terme de destruction basé sur la distance de mur rend la résolution adéquate du maillage proche du mur important. Le modèle a été développé à l'origine pour les débits aérodynamiques à haute-{term}`Nombre de Reynolds <Reynolds number>` (aéroespace) avec des gradients de pression défavorables légers, et est adapté en TELEMAC-2D comme une fermeture en moyenne de profondeur {term}`Moyenne de Reynolds <RANS>`. Les mots-clés suivants s'appliquent; notez que les mots-clés contenant `K-EPSILON` dans leur nom régissent également le solveur Spalart-Allmaras:
  * `INFORMATION ABOUT SPALART-ALLMARAS MODEL : YES` permet la sortie de console pour le solveur SA (par défaut = OUI).
  * `TURBULENCE REGIME FOR SOLID BOUNDARIES : 2` pour les murs solides bruts (utiliser `1` pour les murs lisses); le même rôle et les mêmes valeurs que pour le modèle $k-\epsilon$ (voir {ref}`tm2d-friction`).
  * `VELOCITY DIFFUSIVITY : 1.E-6` -- viscosité cinématique de l'eau (10$^{-6}$ m$^2$/s), le même rôle que dans le modèle $k-\epsilon$.
  * `ACCURACY OF SPALART-ALLMARAS : 1.E-9` -- seuil de convergence pour l'étape de diffusion et de terme source de l'équation $\tilde{\nu}$ (par défaut $10^{-9}$).
  * `SCHEME FOR ADVECTION OF K-EPSILON` contrôle l'advection de $\tilde{\nu}$; utiliser les mêmes recommandations que pour $k-\epsilon$ (p. ex., `14` avec les appartements de marée, `4` sans).
  * Le 5ème élément de `DISCRETIZATIONS IN SPACE` définit la discrétisation spatiale pour $\tilde{\nu}$ (par défaut `11`).
  * `SOLVER FOR K-EPSILON MODEL`, `MAXIMUM NUMBER OF ITERATIONS FOR K AND EPSILON`, et `PRECONDITIONING FOR K-EPSILON MODEL` tous régissent également le système de solveur SA.

```{admonition} Near-wall resolution for the Spalart-Allmaras model
:class: note

Dans TELEMAC-2D, **walls** se rapportent à des limites latérales solides, c'est-à-dire les rives, les jetées de pont, les murs d'entraînement, **et non le lit** (la rugosité du lit est traitée séparément par le modèle de rugosité du fond). Le terme de destruction Spalart-Allmaras s'échelle avec $C_{w1} f_w \left(\tilde{\nu}/l_w\right)^2$, où $l_w$ est la plus courte distance d'un noeud de maille à la limite solide la plus proche. Cette dépendance provoque $\tilde{\nu}$, et par conséquent $\nu_t$, pour se désintégrer vers zéro en s'approchant de la paroi, ce qui produit le profil de gradient de vitesse attendu dans un flux mural turbulent.

Pour que cette désintégration soit bien résolue, ** au moins 2 à 3 nœuds de mailles doivent se trouver à l'intérieur de la couche de cisaillement près de la paroi** le long des limites latérales solides. Si le nœud le plus proche est situé trop loin du mur, $l_w$ est surestimé, le terme de destruction est trop faible, et la viscosité de eddy près de la frontière sera artificiellement élevée. Dans la pratique, cela signifie qu'il est important d'appliquer le raffinement des mailles locales le long des frontières solides : une cible utile est la longueur des bords des éléments d'environ. 1/10$^{th}$ de la largeur prévue de la couche latérale de cisaillement, qui dans l'hydraulique fluviale varie généralement de quelques décimètres près des structures hydrauliques à quelques mètres le long des berges ouvertes de la plaine inondable.

Notez que cette exigence est plus stricte que pour le modèle $k-\epsilon$. Avec `TURBULENCE REGIME FOR SOLID BOUNDARIES : 2`, le modèle $k-\epsilon$ applique le modèle de rugosité du bas directement aux nœuds limites et ne compte pas sur la résolution de la désintégration turbulente de la viscosité à travers le maillage.
```

Ce tutoriel utilise le modèle $k-\epsilon$ (`3`) en raison de sa popularité et de sa grande applicabilité (pour ne pas confondre avec la justesse).

```
DIFFUSION OF VELOCITY : YES / enabled by default
TURBULENCE MODEL : 3
```


(tm2d-run)=
## Exécuter Telemac2d

Avec le fichier de direction (`*.cas`), le dernier ingrédient nécessaire pour effectuer une simulation hydrodynamique 2d avec Telemac2d est disponible. Assurez-vous de mettre tous les fichiers requis dans un dossier de simulation (par exemple, `~HOMETEL/mysimulations/steady2d-tutorial/`). Les fichiers requis peuvent également être téléchargés à partir du dépôt de tutoriels eBook [steady2d](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial/) et inclure:

* [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/qgismesh.slf)
* [boundaires.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli)]
* [steady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)

Avec ces fichiers préparés, chargez l'environnement TELEMAC, et lancez Telemac2d en suivant les explications dans les sections suivantes.

### Charger l'environnement et les fichiers

Allez dans le dossier de configuration de l'installation Telemac (par exemple, `HOMETEL/configs/` où `HOMETEL` pourrait être quelque chose comme `/home/telemac/v9.0.0/`) et chargez l'environnement (par exemple, `pysource.gfortranHPC.sh` - utilisez la même chose que pour {ref}`compiling Telemac <tm-compile>`).

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
```

````{admonition} If you are using the Hydro-Informatics (Hyfo) Mint VM
:class: note, dropdown

Si vous travaillez avec le {ref}`Mint Hyfo VM <hyfo-vm>`, chargez l'environnement TELEMAC comme suit :

```
cd ~/telemac/v8p2/configs
source pysource.hyfo-dyn.sh
```
````

### Démarrer une simulation Telemac2d

Pour commencer une simulation, changez le répertoire (`cd`) où les fichiers de simulation vivent et lancez le fichier de direction (`.cas`) avec le script **telemac2d.py** :

```
cd ~/telemac/v9.0.0/mysimulations/steady2d-tutorial/
telemac2d.py steady2d.cas -s
```

Le drapeau `-s` n'est pas strictement nécessaire mais utile pour réviser les caractéristiques de simulation, comme les flux à travers les limites du liquide ou le temps total de simulation. Il écrira un fichier nommé `steady2d.cas.[...].sortie` et pourra être utilisé pour l'analyse de la convergence décrite dans le chapitre des projecteurs sur {ref}`quantitative convergence <tm-convergence>`.

Par conséquent, un calcul réussi devrait se terminer par les lignes (ou similaires) suivantes dans *Terminal* :

```fortran
[...]
                     *************************************
                     *    END OF MEMORY ORGANIZATION:    *
                     *************************************

 CORRECT END OF RUN

 ELAPSE TIME :
                             03  MINUTES
                             44  SECONDS
... merging separated result files

... handling result files
        moving: r2dsteady.slf
... deleting working dir

My work is done
```

Ainsi, Telemac2d a produit le fichier *r2dsteady.slf* qui peut maintenant être analysé dans le {ref}`post-processing with QGIS <tm-steady2d-postpro>` ou ParaView.


(tm-steady2d-postpro)=
# Traitement après

Le post-traitement du scénario stable 2d utilise le QGIS et le {ref}`PostTelemac plugin <tm-qgis-plugins>`. Les résultats de Telemac peuvent également être visualisés avec [ParaView](https://www.paraview.org) ou BlueKenue.

(tm-use-q4ts)=
## Charger les résultats et le plugin Q4TS

Lancez QGIS, {ref}`create a new QGIS project <qgis-project>`, définissez le projet {term}`Système de coordonnées <CRS>` à `UTM zone 33N`, ajoutez une imagerie satellite {ref}`basemap <basemap>`, et enregistrez le projet (par exemple, `tm2d-postpro.qgis`) dans le même dossier où se trouve le fichier de résultats de simulation de Telemac2d (*r2dsteady.slf*), semblable aux descriptions de {ref}`pre-processing tutorial <tm-qgis-prepro>`.

Chargez le fichier de géométrie `r2dsteady.slf` en maillage avec glisser-déposer du panneau du navigateur vers le panneau des calques. Assurez-vous de l'importer avec sa géoréférence correcte: **EPSG:32633** (ETRS 89 / zone UTM 33N).

Pour continuer avec cette section, assurez-vous que le plugin Q4TS est installé (voir instructions dans le {ref}`Software Requirements section <qgis-telemac>`). Pour explorer les résultats sans le plugin Q4TS, directement {ref}`jump to the next section <tm2d-post-export>`. Q4TS est utile pour effectuer l'analyse SALOME/ParaVis-like (p. ex., sonde avancée, pipelines de post-traitement, workflows centrés sur MED) par le traitement de conversion:

* Dans **Processing > Toolbox**, lancez **slf2med** (fournisseur Q4TS):
  * **Input .slf**: `r2dsteady.slf`
  * **Input .cli** (facultatif): votre fichier limite si vous le souhaitez
  * ** Sortie .med**: enregistrer `r2dsteady.med`

Ouvrez ensuite le fichier `*.med` dans votre workflow post-traitement MED (ParaVis/SALOME). Il s'agit de la seule fonctionnalité Q4TS qui relie significativement en « post-traitement réel » à l'extérieur de QGIS.

## Analyse transversale (valeurs extraites selon les lignes de section)

Ceci remplace l'ancienne routine "draw a line and inspect/export" de PostTelemac, mais il est plus propre car il produit un CSV reproductible à partir d'une couche de ligne.

1. Créer une ligne de coupe transversale :
  * Créer une nouvelle couche de ligne (GeoPackage recommandé) appelée, par exemple, `control_sections`.
  * numériser une ou plusieurs lignes transversales à travers le chenal (en amont, en aval, sections de contrôle, etc.).

2. Exporter des valeurs transversales du maillage vers le CSV
  * Ouvrir **Processing > Toolbox** et exécuter **Exporter les valeurs de l'ensemble de données de section transversale sur les lignes du maillage**
  * Configuration & #160;:
    * **Couche de maille d'entrée**: `r2dsteady`
    * **Groupes de données** : choisissez ce que vous voulez analyser (exemples)
      * `WATER DEPTH` (stabilité / comportement de séchage humide)
      * composants de vitesse ou magnitude (hydraulique + points chauds de stabilité)
      * toute variable diagnostique que vous avez écrite aux résultats (si disponible)
    * **Heure des données**:
      * utiliser **Temps de toile actuel** pour les vérifications « snapshot », ou
      * exécutez plusieurs fois des horodatages spécifiques.
    * **Lines for data export**: `control_sections`
    * **Résolution de segmentation de ligne**: définissez ceci à quelque chose qui a du sens pour votre résolution de maillage (don=t suréchantillon).
    * **Output**: enregistrer comme `*.csv`

Ouvrir le CSV exporté dans {ref}`Libre Office <lo>` et tracer les profils de section (p. ex., profondeur vs chaîne, vitesse vs chaîne). Répéter pour les sections amont/aval et comparer.

**Ce que cela vous dit (angle de performance du modèle):**
* les vérifications de la santé section par section (p. ex., les modèles de profondeur/vitesse où vous les attendez);
* détection des points chauds (épis non physiques près des limites, autour de gradients bathymétriques abrupts, etc.),
* « est-il stable encore? » vérifie en comparant la même section à plusieurs étapes.

## Analyse des nœuds (séries chronologiques aux points de contrôle)

Pour les contrôles de convergence / stabilité, les séries chronologiques ponctuelles sont généralement le signal le plus rapide.

1. Créer un calque de contrôle :
  * Créez un calque point appelé `control_points`.
  * Ajoutez des points aux endroits qui vous intéressent :
    * près des limites d'entrée/sortie,
    * à proximité des commandes hydrauliques,
    * dans les zones où l'instabilité est probable (zones de chasse, fortes pentes, front mouillant/séchant).
2. Exporter des séries chronologiques du maillage vers le CSV:
  * Ouvrir **Processus > Boîte à outils** et exécuter **Exporter des valeurs de séries chronologiques à partir de points d'un ensemble de données de maillage**
  * Configuration & #160;:
    * **Couche de maille d'entrée**: `r2dsteady`
    * **Groupes de données**: choisissez les variables clés que vous souhaitez surveiller (profondeur, vitesse et tous les champs de diagnostic que vous produisez)
    * **Points for data export**: `control_points`
    * **Output**: enregistrer comme `*.csv`

Placez la série chronologique à {ref}`Libre Office <lo>` et utilisez-la comme un tableau de bord de performance rapide:

* La profondeur/vitesse est-elle stable (état stable)?
* Voyez-vous des oscillations ou des pics (problèmes numériques, problèmes de conditions limites)?
* Est-ce que les noeuds peu profonds se retournent mouillés/séchés de façon irréaliste (question d'accord mouillant/séchant)?

Ces séries extraites sont directement utilisables dans le {ref}`wet initialization exercise below <tm2d-init-wet>`.

(tm2d-post-export)=
## Exportation vers GeoTIFF

Pour exporter les résultats du modèle vers un raster {term}`GeoTIFF`, allez dans la **Processing Toolbox** (en QGIS), élargissez l'entrée **Mesh** et ouvrez l'outil **Rasterize mesh. Dans la fenêtre contextuelle **Rasterize Mesh Dataset** ({numref}`Figure %s <rasterize-v-mesh>`) effectuez les réglages suivants :

* **Couche de maille d'entrée** : sélectionnez la couche de maille de résultats de Telemac (`r2dsteady`)
* **Groupes de données** : cliquez sur le bouton **...** > **Choisissez Groupes de données disponibles** et sélectionnez une quantité d'intérêt. Ce tutoriel présente l'exportation d'une vitesse d'écoulement. Cliquez sur **OK** pour revenir à l'outil Rasterize Mesh Dataset.
* **Heure des données**: cliquez sur le symbole de la flèche vers le haut/vers le bas pour défiler vers le bas et sélectionnez la dernière étape. Dans une simulation instable (c.-à-d. quasi stable), d'autres étapes de temps pourraient également être intéressantes.
* **Extent** : cliquez sur la flèche déroulante > **Calculer à partir du calque** > sélectionner **r2dsteady**
* ** Taille du pixel**: `1.0` (par défaut). Avec des mailles plus grossières ou plus fines, la taille du pixel doit être variée.
* **Système de coordonnées de sortie** : sélectionnez `EPSG:32633` (c'est-à-dire le système de référence de coordonnées du maillage)
* **Output raster layer** : cliquez sur **...** pour naviguer dans un dossier cible et entrer un nom pour le raster. Ici : `velocity-tmax.tif`.
* **Run** la rastérisation.


```{figure} ../../img/telemac/rasterize-mesh.png
:alt: telemac qgis export velocity geotiff raster
:name: rasterize-v-mesh

L'outil Rasterize Mesh Dataset dans QGIS.
```

Le résultat **vitalité-tmax** raster sera ajouté au panneau Calques. Pour une meilleure visualisation, une certaine couleur est utile. Par conséquent, double-cliquez sur le nouveau **vitesse-tmax** pour ouvrir ses propriétés. Allez à la **Symbologie**, changez le type **Rendre** à `Singleband pseudocolor`, et utilisez votre rampe de couleur préférée et le nombre de classes pour visualiser la vitesse. Pour rendre `0`-entries invisibles, cliquez sur le symbole **Color** et fixez l'opacité ** à 0%, ou fixez le **Min** à `0.0001`.


```{figure} ../../img/telemac/qgis-exported-v.png
:alt: qgis telemac flow velocity vitesse results slf raster geotiff tif
:name: qgis-exported-v

La vitesse d'écoulement exportée (VITESSE) GeoTIFF raster dans QGIS (carte de fond: {cite:t}`googlesat` imagerie satellite). L'emplacement de l'outil Raster mesh dans la boîte à outils de traitement est mis en évidence à droite.
```


## Analyser les résultats

La première analyse des résultats devrait porter sur l'exactitude fondamentale du modèle, par exemple en ce qui concerne le bilan massique et son évolution dans le temps. Pour ce faire, ouvrez le menu supérieur **Time Controller** <img src="../../img/qgis/time-controller.png" width="15" height="15"> dans QGIS.


(verify-steady-tm2d)=
### Convergence des rejets quantitatifs

Pendant la simulation, les mots-clés `MASS-BALANCE : YES` et/ou `PRINTING CUMULATED FLOWRATES : YES` impriment des flux de masse au-delà des limites des liquides dans le terminal. Pour revoir rétrospectivement les taux de flux et l'équilibre du volume, la simulation doit avoir exécuté avec le drapeau `-s`, qui enregistre l'état de simulation dans un fichier appelé similaire à `steady2d.cas_YEAR-MM-DD-HHhMMminSSs.sortie`. Sur la base du fichier `.sortie`, les montants des flux, le volume total et l'erreur de volume peuvent être extraits et analysés avec les scripts Python fournis avec l'installation Telemac (*HOMETEL/scripts/python3/*). Les carnets Telemac Jupyter (*HOMETEL/notebooks/* > *data manip/extraction/*.ipynb* ou *workshops/exo fluxes.ipynb*) illustrent l'utilisation des scripts Python. Une discussion détaillée sur la convergence et les scripts Python ([pythomac](https://pythomac.readthedocs.io)) peut être trouvée dans ce livre électronique, dans le chapitre sur {ref}`quantitative Telemac convergence analysis <tm-convergence>`. Avec ces scripts, {numref}`Fig. %s <steady-flux-convergence-standalone>` a été généré montrant les flux à travers les deux limites de l'étude stable-2d, indiquant la convergence après environ 7000 pas de temps.

```{figure} ../../img/telemac/steady-flux-convergence.png
:alt: python telemac flux discharge convergence pythomac
:name: steady-flux-convergence-standalone

Graphique de convergence du flux sur les deux limites de la simulation stable à sec Telemac2d (créée avec pythomac).
```

(qualitative-postel)=
### Velocité qualitative, profondeur et évolution de décharge

La convergence de la profondeur d'eau et de la vitesse d'écoulement, et donc du débit, peut être observée qualitativement dans le QGIS par l'intermédiaire du **Time Controller** (voir activation à {numref}`Fig. %s <qgis-time-controller-tm>`). La fréquence des images peut être réglée en cliquant sur la roue du régulateur de temps, et les séquences d'images jouées en cliquant sur le bouton *Play*. De plus, {numref}`Fig. %s <qgis-time-controller-tm>` utilise une superposition de couleurs de pixel de profondeur d'eau (point de conversion) et de vecteurs de vitesse d'écoulement, définis dans le panneau *Layer Styling*. Le Nord et les flèches de décharge, et le titre sont *Décorateurs*, qui se trouvent dans **View** > **Décorateurs**.

```{figure} ../../img/telemac/qgis-time-controller.jpg
:alt: time controller qgis telemac
:name: qgis-time-controller-tm

Le contrôleur de temps activé dans QGIS permet de se déplacer le long de l'axe temporel des quantités modélisées (carte de fond : {cite:t}`googlesat` imagerie satellite). Les boutons rouge surlignés activent le régulateur de temps, jouent la séquence d'images de quantités sélectionnées, fournissent un réglage pour jouer une fréquence d'images par seconde et permettent d'enregistrer des images de tous les temps (voir les instructions ci-dessous).
```

Pour **exporter une série d'images pour les transformer en GIF** comme un film, utilisez le bouton **Save** du régulateur de temps. Configurez la résolution souhaitée et définissez un dossier de sortie. La série d'images PNG peut ensuite être convertie, par exemple, avec [GIMP](https://www.gimp.org/), en un GIF. À cette fin, téléchargez et ouvrez GIMP, puis:

* Ouvrez la première image de la série exportée.
* Tirez toutes les autres images exportées dans le panneau *Layers* de GIMP.
* Inverser l'ordre des calques dans GIMP : **Layer** > **Stack** > **Reverser l'ordre des calques**.
* Enregistrer l'image comme GIF: **Fichier** > **Exporter sous...**.
* Sélectionnez un dossier pour enregistrer le fichier, dans le champ **Nom** entrer `[any-name].GIF`, et cliquez sur **Export**.
* Dans la fenêtre popup activer **En animation** et **Loop forever** avec un délai recommandé entre les cadres de **100 millisecondes**. Gardez toutes les autres valeurs par défaut et cliquez sur **Export**.

La figure animée ci-dessous présente un GIF exporté avec une profondeur d'eau en arrière-plan et une vitesse d'écoulement en tant que vecteur de rationalisation allant de 0 à 2,0 m/s. L'animation montre comment le modèle est rempli à partir de ses limites amont (gauche) et aval (droite) au début de la simulation. Alors que le rejet en amont a été imposé avec une profondeur d'eau à travers une limite `5 5 5`, la limite en aval avait seulement une profondeur d'eau prescrite `5 4 4` limite. La prescription d'une profondeur d'eau suffisante était nécessaire pour éviter les débits supercritiques aux limites, ce qui rendrait le modèle numérique en panne immédiatement. Comme le flux provenant de la limite en aval doit se déplacer vers le haut, il ne peut pas aller très vite et est renversé par une vague d'eau provenant de la limite en amont. Si un flux en aval était prescrit, le modèle aurait été plus instable et surdéterminé.

````{div}
:class: full-width
```{admonition} GIF sequence of a dry-initialized Telemac2d model (large file size!)
:class: tip, dropdown
:name: telemac-flow-convergence-gif

<img src="../../img/telemac/inn-dry-init.gif" alt="Telemac dry-init GIF" />

```
````

```{admonition} Recall: boundary conditions and mass balance
:class: important

L'équilibre de masse est un critère crucial pour un modèle numérique sonore. En savoir plus dans le chapitre sur la mise en place {ref}`boundary conditions for mass balance <foc-mass-bc>`.
```

(vtk2slf)=
### Convertir en VTK (ParaView)

ParaView est idéal pour l'analyse 3D. Une façon simple de charger les fichiers de résultats TELEMAC `.slf` est de les convertir au format `.vtk`. Un moyen rapide de faire cette conversion est d'utiliser [pputils](https://codeberg.org/pprodano/pputils). À cette fin, d'abord clone pputils, puis assurez-vous que la dépendance `numpy` est installée dans le même environnement Python que vous utiliserez pour la conversion. Rappelez-vous où vous avez téléchargé des pputils :

```bash
git clone https://codeberg.org/pprodano/pputils.git
python -m pip install numpy
```

Après cela, `cd` dans votre répertoire modèle TELEMAC (où vit le fichier `.slf`) et créer un nouveau script Python nommé `slf2vtk.py` avec le contenu suivant. Assurez-vous de définir `PPUTILS_DIR` dans le répertoire des pputils clonés et de modifier `input_slf="results.slf"` et `output_template="vtk/results.vtk"` selon vos besoins :

````{admonition} Click to unroll Python code
:class: note, dropdown

```python
"""slf2vtk.py"""
from pathlib import Path
import subprocess
import sys
from typing import List, Optional, Union


PPUTILS_DIR = Path(r"/path/to/pputils").expanduser().resolve()


def slf_to_vtk(
    input_slf: Union[str, Path],
    output_template: Union[str, Path],
    *,
    binary: bool = True,
    start: Optional[int] = None,
    end: Optional[int] = None,
) -> List[Path]:
    """Convert a SELAFIN file to one VTK file per time step."""

    input_slf = Path(input_slf).expanduser().resolve()
    output_template = Path(output_template).expanduser().resolve()

    if not input_slf.is_file():
        raise FileNotFoundError(input_slf)

    if output_template.suffix.lower() != ".vtk":
        raise ValueError("output_template must end in .vtk")

    if "." in output_template.stem:
        raise ValueError("Avoid additional dots in the output filename")

    if (start is None) != (end is None):
        raise ValueError("Specify both start and end, or neither")

    if start is not None and end is not None:
        if start < 0 or end < 0:
            raise ValueError("start and end must be non-negative")
        if start > end:
            raise ValueError("start must be less than or equal to end")

    converter = PPUTILS_DIR / (
        "sel2vtk_bin.py" if binary else "sel2vtk.py"
    )

    if not converter.is_file():
        raise FileNotFoundError(f"PPUTILS converter not found: {converter}")

    output_template.parent.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(converter),
        "-i",
        str(input_slf),
        "-o",
        output_template.name,
    ]

    if start is not None and end is not None:
        # start/end are zero-based time-step indices.
        command += ["-t_start", str(start), "-t_end", str(end)]

    subprocess.run(
        command,
        cwd=output_template.parent,
        check=True,
    )

    pattern = output_template.stem + "[0-9]" * 5 + ".vtk"
    generated_files = sorted(output_template.parent.glob(pattern))

    if not generated_files:
        raise RuntimeError("pputils did not produce any VTK files")

    return generated_files


if __name__ == "__main__":
    generated_files = slf_to_vtk(
        input_slf="results.slf",
        output_template="vtk/results.vtk",
        binary=True,
        # start=0,
        # end=10,
    )

    for path in generated_files:
        print(path)
```
````

Ensuite, lancez-le dans un terminal à partir de votre répertoire modèle TELEMAC:

```bash
python slf2vtk.py
```

La valeur donnée sous `output_template` est un modèle de nom de fichier plutôt que le nom d'un fichier final. Par exemple, `vtk/results.vtk` produit `vtk/results00000.vtk`, `vtk/results00001.vtk`, et ainsi de suite; un fichier pour chaque étape dans le fichier `.slf`.

Par défaut, le script utilise `sel2vtk_bin.py` pour écrire des fichiers VTK binaires. Définir `binary=False` pour écrire les fichiers ASCII VTK à la place. Pour ne convertir qu'une partie de la série de résultats, décommenter `start` et `end`; ces valeurs sont des indices temps-étape inclusifs basés sur zéro plutôt que des temps de simulation.

### Charger les vitesses TELEMAC-3D dans ParaView

Les fichiers VTK générés dans le workflow précédent contiennent les composants de vitesse TELEMAC-3D \(u\), \(v\) et \(w\). Ces quantités représentent les vitesses signées dans les directions \(x\)-, \(y\)- et \(z\)-, respectivement. La vitesse en trois dimensions correspondante est

$$
|\mathbf{u}| = \sqrt{u^2 + v^2 + w^2}.
$$

Sur un ordinateur Debian, installer ParaView à partir du dépôt Debian s'il n'est pas déjà disponible, puis ouvrir la série de fichiers convertis à partir du répertoire modèle:

```bash
sudo apt update
sudo apt install paraview

cd /path/to/telemac/model/vtk
paraview --data="$PWD/results..vtk"
```

Dans la commande finale, les deux périodes consécutives remplacent la partie numérotée des fichiers comme `results00000.vtk`, `results00001.vtk`, et `results00002.vtk`. ParaView reconnaît normalement ce motif de nommage comme une série de fichiers temporels. Après que le lecteur apparaît dans le **Pipeline Browser**, sélectionnez-le et cliquez sur **Appliquer**.

Lorsque `sel2vtk_bin.py` ou `sel2vtk.py` détecte les variables TELEMAC `VELOCITY U`, `VELOCITY V` et `VELOCITY W`, [pputils](https://codeberg.org/pprodano/pputils) les combine dans le vecteur de données point `Velocity`. Pour afficher directement la vitesse totale, sélectionnez **Vélocity** dans le menu **Coloring**, puis sélectionnez **Magnitude**. Les composants vectoriels **X**, **Y** et **Z** correspondent respectivement à \(u\), \(v\) et \(w\). Les tableaux scalaires originaux sont également disponibles sous la forme de `VELOCITY_U`, `VELOCITY_V` et `VELOCITY_W`.

Si l'amplitude de la vitesse est requise comme tableau séparé pour le découpage, le seuil, l'étude ou l'exportation, sélectionnez le lecteur VTK dans le **Pipeline Browser**, puis choisissez **Filters > Common > Calculatrice**. Définir **Result Array Nom** à `VELOCITY_MAGNITUDE`, confirmer que l'association de données est **Point Data**, et entrer:

```text
mag(Velocity)
```

Cliquez sur **Appliquer**, puis colorez la sortie Calculatrice par `VELOCITY_MAGNITUDE`. Pour une animation, utilisez **Rescale to Data Range over All Timesteps** de façon à ce qu'une échelle de couleur soit appliquée de façon uniforme tout au long de la simulation. Cette opération se lit à chaque étape et peut donc nécessiter un délai supplémentaire pour un grand ensemble de résultats TELEMAC-3D.

La syntaxe de la série de fichiers, la coloration vectorielle et l'expression Calculatrice suivent la documentation [ParaView data-loading](https://docs.paraview.org/en/latest/UsersGuide/dataIngestion.html), [color-mapping](https://docs.paraview.org/en/latest/ReferenceManual/colorMapping.html), et [Calculator](https://docs.paraview.org/en/latest/UsersGuide/filteringData.html#calculator). ParaView est disponible en tant que [Paquet Debian](https://packages.debian.org/stable/paraview).



(tm2d-init-wet)=
## Exercice: Conditions initiales

Le point {numref}`Fig. %s <steady-flux-convergence>` et {ref}`depth-velocity animation <telemac-flow-convergence-gif>` ci-dessus à la stabilité atteinte après environ 7000 étapes. Un modèle d'initialisation humide converge beaucoup plus vite, mais nécessite soit une première opération d'initialisation du modèle sec, soit il peut utiliser d'autres mots clés de l'état initial dans Telemac. Idéalement, le modèle d'initialisation à sec est utilisé comme condition de démarrage à chaud pour un modèle d'initialisation par voie humide, comme décrit dans le {ref}`unsteady 2d tutorial <tm2d-hotstart>`.
  
````{admonition} Challenge: initialize Telemac with an initial water depth
:class: important

Même si ce n'est pas la meilleure pratique pour modéliser une rivière, exécuter la simulation stable2d.cas avec une profondeur initiale d'eau de 1 m est un exercice intéressant pour découvrir pourquoi ce n'est pas un bon choix. Pour exécuter le modèle avec une première profondeur d'eau, nous pouvons faciliter les conditions limites en supprimant la contrainte de profondeur en amont (c.-à-d. en définissant la première entrée du mot clé `PRESCRIBED ELEVATIONS` à `0.`), et en modifiant les mots clés `INITIAL [...]` condition à `'CONSTANT DEPTH'` de `1` meter:

```fortran
/ steady2d_wet.cas
/ ... header
/ ...
PRESCRIBED FLOWRATES  : 35.;0.
PRESCRIBED ELEVATIONS : 0.;371.33
/ ...
INITIAL CONDITIONS : 'CONSTANT DEPTH'
INITIAL DEPTH : 1
/ ...
/ ... footer
```

Aussi, changez le type de limite en amont en un type moins limité `4 5 5` (Q prescrit seulement) dans le fichier {ref}`boundaries.cli <bk-liquid-bc>`. Pour cette modification, il suffit d'ouvrir les limites.cli dans n'importe quel éditeur de texte** et d'utiliser sa fonction **find-and-remplace** (par exemple, `CTRL` + `H` touches en {ref}`npp`):

* Dans le champ **Find**, tapez `5 5 5`.
* Dans le **Replacez avec** type de champ `4 5 5`.
* Cliquez sur **Replacer** jusqu'à ce que tous les types de bornes **upstream** soient modifiés.
* Enregistrer et fermer **borderies.cli**.

Enregistrer les fichiers `.cas` et `.cli` modifiés, et re-run Telemac:

```
telemac2d.py steady2d_wet.cas
```

Le diagramme en {numref}`Fig. %s <convergence-diagram-tm2d-wet>` trace les deux colonnes de flux aux limites ouvertes en amont et en aval au fil du temps pour la configuration de simulation dans ce tutoriel. Le diagramme suggère que le modèle atteint la stabilité (c'est-à-dire converge) après la 55e liste de sortie (temps de simulation $t \leq 5500$).

```{figure} ../../img/telemac/convergence-diagram-tm-pt.png
:alt: telemac2d convergence steady simulation wet initialization
:name: convergence-diagram-tm2d-wet

Convergence des entrées (en amont) et des sorties (en aval) aux limites ouvertes du modèle humide.
```

```{figure} ../../img/telemac/qgis-exported-tif.png
:alt: qgis flow velocity vitesse results slf PostTelemac raster geotiff tif
:name: exported-tif

La vitesse d'écoulement (VITESSE) GeoTIFF raster après une simulation Telemac à l'initialisation humide, montrée dans QGIS (plan d'arrière-plan : {cite:t}`googlesat` imagerie satellite).
```

```{admonition} Question: what are the pros and cons of the wet-initialized simulation with constant water depth?
:class: note, dropdown

** Positive (pro)** est que la simulation converge considérablement plus vite que dans le cas du modèle initialisé à sec.

**Les indicateurs de performance negatifs (contra)** sont des pixels de vitesse d'écoulement non nulle sur les plaines inondables (au-delà des berges) à {numref}`Fig. %s <exported-tif>`. Ces pixels apparemment mal modélisés sont un artéfact de l'utilisation de conditions initiales humides, qui mettent une couche d'eau de 1 m d'épaisseur sur tout le modèle. Plus précisément, les parcelles d'eau sont restées dans de petites dépressions locales entre les limites solides (`2 2 2`) et les digues le long des rives. Cette eau ne pouvait s'écouler et rester sur ces patchs jusqu'à la fin de la simulation. Il s'agit d'un drapeau d'exclusion physiquement déraisonnable, qui disqualifie un modèle pour toute application.
```
````

(tm2d-calibration)=
# Notes sur l'étalonnage

## Rafraîchisseur: Comment fonctionne l'étalonnage?

{ref}`Calibration <calibration>` implique l'adaptation par étapes des paramètres d'entrée du modèle pour obtenir un meilleur ajustement (statistique) des données modélisées et mesurées. Dans le processus d'étalonnage du modèle, un seul paramètre doit être modifié à la fois par des écarts de 10 à 20 % par rapport à sa valeur par défaut. Par exemple, si le début `FRICTION COEFFICIENT : 0.03`, l'étalonnage peut tester pour `FRICTION COEFFICIENT : 0.033`, puis `FRICTION COEFFICIENT : 0.036`, `FRICTION COEFFICIENT : 0.027` et ainsi de suite, finalement pour savoir quelle valeur pour **FRICTION COEFFICIENT** apporte les résultats du modèle le plus proche des observations.

De plus, une analyse de sensibilité compare les modifications progressives de plusieurs paramètres (toujours : un à la fois) et leur effet sur les résultats du modèle. Par exemple, si une variation de 10 % de **FRICTION COEFFICIENT** entraîne une variation de 5 % de la profondeur globale de l'eau alors qu'une variation de 10 % de la taille du quadrillage (longueur de la bordure) entraîne une variation de 20 % de la profondeur globale de l'eau, on peut conclure que la sensibilité du modèle est plus élevée par rapport à la taille du quadrillage. Toutefois, ces conclusions exigent des considérations minutieuses dans les modèles multiparamétriques et complexes des écosystèmes fluviaux.

## Paramètres d'étalonnage dans Telemac
Les paramètres suivants peuvent être utilisés pour l'étalonnage d'un modèle 2d aux mesures (p. ex. élévation de la surface de l'eau, profondeur de l'eau ou données de vitesse du débit):

* ** COEFFICIENT DE LA FRICTION** ({ref}`friction section <tm2d-friction>`)
* Solveurs, options de solveur, implicites et autres paramètres numériques ({ref}`numerical parameter section <tm2d-solver-pars>`)
* Type de modèle {ref}`initialization <tm2d-init-dry>`
* {ref}`Turbulence models and parameters <tm2d-turbulence>`

```{admonition} Avoid accuracy-reducing keyword settings
Les paramètres de mots clés tels que `MASS-LUMPING ... : ...` conduisent à un lissage accru (c.-à-d. une précision réduite) des résultats pour augmenter la vitesse de calcul. Cependant, dans la plupart des cas, il vaut la peine d'accepter des temps de calcul plus longs et d'obtenir une plus grande précision, ce qui réduira les efforts d'étalonnage des modèles et permettra ainsi d'économiser plus de temps.
```

# Prochaines étapes

1. Assurez-vous que la simulation est prudente selon les descriptions dans le chapitre des projecteurs sur {ref}`mass balance <foc-mass-bc>`.
1. Trouver une durée de simulation significative pour la convergence d'une simulation à sec à la suite des algorithmes fournis avec le chapitre {ref}`quantitative convergence <tm-convergence>`.
1. Utilisez le modèle initialisé à sec pour simuler au moins 2-3 rejets réguliers (avec {ref}`hotstart conditions <tm2d-hotstart>`) pour lesquels des données de mesure sont disponibles pour {ref}`calibration <calibration>` et validation.
1. Le modèle étalonné et validé peut être
  * utilisé pour les simulations {ref}`unsteady hydrodynamic <chpt-unsteady>`, et
  * servir de base pour la morphodynamique {ref}`sediment transport modeling with Gaia <tm-gaia>`.
