---
description: Tutoriel pour le prétraitement d'un modèle d'élévation numérique (Modèle numérique de terrain (MNT)) en QGIS pour générer un maillage de calcul au format SMS 2dm pour les simulations hydrodynamiques de BASE.
---

(qgis-prepro-bm)=
# Prétraitement avec QGIS

```{admonition} Requirements
:class: attention
Ce tutoriel est conçu pour **débutants** et avant de plonger dans ce tutoriel assurez-vous de:

* Suivez les instructions d'installation pour {ref}`qgis-install` dans ce livre électronique.
* Lisez (ou regardez) et comprenez ce livre électronique {ref}`qgis-tutorial`.
```

Les premières étapes de la modélisation numérique d'une rivière avec BASE consistent en la conversion d'un modèle d'élévation numérique ** ({term}`DEM`)** en maillage informatique. Ce tutoriel guide la création d'un projet QGIS pour la conversion d'un {term}`DEM` ({term}`GeoTIFF`) en maillage informatique qui peut être utilisé avec divers logiciels de modélisation numérique présentés dans ce livre électronique. À la fin de ce tutoriel, les utilisateurs {ref}`chpt-basement` auront généré une grille de calcul au format {term}`SMS 2dm`.

```{admonition} Platform compatibility
:class: tip
Toutes les applications logicielles présentées dans ce tutoriel peuvent être exécutées sur des plateformes *Linux*, *Windows* et *macOS* (en théorie - non testées). Notez que {ref}`chpt-basement` ne fonctionnera pas sur les plateformes *macOS*.
```

```{admonition} Recall: BASEMENT versions, BASEMD, and BASEHPC
:class: note

La version 2 (v2) de BASE a été développée avec des structures complexes et un large éventail de capacités, mais l'accent a été mis peu sur le temps de calcul. La version 3 (v3) de BASE a considérablement simplifié le processus de modélisation pour les utilisateurs et est venue avec des options informatiques très efficaces, y compris la parallélisation massive sur les GPU. Toutefois, la version simplifiée de la v3 manque de nombreux modules pertinents, tels que les lits de rivière multicouches pour calculer le changement topographique en fonction des formules de transport de lit multigrains. Maintenant, la version 4 de BASEMENT (v4) fournit à la fois les capacités multiples de v2 sous forme de configurations de BASEMD, et l'efficacité de calcul de v3 sous forme de configurations de BASEHPC. Ce tutoriel explique la configuration d'un modèle BASEHPC.

```

(start-qgis)=
## Configuration de QGIS

### Système de référence des coordonnées

Lancez QGIS et {ref}`create a new QGIS project <qgis-project>` pour commencer avec ce tutoriel.
Comme indiqué dans le {ref}`qgis-tutorial`, mettre en place un système de référence de coordonnées (SCR) pour le projet. Cet exemple utilise les données d'un fleuve en Bavière (zone 4 de l'Allemagne), qui nécessite le Système de coordonnées suivant:

* Dans le menu supérieur QGIS, allez à **Project** > **Propriétés**.
* Activez l'onglet **Système de coordonnées**.
* Entrez `Germany_Zone_4` et sélectionnez le CS Ex affiché à {numref}`Fig. %s <qgis-crs>`.
* Cliquez sur **Appliquer** et **OK**.

```{figure} ../img/qgis/inn-crs.png
:alt: qgis set coordinate reference system crs germany zone_4 Inn river
:name: qgis-crs

Définir Germany Zone 4 comme projet Système de coordonnées.
```

```{admonition} Save the project...
:class: tip
Enregistrer le projet QGIS (**Projet** > **Enregistrer sous...**), par exemple, sous le nom **prépro-tutorial.qgz**.
```

(get-basemesh)=
### Obtenez le plugin BASEmesh

Installez le module de connexion *BASEMESH* de *BASEMESH* (instructions du manuel du système *BASEM*):

