---
description: Vorverarbeitungs-Tutorial für TELEMAC mit QGIS und BlueKenue, um ein SELAFIN (SLF) Rechennetz aus einem Digital Elevation Model (Digitales Oberflächenmodell (DOM)) für hydrodynamische Simulationen zu erzeugen.
---

(slf-prepro-tm)=
# Vorverarbeitung

```{admonition} Requirements
:class: attention
Dieses Tutorial richtet sich an **fortgeschrittene Anfänger ** und bevor Sie in dieses Tutorial eintauchen, stellen Sie sicher:

* Follow the installation instructions for {ref}`qgis-install` in this eBook.
* Read (or watch) and understand this eBook's {ref}`qgis-tutorial`.
* Installieren Sie {ref}`BlueKenue <bluekenue>`.
```

Die ersten Schritte bei der numerischen Modellierung eines Flusses mit TELEMAC bestehen in der Umwandlung eines digitalen Höhenmodells (**{term}`Digitales Oberflächenmodell <DEM>`**) in ein Rechennetz. Dieses Tutorial führt durch die Erstellung von:

* A QGIS project for creating a computational mesh (similar to the {ref}`BASEMENT <qgis-prepro-bm>` pre-processing).
* Optional wird die Mesh-Generierung mit der BlueKenue<sup>TM</sup>-Software vorgestellt.
* A {ref}`BlueKenue <bluekenue>` workspace to interpolate terrain elevations from a {term}`Digitales Oberflächenmodell <DEM>`, including the export of a mesh to the SELAFIN/SERAFIN (`.slf`) geometry format for Telemac, and the definition boundary edges.

At the end of this tutorial, {ref}`chpt-telemac` users will have generated a computational mesh in the `*.slf` file format, which is ready to use for the {ref}`Telemac2d steady <telemac2d-steady>` simulation tutorial. Additional materials and intermediate data products are provided in this eBook's supplemental [telemac](https://github.com/hydro-informatics/telemac) data repository.

```{admonition} Platform compatibility
:class: tip
Alle in diesem Tutorial vorgestellten Softwareanwendungen können auf * Linux *, * Windows * und möglicherweise auch * MacOS * (nicht getestet) Plattformen ausgeführt werden.
```

(tm-qgis-prepro)=
# QGIS

## Erstellen und Einrichten eines neuen Projekts
Launch QGIS and {ref}`create a new QGIS project <qgis-project>` to get started with this tutorial. As featured in the {ref}`qgis-tutorial`, set up a coordinate reference system ({term}`Koordinatenreferenzsystem <CRS>`) for the project. This example uses data of a river in Bavaria (Germany, UTM zone 33N), which requires the following {term}`Koordinatenreferenzsystem <CRS>`:

* Gehen Sie im QGIS-Spitzenmenü zu **Project** > **Properties**.
* Aktivieren Sie den **Koordinatenreferenzsystem**-Tab.
* Geben Sie `UTM zone 33N` ein und wählen Sie das Koordinatenreferenzsystem aus, das unter {numref}`Fig. %s <qgis-crs-utm33n>`: EPSG 32633 gezeigt wird.
* Klicken Sie auf **Apply** und **OK**.

Beachten Sie, dass sich das mit TELEMAC verwendete Koordinatenreferenzsystem von dem mit BASEMENT unterscheidet, um die Kompatibilität von Geodatenprodukten von QGIS mit {ref}`BlueKenue <bluekenue>` zu ermöglichen. Auch EPSG 32633 ist wegen seiner geringen Präzision (bestenfalls 2 m) keine gute Wahl, aber es wird die Arbeit für dieses Tutorial erledigen.

```{figure} ../img/qgis/crs-utm-33n.png
:alt: qgis set coordinate reference system crs germany utm zone 33n Inn river
:name: qgis-crs-utm33n

UTM-Zone 33N (WGS84) als Projekt Koordinatenreferenzsystem definieren.
```

```{admonition} Save the project...
:class: tip
Speichern Sie das QGIS-Projekt (**Project** > **Save As...**), zum Beispiel mit dem Namen **prepro-tutorial.qgz**.
```

(tm-qgis-plugins)=
## Plugins von Drittanbietern

Die TELEMAC Tutorials basieren auf dem BASEmesh Plugin und dem *PostTelemac* Plugin. Zu diesem Zweck öffnen Sie den **QGIS-Plugin-Manager ** (** Plugins ** Menü > ** Plugins verwalten und installieren **), um das ** Plugins ** Fenster zu öffnen ({numref}`Fig. %s <open-qgis-plugin-manager>`).

```{figure} ../img/qgis/plugin-manager-open.png
:alt: qgis basement telemac plugins manager
:name: open-qgis-plugin-manager

Open QGIS Plugins Manager.
```

Fügen Sie im Fenster **Plugins** beide Plugins wie folgt hinzu:

* BASEmesh requires to add the developer's plugin repository (more details are available in the {ref}`BASEMENT pre-processing <get-basemesh>` tutorial):
  * Gehe zum Tab **Einstellungen **.
  * Scrollen Sie nach unten (**Plugin Repositories** listbox in {numref}`Fig. %s <qgis-plugins2>`), klicken Sie auf **Add...**.
  * Im Popup-Fenster geben Sie ein:
    * ein Name für das neue Repository, zum Beispiel `BASEmesh Plugin Repository`;
    * the repository address: [https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml).
  * Klicken Sie auf **OK**. Das neue Repository sollte nun in der Liste **Plugin Repositories** sichtbar sein.
* Installieren Sie das BASEmesh Plugin:
  * Gehen Sie auf die Registerkarte **All** (immer noch im Fenster *Plugins*) und geben Sie `basemesh` im Suchfeld ein.
  * Finden Sie das **neueste BASEmesh ** (dh **Verfügbare Version ** >= 2.0.0) Plugin und klicken Sie auf **Install Plugin **.
