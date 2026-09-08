---
description: Geodaten erklärt und mit Quellen von Rastern und Shapefiles
---

(geospatial-data)=
# Geodaten

```{tip}
Verwenden Sie {ref}`qgis-install`, um Geodaten anzuzeigen und Karten in *PDF* oder Bildformaten zu erstellen (z. B. *tif*, *png*, *jpg*). Darüber hinaus bietet das {ref}`qgis-tutorial` einen einfachen und interaktiven Spaziergang durch geospatiale Analysen.
```

```{admonition} Geodata explained on YouTube
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/lJUvZv5ts3U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Watch this section as a video on the <a href="https://www.youtube.com/@hydroinformatics">@Hydro-Morphodynamics channel on YouTube</a>.</p>
```

## Geodatenquellen
Geodaten können für verschiedene Zwecke aus verschiedenen Quellen abgerufen werden. Hier sind einige davon:

* Geografische Kartendaten im Atlas-Stil werden von [naturalearthdata.com](https://www.naturalearthdata.com)] bereitgestellt (z. B. die ~230 MB [Natural Earth Quick Start Kit](https://www.naturalearthdata.com/downloads/) gebündelt mit vorgefertigten QGIS-Projekten].
* {term}`Digitales Oberflächenmodell <DEM>`s, ozeanographische und weitere wasserbezogene Karten sind unter den USA verfügbar [NOAA Geo-platform](https://noaa.maps.arcgis.com/home/search.html?q=owner%3Ancei_noaa&t=content&start=1&sortOrder=desc&sortField=modified&focus=layers) und seine [TDS Catalog](https://www.ncei.noaa.gov/thredds/catalog/catalog.html)]
* [OpenStreetMap](https://www.openstreetmap.org) data extractions are available at [https://download.geofabrik.de/](https://download.geofabrik.de/)
* Satellitenbilder sind verfügbar unter
    - [USGS] Earth Explorer](https://earthexplorer.usgs.gov/)
    - [ESA Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (Sentinel-1/2/3/5P; diese ersetzte den ehemaligen Copernicus Open Access Hub / *SciHub*, der am 2. November 2023 stillgelegt wurde]
    - [planet.com](https://www.planet.com/products/monitoring/) (kommerziell)]
* [LiDAR](https://oceanservice.noaa.gov/facts/lidar.html) Daten finden Sie unter [opentopography.org](https://opentopography.org/)].
* Klimatologische Daten werden von [NASA Earth Observations (NEO)](https://neo.gsfc.nasa.gov/) bereitgestellt.
* Meteorologische (z. B. Temperatur oder Niederschlag) und Echtzeit-Satellitendaten sind unter [wunderground.com](https://www.wunderground.com/) und dessen [wundermap](https://www.wunderground.com/wundermap)] verfügbar.
* Klima- und Wetterdaten und -vorhersagen sind unter [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu) verfügbar, einschließlich z. B. ERA5 monatlich gemittelte Temperaturdaten]
* Daten zur Landnutzung (einschließlich Baumkronenabdeckung), sozioökonomischen Merkmalen und globalen Veränderungen sind im [FAO-Kartenkatalog (GeoNetwork)](https://data.apps.fao.org/map/catalog/srv/eng/catalog.search) oder im archivierten ISCGM Global Map-Portal ([gehen Sie zu ihrem GitHub-Archiv](https://globalmaps.github.io/)].]
* Topographical data  (1 to 5-m resolution) from the state of Bavaria, Germany, can be found at [https://www.ldbv.bayern.de](https://www.ldbv.bayern.de/produkte/3dprodukte/gelaende.html).
* Topographical data from EU countries can be found at [https://www.mapsforeurope.org](https://www.mapsforeurope.org/datasets/euro-dem).

## Visualisierung
GIS software is needed to display geospatial data and many tools exist. This website primarily provides examples using {ref}`qgis-install`. Since the use of GIS software, especially *QGIS*, is necessary for several sections in this eBook, explanations on how to install *QGIS* are already included in the {ref}`chpt-geo-software`.

```{tip}
The {ref}`qgis-tutorial` features the basics of geospatial data handling with {ref}`qgis-install`.
```

(gdb)=
## Geodatenbank
Eine Geodatenbank (auch bekannt als *spatial database*) kann speichern, abfragen (z. B. unter Verwendung von [Structured Query Language SQL](https://en.wikibooks.org/wiki/Structured_Query_Language)]) oder Daten mit geografischen Referenzen ändern (*geospatial data*). Geodaten bestehen in erster Linie aus Vektordaten (siehe Shapefiles), es können aber auch Rasterdaten implementiert werden. Eine Geodatenbank verknüpft diese Daten mit Attributtabellen und geografischen Koordinaten. Eine Besonderheit von Geodatenbanken ist, dass sie über einen (Web- oder lokalen) GIS-Server (Geographic Information System) visualisiert und manipuliert werden können. Zum Beispiel ermöglicht Software wie {ref}`qgis-install` (oder *ArcGIS Pro*) das Erstellen von Karten und Abfragen auf einer Art lokalem Server mit lokal gespeicherten Geodaten. Das typische Geodatenbankformat ist `.gdb`, das als Verzeichnis in {ref}`qgis-install` oder *ArcGIS* funktioniert, und die maximale Größe einer `.gdb`-Datei beträgt 1 Terabyte.

```{figure} ../img/geo-database.png
:alt: gdb

Das funktionale Skelett einer Geodatenbank.
```

(vector)=
## Vektordaten

Vektordaten sind optisch glatt und effizient für Überlagerungsoperationen, insbesondere in Bezug auf formgesteuerte Geoinformationen wie Straßen oder Oberflächenabgrenzungen. Vektordaten werden als wenig speicherintensiv, einfach zu skalieren und mit relationalen Umgebungen kompatibel charakterisiert. Gängige Formate sind `.shp`, `JSON` oder `TIN`.

Das Shapefile-Format wurde von *Esri* in den frühen 1990er Jahren erfunden (das Original [shapefile technical description (PDF)](https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/shapefile.pdf) bleibt die maßgebliche Referenz) und die in einer Shapefile enthaltenen Informationen können sein:

* Polygone (Oberflächenflecken),
* Punkte mit x-y-z-Koordinaten und einem *m*-Feld mit Punktdaten und
* (Poly) Linien, die aus Linien bestehen, die durch Startpunkte und Endpunkte definiert sind.

(shp)=
### Shapefil

```{note}
Der `gdal.ogr` Treibername für Shapefile-Handling ist `ogr.GetDriverByName('ESRI Shapefile')`.
```

Eine Shapefile besteht aus mehreren Dateien auf der Festplatte mit den folgenden wesentlichen Teilen:

* eine `.shp`-Datei, in der Geometrien gespeichert sind,
* eine `.shx`-Datei, in der Indizes der Geometrien gespeichert sind,
* a `.prj` file that stores the projection, and
* eine `.dbf`-Datei mit Attributinformationen (bildet die Attributtabelle).

These files need to be in the same folder - otherwise, the shapefile is incomplete and does not work (correctly). A couple of other files may occur when we manipulate a shapefile (e.g., `.atx`, `.sb*`, `.shp.xml`, `.cpg`, `.mxs`, `.ai*`, or `.fb*`), but we can ignore those files.

Shapefile-Vektordaten haben typischerweise eine Attributtabelle (wie jede andere Geodatenbank), in der jedem Polygon, jeder Linie oder jedem Punktobjekt ein Attributwert zugewiesen werden kann. Attribute werden durch Spalten zusammen mit ihren Namen (Spaltenüberschriften) definiert und können numerische Formate (z.B. *float*, *double*, *int* oder *long*), Text (*string*) oder Datum/Uhrzeit (z.B. *yyyymmdd* oder *HH:MM:SS*) haben.

```{figure} ../img/geo-shp-illu.png
:alt: shp-illu

Darstellung von Punkt (rot), (Poly) Linie (grün) und Polygon (blau) Shapefile Features.
```

### Shapefile versus Geodatabase
Eine Shapefile kann als Konkurrenzformat zu einer Geodatenbank verstanden werden. Welches Dateiformat ist besser? Streng genommen können sowohl eine Geodatenbank als auch eine Shapefile ähnliche Operationen ausführen, aber eine Shapefile benötigt mehr Speicherplatz zum Speichern ähnlicher Inhalte, kann keine kombinierten Datums- und Zeitfelder speichern und unterstützt keine Rasterdaten oder *Null* (*not-a-number*) Werte. Shapefiles sind auch auf 2 GB pro Komponentendatei, Attributnamen von 10 Zeichen oder weniger und Textfelder von 255 Zeichen oder weniger begrenzt. Daher haben Geodatenbanken (und das portablere {ref}`GeoPackage <gpkg>`-Format) einen technischen Vorteil gegenüber Shapefiles, aber die Verwendung von Shapefiles ist immer noch beliebt und viele ältere Geodaten-Workflows konzentrieren sich auf Shapefil-Manipulationen.

(tin)=
### Trianguliertes unregelmäßiges Netzwerk (TIN)

A triangulated irregular network (TIN) represents a surface composed of multiple triangles. In hydraulic engineering and water resources research, one of the most important uses of a TIN is the generation of computational meshes for numerical models (read more in the {ref}`chpt-basement` tutorial, for example). In such models, a TIN consists of lines and nodes forming georeferenced, three-dimensionally sloped triangles of the surface, which represent a digital elevation model (DEM). TIN nodes have georeferenced coordinates and potentially more attribute information such as node IDs and elevation. The advantage of a TIN DEM over a raster (see below) DEM is that it requires less storage space. However, manipulating a TIN is not as straightforward as manipulating a raster. The below figure shows an example TIN created with [`matplotlib.tri.TriAnalyzer`](https://matplotlib.org/stable/api/tri_api.html#matplotlib.tri.TriAnalyzer), and based on a [showcase from the matplotlib docs](https://matplotlib.org/stable/gallery/images_contours_and_fields/tricontour_smooth_delaunay.html). The file ending of a TIN is `.tin`.

```{figure} ../img/geo-tin.png
:alt: tin-illu

Illustration einer TIN.
```

(geojson)=
### GeoJSON

```{note}
Der `gdal.ogr` Treibername für das GeoJSON-Handling ist `ogr.GetDriverByName('GeoJSON')`.
```

[GeoJSON](https://geojson.org/) ist ein offenes Format zur Darstellung geografischer Daten mit einfachen Feature-Zugriffsstandards, wobei *JSON* *JavaScript Object Notation* bezeichnet (lesen Sie mehr über {ref}`json`Dateimanipulation in den Python-Grundlagen). GeoJSON ist standardisiert als [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946)]. Das Ende des GeoJSON-Dateinamens ist `.geojson` und eine Datei hat normalerweise die folgende Struktur:

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

While GeoJSON metadata can provide height information (`z` values) as a `properties` value, there is a more suitable offspring to encode geospatial topology in the form of the [TopoJSON](https://github.com/topojson/topojson/wiki) format. To manipulate GeoJSON files with Python, go to the {ref}`geojson-pckg` section. To build a customized GeoJSON file, visit [geojson.io](https://geojson.io/).

(gpkg)=
## GeoPackage (GPKG)

```{note}
The `gdal.ogr` driver name for GeoPackage handling is `ogr.GetDriverByName('GPKG')`. The same `GPKG` driver in GDAL also handles raster tiles (see the [GDAL GPKG vector](https://gdal.org/en/stable/drivers/vector/gpkg.html) and [GDAL GPKG raster](https://gdal.org/en/stable/drivers/raster/gpkg.html) docs).
```

[GeoPackage](https://www.geopackage.org/) (`.gpkg`) ist ein offenes, plattformunabhängiges, standardbasiertes Geodatenformat, das vom [Open Geospatial Consortium (OGC)](https://www.ogc.org/) (OGC-Standard 12-128r19) veröffentlicht wird.] Technisch gesehen ist ein GeoPackage eine einzige [SQLite](https://www.sqlite.org/)3 Datenbankdatei, die der GeoPackage-Spezifikation folgt, was bedeutet, dass es mit jedem SQLite-basierten Tool zusätzlich zu GIS-Software wie {ref}`QGIS <qgis-install>` geöffnet, abgefragt und geändert werden kann.

In contrast to a {ref}`shapefile <shp>` (which is really a small bundle of sidecar files), a GeoPackage is *one single file* that can simultaneously contain:

* Mehrere **Vektorenschichten (Punkte, Linien, Polygone, Mischgeometrie) in einem Behälter,
* **Raster** Fliesenpyramiden (z.B. {term}`GeoTIFF`-style Bilder oder DEMs),
* **Attributtabellen** ohne Geometrie,
* **Räumliche Indizes** (R-Baum) für schnelle räumliche Abfragen,
* **Metadaten** und Stile.

### Warum ein GeoPackage anstelle eines Shapefiles verwenden?

Im Vergleich zur alten Shapefile entfernt das GeoPackage-Format die meisten bekannten Einschränkungen der Shapefile:

| Eigentum | Shapefile | GeoPackage |
|-----------
| Anzahl der Dateien pro Datensatz | Mindestens 3 (`.shp`, `.shx`, `.dbf`, plus `.prj`, `.cpg`, ...) | 1 (`.gpkg`) |
| Anzahl der Schichten pro Datei | 1 | Viele (Vektor und Raster gemischt) |
| Maximale Größe | 2 GB pro Komponentendatei | ~140 TB (SQLite Limit) |
| Feldnamenlänge | ≤ 10 Zeichen | Unbegrenzt (praktisch) |
| Textfeldlänge | ≤ 255 Zeichen | Unlimited (TEXT) |
| Zeichenkodierung | Codeseitenabhängig (`.cpg`) | UTF-8 (voller Unicode) |
| Datentyp Datum/Uhrzeit | Nur Datum | Voll `DATETIME`
| Null / NaN Werte | Nicht unterstützt | Unterstützt |
| Räumlicher Index | Extern (`.sbn`/`.sbx`) | Eingebauter R-Baum |
| Raster-Unterstützung | Nein | Ja (kachelt) |
| Standardisierung | De-facto (Esri Whitepaper) | Offener OGC-Standard |

### Lesen und Schreiben eines GeoPackage mit Python

GeoPackage wird nativ von GDAL/OGR, [Fiona](https://fiona.readthedocs.io/), [geopandas](https://geopandas.org/) und [rasterio](https://rasterio.readthedocs.io/)] unterstützt. Eine typische Rundreise mit *geopandas* sieht so aus:

```python
import geopandas as gpd

# Read a specific layer from a GeoPackage
gdf = gpd.read_file("rivers.gpkg", layer="centerlines")

# Write (or append) another layer into the same .gpkg
gdf.to_file("rivers.gpkg", layer="centerlines_buffered", driver="GPKG")
```

So listen Sie alle in einem GeoPackage enthaltenen Schichten auf:

```python
import fiona
print(fiona.listlayers("rivers.gpkg"))
```

Da es sich bei einem GeoPackage um eine SQLite-Datenbank handelt, können Attributabfragen auch direkt über SQL ausgegeben werden:

```python
import sqlite3
con = sqlite3.connect("rivers.gpkg")
for row in con.execute("SELECT name, length_m FROM centerlines WHERE length_m > 1000"):
    print(row)
```

```{tip}
Für neue Projekte in {ref}`qgis-tutorial` und {ref}`Geospatial Python tutorials <sec-geo-python>`, bevorzugen Sie **GeoPackage gegenüber Shapefile**. QGIS verwendet sogar GeoPackage als Standard-Speicherformat, wenn Sie eine neue Vektorschicht über *Layer* > *Create Layer* > *New GeoPackage Layer...* erstellen.
```

(raster)=
## Gitterzellendaten (Raster)
Raster-Datensätze speichern Pixelwerte (*Zellen*), die großen Speicherplatz benötigen, aber eine einfache Struktur haben. Ein weiterer großer Vorteil von Rastern ist die Möglichkeit, geospatiale Algebra und statistische Analysen durchzuführen. Gängige Raster-Datensatzformate sind unter anderem `.tif` ({term}`GeoTIFF`), *GRID* (ein Ordner mit `BND`, `HDR`, `STA`, `VAT` und anderen Dateien), `.flt` (schwimmende Punkte), {term}`ASCII` (American Standard Code for Information Interchange) und viele weitere bildähnliche Dateitypen.

```{tip}
Preferably use the {term}`GeoTIFF` format for raster analyses. A GeoTIFF file typically includes a `.tif` file (with heavy data) and a `.tfw` (a six-line plain text world file containing georeference information) file.
```

```{note}
Der `gdal` Treibername für {term}`GeoTIFF`Handling ist `gdal.GetDriverByName('GTiff')`.
```

```{figure} ../img/geo-raster-illu.png
:alt: raster-illu

Illustration des NE1 50M SR W.tif-Rasters der natürlichen Erde, das auf Nepal gezoomt wurde, mit Punkt- und Linienformdateien, die auf Großstädte bzw. Ländergrenzen hinweisen. Beachten Sie das kachelartige Erscheinungsbild des Gitters, bei dem jede Kachel einer 50m-x-50m-Rasterzelle entspricht.
```

## Lidar und Unterwasser Digitale Höhenmodelle (Bathymetrien)

Terrain survey data are often delivered in the shape of an x-y-z point dataset along with point attribute parameters. Three-dimensional datasets of the bare Earth's topographic surface are referred to as a Digital Elevation Model (read more about **{term}`Digitales Oberflächenmodell <DEM>`** terminology in the glossary), which represents the baseline for any physical analysis of a river ecosystem. The underwater topography is called the **bathymetry** of a river or other water body. Nowadays, x-y-z point clouds for generating a DEM mostly stem from {term}`Lidar` combined with {term}`Echolot <Echo sounder>` surveys. Older approaches rely on manual surveying (e.g., with a total station) of cross-sectional river profiles and interpolating the terrain between the profiles. The newer {term}`Lidar` technique employs light (laser) sources and provides bathymetry data up to 2-m deep water in the form of `*.las` or the zipped form `*.laz` files. Deeper waters are mapped with an {term}`Echolot <Echo sounder>` and the merged {term}`Lidar` and echo-sounding datasets produce seamless point clouds of river ecosystems, which may be stored in different file types.

{term}`Lidar` produces massive point clouds, which quickly overcharge even powerful computers. This is why in practice, {term}`Lidar` data may need to be broken down into smaller zones of less than 10<sup>6</sup> points each. Particular {term}`Lidar` processing software (e.g., [LAStools](http://lastools.org/)) is helpful in this task.


(prj)=
## Projektionen und Koordinatensysteme
In geospatial data analyses, a projection represents an approach to flatten (a part of) the globe. In this flattening process, latitudinal (North/South) and longitudinal (West/East) coordinates of a location on the globe (three-dimensional - 3d) are projected onto the coordinates of a two-dimensional (2d) map. When 3d coordinates are projected onto 2d coordinates, distortions occur, and a variety of projection systems are used in geospatial analyses. In practice, this means that if we use geospatial data files with different projections, a distortion effect propagates into all subsequent calculations. It is crucial to avoid such distortion effects by ensuring that the same projection and coordinate reference system (CRS) is applied consistently to all geospatial data. This starts with the creation of a new geospatial layer (e.g., a point vector shapefile or {ref}`GeoPackage <gpkg>`) in {ref}`QGIS (get installation instructions) <qgis-install>` and should be used consistently in all program codes. To specify a CRS; for instance, in **QGIS** (tutorial in the {ref}`next section <qgis-tutorial>`), click on **Project** > **Properties** > **CRS** tab and select a `COORDINATE_SYSTEM`. For example, an appropriate coordinate system for central Europe is `ESRI:31493` (read more in the [QGIS docs](https://docs.qgis.org/latest/en/docs/user_manual/working_with_projections/working_with_projections.html)). Projected systems vary with region (*local coordinate systems*), which can be found, for example, at [epsg.io](https://epsg.io/) or [spatialreference.org](https://spatialreference.org/).

In **shapefiles**, information about the projection is stored in a `.prj` file (recall definitions in the {ref}`shapefile section <shp>`), which is a plain text file. The Open Geospatial Consortium (*OGC*) and Esri use [*Well-Known Text* (**WKT**)](https://docs.ogc.org/is/18-010r11/18-010r11.html) files for standard descriptions of coordinate systems, and a WKT-formatted `.prj` file is shown in the code block below. The units and measures defined in the WKT-formatted `.prj` file also determine the units of *WK**B*** (*Well-Known Binary*) definitions of geometries such as line length (e.g., in meters, feet, or many more), or polygon area (square meters, square kilometers, acres, and many more).


```python
PROJCS["unknown",GEOGCS["GCS_unknown",
                        DATUM["D_Unknown_based_on_GRS80_ellipsoid",SPHEROID["GRS_1980",6378137.0,298.257222101]],
                        PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
       PROJECTION["Lambert_Conformal_Conic"], PARAMETER["False_Easting",6561666.66666667],
       ..., UNIT["US survey foot",0.304800609601219]]
```

In {ref}`geojson` files, the default coordinate reference system is **WGS 84** (longitude/latitude, [EPSG:4326](https://epsg.io/4326)), as mandated by [RFC 7946 §4](https://datatracker.ietf.org/doc/html/rfc7946#section-4).


```{admonition} Use EPSG:3857
:class: tip

Um sicherzustellen, dass alle Geometrien in Metern und Meterpotenzen gemessen werden, verwenden Sie [**EPSG: 3857**](https://epsg.io/3857)] (die *Web Mercator*-Projektion, die von den meisten Online-Kartendiensten verwendet wird; früher bekannt als `EPSG:900913` -- *g00glE*), um die WKT-formatierte Projektionsdatei zu definieren.
```