* Chargez le gestionnaire de plugins *QGIS* : ** Menu Plugins** > **Gérer et installer des plugins**.
* Allez à l'onglet **Paramètres**.
* Faites défiler vers le bas (**Plugin Repositories** listbox in {numref}`Fig. %s <qgis-plugins2>`), cliquez sur **Ajouter...**.
* Dans la fenêtre contextuelle saisissez :
  * un nom pour le nouveau dépôt, par exemple, `BASEmesh Plugin Repository`
  * the repository address: [https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml)
  * garder tous les autres défauts.
* Cliquez sur **OK**. Le nouveau dépôt devrait maintenant être visible dans la listbox **Plugin Repositories**. Si la connexion est **OK**.

```{figure} ../img/qgis/bm-plugin.png
:alt: qgis basement plugins
:name: qgis-plugins2

Ajouter le dépôt de BASE au gestionnaire de plugins de QGIS.
```

* Toujours dans la fenêtre popup **Plugins** retourner à l'onglet **All** une entrée `basemesh` dans le champ de recherche.
* Trouvez le plugin **le plus récent BASEmesh** (c.-à-d. **Version disponible** >= 2.0.0) et cliquez sur **Installer le plugin**.
* Après l'installation réussie **Fermer** la fenêtre popup **Plugins**.
* Vérifiez que le plugin *BASEmesh 2* est maintenant disponible dans le menu QGIS **Plugins** (voir {numref}`Fig. %s <qgis-pluggedin>`).

```{figure} ../img/qgis/bm-pluggedin.png
:alt: qgis basement plugins
:name: qgis-pluggedin

Le plugin BASEmesh 2 est disponible dans le menu Plugins de QGIS après l'installation réussie.
```


(get-dem)=
## Charger Modèle numérique de terrain (MNT)

This tutorial uses an application-ready {term}`DEM` in {term}`GeoTIFF` {ref}`raster` format that stems from a {term}`Lidar` point cloud. The {term}`DEM` raster provides height (Z) information from a section of a gravel-cobble bed river in South-East Germany, which constitutes the baseline for the computational grids featured in the next sections. To get the provided DEM in the *QGIS* project:

* [**Télécharger l'exemple Modèle numérique de terrain (MNT) GeoTIFF**](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/dem.tif) et enregistrez-le dans le même dossier (`/Project Home/` ou un sous-répertoire) que le projet de création **qgz**.
* Ajouter le Modèle numérique de terrain (MNT) téléchargé comme nouveau calque raster dans *QGIS*:
  * Dans *QGIS*' **Parcourir**, vous trouverez le répertoire **Project Home** où vous avez téléchargé le code Modèle numérique de terrain (MNT) *tif*.
  * Faites glisser le Modèle numérique de terrain (MNT) *tif* du dossier **Project Home** dans le panneau **Layer** de QGIS.
* Pour faciliter la délimitation de certaines régions de l'écosystème fluvial plus tard, ajoutez un {ref}`satellite imagery basemap <basemap>` (carrelage XYZ) sous le {term}`DEM` et personnalisez la symbolique du calque.

```{admonition} What are QGIS panels again?
:class: tip
En savoir plus dans le tutoriel *QGIS* sur {ref}`qgis-tbx-install`.
```

Le Modèle numérique de terrain (MNT) doit maintenant être affiché sur la carte (si non : faites un clic droit sur le calque Modèle numérique de terrain (MNT) et cliquez sur **Zoom to Layer(s)** dans le menu contextuel) comme indiqué dans {numref}`Fig. %s <qgis-dem-basemap>`.

```{figure} ../img/qgis/dem-basemap.png
:alt: qgis import raster DEM basemap
:name: qgis-dem-basemap

Le Modèle numérique de terrain (MNT) importé sur une carte de base Google Satellite (source: Google / GeoBasis-DEBKG 2019). La direction d'écoulement est de gauche à droite suivant la flèche **Q**.
```


(make-2dm)=
## Créer 2dm Mesh

La génération d'un {term}`SMS 2dm` utilise le {ref}`QGIS BASEmesh plugin <get-basemesh>`

* {ref}`Line Shapefile <create-line-shp>` contenant les limites du modèle et les lignes de rupture internes entre les régions modèles ayant des caractéristiques différentes (section sur {ref}`boundary`);
* {ref}`Line Shapefile <create-line-shp>` contenant les limites du modèle pour l'attribution des conditions d'entrée et de sortie (section sur {ref}`liquid-boundary`);
* {ref}`Point Shapefile <create-point-shp>` contenant des marqueurs pour la définition des caractéristiques des régions modèles (section sur {ref}`regions`).

Ces shapefiles permettent de générer un {ref}`Quality Mesh <qualm>`. En fin de compte, l'information sur la hauteur est {ref}`interpolated to the quality mesh <qualm-interp>` et le maillage résultant est enregistré comme fichier {term}`SMS 2dm`. Les sections suivantes passent par la procédure étape par étape avec des explications détaillées. Des matériaux supplémentaires et des produits de données intermédiaires sont fournis dans le dépôt de données supplémentaires ([materials-bm](https://github.com/hydro-informatics/materials-bm)) pour ce tutoriel.


(boundary)=
### Modèle de limite et lignes de rupture

La limite du modèle définit l'étendue du modèle et peut être divisée en régions présentant des caractéristiques différentes (p. ex. valeurs de rugosité) par des lignes de rupture. Les lignes d'arrêt indiquent, par exemple, les berges du chenal et le lit du fleuve (le chenal principal) et doivent être à l'intérieur des limites du Modèle numérique de terrain (MNT). Les lignes de démarcation et les lignes de rupture sont stockées dans un {ref}`Line Shapefile <create-line-shp>` que BASEmesh utilise pour trouver les limites du modèle et les lignes de rupture internes entre les régions modèles. À cette fin, {ref}`create-line-shp` avec **un champ de texte** appelé **Type de ligne** et l'appeler **breaklines.shp** (**Layer** > **Créer un calque** > **Nouveau calque de fichier de forme**). Cliquez sur QGIS' **Layers** menu > **Créer un calque** > **Nouveau calque de fichier de forme...** (voir {numref}`Fig. %s <qgis-new-lyr>`). Assurez-vous de sélectionner `ESRI: 31494 - Germany_Zone_4` comme {term}`CRS` <img src="../img/qgis/sym-crs.png">.

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: qgis-new-lyr

Créez un nouveau shapefile à partir du menu Calques de QGIS.
```

Il est important que les lignes ne se chevauchent pas pour éviter les définitions ambiguës ou manquantes des régions et pour s'assurer que toutes les lignes frontalières forment des régions fermées (zones). Par conséquent, activez le snapping:

* Activer la barre d'outils *Snapping* : **Voir** > **Barres d'outils** > **Snapping Toolbar**
* Dans la barre d'outils **Snapping** > **Enable Snapping** <img src="../img/qgis/snapping-horseshoe.png">
* Activer le snapping pour
  * ** Vertex**, **Segment** et **Moyen de segments** <img src="../img/qgis/snapping-vertex-segments.png">.
  * **Sonder sur les intersections** <img src="../img/qgis/snapping-intersection.png">.

Ensuite, commencez à modifier **breaklines.shp** en cliquant sur le stylo jaune <img src="../img/qgis/yellow-pen.png"> et dessinez les lignes indiquées dans {numref}`Fig. %s <breaklines>` en activant **Ajouter la ligne Feature** <img src="../img/qgis/sym-add-line.png">.

* ** Limites du modèle** à gauche et à droite ** Limites des plaines d'inondation** :
  * Délimitez les limites extérieures des plaines inondables.
  * Assurez-vous que tous les points et lignes sont à l'intérieur de {ref}`DEM layer <get-dem>`.
  * Ne pas traverser la rivière (zone humide indiquée par la carte de base des images satellite).
  * **Finaliser** chaque ligne avec un ** clic droit**.
  * Pour le champ **LineType**, utilisez des valeurs de texte telles que **boundary left/right floodplain**.
  * Consultez les lignes rouges à {numref}`Fig. %s <breaklines>`**.
* **Lignes limites de la rive gauche (LB) et de la rive droite (RB)**:
  * Dessiner des lignes le long du canal principal mouillé indiqué dans la carte de base des images satellitaires.
  * Assurez-vous que la ligne se termine parfaitement avec les lignes de limite de la plaine inondable avant la création (c'est là que le claquage aide); ainsi, les lignes de rupture du chenal principal et les lignes de limite de la plaine inondable doivent enfermer les plaines inondables sans aucun écart entre les lignes.
  * Pour le champ **LineType**, utilisez des valeurs de texte telles que **hardline LB/RB**.
  * Reportez-vous aux lignes **yellow-orange dans {numref}`Fig. %s <breaklines>`** (notez la délimitation des petits affluents en haut à gauche sur la rive gauche et en bas à droite sur la rive droite).
* **Breaklines des berges de gravier**:
  * Dessinez des lignes le long des berges de gravier qui sont visibles dans la carte de base de l'imagerie satellite dans le canal principal.
  * Assurez-vous que la ligne se termine parfaitement avec les lignes de rupture du chenal principal avant la création (lignes rigides); ainsi, les lignes de rupture du chenal principal et les lignes de rupture du banc de gravier doivent enfermer les berges de gravier sans écart entre les lignes.
  * Pour le champ **LineType**, utilisez des valeurs de texte telles que **hardline gravillon**.
  * Voir les lignes en vert dans {numref}`Fig. %s <breaklines>`**.
* Facultatif : **Breaklines des rampes de blocs** :
  * Trouvez les rampes de blocs rugueux (eaux de coupe) dans la carte de base des images satellitaires et délimitez-les en dessinant des lignes à travers le canal principal mouillé.
  * Assurez-vous que la ligne se termine parfaitement avec les lignes de rupture du canal principal; ainsi, les lignes de rupture du canal principal et les lignes de rupture de la rampe de bloc doivent enfermer les rampes de bloc sans aucun écart entre les lignes.
  * Pour le champ **LineType**, utilisez des valeurs de texte telles que **hardline sss** (ou n'importe quoi d'autre - l'exemple renvoie au mot allemand <u>S</u>chütt<u>s</u>tein<u>s</u>chwelle).
  * Voir les lignes bleues à {numref}`Fig. %s <breaklines>`**.
* Facultatif: **Ligne de rupture d'un banc de sable**:
  * Trouvez le dépôt de sable dans le coin supérieur gauche à {numref}`Fig. %s <breaklines>` sur la carte de base de l'imagerie satellite et délimitez-le en dessinant une ligne bien courbe.
  * Assurez-vous que la ligne se termine parfaitement avec les lignes de rupture du canal principal et embrassez une zone fermée sans écart entre les lignes.
  * Pour le champ **LineType**, utilisez des valeurs de texte telles que **hardline sand**.
  * Reportez-vous à la ligne **pourpre** dans le coin supérieur gauche **à {numref}`Fig. %s <breaklines>`**.

Pour ** corriger les erreurs de dessin** utilisez l'outil ** Vertex** <img src="../img/qgis/sym-vertex-tool.png">. Enfin, enregistrez les nouvelles lignes (édits de **breaklines.shp**) en cliquant sur le symbole **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png">. **Arrêtez (Toggle) Édition** en cliquant à nouveau sur le stylo jaune <img src="../img/qgis/yellow-pen.png"> symbole.

```{figure} ../img/qgis/breaklines.png
:alt: qgis basement basemesh draw breaklines boundaries
:name: breaklines

Frontière et lignes de rupture pour dessiner **breaklines.shp**. Les rives gauche et droite et les plaines inondables sont orientées dans la direction de l'écoulement ( flèche**Q**).
```

```{admonition} Troubles with drawing boundaries and breaklines?
:class: tip
Téléchargez le [shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/breaklines.zip)] montré dans la figure ci-dessus et déballer dans le dossier du projet, par exemple `/Project Home/shapefiles/breaklines.[SHP]`.
```

Le style de calque par défaut est **Single Symbol**. Pour une meilleure représentation, double-cliquez sur le calque des lignes de rupture, allez à l'onglet **Symbole** et sélectionnez **Categorized** (ou **Graduated**) au lieu de **Symbole unique** (en haut de la fenêtre **Propriétés de couche**). Dans le champ **Value**, sélectionnez **LineType**, puis cliquez sur le bouton **classify** au bas de la fenêtre **Layer Properties**. La listbox va maintenant afficher les valeurs *LineType*.

```{admonition} Draw boundaries of complex DEMs...
:class: tip
Dessiner des limites manuellement autour de grand {term}`DEM`s peut être très long, en particulier, si les données brutes sont un nuage de point et pas encore converti en {ref}`raster`.

