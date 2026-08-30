---
description: TELEMAC guide d'optimisation des modèles couvrant l'amélioration de la vitesse de calcul, l'étalonnage de la correction physique, la conservation de la masse et le raffinement des modèles assistés par machine.
---

(telemac-opti)=
# Optimisation

L'étalonnage d'un modèle numérique devrait donner un modèle fonctionnel et physiquement au moins raisonnablement précis. Le calibrage du modèle a déjà été couvert dans le tutoriel {ref}`results analysis section <tm2d-post-export>` de Telemac2d. Ce chapitre fournit d'abord plus de conseils pour augmenter la justesse physique d'un modèle, surtout en ce qui concerne la conservation de la masse, qui peut parfois être difficile à Telemac. En outre, des méthodes d'étalonnage avancées qui utilisent l'apprentissage automatique supervisé pour améliorer la précision du modèle physique sont présentées.

```{admonition} Goals and requirements
Ce tutoriel explique comment un modèle Telemac peut être affiné en améliorant sa stabilité informatique et sa justesse physique. Ainsi, il est pertinent après avoir mis en place un modèle Telemac, comme expliqué pour un cas simple dans le {ref}`steady 2d chapter <telemac2d-steady>`.

```


## Temps de calcul

Certains mots clés du fichier de direction de TELEMAC (`*.cas`) affectent la vitesse de calcul.

* Utilisez les mots-clés {ref}`ACCURACY and MAXIMUM ITERATION <tm2d-accuracy>` pour obtenir une convergence plus rapide.
* Désactiver `TIDAL FLATS`, même si désactiver {ref}`tidal flats <tm2d-tidal>` ne peut pas être recommandé pour produire des modèles physiquement significatifs et stables.
* Lorsque vous utilisez le solveur GMRES (`SOLVER : 7`), varier le {ref}`solver options <tm2d-solver-pars>` peut aider à réduire le temps total de calcul.
* Assurez-vous d'utiliser le mot-clé `MATRIX STORAGE : 3` par défaut.
* Utilisez une simulation antérieure (p. ex., avec un maillage plus grossier) pour lancer le modèle avec les mots-clés `COMPUTATION CONTINUED : YES` et `PREVIOUS COMPUTATION FILE : *.slf` (voir la section 4.1.3 du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf)).

De plus, Telemac2d permet d'arrêter une simulation (étape) lorsque les flux se stabilisent. Pour activer cette fonctionnalité, ajoutez le bloc suivant dans le fichier de direction (`*.cas`) :

```
/ steady state stop criteria in steering.cas
STOP IF A STEADY STATE IS REACHED : YES / default is NO
STOP CRITERIA : 1.E-3;1.E-3;1.E-3 / use list of three values - defaults are 1.E-4
```