* Um das [**PostTelemac** Plugin](https://github.com/Artelia/PostTelemac/wiki#T45) Typ `posttelemac` in der Registerkarte **All** zu installieren und auf **Install Plugin** zu klicken.
* Nach der erfolgreichen Installation ** Schließen** das **Plugins** Fenster.

Now, the *BASEmesh 2* plugin should be available in QGIS' *Plugins* menu and the [PostTelemac](https://github.com/Artelia/PostTelemac/wiki#T45) <img src="../img/qgis/sym-posttm.png"> symbol should be visible in QGIS' menu bar.

```{admonition} Why use BASEmesh for TELEMAC?
Durch die Verwendung von BASEmesh verwendet dieses Tutorial den effizienten Mesh-Generator von BASEMENT, um die Anzahl der Arbeitsschritte in BlueKenue<sup>TM</sup> zu minimieren. Der Grund für diesen Ansatz ist, dass QGIS stabiler und benutzerfreundlicher ist als BlueKenue<sup>TM</sup>, zum Beispiel, um Zeichnungsfehler von Grenzlinien zu korrigieren.
```

(get-dem-xyz)=
## Belastung Digitales Oberflächenmodell (DOM)

This tutorial uses height information that is stored in a {term}`Digitales Oberflächenmodell <DEM>`. For the QGIS section, preferably use the {term}`GeoTIFF` {term}`Digitales Oberflächenmodell <DEM>` with UTM zone 33N as {term}`Koordinatenreferenzsystem <CRS>` as follows:

* [** Laden Sie das GeoTIFF Digitales Oberflächenmodell (DOM)**](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem-utm33n.tif) herunter und speichern Sie es im gleichen Ordner (`/ProjectHome/` oder einem Unterverzeichnis) wie das oben erstellte **qgz**-Projekt.
* Fügen Sie die heruntergeladene Digitales Oberflächenmodell (DOM) als neue Rasterschicht in *QGIS* hinzu:
  * Im *QGIS*' **Browser**-Bereich finden Sie das **ProjectHome**-Verzeichnis, in dem Sie das Digitales Oberflächenmodell (DOM) *tif* heruntergeladen haben.
  * Ziehen Sie das Digitales Oberflächenmodell (DOM) *tif* aus dem Ordner **ProjectHome** in das **Layer**-Panel von QGIS.
* Um später die Abgrenzung bestimmter Regionen des Flussökosystems zu erleichtern, fügen Sie unter {term}`Digitales Oberflächenmodell <DEM>` ein {ref}`satellite imagery basemap <basemap>` (XYZ-Kachel) hinzu und passen Sie die Ebenensymbologie an.

```{admonition} What are QGIS panels, what is a basemap, and how can I re-order layers?
:class: tip
Erfahren Sie mehr im *QGIS* Tutorial unter {ref}`qgis-tbx-install`.
```

Die **dem-utm33n**-Ebene sollte nun im Viewport sichtbar und im **Layers**-Panel aufgeführt sein. **Klicken Sie mit der rechten Maustaste auf die **dem-utm33n**-Ebene und wählen Sie **Zoom in Layer(s)**, um die Ebene anzuzeigen.

````{admonition} Alternatively work with a .xyz DEM pointcloud
:class: note, dropdown
This tutorial uses later in the section on BlueKenue<sup>TM</sup> a `*.xyz` file as {term}`Digitales Oberflächenmodell <DEM>`, which was derived from the {term}`GeoTIFF` using the workflow described in the {ref}`QGIS tutorial <make-xyz>`. The `*.xyz` file can also be used with QGIS and it can be [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem.xyz). To **import** the **dem.xyz** file in QGIS, open the *Data Source Manager* from the **Layer** top menu, select **Add Layer** and **Add Delimited Text Layer...**. In the opening **Data Source Manager** window (see {numref}`Fig. %s <qgis-import-xyz>`) take the following actions:

* Select the downloaded `dem.xyz` file in the **file name** field.
* Stellen Sie im **File Format**-Rahmen sicher, dass Sie **benutzerdefinierte Trennzeichen** auswählen und das **Space**-Grenzfeld aktivieren.
* In the **Record and Fields Options** frame, set the **Number of header lines to discard** to `13` and check the **First record has field names** box.
* In the **Geometry Definition** frame, select `:EndHeader` as **X field**, `field_2` as **Y field**, and `field_3` as **Z field**. Select `Project CRS: ESRI:32633 - WGS 84 / UTM zone 33N` as **Geometry CRS**.
* Klicken Sie auf **Add** und **Close** das Fenster *Data Source Manager*.

```{figure} ../img/qgis/import-dem-xyz.png
:alt: qgis import XYZ point cloud file dem
:name: qgis-import-xyz

Import the `*.xyz` point cloud as QGIS layer.
```
````


## Snapping ermöglichen
Es ist wichtig, dass sich die Linien nicht überschneiden, um mehrdeutige oder fehlende Definitionen von Regionen zu vermeiden und sicherzustellen, dass die Grenzlinien geschlossen werden. Aktivieren Sie daher Snapping:

* Aktivieren Sie die *Snapping Toolbar *: **View * > **Snapping Toolbar *
* In der **Snapping-Symbolleiste** > **Snapping** aktivieren <img src="../img/qgis/snapping-horseshoe.png">
* Ermöglichen Sie Snaping für
  * **Vertex**, **Segment** und **Mitte der Segmente** <img src="../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../img/qgis/snapping-intersection.png">.
  * **Self Snapping** <img src="../img/qgis/sym-self-snapping.png">.

(make-tm-shp)=
## Modellgrenzen und Breaklines

This section resembles the instructions of the {ref}`BASEMENT pre-processing <make-2dm>` tutorial to generate an {term}`SMS 2dm` mesh file. The differences are that the shapefiles for the TELEMAC pre-processing use the *UTM zone 33N* {term}`Koordinatenreferenzsystem <CRS>` and that the height (elevation) interpolation needs to be done with the BlueKenue<sup>TM</sup> software to generate liquid boundary lines and an `*.slf` geometry file for TELEMAC. The generation of the {term}`SMS 2dm` mesh relies on the {ref}`QGIS BASEmesh plugin <get-basemesh>` and requires drawing a

* {ref}`Line Shapefile <create-line-shp>` namens *breaklines.shp*, das Modellgrenzen und interne Bruchlinien zwischen Modellregionen mit unterschiedlichen Eigenschaften enthält;
* {ref}`Line Shapefile <create-line-shp>` aufgerufen *liquid-boundaries.shp*, das Modellgrenzen für die Zuweisung von Zu- und Abflussbedingungen enthält;
* {ref}`Point Shapefile <create-point-shp>` heißt *region-pts.shp* und enthält Markierungen für die Definition von Merkmalen von Modellregionen.

{numref}`Figure %s <tm-shapefiles>` bietet einen Überblick über die Shapefiles, die für die Generierung eines Qualitäts-Meshs mit dem BASEmesh-Plugin gezeichnet werden sollen.

```{figure} ../img/telemac/tm-prepro-illu.png
:alt: qgis telemac basemesh point line shapefiles
:name: tm-shapefiles

The breaklines, liquid boundaries, and region points shapefile to draw for creating a 2dm quality mesh with the BASEmesh plugin (background map: {cite:t}`googlesat` satellite imagery).
```

(tm-bm-breaklines)=
### Breaklines und Model Outline

The model boundary defines the model extent and can be divided into regions with different characteristics (e.g., roughness values) through **breaklines**. Breaklines indicate, for instance, channel banks and the riverbed (main channel), and need to be inside the DEM extents. Boundary lines and breaklines are stored in a {ref}`Line Shapefile <create-line-shp>` that BASEmesh uses to find both model boundaries and internal breaklines between model regions. For this purpose, {ref}`create-line-shp` and call it **breaklines.shp** (**Layer** > **Create Layer** > **New Shapefile Layer**). Click on QGIS' **Layers** menu > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <tm-qgis-new-lyr>`). Make sure to select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`Koordinatenreferenzsystem <CRS>` <img src="../img/qgis/sym-crs.png">. Do not add any field.

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: tm-qgis-new-lyr

Erstellen Sie ein neues Shapefile aus dem QGIS Layers-Menü.
```

Beginnen Sie mit dem Bearbeiten von **breaklines.shp**, indem Sie auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> klicken und zeichnen Sie die in {numref}`Fig. %s <tm-shapefiles>` angegebenen Bruchlinien, indem Sie ** Line Feature** <img src="../img/qgis/sym-add-line.png"> aktivieren, was Folgendes beinhaltet:

* Die **Grenzen des** Modells links und rechts **Grenzen der Überschwemmungsgebiete**:
  * Begrenzen Sie die äußeren Grenzen der Auen.
  * Make sure that all points and lines are inside the {ref}`DEM layer <get-dem>`.
  * Überqueren Sie nicht den Fluss (benetzter Bereich, der durch die Satelliten-Basemap angezeigt wird).
  * **Beende jede Zeile mit einem **Rechtsklick**.
* Die **Unterbrechungen der linken Bank (LB) und rechten Bank (RB)**:
  * Zeichnen Sie Linien entlang des benetzten Hauptkanals, die in den Satellitenbildern angezeigt werden (Basiskarte).
  * Stellen Sie sicher, dass die Leitungsenden perfekt mit den zuvor erstellten Auengrenzlinien übereinstimmen (Schnappen ist erforderlich); Daher müssen die Trennlinien des Hauptkanals und die Auengrenzlinien die Auen ohne Lücke zwischen den Linien einschließen.
* **Breaklines von Kiesbänken**:
  * Zeichnen Sie Linien entlang der Schotterbänke, die in der Satellitenbild-Basiskarte im Hauptkanal sichtbar sind.
  * Stellen Sie sicher, dass die Leitungsenden perfekt mit den zuvor erstellten Hauptkanaltrennlinien übereinstimmen (Verwendung von Schnappschüssen); Daher müssen die harten Trennlinien des Hauptkanals und die Schotterbanktrennlinien die Schotterbänke ohne Lücke zwischen den Linien einschließen.
* Optional: **Unterbrechungen von Blockrampen**:
  * Finden Sie die rauen Blockrampen (ausblasende Gewässer) in der Satellitenbild-Basiskarte und beschreiben Sie sie, indem Sie Linien über den benetzten Hauptkanal zeichnen.
  * Stellen Sie sicher, dass die Leitungsenden perfekt mit den Hauptkanaltrennlinien übereinstimmen; Daher müssen die harten Trennlinien des Hauptkanals und die Blockrampentrennlinien die Blockrampen ohne Zwischenraum zwischen den Leitungen einschließen.

To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">. Finally, save the new lines (edits of **breaklines.shp**) by clicking on the **Save Layer Edits** <img src="../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../img/qgis/yellow-pen.png"> symbol.


```{admonition} Troubles with drawing boundaries and breaklines?
:class: tip
Laden Sie die [zipped breaklines shapefile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) in der obigen Abbildung gezeigt und entpacken Sie es in den Projektordner, zum Beispiel `/ProjectHome/shapefiles/breaklines.[SHP]`.
```

```{admonition} Draw boundaries of complex DEMs...
:class: tip
Drawing boundaries manually around large {term}`Digitales Oberflächenmodell <DEM>`s can be very time consuming, in particular, if the raw data are a point cloud and not yet converted to a {ref}`raster`.

Wenn Sie es mit einer Punktwolke zu tun haben, sollten Sie QGIS verwenden [Convex Hull tool](https://docs.qgis.org/3.16/en/docs/training_manual/vector_analysis/spatial_statistics.html?highlight=convex%20hull#basic-fa-create-a-test-dataset), das ein eng umgrenzendes Polygon um Punkte zeichnet].

If you are dealing with a large {term}`GeoTIFF`, consider using QGIS' [Raster to Vector](https://docs.qgis.org/3.16/en/docs/training_manual/complete_analysis/raster_to_vector.html) tool.
```

(tm-bm-liquid-boundaries)=
### Flüssige Grenzen

The **liquid boundaries** define where hydraulic conditions, such as a given discharge or stage-discharge relationship, apply at the model inflow (upstream) and outflow (downstream) limits. Thus, a functional river model requires at least one inflow boundary (line) where mass fluxes enter the model and one outflow boundary (line) where mass fluxes leave the model. For this purpose, {ref}`create-line-shp` called **liquid-boundaries.shp**, select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`Koordinatenreferenzsystem <CRS>` <img src="../img/qgis/sym-crs.png">, and define **two text data fields** named **type** and **stringdef**. Make sure that **snapping** is still **enabled** and **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **liquid-boundaries.shp**. Then draw two lines:

* Aktivieren Sie **Hinzufügen-Funktion** <img src="../img/qgis/sym-add-line.png">.
* Draw an inflow boundary line (light blue line on the left of {numref}`Fig. %s <tm-shapefiles>`):
  * Zoomen Sie auf den Zuflussbereich der Digitales Oberflächenmodell (DOM)-Grenzen, wo es eine **Lücke zwischen** den oben erstellten **Überflutungsgrenzlinien** gibt.
  * Beginnen Sie mit dem Zeichnen einer Linie an einem Ufer (oben in der unteren Abbildung) und bewegen Sie sich zum anderen Ufer, um ungefähr sieben weitere Punkte über den Fluss zu machen.
  * Der **letzte Punkt ** muss mit dem Ende der **Überflutungsgrenze der anderen Bank ** zusammenfallen **.
  * ** Beenden Sie die Zeile mit einem **Rechtsklick** und geben Sie `Inflow` im **Typ**-Feld und `inflow` im **Stringdef**-Feld ein (der Fall ist wichtig).
* Zeichnen Sie eine Outflow-Grenzlinie (hellblaue Linie rechts von {numref}`Fig. %s <tm-shapefiles>`):
  * Zoomen Sie auf den Abflussbereich der Digitales Oberflächenmodell (DOM)-Grenzen, wo es eine **Lücke zwischen** den oben erstellten **Überflutungsgrenzlinien** gibt.
  * Beginnen Sie mit dem Zeichnen einer Linie an einem Ufer (oben in der unteren Abbildung) und bewegen Sie sich zum anderen Ufer, um ungefähr sieben weitere Punkte über den Fluss zu machen.
  * Der **letzte Punkt ** muss mit dem Ende der **Überflutungsgrenze der anderen Bank ** zusammenfallen **.
  * ** Beenden Sie die Zeile mit einem **Rechtsklick** und geben Sie `Outflow` im **Typ**-Feld und `outflow` im **Stringdef**-Feld ein (der Fall ist wichtig).


To **correct drawing errors** use the **Vertex Tool** <img src="../img/qgis/sym-vertex-tool.png">.

Speichern Sie schließlich die flüssigen Grenzlinien (Bearbeitungen von **liquid-boundaries.shp**), indem Sie auf das **Layer Edits** <img src="../img/qgis/sym-save-edits.png"> Symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.

```{admonition} Troubles with drawing the liquid boundary lines?
:class: tip
Laden Sie die [zipped liquid-boundaries shapefile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip)] herunter und entpacken Sie sie in den Projektordner, zum Beispiel `/ProjectHome/shapefiles/liquid-boundaries.[SHP]`.
```

### Regionspunktmarkierungen

**Regionspunkt-Marker werden innerhalb von Regionen platziert, die durch Grenzlinien und Bruchlinien definiert sind. Jeder Regionsmarker (d.h. ein Punkt irgendwo im Regionsbereich) weist beispielsweise eine Materialkennung (MATIDs) und eine maximale Mesh-Zellfläche zu. Die MATID wird (derzeit) nicht für TELEMAC (nur BASEMENT) benötigt, aber die Einträge im Feld **max area** bestimmen die Zellgröße der Maschenregionen und haben große Auswirkungen auf die Qualität und Effizienz der TELEMAC-Simulation. Um Regionspunkte zu zeichnen, heißt {ref}`create a new point shapefile <create-point-shp>` **raster-points.shp** mit den folgenden Definitionen (ähnlich {numref}`Fig. %s <qgis-reg-lyr>` im BASEMENT-Vorverarbeitungs-Tutorial):

* Definieren Sie den ** Dateinamen** als **region-points.shp** (oder ähnlich)
* Stellen Sie sicher, dass der **Geometrietyp** **Point** ist
* Select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`Koordinatenreferenzsystem <CRS>` <img src="../img/qgis/sym-crs.png">
* Fügen Sie drei **New Field**s hinzu (zusätzlich zum Standardfeld **Integer** Typ **ID**):
  * **max area** = **Dezimalzahl** (**Länge** = 10, **Präzision** = 3)
  * **MATID** = **Ganzzahl** (**Länge** = 3)
  * **type** = **Textdaten** (**Länge** = 20)
* Klicken Sie auf **OK**, um das neue Punkt-Shapefile zu erstellen.

Consider to **deactivate snapping** for drawing the region markers because the points should not coincide with any line. Then, **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **region-points.shp** file and activate **Add Point Feature** <img src="../img/qgis/sym-add-point.png">. Draw one point in every area section that is enclosed by breaklines and (liquid) boundary lines (refer to the round and triangular-shaped points in {numref}`Fig. %s <tm-shapefiles>`). Depending on the apparent area type from the satellite imagery basemap, assign one of the four regions listed in {numref}`Tab. %s <tab-tm-region-defs>` to every point.

```{list-table} Region names and their **max_area**, **MATID**, and **type** field values.
:header-rows: 1
:name: tab-tm-region-defs

* - Region
  - Flussbett
  - Blockrampen
  - Grasbanken
  - Überschwemmungsgebiete
* - **max area**
  -  25,0
  -  20.0
  -  25,0
  -  80,0
* - **MATID**
  - 1
  - 2
  - 3
  - 4
* - **Typ**
  - Flussbett
  - block ramp
  - gravel bank
  - Überschwemmungsgebiet
```

Speichern Sie nach dem Zeichnen eines Punktes in jedem geschlossenen Bereich die Regionspunktmarkierungen (Bearbeitungen von **region-points.shp**), indem Sie auf das **Layer Edits** <img src="../img/qgis/sym-save-edits.png"> Symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.

```{admonition} Troubles with drawing the region marker points?
:class: tip
Laden Sie die [zipped region-points shapefile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/region-points.zip)] herunter und entpacken Sie sie in den Projektordner, zum Beispiel `/ProjectHome/shapefiles/region-points.[SHP]`.
```

(tm-qualm)=
## Qualitätsmaschen (.2dm)

*BASEmesh*'s quality mesh tool creates a computationally efficient triangular mesh based on {cite:t}`shewchuk1996` and within the above-defined model boundaries. The tool associates mesh properties with the regions shapefile, but it does not include elevation data. Thus, after generating a quality mesh in {term}`SMS 2dm` format, elevation information needs to be added with the BlueKenue<sup>TM</sup> software. To generate the quality mesh, open BASEmesh's **QUALITY MESHING** tool (QGIS' **Plugins** > **BASEmesh 2** > **QUALITY MESHING**). Make the following settings in the popup window (see also {numref}`Fig. %s <fig-tm-qualm>`):

* Rahmen für Triangulationsbeschränkungen:
  * **Breaklines** = **breaklines** (siehe {ref}`make-tm-shp`).
  * Behalten Sie alle anderen Standardwerte.
* Regionsrahmen:
  * ** Aktivieren Sie das Kontrollkästchen Regionen**.
  * **Region marker layer** = **regions-points** (siehe {ref}`make-tm-shp`).
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
  * Klicken Sie auf die Schaltfläche **Browse...** und definieren Sie einen **2dm** Dateinamen im `/ProjectHome/` Verzeichnis, z. B. **prepro-tutorial quality-mesh.2dm**.
* Klicken Sie auf die Schaltfläche **Run**, um das Qualitätsnetz zu erstellen.


```{figure} ../img/qgis/bm-quality-meshing-success.png
:alt: basement qgis quality mesh tin
:name: fig-tm-qualm

