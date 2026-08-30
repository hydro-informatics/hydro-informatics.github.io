---
description: Tutoriel pour la modélisation d'hydrographies de décharge et d'inondations instables (quasi-stables) avec des débits de temps discrétisants de Telemac2d pour des simulations hydrauliques de rivière 2D.
---

(chpt-unsteady)=
# Pas stable 2d

```{admonition} Requirements
Ce tutoriel est conçu pour ** modélistes avancés** et avant de plonger dans ce tutoriel assurez-vous de compléter les tutoriels {ref}`TELEMAC pre-processing <slf-prepro-tm>` et {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>`.

Le cas présenté dans ce tutoriel a été établi avec le logiciel suivant:
* un éditeur de texte, comme {ref}`Notepad++ <npp>` (tout autre éditeur de texte fera le travail).
* Télémac v8p2r0 ou plus récent ({ref}`standalone installation <modular-install>`).
* {ref}`QGIS <qgis-install>`.
* Debian Linux 11 installé sur une machine virtuelle (en savoir plus sur {ref}`software chapter <chpt-vm-linux>`).
```

## Commencez

L'hypothèse {ref}`steady 2d tutorial <telemac2d-steady>` que la décharge d'une rivière est constante au fil du temps. Cependant, le débit d'une rivière n'est jamais vraiment constant (c.-à-d. jamais stable) et varie légèrement de seconde à seconde, même dans les rivières contrôlées. Pour modéliser les débits intrinsèquement instables des rivières, nous pouvons discriminer les débits dépendant du temps (p. ex., un hydrographe d'inondation) dans un modèle numérique comme une série de débits réguliers. {numref}`Figure %s <unsteady-hydrograph>` illustre la discrétisation d'un hydrographe d'inondation naturel en étapes de débits réguliers, qui sera utilisé dans ce chapitre. Notez que l'hydrographe ** commence à temps = 15000**, ce qui est le résultat de la simulation stable2d à sec.

```{figure} ../../img/telemac/unsteady-hydrograph.png
:alt: unsteady flow discharge quasi steady telemac telemac2d hydrodynamic
:name: unsteady-hydrograph

La discrétisation d'un hydrographe continu en étapes de débits réguliers (hydrographe qualitatif pour ce tutoriel).
```

Ce chapitre présente la mise en œuvre d'un hydrographe de décharge quasi stationnaire dans une simulation de Telemac2d hydrodynamique par la définition d'une séquence d'écoulement (cercles rouges dans {numref}`Fig. %s <unsteady-hydrograph>`). Le tutoriel s'appuie sur la simulation régulière d'une décharge de 35 m$^3$/s et nécessite les données suivantes des tutoriels {ref}`pre-processing <slf-prepro-tm>` et {ref}`steady2d <telemac2d-steady>`, qui peuvent être téléchargés en cliquant sur les noms de fichiers :

* Le maillage informatique [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf) fichier (usages **EPSG:32633** - ETRS 89 / UTM zone 33N).
* Les définitions des limites [boundaires.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli) fichier.
* Le fichier des résultats [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) du {ref}`dry initialized steady 2d simulation <tm2d-init-dry>` finissant à `t=15000` pour 35 m$^3$/s.

Envisagez de sauvegarder les fichiers dans un nouveau dossier, comme `/unsteady2d-tutorial/`.

```{admonition} Unsteady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/).
```

(prepro-unsteady)=
## Adaptations modèles

La mise en œuvre de flux instables nécessite l'adaptation de mots-clés et de mots-clés supplémentaires (par exemple, pour lier les fichiers de limites liquides) dans le fichier de direction (`.cas`) à partir du tutoriel stabilisate2d ([télécharger stabilisate2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

```{admonition} View the unsteady steering file
Pour voir l'intégration des mots-clés de simulation instables dans le fichier de pilotage, [téléchargez unsteady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/unsteady2d.cas).
```

(tm2d-hotstart)=
### Conditions initiales de démarrage à chaud

**Les descriptions suivantes se réfèrent à la section 4.1.3 du [Manuel de Télémac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Pour accélérer les calculs et fournir une base de référence bien convergente pour les calculs quasi stationnaires, ce tutoriel réutilise la sortie de la simulation stable 2d avec des conditions initiales sèches (voir la section {ref}`tm2d-init-dry`). Ce type d'initialisation du modèle s'appelle aussi *hotstart*. Pour démarrer la simulation, le fichier de résultats stables [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) doit être défini comme étant **DOSSIER DE COMPUTATION PRÉCÉDENT**:

```fortran
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
/ INITIAL TIME SET TO ZERO : 0 / avoid restarting at 15000
```

Un mot clé **INITIAL TEMPS SET TO ZERO** peut être défini pour réinitialiser l'heure du fichier de calcul précédent de `15000` à `0`. Cependant, ce tutoriel n'utilise pas cette option et se poursuit à l'étape 15000.

Pour éviter les définitions ambiguës des conditions initiales, **désactiver** (c.-à-d. supprimer ou commenter les lignes avec un `/`) le mot-clé ** CONDITIONS INITIALES**:

```fortran
/ INITIAL CONDITIONS : 'ZERO DEPTH'
```

### Paramètres généraux

Pour simuler l'hydrographe indiqué à {numref}`Fig. %s <unsteady-hydrograph>`, la simulation doit courir pendant au moins 15000 autres étapes (c.-à-d. de `t=15000` à `t=30000`). Puisque les résultats d'impression (intermédiaires) ont un effet significatif sur le temps de calcul, augmentez le temps d'impression graphique à `500` (c.-à-d., réduisez la fréquence d'impression par rapport à `200` utilisé pour la simulation régulière) :

```fortran
TIME STEP : 1.
NUMBER OF TIME STEPS : 15000
GRAPHIC PRINTOUT PERIOD : 500
LISTING PRINTOUT PERIOD : 500
```

(tm2d-liq-file)=
### Limites ouvertes

Cette section présente les conditions d'écoulement quasi stationnaires (non stables) aux limites ouvertes des liquides avec un hydrographe d'écoulement dépendant du temps et un en aval {term}`Courbe d'étalonnage <Stage-discharge relation>` (rappelez les raisons derrière le choix des types de limites de {ref}`pre-processing tutorial <bk-liquid-bc>`).


