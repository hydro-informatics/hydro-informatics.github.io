---
description: Définir des zones de frottement et de rugosité réparties spatialement dans TELEMAC2d en utilisant QGIS et BlueKenue, en attribuant des coefficients Manning ou Strickler à différents types de matériaux de lit de rivière.
---

```{admonition} Contributors
:class: tip
Ce chapitre a été coécrit et développé par [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/) <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="25" height="25"> et [Sebastian Schwindt](https://sebastian-schwindt.org) <img src="../../img/authors/sebastian.jpg" alt="Sebastian Schwindt" width="25" height="25">.
```

(tm-friction-zones)=
# Zones de frottement

Comme pour l'attribution de valeurs de coefficient de frottement multiple à plusieurs régions modèles figurant dans le fichier de mailles {ref}`BASEMENT tutorial <bm-geometry>`, Telemac2d fournit des routines pour les définitions de zones de friction par domaine (c.-à-d. zonal) dans le fichier de mailles de géométrie (`.slf`). Plus précisément, si le domaine d'étude est caractérisé par des régions de rugosité différente, il ne suffit pas de définir la friction globale par un mot clé `FRICTION COEFFICIENT` dans le fichier de direction (`.cas`). La définition des zones de rugosité dans le fichier mesh (`.slf`) nécessite une couche supplémentaire appelée `BOTTOM FRICTION` ou `FRIC_ID` en haut de l'altitude `BOTTOM`. À cette fin, les valeurs de rugosité peuvent être définies dans un fichier de rugosité `.xyz` créé avec QGIS ({ref}`recommended <tm-friction-qgis>`) ou *Fermé Lines* `.i2s` créé avec BlueKenue ({ref}`see the meshing section <bk-import-friction>`). Alors que le QGIS est recommandé pour délimiter les zones de rugosité avec des géoréférences correctes et éventuellement précises, BlueKenue est toujours nécessaire pour interpoler la rugosité du fichier `.xyz` ou `.i2s` sur le fichier `.slf` dans la dernière étape.


```{admonition} Requirements

* Comprendre les formats de données géospatiales et savoir travailler avec QGIS (voir {ref}`QGIS tutorial <qgis-tutorial>`).
* Remplissez le {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>`.
* Installation de {ref}`BlueKenue (also works on Linux, see the installation guide) <bluekenue>`, et {ref}`Telemac <telemac-install>`.
```

```{admonition} Roughness versus friction