Definitionen, die in BASEmeshs Quality Meshing Tool gemacht werden müssen.
```

Qualitätsverzahnung kann eine kurze Zeit dauern. Nach einer erfolgreichen Mesh-Generierung wurde die Datei **prepro-tutorial quality-mesh-interp.2dm** generiert und erscheint automatisch in QGIS als einfarbige Oberfläche mit `0-0` **Bed Elevation**. Der nächste Abschnitt zeigt die Interpolation von Höhendaten mit der BlueKenue<sup>TM</sup>Software.

```{admonition} Troubles with running the quality mesh generator?
:class: tip
Laden Sie die [Tutorialqualität Mesh file](https://github.com/hydro-informatics/telemac/raw/main/meshes/prepro-tutorial_quality-mesh-utm33n.2dm)] herunter und speichern Sie sie im Projektordner, zum Beispiel `/ProjectHome/meshes/prepro-tutorial_quality-mesh-utm33n.2dm`.
```

(bk-tutorial)=
# BlueKenue

(bk-intro)=
## Beginnen Sie
Dieser Abschnitt enthält die {ref}`BlueKenue <bluekenue>`-Software, um Geländehöhen aus einer {term}`Digitales Oberflächenmodell <DEM>`.xyz-Datei in einem {term}`SMS 2dm`-Mesh zu interpolieren, das Mesh in das Geometrieformat SELAFIN/SERAFIN (`*.slf`) für TELEMAC zu exportieren und Grenzlinien zu definieren.

In addition, the {ref}`Meshing with BlueKenue <bk-meshing>` section explains the mesh generation with BlueKenue<sup>TM</sup>, which might be unstable because of program crashes and inflexible for correcting line drawing errors. Still, meshing with BlueKenue<sup>TM</sup> might be desirable to create a computational mesh with long triangular cells that approximately follow the river streamlines (i.e., using a channel sub-mesh).

Um sich mit BlueKenue<sup>TM</sup> vertraut zu machen, starten Sie die Software (weitere Details unter {ref}`installation chapter <bluekenue>`) und suchen Sie

* der **WorkSpace** Browser (links im Fenster),
* den Eintrag **Data Items** im **WorkSpace**, in dem Dateiobjekte aufgelistet werden,
* den **Views**-Eintrag im **WorkSpace**, wobei standardmäßig ein **2D-Ansicht (1)**-Eintrag erscheint und eine *3D-Ansicht* aus dem **Window**-Top-Menü > **Neue 3D-Ansicht** hinzugefügt werden kann.

Werfen Sie einen Blick auf das Menü **File**, das Folgendes ermöglicht:

* Erstellen Sie **New** BlueKenue<sup>TM</sup>Objekte wie SELAFIN, Conlim Boundary Condition, T3 Mesh Generator oder 2D Interpolator Objekte.
* **Open** file types such as `*.slf` geometry files or `*.xyz` point clouds.
* **Import** Dateien wie:
  * ein **ArcView Shapefile** (lesen Sie mehr über {ref}`shapefiles <shp>`),
  * an {term}`SMS 2dm` Mesh like the one created in the above {ref}`pre-processing with QGIS <tm-qualm>`section, or
  * ein {term}`GeoTIFF`-Raster, das in der Praxis nicht mit vielen GeoTIFF-Rastern funktioniert, da BlueKenue<sup>TM</sup> in einem GeoTIFF keine Float32- oder Float64-Daten verarbeiten kann.

Das **Edit**-Menü ermöglicht das Bearbeiten von BlueKenue<sup>TM</sup>Objekten wie Linien, Punktmengen oder Meshes.

Das Menü **Tools** bietet Routinen, die auf bestimmte BlueKenue<sup>TM</sup>Objekte oder zum Kombinieren von Objekten angewendet werden können. Insbesondere wird dieses Tutorial das Tool **Map Objects...** verwenden.

(bk-files)=
## Dateien und Objekte

BlueKenue<sup>TM</sup> Speichert jedes Objekt in softwarespezifischen Dateiformaten und dieses eBook bezieht sich auf die folgenden BlueKenue<sup>TM</sup>Dateiobjekte (alphabetische Reihenfolge der Dateiendungen):

* `*.bc2` Dateien enthalten Conlim Boundary Conditions.
* `*.cli` Dateien enthalten gebrauchsfertige Randbedingungen für TELEMAC und können mit einem `*.bc2` Objekt erzeugt werden.
* `*.i2s` Dateien enthalten geschlossene oder offene Linien.
* `*.in2` Dateien enthalten 2D-Interpolatoren zum Abbilden von Höhendaten (oder anderen) in einem Mesh.
* `*.slf` Dateien enthalten gebrauchsfertige TELEMAC-Meshes, die aus einem BlueKenue<sup>TM</sup>SELAFIN-Objekt und einer `*.t3s`Mesh-Datei stammen.
* `*.t3c` Dateien enthalten BlueKenue<sup>TM</sup> Channel Mesh Generator-Objekte.
* `*.t3m` Dateien enthalten BlueKenue<sup>TM</sup>Mesh-Generator-Objekte, um ein `*.t3s`Mesh-Objekt zu erstellen.
* `*.t3s` Dateien enthalten BlueKenue<sup>TM</sup>Mesh-Objekte, die entweder importiert (z. B. aus einer {term}`SMS 2dm`-Datei) oder mit einem `*.t3m`Mesh-Generator erstellt werden können.

All files that are created with BlueKenue<sup>TM</sup> are based on the ASCII EnSim 1.0 file type standard. The EnSim Core builds on {term}`HDF` and it is documented in BlueKenue<sup>TM</sup>'s [user manual PDF](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/2011_UserManual.pdf) that comes along with the [BlueKenue installer](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) (in BlueKenue<sup>TM</sup> press the `F1` key to open the manual). Note that understanding the EnSim Core can significantly facilitate troubleshooting structural errors of BlueKenue<sup>TM</sup> files.

(bk-xyz)=
## XYZ-Punkte laden

Download the provided [dem.xyz](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem.xyz) point cloud that contains EnSim-formatted 3d coordinates of the river ecosystem {term}`Digitales Oberflächenmodell <DEM>` that will be modelled in this tutorial. The `*.xyz` file was derived from the {term}`GeoTIFF` {term}`Digitales Oberflächenmodell <DEM>` used in the {ref}`QGIS pre-processing <get-dem-xyz>`.

 ```{aside} The .xyz file is not an XYZ tile
 The point cloud in the `*.xyz` file is different than the regular XYZ tile raster that constitutes the {ref}`satellite imagery basemap <basemap>`.
 ```

Um die Datei **dem.xyz** in BlueKenue<sup>TM</sup> zu laden, öffnen Sie sie im Menü **File** (**File** > **Open...**) und führen Sie die folgenden Aktionen im Popup-Fenster aus:

* Navigieren Sie zum Download-Ordner.
* Suchen Sie neben dem Feld **Dateiname:** das Dropdown-Menü des Dateityps und ** ändern Sie den Standard von Telemac Selafin File (`*.slf`) zu Point Sets (`*.pt2`, `*.xyz`, `*.pcl`)**.
* Klicken Sie auf **Öffnen**, um den Import abzuschließen.

Um zu überprüfen, ob die Punktwolke korrekt importiert wurde, **drag** die neuen **dem (Z)** Datenelemente in den **2D View (1)** Eintrag. {numref}`Figure %s <bk-import-xyz>` zeigt die importierte XYZ-Punktwolke in BlueKenue<sup>TM</sup>.

```{figure} ../img/telemac/bk-imported-pts.png
:alt: bluekenue import xyz point cloud DEM
:name: bk-import-xyz

Die bereitgestellte dem.xyz importiert in BlueKenue<sup>TM</sup>.
```

Um den {term}`Koordinatenreferenzsystem <CRS>` des Punktdatensatzes zu überprüfen, klicken Sie mit der rechten Maustaste auf **dem (Z)**, wählen Sie Eigenschaften aus, gehen Sie auf die Registerkarte **Räumlich** und stellen Sie sicher, dass BlueKenue<sup>TM</sup> korrekt identifiziert wurde **UTM Zone 33** im **Koordinatensystem**-Rahmen und **WGS 84** als **Ellipsoid**.


(bk-meshing)=
## BlueKenue Meshing (optional)

```{admonition} Skip this section if you created a *.2dm* quality mesh with BASEMESH
This is an optional section for users who do not want to use QGIS and the BASEmesh plugin for meshing. Generating a mesh with BlueKenue<sup>TM</sup> can be useful, for instance, to produce a computational grid that has triangular cells oriented parallel to the riverbanks (i.e., a channel sub-mesh). Otherwise, **if the `*.2dm` mesh file was created** with QGIS, **jump to the section on creating a {ref}`Selafin Object <bk-create-slf>`**.
```

This section features the basic mesh generation with BlueKenue<sup>TM</sup>, which also runs smoothly on Linux through the {ref}`PlayOnLinux <play-on-linux>` app. Additionall, the Baxter tutorial {cite:p}`baxter2013` provides more details for getting started with BlueKenue along with detailed screenshots.

### Zeichenmodellgrenze (geschlossene Linie)

Beschreiben Sie die Modellgrenze (Outline) mit einem geschlossenen Linienobjekt (siehe auch {numref}`Fig. %s <bk-model-outline>`):

* Erstellen Sie eine neue ** Geschlossene Linie**, indem Sie auf das <img src="../img/telemac/bk-sym-cl.png">-Symbol im Menü BlueKenue<sup>TM</sup> klicken.
* **Zeichne die neue geschlossene Linie:
  * Machen Sie Punkte, indem Sie in der Nähe der äußeren Ausdehnung der Schicht **dem (Z)** im Fenster **2D-Ansichten (1)** klicken. Stellen Sie sicher, dass kein Punkt außerhalb der Region liegt, in der Höhendaten verfügbar sind (d. h. eng **dem (Z)** abgegrenzt).
* Schließen Sie die geschlossene Linie durch Drücken **Esc** ab.
* Nennen Sie die geschlossene Zeile, zum Beispiel `model-outline`.
* **Skip** **Ein neues Attribut** hinzufügen, indem Sie einfach auf **OK** klicken.

```{figure} ../img/telemac/bk-model-outline.png
:alt: bluekenue draw closed line model boundary outline
:name: bk-model-outline

Die geschlossene Linie der Modellgrenzen in BlueKenue<sup>TM</sup>s 2D-Ansichtsfenster.
```

Um den Modellumriss** zu speichern, markieren Sie das neue Closed Line-Objekt im **WorkSpace**-Browser und klicken Sie auf das Symbol <img src="../img/telemac/bk-sym-save.png">. Erwägen Sie, einen neuen Ordner mit dem Namen `bk-mesh` zu erstellen, der alle für das Meshing erforderlichen BlueKenue<sup>TM</sup>-Objekte enthält. Speichern Sie also den Modellumriss (Closed Line), beispielsweise als **/bk-mesh/model-outline.i2s**.

```{admonition} Troubles with drawing the model outline?
:class: tip
Die Gliederung kann auch aus dem Archiv für ergänzende Materialien heruntergeladen werden ([Modell-outline.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/model-outline.i2s)download]. Um die geschlossene Linie aus dem Repository in BlueKenue<sup>TM</sup> zu öffnen, gehen Sie zu **File** > **Open...** > Wählen Sie **Line Sets (`*.i2s`, `*.i3s`)** als Dateityp und navigieren Sie zum Download-Verzeichnis.
```

Der aktuelle Status von BlueKenue<sup>TM</sup> kann in Form einer Datei **workspace.ews** gespeichert werden (**File** > **Save WorkSpace...** > einen Namen definieren). Um den Arbeitsbereich zu speichern, müssen alle BlueKenue<sup>TM</sup>Objekte auf der Festplatte gespeichert werden. Optional laden Sie [meshing-workspace.ews](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/meshing-workspace.ews)] aus dem Archiv für ergänzende Materialien herunter.

```{admonition} Loading a WorkSpace
:class: attention
Theoretisch kann der gespeicherte Arbeitsbereich nach dem Schließen von BlueKenue<sup>TM</sup> geladen werden, aber die Operation **Load WorkSpace...** scheitert oft **aus scheinbar willkürlichen Gründen. Dieses Problem ist einer der Gründe, warum QGIS eine bessere Option für Meshing ist.
```

(bk-draw-ol)=
### Zeichnen Sie offene Linien der Kanalbanken

Similar to the {ref}`above-created breaklines in QGIS <make-tm-shp>`, the channel banks can be delineated with Open Line objects. For this purpose create two Open Line objects as follows:

* Erstellen Sie eine neue **Offene Linie**, indem Sie auf das <img src="../img/telemac/bk-sym-ol.png">-Symbol im Menü BlueKenue<sup>TM</sup> klicken.
* **Zeichne die neue offene Linie:
  * Make points by following the blue-ish-green areas as indicated in {numref}`Fig. %s <bk-lines-all>` **2D Views (1)** window (flow direction from left to right).
* Beenden Sie die offene Linie, indem Sie **Esc** drücken.
* Nennen Sie eine offene Linie `LeftBank` und die andere `RightBank`.
* **Skip** ** Hinzufügen eines neuen Attributes zu:** indem Sie einfach auf **OK** klicken.

```{figure} ../img/telemac/bk-lines-all.png
:alt: bluekenue draw open line channel river banks
:name: bk-lines-all

Die finalisierten Open- und Closed-Line-Objekte beschreiben die Modellgrenzen und die Kanalbänke. Die RightBank Open Line wird durch die gestrichelte schwarze Linie und die LeftBank Open Line in rot dargestellt.
```

```{admonition} Troubles with drawing the open lines of the channel banks?
:class: tip
Laden Sie die Zeilen aus dem Repository für ergänzende Materialien herunter. Laden Sie insbesondere [LeftBank.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/LeftBank.i2s) und [RightBank.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/RightBank.i2s)] herunter. Um die Open Line-Objekte aus dem Repository in BlueKenue<sup>TM</sup> zu öffnen, gehen Sie zu **File** > **Open...** > Wählen Sie **Line Sets (`*.i2s`, `*.i3s`)** als Dateityp und navigieren Sie zum Download-Verzeichnis.
```

### Erzeugung von Maschen

BlueKenue<sup>TM</sup> bietet Mesh-Generatoren zum Erstellen von regulären oder unstrukturierten Rechengittern (Meshs). Dieses Beispiel zeigt den **T3-Kanal-Mesher **, um ein Dreiecksnetz zu erzeugen, bei dem zuerst ein Kanalnetz (Untermaschen) erzeugt wird und zweitens ein zusammengesetztes Netz erzeugt wird, das das Kanaluntermaschen in ein gröberes Netz der Auen einbettet. Beginnen Sie zu diesem Zweck mit dem Erstellen eines neuen **T3 Channel Mesher**-Objekts (**File** > **New** > **T3 Channel Mesher**). Im Popup-Fenster:

* **CrossChannelNodeCount** an `20` und
* **AlongChannelInterval** an `15`.

Click **OK** (**not Run**) to close the new T3 Channel Mesh window. Next, drag and drop the above-created **LeftBank** and **RightBank** Open Line objects on their equivalent attributes of the **new T3 Channel Mesh** object in the WorkSpace browser as indicated in {numref}`Fig. %s <bk-channel-mesh>`. Next, generate the channel mesh by double-clicking on the **new T3 Channel Mesh** object and click **Run**. To visualize the resulting **Mesh**, drag it on the **2D View (1)** object.

```{figure} ../img/telemac/bk-channel-mesh.png
:alt: bluekenue create channel mesh
:name: bk-channel-mesh

