---
description: Introduction à l'ouverture de TELEMAC-MASCARET pour la simulation hydromorphodynamique des rivières 2D et 3D, avec un guide de tous les tutoriels couvrant le prétraitement, l'écoulement régulier, l'écoulement instable et le transport des sédiments GAIA.
---

(chpt-telemac)=
# TELEMAC

Les méthodes de simulation numérique décrites sur ces pages utilisent le logiciel libre *open TELEMAC-MASCARET* (appelé ci-après TELEMAC), qui a été lancé comme code commercial par le groupe R & D de l'Électricité de France (EDF). Depuis 2010, le consortium TELEMAC-MASCARET a repris le développement (la R & D EDF est toujours très impliquée) et fournit librement le logiciel et son code source sous une [GPLv3 license](http://www.gnu.org/licenses/gpl-3.0.html). Visitez leur [site Web](http://www.opentelemac.org/) pour en savoir plus sur TELEMAC.

Travailler sur [Debian Linux](https://www.debian.org/) ou l'un de ses dérivés (voir le chapitre {ref}`Virtual Machines (VMs) and Linux <chpt-vm-linux>`) facilite le traitement de TELEMAC, car la plupart de ses algorithmes de base ont été développés à l'origine sur les plateformes Linux. En utilisant Linux, suivez le chapitre {ref}`TELEMAC installation <telemac-install>` (comptez environ 2 heures pour l'installation).

(tm-tutorial-guide)=
## Introduction générale et guide pédagogique

L'analyse de l'hydroenvironnement avec TELEMAC implique le prétraitement pour l'abstraction du paysage fluvial, la mise en place de fichiers de contrôle, l'exploitation d'un solveur TELEMAC et le post-traitement. La première fois, l'utilisateur est confronté à un nombre écrasant d'options logicielles pour le pré- et post-traitement. De plus, TELEMAC propose une large gamme de modules pour la modélisation bidimensionnelle (2d) et tridimensionnelle (3d) des processus hydromorphodynamiques de divers plans d'eau, des rivières de montagne aux deltas côtiers sous l'influence des marées. De plus, plusieurs phénomènes de transport des sédiments peuvent être modélisés et associés à des conditions d'écoulement stables ou instables. Par conséquent, la gamme d'applications de TELEMAC est très large et ce livre électronique fournit des tutoriels pour une bonne compréhension des éléments fondamentaux de la modélisation des écosystèmes fluviaux. À cette fin, ce livre électronique propose les tutoriels suivants:

* Générer un maillage géométrique Selafin `*.slf*` avec les conditions limites avec QGIS, le plugin BASEmesh et BlueKenue dans le {ref}`pre-processing tutorial <slf-prepro-tm>`. **Recommandé comme premier tutoriel d'introduction pour les débutants.**
* Mettre en place une simulation purement hydrodynamique et stable Telemac2d dans la géométrie {ref}`steady 2d tutorial <telemac2d-steady>` (Selafin `*.slf*`). **Recommandé comme deuxième tutoriel pour les débutants.**
* Appliquer des conditions d'écoulement quasi stables (près de census instables) (p. ex. importantes pour modéliser un hydrographe d'inondation) dans le {ref}`unsteady Telemac2d tutorial <chpt-unsteady>`. Ce tutoriel s'appuie sur le tutoriel régulier Telemac2d.
* Mettre en place un modèle 3d purement hydrodynamique dans le {ref}`Telemac3d tutorial <chpt-telemac3d-slf>`.
* Couple hydrodynamique (c.-à-d. Telemac2d ou Telemac3d) avec morphodynamique (c.-à-d. {term}`Sediment transport`) dans le {ref}`Gaia tutorial <tm-gaia>`.