Toutefois, les critères d'arrêt ne sont pas fonctionnels pour les débits non stationnaires (p. ex., rue {cite:t}`von_karman_mechanische_1930` vortex en aval des jetées de pont). En savoir plus sur les critères d'arrêt de convergence dans le [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (section 5.1).

```{admonition} More recommendations are in the user manual
:class: tip

Le [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) fournit plus de recommandations pour l'optimisation du temps, de la stabilité et du modèle, y compris le maillage, à la section 16.
```

## Stabilité et correction physique


### Précision

Lorsque les mots clés de précision sont mal définis, TELEMAC peut ne pas être en mesure de terminer la simulation. Dans ce cas, assurez-vous de commenter les mots-clés de précision et laissez TELEMAC utiliser ses valeurs par défaut:

```fortran
/ SOLVER ACCURACY : 1.E-4
/ ACCURACY FOR DIFFUSION OF TRACERS : 1.E-4
/ ACCURACY OF K : 1.E-6
/ ACCURACY OF EPSILON : 1.E-6
/ ACCURACY OF SPALART-ALLMARAS : 1.E-6
```

### Étapes de temps variables et état de la LFC

Des simulations instables peuvent se produire lorsque la condition {term}`CFL` est insuffisamment remplie. Pour s'assurer que la condition {term}`CFL` est respectée, activez le calcul à temps variable et utilisez le mot-clé **DESIRED COURANT** (valeur par défaut `1`), par exemple:

```fortran
TIME STEP : 5
VARIABLE TIME-STEP : YES
DURATION : 5000
DESIRED COURANT NUMBER : 0.9
```

Notez que le **TIME STEP** est toujours nécessaire parce que le **GRAPHIQUE PRINTOUT PERIOD** est un multiple du **TIME STEP** défini.

```{admonition} Use the DURATION keyword
Un calcul de temps variable peut s'exécuter éternellement. L'attribution du mot-clé **DURATION** évite de telles courses éternelles.
```

### Implicitation
Pour augmenter la stabilité du modèle, modifiez les variables suivantes ou assurez-vous que les variables se trouvent dans des intervalles raisonnables dans le fichier *CAS* :

* `IMPLICITATION FOR DEPTH` doit être entre `0.5` et `0.6`.
* `IMPLICITATION FOR VELOCITIES` doit être entre `0.5` et `0.6`.
* `IMPLICITATION FOR DIFFUSION` doit être `1.` ou plus petit.

### Oscillations de surface
Lorsque des gradients ou oscillations physiques non significatifs se produisent à la surface de l'eau ou que la bathymétrie a des pentes raides, les paramètres de mots clés suivants peuvent aider:

* `FREE SURFACE GRADIENT` - par défaut est `1.0`, mais il peut être réduit à `0.1` pour atteindre la stabilité (jamais, commencer par descendre progressivement, comme une valeur de `0.9`).
* `DISCRETIZATIONS IN SPACE : 12;11` - utilise la discrétisation spatiale quasi-bulle avec des triangles 4 nœuds pour la vitesse.

### Erreurs de masse résiduelles
Pour réduire les erreurs de masse résiduelles utilisées dans le fichier de direction:

```fortran
CONTINUITY CORRECTION : YES
```

### Divergence

Pour limiter les divergences, utilisez les mots-clés `CONTROL OF LIMITS` et `LIMIT VALUES`. Le mot-clé `LIMIT VALUES` est une liste de 8 entiers pour des valeurs minimales et maximales pour H, U, V et T (tracers). La mise en œuvre dans le dossier de pilotage ressemble à ceci:

```fortran
CONTROL OF LIMITS : YES / default is NO
LIMIT VALUES : -1000;9000;-1000;1000;-1000;1000;-1000;1000 / default mins and max for H, U, V, tracer
```

### Plats à marée

L'humidification et le séchage des cellules de la grille, par exemple, lors d'une simulation de ruptures de barrages ou d'hydrographies d'inondation, peuvent entraîner une instabilité du modèle. Alors que la section {ref}`tm2d-tidal` dans le tutoriel de modélisation stable de Telemac2d suggère des combinaisons d'options de mots clés significatives sur le plan physique et informatique, la section 16.5 du [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) recommande d'utiliser les paramètres suivants dans le fichier de pilotage comme choix prudent à partir de l'exemple Wesel de BAW.

```fortran
VELOCITY PROFILES : 4;0
TURBULENCE MODEL : 1
VELOCITY DIFFUSIVITY : 2.
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2
FREE SURFACE GRADIENT COMPATIBILITY : 0.9
H CLIPPING : NO
TYPE OF ADVECTION : 1;5
SUPG OPTION : 0;0
TREATMENT OF THE LINEAR SYSTEM : 2
SOLVER : 2
PRECONDITIONING : 2
SOLVER ACCURACY : 1.E-5
CONTINUITY CORRECTION : YES
```

````{admonition} How to find the Wesel example
:class: tip

Cet exemple est généralement installé dans le répertoire suivant :

```
/telemac/v9.0.0/examples/telemac2d/wesel/
```
````


### Système de discrétion

Le réglage par défaut de `DISCRETIZATIONS IN SPACE : 11;11` assigne une discrétisation linéaire pour la vitesse et la profondeur de l'eau, qui est calculablement rapide mais potentiellement instable (lire plus dans la section sur {ref}`general Telemac2d parameters <tm2d-numerical>`). Pour surmonter les problèmes de stabilité liés au schéma de discrétisation, envisagez d'utiliser `DISCRETIZATIONS IN SPACE : 12;11`. En outre, le réglage `FREE SURFACE GRADIENT COMPATIBILITY : 0.01` (i.e., près de zéro) peut aider à résoudre les problèmes de stabilité liés à la discrétisation de la vitesse et de la profondeur.


### Dépassement des valeurs maximales
*Cette section est co-écrite par [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*.

Une simulation peut imprimer `EXCEEDING MAXIMUM ITERATIONS` dans le *Terminal* :

```fortran
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  0.7234532E-01
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
```

`EXCEEDING MAXIMUM ITERATIONS` les avertissements peuvent se produire lors de l'utilisation de **CHEME POUR L'ADOPTION de [...]** mots clés avec les valeurs `3`, `4`, `5`, `13`, ou `14`. La raison en est que ces schémas donnent {term}`CFL` conditions de moins d'un en déclenchant itérative, adaptative timesteping. Pour dépanner les avertissements `EXCEEDING MAXIMUM ITERATIONS`, essayez les options suivantes :

*	Diminuer progressivement le temps.
*	Diminuer la précision du résolveur (par exemple de `1.E-8` à `1.E-6`).
* Utilisez d'autres valeurs pour `SCHEME FOR ADVECTION OF [...]`.
*	Augmenter la valeur `MAXIMUM NUMBER OF ITERATIONS FOR SOLVER`, mais ne pas dépasser `200`.
*	Modifier le type `VELOCITY PROFILE` (lire les instructions de ce livre électronique pour {ref}`2d <tm2d-bounds>` ou {ref}`3d  <tm3d-slf-boundaries>`).
*	Les démarrages à froid (c.-à-d. {ref}`defining initial conditions with the INITIAL CONDITIONS keyword in the steering file <tm2d-init-dry>`) peuvent ne pas converger. Par conséquent,
    -	augmenter progressivement le `PRESCRIBED FLOWRATES` (ou dans un {ref}`liquid boundary file <tm2d-liq-file>`), ou
    -	{ref}`create an initial conditions Selafin file <bk-create-slf>`, en attribuant une profondeur d'eau aux nœuds d'entrée.


## Étalonnage bayésien

```{admonition} Requirements
Soyez à l'aise avec {ref}`supervised learning concepts (read on hydro-informatics.com) <supervisedlearning>`, et familiarisez-vous avec le vocabulaire requis.

```


```{admonition} This section is under construction

Jusqu'à ce que nous ayons trouvé le temps de décrire l'étalonnage bayésien avec la qualité habituelle d'hydro-informatique.com, nous vous invitons à jeter un coup d'oeil à notre publication en libre accès sur le couplage Telemac avec des modèles de substitution pour les optimisations bayésiennes : {cite:t}`mouris_stability_2023`. De plus amples renseignements sont également disponibles à {cite:t}`schwindt_bayesian_2023`, {cite:t}`mohammadi_bayesian_2018` et {cite:t}`oladyshkin_bayesian3_2020`.

```