Erstellen und visualisieren Sie das Kanal-Mesh, nachdem Sie die Open Line-Objekte LeftBank und RightBank auf ihre Namensäquivalente des T3-Kanal-Mesh-Objekts gezogen haben.
```

```{admonition} Troubles with creating the channel mesh?
:class: tip
Laden Sie den [channel-mesh.t3c](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/channel-mesh.t3c) mesh generator] und die [channel-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/channel-mesh.t3) mesh objects] aus dem Archiv für ergänzende Materialien herunter. Um das T3 Mesh-Objekt aus dem Repository in BlueKenue<sup>TM</sup> zu öffnen, gehen Sie zu **File** > **Open...** > Wählen Sie **2D T3 Mesh (`*.t...`)** als Dateityp und navigieren Sie zum Download-Verzeichnis.
```

Als nächstes betten Sie das Kanalgitter in ein gröberes Auengitter ein, indem Sie ein **neues T3 Mesh Generator**-Objekt erstellen (**File** > **New** > **T3 Mesh Generator**). Führen Sie im Popup-Fenster **T3 Mesh** folgende Einstellungen durch (siehe auch {numref}`Fig. %s <bk-t3-mesher>`):

* ** Aktivieren Sie die Checkbox **Resample Outline **.
* Stellen Sie die **Default Edge Length** auf `20` ein.
* Behalten Sie alle anderen Standardwerte.
* Drücken Sie **OK** (**nicht Run**).

```{figure} ../img/telemac/bk-t3-mesher.png
:alt: bluekenue create combined mesh generator
:name: bk-t3-mesher

