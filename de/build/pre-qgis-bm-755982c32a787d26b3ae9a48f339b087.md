---
description: Tutorial für die Vorverarbeitung eines digitalen Höhenmodells (Digitales Oberflächenmodell (DOM)) in QGIS zur Generierung eines Rechennetzes im SMS 2dm-Format für hydrodynamische BASEMENT-Simulationen.
---

(qgis-prepro-bm)=
# Vorverarbeitung mit QGIS

```{admonition} Requirements
:class: attention
Dieses Tutorial ist für ** Anfänger ** und vor dem Tauchen in dieses Tutorial stellen Sie sicher:

* Follow the installation instructions for {ref}`qgis-install` in this eBook.
* Read (or watch) and understand this eBook's {ref}`qgis-tutorial`.
```

The first steps in numerical modeling of a river with BASEMENT consist in the conversion of a **Digital Elevation Model ({term}`Digitales Oberflächenmodell <DEM>`)** into a computational mesh. This tutorial guides through the creation of a QGIS project for converting a {term}`Digitales Oberflächenmodell <DEM>` ({term}`GeoTIFF`) into a computational mesh that can be used with various numerical modeling software featured in this eBook. At the end of this tutorial, {ref}`chpt-basement` users will have generated a computational grid in the {term}`SMS 2dm` format.

```{admonition} Platform compatibility
:class: tip
All software applications featured in this tutorial can be run on *Linux*, *Windows*, and *macOS* (in theory - not tested) platforms. Note that {ref}`chpt-basement` itself will not work on *macOS* platforms.
```

```{admonition} Recall: BASEMENT versions, BASEMD, and BASEHPC
:class: note

BASEMENT Version 2 (v2) wurde mit komplexen Strukturen und einer breiten Palette von Kapazitäten entwickelt, wobei der Schwerpunkt jedoch wenig auf der Rechenzeit lag. BASEMENT Version 3 (v3) vereinfachte den Modellierungsprozess für die Benutzer erheblich und bot hocheffiziente Rechenoptionen, einschließlich einer massiven Parallelisierung von GPUs. Dem vereinfachten v3 fehlen jedoch viele relevante Module, wie z. B. mehrschichtige Flussbetten zur Berechnung der topografischen Veränderung in Abhängigkeit von mehrkörnigen Transportformeln. Jetzt bietet BASEMENT Version 4 (v4) sowohl die vielfältigen Kapazitäten von v2 in Form von BASEMD-Setups als auch die Recheneffizienz von v3 in Form von BASEHPC-Setups. Dieses Tutorial erklärt die Einrichtung eines BASEHPC-Modells.

```

(start-qgis)=
## QGIS Setup

### Koordinatenreferenzsystem (Koordinatenreferenzsystem)

Launch QGIS and {ref}`create a new QGIS project <qgis-project>` to get started with this tutorial.
As featured in the {ref}`qgis-tutorial`, set up a coordinate reference system (CRS) for the project. This example uses data of a river in Bavaria (Germany zone 4), which requires the following CRS:

* Gehen Sie im QGIS-Spitzenmenü zu **Project** > **Properties**.
* Aktivieren Sie den **Koordinatenreferenzsystem**-Tab.
* Geben Sie `Germany_Zone_4` ein und wählen Sie das Koordinatenreferenzsystem aus, das unter {numref}`Fig. %s <qgis-crs>` angezeigt wird.
* Klicken Sie auf **Apply** und **OK**.

```{figure} ../img/qgis/inn-crs.png
:alt: qgis set coordinate reference system crs germany zone_4 Inn river
:name: qgis-crs

Definieren Sie Germany Zone 4 als Projekt Koordinatenreferenzsystem.
```

```{admonition} Save the project...
:class: tip
Speichern Sie das QGIS-Projekt (**Project** > **Save As...**), zum Beispiel unter dem Namen **prepro-tutorial.qgz**.
```

(get-basemesh)=
### Holen Sie sich das BASEmesh Plugin

Installieren Sie *BASEMENT*s *BASEmesh* Plugin (Anleitung aus dem *BASEMENT* Systemhandbuch):

