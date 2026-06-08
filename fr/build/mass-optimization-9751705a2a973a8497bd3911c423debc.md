---
description: Flux de travail et meilleures pratiques pour la conservation de la masse dans les modèles de rivière TELEMAC, couvrant la configuration de l'état des limites, l'initialisation à sec et l'étalonnage de la relation étape-décharge.
---

(tm-foc-mass)=
# Conservation de masse

```{admonition} Tips for modeling rivers
:class: important

Les flux de travail et les conseils présentés dans ce chapitre se rapportent principalement à la modélisation numérique des rivières avec Telemac. Des conditions similaires peuvent s'appliquer aux estuaires du lac, mais d'autres environnements, comme les régions côtières, nécessiteront des considérations différentes pour la conservation de masse.
```

Ce tutoriel ne nécessite pas de code d'exécution, mais nous recommandons au moins de mettre en place un modèle Telemac, tel que décrit dans le {ref}`steady 2d tutorial <telemac2d-steady>`, ce qui facilite la compréhension des concepts et des termes.

(tm-foc-mass-workflow)=
## Flux de travail pour la conservation de masse

Avec la compréhension des conditions limites, un modèle Telemac peut être solidement construit selon le flux de travail suivant:

1. Assurez-vous à {ref}`draw liquid boundaries according to the recommendations in the section on boundaries <tm-foc-draw-bc>`.
1. Pour un modèle **dry-initialisé** (par exemple, dans le fichier {ref}`steady 2d tutorial <telemac2d-steady>`), utiliser `5 5 5` en amont (préciser Q et H) et une limite `5 4 4` en aval (préciser H) dans le fichier `.cli` pour prescrire **décharges par les mots-clés `PRESCRIBED FLOWRATES` et `PRESCRIBED ELEVATIONS`, respectivement dans le fichier de direction (`.cas`).
* A `4 5 5` en amont (préciser Q) limite peut provoquer des accidents de simulation en raison des conditions de débit supercritiques résultant de la profondeur zéro de l'eau et de la vitesse de débit non nulle (rappeler le {term}`definition of the Froude number <Froude number>`) à la limite concernée.
* La limite `5 5 5` du modèle initialisé à sec nécessite un {term}`stage-discharge relation <Stage-discharge relation>` bien défini qui peut être établi en fonction du {ref}`1d hydraulics Python exercise <ex-1d-hydraulics>` et de la valeur optimale qui en résulte pour le mot-clé ** COEFFICIENT DES MOINS** dans le fichier de direction (voir ci-dessous).
* Pour un modèle **initialisé** (c.-à-d. {ref}`hotstarted <tm2d-hotstart>`) tel que décrit dans la limite {ref}`unsteady 2d simulation tutorial <tm2d-hotstart>`, **utiliser un `4 5 5` en amont (préciser Q)** ainsi qu'une limite `5 4 4` en aval (préciser H) pour éviter des conditions surdéterminées. Cependant, une fois fermement déterminé, ne modifiez jamais le mot-clé **ROUGHNESS COEFFICIENT OF BOUNDARIES** dans le fichier de direction (voir ci-dessous).
* Si nécessaire, modifier les limites dans le fichier `.cli` avec les mots-clés corrects dans le fichier de direction (`.cas`). Pour plus de détails, voir {ref}`our tutorial on editing boundaries <tm-edit-bc>`.
1. Utilisez les mots-clés suivants pour prescrire des coefficients de rugosité aux limites qui correspondent à **mesurés {term}`stage-discharge relation <Stage-discharge relation>`** et à l'hydraulique moyenne de section rétrocalculée:
* ** PERSONNEL DE FRICTION SUR LES TERRES LATÉRALES (en entier)**
* ** COEFFICIENT DE LA ROUTE DES BOUNDARIES (float)**
* Pour recalculer un coefficient de rugosité (friction) correspondant à une paire mesurée de profondeur d'eau et de décharge, regardez la formule {ref}`Python exercise on 1-d hydraulics for solving the Manning-Strickler <ex-1d-hydraulics>`.
* *<span style="color: #41C639 "> Notez que **ne pas utiliser ces mots-clés** fera que tout calibrage de rugosité ** affecte le bilan massique**.</span>*
1. Effectuer des simulations constantes avec **PRESCRIBED FLOWRATES** correspondant à des décharges pour lesquelles on dispose de ** mesures** hydrauliques (p. ex. profondeur d'eau et vitesse d'écoulement) pour ** étalonner la rugosité** (c.-à-d. **FRICTION**).
* Toute simulation initiale en état d'équilibre doit être suffisamment longue ($\geq$ 10$^4$ timesteps) pour atteindre {ref}`mass convergence <tm-convergence>`, c'est-à-dire proche de l'égalité des entrées et sorties écrites par le mot clé **MASS-BALANCE : OUI**.
* La rugosité devrait de préférence être définie spécifiquement pour les zones avec des attributs de terrain égaux (p. ex., *cobble*, *sand bar* ou *vegetation*), comme décrit dans le point focal sur {ref}`defining roughness zones <tm-friction-zones>`. Par conséquent, les profondeurs d'eau simulées et mesurées (ou les élévations de surface de l'eau) et les vitesses d'écoulement devraient être dans des fourchettes semblables (pas plus de $\pm$0,10 m de différence).
1. Utilisez le modèle étalonné pour vos besoins dans des conditions de démarrage à chaud :
* Le mot-clé **PRESCRIBED FLOWRATES** dans le fichier `.cas` est suffisant pour calculer les sorties physiques {ref}`habitat suitability indices <hsi-def-ex>`.
* Définissez les entrées instables à partir d'un fichier d'hydrographe, comme `inflows.liq` utilisé dans le tutoriel {ref}`unsteady 2d <tm2d-liq-file>`.


