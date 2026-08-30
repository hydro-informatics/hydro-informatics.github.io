---
description: Anfänger QGIS Tutorial mit Video-Anleitung zum Laden, Visualisieren und Analysieren von Geodaten einschließlich Shapefiles und Rastern für die Wasserressourcentechnik.
---

(qgis-tutorial)=
# QGIS Tutorial

````{admonition} Requirements
This tutorial is designed for **beginners** and has embedded videos featuring the text descriptions in every section. Before diving into this tutorial make sure to install {ref}`QGIS <qgis-install>`.


```{admonition} Expand to watch the video for installing QGIS
:class: dropdown, tip
Find for explanation in the {ref}`qgis-install` section in this eBook.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/_0_NOKi-RxY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

```

```{admonition} If you read: *Videos not showing up (Firefox Can’t Open This Page)*...
:class: attention, dropdown
Wenn Videos nicht angezeigt werden, kann dies durch strenge Datenschutzeinstellungen verursacht werden. Um das Problem zu beheben, öffnen Sie entweder die Videolinks, indem Sie auf die Schaltfläche **Seite öffnen in Neuem Fenster** klicken oder indem Sie die Datenschutzeinstellungen des Browsers ändern (z. B. in [Mozilla Firefox](https://support.mozilla.org/en-US/questions/1108783)].
```
````

(qgis-project)=
## Erstes Projekt

Sobald Sie QGIS installiert haben, starten Sie das Programm und gehen Sie durch die folgenden Schritte, um grundlegende Einstellungen vorzunehmen:

- Offen *QGIS*
- Erstellen Sie ein neues Projekt (**New Empty Project**)
- Überprüfen Sie **Project Properties**:
  * Im oberen Menü gehen Sie zu **Projekt** > **Eigenschaften**
  * Stellen Sie das Koordinatenreferenzsystem **Koordinatenreferenzsystem** auf **EPSG:4326** ein:
    * WGS84 (Koordinatenreferenzsystem): -180.0000, -90.0000, 180.0000, 90.0000
    * Projizierte Hunde: -180.0000, -90.0000, 180.0000, 90.0000
    * Scope: Horizontale Komponente eines 3D-Systems. Wird vom GPS-Satellitennavigationssystem und für die militärische geodätische Vermessung der NATO verwendet.
    * Zuletzt überarbeitet: 27. August 2007
    * Gebiet: Welt
  * Erfahren Sie mehr unter http://epsg.io
    * Abrufpunktkoordinaten in jedem Koordinatenreferenzsystem-Format
    * Konvertieren zwischen verschiedenen Koordinatenreferenzsystem (z. B. Konvertieren 48.745, 9.103 von EPSG 3857 in EPSG 4326)
- ** Speichern Sie das Projekt als **qgis-project.qgz** in einem neuen **qgis-Übungs-Ordner