* Laden Sie den *QGIS* Plugin-Manager: **Plugins** Menü > ** Plugins verwalten und installieren**.
* Gehe zum Tab **Einstellungen **.
* Scrollen Sie nach unten (**Plugin Repositories** listbox in {numref}`Fig. %s <qgis-plugins2>`), klicken Sie auf **Add...**.
* Im Popup-Fenster geben Sie ein:
  * ein Name für das neue Repository, zum Beispiel `BASEmesh Plugin Repository`
  * the repository address: [https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml)
  * alle anderen Ausfälle beibehalten.
* Klicken Sie auf **OK**. Das neue Repository sollte nun in der Liste **Plugin Repositories** sichtbar sein. Wenn die Verbindung ** OK** ist.

```{figure} ../img/qgis/bm-plugin.png
:alt: qgis basement plugins
:name: qgis-plugins2

Fügen Sie das BASEMENT-Repository zum QGIS Plugins Manager hinzu.
```

* Still in the **Plugins** popup window go back to the **All** tab an enter `basemesh` in the search field.
* Finden Sie das **neueste BASEmesh ** (dh **Verfügbare Version ** >= 2.0.0) Plugin und klicken Sie auf **Install Plugin **.
* Nach der erfolgreichen Installation **Close** das **Plugins** Popup-Fenster.
* Stellen Sie sicher, dass das *BASEmesh 2* Plugin jetzt im QGIS **Plugins** Menü verfügbar ist (siehe {numref}`Fig. %s <qgis-pluggedin>`).

```{figure} ../img/qgis/bm-pluggedin.png
:alt: qgis basement plugins
:name: qgis-pluggedin

Das BASEmesh 2-Plugin ist nach der erfolgreichen Installation im Plugin-Menü von QGIS verfügbar.
```


(get-dem)=
## Belastung Digitales Oberflächenmodell (DOM)

This tutorial uses an application-ready {term}`Digitales Oberflächenmodell <DEM>` in {term}`GeoTIFF` {ref}`raster` format that stems from a {term}`Lidar` point cloud. The {term}`Digitales Oberflächenmodell <DEM>` raster provides height (Z) information from a section of a gravel-cobble bed river in South-East Germany, which constitutes the baseline for the computational grids featured in the next sections. To get the provided DEM in the *QGIS* project:

* [** Laden Sie das Beispiel Digitales Oberflächenmodell (DOM) GeoTIFF**](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/dem.tif) herunter und speichern Sie es im gleichen Ordner (`/Project Home/` oder einem Unterverzeichnis) wie das oben erstellte **qgz** Projekt.
* Fügen Sie die heruntergeladene Digitales Oberflächenmodell (DOM) als neue Rasterschicht in *QGIS* hinzu:
  * Im *QGIS*' **Browser**-Bereich finden Sie das **Project Home**-Verzeichnis, in dem Sie das Digitales Oberflächenmodell (DOM) *tif* heruntergeladen haben.
  * Ziehen Sie das Digitales Oberflächenmodell (DOM) *tif* aus dem Ordner **Project Home** in das **Layer**-Panel von QGIS.
* Um später die Abgrenzung bestimmter Regionen des Flussökosystems zu erleichtern, fügen Sie unter {term}`Digitales Oberflächenmodell <DEM>` ein {ref}`satellite imagery basemap <basemap>` (XYZ-Kachel) hinzu und passen Sie die Ebenensymbologie an.

```{admonition} What are QGIS panels again?
:class: tip
Erfahren Sie mehr im *QGIS* Tutorial unter {ref}`qgis-tbx-install`.
```

Die Digitales Oberflächenmodell (DOM) sollte nun auf der Karte angezeigt werden (falls nicht: mit der rechten Maustaste auf der Digitales Oberflächenmodell (DOM)-Ebene und klicken Sie auf **Zoom zu Layer(s)** im Kontextmenü), wie unter {numref}`Fig. %s <qgis-dem-basemap>` gezeigt.

```{figure} ../img/qgis/dem-basemap.png
:alt: qgis import raster DEM basemap
:name: qgis-dem-basemap

Die importierte Digitales Oberflächenmodell (DOM) auf einer Google Satellite Imagery Basemap (Quelle: Google / GeoBasis-DEBKG 2019). Die Strömungsrichtung verläuft von links nach rechts und folgt dem Pfeil **Q**.
```


(make-2dm)=
## 2dm Mesh erstellen