Richten Sie die Eigenschaften des neuen T3 Mesh Generator-Objekts ein.
```

Definieren Sie die **Outline (Wert)** durch Ziehen (siehe auch {numref}`Fig. %s <bk-mesh-compound>`):

* das oben erstellte **model-outline**-Objekt im **Outline (Value)** des **neuen T3 Mesh** und
* Der Kanal **Mesh** auf dem **SubMeshes**-Attribut des **neuen T3 Mesh**.

Generieren Sie das Verbundnetz durch Doppelklick auf das **neue T3 Mesh**-Objekt und durch Einzelklick auf **Run**. Bestätigen Sie das Fragefeld (*Weiter?* > **Ja**) und drücken Sie **OK**, nachdem der Mesh-Generator fertig ist (*Fertig...*). Um das resultierende **Mesh** zu visualisieren, ziehen Sie es in die **2D-Ansicht (1)**.

```{figure} ../img/telemac/bk-mesh-compound.png
:alt: bluekenue generate combined mesh drag and drop
:name: bk-mesh-compound

Die Verbindung wird nach dem Ziehen des Modellumrisses in der Gliederung (Wert) und des Kanals Mesh im SubMeshes-Attribut des neuen T3-Mesh-Generatorobjekts vermascht.
```

```{admonition} What is the difference between the channel mesher and the mesh generator?
:class: note
{numref}`Figure %s <bk-mesh-compound>` zeigt, dass das Channel Mesh nach den Channelbanken streamline-adjustiert ist. Eine derartige Masche ist bekanntlich für die Rechengeschwindigkeit und Modellstabilität vorteilhaft. Daher ist die Verfügbarkeit des Channel Meshers in BlueKenue<sup>TM</sup> eine Stärke und das **beste Argument dafür, BASEmesh** in QGIS für die Mesh-Generation nicht zu verwenden.
```

```{admonition} Troubles with creating the compound mesh?
:class: tip
Laden Sie die [compound-mesher.t3m](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesher.t3m)] und die [compound-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesh.t3s)-Objekte aus dem Archiv für ergänzende Materialien herunter. Um das T3 Mesh-Objekt aus dem Repository in BlueKenue<sup>TM</sup> zu öffnen, gehen Sie zu **File** > **Open...** > Wählen Sie **2D T3 Mesh (`*.t...`)** als Dateityp und navigieren Sie zum Download-Verzeichnis.
```

(bk-slf)=
## SELAFIN

### Open und Import Zutaten
Ob das Mesh mit BlueKenue<sup>TM</sup> oder QGIS (und dem BASEmesh-Plugin) erstellt wurde, stellen Sie sicher, dass Sie jetzt einen BlueKenue<sup>TM</sup>Workspace haben, in dem nur die XYZ-Punktwolke geladen ist (siehe Abschnitt {ref}`bk-xyz`). Bevor ein SELAFIN-Objekt erstellt werden kann, muss das zuvor erstellte Mesh (dh entweder das [quality-mesh.2dm](https://github.com/hydro-informatics/telemac/raw/main/meshes/prepro-tutorial_quality-mesh-utm33n.2dm)] oder das [compound-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesh.t3s)]) zusätzlich zur Punktwolke in den WorkSpace importiert werden. Die folgenden Anweisungen zeigen den Import und die Verwendung der `*.2dm`-Datei:

* Gehen Sie in BlueKenue<sup>TM</sup> zu **File** > **Import** > **SMS 2DM Mesh**.
* Navigieren Sie im Importfenster zu dem Ordner, in dem sich die `*.2dm`-Datei befindet, wählen Sie die `*.2dm`-Datei aus und klicken Sie auf **Öffnen**.
* Wenn der Prozess * SMS 2d Mesh File lesen * Fertig ... * klicken Sie auf **OK**.

```{admonition} How to load a BlueKenue .T3S mesh file?
:class: note, dropdown
Im Gegensatz zu einer {term}`SMS 2dm` (`*.2dm`) Datei, die *importiert* werden muss, muss eine `*.t3s` Datei in BlueKenue<sup>TM</sup>** geöffnet werden. Zu diesem Zweck öffnen Sie den T3 Mesh (`*.t3s`) aus **File** > **Open...** > wählen Sie **2D T3 Mesh (`*.t...`)** als Dateityp und navigieren Sie zum Download-Verzeichnis. Wählen Sie die `*.t3s`Mesh-Datei und klicken Sie auf **Öffnen**.
```

Ignore warning messages regarding the projection, but make sure that BlueKenue<sup>TM</sup> correctly read the mesh coordinates by **dragging** the imported (or opened) mesh onto the **2D View (1)**. The BlueKenue<sup>TM</sup> window should now look similar to {numref}`Fig. %s <bk-imported-mesh>`.

```{figure} ../img/telemac/bk-imported-mesh.png
:alt: bluekenue import open 2dm t3s mesh drag
:name: bk-imported-mesh

