---
description: Geospatiale Daten erklärt und mit Quellen von Rastern und Formdateien
---

(geospatial-data)=
# Geodaten

```{tip}
Verwenden Sie {ref}`qgis-install`, um geospatiale Daten anzuzeigen und Karten in *PDF* oder Bildformaten zu erstellen (z.B. *tif*, *png*, *jpg*). Darüber hinaus bietet die {ref}`qgis-tutorial` einen einfachen und interaktiven Spaziergang durch geospatiale Analysen.
```

```{admonition} Geodata explained on YouTube
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/lJUvZv5ts3U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Watch this section as a video on the <a href="https://www.youtube.com/@hydroinformatics">@Hydro-Morphodynamics channel on YouTube</a>.</p>
```

## Geodatenquellen
Geospatiale Daten können für verschiedene Zwecke aus verschiedenen Quellen abgerufen werden. Hier sind einige von ihnen:

* Geographical, atlas-style map data are provided by [naturalearthdata.com](https://www.naturalearthdata.com) (e.g., the ~230 MB [Natural Earth quick start kit](https://www.naturalearthdata.com/downloads/) bundled with pre-styled QGIS projects).
* {term}`DEM`s, oceanographic and more water-related maps are available at the US' [NOAA Geo-platform](https://noaa.maps.arcgis.com/home/search.html?q=owner%3Ancei_noaa&t=content&start=1&sortOrder=desc&sortField=modified&focus=layers) and its [TDS Catalog](https://www.ncei.noaa.gov/thredds/catalog/catalog.html)
* [OpenStreetMap](https://www.openstreetmap.org) data extractions are available at [https://download.geofabrik.de/](https://download.geofabrik.de/)
* Satellite imagery is available at
    - the [USGS' Earth Explorer](https://earthexplorer.usgs.gov/)
    - the [ESA's Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) (Sentinel-1/2/3/5P; this replaced the former Copernicus Open Access Hub / *SciHub*, which was decommissioned on 2 November 2023)
    - [planet.com](https://www.planet.com/products/monitoring/) (commercial)
* [LiDAR](https://oceanservice.noaa.gov/facts/lidar.html) data can be found at [opentopography.org](https://opentopography.org/).
* Climatological data are provided by [NASA Earth Observations (NEO)](https://neo.gsfc.nasa.gov/).
* Meteorological (e.g., temperature or precipitation) and real-time satellite data are available at [wunderground.com](https://www.wunderground.com/) and its [wundermap](https://www.wunderground.com/wundermap).
* Climate and meteorological data and forecasts are available at [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu), including, for example, ERA5 monthly averaged temperature data
* Data on land use (including canopy cover), socioeconomic characteristics, and global change are available at the [FAO Map Catalog (GeoNetwork)](https://data.apps.fao.org/map/catalog/srv/eng/catalog.search) or the archived ISCGM Global Map portal ([go to their GitHub archive](https://globalmaps.github.io/)).
* Topographical data  (1 to 5-m resolution) from the state of Bavaria, Germany, can be found at [https://www.ldbv.bayern.de](https://www.ldbv.bayern.de/produkte/3dprodukte/gelaende.html).
* Topographical data from EU countries can be found at [https://www.mapsforeurope.org](https://www.mapsforeurope.org/datasets/euro-dem).

## Visualisierung
GIS-Software wird benötigt, um geospatiale Daten anzuzeigen und viele Werkzeuge existieren. Diese Website bietet in erster Linie Beispiele mit {ref}`qgis-install`. Da die Verwendung von GIS-Software, insbesondere *QGIS*, für mehrere Abschnitte in diesem eBook erforderlich ist, sind bereits Erläuterungen zur Installation von *QGIS* in der {ref}`chpt-geo-software` enthalten.

```{tip}
Die {ref}`qgis-tutorial` bietet die Grundlagen der Geospatialdatenverarbeitung mit {ref}`qgis-install`.
```

(gdb)=
## Geodatenbasis
Eine Geodatenbasis (auch bekannt als *spatiale Datenbank*) kann speichern, abfragen (z.B. mit [Structured Query Language SQL](https://en.wikibooks.org/wiki/Structured_Query_Language)) oder Daten mit geographischen Referenzen modifizieren (*geospatial data*). Geospatiale Daten bestehen in erster Linie aus Vektordaten (siehe Formdateien), können aber auch Rasterdaten implementiert werden. Eine Geodatenbank verknüpft diese Daten mit Attributtabellen und geographischen Koordinaten. Eine Besonderheit der Geodatenbanken besteht darin, dass sie über einen (Web- oder lokale) GIS-Server (geografisches Informationssystem) visualisiert und manipuliert werden können. So können beispielsweise Software wie {ref}`qgis-install` (oder *ArcGIS Pro*) Karten erstellen und Abfragen auf einem lokalen Server unter Verwendung von lokal gespeicherten Geodaten vornehmen. Das typische Geodatenbasisformat ist `.gdb`, das als Verzeichnis in {ref}`qgis-install` oder *ArcGIS* fungiert, und die maximale Größe einer `.gdb`Datei beträgt 1 Terabyte.

```{figure} ../img/geo-database.png
:alt: gdb

Das funktionale Skelett einer Geodatenbank.
```

(vector)=
## Vector Data

Vektordaten sind optisch glatt und effizient für Overlay-Operationen, insbesondere in Bezug auf formgetriebene Geoinformationen wie Straßen oder Oberflächendelineationen. Vektordaten zeichnen sich dadurch aus, dass sie wenig speicherintensive, einfach skaliert und mit relationalen Umgebungen kompatibel sind. Gemeinsame Formate sind `.shp`, `JSON` oder `TIN`.

 The shapefile format was invented by *Esri* in the early 1990s (the original [shapefile technical description (PDF)](https://www.esri.com/content/dam/esrisites/sitecore-archive/Files/Pdfs/library/whitepapers/pdfs/shapefile.pdf) remains the authoritative reference) and information contained in a shapefile can be:

* Polygone (Flächen),
* Punkte mit x-y-z-Koordinaten und ein *m*-Feld mit Punktdaten und
* (Poly) Linien aus Linien, die durch Startpunkte und Endpunkte definiert sind.

(shp)=
### Formblatt

```{note}
Der `gdal.ogr` Treibername für Shapefile Handling ist `ogr.GetDriverByName('ESRI Shapefile')`.
```

Eine Shapefile besteht aus mehreren Dateien auf der Festplatte mit folgenden wesentlichen Teilen:

* eine `.shp`-Datei, in der Geometrien gespeichert sind,
* eine `.shx`-Datei, in der Indizes der Geometrien gespeichert sind,
* eine `.prj`-Datei, die die Projektion speichert und
* eine `.dbf`-Datei mit Attributinformationen (entspricht der Attributtabelle).

These files need to be in the same folder - otherwise, the shapefile is incomplete and does not work (correctly). A couple of other files may occur when we manipulate a shapefile (e.g., `.atx`, `.sb*`, `.shp.xml`, `.cpg`, `.mxs`, `.ai*`, or `.fb*`), but we can ignore those files.

Shapefile Vektordaten haben typischerweise eine Attributtabelle (genau wie jede andere Geodatenbank), in der jedem Polygon, Zeile oder Punktobjekt ein Attributwert zugewiesen werden kann. Attribute werden durch Spalten zusammen mit ihren Namen (Spaltenköpfe) definiert und können numerisch (z.B. *float*, *double*, *int* oder *long*), Text (*string*) oder Datum/Zeit (z.B. *yyyymmd* oder *HH:MM:SS*) Formate haben.

```{figure} ../img/geo-shp-illu.png
:alt: shp-illu

Abbildung von Punkt (rot), (Poly) Linie (grün), und Polygon (blau) Formdatei Features.
```

### Shapefile versus Geodatabase
Eine Formdatei kann als konkurrierendes Format einer Geodatenbank verstanden werden. Welches Dateiformat ist besser? Streng genommen können sowohl eine Geodatenbank als auch eine Formdatei ähnliche Operationen ausführen, aber eine Formdatei benötigt mehr Speicherplatz, um ähnliche Inhalte zu speichern, kann keine kombinierten Datums- und Zeitfelder speichern und unterstützt keine Rasterdaten oder *Null* (*not-a-number*) Werte. Shapefiles sind auch auf 2 GB pro Komponentendatei, Attributnamen von 10 Zeichen oder weniger und Textfelder von 255 Zeichen oder weniger beschränkt. So haben Geodatenbasen (und das tragbarere {ref}`GeoPackage <gpkg>` Format) einen technischen Vorteil gegenüber Formdateien, aber die Verwendung von Formdateien ist immer noch beliebt und viele ältere geospatiale Workflows konzentrieren sich auf Shapefile Manipulationen.

(tin)=
### Triangulated Unegular Network (TIN)

A triangulated irregular network (TIN) represents a surface composed of multiple triangles. In hydraulic engineering and water resources research, one of the most important uses of a TIN is the generation of computational meshes for numerical models (read more in the {ref}`chpt-basement` tutorial, for example). In such models, a TIN consists of lines and nodes forming georeferenced, three-dimensionally sloped triangles of the surface, which represent a digital elevation model (DEM). TIN nodes have georeferenced coordinates and potentially more attribute information such as node IDs and elevation. The advantage of a TIN DEM over a raster (see below) DEM is that it requires less storage space. However, manipulating a TIN is not as straightforward as manipulating a raster. The below figure shows an example TIN created with [`matplotlib.tri.TriAnalyzer`](https://matplotlib.org/stable/api/tri_api.html#matplotlib.tri.TriAnalyzer), and based on a [showcase from the matplotlib docs](https://matplotlib.org/stable/gallery/images_contours_and_fields/tricontour_smooth_delaunay.html). The file ending of a TIN is `.tin`.

```{figure} ../img/geo-tin.png
:alt: tin-illu

Illustration einer TIN.
```

(geojson)=
### GeoJSON

```{note}
Der `gdal.ogr` Treibername für GeoJSON Handling ist `ogr.GetDriverByName('GeoJSON')`.
```

[GeoJSON](https://geojson.org/) ist ein offenes Format für die Darstellung geografischer Daten mit einfachen Funktionszugriffsstandards, wobei *JSON* *JavaScript Object Notation* (weitere Informationen zu {ref}`json`Dateimanipulation in den Python-Grundlagen) bedeutet. GeoJSON ist standardisiert als [RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946). Der GeoJSON-Dateiname ist `.geojson` und eine Datei hat typischerweise die folgende Struktur:

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

Während GeoJSON-Metadaten Höheninformationen (`z`-Werte) als `properties`-Wert bereitstellen können, gibt es einen geeigneteren Nachwuchs, um geospatiale Topologie in Form des [TopoJSON](https://github.com/topojson/topojson/wiki)-Formats zu kodieren. Um GeoJSON-Dateien mit Python zu manipulieren, gehen Sie auf den Abschnitt {ref}`geojson-pckg`. Um eine angepasste GeoJSON-Datei zu erstellen, besuchen Sie [geojson.io](https://geojson.io/).

(gpkg)=
## GeoPackage (GPKG)

```{note}
Der `gdal.ogr` Treibername für GeoPackage Handling ist `ogr.GetDriverByName('GPKG')`. Der gleiche `GPKG`-Treiber in GDAL übernimmt auch Rasterfliesen (siehe die [GDAL GPKG vector](https://gdal.org/en/stable/drivers/vector/gpkg.html) und [GDAL GPKG raster](https://gdal.org/en/stable/drivers/raster/gpkg.html) docs).
```

[GeoPackage](https://www.geopackage.org/) (`.gpkg`) ist ein offenes, plattformunabhängiges, standardbasiertes Geospatial-Datenformat, das vom [Open Geospatial Consortium (OGC)](https://www.ogc.org/) (OGC Standard 12-128r19) veröffentlicht wird. Technisch ist ein GeoPackage eine einzige [SQLite](https://www.sqlite.org/)3 Datenbankdatei, die der GeoPackage-Spezifikation folgt, was bedeutet, dass es neben GIS-Software wie {ref}`QGIS <qgis-install>` mit jedem SQLite-Aware-Tool geöffnet, abgefragt und modifiziert werden kann.

Im Gegensatz zu einer {ref}`shapefile <shp>` (die wirklich ein kleines Paket von Sidecar-Dateien ist), ist eine GeoPackage * eine einzelne Datei*, die gleichzeitig enthalten kann:

* Mehrere **vector** Schichten (Punkte, Linien, Polygone, Mischgeometrie) in einem Behälter,
* **Raster** Fliesenpyramiden (z.B. {term}`GeoTIFF`-Stil-Bilder oder DEMs),
* **Beitragstabellen* ohne Geometrie,
* **Spatial-Indizes* (R-tree) für schnelle räumliche Abfragen,
**Metadata** und Styles.

### Warum ein GeoPackage anstelle einer Formdatei verwenden?

Im Vergleich zur Legacy Shapefile entfernt das GeoPackage-Format die meisten bekannten Einschränkungen der Shapefile:

Objekt | Shapefile | GeoPackage |
|----------
| Anzahl der Dateien pro Datensatz | Mindestens 3 (`.shp`, `.shx`,`.dbf`, plus`.prj`,`.cpg`, ...) | 1 (`.gpkg`) |
| Anzahl der Schichten pro Datei | 1 | Viele (Vektor und Raster gemischt) |
| Maximale Größe | 2 GB pro Komponente Datei | ~140 TB (SQLite Limit) |
| Feldname Länge | ≤ 10 Zeichen | Unbegrenzt (praktisch) |
| Textfeldlänge | ≤ 255 Zeichen | Unbegrenzt (TEXT) |
| Zeichencodierung | Code-Seite abhängig (`.cpg`) | UTF-8 (vollständiger Unicode) |
Datums-/Zeitdatentyp | Datum nur | Vollständig`DATETIME` |
| Null / NaN Werte | Nicht unterstützt | Unterstützt |
| Spatial index | External (`.sbn`/`.sbx`) | Eingebauter R-Tree |
| Raster-Unterstützung | Nein | Ja (gekippt) |
| Standardisierung | De-facto (Esri Whitepaper) | Open OGC Standard |

### Lesen und Schreiben eines GeoPackage mit Python

GeoPackage wird von GDAL/OGR, [Fiona](https://fiona.readthedocs.io/), [geopandas](https://geopandas.org/), und [rasterio](https://rasterio.readthedocs.io/). Eine typische Rundreise mit *geopandas* sieht aus wie:

```python
import geopandas as gpd

# Read a specific layer from a GeoPackage
gdf = gpd.read_file("rivers.gpkg", layer="centerlines")

# Write (or append) another layer into the same .gpkg
gdf.to_file("rivers.gpkg", layer="centerlines_buffered", driver="GPKG")
```

Zur Auflistung aller in einem GeoPackage enthaltenen Schichten:

```python
import fiona
print(fiona.listlayers("rivers.gpkg"))
```

Da eine GeoPackage eine SQLite-Datenbank ist, können Attributabfragen auch direkt über SQL ausgegeben werden:

```python
import sqlite3
con = sqlite3.connect("rivers.gpkg")
for row in con.execute("SELECT name, length_m FROM centerlines WHERE length_m > 1000"):
    print(row)
```

```{tip}
Für neue Projekte in der {ref}`qgis-tutorial` und der {ref}`Geospatial Python tutorials <sec-geo-python>` bevorzugen **GeoPackage über Shapefile**. QGIS verwendet sogar GeoPackage als Standard-Saving-Format, wenn Sie eine neue Vektor-Schicht durch *Layer* > *Create Layer* > *Neue GeoPackage-Schicht erstellen...*.
```

(raster)=
## Gridded Cell (Raster) Daten
Raster datasets store pixel values (*cells*), which require large storage space, but have a simple structure. Another big advantage of rasters is the possibility to perform geospatial algebra and statistical analyses. Common raster dataset formats are, among others, `.tif` ({term}`GeoTIFF`), *GRID* (a folder with `BND`, `HDR`, `STA`, `VAT`, and other files), `.flt` (floating points), {term}`ASCII` (American Standard Code for Information Interchange), and many more image-like file types.

```{tip}
Verwenden Sie vorzugsweise das {term}`GeoTIFF`-Format für Rasteranalysen. Eine GeoTIFF-Datei enthält in der Regel eine `.tif`-Datei (mit schweren Daten) und eine `.tfw` (eine 6-line-Datei mit Georeferenzinformationen)-Datei.
```

```{note}
Der `gdal`Treibername für {term}`GeoTIFF` Handling ist `gdal.GetDriverByName('GTiff')`.
```

```{figure} ../img/geo-raster-illu.png
:alt: raster-illu

Abbildung des NE1 50M SR W.tif-Rasters, der auf Nepal gezoomt wurde, mit Punkt- und Linienformdateien, die größere Städte bzw. Ländergrenzen angeben. Beachten Sie das fliesenartige Erscheinungsbild des Rasters, bei dem jede Kachel einer 50m-x-50m Rasterzelle entspricht.
```

## Lidar und Unterwasser Digitale Aufzugsmodelle (Bathymetrien)

Terrain-Erhebungsdaten werden oft in Form eines x-y-z-Punkt-Datensatzes zusammen mit Punktatparametern geliefert. Dreidimensionale Datensätze der bloßen Erdoberfläche werden als Digital Elevation Model bezeichnet (lesen Sie mehr über **{term}`DEM`** Terminologie im Glossar), das die Basis für jede physikalische Analyse eines Flussökosystems darstellt. Die Unterwassertopographie wird als **Badymetrie* eines Flusses oder eines anderen Wasserkörpers bezeichnet. Heutzutage stammen x-y-z-Punktwolken zur Generierung einer Digitales Oberflächenmodell (DOM) meist aus {term}`Lidar`, kombiniert mit {term}`Echo sounder`-Umfragen. Ältere Ansätze verlassen sich auf manuelle Vermessung (z.B. mit einer Gesamtstation) von Querschnitts-Flussprofilen und interpolieren das Gelände zwischen den Profilen. Die neuere {term}`Lidar`-Technik verwendet Lichtquellen und liefert Badedaten bis zu 2-m tiefes Wasser in Form von `*.las` oder das Reißverschlussformular `*.laz`-Dateien. Tiefere Gewässer werden mit einem {term}`Echo sounder` kartiert und die zusammengeführten {term}`Lidar`- und Echo-Sounding-Datensätze produzieren nahtlose Punktwolken von Flussökosystemen, die in verschiedenen Dateitypen gespeichert werden können.

{term}`Lidar` erzeugt massive Punktwolken, die auch leistungsstarke Computer schnell überladen. Deshalb müssen in der Praxis {term}`Lidar`-Daten in kleinere Zonen von weniger als 10<sup>6</sup>-Punkten aufgegliedert werden. Besondere {term}`Lidar` Verarbeitungssoftware (z.B. [LAStools](http://lastools.org/)) ist dabei hilfreich.


(prj)=
## Projekte und Koordinatensysteme
Bei georäumlichen Datenanalysen stellt eine Projektion einen Ansatz dar, um den Globus (ein Teil) zu flachen. In diesem Abflachungsprozess werden auf die Koordinaten einer zweidimensionalen (2d) Karte latitudinale (Nord/Süd) und longitudinale (West/Ost) Koordinaten eines Ortes auf der Welt (dreidimensional - 3d) projiziert. Werden 3d-Koordinaten auf 2d-Koordinaten projiziert, treten Verzerrungen auf und in geospatialen Analysen werden unterschiedliche Projektionssysteme eingesetzt. In der Praxis bedeutet dies, dass, wenn wir geospatiale Datendateien mit unterschiedlichen Projektionen verwenden, sich ein Verzerrungseffekt in alle nachfolgenden Berechnungen ausbreitet. Es ist entscheidend, solche Verzerrungseffekte zu vermeiden, indem sichergestellt wird, dass das gleiche Projektions- und Koordinatenreferenzsystem (Koordinatenreferenzsystem) konsequent auf alle geospatialen Daten angewendet wird. Dies beginnt mit der Schaffung einer neuen geospatialen Schicht (z.B. einer Punktvektorformdatei oder {ref}`GeoPackage <gpkg>`) in {ref}`QGIS (get installation instructions) <qgis-install>` und sollte konsequent in allen Programmcodes verwendet werden. Um ein Koordinatenreferenzsystem anzugeben; z.B. in **QGIS** (tutorial in the {ref}`next section <qgis-tutorial>`), klicken Sie auf **Projekt*** > **Properties**** **Koordinatenreferenzsystem**-Tab und wählen Sie eine `COORDINATE_SYSTEM`. Ein geeignetes Koordinatensystem für Mitteleuropa ist z.B. `ESRI:31493` (weitere Informationen finden Sie in der [QGIS docs](https://docs.qgis.org/latest/en/docs/user_manual/working_with_projections/working_with_projections.html)). Die projizierten Systeme variieren mit der Region (*lokale Koordinatensysteme*), die beispielsweise unter [epsg.io](https://epsg.io/) oder [spatialreference.org](https://spatialreference.org/).

In **shapefiles* werden Informationen über die Projektion in einer `.prj`-Datei gespeichert (Recall-Definitionen in der {ref}`shapefile section <shp>`), die eine einfache Textdatei ist. Das Open Geospatial Consortium (*OGC*) und Esri verwenden [*Well-Known Text* (**WKT*)](https://docs.ogc.org/is/18-010r11/18-010r11.html)-Dateien für Standardbeschreibungen von Koordinatensystemen und eine WKT-formatierte `.prj`-Datei wird im folgenden Codeblock angezeigt. Die in der WKT-formatierten `.prj`-Datei definierten Einheiten und Maßnahmen bestimmen auch die Einheiten von *WK*B*** (*Well-Known Binary*) Definitionen von Geometrien wie Linienlänge (z.B. in Metern, Füße oder vieles mehr) oder Polygonfläche (Quadratmeter, Quadratkilometer, Acres und vieles mehr).


```python
PROJCS["unknown",GEOGCS["GCS_unknown",
                        DATUM["D_Unknown_based_on_GRS80_ellipsoid",SPHEROID["GRS_1980",6378137.0,298.257222101]],
                        PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],
       PROJECTION["Lambert_Conformal_Conic"], PARAMETER["False_Easting",6561666.66666667],
       ..., UNIT["US survey foot",0.304800609601219]]
```

In {ref}`geojson`-Dateien ist das Standard-Koordinaten-Referenzsystem **WGS 84** (Länge/Länge, [EPSG:4326](https://epsg.io/4326)), wie es von [RFC 7946 §4](https://datatracker.ietf.org/doc/html/rfc7946#section-4).


```{admonition} Use EPSG:3857
:class: tip

Um sicherzustellen, dass alle Geometrien in Metern und Meternstärken gemessen werden, verwenden Sie [**EPSG:3857*](https://epsg.io/3857) (die *Web Mercator*-Projektion, die von den meisten Online-Kartendiensten verwendet wird; früher bekannt als `EPSG:900913` -- *g00glE*) zur Definition der WKT-formatierten Projektionsdatei.
```
