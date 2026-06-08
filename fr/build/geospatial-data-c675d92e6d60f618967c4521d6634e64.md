---
description: Données géospatiales expliquées et avec les sources de rasters et de shapefiles
---

(geospatial-data)=
# Données géospatiales

```{tip}
Utilisez {ref}`qgis-install` pour afficher les données géospatiales et créer des cartes en format *PDF* ou image (p. ex., *tif*, *png*, *jpg*). En outre, le {ref}`qgis-tutorial` offre une promenade facile et interactive à travers les analyses géospatiales.
```

```{admonition} Geodata explained on YouTube
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/lJUvZv5ts3U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Watch this section as a video on the <a href="https://www.youtube.com/@hydroinformatics">@Hydro-Morphodynamics channel on YouTube</a>.</p>
```

## Sources de données géographiques
Les données géospatiales peuvent être récupérées à diverses fins à partir de différentes sources. Voici quelques-uns d'entre eux:

* Les données géographiques de la carte de type atlas sont fournies par [naturalearthdata.com](https://www.naturalearthdata.com) (p. ex., le kit de démarrage rapide de la Terre naturelle](https://www.naturalearthdata.com/downloads/) avec des projets QGIS pré-classés).
* {term}`DEM`s, cartes océanographiques et plus liées à l'eau sont disponibles à la [NOAA Geo-platform](https://noaa.maps.arcgis.com/home/search.html?q=owner%3Ancei_noaa&t=content&start=1&sortOrder=desc&sortField=modified&focus=layers) et son [TDS Catalog](https://www.ncei.noaa.gov/thredds/catalog/catalog.html)
* [OpenStreetMap](https://www.openstreetmap.org) data extractions are available at [https://download.geofabrik.de/](https://download.geofabrik.de/)
* L'imagerie satellitaire est disponible à l'adresse suivante:
    - le [USGS' Earth Explorer](https://earthexplorer.usgs.gov/)
    - l'écosystème de données Copernicus de l'ESA](https://dataspace.copernicus.eu/) (Sentinel-1/2/3/5P; cela a remplacé l'ancien centre d'accès ouvert Copernicus / *SciHub*, qui a été mis hors service le 2 novembre 2023)
    - [planet.com](https://www.planet.com/products/monitoring/) (commercial)
* [LiDAR](https://oceanservice.noaa.gov/facts/lidar.html) les données peuvent être trouvées à [opentopographie.org](https://opentopography.org/).
* Les données climatologiques sont fournies par [NASA Earth Observations (NEO)](https://neo.gsfc.nasa.gov/).
* Les données météorologiques (p. ex. température ou précipitations) et les données satellitaires en temps réel sont disponibles à [wunderground.com](https://www.wunderground.com/) et ses [wundermap](https://www.wunderground.com/wundermap).
* Les données et prévisions climatiques et météorologiques sont disponibles à [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu), y compris, par exemple, les données mensuelles moyennes de température ERA5
* Les données sur l'utilisation des terres (y compris la couverture du couvert végétal), les caractéristiques socioéconomiques et les changements planétaires sont disponibles au catalogue de cartes de la FAO (GeoNetwork)](https://data.apps.fao.org/map/catalog/srv/eng/catalog.search) ou au portail de cartes mondiales de l'ISCGM archivé ([aller à leur archive GitHub](https://globalmaps.github.io/)).
* Topographical data  (1 to 5-m resolution) from the state of Bavaria, Germany, can be found at [https://www.ldbv.bayern.de](https://www.ldbv.bayern.de/produkte/3dprodukte/gelaende.html).
* Topographical data from EU countries can be found at [https://www.mapsforeurope.org](https://www.mapsforeurope.org/datasets/euro-dem).

## Visualisation
Un logiciel SIG est nécessaire pour afficher les données géospatiales et de nombreux outils existent. Ce site Web fournit principalement des exemples en utilisant {ref}`qgis-install`. Puisque l'utilisation du logiciel SIG, en particulier *QGIS*, est nécessaire pour plusieurs sections de ce livre électronique, des explications sur la façon d'installer *QGIS* sont déjà incluses dans le {ref}`chpt-geo-software`.

```{tip}
Le {ref}`qgis-tutorial` présente les bases du traitement des données géospatiales avec {ref}`qgis-install`.
```

(gdb)=
## Base de données géographiques
Une base de données géodonnées (également connue sous le nom de base de données *spatiale*) peut stocker, interroger (par exemple, en utilisant [Structured Query Language SQL](https://en.wikibooks.org/wiki/Structured_Query_Language)) ou modifier des données avec des références géographiques (*geospatial data*). Les données géospatiales se composent principalement de données vectorielles (voir shapefiles), mais les données raster peuvent également être mises en œuvre. Une base de données géodonnées relie ces données à des tableaux d'attributs et à des coordonnées géographiques. Une caractéristique particulière des bases de données géographiques est qu'elles peuvent être visualisées et manipulées via un serveur (web ou local) SIG (système d'information géographique). Par exemple, des logiciels comme {ref}`qgis-install` (ou *ArcGIS Pro*) permettent de créer des cartes et de faire des requêtes sur une sorte de serveur local en utilisant des données géodonnées stockées localement. Le format de base géographique typique est `.gdb`, qui fonctionne comme un répertoire à {ref}`qgis-install` ou *ArcGIS*, et la taille maximale d'un fichier `.gdb` est de 1 téraoctet.

```{figure} ../img/geo-database.png
:alt: gdb

Le squelette fonctionnel d'une base de données géographiques.
```

(vector)=
## Données sur les vecteurs

Les données vectorielles sont visuellement lisses et efficaces pour les opérations de recouvrement, en particulier en ce qui concerne l'information géocompatible, comme les routes ou les délimitations de surface. Les données vectorielles sont caractérisées comme étant peu intensives en stockage, faciles à évaluer et compatibles avec les environnements relationnels. Les formats communs sont `.shp`, `JSON` ou `TIN`.

Le format shapefile a été inventé par *Esri* au début des années 1990 (la description technique originale [shapefile (PDF)](https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/shapefile.pdf) reste la référence autorisée) et l'information contenue dans un shapefile peut être :

* Polygones (plaques de surface),
* Points avec coordonnées x-y-z et un champ *m* contenant des données ponctuelles, et
* (Poly) lignes composées de lignes définies par les points de départ et les points de départ.

(shp)=
### Fichier de forme

```{note}
Le nom du pilote `gdal.ogr` pour le traitement du fichier de formes est `ogr.GetDriverByName('ESRI Shapefile')`.
```

Un shapefile se compose de plusieurs fichiers sur le disque avec les parties essentielles suivantes:

* un fichier `.shp`, où les géométries sont stockées,
* a fichier `.shx`, où les indices des géométries sont stockés,
* un fichier `.prj` qui stocke la projection, et
* un fichier `.dbf` contenant des informations sur les attributs (constitue la table des attributs).

Ces fichiers doivent être dans le même dossier - sinon, le shapefile est incomplet et ne fonctionne pas (correctement). Quelques autres fichiers peuvent survenir lorsque nous manipulons un shapefile (par exemple, `.atx`, `.sb*`, `.shp.xml`, `.cpg`, `.mxs`, `.ai*`, ou `.fb*`), mais nous pouvons ignorer ces fichiers.

Les données vectorielles de Shapefile possèdent généralement une table d'attributs (comme n'importe quelle autre base de données géodonnées) dans laquelle chaque objet polygone, ligne ou point peut recevoir une valeur d'attribut. Les attributs sont définis par des colonnes avec leurs noms (en-têtes de colonnes) et peuvent avoir des formats numériques (p. ex. *float*, *double*, *int* ou *long*), texte (*string*), ou date/heure (p. ex. *aaammdd* ou *HH:MM:SS*).

```{figure} ../img/geo-shp-illu.png
:alt: shp-illu

Illustration des caractéristiques du fichier de formes point (rouge), (poly) ligne (vert) et polygone (bleu).
```

### Shapefile versus Geodatabase
Un shapefile peut être compris comme un format concurrent à une base de données géographiques. Quel est le meilleur format de fichier ? Strictement parlant, une base de données géodonnées et un fichier de formes peuvent effectuer des opérations similaires, mais un fichier de formes nécessite plus d'espace de stockage pour stocker des contenus similaires, ne peut pas stocker des champs de date et d'heure combinés, et ne supporte pas les données raster ou les valeurs *Null* (*not-a-number*). Les fichiers de formes sont également limités à 2 Go par fichier composant, les noms d'attributs de 10 caractères ou moins et les champs de texte de 255 caractères ou moins. Ainsi, les bases de données géographiques (et le format {ref}`GeoPackage <gpkg>` le plus portable) ont un avantage technique sur les fichiers de forme, mais l'utilisation des fichiers de forme est encore populaire et de nombreux flux de travail géospatials traditionnels se concentrent sur les manipulations de fichiers de forme.

(tin)=
### Réseau irrégulier triangulé (TIN)

A triangulated irregular network (TIN) represents a surface composed of multiple triangles. In hydraulic engineering and water resources research, one of the most important uses of a TIN is the generation of computational meshes for numerical models (read more in the {ref}`chpt-basement` tutorial, for example). In such models, a TIN consists of lines and nodes forming georeferenced, three-dimensionally sloped triangles of the surface, which represent a digital elevation model (DEM). TIN nodes have georeferenced coordinates and potentially more attribute information such as node IDs and elevation. The advantage of a TIN DEM over a raster (see below) DEM is that it requires less storage space. However, manipulating a TIN is not as straightforward as manipulating a raster. The below figure shows an example TIN created with [`matplotlib.tri.TriAnalyzer`](https://matplotlib.org/stable/api/tri_api.html#matplotlib.tri.TriAnalyzer), and based on a [showcase from the matplotlib docs](https://matplotlib.org/stable/gallery/images_contours_and_fields/tricontour_smooth_delaunay.html). The file ending of a TIN is `.tin`.

```{figure} ../img/geo-tin.png
:alt: tin-illu

Illustration d'un TIN.
```

(geojson)=
### GéoJSON

```{note}
Le nom du pilote `gdal.ogr` pour le traitement de GeoJSON est `ogr.GetDriverByName('GeoJSON')`.
```

[GeoJSON](https://geojson.org/) est un format ouvert pour représenter les données géographiques avec des normes d'accès aux fonctionnalités simples, où *JSON* indique *JavaScript Object Notation* (lisez plus sur {ref}`json` manipulation de fichiers dans les bases de Python). GeoJSON est normalisé comme [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946). Le nom du fichier GeoJSON se terminant est `.geojson` et un fichier a généralement la structure suivante:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [9.104028940200806, 48.74417005744522]
      },
      "properties": {
        "name": "IWS"
      }
    }
  ]
}
```

Alors que les métadonnées GeoJSON peuvent fournir des informations sur la hauteur (`z` valeurs) en tant que valeur `properties`, il y a une progéniture plus appropriée pour coder la topologie géospatiale sous la forme du [TopoJSON](https://github.com/topojson/topojson/wiki) format. Pour manipuler les fichiers GeoJSON avec Python, allez à la section {ref}`geojson-pckg`. Pour créer un fichier GeoJSON personnalisé, visitez [geojson.io](https://geojson.io/).

(gpkg)=
## Géoemballage (GPKG)

```{note}
Le nom du pilote `gdal.ogr` pour le traitement de GeoPackage est `ogr.GetDriverByName('GPKG')`. Le même pilote `GPKG` dans GDAL gère également les tuiles raster (voir [GDAL GPKG vector](https://gdal.org/en/stable/drivers/vector/gpkg.html) et [GDAL GPKG raster](https://gdal.org/en/stable/drivers/raster/gpkg.html) docs).
```

[GeoPackage](https://www.geopackage.org/) (`.gpkg`) est un format de données géospatiales ouvert, indépendant de la plate-forme et fondé sur des normes, publié par le [Open Geospatial Consortium (OGC)](https://www.ogc.org/) (norme 12-1228r19 de l'OGC). Techniquement, un GeoPackage est un seul fichier de base de données [SQLite](https://www.sqlite.org/) 3 qui suit les spécifications de GeoPackage, ce qui signifie qu'il peut être ouvert, interrogé et modifié avec n'importe quel outil SQLite-aware en plus du logiciel SIG comme {ref}`QGIS <qgis-install>`.

Contrairement à un {ref}`shapefile <shp>` (qui est vraiment un petit paquet de fichiers sidecar), un GeoPackage est *un seul fichier* qui peut contenir simultanément:

* Des couches multiples **vecteur** (points, lignes, polygones, géométrie mixte) dans un conteneur,
* **Pyramides de carrelage (par exemple, images {term}`GeoTIFF`-style ou Modèle numérique de terrain (MNT)),
* **Tableaux attributs** sans géométrie,
* **Index satellites** (R-tree) pour les requêtes spatiales rapides,
* **Métadonnées** et styles.

### Pourquoi utiliser un GeoPackage au lieu d'un shapefile ?

Comparé au shapefile, le format GeoPackage supprime la plupart des limitations bien connues du shapefile :

| Property | Shapefile | GeoPackage |
|---|---|---|
| Number of files per dataset | At least 3 (`.shp`, `.shx`, `.dbf`, plus `.prj`, `.cpg`, ...) | 1 (`.gpkg`) |
| Number of layers per file | 1 | Many (vector and raster mixed) |
| Maximum size | 2 GB per component file | ~140 TB (SQLite limit) |
| Field name length | ≤ 10 characters | Unlimited (practically) |
| Text field length | ≤ 255 characters | Unlimited (TEXT) |
| Character encoding | Code-page dependent (`.cpg`) | UTF-8 (full Unicode) |
| Date/time data type | Date only | Full `DATETIME` |
| Null / NaN values | Not supported | Supported |
| Spatial index | External (`.sbn`/`.sbx`) | Built-in R-tree |
| Raster support | No | Yes (tiled) |
| Standardization | De-facto (Esri whitepaper) | Open OGC standard |

### Lecture et écriture d'un GeoPackage avec Python

GeoPackage est nativement soutenu par GDAL/OGR, [Fiona](https://fiona.readthedocs.io/), [geopandas](https://geopandas.org/), et [rastério](https://rasterio.readthedocs.io/). Un aller-retour typique avec *geopandas* ressemble à :

```python
import geopandas as gpd

# Read a specific layer from a GeoPackage
gdf = gpd.read_file("rivers.gpkg", layer="centerlines")

# Write (or append) another layer into the same .gpkg
gdf.to_file("rivers.gpkg", layer="centerlines_buffered", driver="GPKG")
```

Pour lister tous les calques contenus dans un GeoPackage :

```python
import fiona
print(fiona.listlayers("rivers.gpkg"))
```

Parce qu'un GeoPackage est une base de données SQLite, les requêtes d'attributs peuvent également être émises directement via SQL:

```python
import sqlite3
con = sqlite3.connect("rivers.gpkg")
for row in con.execute("SELECT name, length_m FROM centerlines WHERE length_m > 1000"):
    print(row)
```

```{tip}
Pour les nouveaux projets dans le {ref}`qgis-tutorial` et le {ref}`Geospatial Python tutorials <sec-geo-python>`, préférez **GeoPackage sur shapefile**. QGIS utilise même GeoPackage comme format de sauvegarde par défaut lorsque vous créez un nouveau calque vectoriel à travers *Layer* > *Créer un calque* > *Nouveau calque GeoPackage...*.
```

(raster)=
## Données sur les cellules broyées
Les ensembles de données Raster stockent des valeurs de pixel (*cellules*), qui nécessitent un grand espace de stockage, mais ont une structure simple. Un autre grand avantage des rasters est la possibilité d'effectuer des analyses géospatiales et statistiques. Les formats courants des ensembles de données de raster sont, entre autres, `.tif` ({term}`GeoTIFF`), *GRID* (un dossier avec `BND`, `HDR`, `STA`, `VAT`, et d'autres fichiers), `.flt` (points flottants), {term}`ASCII` (American Standard Code for Information Interchange) et beaucoup d'autres types de fichiers semblables à des images.

```{tip}
Utiliser de préférence le format {term}`GeoTIFF` pour les analyses de raster. Un fichier GeoTIFF comprend généralement un fichier `.tif` (avec des données lourdes) et un fichier `.tfw` (un fichier du monde en texte simple de six lignes contenant des informations géoréférencées).
```

```{note}
Le nom du pilote `gdal` pour la manipulation {term}`GeoTIFF` est `gdal.GetDriverByName('GTiff')`.
```

```{figure} ../img/geo-raster-illu.png
:alt: raster-illu

Illustration du raster NE1 50M SR W.tif de la Terre naturelle zoomé sur le Népal, avec des fichiers de forme point et ligne indiquant respectivement les grandes villes et les frontières du pays. Prenez note de l'aspect carrelé de la grille, où chaque carrelage correspond à une cellule raster 50m-x-50m.
```

## Modèles d'élévation numérique lidar et sous-marine (Bathymetries)

Les données des relevés terrestres sont souvent fournies sous la forme d'un ensemble de données point-y-z ainsi que de paramètres d'attribut point. Les ensembles de données tridimensionnels de la surface topographique nue de la Terre sont appelés un modèle d'élévation numérique (lisez la terminologie **{term}`DEM`** dans le glossaire), qui représente la base de toute analyse physique d'un écosystème fluvial. La topographie sous-marine est appelée la **bathymétrie** d'une rivière ou d'un autre plan d'eau. De nos jours, les nuages point x-y-z pour générer un Modèle numérique de terrain (MNT) proviennent principalement de sondages {term}`Lidar` combinés avec {term}`Echo sounder`. Les approches plus anciennes reposent sur l'arpentage manuel (p. ex., avec une station totale) de profils de rivières transversales et l'interpolation du terrain entre les profils. La nouvelle technique {term}`Lidar` utilise des sources de lumière (laser) et fournit des données bathymétriques jusqu'à 2 m d'eau profonde sous la forme de `*.las` ou le formulaire zippé `*.laz` fichiers. Les eaux plus profondes sont cartographiées avec un {term}`Echo sounder` et les ensembles de données fusionnés {term}`Lidar` et échosounding produisent des nuages de points sans soudure des écosystèmes fluviaux, qui peuvent être stockés dans différents types de fichiers.

{term}`Lidar` produit des nuages de points massifs, qui surchargent rapidement même des ordinateurs puissants. C'est pourquoi dans la pratique, les données {term}`Lidar` peuvent devoir être ventilées en zones plus petites de moins de 10<sup>6</sup> points chacun. Le logiciel de traitement {term}`Lidar` (par exemple, [LASTools](http://lastools.org/)) est utile dans cette tâche.


(prj)=
## Projections et systèmes de coordination
Dans les analyses de données géospatiales, une projection représente une approche pour aplatir (une partie du) globe. Dans ce processus d'aplatissement, les coordonnées latitudinales (Nord/Sud) et longitudinales (Ouest/Est) d'un emplacement sur le globe (trois dimensions - 3d) sont projetées sur les coordonnées d'une carte bidimensionnelle (2d). Lorsque les coordonnées 3d sont projetées sur des coordonnées 2d, des distorsions se produisent, et divers systèmes de projection sont utilisés dans les analyses géospatiales. Dans la pratique, cela signifie que si nous utilisons des fichiers de données géospatiales avec des projections différentes, un effet de distorsion se propage dans tous les calculs ultérieurs. Il est essentiel d'éviter de tels effets de distorsion en veillant à ce que le même système de projection et de coordonnées de référence (SCR) soit appliqué de manière cohérente à toutes les données géospatiales. Cela commence par la création d'une nouvelle couche géospatiale (p. ex., un fichier de forme vectoriel point ou {ref}`GeoPackage <gpkg>`) à {ref}`QGIS (get installation instructions) <qgis-install>` et doit être utilisé de façon cohérente dans tous les codes de programme. Pour spécifier un CS Ex; par exemple, dans **QGIS** (tutoriel dans le {ref}`next section <qgis-tutorial>`), cliquez sur **Projet** > **Propriétés** > **onglet Système de coordonnées** et sélectionnez un `COORDINATE_SYSTEM`. Par exemple, un système de coordination approprié pour l'Europe centrale est `ESRI:31493` (lire plus dans le [QGIS docs](https://docs.qgis.org/latest/en/docs/user_manual/working_with_projections/working_with_projections.html)). Les systèmes projetés varient selon la région (*systèmes de coordonnées locales*), qui peuvent être trouvés, par exemple, à [epsg.io](https://epsg.io/) ou [spatialereference.org](https://spatialreference.org/).

Dans **shapefiles**, l'information sur la projection est stockée dans un fichier `.prj` (rappelez les définitions dans {ref}`shapefile section <shp>`), qui est un fichier texte. Le Consortium géospatial ouvert (*OGC*) et Esri utilisent [*Well-Known Text* (**WKT**)](https://docs.ogc.org/is/18-010r11/18-010r11.html) fichiers pour la description standard des systèmes de coordonnées, et un fichier formaté WKT `.prj` est affiché dans le bloc de code ci-dessous. Les unités et les mesures définies dans le fichier formaté WKT `.prj` déterminent également les unités de *WK**B*** (*Well-Known Binary*) définitions des géométries telles que la longueur des lignes (par exemple, en mètres, pieds, ou bien d'autres), ou la surface polygonale (mètres carrés, kilomètres carrés, acres, et bien d'autres).


```python
PROJCS["unknown",GEOGCS["GCS_unknown",
                        DATUM["D_Unknown_based_on_GRS80_ellipsoid",SPHEROID["GRS_1980",6378137.0,298.257222101]],
                        PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
       PROJECTION["Lambert_Conformal_Conic"], PARAMETER["False_Easting",6561666.66666667],
       ..., UNIT["US survey foot",0.304800609601219]]
```

Dans les fichiers {ref}`geojson`, le système de référence de coordonnées par défaut est **WGS 84** (longitude/latitude, [EPSG:4326](https://epsg.io/4326)), comme prescrit par [RFC 7946 §4](https://datatracker.ietf.org/doc/html/rfc7946#section-4).


```{admonition} Use EPSG:3857
:class: tip

Pour s'assurer que toutes les géométries sont mesurées en mètres et puissances de compteurs, utilisez [**EPSG:3857**](https://epsg.io/3857) (la projection *Web Mercator* utilisée par la plupart des services de cartes en ligne; anciennement connue sous le nom `EPSG:900913` -- *g00glE*) pour définir le fichier de projection formaté WKT.
```