````{admonition} Finite volume solver
:class: tip
:name: fv-tip

Jetez un coup d'œil au plan de volume fini de Telemac, qui est mieux dans la préservation du bilan massique, et ne nécessite pas de traiter avec **TIDAL FLATS**. Il peut être activé en définissant les mots clés suivants:

```fortran
/ steering .cas file
EQUATIONS : 'SAINT-VENANT FV' / the apostrophes are strictly needed here
VARIABLE TIME-STEP : TRUE / use instead of the TIME STEP keyword
DURATION: 1000 / example value
DESIRED COURANT NUMBER : 0.6
/
/ additional FV recommendations
OPTION FOR THE DIFFUSION OF VELOCITIES : 2 / only option to get mass conservation but can cause problems with tidal flats
SCHEME FOR ADVECTION OF VELOCITIES : 3 / use 3, also for FV - MATRIX STORAGE must be 3
SCHEME OPTION FOR ADVECTION OF VELOCITIES : 4 / overrides SUPG OPTION and OPTION FOR CHARACTERISTICS
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2 / increase for higher accuracy and longer computing time, requires SCHEME OF ADVECTION 3,4,5, or 15 and OPTION 2,3,4
TYPE OF SOURCES : 2 / 2=Dirac is the only possibility for mass conservation, the default=1 means linear function and is not mass conservative
CONTINUITY CORRECTION : YES / particularly important when not only discharge but also depth is imposed at boundaries
```

Pour en savoir plus sur le plan du volume fini, voir la section 7.2.2 du [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf), et l'exemple de malpasset (`telemac/v9.0.0/examples/malpasset/`).

````

(tm-foc-mass-keywords)=
## Mots clés supplémentaires du fichier de direction

Lors d'une simulation, on peut observer le bilan massique en activant le mot-clé **MASS BALANCE** dans le fichier de direction, qui, cependant, ** n'impose pas le bilan massique**:

```fortran
/ steering .cas file
MASS-BALANCE : YES
```

Après la simulation, la conservation de la masse peut être vérifiée comme discuté dans l'analyse du {ref}`results in the steady 2d tutorial <verify-steady-tm2d>`.

La priorité utilisée par Télémac pour produire le bilan massique peut être définie par:

```fortran
/ steering .cas file
TREATMENT OF FLUXES AT THE BOUNDARIES : 1 / 1-priority of prescribed values, 2-priority of correct fluxes
```

D'autres mots clés peuvent être définis pour non seulement observer mais aussi améliorer le bilan massique. Par exemple, le nombre par défaut de nœuds limites dans un fichier de direction est de 30, ce qui est rapidement dépassé dans un grand modèle. Ainsi, s'il y a plus de 30 nœuds limites, augmenter le nombre maximum de nœuds limites dans le fichier de direction (`.cas`), par exemple à `50`:

```fortran
/ steering .cas file
MAXIMUM NUMBER OF BOUNDARIES : 50
```

De plus, une trop petite profondeur d'eau peut causer des débits supercritiques aux limites du liquide, qui doivent être évités, soit en définissant correctement les nœuds de limite au fond du lit de rivière seulement (appelez le {ref}`recommendations to draw liquid boundaries <tm-foc-draw-bc>`) ou en augmentant la profondeur minimale d'eau de sa valeur par défaut de 0,1 m à une valeur plus élevée dans le fichier de direction, par exemple à 0,2 m:

```fortran
/ steering .cas file
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES BOUNDARY CONDITIONS : 0.2
MINIMUM DEPTH TO COMPUTE TIDAL VELOCITIES INITIAL CONDITIONS : 0.2
```

De plus, le mot-clé `MINIMUM VALUE OF DEPTH` peut être augmenté à partir de sa valeur par défaut de `0.0`, mais de telles augmentations pourraient avoir un effet négatif sur le bilan de masse.

Pour augmenter la vitesse de calcul, certains didacticiels recommandent d'utiliser le montage de masse, qui, cependant, affecte négativement la conservation de masse:

* Éviter **MASSING LAMPING ...** mots clés: ils introduisent un lissage incorrect.
* Gardez la valeur par défaut pour **H CLIPPING** car les modifications nuisent à la conservation de la masse.