The tutorials build on the user manuals provided by the TELEMAC developers at [http://wiki.opentelemac.org](http://wiki.opentelemac.org/doku.php).


### Prétraitement

Le traitement préalable consiste à extraire le paysage de la rivière en un maillage informatique (grille) avec des conditions limites. De nombreux outils logiciels peuvent être utilisés à cette fin, notamment:

* {ref}`qgis-install` et le plugin BASEmesh, qui sont illustrés dans le {ref}`QGIS pre-processing tutorial <slf-prepro-tm>` (**le choix préféré de l'auteur**).
* Le logiciel du Conseil national de recherches du Canada {ref}`Blue Kenue <bluekenue>` GUI (principalement pour *Windows*).
* {ref}`SALOME <salome-install>` pour générer des maillages informatiques au format des fichiers MED.

### Configuration et exécution du modèle

La pièce maîtresse de tout modèle TELEMAC est le fichier de contrôle (direction ou CAS), qui peut être configuré avec {ref}`Fudaa PrePro <fudaa>`. La configuration du modèle est expliquée dans le {ref}`tutorial guide <tm-tutorial-guide>` ci-dessus pour TELEMAC.

### Traitement après

*Artelia Eau et Environnement* a créé le plugin [PostTelemac](https://plugins.qgis.org/plugins/PostTelemac/) pour {ref}`qgis-install`, qui est un outil puissant et pratique pour visualiser et post-traitement des résultats de simulation TELEMAC. Le {ref}`Telemac2d (steady) Post-processing <tm-steady2d-postpro>` illustre l'utilisation du plugin QGIS PostTelemac (lisez plus dans le {ref}`TELEMAC pre-processing tutorial <tm-qgis-plugins>`) pour créer des cartes {ref}`raster <raster>` et d'autres dérivés de données utiles à partir de la sortie TELEMAC.


(tm-files)=
## La structure des fichiers TELEMAC

Pour toute simulation TELEMAC, les fichiers d'entrée suivants sont **obligatoire**:

* Dossier de pilotage
  + Format du fichier : `*.cas`
  + Préparer avec {ref}`Fudaa PrePro <fudaa>` ou utiliser un éditeur de texte (par exemple, {ref}`npp`).
* Fichier de géométrie
  + Formats de fichiers : `*.slf` ([selafin](https://gdal.org/drivers/vector/selafin.html) ou `*.med` (bibliothèque de fichiers MED à partir du [salome-platform](https://www.salome-platform.org))
  + Préparez `*.slf` géométries avec {ref}`QGIS <qgis-tutorial>`or {ref}`Blue Kenue <bluekenue>` (en savoir plus sur {ref}`TELEMAC pre-processing tutorial <bk-create-slf>`).
  + Préparez `*.med` géométries avec {ref}`SALOME <salome-install>`.
* Conditions limites
  + File format: `*.cli` (with `*.slf`) or `*.bnd`/`*.bcd` (with `*.med`)
  + Préparez des fichiers `*.cli` avec {ref}`Fudaa PrePro <fudaa>` ou {ref}`Blue Kenue <bluekenue>` (lisez plus dans le {ref}`TELEMAC pre-processing tutorial <bk-bc>`).
  + Prepare `*.bnd`/`*.bcd` files either with {ref}`SALOME <salome-install>` or with a text editor.

Il y a beaucoup d'autres fichiers qui ne sont pas obligatoires par calcul pour chaque simulation TELEMAC, mais qui sont essentiels pour des scénarios particuliers (p. ex. des débits instables) et des modules (p. ex. le transport des sédiments avec Gaia). Ces fichiers **facultatifs** comprennent:

* Fichier de débit instable (p. ex. pour l'élévation de la surface de l'eau ou les débits)
  + Nécessite un fichier relation étape-décharge
  + Format du fichier : `*.qsl`
* Fichier de données de friction
  + Format de fichier : `*.tbl` ou `*.txt` (`ASCII`)
* Redémarrage / référence (pour validation du modèle)
  + Format de fichier : `.slf` ou `.med`
  + Plus d'information dans le [Manuel de Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (section 4.1.3) (voir aussi {cite:t}`hervouet_user_2014`).
* Fichier des sections pour définir les sections de contrôle (p. ex., vérifier les débits, la vitesse ou l'élévation de la surface de l'eau)
* Fichier de données sur les sources (p. ex. eau ou sédiments)
* Fichier de relation étape-décharge
  + Format de fichier : `*.tbl` ou `*.txt` (`ASCII`)
* Fichiers zones pour décrire le frottement réginal ou d'autres propriétés zonales

Lorsque des structures hydrauliques sont intégrées dans un modèle, certains des fichiers suivants sont requis (selon le type de structure):

* Fichier de données des ponceaux
* Fichier de données Weirs

De plus, un fichier *FORTRAN* (`.f`) peut être créé pour spécifier des conditions de limites particulières, des algorithmes personnalisés ou l'utilisation d'une seule ou d'une double précision.

```{admonition} Single and double precision
Dans la modélisation hydro-morphodynamique, une seule précision (c.-à-d. 32 bits *floats*) plutôt que la double précision (c.-à-d. 64 bits *floats*) est suffisante et beaucoup plus rapide.
```

D'autres fichiers d'entrée peuvent être définis pour simuler les déversements d'hydrocarbures, le transport des polluants, le vent et les effets des marées.


## Descriptions détaillées des fichiers

### Le dossier de direction (CAS)

Le fichier de pilotage est le fichier de simulation principal avec des informations sur les fichiers obligatoires (p. ex., la géométrie [*selafin*](https://gdal.org/drivers/vector/selafin.html) ou la limite), les fichiers optionnels et les paramètres de simulation. Le fichier de direction peut être créé ou édité avec un éditeur de texte de base ou un logiciel avancé tel que {ref}`Fudaa PrePro <fudaa>` ou {ref}`Blue Kenue <bluekenue>`.


### Fichiers de géométrie (SLF ou MED)

Le fichier géométrique au format [`*.slf` (*selafin* ou *SERAFIN*)](https://gdal.org/drivers/vector/selafin.html) contient des données binaires sur le maillage avec ses nœuds. Le format de nom du fichier de géométrie peut être modifié dans le fichier de direction avec:

```
/steering.cas
GEOMETRY FILE            : 't2d_channel.slf'
GEOMETRY FILE FORMAT     : SLF / or MED with SALOME preferably for 3D
```

*Les fichiers MED* sont généralement traités avec soit {ref}`SALOME <salome-install>`.


### Dossiers sur les conditions limites (CLI ou BND/BCD) et les limites liquides (QSL)

Le fichier limite au format `*.cli` contient des informations sur les nœuds entrants et sortants (coordonnées et ID). Le fichier `*.cli` peut être ouvert et modifié avec n'importe quel éditeur de texte, ce qui n'est pas recommandé pour éviter les incohérences. Utilisez de préférence {ref}`Fudaa PrePro <fudaa>` ou {ref}`Blue Kenue <bluekenue>` pour générer et/ou modifier des fichiers `*.cli` (lisez plus dans le {ref}`TELEMAC pre-processing tutorial <bk-bc>`). Voici un exemple (en-tête seulement) pour un fichier de conditions limites `*.cli`:

```
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    101     1
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    102     2
  2 2 2  0.000  0.000  0.000  0.000 2  0.000  0.000  0.000    103     3
  ...
```


`*.bnd`/`*.bcd` files can be created and edited either with {ref}`SALOME <salome-install>` or a text editor. The following block box shows how a `*.bnd` boundary file for a simple block geometry may look like.

```
4
5 4 4 4 downstream
4 5 5 4 upstream
2 0 0 2 leftwall
2 0 0 2 rightwall

```

Les utilisateurs peuvent définir un fichier de conditions limites liquides (`*.qsl`) pour définir des conditions limites dépendantes du temps (non stables) (p. ex., décharge, profondeur d'eau, vitesse d'écoulement ou traceurs). Le bloc suivant montre un exemple pour un fichier de conditions limites liquides (`*.qsl`) :
```
# bc_unsteady.qsl
# Time-dependent inflow (discharge Q(2) and outflow (depth SL(1)
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

Les conditions limites et les fichiers de limites liquides peuvent être ajoutés dans le fichier de direction avec:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
```

### Dépôt par étape (ou WSE-Q) Fichier (txt - ASCII)

Définir un fichier de décharge étape pour utiliser un stade (élévation de surface de l'eau *WSE*) - relation de décharge pour les conditions limites. Ces fichiers s'appliquent généralement à la limite en aval d'un modèle aux sections de contrôle (p. ex., un déversoir libre). Le bloc suivant montre un exemple pour un fichier de décharge étape (`*.txt`) :

```
# wse_Q.txt
#
Q(1)     Z(1)
m3/s     m
 50.     0.0
 60.     0.9
100.     1.5
```

Pour utiliser un fichier de décharge étape, définissez le mot clé suivant dans le fichier de direction :

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```

### Fichier de données de friction (tbl/txt - ASCII)

Ce fichier optionnel permet d'utiliser la définition du frottement de fond concernant la loi sur la rugosité et les coefficients de fonction associés.

Pour activer et utiliser les données de frottement, définissez les mots clés suivants dans le fichier de direction :

```
/steering.cas
FRICTION DATA            : YES
FRICTION DATA FILE       : 'friction.tbl'
```

### Le fichier Résultats/Redémarrage (SLF ou MED)


Un fichier de redémarrage provient d'une simulation TELEMAC précédente et n'a pas besoin d'exister au début. Une bonne option pour visualiser le fichier de résultats est {ref}`PostTelemac plugin <tm-qgis-plugins>` dans QGIS. Les fichiers de redémarrage au format MED sont généralement traités avec le module ParaVis à {ref}`SALOME <salome-install>`.

Le fichier résultats/redémarrage peut être défini comme suit dans le fichier de direction:
```
/steering.cas
RESULTS FILE             : 't2d_channel_output.slf'
```

Le [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (section 4.1.3) fournit des explications supplémentaires sur l'utilisation des fichiers de résultats/redémarrage (p. ex., pour accélérer les simulations).