Das importierte Mesh in der 2D-Ansicht (1).
```

(bk-create-slf)=
### SELAFIN-Objekt erstellen

Mit dem offenen *dem.xyz* und dem importierten (oder geöffneten) Mesh sind alle Zutaten verfügbar, die von einem BlueKenue<sup>TM</sup>SELAFIN-Objekt benötigt werden. Erstellen Sie nun ein neues SELAFIN-Objekt:

* Gehen Sie zu **File** > **New** > **SELAFIN Object...**

```{image} ../img/telemac/bk-create-selafin-object.png
```

* Klicken Sie im Popup-Fenster (*Eigenschaften von:new Selafin*) auf **OK** und ein **neues Selafin**-Objekt erscheint im WorkSpace **Data Items**.
* **Rechtsklick** auf das **neue Selafin**-Objekt und **Variable hinzufügen...**
* Führen Sie die folgende Aktion im Fenster ** Neue SELAFIN-Variable hinzufügen** aus:
  * Wählen Sie im Feld **Mesh** das oben importierte (oder geöffnete) Mesh (z. B. `prepro-tutorial_quality-mesh-utm33n.2dm`).
  * Wählen Sie im Feld **Name** **BOTTOM** aus.
  * Wählen Sie im Feld **Units** **M** (d.h. Meter).
  * Behalten Sie alle anderen Standardwerte und klicken Sie auf **OK**.
* Save the new Selafin object by highlighting it in the **Data Item** tree of the WorkSpace and clicking the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Give the mesh a meaningful and short name, such as `qgismesh.slf`.

(bk-2dinterp)=
### 2D Interpolator erstellen

Ein 2D-Interpolator-Objekt ist erforderlich, um Höheninformationen auf das Selafin-Netz abzubilden. Erstellen Sie zu diesem Zweck ein neues 2D-Interpolator-Objekt und kartieren Sie Erhöhungen auf das BOTTOM-Mesh:

* Gehen Sie zu **File** > **New** > **2D Interpolator...** und ein **neues 2D Interpolator** Objekt erscheint im **Datenelement** des WorkSpace.

```{image} ../img/telemac/bk-create-2Dinterpolator.png
```

* **Drag dem (Z)** (d.h. die oben geöffnete *dem.xyz*-Punktwolke) auf das **neue 2D-Interpolator**-Objekt (roter Pfeil in {numref}`Fig. %s <bk-mesh-interpolated>`).
* **Highlight** (klicken Sie auf) das **BOTTOM (Anonymous Attribut)** Mesh-Attribut des oben erstellten SELAFIN-Objekts (z. B. `qgismesh`).
* Mit dem Mesh hervorgehoben, gehen Sie zum **Tools** Top-Menü > **Map Object...**.
* Im öffnenden Fenster **Verfügbare Objekte** wählen Sie den **neuen 2D-Interpolator** und klicken Sie auf **OK**.
* Sobald die *Bearbeitung...* abgeschlossen ist, klicken Sie auf **OK**.
* Speichern Sie die letzten Maschen:
  * The BOTTOM mesh is a BlueKenue<sup>TM</sup> `*.t3s` mesh object; to save it, highlight it in the **Data Items** tree and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Then, save the mesh, for instance, as `BOTTOM.t3s` file.
  * To save the Selafin mesh in its current (with interpolated elevations) state, highlight the Selafin object (e.g., `qgismesh`) and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. This action overwrites the above-saved `*.slf` file (click **Yes** to confirm replacing it).

To verify if the 2D interpolator correctly interpolated the elevations on the BOTTOM mesh, drag the BOTTOM mesh onto the **2D View (1)**. Uncheck the visibility of dem (Z) and the imported (or opened) mesh with a right-click on these elements in the 2D View (1) tree and **deselect** the **Visible** entry. Thus, only the height-interpolated mesh should be visible now, as indicated in {numref}`Fig. %s <bk-mesh-interpolated>`. If the **interpolation has been successful, the mesh is displayed in a variety of (rainbow) colors**. Otherwise, **if the mesh is** completely, monotonously **monochrome (red)**, the elevation **interpolation** has **not** been **successful** and must be repeated (the numerical model cannot work properly without elevation information).

```{figure} ../img/telemac/bk-mesh-interpolated.png
:alt: bluekenue 2dm t3s mesh interpolate height elevation 2D interpolator map object
:name: bk-mesh-interpolated

