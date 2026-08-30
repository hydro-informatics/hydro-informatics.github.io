---
description: Débutant QGIS tutoriel avec des conseils vidéo pour le chargement, la visualisation et l'analyse des données géospatiales, y compris les fichiers de forme et les rasters pour l'ingénierie des ressources en eau.
---

(qgis-tutorial)=
# Tutoriel QGIS

````{admonition} Requirements
Ce tutoriel est conçu pour **beginners** et contient des vidéos contenant les descriptions de texte dans chaque section. Avant de plonger dans ce tutoriel, assurez-vous d'installer {ref}`QGIS <qgis-install>`.


```{admonition} Expand to watch the video for installing QGIS
:class: dropdown, tip
Trouvez des explications dans la section {ref}`qgis-install` dans ce livre électronique.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/_0_NOKi-RxY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

```

```{admonition} If you read: *Videos not showing up (Firefox Can’t Open This Page)*...
:class: attention, dropdown
Si les vidéos ne s'affichent pas, cela pourrait être causé par des paramètres de confidentialité stricts. Pour résoudre le problème, ouvrez les liens vidéo en cliquant sur le bouton **Ouvrir le site dans Nouvelle fenêtre** ou en modifiant les paramètres de confidentialité du navigateur (par exemple, dans [Mozilla Firefox](https://support.mozilla.org/en-US/questions/1108783)).
```
````

(qgis-project)=
## Premier projet

Une fois que vous avez installé QGIS, lancez le programme et passez par les étapes suivantes pour faire les paramètres fondamentaux:

- Ouvrir *QGIS*
- Créer un nouveau projet (**Nouveau projet vide**)
- Vérifier **Propriétés du projet**:
  * Dans le menu supérieur, allez à **Projet** > **Produits**
  * Définir le système de référence des coordonnées **Système de coordonnées** à **EPSG:4326**:
    * WGS84 (Système de référence coordonné) Bounds: -180.0000, -90.0000, 180.0000, 90.0000
    * Bounds prévus: -180.0000, -90.0000, 180.0000, 90.0000
    * Portée : Composante horizontale d'un système 3d. Utilisé par le système GPS de navigation par satellite et pour les levés géodésiques militaires de l'OTAN.
    * Dernière révision : 27 août 2007
    * Zone : Monde
  * Pour en savoir plus à http://epsg.io
    * Récupérer les coordonnées point dans n'importe quel format Système de coordonnées
    * Convertir entre différents Système de coordonnées (par exemple, convertir 48.745, 9.103 de EPSG 3857 en EPSG 4326)
- **Enregistrer** le projet en tant que **qgis-project.qgz** dans un nouveau dossier **qgis-exercice**