Si vous avez affaire à un nuage de points, envisagez d'utiliser *QGIS* [Convex Hull tool](https://docs.qgis.org/3.16/en/docs/training_manual/vector_analysis/spatial_statistics.html?highlight=convex%20hull#basic-fa-create-a-test-dataset) qui tire un polygone serré autour de points.

Si vous avez affaire à un grand {term}`GeoTIFF`, envisagez d'utiliser QGIS [Raster à Vector](https://docs.qgis.org/3.16/en/docs/training_manual/complete_analysis/raster_to_vector.html) outil.
```


(liquid-boundary)=
### Limites des liquides (hydrauliques)

Les limites des liquides définissent les endroits où les conditions hydrauliques, telles qu'un débit donné ou une relation étape-décharge, s'appliquent aux limites d'écoulement (en amont) et d'écoulement (en aval). Ainsi, un modèle de rivière fonctionnel nécessite au moins une limite d'écoulement (ligne) où le débit massique dans le modèle et une limite d'écoulement (ligne) où les flux massiques quittent le modèle. À cette fin, {ref}`create-line-shp` appelé **liquide-boundarys.shp** et définir **deux champs de données texte** nommé **type** et **stringdef**. Assurez-vous que **snapping** est toujours **enabled** (comme expliqué plus haut dans la section {ref}`boundary`) et **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **liquide-boundarys.shp**. Puis dessinez deux lignes :

* Activer **Ajouter la fonctionnalité de ligne** <img src="../img/qgis/sym-add-line.png">.
* Dessiner une ligne limite d'entrée (voir aussi {numref}`Fig. %s <inflow-boundary>`):
  * Zoomer sur la zone d'entrée des limites de Modèle numérique de terrain (MNT), où il y a un écart entre** les lignes de rupture de la limite de la plaine d'inondation.
  * Commencer à tracer une ligne sur la rive gauche (côté gauche de la figure ci-dessous) et se diriger vers l'est (c'est-à-dire vers la droite) pour faire sept points de plus sur la rivière.
  * Le **septième point** doit **coïncide** avec la fin de la ligne de démarcation de la rive droite**.
  * Ainsi, le flux en amont provient du côté droit de la ligne limite d'entrée (c.-à-d., la direction de flux en amont sera `right` pour le modèle numérique).
  * **Finaliser** la ligne avec un ** clic droit**, et entrer `Inflow` dans le champ **type** et `inflow` dans le champ **stringdef** (l'affaire est importante).
  * Pour ** corriger les erreurs de dessin** utilisez l'outil ** Vertex** <img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/inflow-boundary.png
:alt: qgis basemesh draw inflow boundary line
:name: inflow-boundary

La limite d'entrée est tracée de gauche à droite (c.-à-d. que le débit en amont provient du côté droit de la limite d'entrée). La séquence des boutons à utiliser est surlignée par les boîtes rouges.
```