```{admonition} Boundary conditions and mass balance

Les paramètres des conditions limites affectent le bilan massique, qui est un critère crucial pour un modèle numérique sonore. En savoir plus dans le chapitre sur la mise en place {ref}`boundary conditions for mass balance <foc-mass-bc>`.
```


---

**Définir un hydrographe quasi stable**

Avec le modèle initialisé sec se terminant à $t$=15000, l'hydrographe doit commencer à `15000`, même si le début du modèle représentera le temps *zéro* de la simulation instable. Pour implémenter l'hydrographe en forme triangulaire montré à {numref}`Fig. %s <unsteady-hydrograph>`, **créez un nouveau fichier appelé `inflows.liq`** dans le dossier de simulation. Ouvrez le nouveau fichier `inflows.liq` dans un éditeur de texte et ajoutez les points en cercle rouge dans {numref}`Fig. %s <unsteady-hydrograph>` comme informations de flux dépendant du temps aux limites **upstream (1)** et **downstream (2)** open (liquide). Dans ce fichier :

* Ajouter un en-tête de fichier commençant par `#` signes (lignes commentées ignorées par TELEMAC).
* Mettre en œuvre 2 colonnes pour le temps **T** ($t$) et le taux d'entrée en amont **Q(1)**.
* Séparer les colonnes avec *espaces*.
* La première colonne doit être time `T` avec des valeurs qui augmentent strictement de façon monotone et la dernière valeur doit être supérieure ou égale à la dernière étape de simulation.

```{admonition} How does Telemac count open (liquid) boundaries?
Cette information, ainsi que d'autres sur la définition des limites, est fournie dans le chapitre des projecteurs sur {ref}`boundary conditions <tm-foc-bc>`.
```

Ainsi, le fichier [inflows.liq](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/inflows.liq) devrait ressembler à ceci:

```python
# Inflow hydrograph
#
T	Q(1)
s	m3/s
15000	35
16000	35
17000	50
19000	1130
22000	101
25000	35
99000	35
```

Le fichier *boundaires.cli* original décrit la limite en aval avec *prescriptiond Q et H* (type `5 5 5`). Cependant, dans le calcul instable, `Q` doit être libre (autrement, Q(2) doit être défini dans `inflows.liq` avec une colonne supplémentaire) et pour cette raison, le fichier `boundaries.cli` nécessite quelques adaptations:

* **Ouvrir** le fichier [boundarys.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli) avec un éditeur de texte (par exemple, {ref}`npp` sur Windows).
* Utilisez les touches de recherche et de remplacement (par exemple, `CTRL` + `H` à {ref}`Notepad++ <npp>`, ou `CTRL` + `F` à d'autres éditeurs de texte):
  * **Trouver** `5 5 5`
  * **Remplacement** avec `4 5 5`
  * Cliquez sur **Replacer** tous les nœuds en amont.
* **Enregistrer** le fichier comme **borderies-unsteady.cli** et le fermer.

Pour vérifier les paramètres corrects [téléchargez les limites-unsteady.cli](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/boundaries-unsteady.cli) pour la simulation unsteady.

Dans le fichier **steering**, adapter le nom du fichier ** pour les conditions limites** et ajouter le lien à **inflows.liq**:

```
BOUNDARY CONDITIONS FILE : boundaries-unsteady.cli
/ ...
LIQUID BOUNDARIES FILE : inflows.liq
```

---

**Courbe de cotation (relation entre l'étage et la décharge)**
Pour activer l'utilisation d'un {term}`Courbe d'étalonnage <Stage-discharge relation>` pour une limite ouverte (liquide), le mot clé **STAGE-DISCHARGE CURVES** doit être ajouté au fichier de direction. Ce mot-clé nécessite une liste composée des entiers suivants:

* `0` est le **default** qui désactive l'utilisation d'une courbe de décharge.
* `1` applique les élévations prescrites en fonction du débit calculé (décharge).
* `2` applique les débits prescrits (décharge) en fonction de l'altitude calculée.

Le mot-clé **STAGE-DISCHARGE CURVES** est une liste qui attribue l'un des trois entiers (soit `0`, `1`, ou `2`) aux limites ouvertes (liquides). Dans ce tutoriel, le réglage `STAGE-DISCHARGE CURVES : 0;1` active l'utilisation d'un {term}`Courbe d'étalonnage <Stage-discharge relation>` pour la limite en aval uniquement lorsque le **en amont de la limite ouverte 1** est défini à `0` et le **en aval de la limite ouverte 1** est défini à `0`.

Le formulaire (courbe) du {term}`Courbe d'étalonnage <Stage-discharge relation>` doit être défini dans un fichier de sortie d'étape ({term}`ASCII` format texte). Ces fichiers s'appliquent généralement à la limite en aval d'un modèle aux sections de contrôle (p. ex., un déversoir libre). Ce tutoriel utilise la relation suivante qui est stockée dans un fichier appelé [ratingcurve.txt (télécharger)](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/ratingcurve.txt):

```
# Downstream ratingcurve.txt
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
```


````{admonition} How to assign different stage-discharge curves at multiple boundaries?
:class: tip, dropdown

Pour définir {term}`Courbe d'étalonnage <Stage-discharge relation>`s à plusieurs limites ouvertes (p. ex., aux dérivations fluviales ou aux affluents), ajouter les courbes au même fichier. TELEMAC reconnaît automatiquement où les courbes s'appliquent par le nombre indiqué entre parenthèses après le nom du paramètre dans l'en-tête de colonne. Par exemple, dans l'exemple ci-dessus pour ce tutoriel, les en-têtes de colonne `Z(2)` et `Q(2)` dire à TELEMAC d'utiliser ces valeurs pour la deuxième (c.-à-d. ici, la limite en aval) ouverte. L'ordre des colonnes n'est pas important car TELEMAC lit le type de courbe (c.-à-d. soit $Q(Z)$ ou $Z(Q)$) à partir du mot-clé **STAGE-DISCHARGE CURVES**.

Le bloc de fichiers suivant prescrirait {term}`Courbe d'étalonnage <Stage-discharge relation>`s aux conditions limites en amont et en aval dans ce tutoriel. Cependant, le fichier ne peut être utilisé ici à moins que le type de limite en amont ne soit modifié à `5 5 5` (`prescribed H and Q`) dans le fichier `boundaries.cli` (lire plus dans le fichier {ref}`pre-processing tutorial <bk-liquid-bc>`).
```
#
# Downstream Rating Curve
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
#
# Upstream Rating Curve
#
Q(1)  Z(1)
m3/s  m
35    371.33
50    371.45
101   371.86
1130  375.73
2560  379.08
```
````

Pour utiliser le fichier étape-décharge, ** définir les mots-clés STAGE-DISCHARGE ... dans le fichier direction**:

```
/ steering.cas
STAGE-DISCHARGE CURVES : 0;1
STAGE-DISCHARGE CURVES FILE : ratingcurve.txt
```

---

**Supprimer les mots clés de la définition de la frontière ouverte

Pour éviter les définitions ambiguës des conditions de limites ouvertes, **désactiver** (c.-à-d. supprimer ou commenter les lignes avec un `/`) les mots clés **PRESCRIBED ...** dans le fichier de direction:

```fortran
/ PRESCRIBED FLOWRATES  : 35.;0.
/ PRESCRIBED ELEVATIONS : 374.80565;371.33
```

### Paramètres numériques

Les schémas prédicteurs-correcteurs (**CHEME POUR ...** mots clés définis avec `3`, `4`, `5`, ou `15` s'appuient sur un paramètre définissant le nombre d'itérations à chaque étape de la convergence (voir {ref}`steady2d tutorial <telemac2d-steady>`). Pour les simulations quasi stationnaires, les développeurs de Telemac recommandent de définir ce paramètre à `2` ou un peu plus grand (section 7.2.1 dans le [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf)). Par conséquent, **ajouter la ligne suivante au dossier de direction**:

```fortran
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2
```

(tm-control-sections)=
### Sections de contrôle

Une façon cohérente de vérifier les flux aux frontières ouvertes ou à d'autres lignes particulières (p. ex. entrées d'affluents ou détournements) consiste à utiliser le mot clé ** SECTIONS DE CONTROL**. Une section de contrôle est définie par une séquence de numéros de nœuds voisins. Par exemple, pour vérifier les flux au-dessus des limites ouvertes dans ce tutoriel, vérifiez les numéros de nœud dans le fichier *boundarys.cli* (par exemple 144 à 32 pour l'amont et 34 à 5 pour la limite en aval). Ensuite, **créer un nouveau fichier texte** (par exemple **control-sections.txt**) et:

* ** Ajouter une ligne de commentaires** avec quelques brèves informations (par exemple, `# control sections input file`). Notez que cette ligne est **obligatoire**.
* Dans la **deuxième ligne** ajouter une liste **séparée de 2 entiers** où
  * le premier entier définit le nombre de sections transversales, et
  * le second entier définit si les nombres de nœuds (c.-à-d. les ID de *boundaries.cli* ou *qgismesh.slf*) ou les coordonnées sont définis. Un nombre négatif permet le mode ID du noeud, et un nombre positif permet le mode coordonnées.
* **Définir autant de sections transversales que le premier entier.** Chaque définition transversale comprend deux lignes:
  * La première ligne est un *string* (texte) sans espaces qui désigne la section transversale (par exemple, `inflow_cs`).
  * La deuxième ligne se compose de deux nombres définissant les points de départ et de fin des sections transversales. Si le deuxième entier de la ligne de fichier est négatif, fournir deux entiers séparés de l'espace. Si le deuxième entier est positif, fournir deux paires de coordonnées séparées de l'espace (mettre un espace entre les coordonnées).

Par exemple, le fichier *control-sections.txt* suivant peut être utilisé avec la simulation régulière dans ce tutoriel ([télécharger control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/control-sections.txt)).

```
# control sections steady2d
2 -1
Inflow_boundary
144 32
Outflow_boundary
34 5
```

````{dropdown} Expand to view an example for coordinate-based control sections
Le fichier de section de contrôle suivant utilise des coordonnées ponctuelles plutôt que des numéros d'identification de noeud pour définir trois sections. En savoir plus sur {cite:t}`baxter2013` (c.-à-d., section 4.1.2 dans le tutoriel Baxter](http://www.opentelemac.org/index.php/component/jdownloads/summary/4-training-and-tutorials/185-telemac-2d-tutorial?Itemid=55)).
```
# control section file using coordinates
3 0
affluent_creek
19572355.895577 626823.06664 1952347.2733 626923.9554
main_river_upstream
1946449.824 635349.6070 194.919 635209.807
main_river_downstream
1967737.56993 620784.415608 1967998.16429 620638.17849
```
````

La deuxième ligne de ce fichier indique à TELEMAC d'utiliser les sections de contrôle `2`, qui sont définies par des ID de nœud (`-1`). Pour utiliser les sections de commande pour la simulation, ajouter ce qui suit au dossier de direction :

```
/ steady2d.cas
/ ...
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
```

Ainsi, le ré-exécution de la simulation écrira les flux à travers les deux sections de contrôle définir un fichier appelé *r-control-flows.txt*. Le [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) fournit des explications à la section 5.2.2.

## Exécuter Telemac2d Unsteady

Allez dans le dossier de configuration de l'installation locale TELEMAC (par exemple, `~/telemac/v9.0.0/configs/`) et chargez l'environnement (par exemple, `pysource.openmpi.sh` - utilisez la même chose que pour compiler TELEMAC).

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

Avec l'environnement TELEMAC chargé, changez vers le répertoire où vit la simulation instable (par exemple `/home/telemac/v9.0.0/mysimulations/unsteady2d-tutorial/`) et lancez le fichier `*.cas` en appelant le script **telemac2d.py**.

```
cd ~/telemac/v9.0.0/mysimulations/unsteady2d-tutorial/
telemac2d.py unsteady2d.cas
```

````{admonition} Speed up
Avec {ref}`parallelism <tm-system-wide-opts>` activé (par exemple, dans le {ref}`Mint Hyfo Virtual Machine <hyfo-vm>`), accélérer le calcul en utilisant plusieurs cœurs à travers le drapeau `--ncsize=N`. Par exemple, la ligne suivante exécute la simulation instable sur les cœurs `N=2`:

```
telemac2d.py unsteady2d.cas --ncsize=2
```
````
Un calcul réussi devrait se terminer par les lignes (ou similaires) suivantes dans *Terminal*:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                            10  MINUTES
                            32  SECONDS
... merging separated result files

... handling result files
       moving: r2dunsteady.slf
       moving: r-control-sections.txt
... deleting working dir

My work is done
```

Telemac2d écrira les fichiers *r2dunsteady.slf* et *r-control-sections.txt*. Les deux fichiers de résultats sont également disponibles dans le dépôt TELEMAC de ce livre électronique pour permettre d'accomplir le tutoriel post-traitement:

* [get r2dunsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dunsteady.slf), et
* [Get r-control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r-control-sections.txt).


## Traitement après

### Flux de frontières ouvertes

La simulation instable a l'intention de modéliser les débits variables dans le temps (flux) sur les limites en amont et en aval des liquides. La définition ci-dessus {ref}`control sections <tm-control-sections>` permet d'avoir une idée de l'adaptation correcte du débit à la limite d'entrée en amont (* prescrit Q* par *inflows.liq*) et à la limite de sortie en aval (* prescrit H* par *ratingcurve.txt*). {numref}`Figure %s <res-unsteady-hydrograph>` montre les débits modélisés où le *Inflow boundary* montre un accord parfait avec *inflows.liq* et le *Outflow boundary* reflète l'aplatissement de la courbe de décharge dans la rivière de gravier-cobble modèle.

```{figure} ../../img/telemac/res-unsteady-hydrograph.png
:alt: result unsteady flow discharge telemac2d hydrodynamic inflow outflow control sections
:name: res-unsteady-hydrograph

Les flux simulés sur les sections de contrôle *Inflow boundary* en amont et *Outflow boundary* en aval.
```

The peak inflow corresponds to the specified 1130 m$^3$/s while the outflow peak discharge is only 889 m$^3$/s and the peak takes about 1070 seconds (inflow at $t$=19000 and outflow at $t\approx$ 20070) to travel through the section.


````{admonition} Resolve volume balance issues in unsteady simulations
:class: warning, dropdown
Le volume total d'entrées et d'sorties dans le tableau ci-dessous est de 3479930,958 m$^3$ et 3430100,437 m$^3$, respectivement. Il y a donc une erreur de volume totale de 1,4$\%$. Pour surmonter ces problèmes, le manuel [Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) recommande d'utiliser une valeur minimale pour la profondeur de l'eau pour définir quand une cellule est humide ou sèche. Dans le même temps, les développeurs ne recommandent pas d'utiliser une profondeur d'eau minimale pour la plupart des simulations et insistent sur l'utilisation de cette option uniquement pour des simulations non stables (quasi-stables). Définir une profondeur d'eau minimale nécessite de définir le mot-clé **TREATMENT DES FLATS TIDAUX** à `2` (lire davantage dans le {ref}`steady2d tutorial <tm2d-tidal>`), qui n'est ni compatible avec les routines de parallélisation, ni avec les paramètres utilisés ici `SCHEME FOR ADVECTION ... : 14`. Ainsi, de meilleurs résultats, mais de longs calculs quasi stationnaires non parallèles, pourraient être obtenus avec les mots clés suivants dans le fichier de direction:

```fortran
OPTION FOR THE TREATMENT OF TIDAL FLATS : 2 / use segment-wise flux control
MINIMUM VALUE OF DEPTH : 0.1 / in meters
```
````

(tm-unsteady-qgis)=
### Visualisation avec QGIS

Les résultats de la simulation instable peuvent être visualisés et des instantanés exportés vers les formats raster (par exemple, {term}`GeoTIFF`) ou shapefile dans QGIS, comme expliqué dans le {ref}`steady2d post-processing <tm2d-post-export>`. Plus précisément, les dernières versions de QGIS permettent de charger le fichier de maillage des résultats Selafin (ici : *r2dunsteady.slf*) en tant que couche de maillage QGIS. Par conséquent, **lancer QGIS**, allez dans le menu **Layer** et cliquez sur **Ajouter un calque** > **Ajouter un calque...**. Dans la fenêtre popup (*Data Source Manager / Mesh*), **sélectionnez r2dunsteady.slf**, cliquez sur **Add**, et **Fermer**. {numref}`Figure %s <qgis-r2dunsteady-imported>` montre la couche de maille de r2dunsteady importée dans QGIS avec un mélange *Softlight* (réglé dans le *Symbologie*) sur l'imagerie satellite google.

```{figure} ../../img/telemac/qgis-r2dunsteady-imported.png
:alt: qgis telemac2d unsteady quasi steady simulation results slf
:name: qgis-r2dunsteady-imported

La simulation instable (quasi-stable) résultats fichier r2dunsteady.slf importé comme couche de maille dans QGIS et super-positionné sur google satellite imagerie {cite:p}`googlesat`.
```

```{admonition} r2dunsteady.slf (results file) not correctly showing in QGIS
:class: error, dropdown

Le fichier de résultats `r2dunsteady.slf` n'apparaît-il pas dans QGIS? Assurez-vous de l'importer avec sa géoréférence correcte: **EPSG:32633** (ETRS 89 / zone UTM 33N).
```


Les paramètres de sortie de simulation (par exemple, `U`, `V`, ou `Q`) à un moment donné peuvent être contrôlés dans les propriétés de la couche `r2dunsteady` (double-cliquez dessus dans le panneau *Layers*).

Pour **créer une vidéo des résultats de simulation**, utilisez le **Time Controller** (voir activation à {numref}`Fig. %s <qgis-time-controller-tm-recall>`). La fréquence des images peut être réglée en cliquant sur la roue du régulateur de temps, et les séquences d'images jouées en cliquant sur le bouton *Play*. De plus, {numref}`Fig. %s <qgis-time-controller-tm>` utilise une superposition de couleurs de pixel de profondeur d'eau (point de conversion) et de vecteurs de vitesse d'écoulement, définis dans le panneau *Layer Styling*. Le Nord et les flèches de décharge, et le titre sont *Décorateurs*, qui se trouvent dans **View** > **Décorateurs**.

````{admonition} Expand to see the Time Controller
```{figure} ../../img/telemac/qgis-time-controller.jpg
:alt: time controller qgis telemac
:name: qgis-time-controller-tm-recall

Le contrôleur de temps activé dans QGIS permet de se déplacer le long de l'axe temporel des quantités modélisées (carte de fond : {cite:t}`googlesat` imagerie satellite). Les boutons rouge surlignés activent le régulateur de temps, jouent la séquence d'images de quantités sélectionnées, fournissent un réglage pour jouer une fréquence d'images par seconde et permettent d'enregistrer des images de tous les temps (voir les instructions ci-dessous).
```
````

La série d'images exportées peut être convertie en vidéo avec un logiciel d'édition vidéo, comme les outils faciles et gratuits [OpenShot](https://www.openshot.org/) (bon pour Windows) ou [kdenlive](https://kdenlive.org/) (bon pour Linux). La boîte ci-dessous présente une vidéo exemplaire créée avec [kdenlive](https://kdenlive.org/).

```{admonition} Expand to view the results as video
:class: tip, dropdown
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/UJovUYb_Bo0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@ Hydro-Morphodynamics channel on YouTube</a>.</p>
```