```{admonition} Project setup (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/7_3QqbFonLg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

```{hint}
Tous les fichiers créés dans ce tutoriel peuvent être téléchargés à partir du dépôt [QGIS tutoriel](https://github.com/Ecohydraulics/qgis-tutorial).
```

(qgis-tbx-install)=
## Panneaux, barres d'outils et greffons

Suivez les instructions illustrées ci-dessous pour activer le *QGIS* *Toolbox*.

```{figure} ../img/qgis-tbx.png
:alt: enable QGIS toolbox
:name: qgis-tbx

Ouvrez la boîte à outils QGIS depuis le menu principal.
```

De plus, la barre d'outils **Digitizing** (**View** > **Toolbars** > check **Digitizing Toolbar**) est requise pour compléter ce tutoriel.

La conversion entre les types de données géospatiales et les grilles numériques (computationnelles) peut être facilitée par des plugins. Pour installer n'importe quel plugin dans QGIS, allez dans le menu **Plugins** > **Gérer et installer des plugins...** > **All** onglet > **Rechercher...** pour un plugin pertinent et l'installer.

Dans le cadre de l'analyse fluviale, les plugins suivants sont recommandés et utilisés à plusieurs endroits sur ce site:

```{admonition} QGIS plugins for hydro-informatics
:name: qgis-plugins
* Le plugin *Crayfish* pour post-traitement de la sortie numérique du modèle.
* Le plugin *BASEmesh2* fournit des routines pour créer des maillages de calcul pour des simulations numériques avec {ref}`chpt-basement`.
* Le plugin *PostTelemac* permet la visualisation géospatiale et la conversion des résultats des modèles numériques produits avec {ref}`chpt-telemac`.
```

BASEmesh n'est qu'un seul générateur de mailles (très performant) pour QGIS et {numref}`Tab. %s <tab-mesh-plugins>` listes d'autres plugins pour générer des mailles de calcul pour les modèles numériques ainsi que des formats de fichiers cibles et des modèles

````{admonition} Mesh generators
:class: full-width

```{list-table} A list of QGIS mesh generator plugins.
:header-rows: 1
:name: tab-mesh-plugins

* - Nom et lien du plugin Mesh
  - Compatibilité du modèle
  - Format de fichier Mesh de sortie
  - Caractéristiques du mesh
* - [GMSH](http://geuz.org/gmsh) ([Wiki](https://github.com/ccorail/qgis-gmsh/wiki))
  - [Ouvrir la technologie CASCADE](https://www.opencascade.com/open-cascade-technology/) / {ref}`OpenFOAM <openfoam-install>`
  - `*.geo`, `*.stl`, `*.msh`
  - 3D éléments finis ([Netgen](http://ngsolve.org/) et [Mmg3d](https://www.mmgtools.org/)), compatibilité avec {ref}`salome-install`
* - [QGribDownloader](https://plugins.qgis.org/plugins/gribdownloader/)
  - [OpenGribs / XyGrib](https://opengribs.org/)
  - `*.GRIB`
  - Objectif: Modélisation météorologique et atmosphérique
* - [TULOW](https://plugins.qgis.org/plugins/tuflow/)
  - [TULOW](https://tuflow.com/) (propriétaire)
  - `*.2dm` (entre autres), conversion à `.slf` possible avec Crayfish
  - TUFLOW génère automatiquement des maillages (volumes finis / différences finies)
* - [MeshTools](https://github.com/jdugge/MeshTools)
  - {ref}`chpt-basement`, Hydro FT/AS (propriétaire), indirectement: {ref}`chpt-telemac`
  - `*.2dm` (conversion vers `.slf` possible avec Crayfish)
  - Plonge dans plusieurs algorithmes de maillage (entre autres : {cite:t}`shewchuk1996`)
* - DEMto3D
  - Raster vers STL (style) fichiers pour Blender
  - `*.geo`, `*.stl`, `*.msh`
  - Créer des jumeaux numériques dans Blender
```
````

(basemap)=
## Cartes de base pour QGIS (Google ou cartes de rue ouvertes)

```{note}
Une connexion Internet rapide est nécessaire pour ajouter des cartes de base en ligne.
```

Pour ajouter une carte de base (p. ex., données satellite, rues ou limites administratives), allez au **Browser**, faites un clic droit sur **XYZ Tiles**, sélectionnez **Nouvelle connexion...**, ajoutez un nom et une URL d'une carte de base en ligne. Une fois la nouvelle connexion ajoutée, elle peut être ajoutée à un projet *QGIS* par glisser-déposer comme n'importe quelle autre couche de géodonnées. La figure ci-dessous illustre la procédure d'ajout d'une nouvelle connexion et de ses tuiles XYZ comme couche au projet. Pour superposer plusieurs cartes de base (ou n'importe quel autre calque), **droit-clic sur un calque**, puis **Propriétés de calque** > **Transparence** > modifier l'opacité** (par exemple à 50 %).

```{figure} ../img/qgis-basemap.png
:alt: basemap

Ajoutez une carte de base à QGIS : (1) localisez le navigateur (2) clic droit sur XYZ-Tiles et sélectionnez Nouvelle connexion... (3) saisissez un nom et une URL (voir tableau ci-dessous) pour la nouvelle connexion, cliquez sur OK (4) glisser et déposer la nouvelle tuile (ici : Google Satellite) dans le panneau Calques.
```

```{admonition} Expand to watch the video tutorial on basemaps
:class: tip, dropdown

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/GJsiEdMzCeQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

L'URL suivante peut être utilisée pour récupérer des tuiles XYZ en ligne (plus d'URL peuvent être trouvées sur Internet).

````{admonition} Basemap providers
:class: full-width

```{list-table} Providers of XYZ basemap tiles
:header-rows: 1
:name: basemap-providers

* - Fournisseur (nom de l'éditeur)
  - URL
* - Imagerie par satellite Bing
  - https://t0.tiles.virtualearth.net/tiles/a{q}.jpeg?g=685&mkt=en-us&n=z
* - Imagerie du monde ESRI
  - https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
* - Rue ESRI
  - https://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}
* - ESRI Topo
  - https://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}
* - Google Satellite
  - https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}
* - Google Street
  - https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}
* - OpenStreetMap (OSM)
  - http://tile.openstreetmap.org/{z}/{x}/{y}.png
* - OSM Noir et blanc
  - http://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png
```
````

```{admonition} Coordinate reference systems of basemaps
:class: tip

La plupart des cartes de base sont fournies dans le système de coordonnées `EPSG:3857 -WGS84` / `Pseudo Mercator`. Pour utiliser des produits géodonnées personnalisés, assurez-vous que toutes les autres couches ont le même système de coordonnées. En savoir plus sur les systèmes de coordination et les projections dans les sections {ref}`geospatial-data` et {ref}`shapefile projection <prj-shp>`.
```

## Créer un fichier de formes

Cette section guide la création d'un point, d'une ligne et d'un polygone {ref}`shp` (données vectorielles). Pour en savoir plus sur ces données vectorielles et d'autres types de données spatialement explicites, lisez la section {ref}`geospatial-data`.

(create-point-shp)=
### Créer un fichier de formes point

Commencez par charger des images satellite et une carte de base de rue (voir ci-dessus) dans le panneau des calques. Zoom sur l'Europe centrale et à peu près localiser Stuttgart dans le sud-ouest de l'Allemagne. Trouvez le fleuve Neckar fortement délabré au nord de Stuttgart et déplacez-vous dans la direction amont (c.-à-d. direction est), passez les villes d'Esslingen et Plochingen jusqu'à la confluence du Neckar et des fleuves Fils. De là, suivez la rivière Fils en direction en amont pendant quelques centaines de mètres et localisez le PEGELHAUS (c.-à-d. une station de jaugeage à la rivière Fils - [cliquez pour visiter](https://www.hvz.baden-wuerttemberg.de/pegel.html?id=00025)). Pour faciliter la recherche de la station de mesure à l'avenir, nous allons maintenant créer un fichier de forme de point comme expliqué dans la vidéo suivante et les instructions analogues ci-dessous la vidéo.

```{admonition} Create point shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/k2LqPM6wicA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

* Dans le menu supérieur de QGIS aller à **Layer** > **Créer un calque** > **Nouveau calque de fichier de forme**
  * Définir un nom de fichier (par exemple **gauges.shp** - ne peut pas dépasser 13 caractères), par exemple, dans un dossier appelé *qgis-exercice*.
  * Type de géométrie: `MultiPoint`
  * Dimensions supplémentaires: `Z(+M Values)`
  * Ajouter deux nouveaux champs :
    * `StnName` (* Données textuelles*)
    * `StnID` (*Numéro du trou*)
* Éditer/draw points
  * **Toggle Editing** (c.-à-d., activer en cliquant sur le stylo jaune <img src="../img/qgis/yellow-pen.png">) > **Digitizing Toolbar** > **Add Point Feature** <img src="../img/qgis/sym-add-point.png">
  * Cliquez sur le PEGELHAUS pour dessiner un point et définir
    * `StnName`: `PlochingenFils`
    * `StnID`: `00025`
  * Ajoutez plus de points si vous voulez.
  * Finaliser les modifications en cliquant sur **Enregistrer les modifications de calque** <img src="../img/qgis/sym-save-edits.png"> > **Arrêter (Toggle) Modifier** en cliquant sur le stylo jaune <img src="../img/qgis/yellow-pen.png"> symbole.
* Améliorer la visualisation en changeant la symlogie :
  * ** Double-cliquez sur** les jauges **couche** > **Symbiologie**
  * Mettre en évidence **Simple Marqueur**, changer le symbole **+** et changer la couleur et la taille de remplissage.
  * Mettre en évidence **Marquer** et changer l'opacité**
  * Cliquez sur **Appliquer** et **OK**
* Vérifiez les paramètres des points dans la table **Attribute** (cliquez à droite sur le calque *gauges* et sélectionnez **Attribute Table**).

(create-line-shp)=
### Créer un fichier de formes de ligne

Créer un **Line Shapefile** appelé **CenterLine.shp** pour dessiner une ligne centrale du Fil $\pm$ 200 m autour de la jauge PEGELHAUS, semblable au shapefile point créé ci-dessus. Ajouter un champ *text* et l'appeler `RiverName`. Puis tracer une ligne le long de la rivière Fils commençant à 200 m en amont et se terminant à 200 m en aval du PEGELHAUS en suivant la rivière sur la couche **OpenStreetMap**. Voir plus dans la vidéo suivante.

```{admonition} Create Line shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/yNuiIlPsguQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

(create-polygon-shp)=
### Créer un fichier de formes Polygon

Pour délimiter différentes zones de rugosité (p. ex., au besoin pour un modèle numérique bidimensionnel), créer un fichier de formes **Polygon** appelé **FlowAreas.shp**. Le fichier contiendra des polygones zonant la section considérée des Fils dans la plaine inondable et le lit du canal principal. Nommez le premier champ `AreaType` (type: *Text*) et le second champ `ManningN` (type: *Numéro de décret*). Voir plus dans la vidéo suivante et les instructions ci-dessous la vidéo.

```{admonition} Create Polygon video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/zTrowT0ULfo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Pour dessiner les polygones:

* Activer le claquage pour éviter les écarts entre la plaine inondable et les polygones du canal principal
  * Activer la barre d'outils ** snapping**: **Voir** > **Barres d'outils** > **Barre d'outils d'échantillonnage**
  * Activer le snapping à partir de la barre d'outils **Snapping** > **Enable Snapping** et **Éviter le chevauchement en polygone**
* Pour dessiner un polygone, allez à la barre d'outils **Digitation** > **Ajouter une fonctionnalité en polygone** avec l'option **Digitiser avec l'option Segment** activée
* Commencez à dessiner en cliquant sur la carte (clic droit final Polygon)
* Dessinez un polygone du canal principal et après la finalisation:
  * `AreaType`: `MainChannel`
  * `ManningN`: `0.028`
* Dessinez deux autres polygones des plaines inondables de la rive droite (RB) et de la rive gauche (LB) et définissez :
  * `AreaType`: `FloodPlainRB` et `FloodPlainLB`
  * `ManningN`: `0.05` (les deux)
* Si vous avez fait une erreur de dessin, utilisez soit la table *Attribute* pour sélectionner et supprimer des polygones entiers, soit utilisez l'outil vertex <img src="../img/qgis/sym-vertex-tool.png"> de la barre de menus.
* Après avoir dessiné tous les polygones, **Enregistrer les éditions** et **Toggle Editing** (désactiver).
* Pour améliorer la visualisation, modifiez la **Symbologie** en **Catégorie** en fonction du champ `AreaType`: Keep **Random Colors** > Cliquez sur **Classifier** > **Appliquer** et si vous aimez la visualisation, cliquez sur **OK**.


## Conversion: Rasterize (Polygon en Raster)

De nombreux modèles numériques exigent que la rugosité soit fournie au format {ref}`raster`. À cette fin, cette section présente la conversion du fichier de forme polygone créé ci-dessus (*FlowAreas.shp*) en une rugosité {ref}`raster`. La vidéo suivante et les instructions ci-dessous décrivent le fonctionnement de la conversion.

```{admonition} Rasterization video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/IRLwYSUnjcE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Pour convertir un ensemble de données vectorielles géospatiales, utilisez l'outil *Rasterize* :

* Dans la barre de menu QGIS, assurez-vous d'activer le panneau *Processing Toolbox* (**View** > **Panels** > **Processing Toolbox**)
* Dans la **Boîte à outils de traitement** > recherche (tap) **Rasterize** > sélectionner **Rasterize (vecteur à raster)**

```{hint}
Si le plugin *Crayfish* est installé, un autre outil *Rasterize* apparaîtra, que nous n'utiliserons pas dans ce tutoriel (c.-à-d., assurez-vous de sélectionner *Rasterize (vecteur à raster)*).
```

* Dans la fenêtre **Rasterize (Vector to Raster)** :
  * **Couche d'entrée**: `FlowAreas`
  * **Field to use for a burn-in value**: `ManningN`
  * ** Unités de taille de raster de sortie**: `Pixels`
  * ** Résolution width/horizontale** : `100` (le plus petit, le plus grossier du raster)
  * **Hauteur/résolution verticale**: `100` (le plus petit, le plus grossier du raster)
  * ... défiler vers le bas ...
  * **Étendue des résultats** : cliquez sur le bouton **...** > **Calculer à partir du calque** > `FlowAreas`
  * **Rasterized** (NOM DU DOSSIER) > cliquez sur le bouton **...** > **Enregistrer dans le fichier...** > `roughness.tif`
  * Cliquez sur **Run**
* Réglez la **Symbologie** à **Singleband pseudocolor** avec **Interpolation**: `Discrete`, **Colorramp**: `Magma`, **Mode**: `Equal Interval` > **Appliquer**. Si la visualisation est satisfaisante, cliquez sur **OK**.

```{admonition} File conversion with Python
:class: tip
La conversion entre les types de données géospatiales peut être facilitée en utilisant Python. Lisez la section sur {ref}`py-conversion` pour en savoir plus.
```

## Polygonize

The inverse operation of *Rasterize* is called **Raster to Vector**, which is documented at [https://docs.qgis.org](https://docs.qgis.org/testing/en/docs/training_manual/complete_analysis/raster_to_vector.html). The creation of a Polygon shapefile from a Raster is described in the video below. The essential steps are:

* Aller à **Raster** (menu supérieur) > **Conversion** > **Polygonize (Raster to Vector)...**
* **Couche d'entrée** : sélectionnez le raster à convertir
* ** Numéro de bande**: la bande de raster pour l'insertion de la valeur de polygone (c.-à-d. champ dans la table d'attribut); quelques notes:
  * cet algorithme va arrondir les décimales aux entiers (voir vidéo ci-dessous)
  * Sinon, recherchez *Raster pixels vers polygones* dans *Processing Toolbox*, mais cela créera un nombre excessif de polygones
* **Nom du champ à créer** : sélectionnez un nom pour le champ de valeur polygone dans la table des attributs (**pas plus de 10 caractères**)
* **Vectorized**: définir le répertoire et le nom du nouveau fichier de formes polygones
* Cliquez sur **Run**

```{admonition} Polygonize (video)

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/r9MwkKvUD-k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

Obtenez le [**mannings-n GeoTIFF ici**](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/mannings-n.tif).

```


Pour convertir un Raster en un fichier ligne/point (vecteur), les options sont l'outil [Contour](https://docs.qgis.org/3.28/en/docs/training_manual/processing/interp_contour.html) (**Raster** menu > **Extraction** > **Contour**) ou l'algorithme [Raster pixels to points](https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorcreation.html#raster-pixels-to-points) (**Processing** toolbox > enter `raster pixels to points`). Regardez aussi les tutoriels sur {ref}`geo file conversion with Python <raster2line>`.



## Travailler avec Rasters

### Calculatrice de grille QGIS (algèbre carte)

Certains modèles de préférence (utilisation par défaut) *n* de Manning, d'autres utilisent le coefficient de rugosité Strickler $k_{st}$, qui est l'inverse de *n* de Manning (c.-à-d. $k_{st} = 1/n$ - lire plus sur les coefficients de rugosité dans l'exercice {ref}`ex-1d-hydraulics`). Ainsi, transformer un raster de rugosité Strickler en raster de rugosité Manning nécessite d'effectuer une opération de raster algébrique (pixel par pixel). La vidéo suivante et les instructions ci-dessous présentent l'utilisation du QGIS **Raster Calculator** pour effectuer de telles opérations algébriques.

```{admonition} Raster calculator (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/DOkV03uij9k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Commencez par l'ouverture de la barre de menus QGIS (**Raster** > **Raster Calculator...**). Puis, convertissez le raster *roughness.tif* créé ci-dessus des valeurs *n* de Manning en un raster de rugosité Strickler :

* Définir une couche **Output** (par exemple, *qgis-exercise/roughness-stickler.tif*) et conserver le format **Output** de **{term}`GeoTIFF`**.
* Sélectionnez en option une étendue de couche correspondant au raster *roughness.tif* créé ci-dessus.
* Dans le type de cadre **Raster Calculator Expression** **1**, puis cliquez sur le bouton **/** (cadre**Operators**), puis sélectionnez **roughness@1** dans le cadre **Raster Bands**.
* Le cadre **Raster Calculatrice Expression** doit maintenant contenir : `1 / "roughness@1"`, où le signe `@` se réfère au numéro de bande `1`.
* Cliquez sur **OK** pour lancer *Raster Calculator*.
* Après un calcul réussi, modifiez en option la symlogie de la nouvelle couche (*roughness-stickler*).

```{admonition} Batch-process geodata
:class: tip
Pour mettre en œuvre une calculatrice sur mesure pour le traitement par lots de fichiers raster avec Python lire la section {ref}`py-raster-calculator` dans l'exercice {ref}`ex-geco`.
```

(make-xyz)=
### Raster à XYZ

Les formats de données scientifiques, tels que {term}`HDF`, fonctionnent mieux avec des ensembles de données géospatiales brutes comme `*.xyz` fichiers. Un fichier `.*xyz` contient uniquement des coordonnées X, Y et Z de points (c.-à-d. des nuages de points) avec ou sans en-tête simple. Par exemple, ce livre électronique utilise des données `*.xyz` pour l'interpolation d'altitude d'une maille de calcul pour le logiciel de modélisation numérique scientifique {ref}`chpt-telemac`. Pour générer un `*.xyz` à partir d'un {term}`GeoTIFF` raster utiliser le workflow suivant:

* Dans le panneau **Layers**, assurez-vous d'importer la couche raster pour la conversion et ** identifiez sa valeur de Non-Données** (** Propriétés de Layer** > **Informations** > **Section Bands** > **No-Données** afficher par défaut le champ `-9999` dans QGIS).
* Dans le menu supérieur QGIS aller à **Raster** > **Conversion** > **Traduit par la Rédaction...**
* Dans la fenêtre **Translate (Format Convert)**, effectuez les réglages suivants :
  * **Couche d'entrée** = le raster (par exemple, un {term}`Modèle numérique de terrain <DEM>`) à convertir
  * ** Paramètres avancés** cadre > **Type de données de sortie** > sélectionner **Float32** (correspond à une seule précision dans les modèles numériques)
  * **Converti** > **...** bouton (à la fin de la ligne) > **Enregistrer dans le fichier...** > définir un nom de fichier** tel que `dem-points` et sélectionner `XYZ files (*.xyz)` dans le champ **Enregistrer comme type**.
  * **Save** et **Run** la traduction (conversion).

Le fichier résultant `*.xyz` contient également des points avec **No-Data** pour remplir des espaces vides dans l'image rectangulaire de {term}`GeoTIFF` (que QGIS a reconnu comme des pixels sans données). Les points sans données peuvent rendre le fichier `*.xyz` inutilement lourd, en particulier lorsqu'il s'agit d'un {term}`Modèle numérique de terrain <DEM>` d'une rivière naturelle proche du recensement. Pour éliminer les points inutiles sans données, ouvrez le fichier `*.xyz` dans un logiciel de tableur, comme {ref}`Calc in LibreOffice <lo>` et utilisez l'outil *Sort* (en **Calc** mettre en évidence tous les points aller à **Données** > **Sort...**) pour trier par `Z` valeurs (le plus grand au plus petit) et ensuite supprimer toutes les lignes qui ont la valeur **No-Data** identifiée ci-dessus (`-9999`) comme `Z` valeur. Enregistrer le fichier `*.xyz` et fermer le logiciel de tableur.

```{admonition} Shapefile to XYZ
:class: tip, dropdown
**Les formulaires** ne doivent pas être convertis en {term}`GeoTIFF` pour créer un fichier `*.xyz`. Pour créer un fichier `*.xyz` à partir d'un fichier **shapefile** :

* Faites un clic droit sur le shapefile dans le panneau **Layer** > **Export** > **Enregistrez la fonctionnalité sous...**.
* Sélectionnez **Comma Valeur séparée ({term}`CSV`)** dans le champ **Format**.
* Définissez un nom de fichier** en cliquant sur le bouton **...**.
* Dans le cadre ** Options Layer**, sélectionnez **AS XYZ** dans le champ **GEOMETRY** et conservez toutes les autres valeurs par défaut.
* Cliquez sur **OK** pour convertir {term}`CSV`.
* Open the {term}`CSV` file in a {ref}`text editor <npp>` and use its *find and replace* function (usually `CTRL`+`F` or `CTRL`+`H`) to replace all COMMA `,` by a space symbol ` `. Note that this action requires that the comma has not been used as decimal separator.
* Enregistrer le fichier {term}`CSV` en tant que fichier `*.xyz`.
```

Pour finaliser le fichier `*.xyz`, ouvrez-le dans un {ref}`text editor <npp>` et ajoutez un en-tête. Par exemple, utilisez l'en-tête suivant pour travailler avec {ref}`Blue Kenue <bluekenue>`:

```
:FileType xyz  ASCII  EnSim 1.0
:EndHeader
```

Enregistrer les changements. Le fichier `*.xyz` est maintenant mince et prêt à être utilisé, par exemple, pour le fichier {ref}`TELEMAC pre-processing <get-dem-xyz>`.

## Créer la mise en page et les cartes PDF / JPG (ou autre)

Les images géoréférencées dans {term}`GeoTIFF` ou d'autres formats raster, éventuellement avec des fichiers de forme superpositionnés sur le dessus, sont pratiques et flexibles pour une utilisation avec des logiciels géospatials, comme QGIS, mais ne conviennent pas pour les présentations ou les rapports. À des fins de présentation, les images ou cartes géospatiales devraient de préférence être exportées vers des formats communs, tels que le **P**ortable **D**occument **F**ormat (PDF) ou **JPEG/JPG**. Pour créer des cartes généralement formatées avec QGIS, il faut d'abord créer une nouvelle mise en page (imprimée), qui peut ensuite être exportée vers un format de carte commun (par exemple, avec une légende, une barre d'échelle et une flèche nord). La vidéo suivante et les descriptions ci-dessous le guide vidéo à travers le processus de création de carte avec QGIS.

```{admonition} Layout creation (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/hmTByzVPVF0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Commencez par créer une nouvelle mise en page en cliquant sur le menu déroulant **Project**, puis sélectionnez **Nouvelle mise en page**. Dans la nouvelle mise en page, préparer la carte et l'exporter comme suit :

* Définir un titre **Layout** (par exemple, *exercice-layout*).
* Dans la nouvelle (* exercice-layout*) Disposition:
  * Aller à **Ajouter un élément** > **Ajouter une carte**.
  * Dessinez un rectangle qui contiendra la carte.
  * **Ajouter un élément** > **Ajouter une barre d'échelle**
  * Pour contrôler les échelles et les unités indiquées dans la barre d'échelle:
    * Dans le panneau **Items**, surlignez `<Scalebar>` et trouvez l'onglet **Item Properties** ci-dessous.
    * Dans l'onglet Propriétés de l'article **, modifiez les unités à votre convenance.
  * **Ajouter un élément** > **Ajouter une légende**
  * Pour contrôler les éléments de la légende :
    * Dans le panneau **Items**, surlignez `<Legend>` et trouvez l'onglet **Item Properties** ci-dessous.
    * Dans l'onglet **Propriétés de l'article**, trouvez **Articles législatifs** > désactivés **Mise à jour automatique** > **supprimer** *OpenStreetMap* et *Google Satellite*.
  * Passez par d'autres **Items** dans la barre de menu **Ajouter l'élément** (p. ex. **Arrow** pour Northing).
* **Enregistrer** le projet de mise en page (dans le menu supérieur **Enregistrer** > **Enregistrer le projet**)
* Exporter la carte aux formats communs:
  * Pour JPG ou PNG: **Layout** > **Exporter en tant qu'image**
  * Pour PDF : **Layout** > **Exporter en format PDF**
  * En option, pour les graphiques SVG-vector: **Layout** > **Exporter en tant que SVG**

QGIS a beaucoup d'autres capacités, mais ce tutoriel fondamental aurait dû vous fournir les connaissances nécessaires pour tirer parti de la puissance de QGIS pour de nombreuses applications.

(pygis)=
## PyQGIS: QGIS et Python

L'interface utilisateur graphique QGIS (GUI) fournit une ligne de commande Python (**Plugins** > **Python Console**), qui permet d'automatiser presque n'importe quel clic de souris dans l'interface graphique. Cette ligne de commande Python est appelée **PyQGIS** et le [QGIS developer docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html) fournit des instructions sur la façon d'importer et d'exécuter des scripts Python autonomes en dehors de l'interface graphique QGIS. Voici le modèle Python de base pour exécuter un script PyQGIS :


```python
from qgis.core import *

# define qgis installation location
QgsApplication.setPrefixPath("/path/to/qgis/installation", True)


# instantiate a QgsApplication, where the second argument (False) disables the GUI
qgs = QgsApplication([], False)


# load providers
qgs.initQgis()

# HERE GOES YOUR CUSTOM CODE

# exit the QGIS application to remove the provider and layer registries from memory
qgs.exitQgis()
```

Cependant, lorsque vous ouvrez le terminal de votre système ou Anaconda Prompt pour lancer un code PyQGIS, vous pouvez être bloqué sur la première ligne de code déjà: `from qgis.core import *` rendements `ImportError: No module named qgis.core`. Selon le [QGIS developer docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html), cette erreur se produit parce que le Python de votre système ne sait pas où vit l'environnement PyQGIS. Pour que votre terminal reconnaisse PyQGIS, prenez les mesures suivantes selon votre système :

`````{tab-set}
````{tab-item} Linux

Ouvrir le terminal et installer `python-qgis`:

```
sudo apt install python-qgis
```

Après l'installation réussie, essayez si vous pouvez maintenant importer `qgis.core`:

```
USER@computer:~$ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from qgis.core import *
>>> exit()
```

If `from qgis.core import *` did not throw any error, you are all set and can stop reading. **Otherwise**, find and open your `.bashrc` file (Debian/Ubuntu/Mint: `/home/USERNAME/.bashrc`). Note that files starting with a `.` name are hidden on Linux and become visible by toggling with simultaneously pressing the `CTRL`+`H` keys.

Au bas de `.bashrc` ajouter ce qui suit

```
export PYTHONPATH=/<qgispath>/share/qgis/python
```

L'expression `<qgispath>` devrait être remplacée par l'endroit où vit l'environnement PyQGIS. Pour savoir où c'est, tapez (dans Terminal):

```
dpkg-query -L python-qgis
```

Ceci indique où vit PyQGIS, qui, sur Ubuntu/Mint est typiquement:

```
/usr/lib/python3/dist-packages/
```

Dans ce cas, ajoutez `.bashrc`:

```
export PYTHONPATH=/usr/lib/python3/dist-packages/
```

Ensuite, connectez-vous et reconnectez-vous à votre système (c.-à-d. rechargez `.bashrc`). La commande `from qgis.core import *` devrait maintenant fonctionner en Python.
````

````{tab-item} Windows

Assurez-vous que votre système sache où vit PyGIS en ajoutant la ligne suivante aux variables d'environnement (Windows 10 : **Mon ordinateur** > **Propriétés** > **Paramètres avancés du système** > **variables d'environnement**). Remplacer `<qgispath>` par le chemin où QGIS vit sur votre système.

* Nom variable = `PYTHONPATH`
* Valeur variable = `C:\<qgispath>\python`

Ou utilisez l'invite Windows :

```
set PYTHONPATH=C:\<qgispath>\python
```

````
`````