La dureté décrit l'inégalité ou la robustesse des surfaces solides, comme les lits de rivière. Le rougissement de la frontière augmente la résistance au débit, ce qui provoque des frictions et ralentit le mouvement de l'eau.
```


(tm-friction-qgis)=
## Dureté.XYZ avec QGIS (recommandé)

La première étape pour délimiter les zones de rugosité dans QGIS est de mettre en place le système de référence de coordonnées et de sauvegarder le projet, analogue à {ref}`QGIS pre-processing tutorial <tm-qgis-prepro>`:

* Ouvrez QGIS, et dans le menu supérieur allez à **Project** > **Propriétés**.
* Activez l'onglet **Système de coordonnées**.
* Définissez le Système de coordonnées que votre {ref}`basemap <basemap>` / {term}`Modèle numérique de terrain <DEM>` data use; pour cet exemple, entrez `UTM zone 33N` et sélectionnez *UTM zone 33N (WGS84)* (EPSG 32633), ce qui n'est pas un grand choix en raison de sa faible précision, mais il fera le travail pour ce tutoriel.
* Cliquez sur **Appliquer** et **OK**.
* Enregistrer le projet dans un nouveau dossier où tous les fichiers de ce tutoriel seront stockés.

Il sera important d'éviter les chevauchements qui conduiraient à des définitions ambiguës ou manquantes des régions. Par conséquent, activez le snapping:

* Activer la barre d'outils *Snapping* : **Voir** > **Barres d'outils** > **Snapping Toolbar**
* Dans la barre d'outils **Snapping** > **Enable Snapping** <img src="../../img/qgis/snapping-horseshoe.png">
* Activer le snapping pour
  * ** Vertex**, **Segment** et **Moyen de segments** <img src="../../img/qgis/snapping-vertex-segments.png">.
  * **Sonder sur les intersections** <img src="../../img/qgis/snapping-intersection.png">.
  * ** Self Snapping** <img src="../../img/qgis/sym-self-snapping.png">.

Ce tutoriel reprend l'exemple de {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>` pour dessiner des polygones le long des [breaklines](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) et [liquid-boundaries](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles. Les zones de friction sont déduites d'un {ref}`Google Satellite basemap <basemap>` et les attributs de friction sont estimés qualitativement, ce qui est tout à fait bien pour un tutoriel. Dans la pratique, nous recommandons fortement d'effectuer des enquêtes sur le terrain sur les distributions de granulométrie avec des systèmes GPS différentiels de haute précision (DGPS) afin de délimiter les zones de rugosité sur place soutenues par des images de drones.

```{admonition} AI can be more efficient (though less effective)
:class: tip
:name: ai-image-recognition-numerics

Ce tutoriel montre comment dessiner manuellement des polygones délimiter des zones de rugosité particulières, comme *sand*, *gravel* ou *végétation*. Cependant, l'intelligence artificielle (IA) a déjà été prouvée pour faire un excellent travail en reconnaissant automatiquement des terrains similaires pour la reconnaissance cohérente des zones de rugosité. On peut trouver des exemples à l'adresse {cite:t}`diazgomez_mapping_2022` ou [la mise en œuvre par Kenny Larrieu des outils d'OT de Segment n'importe quoi](https://github.com/klarrieu/segment-anything-eo).

Ce dont vous avez besoin, c'est :

* un drone moderne (plus trop cher)
* vérité au sol : données sur les distributions granulométriques (> gravier : nombre de galets, sable à gravier : sac et tamis, sédiments très fins : noyau gelé/plaque et tamis), étiquettes des objets (c.-à-d. marquage des points DGPS *végétation/types*, *bois*, *banques renforcées*, *routes*, etc.)
* un algorithme qui classe n'importe quelle image de drone après avoir été entraîné sur le terrain vérité; nous travaillons actuellement sur elle et le fournissons ici - restez à l'écoute.
```

### Polygones de zone de dureté définie

Les zones de rugosité peuvent être décrites par des attributs d'un fichier de forme polygone. Pour créer un nouveau fichier de formes polygones, allez dans **Layer** > **Créer un calque** > **Nouveau calque de fichiers de formes...** (voir {numref}`Fig. %s <new-qgis-lyr-rough>`).

```{figure} ../../img/telemac/qgis-add-lyr.png
:alt: create polygon shapefile roughness zones telemac
:name: new-qgis-lyr-rough

Créez un nouveau fichier de forme polygone.
```

Dans la fenêtre contextuelle, entrez les définitions suivantes :

* **Nom de fichier**: appuyez sur **...**, naviguez jusqu'au dossier du projet, et appuyez sur `friction-polygons`.
* **Encodage de fichier**: garder par défaut (les fichiers échantillons utilisent `UTF-8`).
* **Type de géométrie**: `Polygon`
* Sous les *Dimensions supplémentaires* (non obligatoires), trouvez et cliquez sur le bouton **Système de coordonnées** pour sélectionner le système de coordonnées de projet (exemple de fichiers : `EPSG:32633`).
* Ajouter un nouveau champ** :
  * **Nom**: `dMean`
  * **Type**: `Decimal (double)`
  * ** Longueur** : `10`
  * **Précision** : `5`
  * Cliquez sur **Ajouter à la liste des champs**
* Ajouter un autre champ **Nouveau champ**:
  * **Nom**: `fricID`
  * **Type**: `Integer (32 bit)`
  * ** Longueur** : `5`
  * Cliquez sur **Ajouter à la liste des champs**
* Appuyez sur **OK** pour créer le nouveau fichier de formes.

Pour suivre ce didacticiel, importez [les lignes d'arrêt (télécharger sous forme de fichier zip)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) et [les frontières liquides (télécharger sous forme de fichier zip)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles à partir du prétraitement Telemac. Dessiner des polygones en éditant des polygones de fiction. shp le long des lignes de rupture et des limites de liquide, mettre en évidence **fiction-polygons** dans le panneau *Layers* et activer l'édition en cliquant sur le stylo jaune <img src="../../img/qgis/yellow-pen.png">. Activer **Ajouter une fonction de polygone** et dessiner des polygones en appuyant sur les points des couches *breaklines* et *liquides*, selon {numref}`Fig. %s <tm-fricID-polygons>`. Pour ** finaliser chaque polygone** avec un ** clic droit sur la souris** et ** entrer** les valeurs `fricID` et `dMean` selon {numref}`Tab. %s <tab-tm-fricID-zones>` (tailles qualitatives du grain).

Pour ** corriger les erreurs de dessin** utilisez l'outil ** Vertex** <img src="../../img/qgis/sym-vertex-tool.png">. Enfin, enregistrez les nouveaux polygones (modifications de **friction-zones.shp**) en cliquant sur le symbole **Save Layer Edits** <img src="../../img/qgis/sym-save-edits.png">. **Arrêtez (Toggle) Édition** en cliquant à nouveau sur le stylo jaune <img src="../../img/qgis/yellow-pen.png"> symbole.

**D'autre part, fusionner les lignes de rupture et les limites du liquide, et utiliser l'outil *Polygonize* de la *Processing Toolbox* pour convertir les lignes fusionnées en un fichier de forme polygone.** Cependant, la polygonisation manquera quelques lignes de rupture, qui devront être modifiées. De plus, les champs `fricID` et `dMean` doivent encore être ajoutés par l'édition.

```{figure} ../../img/telemac/fricId-zones-overview.jpeg
:alt: qgis telemac roughness zone polygons
:name: tm-fricID-polygons

Exemple pour décrire les zones de rugosité (friction) avec des polygones par quatre ID de frottement (fricID) délimiteant (1) le lit de la rivière, (2) les rampes, (3), les barres de gravier et (4) les plaines inondables. Carte de fond : {cite:t}`googlesat` images satellitaires.
```

```{list-table} Four exemplary friction zones described by integer fricIDs and mean grain size diameters dMean.
:header-rows: 1
:name: tab-tm-fricID-zones

* - Nom de zone
  - Rivière
  - Rampes de blocs
  - Banques de gravier
  - Plaines inondables
* - frucides
  - 1
  - 2
  - 3
  - 4
* - dMean (m)
  - 0,080
  - 0,300
  - 0,032
  - 1.000
```

```{admonition} Download the friction-polygons shapefile
:class: tip
Téléchargez le [shapefile de friction-polygons]](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-polygons.zip) et décompresser dans le dossier du projet, par exemple `/ProjectHome/friction-polygons.[SHP]`.
```

### Générer des points de dureté

La prochaine étape sur la voie pour créer le fichier XYZ requis pour attribuer des zones de friction à un fichier de géométrie selafin est de générer des points (aléatoire) à l'intérieur des polygones créés ci-dessus. À cette fin, entrez `random points inside polygons`** dans le champ **search** de la boîte à outils ** Processing**. Dans la fenêtre popup **Random Points Inside Polygons** ({numref}`Fig. %s <tm-fric-polygons2pts>`), entrez ce qui suit :

* **Couche d'entrée**: `friction-polygons`
* **Stratégie d'échantillonnage**: `Points density`
* **Nombre ou densité de points**: `0.25` - utilisez une valeur plus petite/plus grande pour les maillages fins/courbés, mais méfiez-vous des tailles de fichiers potentiellement très importantes
* **Distance minimale entre les points**: `5.0` - utiliser une valeur plus petite/plus grande pour les mailles fines/courbées
* **Points de rando** : cliquez sur **...** et définissez un nom de shapefile de point cible, comme `friction-pts.shp` pour être stocké dans le dossier du projet.
* Cliquez sur **Run** pour créer le shapefile de points. Ce processus peut prendre un certain temps en fonction de la densité de points définie.

Le shapefile de point résultant est affiché à {numref}`Fig. %s <tm-fric-pts>`.

```{figure} ../../img/telemac/fric-zones-pts.png
:alt: random points polygons qgis telemac roughness zone
:name: tm-fric-polygons2pts

Paramètres dans l'outil Aléatoire Points Inside Polygons dans QGIS. Sélectionnez soigneusement le nombre de points ou la densité, qui peut causer de très grands fichiers de sortie. Le champ de distance minimale peut être utilisé pour réduire le nombre de points.
```

```{figure} ../../img/telemac/fric-pts.jpg
:alt: random points roughness zone
:name: tm-fric-pts

Le fichier de forme de point résultant de l'utilisation de l'outil Aléatoire Points Inside Polygons dans QGIS. Carte de fond : {cite:t}`googlesat` images satellitaires.
```

```{admonition} Download the friction-pts shapefile
:class: tip
Téléchargez le [shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts.zip) et déposez-le dans le dossier du projet, par exemple `/ProjectHome/friction-pts.[SHP]`.
```


### Attribuer des attributs de friction aux points

Hélas, la génération de points ne reprend pas automatiquement les attributs de polygone, qui doivent être interpolés aux points. Selon la loi de rugosité ciblée pour l'utilisation avec Telemac, soit les ID de frottement ou les coefficients de rugosité directement peuvent être ajoutés à la table des attributs du fichier de forme de point de friction. Dans ce tutoriel, un coefficient de frottement sous forme de rugosité Strickler est interpolé et calculé à l'aide d'une formule empirique. Un cas plus complexe pour le calcul des valeurs de rugosité se trouve dans l'étude de cas Donau (*Danube*) de la BAW (située à `HOMETEL/examples/telemac2d/donau/`).

Le transfert des attributs `dMean` et/ou `fricID` des polygones aux points est essentiellement une opération d'interpolation dans laquelle QGIS regarde chaque point et lui attribue les attributs `dMean` et/ou `fricID` du polygone le plus proche. À cette fin, cliquez sur le menu supérieur **Vector** > **Outils de gestion des données** > **Rejoindre les attributs par lieu** (voir {numref}`Fig. %s <fric-data-mgmt-join-attributes>`).


```{figure} ../../img/telemac/fric-data-mgmt-join-attributes.png
:alt: qgis friction points attribute table
:name: fric-data-mgmt-join-attributes


Ouvrez l'outil Join Attributs by Location dans QGIS.
```


```{figure} ../../img/telemac/fric-join-attributes-by-location.png
:alt: qgis friction join attributes by location
:name: fric-join-attributes-by-location
:width: 75%
:align: right

Ouvrir le tableau des attributs du tableau des points de friction.
```

Dans la fenêtre popup *Join Attributs by Location* ({numref}`Fig. %s <fric-join-attributes-by-location>`) faites les paramètres suivants :

* **Rejoignez les fonctionnalités dans**: `friction-pts`
* ** Caractéristiques (prédice géométrique)** : cochez la case `are within`, désélectionnez tous les autres
* **En comparant à**: `friction-polygons`
* ** Champs à ajouter** : cliquez sur le bouton **...** pour sélectionner `fricID` et/ou `dMean`
* **Rejoindre le type**: `Take attributes of the first matching feature only (one-to-one)`
* **Couche jointe** : cliquez sur le bouton **...** > **Enregistrer dans le fichier** > naviguer dans le dossier **projet** > **entrer un nom de fichier, comme `friction-pts-at`**
* Cliquez sur **Run**.

Le message d'erreur *Aucun indice spatial n'existe pour la couche d'entrée, les performances seront gravement dégradées* peut être ignoré pour cette application. Néanmoins, pour vérifier toute fausse sortie, il pourrait être sage de définir également le calque **Caractéristiques non joignables du premier calque**.

En conséquence, le **friction-pts-at** est disponible dans le panel **Layers** (voir {numref}`Fig. %s <fric-pts-open-at>`).

Pour convertir les tailles moyennes de grains (`dMean`) en valeurs de frottement, ouvrez la table *Attribute* par ** clic droit** sur la couche **friction-pts-at** dans le panneau **Layers** > **Open Attribute Table**.

```{figure} ../../img/telemac/fric-pts-open-at.jpg
:alt: qgis friction points attribute table
:name: fric-pts-open-at


Ouvrez la table Attribut du fichier de forme de point de friction avec la table d'attribut. Carte de fond : {cite:t}`googlesat` images satellitaires.
```


Modifier le tableau d'attribution **** ({numref}`Fig. %s <fric-pts-at-edit>`):

1. permettre l'édition,
1. supprimer les colonnes inutiles, comme le champ `id`, et potentiellement aussi le champ `fricID` (cette vitrine n'utilisera que la colonne `dMean`),
1. ouvrir la calculatrice **Field**, que nous utiliserons dans la prochaine étape pour calculer les valeurs de rugosité Strickler.


```{figure} ../../img/telemac/fric-pts-at-edit.png
:alt: friction points edit attribute table
:name: fric-pts-at-edit

La table d'attributs de la couche de friction-pts-at avec l'édition en surbrillance (rectangles rouges), supprimer les colonnes et les boutons de calculateur de champ (de gauche à droite).
```

````{admonition} Optional: derive x and y coordinates with the Field Calculator
:class: dropdown

Dans la méthode **Field Calculator**, ajouter les coordonnées $x$ et $y$ à la table *Attribut* :

* cocher la case **Créer un nouveau champ**
* **Nom du champ de sortie**: `x_coord`
* **Type de champ de sortie**: `Decimal number (real)`
* **Longueur du champ de sortie**: `10` et **Précision**: `10`
* Entrez une formule en sélectionnant la valeur x à partir de la géométrie dans la boîte de défilement ou en entrant directement dans le champ **Expression**:

```
 x( @geometry ) 
```

**Actuellement, ajouter le `y_coord` avec**:

```
 y( @geometry ) 
```

**Enregistrer** les modifications dans la table *Attribut* en cliquant sur le symbole du disque.

````

According to {cite:t}`meyer-peter_formulas_1948`, the {cite:t}`strickler_beitrage_1923` roughness (friction) coefficient can be approximated with $k_{st}$ $\approx$ 26/$D_{90}^{1/6}$ based on the grain size $D_{90}$, where 90% of the surface sediment grains are smaller. In addition, we will assume that $D_{90} \approx 2.25 \cdot D_{mean}$ {cite:p}`rickenmann_evaluation_2011`. Thus, $k_{st} \approx 26 \cdot (2.25 \cdot D_{mean})^{-1/6}$. To run this calculation, go to the **Field Calculator** and (see {numref}`Fig. %s <fric-pts-open-at>`):

* cocher la case **Créer un nouveau champ**
* **Nom du champ de sortie**: `k_st`
* **Type de champ de sortie**: `Decimal number (real)`
* **Longueur du champ de sortie**: `3` et **Précision**: `2`
* Entrez une formule en sélectionnant `dMean` à partir de `Fields and Values` dans la boîte à défilement ou en entrant directement l'équation dans le champ **Expression**:

```
26 / ( ( 2.25 * "dMean" ) ^ ( 1 / 6 ) )
```

```{figure} ../../img/telemac/fric-field-calc-strickler.png
:alt: calculator strickler roughness qgis field attribute table
:name: fric-field-calc-strickler

Estimer le coefficient Strickler en fonction de la taille moyenne du grain (dMean) avec la calculatrice de champ dans QGIS.
```



```{figure} ../../img/telemac/fric-at-final.png
:alt: x_coord y_coord coordinates strickler roughness qgis attribute table
:name: fric-at-final
:width: 100%
:align: left

Tableau d'attribut final de la couche de frottement-pts-at avec les coordonnées optionnelles x et y, et les coefficients de rugosité Strickler estimés.
```

Enfin, **supprimer tous les champs inutiles restants** de la table *Attribute* et **supprimer** les modifications en cliquant sur le symbole du disque, et basculer (c.-à-d. désactiver) l'édition.

```{admonition} Download the friction-pts-at shapefile
:class: tip
Téléchargez le [shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts-at.zip) et déposez-le dans le dossier du projet, par exemple `/ProjectHome/friction-pts-at.[SHP]`.
```

### Points d'exportation vers XYZ

Commencez par ouvrir le dialogue d'exportation avec un clic droit sur la couche friction-pts-at > Exporter > Enregistrer les fonctionnalités sous... ({numref}`Fig. %s <fric-pts-export-as>`).

```{figure} ../../img/telemac/fric-pts-export-as.png
:alt: export friction points xyz qgis attribute table
:name: fric-pts-export-as
:width: 100%

Ouvrez le dialogue d'exportation avec un clic droit sur la couche friction-pts-at > Exporter > Enregistrer les fonctionnalités sous...
```

Dans la fenêtre déroulante **Enregistrer le calque vectoriel sous...**, faire les paramètres suivants ({numref}`Fig. %s <fric-export-xyz>`):

* **Format**: `Comma Separated Value [CSV`
* **Nom du fichier**: cliquez sur **...**, naviguez jusqu'au dossier du projet et entrez `friction-pts.xyz` pour le nom du fichier ( appuyez sur **Save**).
* ** Nom de la feuille**: garder clair
* **Système de coordonnées**: assurez-vous que le Système de coordonnées de la couche friction-pts-at est défini (dans la vitrine `EPSG:32633 - WGS 84 / UTM zone 33N`)
* **Encodage**: utiliser par défaut (dans la vitrine `UTF-8`)
* **Sélectionnez** tous les champs pertinents**, c'est-à-dire, dans la vitrine, au moins `k_st`. Les champs optionnels `x_coord` et `y_coord` ne sont nécessaires que si la géométrie n'est pas exportée (pour quelque raison que ce soit).
* **Vérifier** les métadonnées des couches permanentes**
* **Type de géométrie**: `Automatic` (essentiellement par défaut)
* **Scrolldown** to the **Layer Options** and:
  * définir le **GEOMETRY** à `AS_XY`
  * définir le **SEPARATEUR** à `TAB`
* **Décocher** la case **Ajouter le fichier sauvegardé à la carte** en bas de la fenêtre.
* **Conservez toutes les autres valeurs par défaut** et cliquez sur **OK**.

```{figure} ../../img/telemac/fric-export-xyz.png
:alt: xyz file export attribute table friction points
:name: fric-export-xyz

Paramètres dans la fenêtre Enregistrer le calque vectorielle comme... pour exporter les points de friction vers un fichier XYZ (tab-séparé CSV).
```

QGIS will have exported the file with a `.xyz.csv` ending. **Rename the file** to **remove `.csv`** at the end. **Verify the correct formatting of the `.xyz` file** by opening it in a {ref}`text editor (e.g., Notepad++) <npp>`. For instance, if you calculated and exported the `x_coord` and `y_coord` fields, and additionally the geometry, the `.xyz` file will hold two times the coordinates. In this case, import the `.xyz` file in a spreadsheet editor (i.e., {ref}`office application <lo>`), delete the `x_coord` and `y_coord` columns, and re-export the file as a tab-separated CSV file. Read more about `.xyz` file conversion in the {ref}`QGIS tutorial <make-xyz>`.

````{admonition} Expand to see the correct header of the showcase friction-pts.xyz file
:class: dropdown

```
X Y k_st  
315976.648906296  5345616.71281044  40.30
315992.808134594  5345521.13037269  40.30
315983.283370604  5345655.68430873  40.30
315915.433790676  5345754.82689794  40.30
[...]
```
````

```{admonition} Download the showcase friction-pts.xyz file
:class: tip
Download [`friction-pts.xyz`](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts.xyz) and save it into the project folder, for instance, `/ProjectHome/friction-pts.xyz`.
```

## Alternative : Dessiner des zones de friction à BlueKenue

Cette procédure est une alternative imprécise à la création `roughness.xyz` décrite ci-dessus en raison des faibles capacités de référence géospatiale de BlueKenue, ce qui explique pourquoi la {ref}`instruction box <bk-closed-fric-lines>` ci-dessous n'est fournie que pour être complète.

````{admonition} Unfold to read this non-recommended alternative
:class: note, dropdown
:name: bk-closed-fric-lines

Commencez par créer de nouvelles lignes fermées ({numref}`Fig. %s <bk-new-closed-lines>`), semblables aux polygones qui délimitent les zones de rugosité.

```{figure} ../../img/telemac/bk-new-closed-lines.png
:alt: bluekenue create closed line
:name: bk-new-closed-lines
:width: 50%
:align: left

Paramètres dans la fenêtre Enregistrer le calque vectorielle comme... pour exporter les points de friction vers un fichier XYZ (tab-séparé CSV).
```

```{figure} ../../img/telemac/bk-finalize-friction-cl.png
:alt: bluekenue roughness friction closed line
:name: bk-finalize-friction-cl
:width: 100%
:align: right

Attribuer une valeur de frottement (roughness) (ici : une rugosité de 50 pierriers) à la zone délimitée par la ligne fermée.
```

Après avoir dessiné une ligne *Fermée* est terminée, appuyez sur la touche `Esc` et la fenêtre affichée dans {numref}`Fig. %s <bk-finalize-friction-cl>` apparaîtra, où une valeur de rugosité peut être attribuée. La figure exemplaire attribue une rugosité Strickler de `50` dans le champ **Value** à une ligne fermée* nommée `A-D_substrate`. Continuer à attribuer des noms à toutes les zones de rugosité pertinentes.

Enfin, **enregistrer** les objets *Fermé ligne* comme `.i2s` / `.i3s` fichiers.
````


(bk-interpolate-fric-zones)=
# Mesh de frction zonale (Kenue bleue)

Cette section passe par l'interpolation des valeurs de frottement sur un fichier de géométrie selafin (`.slf`) existant. La vitrine s'appuie sur le fichier `.slf` créé dans le {ref}`Telemac pre-processing tutorial <slf-prepro-tm>` ([télécharger qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf)). Commencez par **ouvrir BlueKenue** et ouvrez le fichier selafin `.slf` : cliquez sur **Fichier** > **Ouvrir...** > naviguer vers le répertoire où le `.slf` est stocké, assurez-vous de sélectionner **Télémac Selafin File (\*.slf)**, mettre en valeur `qgismesh.slf`, et appuyez sur **Ouvrir**. Tirez la couche `BOTTOM (BOTTOM)` des éléments de données de l'espace de travail vers **Views** > **2D View (1)** pour vérifier et visualiser l'importation correcte du maillage ({numref}`Fig. %s <fric-bk-slf>`).


```{figure} ../../img/telemac/bk-slf.png
:alt: BlueKenue 2dmesh interpolated elevation
:name: fric-bk-slf

La vitrine qgismesh.slf selafin fichier ouvert dans BlueKenue.
```

(bk-import-friction)=
## Importer les zones de friction

Comme alternative à la création de valeurs de friction zonales stockées dans un fichier `.xyz` généré avec QGIS, les zones peuvent également être dessinées directement dans BlueKenue via une série de *lignes fermées*. Cependant, en raison de la capacité très limitée de BlueKenue à traiter les références géospatiales et les systèmes de coordonnées (SCR), **l'option préférable** pour créer l'entrée de zone de friction **est** l'application ci-dessus de **QGIS**.

`````{tab-set}
````{tab-item} Open the .xyz file in BlueKenue
Pour ouvrir le fichier `.xyz` dans BlueKenue :

* cliquez sur **Fichier** > **Ouvrir...**
* naviguer dans le dossier du projet où le `.xyz` est stocké
* Assurez-vous de sélectionner **Tous les fichiers (\*.\*)** à côté du champ **Nom du fichier:**
* highlight `qgismesh.slf`, and press **Open**.

```{figure} ../../img/telemac/bk-fric-xyz-properties.png
:alt: bluekenue roughness friction visualize coefficients
:name: bk-fric-xyz-properties
:width: 100%
:align: left

Attribuer une valeur de frottement (roughness) (ici : une rugosité de 50 pierriers) à la zone délimitée par la ligne fermée.
```

**Ignorer** le message **avertissement** (cliquez sur **OK**). Pour vérifier et visualiser les valeurs de frottement importées **droit-clic** sur la couche **friction-pts (X)** > **Propriétés** > aller à l'onglet **Données** > **sélectionner Z(double)**, appuyez sur **Appliquer**. Ensuite, allez à l'onglet **ColourScale**, appuyez sur **Reset**, **Apply** et **OK**.

Vérifier la représentation correcte des valeurs de frottement en tirant la couche `friction-pts (Z)` des éléments de données de l'espace de travail vers **Views** > **2D View (1)** ({numref}`Fig. %s <bk-fric-pts>`).


```{figure} ../../img/telemac/bk-fric-pts.png
:alt: friction roughness coefficients bluekenue 
:name: bk-fric-pts


Le fichier friction-pts.xyz importé (créé avec QGIS) visualisé dans BlueKenue.
```
````

````{tab-item} Closed lines from BlueKenue
Si ce n'est pas encore fait, importez les *lignes fermées* délimiter les zones de rugosité sous la forme de fichiers `.i2s` / `.i3s`.
````
`````

## Interpolate Friction sur le Mesh

Dans BlueKenue, allez à **File** > **New** > **2D Interpolator**, qui se produira dans l'espace de travail** > **Data Items**. **Drag & drop** soit le **friction-pts** `.xyz` points ou le *Fermé ligne* objets délimiter les zones de rugosité **sur le nouveau 2D Interpolator** (voir {numref}`Fig. %s <bk-fric-2d-interpolator>`).

```{figure} ../../img/telemac/bk-fric-2d-interpolator.png
:alt: bluekenue 2d interpolator roughness friction
:name: bk-fric-2d-interpolator
:width: 100%


Faites glisser et déposez les frottements (ou les lignes fermées) sur un nouvel interpolateur 2D à BlueKenue.
```



Next, add a new variable to the `qgismesh.slf` mesh by highlighting the **Selafin `qgismesh`** object (in **Work Space** > **Data Items**), and **right-clicking** on it.  Click on **Add Variable...** and enter the following in the popup window ({numref}`Fig. %s <bk-new-slf-variable-fric>` or {numref}`Fig. %s <bk-new-slf-variable-fricID>`), depending on if you are working with friction values (as showcased here with Strickler roughness), or {ref}`friction IDs (see below) <tm-fricID>`:

`````{tab-set}
````{tab-item} BOTTOM FRICTION (Strickler) value
```{figure} ../../img/telemac/bk-new-slf-variable-fric.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fric
:width: 100%
:align: right


Ajouter une nouvelle variable à l'objet Selafin pour les valeurs de frottement direct.
```
* **Mesh**: `BOTTOM`
* **Nom**: `BOTTOM FRICTION` (ceci exemple)
* **Unités**: garder à l ' écart (champ non pertinent)
* ** Valeur du nœud par défaut**: `30` (dans cet exemple) pour une valeur par défaut (Strickler) à utiliser lorsqu'aucun point de friction xyz ne se trouve à proximité d'un nœud maillé

````

````{tab-item} FRICTION ID
```{figure} ../../img/telemac/bk-new-slf-variable-fricID.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fricID
:width: 100%
:align: right


Ajouter une nouvelle variable à l'objet Selafin pour les ID de frottement.
```

* **Mesh**: `BOTTOM`
* **Nom**: `FRIC_ID` (ne peut pas être sélectionné dans la liste)
* **Unités**: garder à l ' écart (champ non pertinent)
* ** Valeur du nœud par défaut**: `0` (ID à utiliser lorsqu'aucun point xyz ne se trouve à proximité d'un noeud de maille)

````
`````

Pour interpoler les valeurs de frottement sur le maillage, mettez en évidence la nouvelle variable `BOTTOM FRICTION` (ou `FRIC_ID`) de l'objet `qgismesh` dans **Espace de travail** > **Données**. L'attribut *Anonymous* de la nouvelle variable peut être ignoré. Pour cartographier la nouvelle variable sur le maillage :

* Mettre en évidence la nouvelle variable de mesh `BOTTOM FRICTION` (ou `FRIC_ID`) (en **Données**)
* Allez à **Outils** > **Objet de carte...** (menu supérieur à {numref}`Fig. %s <bk-map-2d-interpolator>`)
* Sélectionnez le **nouveau Interpolateur 2D**, et cliquez sur **OK**, qui ouvre la fenêtre popup **Processing...**
* Une fois le traitement terminé, cliquez sur **OK**.

```{figure} ../../img/telemac/bk-map-2d-interpolator.png
:alt: map object  2dinterpolator roughness friction bluekenue
:name: bk-map-2d-interpolator
:width: 100%

Cartez la valeur de friction sur le nouvel Interpolateur 2D à BlueKenue.
```

```{figure} ../../img/telemac/bk-fric-colourscale.png
:alt: bottom friction colourscale selafin bluekenue
:name: bk-fric-colourscale
:width: 100%
:align: right

Réglez l'échelle de couleur pour BOTTOM FRICTION.
```

Vérifier l'interpolation correcte:

* Définir une échelle de couleur pertinente:
  * Dans **Espace de travail** > **Data Items** > **qgismesh**, **droit-clic** sur la nouvelle variable **FRICTION BOTTOM** > **Propriétés**.
  * Dans les propriétés, allez à l'onglet **ColourScale** et utilisez, par exemple, une échelle *Linear* avec `10` *Levels*, un *Min* de `22`, et un *Interval* de `1.8`. Le minimum et l'intervalle exemplaires sont de bons choix pour la vitrine, mais d'autres paramètres pourraient être préférables pour d'autres applications (p. ex., préférez *Min* de `0` lors de l'utilisation de Manning $n_m$).
  * Appuyez sur **Appliquer** > **OK**.
* **Drag & drop** la variable **BOTTOM FRICTION** dans **Views** > **2D View (1)** pour vérifier l'interpolation correcte des valeurs de frottement (par exemple, voir {numref}`Fig. %s <bk-fric-on-mesh>` pour la vitrine).

```{figure} ../../img/telemac/bk-fric-on-mesh.png
:alt: selfin slf mesh bottom friction bluekenue
:name: bk-fric-on-mesh

La nouvelle variable BOTTOM FRICTION correctement interpolée de la maille qgismesh.slf.
```

Vers **enregistrer** le selafin **mesh** avec interpolation des valeurs de frottement interpolées, ** clic droit** sur l'objet selafin **qgimesh** > **Propriétés** > allez à l'onglet **Meta Data**, et entrez un nouveau **Nom**, par exemple `qgismesh-friction`. Ensuite, ** mettre en lumière l'objet selafin** (par exemple, `qgismesh-friction`) et **cliquer sur le disque <img src="../../img/telemac/bk-sym-save.png"> symbole**. Si le renommage n'a pas pris effet sur le nom du fichier, confirmez le remplacement du fichier existant.


```{admonition} Download qgismesh-friction.slf (with BOTTOM FRICTION)
:class: tip
Téléchargez la mise à jour [qgismesh-friction.slf avec BOTTOM FRICTION](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf).
```


# Reliures Telemac

(zonal-fric-cas)=
## Mise en œuvre dans le fichier CAS

### Mots clés de friction

La mise à jour `qgismesh-friction.slf` mesh peut être utilisée tout comme dans la {ref}`steady 2d tutorial <telemac2d-steady>`, mais certains mots-clés doivent être modifiés, même si les valeurs `BOTTOM FRICTION` assignées dans la `.slf` mesh écrasent automatiquement le mot-clé global **FRICTION COEFFICIENT** dans le fichier de direction `.cas`. Cependant, nous devons faire reconnaître Telemac les zones `BOTTOM FRICTION` nouvellement définies comme étant le type de rugosité **Strickler**. À cette fin, changez le **LAW OF BOTTOM FRICTION** à `3` (au lieu de `4` pointant vers Manning $n_m$) et définissez la valeur par défaut **FRICTION COEFFICIENT** à `33` (inverse de $n_m$ = 0,03). La définition de **FRICTION COEFFICIENT** est pour la cohérence et n'est pas strictement nécessaire car elle sera écrasée par le `BOTTOM FRICTION` de la maillage `.slf`.

`````{tab-set}
````{tab-item} New (Strickler)
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ Friction at the bed
LAW OF BOTTOM FRICTION : 3 / 3-Strickler
FRICTION COEFFICIENT : 33  / will be overwritten by zonal friction values
```
````

````{tab-item} Old (Manning from steady 2d)
```fortran
/ steady2d.cas steering file
/ ...
/ Friction at the bed
LAW OF BOTTOM FRICTION : 4  / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
```
````
`````

Ajouter la lettre `W` aux imprimés graphiques pour écrire le coefficient de friction au fichier de résultats :

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : 'U,V,H,S,Q,W' / add W for friction coefficient
```


````{admonition} Do you have more than 10 different friction zones?
:class: tip, dropdown

Pour augmenter le nombre de zones de friction reconnues par Telemac, définissez le mot-clé **MAXIMUM DES DOMAINES DE FRICTION**, par exemple, à `20`:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
MAXIMUM NUMBER OF FRICTION DOMAINS : 20 / default is 10
```
````


### Conditions initiales de démarrage à chaud (facultatif)

**Les descriptions suivantes se réfèrent à la section 4.1.3 du [Manuel de Télémac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Pour accélérer la simulation, ce tutoriel réutilise la sortie du {ref}`steady 2d simulation <telemac2d-steady>` (bien que recréé avec une période d'impression de `2500` steps). Ce type d'initialisation de modèle s'appelle aussi *hotstart*, ici, basé sur le fichier de résultats réguliers [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf), qui doit être défini comme **DOSSIER DE COMPUTATION PRÉCÉDENT**:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady-t15k.slf / results of 35 CMS steady simulation after 15000 timesteps
```

Avec les conditions de démarrage rapide, les limites peuvent être assouplies à:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.; 0.
PRESCRIBED ELEVATIONS : 0.; 371.33
```

Pour que ces conditions limites prennent effet, le fichier des limites liquides de la simulation constante 2d doit être modifié :

* ouvrir *boundarys.cli* dans un {ref}`text editor <npp>`
* trouver la limite en amont `5 5 5` (préciser Q et H) et la remplacer par `4 5 5` (préciser Q seulement)
* sauver et fermer *boundaires.cli*
* pour plus d'informations, consultez le chapitre sur les projecteurs {ref}`boundary conditions <tm-foc-bc>`
* Sinon, [téléchargez les limites adaptées.cli here](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli).

Enfin, commentez les mots clés des conditions initiales dans le fichier de direction `.cas`, par exemple:


```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ INITIAL CONDITIONS : 'ZERO DEPTH'
/ INITIAL DEPTH : 0.005
```

## Exécuter la simulation de zone de friction

Assurez-vous que tous les fichiers requis sont placés dans un dossier de simulation (p. ex. `/HOME/modeling/friction-tutorial/`), notamment :

* le [qgismesh-friction.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf) maillage avec `BOTTOM` et `BOTTOM FRICTION` information
* les [boundaires.cli](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli)
* le fichier de résultats [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf) pour activer le hotstart
* le fichier de direction [steady2d-zonal-ks.cas](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas) avec mots-clés mis à jour.

Naviguer (`cd`) vers le répertoire d'installation de Telemac (`HOMETEL`) pour activer (`source`) l'environnement de Telemac dans Terminal (utiliser le même environnement que pour {ref}`compiling Telemac <tm-compile>`):

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
```

Ensuite, `cd` dans le dossier de simulation et lancer la simulation, éventuellement avec le drapeau `-s`, pour remonter {ref}`flux convergence <tm-convergence>`:

```
cd ~/modeling/friction-tutorial/
telemac2d.py steady2d-zonal-ks.cas -s
```

La simulation réussie aura fini avec quelque chose comme ceci:

````{admonition} Unfold to see the expected Terminal output
:class: note, dropdown

```
================================================================================
 ITERATION    10000    TIME:  6 H 56 MIN  40.0000 S   (    25000.0000 S)
--------------------------------------------------------------------------------

[...]

--------------------------------------------------------------------------------
                       BALANCE OF WATER VOLUME
     VOLUME IN THE DOMAIN :    268926.5     M3
     FLUX BOUNDARY    1:     35.00000     M3/S  ( >0 : ENTERING  <0 : EXITING )
     FLUX BOUNDARY    2:    -34.99963     M3/S  ( >0 : ENTERING  <0 : EXITING )
     RELATIVE ERROR IN VOLUME AT T =       0.2500E+05 S :    0.2327571E-14
--------------------------------------------------------------------------------
                   FINAL BALANCE OF WATER VOLUME

     RELATIVE ERROR CUMULATED ON VOLUME:    0.4112446E-14

     INITIAL VOLUME              :     268899.0     M3
     FINAL VOLUME                :     268926.5     M3
     VOLUME THAT ENTERED THE DOMAIN:     27.48362     M3  ( IF <0 EXIT )
     TOTAL VOLUME LOST             :    0.1105946E-08 M3

 END OF TIME LOOP

 EXITING MPI

                     *************************************
                     *    END OF MEMORY ORGANIZATION:    *
                     *************************************

 CORRECT END OF RUN

 ELAPSE TIME :
                              3  MINUTES
                              3  SECONDS
Note: The following floating-point exceptions are signalling: IEEE_UNDERFLOW_FLAG IEEE_DENORMAL
STOP 0

... merging separated result files

... handling result files

        moving: r2dsteady-ks-zonal.slf
      copying: steady2d-zonal-ks.cas_2030-07-28-14h55min04s.sortie
... deleting working dir



My work is done

```
````

Le résultat {ref}`flux convergence <tm-flux-convergence>` et {ref}`convergence rates <tm-calculate-convergence>` devrait ressembler à ceci :

`````{tab-set}
````{tab-item} Flux convergence
```{figure} ../../img/telemac/flux-convergence-zonal-fric.png
:alt: zonal friction telemac flux convergence pythomac
:name: tm-friction-flux-convergence

La courbe de convergence du flux franchit les deux limites de la simulation constante à démarrage rapide Telemac2d, à partir d'un temps de simulation de 15000 temps.
```
````

````{tab-item} Convergence rate
```{figure} ../../img/telemac/convergence-rate-zonal-fric.png
:alt: zonal friction convergence rate fluxes telemac boundaries
:name: tm-friction-convergence-rate

Le taux de convergence $\iota$ en fonction 15000 temps de simulation de la simulation stable 2d avec des zones de friction.
```
````
`````

Le [steady2d-zonal-ks.cas 2023-07-28-14h55min04s requis est disponible ici](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas_2023-07-28-14h55min04s) pour une utilisation avec les instructions du chapitre des projecteurs sur {ref}`convergence <tm-convergence>`.

```{admonition} Look at the results in QGIS

Charger le fichier de résultats de simulation (`r2dsteady-ks-zonal.slf`) dans QGIS pour vérifier l'exactitude du frottement de fond utilisé et examiner les légers changements de vitesse d'écoulement et de profondeur d'eau résultant des valeurs maintenant différentes de rugosité (friction).
```

(tm-fricID)=
# Travailler avec les ID de friction

Les zones de frottement peuvent également être attribuées par l'intermédiaire d'ID de frottement, qui nécessitent ensuite la mise en place d'un fichier de zones et d'un fichier de données de friction, par exemple, comme le montre l'exemple de Donau (`HOMETEL/examples/telemac2d/donau/`).

```{admonition} The Donau zonal friction ID example
:class: tip

L'étude de cas Donau de BAW vit à `HOMETEL/examples/telemac2d/donau/` et elle a été présentée à la XXème conférence des utilisateurs de Telemac-Mascaret. Les actes de la conférence sont disponibles sur le portail de la BAW [HENRY portail](https://hdl.handle.net/20.500.11970/100418) (chercher la contribution *Ingénierie inverse des conditions initiales et limites avec Telemac et différenciation algorithmique*). Cependant, cette affaire utilise une complication inutile sous la forme d'un fichier `.bfr` zone. Le système de référence géospatial de cet exemple est EPSG 31468 (GK4) (voir [ce billet dans le Telemac Forum](http://opentelemac.org/index.php/kunena/16-telemac-2d/14284-coordinate-reference-systems-and-projections-of-examples-e-g-donau#43037)).
```

Dans la vitrine de ce tutoriel, travailler avec des tables de friction a exigé d'attribuer les ID de friction définis dans {numref}`Tab. %s <tab-tm-fricID-zones>` à la variable `BOTTOM FRICTION` de la maille `.slf`. Les fichiers peuvent être téléchargés depuis nos dépôts:

* [obt friction-with-IDs.xyz](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction-with-IDs.xyz) pour l'interpolation à BlueKenue ({ref}`see above <bk-interpolate-fric-zones>`, ou directement
* [get qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) avec `BOTTOM` et `FRIC_ID` au lieu de `BOTTOM FRICTION` Coefficients de rugosité Strickler (utilise l'ID de frottement par défaut `0`).

## friction.tbl & CAS

### Créer friction.tbl

Créer un fichier de table de friction appelé `friction.tbl` (considérer ce [friction.tbl template](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl)) avec le contenu suivant, où les entrées `no` (ici commençant par la ligne 36) doivent correspondre à la `FRIC_ID` assignée au maillage (rappel {numref}`Fig. %s <bk-new-slf-variable-fricID>`):

```{aside} More information

L'annexe E du [Manuel Telemac2d](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) fournit plus d'explications sur les paramètres tabulaires (p. ex., `typeB`, `rB`, ou `nDefB`), et les lois de friction (p. ex., STRI, NIKU) sont expliquées plus en détail dans ce livre électronique dans le stable-2d {ref}`section on friction <tm2d-friction>`.
```

```{code-block} fortran
---
name: friction_tbl
linenos: True
caption: |
    Example for a friction(.tbl) ID table.
---
* ----------------------------------------------------------------------------- 
*  EXAMPLE ADAPTED FROM HOMETEL/examples/telemac2d/donau/
*
*  Implemented roughness laws: 
*    NOFR : no friction         (number of values) 
*    HAAL : Haaland   law       (1 value  : rB) 
*    CHEZ : Chezy     law       (1 value  : rB) 
*    STRI : Strickler law       (1 value  : rB) 
*    MANN : Manning   law       (1 value  : rB) 
*    NIKU : Nikuradse law       (1 value  : rB) 
*    LOGW : Log Wall  law       (1 value  : rB) 
*    COWH : Colebrook-White law (2 values : rB, nDef) 
* 
*  no             : FRIC_ID assigned to the SLF mesh
* 
*  Riverbed
*  ------------- 
*  typeB          : roughness law for riverbed
*  rB             : friction value for riverbed
*  nDefB          : Mannings n for shallow flow zones
* 
*  Later walls (only with k-epsilon model) 
*  ----------------------------------------- 
*  typeS          : roughness law for walls          (option) 
*  rS             : friction value for walls         (option) 
*  nDefS          : Mannings n for shallow waters    (option) 
* 
*  Non-submerged Vegetation (if needed) 
*  ------------------------ 
*  dp             : mean diameter                                (option) 
*  sp             : averaged distance between roughness elements (option) 
* 
* ----------------------------------------------------------------------------- 
* no        typeB  rB    NDefB  typeS  rS  NDefS   dp     sp 
* 
  0  STRI   33.0  NULL
  1  STRI   34.6  NULL
  2  STRI   27.7  NULL
  3  STRI   40.3  NULL
  4  STRI   22.7  NULL
END 
```

### Lien friction.tbl dans le fichier CAS

Pour activer les données de frottement, ajoutez les mots-clés suivants au fichier de direction `.cas` et désactivez les mots-clés FRICTION non liés au mur :


`````{tab-set}
````{tab-item} Keywords to activate
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ ACTIVATE these keywords
FRICTION DATA : YES / default is NO
FRICTION DATA FILE : 'friction.tbl'
MAXIMUM NUMBER OF FRICTION DOMAINS : 20 / consider to increase (default is 10)
```
````
````{tab-item} Keywords to deactivate
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ DEACTIVATE these keywords
/ LAW OF BOTTOM FRICTION : 3 / 3-Strickler
/ FRICTION COEFFICIENT : 80 / not use with zonal friction
```
````
`````

Enregistrer le fichier de direction `.cas`.

## Lancez Telemac avec les identifiants de friction

Pour exécuter Telemac avec les ID de friction, assurez-vous que les mots-clés indiqués ci-dessus sont activés dans le fichier de direction `.cas`. Les fichiers requis comprennent maintenant :

* [qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) (mesh avec `FRIC_ID`)
* [boundarys.cli](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/boundaries.cli) ou conditions de démarrage rapide
* [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/r2dsteady-t15k.slf) fichier de résultats pour activer le hotstart
* [steady2d-zonal-ID.cas](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/steady2d-zonal-ID.cas) fichier de pilotage mis à jour mots clés
* [friction.tbl](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl) avec les ID de friction

Avec ces fichiers, activez et exécutez Telemac comme d'habitude :

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
cd ~/modeling/frictionID-tutorial/
telemac2d.py steady2d-zonal-ID.cas
```


# Routines de friction avancées

Modifier le **FRICTION USER** Les sous-routines de Fortran ne sont pas obligatoires pour travailler avec les zones de friction, mais peuvent être utiles pour mettre en œuvre ou adapter le comportement des lois sur la rugosité. Pour activer un subroutine FRICTION USER, par exemple, pour implémenter l'équation de puissance variable de {cite:t}`ferguson_flow_2007`:

* Copiez le modèle de sous-routine FICTION USER de `HOMETEL/sources/telemac2d/friction_user.f` dans un nouveau dossier de votre répertoire de simulation, par exemple :
```
/HOME/modeling/frictionID-tutorial/user_fortran/friction_user.f
```
* Modifier et enregistrer les modifications de `friction_user.f`.
* Dites au fichier de direction (`.cas`) d'utiliser le fichier FRICTION USER Fortran modifié en ajoutant le mot clé `FORTRAN FILE : 'user_fortran'`, ce qui fait que Telemac2d recherche les fichiers Fortran dans le sous-dossier `/user_fortran/`.






