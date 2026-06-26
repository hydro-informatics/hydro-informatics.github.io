---
description: Anfänger QGIS Tutorial mit Videoführung zum Laden, Visualisieren und Analysieren von Geospatialdaten einschließlich Formdateien und Raster für die Wasserressourcen-Engineering.
---

(qgis-tutorial)=
# QGIS Tutorial

````{admonition} Requirements
Dieses Tutorial ist für **starters** konzipiert und verfügt über eingebettete Videos mit den Textbeschreibungen in jedem Abschnitt. Vor dem Tauchen in dieses Tutorial stellen Sie sicher, {ref}`QGIS <qgis-install>`.


```{admonition} Expand to watch the video for installing QGIS
:class: dropdown, tip
In diesem eBook finden Sie eine Erläuterung im Abschnitt {ref}`qgis-install`.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/_0_NOKi-RxY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

```

```{admonition} If you read: *Videos not showing up (Firefox Can’t Open This Page)*...
:class: attention, dropdown
Wenn Videos nicht angezeigt werden, könnte dies durch strenge Datenschutzeinstellungen verursacht werden. Um das Problem zu lösen, öffnen Sie entweder die Video-Links, indem Sie auf die **Open Site in New Window** Schaltfläche oder durch Änderung der Browser-Datenschutzeinstellungen (z.B. in [Mozilla Firefox](https://support.mozilla.org/en-US/questions/1108783)) klicken.
```
````

(qgis-project)=
## Erstes Projekt

Sobald Sie QGIS installiert haben, starten Sie das Programm und gehen Sie durch die folgenden Schritte, um grundlegende Einstellungen zu machen:

- *QGIS*
- Ein neues Projekt erstellen (**Neues leeres Projekt**)
- **Projekteigenschaften* überprüfen*:
  * Im oberen Menü gehen Sie zu **Projekt** > **Properties**
  * Richten Sie das Koordinatenreferenzsystem **Koordinatenreferenzsystem** auf **EPSG:4326**:
    * WGS84 (Koordinatenreferenzsystem) Anlagen: -180.0000, -90.0000, 180.0000, 90.0000
    * Projektierte Anlagen: -180.0000, -90.0000, 180.0000, 90.0000
    * Anwendungsbereich: Horizontale Komponente eines 3d-Systems. Verwendet durch das GPS Satellitennavigationssystem und für militärische geodätische Vermessungen der NATO.
    * Zuletzt überarbeitet: 27. August 2007
    * Bereich: Welt
  * Weitere Informationen unter http://epsg.io
    * Abrufpunktkoordinaten in jedem Koordinatenreferenzsystem-Format
    * Konvertiert zwischen verschiedenen Koordinatenreferenzsystem (z.B. Konvertiert 48.745, 9.103 von EPSG 3857 zu EPSG 4326)
- **Save** das Projekt als **qgis-project.qgz** in einem neuen Ordner **qgis-exercise**