Das höheninterpolierte Gitter in der 2D-Ansicht (1) mit Anzeige von Drag-and-Drop-Aktionen zum Ausführen des Objekt-Mappings mit einem neuen 2D-Interpolator-Objekt.
```

```{admonition} Troubles with creating the Selafin mesh and or the height interpolation?
:class: tip
Laden Sie das BOTTOM-Mesh und das SELAFIN-Objekt aus dem Archiv für ergänzende Materialien herunter:

* [Download BOTTOM.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/BOTTOM.t3s);
* [Download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf) (**EPSG:6173** - ETRS 89 / UTM-Zone 33N).
```

```{admonition} Roughness zone interpolation.
:class: tip

Similar to the elevation, friction values can be assigned to created zones with different roughness in the study domain. Read more in the spotlight focus on {ref}`roughness (friction) zones <tm-friction-zones>`.
```

(bk-bc)=
## Grenzbedingungen (Conlim - CLI)

### Erstellen von Conlim Object
TELEMAC muss wissen, wie man die äußeren Ränder des Modells (Mesh) behandelt. Zu diesem Zweck müssen allen Knoten, die den `*.slf`mesh-Umriss bilden, Randbedingungen zugewiesen werden:

* Gehen Sie zu **File** > **New** > **Grenzbedingungen (Conlim )...** und ein **neues 2D-Interpolator**-Objekt werden in den **Datenelementen** des WorkSpaces angezeigt.

```{image} ../img/telemac/bk-create-bc.png
```

* Wählen Sie im öffnenden Popup-Fenster (**Available t3s Objects**) das oben erstellte **BOTTOM**-Mesh (d.h. das Mesh mit Höheninformationen) und klicken Sie auf **OK**. Ein neues **BOTTOM BC**-Objekt tritt im **Datenelemente**-Baum des WorkSpace auf.
* Ziehen Sie das neue **BOTTOM BC**-Objekt in die **2D-Ansicht (1)**, wodurch ** die *Verschreibung* von Randbedingungstypen** aktiviert wird (Details im nächsten Abschnitt).

{numref}`Figure %s <bk-bc-types>` veranschaulicht das neue BOTTOM BC-Objekt in der 2D-Ansicht (1) und zeigt an, wo im nächsten Abschnitt vor- und nachgelagerte Flüssigkeitsgrenzen angewendet werden.

```{figure} ../img/telemac/bk-bc-types.png
:alt: bluekenue boundary conditions conlim create upstream downstream
:name: bk-bc-types

Das neue Boundary Conditions (Conlim)-Objekt (BOTTOM BC) in der 2D-Ansicht (1) mit einem qualitativen Überblick über die Position der stromaufwärts gelegenen und stromabwärts gelegenen Grenzen, in denen der vorgeschriebene Fluss (Q) und der vorgeschriebene Fluss (Q) und die Tiefe (H) angewendet werden, wird später im TELEMAC-Setup angewendet.
```

Um das neue BOTTOM BC-Objekt** zu speichern, markieren Sie es im Baum **Datenelemente** und klicken Sie auf das Symbol <img src="../img/telemac/bk-sym-save.png">. Definieren Sie einen Dateinamen wie **`boundaries.bc2`**. Durch das Speichern des Objekts übernimmt das BOTTOM BC-Objekt den neuen Dateinamen (z.B. **boundaries**).

(bk-liquid-bc)=
### Definieren Sie flüssige Grenzen

The default boundary type of the **boundaries** object is **Closed boundary (wall)**. To enable mass (i.e., water, sediment, and/or tracer) fluxes through the model, at least two openings must be drawn into the closed boundary. For this purpose, at least one inflow and one outflow open boundary for liquids must be defined. This tutorial uses this minimum number of required open boundaries (i.e., one upstream inflow and one downstream outflow boundary), which are indicated in {numref}`Fig. %s <bk-bc-types>`.

```{admonition} Liquid boundaries must be defined in BlueKenue
Even though the liquid boundaries are already defined in QGIS (see the {ref}`QGIS section on Liquid Boundaries <tm-bm-liquid-boundaries>`), it is always necessary to define the liquid boundaries in BlueKenue<sup>TM</sup> to fit the node numbers (IDs) of the Selafin mesh.
```

The upstream (inflow) liquid boundary will constitute an **Open boundary with prescribed Q and H** (discharge and water depth corresponding to a {term}`Wasserstands-Abfluss Beziehung <Stage-discharge relation>`) with the code `5 5 5` and the downstream outflow (liquid) boundary will constitute an **Open boundary with prescribed H** with the code `5 4 4` (i.e., prescribed water depth). These types of boundary conditions are required for a dry initialization of the model. In practice, the downstream boundary should be located be at a gauging station where a {term}`Wasserstands-Abfluss Beziehung <Stage-discharge relation>` has been calibrated with historic data. To back-calculate cross-section averaged roughness from a {term}`Wasserstands-Abfluss Beziehung <Stage-discharge relation>`, take a look at the {ref}`Python exercise on 1-d hydraulics for solving the Manning-Strickler <ex-1d-hydraulics>` formula.

````{admonition} Drawing boundary conditions for mass balance

The boundary condition settings affect mass balance, which is a crucial criterion for a sound numerical model. Read more in the spotlight focus on setting up {ref}`boundary conditions for mass balance<foc-mass-bc>`. Also, to avoid computational issues, define liquid boundary lines only along the channel bottom as illustrated in the below {numref}`Fig. %s <draw-inflow-pre-slf>`.

```{figure} ../img/telemac/cross-section-sx.png
:alt: draw bluekenue liquid boundary conditions conlim upstream inflow
:name: draw-inflow-pre-slf
:width: 75%