```{admonition} Project setup (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/7_3QqbFonLg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

```{hint}
Alle in diesem Tutorial erstellten Dateien können aus dem [QGIS tutorial repository](https://github.com/Ecohydraulics/qgis-tutorial)] heruntergeladen werden.
```

(qgis-tbx-install)=
## Panels, Toolbars und Plugins

Befolgen Sie die unten dargestellten Anweisungen, um die *QGIS * *Toolbox * zu aktivieren.

```{figure} ../img/qgis-tbx.png
:alt: enable QGIS toolbox
:name: qgis-tbx

Öffnen Sie das Toolbox-Fenster von QGIS aus dem Hauptmenü.
```

Zusätzlich ist die **Digitizing Toolbar** (**View** > **Toolbars** > check **Digitizing Toolbar**) erforderlich, um dieses Tutorial abzuschließen.

Die Konvertierung zwischen Geodatentypen und numerischen (Rechen-)Gittern kann mit Plugins erleichtert werden. Um ein Plugin in QGIS zu installieren, gehen Sie zum Menü **Plugins ** > ** Plugins verwalten und installieren...** > **Alle ** Registerkarte > **Search...** für ein relevantes Plugin und installieren Sie es.

Im Rahmen der Flussanalyse werden die folgenden Plugins empfohlen und an mehreren Stellen auf dieser Website verwendet:

```{admonition} QGIS plugins for hydro-informatics
:name: qgis-plugins
* Das *Crayfish* Plugin zur Nachbearbeitung der numerischen Modellausgabe.
* The *BASEmesh2* plugin provides routines for creating computational meshes for numerical simulations with {ref}`chpt-basement`.
* The *PostTelemac* plugin enables geospatial visualization and conversions of numerical model results produced with {ref}`chpt-telemac`.
```

BASEmesh ist nur ein (sehr gut funktionierender) Mesh-Generator für QGIS und {numref}`Tab. %s <tab-mesh-plugins>` Listen anderer Plugins zur Generierung von Rechenmaschen für numerische Modelle zusammen mit Zieldateiformaten und Modellen.

````{admonition} Mesh generators
:class: full-width

```{list-table} A list of QGIS mesh generator plugins.
:header-rows: 1
:name: tab-mesh-plugins

* - Mesh Plugin Name und Link
  - Modellkompatibilität
  - Output Mesh Dateiformat
  - Maschenmerkmale
* - [GMSH](http://geuz.org/gmsh) (Wiki](https://github.com/ccorail/qgis-gmsh/wiki))]
  - [Open CASCADE Technology](https://www.opencascade.com/open-cascade-technology/) / {ref}`OpenFOAM <openfoam-install>`]
  - `*.geo`, `*.stl`, `*.msh`
  - 3d endliche Elemente ([Netgen](http://ngsolve.org/) und [Mmg3d](https://www.mmgtools.org/)]), Kompatibilität mit {ref}`salome-install`
* - [QGribDownloader](https://plugins.qgis.org/plugins/gribdownloader/)]
  - [OpenGribs / XyGrib](https://opengribs.org/)]
  - `*.GRIB`
  - Zweck: meteorologische/atmosphärische Modellierung
* - [TUFLOW](https://plugins.qgis.org/plugins/tuflow/)
  - [TUFLOW](https://tuflow.com/)(proprietär)]
  - `*.2dm` (unter anderem), Konvertierung zu `.slf` möglich mit Crayfish
  - TUFLOW erzeugt automatisch Meshes (endliche Volumina / endliche Differenzen)
* - [MeshTools](https://github.com/jdugge/MeshTools)]
  - {ref}`chpt-basement`, Hydro FT/AS (proprietär), indirekt: {ref}`chpt-telemac`
  - `*.2dm` (Konvertierung zu `.slf` möglich mit Crayfish)
  - Tweaks into multiple mesh algorithms (among others: {cite:t}`shewchuk1996`)
* - DEMto3D
  - Raster zu STL (Style) Dateien für Blender
  - `*.geo`, `*.stl`, `*.msh`
  - Digitale Zwillinge in Blender erstellen
```
````

(basemap)=
## Basemaps für QGIS (Google oder Open Street Maps Worldmap Tiles)

```{note}
Eine schnelle Internetverbindung ist erforderlich, um Online-Basemaps hinzuzufügen.
```

Um eine Basiskarte (z. B. Satellitendaten, Straßen oder Verwaltungsgrenzen) hinzuzufügen, gehen Sie zum **Browser**, klicken Sie mit der rechten Maustaste auf **XYZ Tiles**, wählen Sie **New Connection...**, fügen Sie einen Namen und eine URL einer Online-Basiskarte hinzu. Sobald die neue Verbindung hinzugefügt wurde, kann sie wie jede andere Geodatenschicht per Drag & Drop zu einem *QGIS*-Projekt hinzugefügt werden. Die folgende Abbildung veranschaulicht den Vorgang des Hinzufügens einer neuen Verbindung und ihrer XYZ-Kacheln als Schicht zum Projekt. Um mehrere Basemaps (oder eine andere Ebene) zu überlagern, **klicken Sie mit der rechten Maustaste auf eine Ebene**, dann **Layer Properties** > **Transparenz** > Ändern der **Opacity** (z.B. auf 50%).

```{figure} ../img/qgis-basemap.png
:alt: basemap

Fügen Sie eine Basiskarte zu QGIS hinzu: (1) Suchen Sie den Browser (2) mit der rechten Maustaste auf XYZ-Tiles und wählen Sie Neue Verbindung aus ... (3) Geben Sie einen Namen und eine URL (siehe Tabelle unten) für die neue Verbindung ein, klicken Sie auf OK (4) ziehen Sie die neue Kachel (hier: Google Satellite) in das Layers Panel.
```

```{admonition} Expand to watch the video tutorial on basemaps
:class: tip, dropdown

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/GJsiEdMzCeQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Die folgende URL kann zum Abrufen von Online-XYZ-Kacheln verwendet werden (mehr URLs finden Sie im Internet).

````{admonition} Basemap providers
:class: full-width

```{list-table} Providers of XYZ basemap tiles
:header-rows: 1
:name: basemap-providers

* - Anbieter (Layer Name)
  - URL
* - Bing Satellitenbilder
  - https://t0.tiles.virtualearth.net/tiles/a{q}.jpeg?g=685&mkt=en-us&n=z
* - ESRI World Bilder
  - https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
* - ESRI Street
  - https://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}
* - ESRI Topo
  - https://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}
* - Google Satellit
  - https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}
* - Google Street
  - https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}
* - OpenStreetMap (OSM)
  - http://tile.openstreetmap.org/{z}/{x}/{y}.png
* - OSM Schwarz und Weiß
  - http://tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png
```
````

```{admonition} Coordinate reference systems of basemaps
:class: tip

Die meisten Basemaps werden im `EPSG:3857 -WGS84` / `Pseudo Mercator` Koordinatensystem (Koordinatenreferenzsystem) bereitgestellt. Um benutzerdefinierte Geodatenprodukte zu verwenden, stellen Sie sicher, dass alle anderen Schichten das gleiche Koordinatensystem haben. Lesen Sie mehr über Koordinatensysteme und Projektionen in den Abschnitten {ref}`geospatial-data` und {ref}`shapefile projection <prj-shp>`.
```

## Erstellen Sie ein Shapefile

This section guides through the creation of a point, a line, and a polygon {ref}`shp` (vector data). To read more about such vector data and other spatially explicit data types, read the section on {ref}`geospatial-data`.

(create-point-shp)=
### Erstellen Sie ein Point Shapefile

Beginnen Sie mit dem Laden von Satellitenbildern und einer Straßenbasiskarte (siehe oben) in den Schichten. Zoomen Sie auf Mitteleuropa und finden Sie Stuttgart in Südwestdeutschland. Finden Sie den stark beeinträchtigten Neckar im Norden Stuttgarts und bewegen Sie sich in stromaufwärts gelegene Richtung (d.h. östliche Richtung), passieren Sie die Städte Esslingen und Plochingen, bis Sie zum Zusammenfluss von Neckar und Fils gelangen. Von dort aus folgen Sie dem Fluss Fils in stromaufwärts gerichtet für ein paar hundert Meter und finden Sie den PEGELHAUS (dh eine Messstation am Fluss Fils - [klicken Sie auf visit](https://www.hvz.baden-wuerttemberg.de/pegel.html?id=00025)]. Um das Finden der Messstation in Zukunft zu erleichtern, erstellen wir nun eine Punktformdatei, wie im folgenden Video und den analogen Anweisungen unter dem Video erläutert.

```{admonition} Create point shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/k2LqPM6wicA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

* Gehen Sie im QGIS-Obermenü zu **Layer** > **Create Layer** > **New Shapefile Layer**
  * Definieren Sie einen Dateinamen (z. B. **gauges.shp** - darf nicht länger als 13 Zeichen sein), z. B. in einem Ordner namens *qgis-exercise *.
  * Geometrietyp: `MultiPoint`
  * Zusätzliche Dimensionen: `Z(+M Values)`
  * Füge zwei neue Felder hinzu:
    * `StnName` (*Textdaten*)
    * `StnID` (*ganze Nummer*)
* Bearbeiten/Zeichnen
  * **Toggle Editing** (d.h. durch Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> aktivieren) > **Digitizing Toolbar** > **Add Point Feature** <img src="../img/qgis/sym-add-point.png">
  * Klicken Sie auf das PEGELHAUS, um einen Punkt zu zeichnen und zu setzen
    * `StnName`: `PlochingenFils`
    * `StnID`: `00025`
  * Fügen Sie weitere Punkte hinzu, wenn Sie möchten.
  * Finalize the edits by clicking on **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> > **Stop (Toggle) Editing** by clicking on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.
* Verbessern Sie die Visualisierung, indem Sie die Symbologie ändern:
  * **Double-click on** the gauges **layer** > **Symbologie**
  * Hervorheben ** Einfache Markierung **, ändern Sie zu ** + ** Symbol und ändern Sie Füllfarbe und Größe.
  * Highlight **Marker** und Ändern der **Opacity**
  * Klicken Sie auf **Apply** und **OK**
* Überprüfen Sie die Punkteinstellungen in der **Attributtabelle** (klicken Sie mit der rechten Maustaste auf die Ebene *gauges* und wählen Sie **Attributtabelle** aus).

(create-line-shp)=
### Erstellen Sie ein Line Shapefile

Erstellen Sie ein **Line Shapefile** namens **CenterLine.shp**, um eine Mittellinie der Fils $\pm$200 m um das PEGELHAUS-Messgerät zu zeichnen, ähnlich dem oben erstellten Punkt-Shapefile. Fügen Sie ein *text * Feld hinzu und rufen Sie es `RiverName` auf. Dann ziehen Sie eine Linie entlang des Fils River, die 200 m stromaufwärts beginnt und 200 m stromabwärts des PEGELHAUS endet, indem Sie dem Fluss auf der **OpenStreetMap**-Schicht folgen. Mehr dazu im folgenden Video.

```{admonition} Create Line shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/yNuiIlPsguQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

(create-polygon-shp)=
### Erstellen Sie ein Polygon Shapefile

Um verschiedene Rauhigkeitszonen abzugrenzen (z. B. für ein zweidimensionales numerisches Modell), erstellen Sie ein **Polygon Shapefile** namens **FlowAreas.shp**. Die Datei enthält Polygone, die den betrachteten Abschnitt der Fils in die Auen- und Hauptkanalbett zonieren. Benennen Sie das erste Feld `AreaType` (Typ: *Text*) und das zweite Feld `ManningN` (Typ: *Dezimalzahl*). Sehen Sie mehr im folgenden Video und den Anweisungen unter dem Video.

```{admonition} Create Polygon video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/zTrowT0ULfo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Um die Polygone zu zeichnen:

* Einrasten ermöglichen, um Lücken zwischen den Auen- und Hauptkanalpolygonen zu vermeiden
  * Aktivieren Sie die **snapping Symbolleiste**: **View** > ** Toolbars** > **Snapping Toolbar**
  * Ermöglichen Sie das Schnappen aus der **Snapping-Symbolleiste ** > **Snapping ** aktivieren und ** Polygonüberlappen vermeiden **
* Um ein Polygon zu zeichnen, gehen Sie zur **Digitalisierungs-Symbolleiste** > **Add Polygon Feature** mit der Option **Digitalisieren mit Segment** aktiviert
* Beginnen Sie mit dem Zeichnen, indem Sie auf die Karte klicken (Rechtsklick schließt Polygon ab)
* Zeichnen Sie ein Polygon des Hauptkanals und nach dem Finalisieren Satz:
  * `AreaType`: `MainChannel`
  * `ManningN`: `0.028`
* Zeichnen Sie zwei weitere Polygone der Auen des rechten Ufers (RB) und des linken Ufers (LB) und setzen Sie:
  * `AreaType`: `FloodPlainRB` und `FloodPlainLB`
  * `ManningN`: `0.05` (beide)
* If you made a drawing error, use either the *Attribute Table* to select and delete entire polygons, or use the vertex tool <img src="../img/qgis/sym-vertex-tool.png"> from the menu bar.
* Nach dem Zeichnen aller Polygone, **Save Edits** und **Toggle Editing** (deaktivieren).
* Um die Visualisierung zu verbessern, ändern Sie die **Symbologie** in **Kategorisiert** als Funktion des Feldes `AreaType`: Behalten Sie **Random Colors** > Klicken Sie auf **Classify** > **Apply** und wenn Ihnen die Visualisierung gefällt, klicken Sie auf **OK**.


## Umwandlung: Rasterize (Polygon zu Raster)

Many numerical models required that roughness is provided in {ref}`raster` format. To this end, this section features the conversion of the above-created polygon shapefile (*FlowAreas.shp*) to a roughness {ref}`raster`. The following video and the instructions below the video describe how the conversion works.

```{admonition} Rasterization video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/IRLwYSUnjcE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Um einen geospatialen Vektordatensatz zu konvertieren, verwenden Sie das Werkzeug *Rasterize*:

* Stellen Sie in der QGIS-Menüleiste sicher, dass Sie das Feld *Processing Toolbox* aktivieren (**View** > **Panels** > **Processing Toolbox**)
* In der **Processing Toolbox** > search (tap) **Rasterize** > select **Rasterize (vektor to raster)**

```{hint}
Wenn das *Crayfish*-Plugin installiert ist, wird ein zusätzliches *Rasterize*-Tool angezeigt, das wir in diesem Tutorial nicht verwenden werden (d. H. Wählen Sie *Rasterize (Vektor zum Raster) * ).
```

* Im Fenster **Rasterize (Vector to Raster)**:
  * **Eingabeschicht**: `FlowAreas`
  * **Feld für einen Burn-In-Wert**: `ManningN`
  * **Ausgaberastergrößeneinheiten**: `Pixels`
  * **Breite/Horizontale Auflösung**: `100` (je kleiner, desto gröber das Raster)
  * **Höhe/Vertikale Auflösung**: `100` (je kleiner, desto gröber das Raster)
  * ... nach unten scrollen ...
  * **Ausgabeumfang**: Klicken Sie auf den **...** Button > **Berechnen aus Layer** > `FlowAreas`
  * **Rasterized** (FILE NAME) > klicken Sie auf den **...** Button > **In Datei speichern...** > `roughness.tif`
  * Klick **Run**
* Stellen Sie die **Symbologie** auf **Singleband pseudocolor** mit **Interpolation**: `Discrete`, **Colorramp**: `Magma`, **Mode**: `Equal Interval` > **Apply**. Wenn die Visualisierung zufriedenstellend ist, klicken Sie auf **OK**.

```{admonition} File conversion with Python
:class: tip
The conversion between geospatial data types can be facilitated by using Python. Read the section on {ref}`py-conversion` to learn more.
```

## Polygon

The inverse operation of *Rasterize* is called **Raster to Vector**, which is documented at [https://docs.qgis.org](https://docs.qgis.org/testing/en/docs/training_manual/complete_analysis/raster_to_vector.html). The creation of a Polygon shapefile from a Raster is described in the video below. The essential steps are:

* Gehen Sie zu **Raster** (Top-Menü) > **Conversion** > **Polygonize (Raster to Vector)...**
* **Eingabeschicht**: Wählen Sie das Raster zum Konvertieren
* **Bandnummer**: das Rasterband zum Rückschluss auf den Polygonwert (d.h. Feld in der Attributtabelle); einige Anmerkungen:
  * Dieser Algorithmus rundet Dezimalzahlen auf Ganzzahlen (siehe Video unten)
  * Alternativ können Sie *Raster-Pixel nach Polygonen * in der *Processing Toolbox * suchen, aber es wird eine übermäßige Anzahl von Polygonen erstellen
* **Name des zu erstellenden Feldes**: Wählen Sie einen Namen für das Polygonwertfeld in der Attributtabelle aus (**nicht mehr als 10 Zeichen**)
* **Vectorized**: Definieren Sie das Verzeichnis und den Namen für die neue Polygon-Shapefile
* Klick **Run**

```{admonition} Polygonize (video)

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/r9MwkKvUD-k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

Holen Sie sich die [**mannings-n GeoTIFF hier**](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/mannings-n.tif).

```


To convert a Raster to a line/point (vector) shapfile, the options are the [Contour](https://docs.qgis.org/3.28/en/docs/training_manual/processing/interp_contour.html) tool (**Raster** menu > **Extraction** > **Contour**) or the [Raster pixels to points](https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorcreation.html#raster-pixels-to-points) algorithm (**Processing** toolbox > enter `raster pixels to points`). Also, have a look at the tutorials on {ref}`geo file conversion with Python <raster2line>`.



## Arbeiten mit Rastern

### QGIS Rasterrechner (Kartenalgebra)

Einige Modelle verwenden vorzugsweise (Standardverwendung) Mannings *n*, andere verwenden den Strickler-Rauheitskoeffizienten $k_{st}$, der das Inverse von Mannings *n* ist (dh $k_{st} = 1/n$ - lesen Sie mehr über Rauheitskoeffizienten in der {ref}`ex-1d-hydraulics` Übung). Daher erfordert die Umwandlung eines Strickler-Rauheitsrasters in ein Manning-Rauheitsraster die Durchführung einer algebraischen Rasteroperation (pixelweise). Das nächste Video und die Anweisungen unter dem Video zeigen die Verwendung des QGIS **Raster Calculators**, um solche algebraischen Operationen durchzuführen.

```{admonition} Raster calculator (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/DOkV03uij9k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Beginnen Sie mit dem Öffnen **Raster Calculator** aus der QGIS-Menüleiste (**Raster** > **Raster Calculator...**). Konvertieren Sie dann das oben erstellte *roughness.tif*-Raster von Mannings *n*-Werten in ein Strickler-Rauheitsraster:

* Definieren Sie eine **Output-Schicht ** (z. B. *qgis-übung/roughness-stickler.tif *) und behalten Sie das **Output-Format ** von **{term}`GeoTIFF`** bei.
* Optional wählen Sie eine Schichtausdehnung entsprechend dem oben erstellten *roughness.tif* Raster.
* Im **Raster Calculator Expression** Frame Typ **1** klicken Sie dann auf den **/** Button (**Operators** Frame), dann wählen Sie **roughness@1** aus dem **Raster Bands** Frame.
* Der **Raster Calculator Expression**-Rahmen sollte nun Folgendes enthalten: `1 / "roughness@1"`, wobei sich das `@`-Zeichen auf die Bandnummer `1` bezieht.
* Klicken Sie auf **OK**, um den *Raster Calculator* auszuführen.
* Nach erfolgreicher Berechnung optional die Symbologie der neuen Schicht ändern (*rauhigkeitskleber*).

```{admonition} Batch-process geodata
:class: tip
To implement a tailored raster calculator for batch-processing of raster files with Python read the {ref}`py-raster-calculator` section in the {ref}`ex-geco` exercise.
```

(make-xyz)=
### Raster nach XYZ

Scientific data formats, such as {term}`HDF`, work best with raw geospatial datasets like `*.xyz` files. A `.*xyz` file contains s only X, Y, and Z coordinates of points (i.e., point clouds) with or without a simple header. For instance, this eBook uses `*.xyz` data for the elevation interpolation of a computational mesh for the scientific numerical modeling software {ref}`chpt-telemac`. To generate a `*.xyz` from a {term}`GeoTIFF` raster use the following workflow:

* Stellen Sie im **Layers**-Bereich sicher, dass die Rasterschicht zur Konvertierung importiert wird, und **identifizieren Sie den No-Data**-Wert (**Layer Properties** > **Information** > **Bands**-Bereich > **No-Data**-Feld standardmäßig `-9999` in QGIS).
* Gehen Sie im QGIS-Obermenü zu **Raster** > **Conversion** > **Translate (Convert Format)...**
* Führen Sie im Fenster **Übersetzen (Konvertieren Format)** die folgenden Einstellungen aus:
  * **Eingabeschicht** = das Raster (z.B. ein {term}`Digitales Oberflächenmodell <DEM>`), das konvertiert werden soll
  * **Advanced Parameters** frame > **Outputdatentyp** > select **Float32** (entspricht Einzelpräzision in numerischen Modellen)
  * **Konvertiert** > **...** Button (am Ende der Zeile) > **In Datei speichern...** > Definieren Sie einen **Dateinamen** wie `dem-points` und wählen Sie `XYZ files (*.xyz)` im Feld **Als Typ speichern** aus.
  * ** Speichern** und **Run** die Übersetzung (Konvertierung).

The resulting `*.xyz` file contains also points with **No-Data** to fill void spaces in the rectangular image of the {term}`GeoTIFF` (which QGIS did recognize as no-data pixels). The no-data points may make the `*.xyz` file unnecessarily heavy, in particular, when it is a {term}`Digitales Oberflächenmodell <DEM>` of a near-census natural river. To eliminate the unnecessary no data points, open the `*.xyz` file in spreadsheet software, such as {ref}`Calc in LibreOffice <lo>` and use the *Sort* tool (in **Calc** highlight all points go to **Data** > **Sort...**) to sort by `Z` values (largest to smallest) and then delete all rows that have the above-identified **No-Data** value (`-9999`) as `Z` value. Save the `*.xyz` file and close the spreadsheet software.

```{admonition} Shapefile to XYZ
:class: tip, dropdown
**Shapefiles** müssen nicht in {term}`GeoTIFF` konvertiert werden, um eine `*.xyz`-Datei zu erstellen. Um eine `*.xyz` Datei aus einem **shapefile** zu erstellen:

* Klicken Sie mit der rechten Maustaste auf das Shapefile im **Layer**-Panel > **Export** > **Save Feature As...**.
* Wählen Sie **Comma Separated Value ({term}`CSV`)** im Feld **Format**.
* Definieren Sie einen ** Dateinamen ** beim Klicken auf den **...** Button.
* Wählen Sie im **Layer Options**-Rahmen **AS XYZ** im **GEOMETRY**-Feld und behalten Sie alle anderen Standardwerte bei.
* Klicken Sie auf **OK** um zu {term}`CSV` zu konvertieren.
* Öffnen Sie die {term}`CSV`-Datei in einem {ref}`text editor <npp>` und verwenden Sie die Funktion *finden und ersetzen* (normalerweise `CTRL`+`F` oder `CTRL`+`H`), um alle COMMA `,` durch ein Leerzeichen ` ` zu ersetzen. Beachten Sie, dass diese Aktion erfordert, dass das Komma nicht als Dezimaltrennzeichen verwendet wurde.
* Speichern Sie die {term}`CSV` Datei als `*.xyz` Datei.
```

To finalize the `*.xyz` file, open it in a {ref}`text editor <npp>` and add a header. For instance, use the following header to work with {ref}`Blue Kenue <bluekenue>`:

```
:FileType xyz  ASCII  EnSim 1.0
:EndHeader
```

Rette die Änderungen. Die `*.xyz`-Datei ist jetzt schlank und zum Beispiel für {ref}`TELEMAC pre-processing <get-dem-xyz>` einsatzbereit.

## Erstellen von Layout und PDF / JPG (oder anderen) Maps

Georeferenced images in {term}`GeoTIFF` or other raster formats, possibly with super-positioned shapefiles on top, are handy and flexible for use with geospatial software, such as QGIS, but not appropriate for presentations or reports. For presentation purposes, geospatial imagery or maps should preferably be exported to common formats, such as the **P**ortable **D**ocument **F**ormat (PDF) or **JPEG/JPG**. To create commonly formatted maps with QGIS, first, a new (print) layout needs to be created, which can then be exported to a common map format (e.g., along with a legend, a scale bar, and a North arrow). The following video and the descriptions below the video guide through the map creation process with QGIS.

```{admonition} Layout creation (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/hmTByzVPVF0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Beginnen Sie mit dem Erstellen eines neuen Drucklayouts, indem Sie auf das Dropdown-Menü **Projekt ** klicken und dann **Neues Drucklayout ** auswählen. Im neuen Drucklayout wird die Karte vorbereitet und die Karte wie folgt exportiert:

* Legen Sie einen **Layout-Titel ** fest (z. B. * Übungslayout *).
* Im neuen (*Übungslayout*) Aufbau:
  * Gehen Sie zu **Hinzufügen** > **Hinzufügen Karte**.
  * Zeichne ein Rechteck, das die Karte enthält.
  * **Hinzufügen ** > **Hinzufügen der Skala Bar **
  * Zur Steuerung von Waagen und Einheiten, die in der Skalaleiste dargestellt sind:
    * In **Items** panel, highlight `<Scalebar>` and find the **Item Properties** tab below.
    * In der Registerkarte **Eigenschaften** ändern Sie Einheiten nach Ihrer Bequemlichkeit.
  * **Hinzufügen** > **Hinzufügen Legende**
  * Um Elemente der Legende zu kontrollieren:
    * In **Items** panel, highlight `<Legend>` and find the **Item Properties** tab below.
    * Unter **Eigenschaften** finden Sie **Legend Items** > Deaktivieren **Auto Update** > **Remove** *OpenStreetMap* und *Google Satellite*.
  * Wechseln Sie durch andere **Items** in der **Add Item** Menüleiste (z. B. **Arrow** für Northing).
* ** Speichern Sie das Layout-Projekt (aus dem oberen Menü **Layout** > **Projekt speichern**)
* Exportieren Sie die Karte in gängige Formate:
  * Für JPG oder PNG: **Layout** > **Export als Bild**
  * Für PDF: **Layout** > **Exportieren als PDF**
  * Fakultativ für SVG-Vektorgraphen: **Layout** > **Export als SVG**

QGIS hat viele andere Fähigkeiten, aber dieses grundlegende Tutorial sollte Ihnen das notwendige Wissen vermittelt haben, um die Leistungsfähigkeit von QGIS für viele Anwendungen zu nutzen.

(pygis)=
## PyQGIS: QGIS und Python

Die grafische Benutzeroberfläche (GUI) von QGIS bietet eine Python-Befehlszeile (**Plugins** > **Python Console**), mit der nahezu jeder Mausklick in der GUI automatisiert werden kann. Diese Python-Befehlszeile wird als **PyQGIS** bezeichnet und der [QGIS-Entwickler docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html) bietet Anweisungen zum Importieren und Ausführen von eigenständigen Python-Skripten außerhalb der QGIS-GUI]. Hier ist die grundlegende Python-Vorlage, um ein PyQGIS-Skript auszuführen:


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

Wenn Sie jedoch das Terminal Ihres Systems oder die Anaconda Prompt öffnen, um einen PyQGIS-Code auszuführen, bleiben Sie möglicherweise bereits in der ersten Codezeile stecken: `from qgis.core import *` liefert `ImportError: No module named qgis.core`. Laut [QGIS-Entwickler docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html)] passiert dieser Fehler, weil das Python Ihres Systems nicht weiß, wo sich die PyQGIS-Umgebung befindet. Um Ihr Terminal PyQGIS erkennen zu lassen, ergreifen Sie die folgenden Maßnahmen entsprechend Ihrem System:

`````{tab-set}
````{tab-item} Linux

Öffnen Sie das Terminal und installieren Sie `python-qgis`:

```
sudo apt install python-qgis
```

Versuchen Sie nach der erfolgreichen Installation, ob Sie jetzt `qgis.core` importieren können:

```
USER@computer:~$ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from qgis.core import *
>>> exit()
```

If `from qgis.core import *` did not throw any error, you are all set and can stop reading. **Otherwise**, find and open your `.bashrc` file (Debian/Ubuntu/Mint: `/home/USERNAME/.bashrc`). Note that files starting with a `.` name are hidden on Linux and become visible by toggling with simultaneously pressing the `CTRL`+`H` keys.

At the bottom of `.bashrc` add the following

```
export PYTHONPATH=/<qgispath>/share/qgis/python
```

Der `<qgispath>`-Ausdruck sollte durch den Ort ersetzt werden, an dem die PyQGIS-Umgebung lebt. Um herauszufinden, wo das ist, tippen Sie (im Terminal):

```
dpkg-query -L python-qgis
```

Dies weist darauf hin, wo PyQGIS lebt, was auf Ubuntu / Mint typischerweise ist:

```
/usr/lib/python3/dist-packages/
```

Thus, in this case add to `.bashrc`:

```
export PYTHONPATH=/usr/lib/python3/dist-packages/
```

Afterward, log out and re-login to your system (i.e., reload `.bashrc`). The command `from qgis.core import *` should now work in Python.
````

````{tab-item} Windows

Make sure your system knows the where PyGIS lives by adding the following line to the Environment Variables (Windows 10: **My Computer** > **Properties** > **Advanced System Settings** > **Environment Variables**). Replace `<qgispath>` with the path where QGIS lives on your system.

* Variablenname = `PYTHONPATH`
* Variabler Wert = `C:\<qgispath>\python`

Oder verwenden Sie die Windows-Eingabeaufforderung:

```
set PYTHONPATH=C:\<qgispath>\python
```

````
`````