The generation of a {term}`SMS 2dm` uses the {ref}`QGIS BASEmesh plugin <get-basemesh>` and requires drawing a

* {ref}`Line Shapefile <create-line-shp>` mit Modellgrenzen und internen Trennlinien zwischen Modellregionen mit unterschiedlichen Eigenschaften (Abschnitt auf {ref}`boundary`);
* {ref}`Line Shapefile <create-line-shp>` mit Modellgrenzen für die Zuweisung von Zu- und Abflussbedingungen (Abschnitt {ref}`liquid-boundary`); und
* {ref}`Point Shapefile <create-point-shp>` mit Markierungen für die Definition von Merkmalen von Modellregionen (Abschnitt unter {ref}`regions`).

These shapefiles enable to generate a {ref}`Quality Mesh <qualm>`. Ultimately, height information is {ref}`interpolated to the quality mesh <qualm-interp>` and the resulting mesh is saved as {term}`SMS 2dm` file. The next sections walk through the procedure step by step with detailed explanations. Additional materials and intermediate data products are provided in the supplemental data repository ([materials-bm](https://github.com/hydro-informatics/materials-bm)) for this tutorial.


(boundary)=
### Modellgrenzen und Breaklines

The model boundary defines the model extent and can be divided into regions with different characteristics (e.g., roughness values) through breaklines. Breaklines indicate, for instance, channel banks and the riverbed (main channel), and need to be inside the DEM extents. Boundary lines and breaklines are stored in a {ref}`Line Shapefile <create-line-shp>` that BASEmesh uses to find both model boundaries and internal breaklines between model regions. For this purpose, {ref}`create-line-shp` with **one Text Field** called **LineType** and call it **breaklines.shp** (**Layer** > **Create Layer** > **New Shapefile Layer**). Click on QGIS' **Layers** menu > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <qgis-new-lyr>`). Make sure to select `ESRI: 31494 - Germany_Zone_4` as {term}`Koordinatenreferenzsystem <CRS>` <img src="../img/qgis/sym-crs.png">.

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: qgis-new-lyr

Erstellen Sie ein neues Shapefile aus dem QGIS Layers-Menü.
```

Es ist wichtig, dass sich die Linien nicht überschneiden, um mehrdeutige oder fehlende Definitionen von Regionen zu vermeiden und sicherzustellen, dass alle Grenzlinien geschlossene Regionen (Gebiete) bilden. Aktivieren Sie daher Snapping:

* Aktivieren Sie die *Snapping Toolbar *: **View * > **Snapping Toolbar *
* In der **Snapping-Symbolleiste** > **Snapping** aktivieren <img src="../img/qgis/snapping-horseshoe.png">
* Ermöglichen Sie Snaping für
  * **Vertex**, **Segment** und **Mitte der Segmente** <img src="../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../img/qgis/snapping-intersection.png">.

Next, start to edit **breaklines.shp** by clicking on the yellow pen <img src="../img/qgis/yellow-pen.png"> and draw the lines indicated in {numref}`Fig. %s <breaklines>` by activating **Add Line Feature** <img src="../img/qgis/sym-add-line.png">.

* **Grenzen des** Modells links und rechts **Grenzen der Überschwemmungsgebiete**:
  * Begrenzen Sie die äußeren Grenzen der Auen.
  * Make sure that all points and lines are inside the {ref}`DEM layer <get-dem>`.
  * Überqueren Sie nicht den Fluss (benetzter Bereich, der durch die Satelliten-Basemap angezeigt wird).
  * **Beende jede Zeile mit einem **Rechtsklick**.
  * Verwenden Sie für das Feld **LineType** Textwerte wie **boundary left/right floodplain**.
  * Siehe die **roten Zeilen unter {numref}`Fig. %s <breaklines>`**.
* **Unterbrechungen der linken Bank (LB) und rechten Bank (RB)**:
  * Zeichnen Sie Linien entlang des benetzten Hauptkanals, der in der Satellitenbild-Basiskarte angegeben ist.
  * Stellen Sie sicher, dass die Linienenden perfekt mit den zuvor erstellten Auengrenzlinien übereinstimmen (hier hilft das Schnappen); Daher müssen die harten Bruchlinien des Hauptkanals und die Auengrenzlinien die Auen ohne Lücke zwischen den Linien einschließen.
  * Verwenden Sie für das Feld **LineType** Textwerte wie **hardline LB/RB**.
  * Beziehen Sie sich auf die **gelb-orangenen Linien unter {numref}`Fig. %s <breaklines>`** (beachten Sie die Abgrenzung der kleinen Nebenflüsse oben links am linken Ufer und unten rechts am rechten Ufer).
* **Breaklines von Kiesbänken**:
  * Zeichnen Sie Linien entlang der Schotterbänke, die in der Satellitenbild-Basiskarte im Hauptkanal sichtbar sind.
  * Stellen Sie sicher, dass die Leitungsenden perfekt mit den zuvor erstellten Hauptkanalbruchlinien (Hardlines) übereinstimmen; Daher müssen die harten Bruchlinien des Hauptkanals und die Schotterbankbruchlinien die Schotterbänke ohne Lücke zwischen den Linien einschließen.
  * Für das Feld **LineType** verwenden Sie Textwerte wie **hardline Kiesbank**.
  * Beziehen Sie sich auf die **green-ish Linien in {numref}`Fig. %s <breaklines>`**.
* Optional: **Unterbrechungen von Blockrampen**:
  * Finden Sie die rauen Blockrampen (ausblasende Gewässer) in der Satellitenbild-Basiskarte und beschreiben Sie sie, indem Sie Linien über den benetzten Hauptkanal zeichnen.
  * Stellen Sie sicher, dass die Leitungsenden perfekt mit den Hauptkanaltrennlinien übereinstimmen; Daher müssen die harten Trennlinien des Hauptkanals und die Blockrampentrennlinien die Blockrampen ohne Zwischenraum zwischen den Leitungen einschließen.
  * Für das Feld **LineType** verwenden Sie Textwerte wie **hardline sss** (oder irgendetwas anderes - das Beispiel bezieht sich auf das deutsche Wort <u>S</u>chütt<u>s</u>tein<u>s</u>chwelle).
  * Siehe die **blauen Linien unter {numref}`Fig. %s <breaklines>`**.
* Optional: **Breakline einer Sandbank**:
  * Find the sandbank deposit in the upper left corner in {numref}`Fig. %s <breaklines>` on the satellite imagery basemap and delineate it by drawing a smoothly curved line.
  * Stellen Sie sicher, dass die Leitungsenden perfekt mit den Hauptkanaltrennlinien übereinstimmen und einen geschlossenen Bereich ohne Lücke zwischen den Leitungen umfassen.
  * Verwenden Sie für das Feld **LineType** Textwerte wie **hardline sand**.
  * Siehe die **lila Linie** in der oberen linken Ecke **in {numref}`Fig. %s <breaklines>`**.

To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">. Finally, save the new lines (edits of **breaklines.shp**) by clicking on the **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.

```{figure} ../img/qgis/breaklines.png
:alt: qgis basement basemesh draw breaklines boundaries
:name: breaklines

Grenze und Bruchlinien, um **breaklines.shp** zu zeichnen. Links und rechts Ufer und Auen sind in Strömungsrichtung orientiert (**Q** Pfeil).
```

```{admonition} Troubles with drawing boundaries and breaklines?
:class: tip
Laden Sie die [zipped breaklines shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/breaklines.zip) in der obigen Abbildung gezeigt und entpacken Sie es in den Projektordner, zum Beispiel `/Project Home/shapefiles/breaklines.[SHP]`.
```

Der Standard-Layer-Stil ist **Single Symbol**. Zur besseren Darstellung doppelklicken Sie auf die Trennlinienebene, gehen Sie auf die Registerkarte **Symbology** und wählen Sie **Categorized** (oder **Graduated**) anstelle von **Single Symbol** (ganz oben im Fenster **Layer Properties**). Wählen Sie im Feld **Value** **LineType** und klicken Sie dann auf die Schaltfläche **classify** am unteren Rand des Fensters **Layer Properties**. In der Liste werden nun die *LineType*-Werte angezeigt.

```{admonition} Draw boundaries of complex DEMs...
:class: tip
Drawing boundaries manually around large {term}`Digitales Oberflächenmodell <DEM>`s can be very time consuming, in particular, if the raw data are a point cloud and not yet converted to a {ref}`raster`.

Wenn Sie es mit einer Punktwolke zu tun haben, sollten Sie *QGIS* [Convex Hull tool](https://docs.qgis.org/3.16/en/docs/training_manual/vector_analysis/spatial_statistics.html?highlight=convex%20hull#basic-fa-create-a-test-dataset), das ein eng umgrenzendes Polygon um Punkte zeichnet] verwenden.

If you are dealing with a large {term}`GeoTIFF`, consider using QGIS' [Raster to Vector](https://docs.qgis.org/3.16/en/docs/training_manual/complete_analysis/raster_to_vector.html) tool.
```


(liquid-boundary)=
### Flüssige (hydraulische) Grenzen

Die Flüssigkeitsgrenzen definieren, wo hydraulische Bedingungen, wie eine gegebene Entladungs- oder Stufenentladungsbeziehung, an den Modellzufluss- (stromaufwärts) und -abflussgrenzen (stromabwärts) gelten. Daher erfordert ein funktionales Flussmodell mindestens eine Zuflussgrenze (Linie), an der der Massenstrom in das Modell fließt, und eine Abflussgrenze (Linie), an der Massenströme das Modell verlassen. Zu diesem Zweck hat {ref}`create-line-shp` **liquid-boundaries.shp** aufgerufen und definiert **zwei Textdatenfelder** mit den Namen **type** und **stringdef**. Stellen Sie sicher, dass **snapping ** immer noch ** aktiviert ist ** (wie oben im Abschnitt {ref}`boundary` erklärt) und **Toggle (Start) Editing ** <img src="../img/qgis/yellow-pen.png"> das neue **liquid-boundaries.shp **. Zeichne dann zwei Linien:

* Aktivieren Sie **Hinzufügen-Funktion** <img src="../img/qgis/sym-add-line.png">.
* Zeichnen Sie eine Zuflussgrenze (siehe auch {numref}`Fig. %s <inflow-boundary>`):
  * Zoomen Sie auf den Zuflussbereich der Digitales Oberflächenmodell (DOM)-Grenzen, wo es eine **Lücke zwischen** den oben erstellten **Überflutungsgrenzlinien** gibt.
  * Beginnen Sie mit dem Zeichnen einer Linie am linken Ufer (linke Seite der unteren Abbildung) und bewegen Sie sich nach Osten (dh nach rechts), um sieben weitere Punkte über den Fluss zu machen.
  * Der **siebte Punkt ** muss mit dem Ende der **Überflutungsgrenze der rechten Bank ** zusammenfallen **.
  * Thus, the upstream flow is coming from the right-hand side of the inflow boundary line (i.e., the upstream flow direction will be `right` for the numerical model).
  * ** Beenden Sie die Zeile mit einem **Rechtsklick** und geben Sie `Inflow` im **Typ**-Feld und `inflow` im **Stringdef**-Feld ein (der Fall ist wichtig).
  * To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/inflow-boundary.png
:alt: qgis basemesh draw inflow boundary line
:name: inflow-boundary

Die Einströmbegrenzungslinie ist von links nach rechts gezeichnet (d.h. die stromaufwärtige Strömung kommt von der rechten Seite der Einströmbegrenzungslinie). Die Reihenfolge der zu verwendenden Tasten wird durch die roten Boxen hervorgehoben.
```

* Zeichnen Sie als nächstes eine Outflow-Grenzlinie (siehe auch {numref}`Fig. %s <outflow-boundary>`):
  * Zoomen Sie auf den Abflussbereich der Digitales Oberflächenmodell (DOM)-Grenzen, wo es eine **Lücke zwischen** den oben erstellten **Überflutungsgrenzlinien** gibt.
  * Beginnen Sie mit dem Zeichnen einer Linie am linken Ufer (oben in der unteren Abbildung) und bewegen Sie sich nach Südwesten (dh nach unten), um sieben weitere Punkte über den Fluss zu machen.
  * Der **siebte Punkt ** muss mit dem Ende der **Überflutungsgrenze der rechten Bank ** zusammenfallen **.
  * Thus, the upstream flow is coming from the right-hand side of the outflow boundary line (i.e., the upstream flow direction will be `right` for the numerical model).
  * ** Beenden Sie die Zeile mit einem **Rechtsklick** und geben Sie `Outflow` im **Typ**-Feld und `outflow` im **Stringdef**-Feld ein (der Fall ist wichtig).
  * To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/outflow-boundary.png
:alt: qgis basemesh draw outflow boundary line
:name: outflow-boundary

Die Abflussbegrenzungslinie ist von oben nach unten gezeichnet (d.h. die stromaufwärtige Strömung kommt von der rechten Seite der Abflussbegrenzungslinie).
```

```{admonition} Constraints of inflow and outflow boundaries
:class: important
Die Zu- und Abflussbegrenzungslinien müssen die gleiche Anzahl von Knoten haben (hier 7 plus 1), und keine Flüssigkeitsbegrenzungslinie darf mehr als 40 Knoten haben.
```

Speichern Sie schließlich die flüssigen Grenzlinien (Bearbeitungen von **liquid-boundaries.shp**), indem Sie auf das **Layer Edits** <img src="../img/qgis/sym-save-edits.png"> Symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.

```{admonition} Troubles with drawing the liquid boundary lines?
:class: tip
Laden Sie die [zipped liquid-boundaries shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/liquid-boundaries.zip)] herunter und entpacken Sie sie in den Projektordner, zum Beispiel `/Project Home/shapefiles/liquid-boundaries.[SHP]`.
```

```{admonition} stringdefs
:class: note
The *stringdefs* field values can be directly used with {ref}`chpt-basement`, where hydraulic data (e.g., discharge, water depth, or stage-discharge relations) can be assigned to the here defined georeferenced inflow and outflow boundary lines.
```

(regions)=
### Regionsmarkierungen

Regionsmarker werden innerhalb von Regionen platziert, die durch Grenzlinien und Bruchlinien definiert sind. Jeder Regionsmarker (d.h. ein Punkt irgendwo im Regionsbereich) weist beispielsweise eine Materialkennung (MATIDs) und eine maximale Mesh-Zellfläche zu. Die letztere Option ermöglicht es, kleine Maschenzellen (Maschenbereiche) im aktiven Kanalbett zu definieren und größere Zellbereiche in den Auenregionen. {ref}`create-point-shp` benannt **raster-points.shp** mit den folgenden Definitionen (siehe auch {numref}`Fig. %s <qgis-reg-lyr>`):

* Definieren Sie den ** Dateinamen** als **region-points.shp** (oder ähnlich)
* Stellen Sie sicher, dass der **Geometrietyp** **Point** ist
* The {term}`Koordinatenreferenzsystem <CRS>` <img src="../img/qgis/sym-crs.png"> corresponds to Germany Zone 4 ({ref}`see project CRS <start-qgis>`)
* Fügen Sie drei **New Field**s hinzu (zusätzlich zum Standardfeld **Integer** Typ **ID**):
  * **max area** = **Dezimalzahl** (**Länge** = 10, **Präzision** = 3)
  * **MATID** = **Ganzzahl** (**Länge** = 3)
  * **type** = **Textdaten** (**Länge** = 20)
* Klicken Sie auf **OK**, um das neue Punkt-Shapefile zu erstellen.

```{figure} ../img/qgis/bm-region-pts-create.png
:alt: basement mesh qgis region layer points
:name: qgis-reg-lyr

Definitionen und Felder, die der Region-Points Shapefile hinzugefügt werden sollen.
```

Consider to **deactivate snapping** for drawing the region markers to avoid that region markers coincide with any line. Then, **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **region-points.shp** file and activate **Add Point Feature** <img src="../img/qgis/sym-add-point.png">. Draw one point in every area section that is enclosed by breaklines and (liquid) boundary lines. Depending on the apparent area type from the satellite imagery basemap, assign one of the five regions listed in {numref}`Tab. %s <region-defs>` to every point.

```{list-table} Region names and their **max_area**, **MATID**, and **type** field values.
:header-rows: 1
:name: region-defs

* - Region
  - Flussbett
  - Blockrampen
  - Grasbanken
  - Überschwemmungsgebiete
  - Sand
* - **max area**
  -  25,0
  -  20.0
  -  25,0
  -  80,0
  -  20.0
* - **MATID**
  - 1
  - 2
  - 3
  - 4
  - 5
* - **Typ**
  - Flussbett
  - block ramp
  - gravel bank
  - Überschwemmungsgebiet
  - Sand Einlage
```

Nachdem Sie in jedem geschlossenen Bereich einen Punkt gezeichnet haben, speichern Sie die Regionspunktmarkierungen (Bearbeitungen von **region-points.shp**), indem Sie auf das **Layer Edits** <img src="../img/qgis/sym-save-edits.png"> Symbol klicken. **Stop (Toggle) Bearbeiten**, indem Sie erneut auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> klicken. {numref}`Figure %s <qgis-reg-pts>` zeigt ein Beispiel für Regionsmarkerpunkte innerhalb der durch die Bruchlinien abgegrenzten Bereiche.

```{figure} ../img/qgis/bm-region-pts-map.png
:alt: basemesh region points
:name: qgis-reg-pts

Beispiel für Regionspunktmarkierungen in den Projektgrenzen.
```

```{admonition} Troubles with drawing the region marker points?
:class: tip
Laden Sie die [zipped region-points shapefile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/region-points.zip)] herunter und entpacken Sie sie in den Projektordner, zum Beispiel `/Project Home/shapefiles/region-points.[SHP]`.
```

(qualm)=
### Erstellen Sie ein Quality Mesh

*BASEmesh*'s quality mesh tool creates a computationally efficient triangular mesh based on {cite:t}`shewchuk1996` and within the above-defined model boundaries. The tool associates mesh properties with the regions shapefile ([see above section on {ref}`regions`), but it does not include elevation data. Thus, after generating a quality mesh, elevation information needs to be added. This section explains the quality mesh generation and the next section features the interpolation of bottom elevations.

Klicken Sie im Menü von QGIS **Plugins** auf **BASEmesh 2** > **QUALITÄTSMESHING**, um das Qualitäts-Mesh-Tool zu öffnen. Führen Sie die folgenden Einstellungen im Popup-Fenster aus (siehe auch {numref}`Fig. %s <qgis-qualm>`):

* Rahmen für Triangulationsbeschränkungen:
  * **Breaklines** = **breaklines** (siehe {ref}`boundary`).
  * Behalten Sie alle anderen Standardwerte.
* Regionsrahmen:
  * ** Aktivieren Sie das Kontrollkästchen Regionen**.
  * **Region marker layer** = **regions-points** (siehe {ref}`regions`).
  * ** Aktivieren Sie das Kontrollkästchen MATID-Feld** und wählen Sie das **MATID-Feld** der Shapefile *regions-points* aus.
  * ** Aktivieren Sie das Kontrollkästchen Maximalfläche** und wählen Sie das **max area-Feld** der Shapefile *regions-points* aus.
* Mesh-Domain-Frame: Standard beibehalten.
* Stringdefinitionsrahmen:
  * ** Aktivieren Sie das Kontrollkästchen Stringdefinitionen**.
  * **Stringdefinitionsschicht** = **liquid borders**.
  * **Stringdefinitionen ID Feld** = **stringdef**.
  * ** Aktivieren Sie das Kontrollkästchen Include in 2DM Node Strings (BASEMENT 3)**.
  * Ignorieren Sie alle Optionen von BASEMENT 2.8.
* Einstellungsrahmen: Standardeinstellungen beibehalten.
* Ausgaberahmen:
  * Klicken Sie auf die Schaltfläche **Browse...** und definieren Sie einen **2dm** Dateinamen im `/Project Home/` Verzeichnis, z. B. **prepro-tutorial quality-mesh.2dm**.
* Klicken Sie auf die Schaltfläche **Run**, um das Qualitätsnetz zu erstellen.


```{figure} ../img/qgis/bm-quality-meshing-success.png
:alt: basement qgis quality mesh tin
:name: qgis-qualm

Definitionen, die in BASEmeshs Quality Meshing Tool gemacht werden müssen.
```

Qualitätsverzahnung kann Zeit in Anspruch nehmen. Nach einer erfolgreichen Mesh-Generierung wurde die Datei **prepro-tutorial quality-mesh-interp.2dm** generiert.

(qualm-interp)=
### Interpolieren Sie Bottom Elevation zu Quality Mesh

The *BASEmesh* plugin's **Interpolation** tool projects bottom elevation data onto the quality mesh by interpolation from another mesh or a {term}`Digitales Oberflächenmodell <DEM>` {ref}`raster`. Here, we use the {ref}`above-introduced DEM GeoTIFF <get-dem>`. To run the interpolation, open *BASEmesh*'s **Interpolation** tool (*QGIS* **Plugins** menu > **BASEmesh 2** > **Interpolation**) and make the following settings (see also {numref}`Fig. %s <qgis-qualm-interp>`):

* Wählen Sie im **Mesh-Layer zum Interpolieren ** Frame **prepro-tutorial quality-mesh **.
* In der Registerkarte **Basic** finden Sie den **Elevation Source** Frame und aktivieren Sie die **Aktivierung über Digitales Oberflächenmodell (DOM) (Raster)** Radio-Taste.
* Wählen Sie **dem.tif** GeoTIFF (siehe {ref}`get-dem`) als **Raster Layer**.
* Klicken Sie im Rahmen **Output** auf die Schaltfläche **Browse**, um einen Output-Mesh-Namen im Verzeichnis `/Project Home/` zu definieren, z. B. **prepro-tutorial quality-mesh-interp.2dm**
* Klicken Sie auf **Run**, um das höheninterpolierte Mesh zu erstellen.

```{admonition} Error with BASEmesh v2.0.9 - Interpolation via DEM not working
:class: error

Seit BASEmesh v2.0.9 erkennt das Fenster **Interpolation** keine **Rasterschicht** (aus dem Dropdown-Menü kann nichts ausgewählt werden). Ein funktionaler Workaround besteht darin, das Digitales Oberflächenmodell (DOM)-Raster in eine Mesh-Datei umzuwandeln:

1. Konvertieren Sie die Digitales Oberflächenmodell (DOM) in eine Punktformdatei (**Raster in Vektor**) und stellen Sie sicher, dass die Attributtabelle des Punktes mit Erhebungen gefüllt ist.
2. Verwenden Sie das Tool **TIN Mesh Creation**, um ein TIN Elevation Mesh mit Elevation-Daten zu generieren.
3. Wählen Sie im BASEmesh-Tool **Interpolation** die Option **Interpolation über Elevation Mesh** und wählen Sie das zuvor erstellte TIN Elevation Mesh aus.
4. Klicken Sie auf **Run**, um mit dem Tutorial fortzufahren.

Um die oben genannten Konvertierungstools zu finden, gehen Sie zu QGIS **Processing ** Top-Menü > **Toolbox ** und geben Sie die Toolnamen im Feld *search...* ein.

```

```{figure} ../img/qgis/bm-mesh-interpolation.png
:alt: qgis quality mesh interpolation basement
:name: qgis-qualm-interp

BASEmeshs Z-Wert (Höhe) Interpolationswerkzeug und Setup, um dem Qualitätsnetz untere Höhenwerte zuzuweisen.
```

Stellen Sie nach der Höheninterpolation sicher, dass die Höhen korrekt zugewiesen sind (dh die **Bed Elevation** sollte Werte zwischen **367** und **387** m a.s.l. angenommen haben). Um die Layer-Visualisierung (Symbologie) zu ändern, doppelklicken Sie auf das neue **prepro-tutorial quality-mesh-interp** und gehen Sie zum **Symbology**-Band. Wählen Sie **Graduated** ganz oben im Fenster, setzen Sie den **Wert** auf Z, **Methode** auf COLOR, wählen Sie eine Farbrampe und klicken Sie auf den **classify** unten (unterer Teil des Fensters). Klicken Sie auf **Apply** und **OK**, um die Symbolisierungseinstellungen zu schließen. {numref}`Figure %s <qgis-verify-qualm>` zeigt eine Beispielvisualisierung des höheninterpolierten Gitters.

```{figure} ../img/qgis/bm-mesh-interp-success.png
:alt: basemesh verify interpolated quality mesh
:name: qgis-verify-qualm

Überprüfen Sie die Höheninterpolation mit Hilfe von abgestuften Farbrampen.
```

(qgis4bm)=
## Nutzung mit BASEMENT

The 2dm mesh file produced in this tutorial can be directly used with {ref}`chpt-basement`, where only the definition of properties of the geometric (e.g., roughness coefficients) and liquid (e.g., discharges) are required as explained later.