```{admonition} Project setup (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/7_3QqbFonLg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

```{hint}
Alle Dateien, die in diesem Tutorial erstellt wurden, können vom [QGIS tutorial repository](https://github.com/Ecohydraulics/qgis-tutorial).
```

(qgis-tbx-install)=
## Panels, Toolbars und Plugins

Folgen Sie den unten dargestellten Anweisungen, um die *QGIS* *Toolbox* zu aktivieren.

```{figure} ../img/qgis-tbx.png
:alt: enable QGIS toolbox
:name: qgis-tbx

Öffnen Sie das Fenster Werkzeugkasten QGIS aus dem Hauptmenü.
```

Darüber hinaus ist die **Digitizing Toolbar** (**Ansicht******* **Toolbars**** überprüfen **Digitizing Toolbar**) erforderlich, um dieses Tutorial abzuschließen.

Die Umwandlung zwischen geospatialen Datentypen und numerischen (computationalen) Gittern kann mit Plugins erleichtert werden. Um ein Plugin in QGIS zu installieren, gehen Sie auf das **Plugins* Menü > **Verwalten und Installieren von Plugins...**** Tab > **Search...*** für ein entsprechendes Plugin und installieren Sie es.

Im Rahmen der Flussanalyse werden folgende Plugins empfohlen und an mehreren Orten auf dieser Website verwendet:

```{admonition} QGIS plugins for hydro-informatics
:name: qgis-plugins
* Das *Crayfish* Plugin zur Nachbearbeitung der numerischen Modellausgabe.
* Das *BASEmesh2* Plugin bietet Routinen für die Erstellung von Rechennetzen für numerische Simulationen mit {ref}`chpt-basement`.
* Das *PostTelemac* Plugin ermöglicht die geospatiale Visualisierung und Konvertierung von numerischen Modellergebnissen mit {ref}`chpt-telemac`.
```

BASEmesh ist nur ein (sehr gut funktionierender) Mesh-Generator für QGIS und {numref}`Tab. %s <tab-mesh-plugins>` Listen anderer Plugins zur Generierung von Rechennetzen für numerische Modelle zusammen mit Zieldateiformaten und -modellen

````{admonition} Mesh generators
:class: full-width

```{list-table} A list of QGIS mesh generator plugins.
:header-rows: 1
:name: tab-mesh-plugins

* - Mesh Plugin Name und Link
  - Modellkompatibilität
  - Ausgabe Mesh Datei Format
  - Mesh Characteristics
* - [GMSH](http://geuz.org/gmsh)[Wiki](https://github.com/ccorail/qgis-gmsh/wiki)]
  - [Open CASCADE Technology](https://www.opencascade.com/open-cascade-technology/) / {ref}`OpenFOAM <openfoam-install>`
  - `*.geo`, `*.stl`, `*.msh`
  - 3d-Finite-Elemente ([Netgen](http://ngsolve.org/) und [Mmg3d](https://www.mmgtools.org/)), Kompatibilität mit {ref}`salome-install`
* - [QGribDownloader](https://plugins.qgis.org/plugins/gribdownloader/)
  - [OpenGribs / XyGrib](https://opengribs.org/)
  - `*.GRIB`
  - Zweck: Meteorologische/atmosphärische Modellierung
* - [TUFLOW](https://plugins.qgis.org/plugins/tuflow/)
  - [TUFLOW](https://tuflow.com/)(proprietär)
  - `*.2dm` (u.a.), Umrechnung auf `.slf` möglich mit Crayfish
  - TUFLOW erzeugt automatisch Maschen (Endvolumen / endliche Unterschiede)
* - [MeshTools](https://github.com/jdugge/MeshTools)
  - {ref}`chpt-basement`, Hydro FT/AS (proprietär), indirekt: {ref}`chpt-telemac`
  - `*.2dm` (Umwandlung an `.slf` möglich mit Crayfish)
  - Tweaks in mehrere Netzalgorithmen (u.a.: {cite:t}`shewchuk1996`)
* - DEMto3D
  - Raster zu STL (Stil) Dateien für Blender
  - `*.geo`, `*.stl`, `*.msh`
  - Digitale Zwillinge in Blender erstellen
```
````

(basemap)=
## Basiskarten für QGIS (Google oder Open Street Maps Worldmap Tiles)

```{note}
Für das Hinzufügen von Online-Basemaps ist eine schnelle Internetverbindung erforderlich.
```

Um eine Basiskarte hinzuzufügen (z.B. Satellitendaten, Straßen oder Verwaltungsgrenzen), gehen Sie zum **Browser**, Rechtsklicken Sie auf **XYZ Tiles*, wählen Sie **New Connection...*, einen Namen hinzufügen und eine URL einer Online-Basiskarte. Sobald die neue Verbindung hinzugefügt wird, kann sie zu einem *QGIS* Projekt hinzugefügt werden, indem sie wie jede andere Geodatenschicht ziehen und fallen. Die nachfolgende Figur zeigt die Prozedur des Hinzufügens einer neuen Verbindung und ihrer XYZ-Fliesen als Schicht zum Projekt. Um mehrere Basemaps (oder jede andere Schicht) zu überlagern, klicken Sie auf eine Schicht**, dann **Layer Properties** > **Transparenz**** die **Opacity** (z.B. auf 50%) ändern.

```{figure} ../img/qgis-basemap.png
:alt: basemap

Fügen Sie eine Basiskarte zu QGIS hinzu: (1) finden Sie den Browser (2) Rechtsklick auf XYZ-Tiles und wählen Sie Neue Verbindung... (3) Geben Sie einen Namen und eine URL (siehe unten Tabelle) für die neue Verbindung ein, klicken Sie auf OK (4) ziehen und fallen Sie die neue Kachel (hier: Google Satellite) in das Layers Panel.
```

```{admonition} Expand to watch the video tutorial on basemaps
:class: tip, dropdown

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/GJsiEdMzCeQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Die folgende URL kann zum Abrufen von Online XYZ-Fliesen verwendet werden (mehr URLs finden Sie im Internet).

````{admonition} Basemap providers
:class: full-width

```{list-table} Providers of XYZ basemap tiles
:header-rows: 1
:name: basemap-providers

* - Anbieter (Layer Name)
  - URL
* - Bing satellite view
  - https://t0.tiles.virtualearth.net/tiles/a{q}.jpeg?g=685&mkt=en-us&n=z
* - ESRI World Images
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

Die meisten Basiskarten werden im Koordinatensystem `EPSG:3857 -WGS84` / `Pseudo Mercator` (Koordinatenreferenzsystem) bereitgestellt. Um benutzerdefinierte Geodaten-Produkte zu verwenden, stellen Sie sicher, dass alle anderen Schichten das gleiche Koordinatensystem haben. Lesen Sie mehr über Koordinatensysteme und Projektionen in den Abschnitten {ref}`geospatial-data` und {ref}`shapefile projection <prj-shp>`.
```

## Erstellen einer Shapefile

Dieser Abschnitt führt durch die Erstellung eines Punktes, einer Zeile und eines Polygons {ref}`shp` (Vektordaten). Um mehr über solche Vektordaten und andere räumlich explizite Datentypen zu erfahren, lesen Sie den Abschnitt unter {ref}`geospatial-data`.

(create-point-shp)=
### Erstellen einer Point Shapefile

Beginnen Sie mit dem Laden von Satellitenbildern und einer Straßenbasiskarte (siehe oben) im Schichtenbereich. Großansicht auf Mitteleuropa und rund um Stuttgart in Südwestdeutschland. Finden Sie den stark beeinträchtigten Neckar-Fluss im Norden von Stuttgart und bewegen Sie sich in die stromaufwärts (d.h. östliche Richtung), durch die Städte Esslingen und Plochingen, bis Sie zum Zusammenfluss des Neckars und der Fils Flüsse gelangen. Von dort aus folgen Sie der Fils-Fluss in der stromaufwärtigen Richtung für ein paar hundert Meter und lokalisieren Sie das PEGELHAUS (d.h. eine gauging-Station an der Fils-Fluss - [click to visit](https://www.hvz.baden-wuerttemberg.de/pegel.html?id=00025)). Um das Finden der Messstation in der Zukunft zu erleichtern, erstellen wir nun eine Punktformdatei, wie sie im folgenden Video und den analogen Anweisungen unter dem Video erläutert wird.

```{admonition} Create point shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/k2LqPM6wicA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

* Im QGIS Top-Menü gehen Sie zu **Layer******Create Layer*********Neue Shapefile Layer*****
  * Definieren Sie einen Dateinamen (z.B. **gauges.shp** - darf nicht länger als 13 Zeichen sein), z.B. in einem Ordner namens *qgis-exercise*.
  * Geometrietyp: `MultiPoint`
  * Zusätzliche Abmessungen: `Z(+M Values)`
  * Zwei neue Felder hinzufügen:
    * `StnName` (*Textdaten*)
    * `StnID` (*Lochnummer*)
* Bearbeiten von Punkten
  * **Toggle Editing** (d.h. durch Anklicken des gelben Stifts <img src="../img/qgis/yellow-pen.png">) > **Digitizing Toolbar*****Add Point Feature***<img src="../img/qgis/sym-add-point.png">
  * Klicken Sie auf das PEGELHAUS, um einen Punkt zu zeichnen und einzustellen
    * `StnName`: `PlochingenFils`
    * `StnID`: `00025`
  * Fügen Sie weitere Punkte hinzu, wenn Sie möchten.
  * Vervollständigen Sie die Bearbeitungen, indem Sie auf **Save Layer Edits**<img src="../img/qgis/sym-save-edits.png">* **Stop (Toggle) Editing* klicken, indem Sie auf das gelbe Stift <img src="../img/qgis/yellow-pen.png">symbol klicken.
* Verbessern Sie die Visualisierung durch Änderung der Symbologie:
  * **Double-Klick auf* die Messgeräte **Schicht** > **Symbolog**
  * Highlight **Simple Marker**, ändern Sie das **+** Symbol und ändern Sie die Füllfarbe und Größe.
  * Highlight **Marker*** und ändern Sie die **Opacity***
  * Klicken Sie auf **Apply** und **OK***
* Überprüfen Sie die Punkteinstellungen in der **Attribute Table** (Rechtsklick auf die *gauges*-Schicht und wählen Sie **Attribute Table**).

(create-line-shp)=
### Erstellen einer Line Shapefile

Erstellen Sie eine **Line Shapefile** mit **CenterLine.shp**, um eine Mittellinie der Fils $\pm$ 200 m um die PEGELHAUS-Messe zu zeichnen, ähnlich wie die oben erstellte Punktformdatei. Fügen Sie ein *text* Feld hinzu und rufen Sie es an `RiverName`. Dann ziehen Sie eine Linie entlang des Fils River ab 200 m stromaufwärts und enden 200 m stromabwärts des PEGELHAUS, indem Sie dem Fluss auf der **OpenStreetMap*-Schicht folgen. Weitere Informationen finden Sie im folgenden Video.

```{admonition} Create Line shapefile video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/yNuiIlPsguQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

(create-polygon-shp)=
### Erstellen einer Polygon Shapefile

Um unterschiedliche Rauheitszonen abzugrenzen (z.B. nach Bedarf für ein zweidimensionales numerisches Modell), erstellen Sie eine **Polygon Shapefile** **FlowAreas.shp***. Die Datei enthält Polygone, die den betrachteten Abschnitt der Fils in das Flut- und Hauptkanalbett zonen. Nennen Sie das erste Feld `AreaType` (Typ: *Text*) und das zweite Feld `ManningN` (Typ: *Decimal Number*). Weitere Informationen finden Sie im folgenden Video und den Anweisungen unter dem Video.

```{admonition} Create Polygon video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/zTrowT0ULfo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Um die Polygone zu zeichnen:

* Aktivieren Sie ein Snapping, um Lücken zwischen dem Flutplain und Hauptkanalpolygonen zu vermeiden
  * Aktivieren Sie die **snapping toolbar*: **Ansicht** > **Werkzeugleisten*****
  * Aktivieren Sie Snapping aus **Snapping toolbar****** und **Avoid Polygon Overlapping**
* Um ein Polygon zu zeichnen, gehen Sie zur **Digitizing Toolbar*** > **Add Polygon Feature** mit der **Digitize mit Segment** Option aktiviert
* Starten Sie das Zeichnen, indem Sie auf die Karte klicken (Rechtsklick beendet Polygon)
* Zeichnen Sie ein Polygon des Hauptkanals und nach der Fertigstellung:
  * `AreaType`: `MainChannel`
  * `ManningN`: `0.028`
* Zwei weitere Polygone der rechten Bank (RB) und der linken Bank (LB) Hochwasserplains zeichnen und setzen:
  * `AreaType`: `FloodPlainRB` and `FloodPlainLB`
  * `ManningN`: `0.05` (beide)
* Wenn Sie einen Zeichnungsfehler gemacht haben, verwenden Sie entweder die *Attribute Tabelle*, um ganze Polygone auszuwählen und zu löschen, oder verwenden Sie das Vertex-Tool <img src="../img/qgis/sym-vertex-tool.png"> aus der Menüleiste.
* Nach dem Zeichnen aller Polygone, **Save edits* und **Toggle Editing** (deaktivieren).
* Um die Visualisierung zu verbessern, ändern Sie die **Symbology***** in Abhängigkeit vom Feld `AreaType`: Keep **Random Colors*** Klicken Sie auf **Classify********************* und wenn Sie die Visualisierung möchten, klicken Sie auf **OK***.


## Umrechnung: Rasterize (Polygon zu Raster)

Viele numerische Modelle verlangten, dass Rauheit im {ref}`raster`-Format zur Verfügung gestellt wird. Zu diesem Zweck enthält dieser Abschnitt die Umwandlung der oben erstellten Polygonformdatei (*FlowAreas.shp*) zu einer Rauhigkeit {ref}`raster`. Das folgende Video und die Anweisungen unter dem Video beschreiben, wie die Konvertierung funktioniert.

```{admonition} Rasterization video
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/IRLwYSUnjcE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Um einen geospatialen Vektordatensatz zu konvertieren, verwenden Sie das *Rasterize* Tool:

* In der QGIS Menüleiste stellen Sie sicher, dass das *Processing Toolbox* Panel (**View**** > **Panels** > **Processing Toolbox***) aktiviert wird.
* In der **Process-Toolbox** > Suche (Tap) **Rasterize*** > Auswahl **Rasterize (Vector to raster)**

```{hint}
Wenn das *Crayfish* Plugin installiert ist, wird ein zusätzliches *Rasterize*-Tool angezeigt, das wir in diesem Tutorial nicht verwenden (d.h., stellen Sie sicher, *Rasterize (Vector to raster)* ) zu wählen.
```

* Im Fensterset **Rasterize (Vector to Raster)**:
  * **Eingangsschicht**: `FlowAreas`
  * **Für einen Einbrennwert zu verwenden*: `ManningN`
  * **Output Rastergrößen**: `Pixels`
  * **Width/Horizontal Resolution*: `100` (je kleiner, desto grober der Raster)
  * **Height/Vertical Resolution*: `100` (je kleiner, desto grober der Raster)
  * ... nach unten scrollen...
  * **Ausgangsmaß**: Klicken Sie auf den **...** Button > **Calculate from Layer** > `FlowAreas`
  * **Rasterized** (FILE NAME) > Klicken Sie auf den **...* Button > **Save to File...** > `roughness.tif`
  * **Run***
* Setzen Sie die **Symbology** auf **Singleband pseudocolor** mit **Interpolation**: `Discrete`, **Colorramp**:`Magma`, **Mode**: `Equal Interval`**Apply***. Wenn die Visualisierung zufriedenstellend ist, klicken Sie auf **OK**.

```{admonition} File conversion with Python
:class: tip
Die Umwandlung zwischen Geodatentypen kann durch die Verwendung von Python erleichtert werden. Lesen Sie den Abschnitt unter {ref}`py-conversion`, um mehr zu erfahren.
```

## Polygon

The inverse operation of *Rasterize* is called **Raster to Vector**, which is documented at [https://docs.qgis.org](https://docs.qgis.org/testing/en/docs/training_manual/complete_analysis/raster_to_vector.html). The creation of a Polygon shapefile from a Raster is described in the video below. The essential steps are:

* Gehen Sie zu **Raster** (Top-Menü) > **Conversion**** **Polygonize (Raster zu Vector)...*
* **Input Layer**: Wählen Sie den Raster aus, um zu konvertieren
* **Bandnummer**: das Rasterband zur Verkleinerung des Polygonwerts (d.h. Feld in der Attributtabelle); einige Anmerkungen:
  * dieser Algorithmus rundet Dezimals zu Ganzzahlen (siehe Video unten)
  * Alternativ suchen *Raster-Pixel zu Polygonen* in der *Processing Toolbox*, aber es wird eine übermäßige Anzahl von Polygonen erstellen
* **Name des zu erstellenden Feldes**: Wählen Sie einen Namen für das Polygonwertfeld in der Attributtabelle (**nicht mehr als 10 Zeichen*)
* **Vectorized**: das Verzeichnis und den Namen für die neue Polygon-Formdatei definieren
* **Run***

```{admonition} Polygonize (video)

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/r9MwkKvUD-k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>

Hier erhalten Sie das [**mannings-n GeoTIFF*](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/mannings-n.tif).

```


Um ein Raster in eine Zeile/Punkt (Vektor)-Shap-Datei umzuwandeln, sind die Optionen die [Contour](https://docs.qgis.org/3.28/en/docs/training_manual/processing/interp_contour.html)tool (**Raster*-Menü > **Extraction*******) oder die [Raster-Pixel zu points](https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorcreation.html#raster-pixels-to-points)algorithmus (**Processing*** Toolbox > geben `raster pixels to points`) ein. Sehen Sie sich auch die Tutorials an {ref}`geo file conversion with Python <raster2line>`.



## Arbeiten mit Rastern

### QGIS Rasterrechner (Karte Algebra)

Einige Modelle verwenden vorzugsweise (Standard-Nutzung) Manning's *n*, andere verwenden den Strickler Rauheitskoeffizienten $k_{st}$, der inverse von Manning's *n* ist (d.h. $k_{st} = 1/n$ - Lesen Sie mehr über Rauheitskoeffizienten in der {ref}`ex-1d-hydraulics` Übung). So erfordert die Umwandlung eines Strickler Rauheitsrasters in einen Manning Rauheitsraster eine algebraische Rasterfunktion (Pixel-by-Pixel). Das nächste Video und die Anweisungen unter dem Video enthalten die Verwendung des QGIS **Raster Calculators**, um solche algebraischen Operationen durchzuführen.

```{admonition} Raster calculator (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/DOkV03uij9k" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Beginnen Sie mit der Eröffnung **Raster-Rechner** aus der QGIS-Menüleiste (**Raster*** > **Raster-Rechner...**). Dann wandeln Sie den oben erstellten *roughness.tif*-Raster von Mannings *n*-Werten in einen Strickler-Raster um:

* Definieren Sie eine **Output-Schicht** (z.B. *qgis-exercise/roughness-stickler.tif*) und halten Sie das **Output-Format** von **{term}`GeoTIFF`**.
* Wählen Sie optional eine Schichterstreckung aus, die dem o.g. *roughness.tif*-Raster entspricht.
* Im **Raster Calculator Expression** Frame Type **1* klicken Sie dann auf die **/** Taste (**Operators** Frame), dann wählen Sie **roughness@1** aus dem **Raster Bands** Rahmen.
* Der **Raster Calculator Expression** Frame sollte jetzt enthalten: `1 / "roughness@1"`, wobei das `@`-Zeichen auf Bandnummer `1` verweist.
* Klicken Sie auf **OK**, um *Raster Calculator* auszuführen.
* Nach erfolgreicher Berechnung gegebenenfalls die Symbologie der neuen Schicht (*roughness-Stickler*) ändern.

```{admonition} Batch-process geodata
:class: tip
Um einen maßgeschneiderten Rasterrechner für die Batch-Verarbeitung von Rasterdateien mit Python zu implementieren, lesen Sie die {ref}`py-raster-calculator` Sektion in der {ref}`ex-geco` Übung.
```

(make-xyz)=
### Raster auf XYZ

Wissenschaftliche Datenformate, wie {term}`HDF`, arbeiten am besten mit rohen Geospatialdatensätzen wie `*.xyz`Dateien. Eine `.*xyz`-Datei enthält nur X-, Y- und Z-Koordinaten von Punkten (d.h. Punktwolken) mit oder ohne einfachen Header. Beispielsweise verwendet dieses eBook `*.xyz`-Daten für die Höheninterpolation eines Rechennetzes für die wissenschaftliche numerische Modellierungssoftware {ref}`chpt-telemac`. Um eine `*.xyz` von einem {term}`GeoTIFF`Raster zu generieren, verwenden Sie den folgenden Workflow:

* Im **Layers*-Panel stellen Sie sicher, dass die Rasterschicht zur Konvertierung importiert wird und ** den No-Data**-Wert identifiziert (**Layer Properties** > **Information** > **Bands** Abschnitt > **No-Data**-Feldshow standardmäßig `-9999` in QGIS).
* Im QGIS Top-Menü gehen Sie zu **Raster**** **Conversion**** **Übersetzen (Convert Format)...**
* Im Fenster **Übersetzen (Konvertieren Format)** die folgenden Einstellungen vornehmen:
  * **Input Layer** = raster (z.B. {term}`DEM`) zum Umwandeln
  * ** Fortgeschrittene Parameter** Frame > **Output-Datentyp****** auswählen **Float32** (entspricht Einzelgenauigkeit in numerischen Modellen)
  * **Konvertiert******* Knopf (am Ende der Zeile) > **Save to File...* > definieren Sie einen **Dateinamen** wie `dem-points` und wählen Sie `XYZ files (*.xyz)` im **Save as type** Feld.
  * **Save** und **Run** die Übersetzung (Konversion).

The resulting `*.xyz` file contains also points with **No-Data** to fill void spaces in the rectangular image of the {term}`GeoTIFF` (which QGIS did recognize as no-data pixels). The no-data points may make the `*.xyz` file unnecessarily heavy, in particular, when it is a {term}`DEM` of a near-census natural river. To eliminate the unnecessary no data points, open the `*.xyz` file in spreadsheet software, such as {ref}`Calc in LibreOffice <lo>` and use the *Sort* tool (in **Calc** highlight all points go to **Data** > **Sort...**) to sort by `Z` values (largest to smallest) and then delete all rows that have the above-identified **No-Data** value (`-9999`) as `Z` value. Save the `*.xyz` file and close the spreadsheet software.

```{admonition} Shapefile to XYZ
:class: tip, dropdown
**Shapefiles** muss nicht in {term}`GeoTIFF` um eine `*.xyz`-Datei zu erstellen umgewandelt werden. Um eine `*.xyz`-Datei aus einer **shapefile** zu erstellen:

* Klicken Sie mit der rechten Maustaste auf die Formdatei im **Layer* Panel > **Export** > **Save Feature als...**
* Wählen Sie **Comma Separated Value ({term}`CSV`)** im Feld **Format**.
* Definieren Sie einen **Dateinamen**, indem Sie auf den **...** Button klicken.
* Wählen Sie im **Layer-Optionen**-Rahmen **AS XYZ** im **GEOMETRY**-Feld aus und halten Sie alle anderen Standardeinstellungen.
* Klicken Sie auf **OK**, um {term}`CSV` zu konvertieren.
* Open the {term}`CSV` file in a {ref}`text editor <npp>` and use its *find and replace* function (usually `CTRL`+`F` or `CTRL`+`H`) to replace all COMMA `,` by a space symbol ` `. Note that this action requires that the comma has not been used as decimal separator.
* Speichern Sie die {term}`CSV` Datei als `*.xyz` Datei.
```

Um die `*.xyz`-Datei abzuschließen, öffnen Sie sie in einer {ref}`text editor <npp>` und fügen Sie einen Header hinzu. Verwenden Sie beispielsweise den folgenden Header, um mit {ref}`Blue Kenue <bluekenue>` zu arbeiten:

```
:FileType xyz  ASCII  EnSim 1.0
:EndHeader
```

Speichern Sie die Änderungen. Die `*.xyz`-Datei ist jetzt schlank und bereit, zum Beispiel für die {ref}`TELEMAC pre-processing <get-dem-xyz>`.

## Layout und PDF / JPG (oder andere) Karten erstellen

Georeferenzierte Bilder in {term}`GeoTIFF` oder anderen Rasterformaten, möglicherweise mit übergeordneten Formdateien oben, sind handlich und flexibel für den Einsatz mit geospatialer Software, wie QGIS, aber nicht für Präsentationen oder Berichte geeignet. Für Präsentationszwecke sollten Geospatial-Bilder oder Karten vorzugsweise in gemeinsame Formate exportiert werden, wie z.B. die **P*ortable **D*ocument **F*ormat (PDF) oder **JPEG/JPG***. Um gemeinsam formatierte Karten mit QGIS zu erstellen, muss zunächst ein neues (Druck-)Layout erstellt werden, das dann in ein gemeinsames Kartenformat exportiert werden kann (z.B. zusammen mit einer Legende, einer Skalenleiste und einem Nordpfeil). Das folgende Video und die Beschreibungen unter dem Videoführer durch den Kartenerstellungsprozess mit QGIS.

```{admonition} Layout creation (video)
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/hmTByzVPVF0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

Starten Sie mit der Erstellung eines neuen Drucklayouts, indem Sie auf das **Projekt** Dropdown-Menü klicken, dann wählen Sie **Neues Drucklayout***. Im neuen Drucklayout die Karte vorbereiten und die Karte wie folgt exportieren:

* Setzen Sie einen **Layout-Titel** (z.B. *exercise-layout*).
* Im neuen (*exercise-layout*) Layout:
  * Gehen Sie zu **Hinzufügen*****Hinzufügen.
  * Zeichnen Sie ein Rechteck, das die Karte enthält.
  * **Add Item*** **Add Scale Bar***
  * Zur Steuerung von Skalen und Einheiten im Maßstabstab:
    * In **Items** Panel, markieren Sie `<Scalebar>` und finden Sie die **Item Properties** Tab unten.
    * In der Registerkarte **Item Properties* ändern Sie Einheiten auf Ihren Komfort.
  * **Add Item*****Add Legend**
  * Zur Steuerung von Elementen der Legende:
    * In **Items** Panel, markieren Sie `<Legend>` und finden Sie die **Item Properties** Tab unten.
    * In der Registerkarte **Item Properties* finden Sie **Legend Items** > deaktivieren **Auto-Update********* *OpenStreetMap* und *Google Satellite*.
  * In der Menüleiste ** Artikel** einfügen (z.B. **Arrow** für Northing).
* **Save*** das Layoutprojekt (aus dem oberen Menü **Layout*****Save Project**)
* Exportieren Sie die Karte in gemeinsame Formate:
  * Für JPG oder PNG: **Layout** > **Export als Bild**
  * Für PDF: **Layout** > **Export als PDF*
  * Optional für SVG-Vektor-Diagramme: **Layout** > **Export als SVG**

QGIS hat viele andere Kapazitäten, aber dieses grundlegende Tutorial sollte Ihnen das notwendige Wissen zur Nutzung der Macht von QGIS für viele Anwendungen zur Verfügung gestellt haben.

(pygis)=
## PyQGIS: QGIS und Python

Die QGIS grafische Benutzeroberfläche (GUI) bietet eine Python Befehlszeile (**Plugins** > **Python Console**), die es ermöglicht, fast jeden Mausklick in der GUI zu automatisieren. Diese Python-Befehlszeile wird als **PyQGIS*** bezeichnet und der [QGIS-Entwickler docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html) gibt Anweisungen, wie man eigenständige Python-Skripte außerhalb der QGIS GUI importiert und ausgeführt. Hier ist die grundlegende Python Vorlage, um ein PyQGIS-Skript auszuführen:


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

Wenn Sie jedoch das Terminal Ihres Systems oder Anaconda Prompt zum Ausführen eines PyQGIS-Codes öffnen, können Sie bereits auf der ersten Zeile des Codes festhalten: `from qgis.core import *`r gibt `ImportError: No module named qgis.core`. Laut dem [QGIS-Entwickler docs](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html) geschieht dieser Fehler, weil Ihr System Python nicht weiß, wo die PyQGIS-Umgebung lebt. Um Ihr Terminal erkennen PyQGIS, nehmen Sie die folgende Aktion nach Ihrem System:

`````{tab-set}
````{tab-item} Linux

Öffnen Sie Terminal und installieren Sie `python-qgis`:

```
sudo apt install python-qgis
```

Nach der erfolgreichen Installation versuchen Sie, ob Sie jetzt `qgis.core` importieren können:

```
USER@computer:~$ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from qgis.core import *
>>> exit()
```

If `from qgis.core import *` did not throw any error, you are all set and can stop reading. **Otherwise**, find and open your `.bashrc` file (Debian/Ubuntu/Mint: `/home/USERNAME/.bashrc`). Note that files starting with a `.` name are hidden on Linux and become visible by toggling with simultaneously pressing the `CTRL`+`H` keys.

Am unteren Rand von `.bashrc`

```
export PYTHONPATH=/<qgispath>/share/qgis/python
```

Der `<qgispath>`-Ausdruck sollte durch den Ort ersetzt werden, an dem die PyQGIS-Umgebung lebt. Um herauszufinden, wo das ist, tippen Sie auf (in Terminal):

```
dpkg-query -L python-qgis
```

Dies deutet darauf hin, wo PyQGIS lebt, was auf Ubuntu/Mint typischerweise ist:

```
/usr/lib/python3/dist-packages/
```

So fügen Sie in diesem Fall `.bashrc`:

```
export PYTHONPATH=/usr/lib/python3/dist-packages/
```

Anschließend melden Sie sich an und melden Sie sich an Ihr System (d.h. reload `.bashrc`). Der Befehl `from qgis.core import *` soll nun in Python arbeiten.
````

````{tab-item} Windows

Stellen Sie sicher, dass Ihr System weiß, wo PyGIS lebt, indem Sie die folgende Zeile zu den Umweltvariablen hinzufügen (Windows 10: **Mein Computer** > **Properties**** ** Fortgeschrittene Systemeinstellungen******** **Umweltvariablen***). Ersetzen Sie `<qgispath>` mit dem Pfad, in dem QGIS auf Ihrem System lebt.

* Variabler Name = `PYTHONPATH`
* Variabler Wert = `C:\<qgispath>\python`

Oder verwenden Sie die Windows-Prompt:

```
set PYTHONPATH=C:\<qgispath>\python
```

````
`````