* Ensuite, dessinez une limite de sortie (voir aussi {numref}`Fig. %s <outflow-boundary>`):
  * Zoom sur la zone de sortie des limites de Modèle numérique de terrain (MNT), où il y a un écart entre** les lignes de rupture de la limite de la plaine d'inondation**.
  * Commencez à tracer une ligne sur la rive gauche (au sommet de la figure ci-dessous) et déplacez-vous vers le sud-ouest (c.-à-d. vers le bas) pour faire sept points de plus à travers la rivière.
  * Le **septième point** doit **coïncide** avec la fin de la ligne de démarcation de la rive droite**.
  * Ainsi, le flux en amont provient du côté droit de la ligne de limite de sortie (c.-à-d., la direction de flux en amont sera `right` pour le modèle numérique).
  * **Finaliser** la ligne avec un ** clic droit**, et entrer `Outflow` dans le champ **type** et `outflow` dans le champ **stringdef** (l'affaire est importante).
  * Pour ** corriger les erreurs de dessin** utilisez l'outil ** Vertex** <img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/outflow-boundary.png
:alt: qgis basemesh draw outflow boundary line
:name: outflow-boundary

La ligne limite de sortie est tirée du haut vers le bas (c.-à-d. que le débit en amont provient du côté droit de la ligne limite de sortie).
```

```{admonition} Constraints of inflow and outflow boundaries
:class: important
Les lignes limites d'entrée et de sortie doivent avoir le même nombre de nœuds (ici 7 plus 1) et aucune ligne limite liquide ne peut avoir plus de 40 nœuds.
```

Enfin, enregistrez les lignes limites de liquide (édits de **liquide-boundarys.shp**) en cliquant sur le symbole **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png">. **Arrêter (Toggle) Édition** en cliquant à nouveau sur le stylo jaune <img src="../img/qgis/yellow-pen.png"> symbole.

```{admonition} Troubles with drawing the liquid boundary lines?
:class: tip
Téléchargez le [shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/liquid-boundaries.zip) et déballer dans le dossier du projet, par exemple `/Project Home/shapefiles/liquid-boundaries.[SHP]`.
```

```{admonition} stringdefs
:class: note
Les valeurs de champ *stringdefs* peuvent être directement utilisées avec {ref}`chpt-basement`, où les données hydrauliques (p. ex., décharge, profondeur d'eau ou relations étape-décharge) peuvent être affectées aux lignes limites d'entrée et de sortie géoréférencées ici définies.
```

(regions)=
### Marqueurs régionaux

Les marqueurs régionaux sont placés dans des régions définies par les lignes limites et les lignes de rupture. Chaque marqueur régional (c.-à-d. un point quelque part dans la région) attribue, par exemple, un identifiant matériel (MATIDs) et une zone cellulaire maillage maximale. Cette dernière option permet de définir les petites cellules à mailles (zones de mailles) dans le lit du chenal actif et de les agrandir dans les régions de la plaine inondable. {ref}`create-point-shp` nommé **raster-points.shp** avec les définitions suivantes (voir aussi {numref}`Fig. %s <qgis-reg-lyr>`):

* Définir le nom de fichier **** comme **region-points.shp** (ou similaire)
* Assurez-vous que le type **Géométrie** est **Point**
* Le {term}`CRS` <img src="../img/qgis/sym-crs.png"> correspond à l'Allemagne Zone 4 ({ref}`see project CRS <start-qgis>`)
* Ajouter trois **Nouveau champ** (en plus du champ par défaut **Type entier** **ID**):
  * **max area** = **Nombre décimal** (**longueur** = 10, **précision** = 3)
  * **MATID** = **Nombre de trous** (**longueur** = 3)
  * **type** = **données textuelles** (**longueur** = 20)
* Cliquez sur **OK** pour créer le nouveau shapefile point.

```{figure} ../img/qgis/bm-region-pts-create.png
:alt: basement mesh qgis region layer points
:name: qgis-reg-lyr

Définitions et champs à ajouter au fichier de formes des points régionaux.
```

Considérez que **désactiver le snapping** pour dessiner les marqueurs de région pour éviter que les marqueurs de région coïncident avec n'importe quelle ligne. Ensuite, **Toggle (Démarrer) Modifier** <img src="../img/qgis/yellow-pen.png"> le nouveau fichier **region-points.shp** et activer **Ajouter un élément** <img src="../img/qgis/sym-add-point.png">. Dessinez un point dans chaque section qui est fermée par des lignes de rupture et des lignes limites (liquides). Selon le type de zone apparent à partir de la carte de base de l'imagerie satellitaire, assignez une des cinq régions énumérées à {numref}`Tab. %s <region-defs>` à chaque point.

```{list-table} Region names and their **max_area**, **MATID**, and **type** field values.
:header-rows: 1
:name: region-defs

* - Région
  - Rivière
  - Rampes de blocs
  - Banques de gravier
  - Plaines inondables
  - Sable
* - **max aire**
  -  25,0
  -  20,0
  -  25,0
  -  80,0
  -  20,0
* - **MATIDE**
  - 1
  - 2
  - 3
  - 4
  - 5
* - **Type**
  - lit de rivière
  - block ramp
  - banc de gravier
  - plaine inondable
  - Dépôt de sable
```

Après avoir dessiné un point dans chaque zone fermée, enregistrez les marqueurs de point de la région (modificateurs de **region-points.shp**) en cliquant sur le symbole **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png">. **Arrêtez (Toggle) Édition** en cliquant à nouveau sur le stylo jaune <img src="../img/qgis/yellow-pen.png"> symbole. {numref}`Figure %s <qgis-reg-pts>` montre un exemple de point de repère régional dans les zones délimitées par les lignes de rupture.

```{figure} ../img/qgis/bm-region-pts-map.png
:alt: basemesh region points
:name: qgis-reg-pts

Exemple pour les marqueurs de points régionaux dans les limites du projet.
```

```{admonition} Troubles with drawing the region marker points?
:class: tip
Download the [zipped region-points shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/region-points.zip) and unpack it into the project folder, for instance, `/Project Home/shapefiles/region-points.[SHP]`.
```

(qualm)=
### Créer un mesh de qualité

*L'outil de maillage de qualité de BASEmesh* crée un maillage triangulaire efficace par calcul basé sur {cite:t}`shewchuk1996` et à l'intérieur des limites du modèle. L'outil associe les propriétés du maillage aux régions shapefile ([voir section ci-dessus sur {ref}`regions`), mais il n'inclut pas les données d'élévation. Ainsi, après avoir généré un maillage de qualité, des informations sur l'élévation doivent être ajoutées. Cette section explique la génération de mailles de qualité et la section suivante présente l'interpolation des élévations de fond.

Dans le menu **Plugins** de QGIS, cliquez sur **BASEmesh 2** > **QUALITY MESHING** pour ouvrir l'outil de maillage de qualité. Faites les paramètres suivants dans la fenêtre contextuelle (voir aussi {numref}`Fig. %s <qgis-qualm>`):

* Cadre des contraintes de triangulation:
  * **Breaklines** = **Breaklines** (voir {ref}`boundary`).
  * Gardez tous les autres défauts.
* Cadre régional:
  * **Activer la case Régions**.
  * **Couche de repère de la région** = **régions-points** (voir {ref}`regions`).
  * **Activer le champ MATID** et sélectionner le champ *regions-points* du fichier de formes **MATID**.
  * **Activez le champ Zone maximale** et sélectionnez le champ *régions-points* du fichier de formes **max area**.
* Mesh domain frame : gardez les valeurs par défaut.
* Cadre de définitions des chaînes:
  * **Activer les définitions de la chaîne**.
  * **Couche des définitions de l'établissement** = **limites liquides**.
  * **Champ ID de définitions de fichiers** = **stringdef**.
  * **Activez la case Inclure dans les chaînes de nœuds 2DM (BASEMENT 3)**.
  * Ignorez toutes les options de base 2.8.
* Cadre de paramètres : conservez les valeurs par défaut.
* Cadre de sortie :
  * Cliquez sur le bouton **Parcourir...** et définissez un nom de fichier **2dm** dans le répertoire `/Project Home/`, comme **prepro-tutorial quality-mesh.2dm**.
* Cliquez sur le bouton **Run** pour créer le maillage de qualité.


```{figure} ../img/qgis/bm-quality-meshing-success.png
:alt: basement qgis quality mesh tin
:name: qgis-qualm

Définitions à faire dans l'outil de maillage Qualité de BASEmesh.
```

Un maillage de qualité peut prendre du temps. Après une génération réussie de maillage, le fichier **prepro-tutorial quality-mesh-interp.2dm** aura été généré.

(qualm-interp)=
### Interpoler l'élévation du bas à la qualité Mesh

The *BASEmesh* plugin's **Interpolation** tool projects bottom elevation data onto the quality mesh by interpolation from another mesh or a {term}`DEM` {ref}`raster`. Here, we use the {ref}`above-introduced DEM GeoTIFF <get-dem>`. To run the interpolation, open *BASEmesh*'s **Interpolation** tool (*QGIS* **Plugins** menu > **BASEmesh 2** > **Interpolation**) and make the following settings (see also {numref}`Fig. %s <qgis-qualm-interp>`):

* Dans la couche **Mesh à interpoler**, sélectionnez **prepro-tutorial quality-mesh**.
* Dans l'onglet **Basic**, trouvez le cadre **Source d'élévation** et activez le bouton **Activation via Modèle numérique de terrain (MNT) (Raster)**.
* Sélectionnez **dem.tif** GeoTIFF (voir {ref}`get-dem` section) comme **Couche de grille**.
* Dans le cadre **Output** cliquez sur le bouton **Browse** pour définir un nom de maille de sortie dans le répertoire `/Project Home/`, par exemple, **prepro-tutorial quality-mesh-interp.2dm**
* Cliquez sur **Run** pour créer le maillage interpolé en hauteur.

```{admonition} Error with BASEmesh v2.0.9 - Interpolation via DEM not working
:class: error

Depuis BASEmesh v2.0.9, la fenêtre **Interpolation** ne détecte aucune couche **Raster** (rien ne peut être sélectionné dans le menu déroulant). Une solution fonctionnelle consiste à convertir le raster Modèle numérique de terrain (MNT) en un fichier maillé :

1. Convertissez le Modèle numérique de terrain (MNT) en un shapefile point (**raster en vector**) et assurez-vous que la table d'attribut point est remplie d'élévations.
2. Utilisez l'outil **TIN Mesh Creation** pour générer un maillage d'élévation TIN avec des données d'élévation.
3. Dans l'outil **Interpolation** de BASEmesh, sélectionnez l'option **Interpolation via élévation Mesh** et sélectionnez le maillage d'élévation TIN créé avant.
4. Cliquez sur **Run** pour continuer avec le tutoriel.

Pour trouver les outils de conversion mentionnés ci-dessus, allez dans QGIS **Processing** top menu > **Toolbox** et entrez les noms d'outils dans le champ *search...*.

```

```{figure} ../img/qgis/bm-mesh-interpolation.png
:alt: qgis quality mesh interpolation basement
:name: qgis-qualm-interp

Outil d'interpolation de la valeur Z (hauteur) de BASEmesh et configuration pour attribuer les valeurs d'élévation du bas au maillage de qualité.
```

Après l'interpolation de l'altitude, vérifier que les élévations sont correctement assignées (c.-à-d. que l'élévation de la couche d'eau** aurait dû prendre des valeurs entre **367** et **387** m a.s.l.). Pour modifier la visualisation des calques (symbologie) double-cliquez sur le nouveau **prepro-tutorial quality-mesh-interp** et allez au ruban **Symbologie**. Sélectionnez **Gradué** en haut de la fenêtre, définissez le **Value** en Z, **Méthod** en COULEUR, choisissez une rampe de couleur et cliquez sur le **classify** en bas (partie inférieure de la fenêtre). Cliquez sur **Appliquer** et **OK** pour fermer les paramètres symlogy. {numref}`Figure %s <qgis-verify-qualm>` montre un exemple de visualisation du maillage interpolé en hauteur.

```{figure} ../img/qgis/bm-mesh-interp-success.png
:alt: basemesh verify interpolated quality mesh
:name: qgis-verify-qualm

Vérifier l'interpolation de l'altitude à l'aide de rampes de couleur graduées.
```

(qgis4bm)=
## Utilisation avec base

Le fichier maillage 2dm produit dans ce tutoriel peut être utilisé directement avec {ref}`chpt-basement`, où seule la définition des propriétés géométriques (par exemple, coefficients de rugosité) et liquides (par exemple, rejets) est requise comme expliqué plus loin.
