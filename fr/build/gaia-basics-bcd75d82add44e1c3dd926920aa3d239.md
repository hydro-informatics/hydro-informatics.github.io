---
description: Configuration de base du fichier de direction TELEMAC-GAIA pour les simulations morphodynamiques, couvrant les paramètres obligatoires, les conditions limites, les propriétés sédimentaires et les caractéristiques du lit de rivière.
---

(gaia-basics)=
# Configuration de base de Gaia

Les instructions suivantes se rapportent à la configuration du fichier de direction Gaia (*gaia-morphodynamics.cas*) créé ci-dessus, qui nécessite certains paramètres obligatoires et permet beaucoup plus de paramètres de mots-clés optionnels. Vous trouverez un aperçu des mots-clés disponibles dans le manuel de référence de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/reference/gaia_reference_9.0.pdf) et le fichier du dictionnaire de Gaia `/telemac/v9.0.0/sources/gaia/gaia.dico`. Comme pour le fichier de direction hydrodynamique Telemac2d ou Telemac3d, le fichier de direction Gaia peut être distingué entre les groupes clés pour les paramètres généraux (liés au fichier), physiques (transport des sédiments) et numériques. Cette section présente les paramètres généraux qui englobent la configuration des fichiers d'état des limites et les définitions de base des caractéristiques des sédiments et des lits de rivière. La mise en œuvre de {term}`Bedload` et/ou {term}`Suspended load` est traitée dans des sections distinctes.

(gaia-gen)=
## Paramètres généraux

Les paramètres généraux définissant les fichiers d'entrée et de sortie obligatoires ressemblent à ceux du fichier de direction hydrodynamique. Les fichiers d'entrée peuvent même être les mêmes utilisés dans le fichier de direction hydrodynamique. Par exemple, **définir** le **[qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf)** du fichier de géométrie {ref}`pre-processing <slf-prepro-tm>` **. En outre, ajouter **boundaries-gaia.cli** sous **DOSSIER DES CONDITIONS BONDAIRES**, qui sera expliqué dans la section sur {ref}`boundary conditions for Gaia <gaia-bc>`. Le mot clé Gaia **RESULTS FILE** devrait également différer du mot clé RESULTS FILE dans le fichier de direction hydrodynamique.

```fortran
/ gaia-morphodynamics.cas
/
/ COMPUTATION ENVIRONMENT
/
GEOMETRY FILE : qgismesh.slf
BOUNDARY CONDITIONS FILE : boundaries-gaia.cli
RESULTS FILE : rGaia-steady2d.slf
MASS-BALANCE : YES
```

Les variables de sortie graphiques liées au transport des sédiments peuvent être définies avec le mot clé **VARIABLES POUR PRINTOUTS GRAPHIQUES** pour {term}`Bedload` et/ou {term}`Suspended load` et les options de liste suivantes:

* `B` pour l'élévation du fond (m a.s.l.)
* `E` pour l'évolution du bas en (m)
* `F` for {term}`Froude number` (-)
* `M` pour l'ampleur (longueur) de l'unité bidirectionnelle (c.-à-d., $x$ et $y$ directions) transport des sédiments $\boldsymbol{q_s}$ (lisez plus dans la définition de l'unité {term}`Exner equation`) à (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `MU` pour le coefficient de frottement cutané (en fonction de {ref}`skin friction correction factors <c-friction>` décrit dans la section sur la charge de lit)
* `N` pour le transport de lit à l'unité à $x$-direction $\boldsymbol{q_b}\cdot\cos\alpha$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$) où $\alpha$ est l'angle entre l'axe longitudinal ($x$) et le vecteur de transport solide $\boldsymbol{q_b}$.
* `P` pour le transport de l'unité en lit à $y$-direction $\boldsymbol{q_b}\cdot\sin\alpha$ à (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `QSBL` pour l'ampleur (longueur) de l'unité bidirectionnelle (c.-à-d., $x$ et $y$ directions) **charge (seulement)** transport $\boldsymbol{q_b}$ in (kg$\cdot$m$^{-1}\cdot$s$^{-1}$)
* `R` pour le fond non comestible (m a.s.l.)
* `S` pour l'élévation de la surface de l'eau à (m a.s.l.)
* `TOB` pour la contrainte de cisaillement du lit à (N$\cdot$m$^{-2}$)

Les paramètres `M` et `QSBL` auront la même sortie si aucune charge suspendue n'est simulée. Pour afficher plusieurs paramètres, **set** le mot-clé **VARIABLES POUR PRINTOUTS GRAPHIQUES** pour ce tutoriel comme suit:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : B,E,M,MU,N,P,QSBL,TOB
```

(gaia-bc)=
## Conditions limites

Les conditions limites de Gaia fonctionnent de la même manière que l'hydrodynamique et peuvent être dérivées de l'hydrodynamique [boundarys.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) file.


````{admonition} Boundary conditions file structure and mass balance
:class: tip

Rappelez-vous la structure de l'hydrodynamique [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) fichier, qui a 13 valeurs (c.-à-d. colonnes) par ligne (ligne), qui sont séparés par un `space` et c'est comme ça que la tête de fichier ressemble (pour les limites de mur fermé `2`-type):

```
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000         138           1   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9836           2   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9838           3   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9194           4   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9827           5   #
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9828           6   #
...
```
Les colonnes (1) à (7) sont les mêmes que celles du fichier hydrodynamique [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli) et les significations de colonne/valeur sont:

* (1) `LIHBOR`: code limite pour la profondeur du flux
* (2) `LIUBOR`: code limite pour le composant $u$ vitesse
* (3) `LIVBOR`: code limite pour le composant $v$ vitesse
* (4) `HBOR`: valeur de profondeur de flux (en m) *-non utilisé dans ce tutoriel*
* (5) `UBOR`: $u$ vitesse (m$\cdot$s$^{-1}$) *-non utilisé dans ce tutoriel*
* (6) `VBOR`: $v$ vitesse (m$\cdot$s$^{-1}$) *-non utilisé dans ce tutoriel*
* (7) `AUBOR`: coefficient de frottement *-non utilisé dans ce tutoriel*
* (8) `LIEBOR`: **Code de limite spécifique à Gaia** pour l'évolution du lit de rivière (ou concentration pour les sédiments cohésifs)
* (9) `Q2BOR`: **Décharge solide spécifique à Gaia** (utilisée pour la charge en lit, en kg$\cdot$m$^{-1}\cdot$s$^{-1}$) ou concentration de sédiments près du lit (en g$\cdot$L$^{-1}$) en cas de charge en suspension (ou de sédiments cohésifs)
* (10) `EBOR`: **Gai spécifique** élévation du lit de rivière (m a.s.l.)
* (11) `CBOR`: **Équilibre spécifique à Gaia** concentration de sédiments en suspension (en g$\cdot$L$^{-1}$) pour la modélisation de charge en suspension (lire plus dans le {ref}`section on suspended load <gaia-sl>`)
* (12) Numéro du point
* 13) Numéro d ' ordre du point de frontière

**La structure du fichier des conditions limites varie entre les modèles Gaia couplés à Telemac2d et à Telemac3d. Ainsi, lors du passage des modèles 2d à 3d, créez de nouveaux fichiers de conditions limites.**

The Gaia-specific boundary type (column 8: `LIEBOR`) of the Gaia boundaries condition can be defined with the following `integer` values:

* `1` définit les limites de l'onde incidente ou Thompson
* `2` définit les limites des murs
* `4` définit les limites libres (Neumann)
* `5` définit une limite de valeur imposée (Dirichlet)

Similar to the hydrodynamics, solid (sediment) discharges (Dirichlet condition: `LIEBOR=5`) can either be defined directly in the boundaries file (i.e., with the `Q2BOR` columns 9), through the keywords **PRESCRIBED SOLID DISCHARGES** or `CLASSES IMPOSED SOLID DISCHARGES DISTRIBUTION`, or as time-series in a liquid boundaries file. The sediment (bedload or suspended load) will adapt to Neumann-type outflow (i.e., `LIEBOR=4`) or equilibrium inflow boundaries. The below box provides more details and for more guidance go to sections 2.3 and 3.1.10-3.1.12 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

Pour ce tutoriel, commencez par **créer une copie du fichier hydrodynamics.cli**, nommez-le **borderies-gaia.cli** et **remplacez la colonne (8)** (c.-à-d. tous `LIHBOR` occurrences) avec les valeurs suivantes:

* Frontières fermées (anciennement `LIHBOR=2`): `LIEBOR=2`
* Limites ouvertes de sortie (anciennement `LIHBOR=4`): `LIEBOR=4`
* Ouvrir les limites d'entrée (anciennement `LIHBOR=5`): `LIEBOR=5` et régler l'entrée d'équilibre dans le fichier de direction (voir ci-dessous)

** La masse de la décharge solide à travers les frontières ouvertes et l'évolution du lit dans le domaine du modèle devraient être cohérentes.** Lorsque les limites du modèle ont un lit statique, elles peuvent causer des erreurs de bilan massique. Une approche appropriée pour prescrire un lit dynamique avec une morphodynamique de conservation de masse est de prescrire un lit d'équilibre à la limite d'entrée. Si la limite d'entrée se trouve dans une zone où l'on peut s'attendre à une érosion, il est important d'avoir plus d'érodibilité dans les cours d'eau. Ainsi, dans ce tutoriel, la limite d'entrée est implémentée avec la condition d'équilibre à travers le fichier de direction (voir ci-dessous), et la limite de sortie avec le type Neumann (c.-à-d., `LIEBOR=4`).

Pour définir les rejets solides à l'équilibre (charge de lit) et la concentration de sédiments en suspension aux limites d'entrée, **ajouter les éléments suivants** au dossier de direction de Gaia :

```fortran
/ gaia-morphodynamics.cas
/
/ BOUNDARY CONDITIONS
EQUILIBRIUM INFLOW CONCENTRATION : YES / use an equilibrium approach at inflow nodes
```
Le mot-clé `EQUILIBRIUM INFLOW CONCENTRATION` correspond à l'hydrodynamique **TREATMENT DES FLUX AUX BONDAIRES** et calcule la concentration de sédiments en suspension près du lit avec des formules empiriques (lire la suite dans le mot {ref}`section on suspended load <gaia-sl>`).
````

```{admonition} Neumann vs. Dirichlet sediment inflow boundaries
:class: dropdown

Si le modèle contient des sources de sédiments clairement définies, avec des quantités connues de sédiments, les conditions limites d'entrée des sédiments de type dirichlet (valeur imposée) sont préférables. Par exemple, si un modèle de perte de sol du bassin hydrographique, comme l'équation universelle révisée de perte de sol (RUSLE) {cite:p}`renard1997`, est disponible, l'approvisionnement en sédiments avec des sédiments fins (cohésifs) peut être défini plus précisément. Par contre, si l'entrée et le transport des sédiments sont entraînés par le débit en vrac, les limites d'équilibre peuvent être plus appropriées.
```

(gaia-sed)=
## Classes de sédiments

Les classes de sédiments utilisées pour Gaia sont définies dans le dossier de direction et représentent les valeurs initiales. Au cours d'une simulation, l'érosion, le transport et le dépôt modifient la répartition spatiale et temporelle des classes de sédiments dans le maillage de calcul du modèle. Cette section présente la configuration de base de la classe de sédiments pour définir une ou plusieurs classes de granulométrie ayant des caractéristiques spécifiques, comme la densité des sédiments. Les sections suivantes sur {ref}`bedload <gaia-bl>` et {ref}`suspended load <gaia-sl>` vont au-delà de ces définitions de base et expliquent comment définir les équations de transport de la charge de lit ou les concentrations de sédiments en suspension.

Gaia distingue les sédiments non cohésifs et cohésifs par le mot clé **CLASSES TYPE DE SEDIMENT**, où les valeurs suivantes s'appliquent:

* `NCO` définit **n**on-**co**sédimentéhésif
* `CO` définit **co**sédiment hesif

Plusieurs types de sédiments peuvent être attribués, séparés par un point-virgule (`;`). Pour garder le tutoriel simple, seuls les sédiments non cohésifs sont utilisés (la mise en œuvre des sédiments cohésifs est toutefois similaire):

```fortran
/ continued: gaia-morphodynamics.cas
/
/ ...
/ SEDIMENT
CLASSES TYPE OF SEDIMENT : NCO;NCO;NCO
```

```{admonition} Cohesive sediment
:class: dropdown

Pour les sédiments cohésifs, des paramètres supplémentaires peuvent être définis, tels que:

* **La CONCENTRATION MUD PAR LAYER** définit les concentrations massiques dans chaque couche (jusqu'à 20) pour le modèle de consolidation à ($g\cdot L^{-1}$).
* **LAYERS PARTHENIADES CONSTANT** defines erosion fluxes in (kg$\cdot$m$^{-2}\cdot$s$^{-1}$) for each layer (up to 20 layers).
* **LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD** définit la contrainte critique de cisaillement d'érosion dans (N$\cdot$m$^{-2}$) pour chaque couche (jusqu'à 20 couches).
* **LAYERS MUD CONCENTRATION** définit les concentrations massiques dans (g$\cdot$L$^{-1}$) pour chaque couche (jusqu'à 20 couches) du modèle de consolidation.
* Beaucoup d'autres sont listés dans [Manuel de référence Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/reference/gaia_reference_9.0.pdf).
```

Le nombre de valeurs assignées aux mots-clés suivants doit correspondre au nombre de classes de sédiments défini ci-dessus (ici: trois). D'autres caractéristiques obligatoires des sédiments se rapportent à la taille du grain (** DIAMÈTRES DE SÉDIMENT DE CLASSES** en mètres) et à la densité (** DENSITÉ DE SÉDIMENT DE CLASSES** en kg$\cdot$m$^{-3}$) d'une classe de sédiments. Pour définir les classes de gravier, de galets et de sable, mettre à jour le dossier de direction comme suit:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ ...
/ SEDIMENT
CLASSES TYPE OF SEDIMENT : NCO;NCO;NCO
CLASSES SEDIMENT DIAMETERS : 0.05;0.1;0.0005
CLASSES SEDIMENT DENSITY : 2680;2680;2680
```

Ce tutoriel utilise trois classes de granulométrie et la densité des sédiments est ici supposée être la même pour les trois classes. Dans le monde réel, les particules plus lourdes (densité plus élevée) ont tendance à être plus grossières et sont moins susceptibles de se déplacer loin en aval dans une rivière donnée. Il faut garder ce phénomène à l'esprit lorsqu'on suppose une densité caractéristique de sédiments.

Dans les sédiments classés, une fraction initiale** du matériau du lit est attribuée à chaque classe de granulométrie avec le mot clé **CLASSES INITIAL FRACTION**. La somme de toutes les fractions de classe doit être égale à une. La fraction peut être estimée à partir des courbes de tamisage, par exemple, en déterminant le pourcentage que chaque classe de sédiments constitue du diamètre des particules $D_{84}$. Dans ce tutoriel, les classes de sédiments ont les fractions initiales suivantes:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ ...
CLASSES INITIAL FRACTION : 0.45;0.45;0.1
```

Les classes de taille des particules peuvent également être assignées à des valeurs spécifiques {term}`Shields parameter` (**CLASSES CRITIQUE SHEAR STRESS**) ou à des vitesses de décantation (**CLASSES SETTLING VELOCITÉS**), par exemple, pour imposer des conditions de non-érosion ou de non-déposition. Il est à noter que le mot-clé SISYPHE NUMÉRO DES TAILLES DES MATÉRIAUX BÉD est obsolète à Gaia.

Les formules particulières de transport des sédiments pour simuler {term}`Bedload` ou {term}`Suspended load` sont liées aux phénomènes à l'étude et leur mise en œuvre dans le dossier de pilotage Gaia est expliquée dans les sections suivantes.

```{admonition} Zonal sediment size and fraction definitions
:class: tip
Les classes de taille des sédiments peuvent être déclarées pour des zones particulières d'un modèle, semblables aux zones de friction (appelez la zone de friction au bas de la {ref}`section on friction boundaries <tm2d-friction>`). Ainsi, un fichier Selafin (`*.slf`) contenant des caractéristiques de lit de rivière peut être déclaré avec la géométrie dans le fichier de direction de Gaia. Un exemple pour les définitions zonales des sédiments est fourni avec le modèle Wilcock-Crowe dans l'installation TELEMAC (par exemple, `/telemac/v9.0.0/examples/gaia/wilcock_crowe-t2d/` - jeter un oeil à **gai ref WC2003.slf** à {ref}`BlueKenue <bluekenue>`).
```

(gaia-active-lyr)=
### Couche active

Le {ref}`boundary conditions <gaia-bc>` d'un modèle définit les taux d'approvisionnement en sédiments (entrée) et de débit, qui peuvent provenir de stations de mesure, de mesures ou de modèles de perte de sol du bassin hydrographique, comme l'équation révisée de la perte universelle de sol (RUSLE) {cite:p}`renard1997`. Les sédiments qui passent juste par le modèle et se règlent de temps en temps avant d'être mobilisés à nouveau (par la théorie {cite:t}`einstein_bed-load_1950`s) sont appelés charge de lavage ou charge de lit itinérante {cite:p}`piton_concept_2017`. Cependant, les sédiments peuvent aussi être recrutés (érodés) dans le lit de la rivière ou déposés sur le lit de la rivière à l'intérieur des limites du modèle. Pour indiquer à un modèle morphodynamique quelles profondeurs il peut éroder (p. ex. parce que le substrat rocheux ou le béton est présent ci-dessous), on peut définir une couche active. En outre, plusieurs couches de lit peuvent être définies sous la couche active, par exemple, pour mettre en œuvre la stratification des sédiments dans le lit de rivière en fonction de la taille des grains. La stratification de la taille des grains joue un rôle particulièrement lorsque le lit de rivière est blindé, ce qui signifie que la couche de sédiments la plus haute est significativement plus grossière que les couches de sédiments plus profondes {cite:p}`hirano1971`. {numref}`Figure %s <active-layers>` illustre qualitativement ce concept, où la couche la plus haute est la couche active (également appelée couche de mélange en Gaia) et les sous-couches inférieures constituent le substrat du lit de rivière.

```{figure} ../../img/telemac/active-layers-web.jpg
:alt: active mixing layer riverbed hyporheic zone
:name: active-layers

Illustration qualitative de la couche active (couche de mélange) et des couches du substrat du lit de rivière. La couche active est à la surface, en contact direct avec la colonne d'eau (figure adaptée conceptuellement de {cite:t}`du_boys_etudes_1879` et {cite:t}`church_what_2017`).
```

Le concept de couche active a été initialement introduit par {cite:t}`du_boys_etudes_1879` comme une séquence de couches du lit de rivière, qui se déplacent à différentes vitesses (plus la couche est profonde, plus la vitesse est lente). {cite:t}`du_boys_etudes_1879` décrit que l'épaisseur de chaque couche était égale au diamètre de la granulométrie représentative et que le lit actif (c.-à-d. la somme de toutes les couches mobiles) peut être jusqu'à 10 fois la granulométrie représentative (c.-à-d. environ 10 diamètres de grains) {cite:p}`frey2011,ravelet2013`. {cite:t}`hirano1971` ramassé sur ce concept et caractérisé la couche active comme une couche d'échange d'une épaisseur de plusieurs fois la $D_{50}$, entre une sous-couche immobile et une couche entièrement mobile dans le flux en vrac le long du lit de rivière. Plusieurs procédés (p. ex. cisaillement hydraulique, collision de grain ou tri) dominent dans la couche d'échange et l'épaisseur de la couche d'échange a été définie différemment par plusieurs auteurs. L'une des raisons des différentes définitions de l'épaisseur de la couche active est qu'elle dépend également de la proportion de la teneur en sédiments fins. La différence entre les sédiments grossiers et fins est que les sédiments fins peuvent former des couches de lit comme des ondulations ou des dunes. Ainsi, en présence de sédiments fins, comme le sable (diamètre inférieur à 1-2 mm), seuls les modèles prenant en compte les formes de lit dans la couche active peuvent reproduire l'aggradation ou la dégradation du lit et les effets de tri des grains {cite:p}`blom2008`. Cependant, un modèle prenant en compte les formes de lit composées de sédiments fins décrit la couche active en fonction (0,5 fois) de la hauteur des dunes (c.-à-d. méga ondulations) {cite:p}`kleinhans2005`, ce qui contraste avec la définition de l'épaisseur de la couche active comme un multiple d'un diamètre de grain (p. ex., 3$\cdot D_{50}$). Ainsi, il y a **deux** définitions paramétriques concurrentes et **conceptuelles de la couche active**, c'est pourquoi {cite:t}`church_what_2017` propose la terminologie suivante qui est adaptée dans ce livre électronique:

* La couche **active décrit le lit de rivière immédiatement mobile** où **temps réel**, **déplacement dynamique** des particules. Son épaisseur est un multiple du diamètre caractéristique du grain.
* La couche **disturbance englobe la progression des vagues de sable** sous la forme de **scour et de remplissage** sur une échelle **événement**. Son épaisseur est de 0,5 fois la hauteur des dunes (ou ondulations).

Bien que Gaia n'accepte qu'un mot-clé **ACTIVE LAYER THICNESS**, il peut se référer à la couche *active* comme un multiple de la taille représentative du grain, ou lorsque les sédiments fins sont présents ($\geq$ 20%), à la couche *disturbance* avec une épaisseur de 0,5 fois la hauteur de la dune. Lorsque le lit de la rivière est composé de galets et de gravier avec une petite part de sédiments fins (environ 1 % à 20 %), l'épaisseur active de la couche doit être généreusement supposée avec un multiple (2-3 fois) de la taille des galets.

```{admonition} Gaia's active layer terminology
:class: note
Dans Gaia, les termes **couche active** et **couche mixte** sont synonymes : les deux se rapportent à la couche de sédiments la plus haute qui est en contact direct avec la colonne d'eau. Cette couche fournit du matériel qui peut être transporté comme charge de lit ou en suspension, et elle reçoit des sédiments déposés. Les couches inférieures à la couche active sont appelées **substratum**.
```

L'épaisseur de la couche active est une valeur de **cible** définie par l'utilisateur dans Gaia (par défaut : 10 000 m, qui mélange efficacement tout le lit). La couche active est automatiquement créée à la surface du lit de sédiments au début d'une simulation lorsque plus d'une classe de sédiments est définie. Pendant la simulation, Gaia maintient l'épaisseur de la couche active cible par des échanges avec le substrat:

* **Pendant l'érosion**: La masse des sédiments est retirée de la couche active pour le transport ou la suspension du lit. Pour maintenir l'épaisseur cible, Gaia transfère la masse du substrat (la première couche non vide sous la couche active) dans la couche active. Le matériau transféré a la composition du substrat, qui peut changer la composition de la couche active au fil du temps.
* **Pendant le dépôt**: La masse des sédiments est ajoutée à la couche active. Pour maintenir l'épaisseur cible, Gaia transfère l'excès de masse de la couche active au substrat. Le matériau transféré a la composition de la couche active.

Si l'épaisseur des sédiments disponibles est inférieure à l'épaisseur de la couche active cible à n'importe quel nœud, l'épaisseur réelle de la couche active est égale à celle des sédiments disponibles. Ce comportement implémente l'algorithme du lit rigide de Gaia (fond non-érodable), où l'érosion ne peut pas dépasser la masse de sédiments disponible dans la couche active à n'importe quelle étape du temps.

Le lit de rivière peut être stratifié en plusieurs sous-couches (cf. {numref}`Fig. %s <active-layers>`) en définissant le mot clé **NUMBRE DES LAYERS POUR LA STRATIFICATION INITIALE** (entier, par défaut: 1). Gaia divise ensuite verticalement le lit de rivière en nombre de couches définies par l'utilisateur plus une, où la couche plus une correspond à la couche active qui est ajoutée en haut. L'épaisseur des couches initiales de lit de rivière peut être définie avec le mot clé **LAYERS INITIAL THICKNESS** (par défaut: 100 m). Si le **ACTIVE LAYER THICKNESS** est plus grand que la première couche de la stratification initiale, Gaia fusionne la première couche dans la couche active et prend des sédiments supplémentaires de couches plus profondes si nécessaire pour atteindre l'épaisseur cible. La composition initiale de la couche active devient alors un mélange de sédiments provenant de ces couches fusionnées.

```{admonition} What happens when Gaia deposits sediment?
Le dépôt de sédiments dans un noeud de grille ajoute de la masse à la couche active. Comme Gaia maintient l'épaisseur de la couche active cible, une portion équivalente de sédiments est transférée de la couche active au substrat (la première couche ci-dessous). Ce flux a la composition de la couche active, donc le dépôt modifie la composition du substrat tandis que la composition de la couche active change selon ce qui a été déposé.
```

Dans ce tutoriel, un mélange de sable, de gravier et de sédiment de galets est utilisé avec une TAILLE DE LAYER ACTIVE** de 3 $\cdot D_{90}$ (de galets). Le lit de rivière est initialement stratifié en trois sous-couches (plus la couche active de 0,3 m d'épaisseur) et l'épaisseur initiale des couches de lit de rivière est supposée avec 1,5 m avec les définitions de mots clés suivantes dans le fichier de direction de Gaia:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ ...
/ RIVERBED LAYERS
ACTIVE LAYER THICKNESS : 0.3 / multiple of D90 - default is 10000
NUMBER OF LAYERS FOR INITIAL STRATIFICATION : 3 / default is 1
LAYERS INITIAL THICKNESS : 1.5 / m - default is 100
```

Gaia dérive des couches mixtes de sédiments cohésifs et non cohésifs de la composition de la couche active. Pour les sédiments mixtes, Gaia calcule le transport de la charge de lit seulement lorsque la fraction massique des sédiments cohésifs dans la couche active est inférieure à 30 %. Au-delà de ce seuil, les sédiments non cohésifs peuvent encore être transportés en suspension. Le [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) fournit de plus amples renseignements sur le transport des sédiments mixtes (cohésifs et non cohésifs) à la section 3.2.1. En outre, on peut simuler la consolidation du lit de rivière en définissant le mot-clé **Modél** avec `2` (cf. [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf), section 3.3).

## Charge de lit contre charge suspendue

La modélisation du transport des sédiments devient rapidement coûteuse en calcul. Par conséquent, il est important d'être clair sur le type principal de transport des sédiments et d'activer seulement le phénomène le plus important (c.-à-d. soit {term}`Bedload` ou {term}`Suspended load`). Pour cette raison, répondez à la question *** Quel est le type de phénomène de transport des sédiments prédominant dans le modèle***? Si vous n'êtes pas sûr de la réponse à cette question, révisez la section sur {ref}`sediment transport modes <gaia-seditrans>`. En outre, voici quelques suggestions axées sur la pratique :

 * **Téléchargement uniquement**: La modélisation de la charge en suspension dans un lit de gravier-cobble avec une teneur en sable (c.-à-d., les sédiments sont généralement supérieurs à 2 mm) inférieure à 5-10 % n'est pas utile et la définition `SUSPENSION FOR ALL SANDS : NO` devrait être utilisée. Dans ce cas, le {ref}`section on bedload modeling <gaia-bl>` fournit toutes les informations nécessaires et la section de charge suspendue peut être ignorée.
* ** Charge suspendue seulement**: Le déplacement des particules fines dans les réservoirs, les lacs ou les zones côtières implique principalement des processus de charge en suspension. Si les sédiments sont généralement plus fins que 1 mm, la modélisation de la charge de lit peut ne pas être nécessaire. Dans ce cas, sauter la section de modélisation de la charge de lit et directement sauter à la {ref}`section on suspended load modeling <gaia-sl>`.
* ** Charge en vrac et en suspension**: Lorsque le mélange de sédiments comporte des particules de sable dont le diamètre est compris entre 1 et 2 mm et/ou des particules qui peuvent être plus fines ou plus grossières, les processus de transport mixte conduisent au transport des sédiments. Dans ce cas, les deux sections sur {ref}`bedload <gaia-bl>` et {ref}`suspended load <gaia-sl>` modélisation doivent être accomplies.
* **Sédiment cohésif**: Lorsque les sédiments cohésifs sont dans le système (c.-à-d. que le diamètre du grain est inférieur à 0,06 mm), il faut activer la modélisation {ref}`suspended load <gaia-sl>`.

Ce livre électronique présente la mise en œuvre de la modélisation combinée de la charge de lit et de la charge en suspension dans une courte section de rivière avec un lit de galets de gravier et une teneur en sable de 10% (avec la classe de 0,5 mm).