Der rot hervorgehobene Teil dieses qualitativen Querschnitts sollte als Zufluss- (vorgelagerte) Randbedingung definiert werden. Mesh-Knoten an den Flussufern und auf den Auen sollten nicht enthalten sein.
```
````


To assign the two liquid boundary lines, zoom into the downstream and upstream regions indicated in  {numref}`Fig. %s <bk-bc-types>` and create both boundaries as follows (toggle tabs):

`````{tab-set}
````{tab-item} Upstream boundary
* Zoomen Sie in die **upstream** Region, die unter {numref}`Fig. %s <bk-bc-types>` angegeben ist.
* Suchen Sie die Hauptkanalbänke entsprechend den Trennlinien in QGIS ({ref}`see above <tm-bm-breaklines>`) oder BlueKenue<sup>TM</sup> ({ref}`see above <bk-draw-ol>`).
* **Doppelklicken** auf einen ** Knoten bei einer Bank** des Modells (egal welche Bank), halten Sie dann ** die ** Umschalttaste und **Doppelklicken** auf einen ** Knoten bei der anderen Bank**, um die Zuflusslinie (lila) hervorzuheben (siehe {numref}`Fig. %s <bk-boundary-us>`).
* **Klicken Sie mit der rechten Maustaste auf die lila Zuflussleitung und wählen Sie ** Grenzsegment hinzufügen **.
* Führen Sie im Öffnungsfenster (**CONLIM Boundary Segment Editor**) folgende Einstellungen aus:
  * Definieren Sie **Boundary Name** als `upstream`.
  * Im Feld **Grenzcode** wählen Sie `Open boundary with prescribed Q and H` (`5 5 5`).
  * Behalten Sie alle anderen Standardwerte und klicken Sie auf **OK**.
* ** Speichern Sie das Objekt **boundaries**, indem Sie auf das Symbol <img src="../img/telemac/bk-sym-save.png"> klicken und bestätigen Sie das Überschreiben `boundaries.bc2` (d.h. klicken Sie auf **Yes**).

** Wechseln Sie zu** der **Downstream-Grenze**, um die Abflussbedingungen gemäß {numref}`Fig. %s <bk-boundary-ds>` zu definieren.

```{figure} ../img/telemac/bk-bm-boundary-us.png
:alt: bluekenue boundary conditions conlim create upstream prescribed discharge flow
:name: bk-boundary-us

Die vorgelagerte Abgrenzung. Doppelklicken Sie auf einen Knoten bei einer Bank, halten Sie dann die **Shift**-Taste und Doppelklicken Sie auf einen Knoten bei der anderen Bank, um die Zuflusslinie (lila) hervorzuheben. Beachten Sie, dass BOTTOM BC möglicherweise mit dem Namen *boundaries* angezeigt wird, wenn das Objekt als *boundaries.bc2* gespeichert wurde.
```
````

````{tab-item} Downstream boundary
* Zoomen Sie in die **downstream** Region, die unter {numref}`Fig. %s <bk-bc-types>` angegeben ist.
* Suchen Sie die Hauptkanalbänke, die den in QGIS ({ref}`see above <tm-bm-breaklines>`) oder BlueKenue<sup>TM</sup> ({ref}`see above <bk-draw-ol>`) gezeichneten Trennlinien entsprechen, die durch die rot gestrichelten Linien in {numref}`Fig. %s <bk-boundary-ds>` angezeigt werden.
* **Doppelklicken Sie auf einen ** Knoten bei einer Bank** des Modells (egal welche Bank), halten Sie dann die ** Umschalttaste und **Doppelklicken Sie auf einen ** Knoten bei der anderen Bank**, um die Abflusslinie (lila) hervorzuheben (siehe {numref}`Fig. %s <bk-boundary-ds>`).
* **Klicken Sie mit der rechten Maustaste auf die lila Abflusslinie und wählen Sie ** Grenzsegment hinzufügen **.
* Führen Sie im Öffnungsfenster (**CONLIM Boundary Segment Editor**) folgende Einstellungen aus:
  * Definieren Sie **Boundary Name** als `downstream`.
  * Im Feld **Grenzcode** wählen Sie `Open boundary with prescribed H` (`5 4 4`).
  * Behalten Sie alle anderen Standardwerte und klicken Sie auf **OK**.
* ** Speichern Sie das Objekt **boundaries**, indem Sie auf das Symbol <img src="../img/telemac/bk-sym-save.png"> klicken und bestätigen Sie das Überschreiben `boundaries.bc2` (d.h. klicken Sie auf **Yes**).

```{figure} ../img/telemac/bk-bm-boundary-ds.png
:alt: bluekenue boundary conditions conlim create upstream prescribed discharge depth flow
:name: bk-boundary-ds

Definition der nachgelagerten Grenzen. Doppelklicken Sie auf einen Knoten bei einer Bank, halten Sie dann die **Shift**-Taste und Doppelklicken Sie auf einen Knoten bei der anderen Bank, um die Abflusslinie (lila) hervorzuheben. Beachten Sie, dass BOTTOM BC möglicherweise mit dem Namen *boundaries* angezeigt wird, wenn das Objekt als *boundaries.bc2* gespeichert wurde.
```
````
`````

```{admonition} Number of nodes
:class: important

Make sure that every liquid boundary has at least 5-10 nodes and that every the number of inflow nodes is approximately equal to the number of outflow nodes (in sum), also when defining multiple inflow/outflow boundaries. Read more tips on drawing boundaries in the spotlight focus on {ref}`boundary conditions <tm-foc-draw-bc>`. 
```


Letztendlich benötigt TELEMAC eine **`.cli` Datei (*Conlim Table*)**, die von
* Hervorheben des **boundaries (LIHBOR)**-Eintrags des **boundaries** (oder BOTTOM BC)-Objekts im **Data Items**-Baum und
* Drücken des Symbols <img src="../img/telemac/bk-sym-save.png"> (siehe {numref}`Fig. %s <bk-bc-fin>`).

Speichern Sie die Borders-Datei beispielsweise als **boundaries.cli**.

```{figure} ../img/telemac/bk-bc-fin.png
:alt: bluekenue liquid boundary conditions conlim upstream inflow outflow downstream cli
:name: bk-bc-fin

Die finalisierten Randbedingungen werden in einer `.cli`-Datei gespeichert, indem der **boundaries (LIHBOR)**-Eintrag des **boundaries**-Objekts (oder BOTTOM BC) im **Data Items**-Baum hervorgehoben wird.
```

```{admonition} Troubles with creating and defining the liquid boundaries?
:class: tip
Laden Sie die Objekte **boundaries** (BOTTOM BC) BlueKenue<sup>TM</sup> und TELEMAC borders (LIHBOR)-CLI aus dem Archiv für ergänzende Materialien herunter:

* [Download boundaries.bc2](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.bc2);
* [Download borders.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli)].
```

The here created Selafin/Serafin (`*.slf`) and boundary conditions (`*.cli`) files are the main products that are needed for running any other SELAFIN-based TELEMAC tutorial in this eBook. The {ref}`steady 2d <telemac2d-steady>` tutorial assigns a constant discharge at the upstream (inflow) and a constant discharge plus constant depth at the downstream (outflow) boundaries. To perform an unsteady calculation, the steady flow rates can be replaced with a `*.qsl` ASCII text file. To this end, the `.cli` file can be easily adapted any time later with a basic {ref}`text editor <npp>`.
