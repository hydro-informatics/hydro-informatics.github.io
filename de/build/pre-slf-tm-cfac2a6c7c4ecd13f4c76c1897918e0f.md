---
description: Vorverarbeitungs-Tutorial für TELEMAC mit QGIS und BlueKenue, um ein SELAFIN (SLF) Rechennetz aus einem Digital Elevation Model (Digitales Oberflächenmodell (DOM)) für hydrodynamische Simulationen zu erzeugen.
---

(slf-prepro-tm)=
# Vorverarbeitung

```{admonition} Requirements
:class: attention
Dieses Tutorial ist konzipiert für ** Fortgeschrittene Anfänger** und vor dem Tauchen in dieses Tutorial stellen Sie sicher:

* Folgen Sie den Installationsanleitungen für {ref}`qgis-install` in diesem eBook.
* Lesen Sie (oder beobachten) und verstehen Sie das eBook {ref}`qgis-tutorial`.
* Installieren Sie {ref}`BlueKenue <bluekenue>`.
```

Die ersten Schritte in der numerischen Modellierung eines Flusses mit TELEMAC bestehen in der Umwandlung eines digitalen Aufzugsmodells (**{term}`DEM`*) in ein Rechennetz. Diese Anleitung führt durch die Schaffung von:

* Ein QGIS-Projekt zur Erstellung eines Rechennetzes (ähnlich der {ref}`BASEMENT <qgis-prepro-bm>`-Vorverarbeitung).
* Optionally, the mesh generation with the BlueKenue<sup>TM</sup> software is featured.
* Ein {ref}`BlueKenue <bluekenue>`-Workspace, um Geländeerhöhungen von einem {term}`DEM` zu interpolieren, einschließlich der Export eines Netzes an das Geometrieformat SELAFIN/SERAFIN (`.slf`) für Telemac und die Definitionsgrenzkanten.

Am Ende dieses Tutorials haben {ref}`chpt-telemac`-Nutzer im Format `*.slf` ein Rechennetz generiert, das für das Simulations-Tutorial {ref}`Telemac2d steady <telemac2d-steady>` bereit ist. Zusätzliche Materialien und Zwischenprodukte werden in der Ergänzung des eBooks bereitgestellt [telemac](https://github.com/hydro-informatics/telemac)data repository.

```{admonition} Platform compatibility
:class: tip
Alle in diesem Tutorial enthaltenen Software-Anwendungen können auf *Linux*, *Windows* und auch potenziell *macOS* (nicht getestet) Plattformen ausgeführt werden.
```

(tm-qgis-prepro)=
# QGIS

## Neues Projekt erstellen und einrichten
Starten Sie QGIS und {ref}`create a new QGIS project <qgis-project>`, um mit diesem Tutorial zu beginnen. Wie in der {ref}`qgis-tutorial` angegeben, wurde für das Projekt ein Koordinatenreferenzsystem ({term}`CRS`) eingerichtet. Dieses Beispiel verwendet Daten eines Flusses in Bayern (Deutschland, UTM-Zone 33N), was folgendes erfordert {term}`CRS`:

* Im QGIS Top-Menü gehen Sie zu **Projekt*****Properties**.
* Aktivieren Sie die Registerkarte **Koordinatenreferenzsystem**.
* Geben Sie `UTM zone 33N` ein und wählen Sie das Koordinatenreferenzsystem unter {numref}`Fig. %s <qgis-crs-utm33n>`: EPSG 32633.
* Klicken Sie auf **Apply** und **OK***.

Beachten Sie, dass sich der Koordinatenreferenzsystem mit TELEMAC von der mit BASEMENT verwendeten unterscheidet, um die Kompatibilität von Geodatenprodukten von QGIS mit {ref}`BlueKenue <bluekenue>` zu ermöglichen. Auch die EPSG 32633 ist wegen ihrer geringen Präzision (maximal 2 m) keine große Wahl, aber sie wird den Job für dieses Tutorial tun.

```{figure} ../img/qgis/crs-utm-33n.png
:alt: qgis set coordinate reference system crs germany utm zone 33n Inn river
:name: qgis-crs-utm33n

Define UTM Zone 33N (WGS84) als Projekt Koordinatenreferenzsystem.
```

```{admonition} Save the project...
:class: tip
Speichern Sie das QGIS-Projekt (*Project*****Save As...**), z.B. mit dem Namen **prepro-tutorial.qgz**.
```

(tm-qgis-plugins)=
## Plugins Dritter

Die TELEMAC Tutorials verlassen sich auf das BASEmesh Plugin und das *PostTelemac* Plugin. Zu diesem Zweck **öffnen*** den **QGIS Plugin Manager** (**Plugins** Menü > **Verwalten und Installieren von Plugins*) um das **Plugins** Fenster ({numref}`Fig. %s <open-qgis-plugin-manager>`) zu öffnen.

```{figure} ../img/qgis/plugin-manager-open.png
:alt: qgis basement telemac plugins manager
:name: open-qgis-plugin-manager

Öffnen Sie QGIS Plugins Manager.
```

Im Fenster **Plugins** fügen Sie beide Plugins wie folgt hinzu:

* BASEmesh muss das Plugin-Repository des Entwicklers hinzufügen (mehr Details sind im {ref}`BASEMENT pre-processing <get-basemesh>` tutorial verfügbar):
  * Gehen Sie zur Registerkarte **Einstellungen**.
  * Scrollen Sie nach unten (**Plugin Repositories** Listbox in {numref}`Fig. %s <qgis-plugins2>`), klicken Sie auf **Add...**.
  * Geben Sie im Popup-Fenster ein:
    * einen Namen für das neue Projektarchiv, z.B. `BASEmesh Plugin Repository`;
    * the repository address: [https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml).
  * Klicken Sie auf **OK**. Das neue Repository sollte nun im Listenfeld **Plugin Repositories** sichtbar sein.
* Installieren Sie das BASEmesh Plugin:
  * Gehen Sie auf die Registerkarte **All** (immer noch im *Plugins*-Fenster) und geben Sie im Suchfeld `basemesh` ein.
  * Finden Sie das **newest BASEmesh** (d.h. ** Verfügbare Version** >= 2.0.0) Plugin und klicken Sie auf **Install Plugin**.
* Um den [***PostTelemac** Plugin](https://github.com/Artelia/PostTelemac/wiki#T45) Type `posttelemac` in der Registerkarte **All** zu installieren und auf **Install Plugin*** zu klicken.
* Nach der erfolgreichen Installation **Close** das **Plugins** Fenster.

Now, the *BASEmesh 2* plugin should be available in QGIS' *Plugins* menu and the [PostTelemac](https://github.com/Artelia/PostTelemac/wiki#T45) <img src="../img/qgis/sym-posttm.png"> symbol should be visible in QGIS' menu bar.

```{admonition} Why use BASEmesh for TELEMAC?
By using BASEmesh, this tutorial employs BASEMENT's efficient mesh generator to minimize the number of work steps to be made in BlueKenue<sup>TM</sup>. The rationale behind this approach is that QGIS is more stable and user-friendly than BlueKenue<sup>TM</sup>, for instance, to correct drawing errors of boundary lines.
```

(get-dem-xyz)=
## Digitales Oberflächenmodell (DOM)

This tutorial uses height information that is stored in a {term}`DEM`. For the QGIS section, preferably use the {term}`GeoTIFF` {term}`DEM` with UTM zone 33N as {term}`CRS` as follows:

* [** Laden Sie das GeoTIFF Digitales Oberflächenmodell (DOM)*](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem-utm33n.tif) herunter und speichern Sie es im gleichen Ordner (`/ProjectHome/` oder Unterverzeichnis) wie das oben erstellte **qgz**-Projekt.
* Fügen Sie die heruntergeladene Digitales Oberflächenmodell (DOM) als neue Rasterschicht in *QGIS* hinzu:
  * In *QGIS*' **Browser** finden Sie das **ProjectHome**-Verzeichnis, in dem Sie das Digitales Oberflächenmodell (DOM) *tif* heruntergeladen haben.
  * Ziehen Sie den Digitales Oberflächenmodell (DOM) *tif* aus dem **ProjectHome** Ordner in das QGIS' **Layer* Panel.
* Um später die Abgrenzung bestimmter Regionen des Flussökosystems zu erleichtern, fügen Sie eine {ref}`satellite imagery basemap <basemap>` (XYZ-Fliese) unter der {term}`DEM` hinzu und passen Sie die Layer-Symbologie an.

```{admonition} What are QGIS panels, what is a basemap, and how can I re-order layers?
:class: tip
Erfahren Sie mehr im *QGIS* Tutorial unter {ref}`qgis-tbx-install`.
```

Die **dem-utm33n*-Schicht sollte nun im Viewport sichtbar und im **Layers*-Panel aufgeführt sein. **Rechtsklick** auf der **dem-utm33n*-Schicht und wählen **Zoom zu Layer(s)**, um die Schicht anzuzeigen.

````{admonition} Alternatively work with a .xyz DEM pointcloud
:class: note, dropdown
This tutorial uses later in the section on BlueKenue<sup>TM</sup> a `*.xyz` file as {term}`DEM`, which was derived from the {term}`GeoTIFF` using the workflow described in the {ref}`QGIS tutorial <make-xyz>`. The `*.xyz` file can also be used with QGIS and it can be [downloaded here](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem.xyz). To **import** the **dem.xyz** file in QGIS, open the *Data Source Manager* from the **Layer** top menu, select **Add Layer** and **Add Delimited Text Layer...**. In the opening **Data Source Manager** window (see {numref}`Fig. %s <qgis-import-xyz>`) take the following actions:

* Wählen Sie die heruntergeladene `dem.xyz` Datei im Feld **Dateiname** aus.
* Im **File Format** Rahmen stellen Sie sicher, dass Sie **Custom-Abgrenzer*** auswählen und die **Space**-Abgrenzerbox überprüfen.
* Im Rahmen **Record and Fields Options** setzen Sie die **Anzahl der Header-Lines auf Disard** an `13` und überprüfen Sie die **Erste Platte hat Feldnamen** Box.
* Im Rahmen **Geometry Definition** wählen Sie `:EndHeader` als **X-Feld**, `field_2` als **Y-Feld* und `field_3` als **Z-Feld**. Wählen Sie `Project CRS: ESRI:32633 - WGS 84 / UTM zone 33N` als **Geometry Koordinatenreferenzsystem***.
* Klicken Sie auf **Add** und **Close** das Fenster *Data Source Manager*.

```{figure} ../img/qgis/import-dem-xyz.png
:alt: qgis import XYZ point cloud file dem
:name: qgis-import-xyz

Importieren Sie die `*.xyz`point Cloud als QGIS-Schicht.
```
````


## Aktivieren Sie Snapping
Es ist wichtig, dass sich die Linien nicht überschneiden, um mehrdeutige oder fehlende Definitionen von Regionen zu vermeiden und sicherzustellen, dass Grenzlinien geschlossen werden. Aktivieren Sie daher Snapping:

* Aktivieren Sie die *Snapping Toolbar*: **View****** **Toolbars*********
* **Snapping toolbar*****Enable Snapping***<img src="../img/qgis/snapping-horseshoe.png">
* Ermöglichen Sie Schnappen für
  * **Vertex**, **Segment** und **Middle of Segments**<img src="../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections*<img src="../img/qgis/snapping-intersection.png">.
  * **Self Snapping**<img src="../img/qgis/sym-self-snapping.png">.

(make-tm-shp)=
## Modellgrenzen und Bruch

This section resembles the instructions of the {ref}`BASEMENT pre-processing <make-2dm>` tutorial to generate an {term}`SMS 2dm` mesh file. The differences are that the shapefiles for the TELEMAC pre-processing use the *UTM zone 33N* {term}`CRS` and that the height (elevation) interpolation needs to be done with the BlueKenue<sup>TM</sup> software to generate liquid boundary lines and an `*.slf` geometry file for TELEMAC. The generation of the {term}`SMS 2dm` mesh relies on the {ref}`QGIS BASEmesh plugin <get-basemesh>` and requires drawing a

* {ref}`Line Shapefile <create-line-shp>`Name *breaklines.shp*, die Modellgrenzen und interne Bruchlinien zwischen Modellregionen mit unterschiedlichen Eigenschaften enthält;
* {ref}`Line Shapefile <create-line-shp>`name *liquid-boundaries.shp*, die Modellgrenzen für die Zu- und Abflussbedingungen enthält;
* {ref}`Point Shapefile <create-point-shp>`name *region-pts.shp*, die Marker für die Definition von Merkmalen der Modellregionen enthält.

{numref}`Figure %s <tm-shapefiles>` bietet einen Überblick über die zu ziehenden Shapefiles zur Erzeugung eines Qualitätsnetzes mit dem BASEmesh Plugin.

```{figure} ../img/telemac/tm-prepro-illu.png
:alt: qgis telemac basemesh point line shapefiles
:name: tm-shapefiles

Die Breaklines, Flüssigkeitsgrenzen und Region Punkte formfile für die Erstellung eines 2dm-Qualitätsnetzes mit dem BASEmesh Plugin (Hintergrundkarte: {cite:t}`googlesat`Satellitenbildarchiv).
```

(tm-bm-breaklines)=
### Breaklines und Model Outline

The model boundary defines the model extent and can be divided into regions with different characteristics (e.g., roughness values) through **breaklines**. Breaklines indicate, for instance, channel banks and the riverbed (main channel), and need to be inside the DEM extents. Boundary lines and breaklines are stored in a {ref}`Line Shapefile <create-line-shp>` that BASEmesh uses to find both model boundaries and internal breaklines between model regions. For this purpose, {ref}`create-line-shp` and call it **breaklines.shp** (**Layer** > **Create Layer** > **New Shapefile Layer**). Click on QGIS' **Layers** menu > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <tm-qgis-new-lyr>`). Make sure to select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`CRS` <img src="../img/qgis/sym-crs.png">. Do not add any field.

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: tm-qgis-new-lyr

Erstellen Sie eine neue Formdatei aus dem QGIS' Layers Menü.
```

Starten Sie die Bearbeitung **breaklines.shp**, indem Sie auf den gelben Stift<img src="../img/qgis/yellow-pen.png">klicken und die in {numref}`Fig. %s <tm-shapefiles>` angegebenen Breaklines zeichnen, indem Sie **Add Line Feature**<img src="../img/qgis/sym-add-line.png"> aktivieren, wobei:

* Die **Grenze des ** Modells links und rechts **Grenze***:
  * Delineieren Sie die äußeren Grenzen der Flutplaine.
  * Stellen Sie sicher, dass alle Punkte und Zeilen innerhalb der {ref}`DEM layer <get-dem>` sind.
  * Überqueren Sie nicht den Fluss (eingebettet durch die Satellitenbildkarte angezeigt).
  * **Finalize*** jede Zeile mit **Rechtsklick***.
* Die **Breitlinien der linken Bank (LB) und der rechten Bank (RB)*:
  * Zeichnen Sie Linien entlang des benetzten Hauptkanals in der Satelliten-Imagery (Basemap).
  * Achten Sie darauf, dass die Linie perfekt mit den vorkonstruierten Überschwemmungsgrenzlinien übereinstimmt (Snapping ist erforderlich); so müssen die Bruchlinien des Hauptkanals und die Überschwemmungsgrenzlinien die Überschwemmungen ohne Lücke zwischen den Leitungen umschließen.
* **Großbritannien**:
  * Zeichnen Sie Linien entlang der Kiesbanken, die in der Satellitenbildkarte im Hauptkanal sichtbar sind.
  * Stellen Sie sicher, dass die Linie endet perfekt zusammenfallen (verwenden Sie Schnappen) mit den vorgefertigten Hauptkanalbruchlinien; so müssen die Hauptkanal harte Bruchlinien und die Kiesbankbruchlinien die Kiesbanken ohne Lücke zwischen den Linien umschließen.
* Optional: **Breaklines of block ramps*:
  * Finden Sie die groben Blockrampen (abstoßende Gewässer) in der Satellitenbildarchiv-Basiskarte und delineieren Sie sie durch Linien über den benetzten Hauptkanal.
  * Stellen Sie sicher, dass die Linie perfekt mit den Hauptkanalbruchlinien zusammenfällt; so müssen die harten Bruchlinien des Hauptkanals und die Blockrampenbruchlinien die Blockrampen ohne Spalt zwischen den Leitungen umschließen.

Zu **richtige Zeichnungsfehler** verwenden Sie das **Vertex Tool**<img src="../img/qgis/sym-vertex-tool.png">. Schließlich speichern Sie die neuen Zeilen (Angaben von **breaklines.shp**), indem Sie auf das **Save Layer Edits**<img src="../img/qgis/sym-save-edits.png">symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.


```{admonition} Troubles with drawing boundaries and breaklines?
:class: tip
Laden Sie das in der obigen Abbildung gezeigte [zipped breaklines formfile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) herunter und entpacken Sie es in den Projektordner, zum Beispiel `/ProjectHome/shapefiles/breaklines.[SHP]`.
```

```{admonition} Draw boundaries of complex DEMs...
:class: tip
Die Zuggrenzen manuell rund um große {term}`DEM`s können sehr zeitaufwendig sein, insbesondere wenn die Rohdaten eine Punktwolke sind und noch nicht in eine {ref}`raster` umgewandelt werden.

Wenn Sie es mit einer Punktwolke zu tun haben, verwenden Sie QGIS [Convex Hull tool](https://docs.qgis.org/3.16/en/docs/training_manual/vector_analysis/spatial_statistics.html?highlight=convex%20hull#basic-fa-create-a-test-dataset), das ein eng begrenztes Polygon um Punkte zieht.

Wenn Sie sich mit einem großen {term}`GeoTIFF` beschäftigen, beachten Sie die Verwendung von QGIS' [Raster an Vector](https://docs.qgis.org/3.16/en/docs/training_manual/complete_analysis/raster_to_vector.html)tool.
```

(tm-bm-liquid-boundaries)=
### Flüssige Bounder

The **liquid boundaries** define where hydraulic conditions, such as a given discharge or stage-discharge relationship, apply at the model inflow (upstream) and outflow (downstream) limits. Thus, a functional river model requires at least one inflow boundary (line) where mass fluxes enter the model and one outflow boundary (line) where mass fluxes leave the model. For this purpose, {ref}`create-line-shp` called **liquid-boundaries.shp**, select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`CRS` <img src="../img/qgis/sym-crs.png">, and define **two text data fields** named **type** and **stringdef**. Make sure that **snapping** is still **enabled** and **Toggle (Start) Editing** <img src="../img/qgis/yellow-pen.png"> the new **liquid-boundaries.shp**. Then draw two lines:

* Aktivieren Sie **Add Line Feature**<img src="../img/qgis/sym-add-line.png">.
* Zeichnen Sie eine Zuflussgrenze (leichte blaue Linie links von {numref}`Fig. %s <tm-shapefiles>`):
  * Zoomen Sie in den Zuflussbereich der Digitales Oberflächenmodell (DOM)-Grenze, wo zwischen** die oben erstellten **-Flottplain-Grenzlinien** liegen.
  * Beginnen Sie, eine Linie auf einer Bank (oben der folgenden Figur) zu ziehen und zu der anderen Bank zu bewegen, um etwa sieben weitere Punkte über den Fluss zu machen.
  * Der **letzte Punkt** muss **Koincide*** mit dem Ende der **Floodplain Grenzlinie** der anderen Bank sein.
  * **Finalize*** die Zeile mit einem **right-click***, und geben Sie `Inflow` im **type*-Feld und `inflow` im **stringdef**-Feld ein.
* Ziehen Sie eine Abflussgrenzlinie (leichte blaue Linie rechts von {numref}`Fig. %s <tm-shapefiles>`):
  * Zoomen Sie in den Abflussbereich der Digitales Oberflächenmodell (DOM)-Grenze, wo zwischen** die oben erstellten **Flottplain-Grenzlinien** liegen.
  * Beginnen Sie, eine Linie auf einer Bank (oben der folgenden Figur) zu ziehen und zu der anderen Bank zu bewegen, um etwa sieben weitere Punkte über den Fluss zu machen.
  * Der **letzte Punkt** muss **Koincide*** mit dem Ende der **Floodplain Grenzlinie** der anderen Bank sein.
  * **Finalize*** die Zeile mit einem **right-click***, und geben Sie `Outflow` im **type*-Feld und `outflow` im **stringdef**-Feld ein.


Zu **richtige Zeichnungsfehler** verwenden Sie das **Vertex Tool**<img src="../img/qgis/sym-vertex-tool.png">.

Schließlich speichern Sie die flüssigen Grenzlinien (Angaben von **liquid-boundaries.shp**), indem Sie auf das **Save Layer Edits**<img src="../img/qgis/sym-save-edits.png">symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.

```{admonition} Troubles with drawing the liquid boundary lines?
:class: tip
Laden Sie das [zipped liquid-boundaries formfile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) herunter und entpacken Sie es in den Projektordner, zum Beispiel `/ProjectHome/shapefiles/liquid-boundaries.[SHP]`.
```

### Marken von Region Point

**Regionspunkt**-Marker werden innerhalb von durch Grenzlinien und Bruchlinien definierten Bereichen platziert. Jeder Bereichsmarker (d.h. ein Punkt irgendwo im Bereich) weist beispielsweise eine Materialkennung (MATIDs) und einen maximalen Netzzellenbereich zu. Die MATID ist (derzeit) für TELEMAC (nur BASEMENT) nicht erforderlich, aber die Einträge im Feld **max area* bestimmen die Zellgröße der Netzbereiche und haben erhebliche Auswirkungen auf die Qualität und Effizienz der TELEMAC-Simulation. Um regionale Punkte zu zeichnen, {ref}`create a new point shapefile <create-point-shp>` named **raster-points.shp** mit folgenden Definitionen (ähnlich {numref}`Fig. %s <qgis-reg-lyr>` im BASEMENT-Vorverarbeitungs-Tutorial):

* Definieren Sie den **Dateinamen* als **region-points.shp*** (oder ähnlich)
* Stellen Sie sicher, dass der **Geometrietyp** *** ist
* Select `EPSG: 32633 - WGS 84 / UTM zone 33N` as {term}`CRS` <img src="../img/qgis/sym-crs.png">
* Fügen Sie drei **Neue Felder**s hinzu (Zusätzlich zum Standard **Integer*** Typ ** Feld):
  * **max area** = **Dezimalzahl*** (**Länge** = 10, **Präzision* = 3)
  * ****** = *****************=***=*****=*************=**************=*****=******************=*************=**********************************=**********************************************************************************************************************
  * **Typ** = **Textdaten** (** Länge** = 20)
* Klicken Sie auf **OK**, um die neue Punktformdatei zu erstellen.

Betrachten Sie ** Deaktivieren Sie das Snapping** zum Zeichnen der Region Marker, weil die Punkte nicht mit einer beliebigen Linie übereinstimmen sollten. Dann **Toggle (Start) Editing**<img src="../img/qgis/yellow-pen.png"> die neue **region-points.shp**-Datei und aktivieren **Add Point Feature***<img src="../img/qgis/sym-add-point.png">. Zeichnen Sie einen Punkt in jedem Bereich, der von Bruchlinien und (flüssigen) Begrenzungslinien umschlossen wird (siehe die runden und dreieckigen Punkte in {numref}`Fig. %s <tm-shapefiles>`). Abhängig vom scheinbaren Flächentyp aus der Satellitenbildarchiv-Basiskarte, ordnen Sie eine der vier in {numref}`Tab. %s <tab-tm-region-defs>` aufgeführten Regionen an jeden Punkt zu.

```{list-table} Region names and their **max_area**, **MATID**, and **type** field values.
:header-rows: 1
:name: tab-tm-region-defs

* - Region
  - Flussbett
  - Blockrampen
  - Gravel Banken
  - Floodplas
* - **max area*
  -  25.0
  -  20.0
  -  25.0
  -  80,0
* - ** MATID**
  - 1
  - 2.
  - 3
  - ANHANG
* - ** Typ**
  - Flussbett
  - Block-Rampe
  - Kroatisch
  - Flutpla
```

Nach dem Zeichnen eines Punktes in jedem geschlossenen Bereich, speichern Sie die Region Punktmarker (Angaben von **region-points.shp**), indem Sie auf das **Save Layer Edits**<img src="../img/qgis/sym-save-edits.png">symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.

```{admonition} Troubles with drawing the region marker points?
:class: tip
Laden Sie die [zipped region-points formfile](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/region-points.zip) herunter und entpacken Sie sie in den Projektordner, z.B. `/ProjectHome/shapefiles/region-points.[SHP]`.
```

(tm-qualm)=
## Qualität Meshing (.2dm)

*BASEmesh*'s quality mesh tool creates a computationally efficient triangular mesh based on {cite:t}`shewchuk1996` and within the above-defined model boundaries. The tool associates mesh properties with the regions shapefile, but it does not include elevation data. Thus, after generating a quality mesh in {term}`SMS 2dm` format, elevation information needs to be added with the BlueKenue<sup>TM</sup> software. To generate the quality mesh, open BASEmesh's **QUALITY MESHING** tool (QGIS' **Plugins** > **BASEmesh 2** > **QUALITY MESHING**). Make the following settings in the popup window (see also {numref}`Fig. %s <fig-tm-qualm>`):

* Triangulation Zwänge Rahmen:
  * **Breaklines** = **Breaklines*** (siehe {ref}`make-tm-shp`)
  * Halten Sie alle anderen Standardeinstellungen.
* Rahmen der Regionen:
  * **Aktivieren Sie das Kontrollkästchen Regionen**.
  * **Regionsmarkerschicht** = **Regionen-Punkte** (siehe {ref}`make-tm-shp`).
  * ** Aktivieren Sie das Kontrollkästchen MATID** und wählen Sie das *regions-points* formfile's **MATID Feld** aus.
  * **Aktivieren Sie das Feld Maximale Fläche*** und wählen Sie die *regions-points* formfiles **max area Feld** aus.
* Mesh-Domainrahmen: Standardeinstellungen beibehalten.
* String Definitionsrahmen:
  * **Aktivieren Sie die String Definitionen** Checkbox.
  * **String Definitionsschicht* = **flüssige Grenzen**.
  * **String-Definitionen ID-Feld* = **stringdef**.
  * **Aktivieren Sie die Include in 2DM-Knotenstrings (BASEMENT 3)* Checkbox.
  * Ignorieren Sie alle BASEMENT 2.8 Optionen.
* Einstellungen Frame: halten Standardeinstellungen.
* Ausgangsrahmen:
  * Klicken Sie auf den **Browse...* Button und definieren Sie einen Dateinamen **2dm** im `/ProjectHome/`-Verzeichnis, wie **prepro-tutorial quality-mesh.2dm***.
* Klicken Sie auf die Schaltfläche **Run**, um das Qualitätsmaschen zu erstellen.


```{figure} ../img/qgis/bm-quality-meshing-success.png
:alt: basement qgis quality mesh tin
:name: fig-tm-qualm

Definitionen in BASEmeshs Qualitätsmaschenwerkzeug.
```

Quality meshing may take a short while. After a successful mesh generation the file **prepro-tutorial_quality-mesh-interp.2dm** will have been generated and it automatically shows up in QGIS as a single-color surface with `0-0` **Bed Elevation**. The next section shows the interpolation of elevation data with the BlueKenue<sup>TM</sup> software.

```{admonition} Troubles with running the quality mesh generator?
:class: tip
Laden Sie die [tutorial quality mesh file](https://github.com/hydro-informatics/telemac/raw/main/meshes/prepro-tutorial_quality-mesh-utm33n.2dm) herunter und speichern Sie sie im Projektordner z.B. `/ProjectHome/meshes/prepro-tutorial_quality-mesh-utm33n.2dm`.
```

(bk-tutorial)=
# Blaue Küche

(bk-intro)=
## Erste Schritte
Dieser Abschnitt enthält die {ref}`BlueKenue <bluekenue>`-Software, um Geländeerhöhungen von einer {term}`DEM`.xyz-Datei auf einem {term}`SMS 2dm`Netz zu interpolieren, das Netz in das Geometrieformat SELAFIN/SERAFIN (`*.slf`) für TELEMAC zu exportieren und Grenzlinien zu definieren.

In addition, the {ref}`Meshing with BlueKenue <bk-meshing>` section explains the mesh generation with BlueKenue<sup>TM</sup>, which might be unstable because of program crashes and inflexible for correcting line drawing errors. Still, meshing with BlueKenue<sup>TM</sup> might be desirable to create a computational mesh with long triangular cells that approximately follow the river streamlines (i.e., using a channel sub-mesh).

To familiarize with BlueKenue<sup>TM</sup>, launch the software (more details in the {ref}`installation chapter <bluekenue>`) and locate

* der **WorkSpace** Browser (links im Fenster),
* den Eintrag **Datenelemente** im **WorkSpace***, in dem Dateiobjekte aufgeführt werden,
* Der **Views**-Eintrag im **WorkSpace***, bei dem ein **2D View (1)**-Eintrag standardmäßig erscheint und ein *3D View* aus dem **Window**-Top-Menü > **Neue 3D-Ansicht** hinzugefügt werden kann.

Sehen Sie sich das **File*-Menü an, das Folgendes ermöglicht:

* Create **New** BlueKenue<sup>TM</sup> objects, such as SELAFIN, Conlim Boundary Condition, T3 Mesh Generator, or 2D Interpolator objects.
* **Open** Dateitypen wie `*.slf` Geometriedateien oder `*.xyz`Point Clouds.
* **Import*** Dateien wie:
  * **ArcView Shapefile** (mehr zu {ref}`shapefiles <shp>`)
  * {term}`SMS 2dm` Mesh wie der in der obigen {ref}`pre-processing with QGIS <tm-qualm>`section erstellte oder
  * a {term}`GeoTIFF` raster, which will not work with many GeoTIFF rasters in practice because BlueKenue<sup>TM</sup> cannot handle Float32 or Float64 data in a GeoTIFF.

The **Edit** menu enables editing BlueKenue<sup>TM</sup> objects, such as lines, point sets, or meshes.

The **Tools** menu provides routines that can be applied to particular BlueKenue<sup>TM</sup> objects or for combining objects. In particular, this tutorial will make use of the **Map Objects...** tool.

(bk-files)=
## Dateien und Objekte

BlueKenue<sup>TM</sup> saves every object in software specific file formats and this eBook refers to the following BlueKenue<sup>TM</sup> file objects (alphabetic order of file endings):

* `*.bc2` Dateien enthalten Conlim Boundary Bedingungen.
* `*.cli`-Dateien enthalten TELEMAC gebrauchsfertige Randbedingungen und können mit einem `*.bc2`-Objekt hergestellt werden.
* `*.i2s` Dateien enthalten geschlossene oder offene Zeilen.
* `*.in2`-Dateien enthalten 2D-Interpolatoren zur Abbildung von Höhendaten auf einem Mesh.
* `*.slf` files contain ready-to-use TELEMAC meshes that stem from a BlueKenue<sup>TM</sup> SELAFIN object and a `*.t3s` mesh file.
* `*.t3c` files contain BlueKenue<sup>TM</sup> channel mesh generator objects.
* `*.t3m` files contain BlueKenue<sup>TM</sup> mesh generator objects to create a `*.t3s` mesh object.
* `*.t3s` files contain BlueKenue<sup>TM</sup> mesh objects that can either be imported (e.g., from an {term}`SMS 2dm` file) or created with a `*.t3m` mesh generator.

All files that are created with BlueKenue<sup>TM</sup> are based on the ASCII EnSim 1.0 file type standard. The EnSim Core builds on {term}`HDF` and it is documented in BlueKenue<sup>TM</sup>'s [user manual PDF](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/2011_UserManual.pdf) that comes along with the [BlueKenue installer](https://chyms.nrc.gc.ca/download_public/KenueClub/BlueKenue/Installer/BlueKenue_3.12.0-alpha+20201006_64bit.msi) (in BlueKenue<sup>TM</sup> press the `F1` key to open the manual). Note that understanding the EnSim Core can significantly facilitate troubleshooting structural errors of BlueKenue<sup>TM</sup> files.

(bk-xyz)=
## XYZ Punkte laden

Download the provided [dem.xyz](https://github.com/hydro-informatics/telemac/raw/main/rasters/dem.xyz) point cloud that contains EnSim-formatted 3d coordinates of the river ecosystem {term}`DEM` that will be modelled in this tutorial. The `*.xyz` file was derived from the {term}`GeoTIFF` {term}`DEM` used in the {ref}`QGIS pre-processing <get-dem-xyz>`.

 ```{aside} The .xyz file is not an XYZ tile
Die Punktwolke in der `*.xyz`-Datei unterscheidet sich von dem regulären XYZ-Fliesenraster, der die {ref}`satellite imagery basemap <basemap>` bildet.
 ```

To load the **dem.xyz** file in BlueKenue<sup>TM</sup>, open it from the **File** menu (**File** > **Open...**) and take the following actions in the popup window:

* Navigieren Sie in den Download-Ordner.
* Neben dem **Dateinamen:**-Feld finden Sie das Dateityp-Drop-down-Menü und ** ändern Sie den Standard von Telemac Selafin File (`*.slf`) an Point Sets (`*.pt2`, `*.xyz`, `*.pcl`)**.
* Klicken Sie auf **Öffnen**, um den Import abzuschließen.

To verify if the point cloud was correctly imported, **drag** the new **dem (Z)** data items to the **2D View (1)** entry. {numref}`Figure %s <bk-import-xyz>` shows the imported XYZ point cloud in BlueKenue<sup>TM</sup>.

```{figure} ../img/telemac/bk-imported-pts.png
:alt: bluekenue import xyz point cloud DEM
:name: bk-import-xyz

The provided dem.xyz imported in BlueKenue<sup>TM</sup>.
```

To verify the {term}`CRS` of the point dataset, right-click on **dem (Z)**, select properties, go to the **Spatial** tab, and make sure that BlueKenue<sup>TM</sup> correctly identified **UTM Zone 33** in the **Coordinate System** frame and **WGS 84** as **Ellipsoid**.


(bk-meshing)=
## BlueKenue Meshing (Optional)

```{admonition} Skip this section if you created a *.2dm* quality mesh with BASEMESH
This is an optional section for users who do not want to use QGIS and the BASEmesh plugin for meshing. Generating a mesh with BlueKenue<sup>TM</sup> can be useful, for instance, to produce a computational grid that has triangular cells oriented parallel to the riverbanks (i.e., a channel sub-mesh). Otherwise, **if the `*.2dm` mesh file was created** with QGIS, **jump to the section on creating a {ref}`Selafin Object <bk-create-slf>`**.
```

This section features the basic mesh generation with BlueKenue<sup>TM</sup>, which also runs smoothly on Linux through the {ref}`PlayOnLinux <play-on-linux>` app. Additionall, the Baxter tutorial {cite:p}`baxter2013` provides more details for getting started with BlueKenue along with detailed screenshots.

### Zeichnung Modell Boundary (Closed Line)

Entscheiden Sie die Modellgrenze (outline) mit einem geschlossenen Zeilenobjekt (siehe auch {numref}`Fig. %s <bk-model-outline>`):

* Create a new **Closed Line** by clicking on the <img src="../img/telemac/bk-sym-cl.png"> symbol in the BlueKenue<sup>TM</sup> menu.
* **Draw** die neue geschlossene Linie:
  * Stellen Sie Punkte, indem Sie auf die äußere Ausdehnung der **dem (Z)* Schicht im **2D Views (1)* Fenster schließen. Stellen Sie sicher, dass kein Punkt außerhalb der Region liegt, in der Erhebungsdaten zur Verfügung stehen (d.h. fest abgrenzen **dem (Z)**).
* Vervollständigen Sie die geschlossene Linie durch Pressen **Esc**.
* Nennen Sie beispielsweise die geschlossene Zeile `model-outline`.
* **Skip*** **Ein neues Attribut** eingeben, indem Sie einfach auf **OK** klicken.

```{figure} ../img/telemac/bk-model-outline.png
:alt: bluekenue draw closed line model boundary outline
:name: bk-model-outline

The Closed Line of the model boundaries in BlueKenue<sup>TM</sup>'s 2D View window.
```

To **save the model outline**, highlight the new Closed Line object in the **WorkSpace** browser and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Consider creating a new folder called `bk-mesh` that will contain all BlueKenue<sup>TM</sup> objects required for meshing. Thus, save the model outline (Closed Line), for example, as **/bk-mesh/model-outline.i2s**.

```{admonition} Troubles with drawing the model outline?
:class: tip
The outline can also be downloaded from the supplemental materials repository ([download model-outline.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/model-outline.i2s)). To open the Closed Line from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **Line Sets (`*.i2s`, `*.i3s`)** as file type and navigate to the download directory.
```

The current state of BlueKenue<sup>TM</sup> can be saved in the form of a **workspace.ews** file (**File** > **Save WorkSpace...** > define a name). Saving the workspace requires that all BlueKenue<sup>TM</sup> objects are saved on the disk. Optionally, download the [meshing-workspace.ews](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/meshing-workspace.ews) from the supplemental materials repository.

```{admonition} Loading a WorkSpace
:class: attention
In theory, the saved workspace can be loaded after closing BlueKenue<sup>TM</sup>, but the **Load WorkSpace...** operation often **fails** for apparently arbitrary reasons. This issue is one of the reasons that make QGIS a better option for meshing.
```

(bk-draw-ol)=
### Offene Linien der Kanalbanken zeichnen

Ähnlich wie die {ref}`above-created breaklines in QGIS <make-tm-shp>` können die Channel-Banken mit Open Line-Objekten delineiert werden. Dazu erstellen Sie zwei Open Line-Objekte wie folgt:

* Create a new **Open Line** by clicking on the <img src="../img/telemac/bk-sym-ol.png"> symbol in the BlueKenue<sup>TM</sup> menu.
* **Draw** die neue offene Linie:
  * Stellen Sie Punkte, indem Sie den blau-grünen Bereichen folgen, wie in {numref}`Fig. %s <bk-lines-all>` **2D Views (1)* Fenster (Flussrichtung von links nach rechts) angegeben.
* Die offene Linie durch Drücken **Esc** beenden.
* Nennen Sie eine offene Zeile `LeftBank` und die andere `RightBank`.
* **Skip*** **Ein neues Attribut angeben:**, indem Sie einfach auf **OK** klicken.

```{figure} ../img/telemac/bk-lines-all.png
:alt: bluekenue draw open line channel river banks
:name: bk-lines-all

Die fertiggestellten Open und Closed Line-Objekte zeichnen die Modellgrenzen und die Kanalbanken ab. Die RightBank Open Line ist durch die gestrichelte schwarze Linie dargestellt und die LeftBank Open Line ist rot dargestellt.
```

```{admonition} Troubles with drawing the open lines of the channel banks?
:class: tip
Download the lines from the supplemental materials repository. Notably download [LeftBank.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/LeftBank.i2s) and [RightBank.i2s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/RightBank.i2s). To open the Open Line objects from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **Line Sets (`*.i2s`, `*.i3s`)** as file type and navigate to the download directory.
```

### Mesh(es) generieren

BlueKenue<sup>TM</sup> provides mesh generators for creating regular or unstructured computational grids (meshes). This example features the **T3 Channel Mesher** to generate a triangular mesh, which involves first creating a channel mesh (sub-mesh) and second generating a compound mesh that embeds the channel sub-mesh in a coarser mesh of the floodplains. To this end, start with creating a new **T3 Channel Mesher** object (**File** > **New** > **T3 Channel Mesher**). In the popup window set:

* **CrossChannelNodeCount** an `20` und
* **AlongChannelInterval** an`15`.

Klicken Sie auf **OK** (**not Run**) um das neue T3 Channel Mesh-Fenster zu schließen. Weiter ziehen und fallen Sie die oben erstellte **LeftBank* und **RightBank*** Open Line Objekte auf ihren entsprechenden Attributen des **new T3 Channel Mesh** Objekts im WorkSpace-Browser, wie unter {numref}`Fig. %s <bk-channel-mesh>` angegeben. Als nächstes erzeugen Sie das Kanalnetz durch Doppelklick auf das **new T3 Channel Mesh* Objekt und klicken Sie auf **Run**. Um das resultierende **Mesh** zu visualisieren, ziehen Sie es auf das **2D View (1)* Objekt.

```{figure} ../img/telemac/bk-channel-mesh.png
:alt: bluekenue create channel mesh
:name: bk-channel-mesh

Erstellen und visualisieren Sie das Kanalnetz nach dem Ziehen der LeftBank und RightBank Open Line Objekte auf ihren Namen Äquivalente des T3 Channel Mesh Objekts.
```

```{admonition} Troubles with creating the channel mesh?
:class: tip
Download the [channel-mesh.t3c](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/channel-mesh.t3c) mesh generator and the [channel-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/channel-mesh.t3) mesh objects from the supplemental materials repository. To open the T3 Mesh object from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **2D T3 Mesh (`*.t...`)** as file type and navigate to the download directory.
```

Als nächstes wird das Kanalnetz in ein gröberes Hochwassernetz eingebettet, indem ein **neues T3 Mesh Generator* Objekt (**File*****************T3 Mesh Generator*** erstellt wird. Im Popup-Fenster **T3 Mesh** machen Sie folgende Einstellungen (siehe auch {numref}`Fig. %s <bk-t3-mesher>`):

* *************** Checkbox.
* Setzen Sie die **Default Edge Länge* an `20`.
* Halten Sie alle anderen Standardeinstellungen.
* Drücken Sie **OK** (**nicht Run***).

```{figure} ../img/telemac/bk-t3-mesher.png
:alt: bluekenue create combined mesh generator
:name: bk-t3-mesher

Richten Sie die Eigenschaften des neuen T3 Mesh Generator-Objekts ein.
```

Definieren Sie die **Outline (Value)** durch Ziehen (siehe auch {numref}`Fig. %s <bk-mesh-compound>`):

* Das oben erstellte **model-outline** Objekt auf dem **Outline (Value)** des **new T3 Mesh* und
* Der Kanal **Mesh*** auf dem **SubMeshes** Attribut des **new T3 Mesh**.

Generieren Sie das Compound-Netz durch Doppelklick auf das **new T3 Mesh*-Objekt und ein einziges Klick auf **Run**. Bestätigen Sie das Fragefeld (*Weiter?******) und drücken Sie **OK*** nach Fertigstellung des Netzgenerators (*Done...*). Um das resultierende **Mesh** zu visualisieren, ziehen Sie es auf die **2D View (1)*.

```{figure} ../img/telemac/bk-mesh-compound.png
:alt: bluekenue generate combined mesh drag and drop
:name: bk-mesh-compound

Das Verbindungsnetz nach dem Ziehen des Modells Umriss auf der Outline (Value) und der Kanal Mesh auf dem SubMeshes Attribut des neuen T3 Mesh Generatorobjekts.
```

```{admonition} What is the difference between the channel mesher and the mesh generator?
:class: note
{numref}`Figure %s <bk-mesh-compound>` shows that the channel mesh is streamline-adjusted following the channel banks. This kind of mesh is known to be advantageous for computation speed and model stability. Thus, the availability of the channel mesher in BlueKenue<sup>TM</sup> is a strength and the **best argument for not using BASEmesh** in QGIS for the mesh generation.
```

```{admonition} Troubles with creating the compound mesh?
:class: tip
Download the [compound-mesher.t3m](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesher.t3m) and the [compound-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesh.t3s) objects from the supplemental materials repository. To open the T3 Mesh object from the repository in BlueKenue<sup>TM</sup>, go to **File** > **Open...** > select **2D T3 Mesh (`*.t...`)** as file type and navigate to the download directory.
```

(bk-slf)=
## SELAFIN

### Open and Import Zutaten
Whether the mesh was created with BlueKenue<sup>TM</sup> or QGIS (and the BASEmesh plugin), make sure to have now a BlueKenue<sup>TM</sup> workspace with only the XYZ point cloud loaded (see the {ref}`bk-xyz` section). Before a SELAFIN object can be created, the previously created mesh (i.e., either the [quality-mesh.2dm](https://github.com/hydro-informatics/telemac/raw/main/meshes/prepro-tutorial_quality-mesh-utm33n.2dm) or the [compound-mesh.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-mesh/compound-mesh.t3s)) needs to be imported into the WorkSpace in addition to the point cloud. The following instructions show the import and use of the `*.2dm` file:

* In BlueKenue<sup>TM</sup> go to **File** > **Import** > **SMS 2DM Mesh**.
* Im Importfenster navigieren Sie in den Ordner, in dem die `*.2dm`-Datei lebt, wählen Sie die `*.2dm`-Datei aus und klicken Sie auf **Öffnen**.
* Wenn der *Reading SMS 2d Mesh File* Prozess ist *Done...*, klicken Sie auf **OK**.

```{admonition} How to load a BlueKenue .T3S mesh file?
:class: note, dropdown
In contrast to an {term}`SMS 2dm` (`*.2dm`) file that has to be *imported*, a `*.t3s` file has to be **opened** in BlueKenue<sup>TM</sup>. To this end, **open** the T3 Mesh (`*.t3s`) from **File** > **Open...** > select **2D T3 Mesh (`*.t...`)** as file type and navigate to the download directory. Select the `*.t3s` mesh file and click **Open**.
```

Ignore warning messages regarding the projection, but make sure that BlueKenue<sup>TM</sup> correctly read the mesh coordinates by **dragging** the imported (or opened) mesh onto the **2D View (1)**. The BlueKenue<sup>TM</sup> window should now look similar to {numref}`Fig. %s <bk-imported-mesh>`.

```{figure} ../img/telemac/bk-imported-mesh.png
:alt: bluekenue import open 2dm t3s mesh drag
:name: bk-imported-mesh

Das importierte Netz in der 2D View (1).
```

(bk-create-slf)=
### SELAFIN Object erstellen

With the open *dem.xyz* and the imported (or opened) mesh, all ingredients required by a BlueKenue<sup>TM</sup> SELAFIN object are available. Now, create a new SELAFIN object:

* *********** **SLAFIN Objekt...**

```{image} ../img/telemac/bk-create-selafin-object.png
```

* Im Popup-Fenster (*Properties of:new Selafin*) klicken Sie auf **** und ein **new Selafin** Objekt wird im WorkSpace's **Data Items** angezeigt.
* **Rechtsklick*** auf das **neue Selafin** Objekt und wählen Sie ** Variable hinzufügen...**
* Nehmen Sie folgende Aktion im **Add New SELAFIN Variable** Fenster:
  * Wählen Sie im Feld **Mesh** das oben importierte (oder geöffnete) Netz (z.B. `prepro-tutorial_quality-mesh-utm33n.2dm`).
  * Im Feld **Name*** wählen Sie **BOTTOM***.
  * Im Feld **Units* wählen Sie **M** (d.h. Meter).
  * Halten Sie alle anderen Standardeinstellungen und klicken Sie auf **OK**.
* Speichern Sie das neue Selafin-Objekt, indem Sie es im **Data Item* Baum des WorkSpace hervorheben und auf die Festplatte <img src="../img/telemac/bk-sym-save.png">symbol klicken. Geben Sie dem Netz einen aussagekräftigen und kurzen Namen wie `qgismesh.slf`.

(bk-2dinterp)=
### 2D Interpolator erstellen

Ein 2D Interpolator-Objekt ist erforderlich, um Höheninformationen auf das Selafin-Netz abzubilden. Zu diesem Zweck erstellen Sie ein neues 2D Interpolator-Objekt und Kartenansichten auf das BOTTOM-Netz:

* Gehen Sie zu **Datei***********2D Interpolator...* und ein **neues 2D Interpolator** Objekt erscheint im **Data Items** des WorkSpace.

```{image} ../img/telemac/bk-create-2Dinterpolator.png
```

* **Drag dem (Z)** (d.h. das oben eröffnete *dem.xyz* pointcloud) auf das **new 2D Interpolator** Objekt (roter Pfeil in {numref}`Fig. %s <bk-mesh-interpolated>`).
* **Highlight** (klicken Sie auf) das **BOTTOM (Anonymes Attribut)** mesh Attribut des oben erstellten SELAFIN-Objekts (z.B. `qgismesh`)
* Mit dem hervorgehobenen Mesh gehen Sie zum **Tools* Top-Menü > **Map-Objekt...**.
* Wählen Sie im Fenster **Available Objects** den **neuen 2D Interpolator*** und klicken Sie auf **OK**.
* Sobald das *Processing...* fertig ist, klicken Sie auf **OK**.
* Speichern Sie die letzten Maschen:
  * The BOTTOM mesh is a BlueKenue<sup>TM</sup> `*.t3s` mesh object; to save it, highlight it in the **Data Items** tree and click on the disk <img src="../img/telemac/bk-sym-save.png"> symbol. Then, save the mesh, for instance, as `BOTTOM.t3s` file.
  * Um das Selafin-Netz in seinem aktuellen Zustand (mit interpolierten Erhebungen) zu speichern, markieren Sie das Selafin-Objekt (z.B. `qgismesh`) und klicken Sie auf das Disk <img src="../img/telemac/bk-sym-save.png">symbol. Diese Aktion überschreibt die oben genannte `*.slf`-Datei (klicken Sie **Ja*, um es zu bestätigen).

Um zu überprüfen, ob der 2D-Interpolator die Erhebungen auf dem BOTTOM-Netz korrekt interpolierte, ziehen Sie das BOTTOM-Netz auf die **2D-Ansicht (1)**. Prüfen Sie die Sichtbarkeit von dem (Z) und das importierte (oder geöffnete) Mesh mit einem Rechtsklick auf diese Elemente im 2D View (1) Baum und **deselect** den **Visible**-Eintrag. So sollte jetzt nur das höheninterpolierte Netz sichtbar sein, wie unter {numref}`Fig. %s <bk-mesh-interpolated>` angegeben. Wenn die **-Interpolation erfolgreich war, wird das Netz in einer Vielzahl von (Regenbogen) Farben* angezeigt. Ansonsten *** wenn das Netz* vollständig, monoton **monochrom (rot)** ist, hat die Erhebung **interpolation***************** und muss wiederholt werden (das numerische Modell kann ohne Höheninformationen nicht richtig funktionieren).

```{figure} ../img/telemac/bk-mesh-interpolated.png
:alt: bluekenue 2dm t3s mesh interpolate height elevation 2D interpolator map object
:name: bk-mesh-interpolated

Das höheninterpolierte Mesh in der 2D-Ansicht (1) mit Anzeige von Drag &amp; Drop-Actions zum Ausführen des Objekt-Mappings mit einem neuen 2D Interpolator-Objekt.
```

```{admonition} Troubles with creating the Selafin mesh and or the height interpolation?
:class: tip
Laden Sie das BOTTOM-Netz und das SELAFIN-Objekt aus dem Zusatzmaterial-Repository herunter:

* [Download BOTTOM.t3s](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/BOTTOM.t3s);
* [Download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf)(*EPSG:6173** - ETRS 89 / UTM-Zone 33N).
```

```{admonition} Roughness zone interpolation.
:class: tip

Ähnlich wie bei der Erhebung können im Studienbereich Reibwerte erstellten Zonen mit unterschiedlicher Rauhigkeit zugeordnet werden. Lesen Sie mehr im Rampenlicht auf {ref}`roughness (friction) zones <tm-friction-zones>`.
```

(bk-bc)=
## Allgemeine Geschäftsbedingungen (Conlim - CLI)

### Conlim Object erstellen
TELEMAC muss wissen, wie man die Außenkanten des Modells (mesh) behandelt. Zu diesem Zweck müssen allen Knoten, die den `*.slf`mesh Umriss darstellen, Randbedingungen zugeordnet werden:

* *********** **Boundary Conditions (Conlim )...** und ein **new 2D Interpolator** Objekt erscheint im **Data Items** des WorkSpace.

```{image} ../img/telemac/bk-create-bc.png
```

* Im geöffneten Popup-Fenster (**Available t3s Objects**) wählen Sie das oben erstellte **BOTTOM* Netz (d.h. das Netz mit Höheninformationen) und klicken Sie auf **OK***. Ein neues **BOTTOM BC* Objekt wird im **Data Items** Baum des WorkSpace auftreten.
* Ziehen Sie das neue **BOTTOM BC** Objekt auf das **2D View (1)**, das ** die *Beschreibung* von Randbedingungstypen* (Details im nächsten Abschnitt) aktivieren wird.

{numref}`Figure %s <bk-bc-types>` illustriert das neue BOTTOM BC-Objekt in der 2D-Ansicht (1) und gibt an, wo im nächsten Abschnitt vor- und nachgeschaltete Flüssigkeitsgrenzen angewendet werden.

```{figure} ../img/telemac/bk-bc-types.png
:alt: bluekenue boundary conditions conlim create upstream downstream
:name: bk-bc-types

Das neue Objekt Boundary Conditions (Conlim) (BOTTOM BC) in der 2D View (1) mit einem qualitativen Überblick über die Position der vor- und nachgeschalteten Grenzen, in denen vorgeschriebener Fluss (Q) und vorgegebener Fluss (Q) und Depth (H) später im TELEMAC-Setup angewendet werden.
```

Um ** das neue BOTTOM BC-Objekt** zu speichern, markieren Sie es im **Data Items**-Baum und klicken Sie auf die Festplatte <img src="../img/telemac/bk-sym-save.png">symbol. Definieren Sie einen Dateinamen wie **`boundaries.bc2`**. Durch das Speichern des Objekts übernimmt das BOTTOM BC-Objekt den neuen Dateinamen (z.B. **boundaries*).

(bk-liquid-bc)=
### Definieren von flüssigen Grenzen

Der Standardgrenztyp des **boundaries* Objekts ist **Closed border (wall)**. Um Massen (d.h. Wasser, Sediment und/oder Tracer) durch das Modell zu ermöglichen, müssen mindestens zwei Öffnungen in die geschlossene Grenze gezogen werden. Dazu müssen mindestens ein Zulauf und eine abfließende offene Grenze für Flüssigkeiten definiert werden. Dieses Tutorial verwendet diese minimale Anzahl an erforderlichen offenen Grenzen (d.h. ein vorgeschalteter Zulauf und eine nachgeschaltete Abflussgrenze), die in {numref}`Fig. %s <bk-bc-types>` angegeben sind.

```{admonition} Liquid boundaries must be defined in BlueKenue
Even though the liquid boundaries are already defined in QGIS (see the {ref}`QGIS section on Liquid Boundaries <tm-bm-liquid-boundaries>`), it is always necessary to define the liquid boundaries in BlueKenue<sup>TM</sup> to fit the node numbers (IDs) of the Selafin mesh.
```

Die stromaufwärts liegende (inflow) Flüssigkeitsgrenze stellt eine **Open-Grenze mit verschriebenem Q und H* (Entladung und Wassertiefe entsprechend einer {term}`stage-discharge relation <Stage-discharge relation>`) mit dem Code `5 5 5` und die nachgeschaltete Abfluss (liquid)-Grenze eine **Open-Grenze mit verschriebenem H* mit dem Code `5 4 4` (d.h. verschriebene Wassertiefe) dar. Für eine trockene Initialisierung des Modells sind solche Randbedingungen erforderlich. In der Praxis sollte die stromabwärtige Grenze an einer Messstation liegen, an der eine {term}`stage-discharge relation <Stage-discharge relation>` mit historischen Daten kalibriert wurde. Um die durchschnittliche Rauhigkeit von {term}`stage-discharge relation <Stage-discharge relation>` zu hinterkalkulieren, werfen Sie einen Blick auf die {ref}`Python exercise on 1-d hydraulics for solving the Manning-Strickler <ex-1d-hydraulics>` Formel.

````{admonition} Drawing boundary conditions for mass balance

Die Randbedingungseinstellungen beeinflussen die Massenbilanz, was ein entscheidendes Kriterium für ein klingendes numerisches Modell ist. Lesen Sie mehr im Rampenlicht auf die Einrichtung {ref}`boundary conditions for mass balance<foc-mass-bc>`. Um rechnerische Probleme zu vermeiden, definieren Sie Flüssigkeitsgrenzlinien nur entlang des Kanalbodens, wie in der folgenden {numref}`Fig. %s <draw-inflow-pre-slf>` dargestellt.

```{figure} ../img/telemac/cross-section-sx.png
:alt: draw bluekenue liquid boundary conditions conlim upstream inflow
:name: draw-inflow-pre-slf
:width: 75%

Der rote hervorgehobene Teil dieses qualitativen Querschnitts sollte als Zufluss (nach oben) Randbedingung definiert werden. Mesh-Knoten an den Flussufern und an den Flutplainen sollten nicht enthalten sein.
```
````


Um die beiden flüssigen Begrenzungslinien zuzuordnen, zoomen Sie in die stromabwärtigen und stromaufwärts gelegenen Regionen unter {numref}`Fig. %s <bk-bc-types>` und erstellen Sie beide Grenzen wie folgt (Tabzeichen):

`````{tab-set}
````{tab-item} Upstream boundary
* Zoom in die **upstream*-Region, die in {numref}`Fig. %s <bk-bc-types>` angegeben ist.
* Locate the main channel banks corresponding to the breaklines drawn in QGIS ({ref}`see above <tm-bm-breaklines>`) or BlueKenue<sup>TM</sup> ({ref}`see above <bk-draw-ol>`).
* **Double-click** auf einer **-Node an einer Bank*** des Modellumrisses (unabhängig von welcher Bank), dann **hold** den **Shift**-Schlüssel und **double-click*** auf einer **-Node an der anderen Bank**, um die Zufluss- (purple)-Linie (siehe {numref}`Fig. %s <bk-boundary-us>`) hervorzuheben.
* **Rechtsklick*** auf der lila Zuflusslinie und wählen Sie **Boundary Segment**.
* Im Öffnungsfenster (***CONLIM Boundary Segment Editor**) ergeben sich folgende Einstellungen:
  * **Boundary Name** als `upstream`.
  * Im Feld **Boundary Code** wählen Sie `Open boundary with prescribed Q and H` (`5 5 5`).
  * Halten Sie alle anderen Standardeinstellungen und klicken Sie auf **OK**.
* **Save*** das **boundaries**-Objekt, indem Sie auf die Festplatte <img src="../img/telemac/bk-sym-save.png">symbol klicken und das Überschreiben `boundaries.bc2` (d.h. klicken Sie auf **Ja**) bestätigen.

**Schalten Sie die **Downstream-Begrenzungstabelle** an, um die Ablaufbedingungen nach {numref}`Fig. %s <bk-boundary-ds>` zu definieren.

```{figure} ../img/telemac/bk-bm-boundary-us.png
:alt: bluekenue boundary conditions conlim create upstream prescribed discharge flow
:name: bk-boundary-us

Die vorgeschaltete Grenzdefinition. Doppelklicken Sie auf einen Knoten an einer Bank, dann halten Sie den **Shift** Schlüssel und doppelklicken Sie auf einen Knoten an der anderen Bank, um die Zufluss (purple) Zeile zu markieren. Beachten Sie, dass BOTTOM BC mit dem Namen *boundaries* erscheinen könnte, wenn das Objekt als *boundaries.bc2* gespeichert wurde.
```
````

````{tab-item} Downstream boundary
* Zoomen Sie in die **downstream*-Region, die in {numref}`Fig. %s <bk-bc-types>` angegeben ist.
* Locate the main channel banks corresponding to the breaklines drawn in QGIS ({ref}`see above <tm-bm-breaklines>`) or BlueKenue<sup>TM</sup> ({ref}`see above <bk-draw-ol>`), which are indicated by the red-dotted lines in {numref}`Fig. %s <bk-boundary-ds>`.
* **Double-click** auf einer **-Node an einer Bank*** des Modellumrisses (unabhängig von welcher Bank), dann **hold** die **Shift**-Taste und **double-click*** auf einer **-Node an der anderen Bank**, um die Ausflusslinie (purple) hervorzuheben (siehe {numref}`Fig. %s <bk-boundary-ds>`).
* **Rechtsklick** auf der lila Abflusslinie und wählen **Boundary Segment hinzufügen**.
* Im Öffnungsfenster (***CONLIM Boundary Segment Editor**) ergeben sich folgende Einstellungen:
  * **Boundary Name** als `downstream`.
  * Im Feld **Boundary Code** wählen Sie `Open boundary with prescribed H` (`5 4 4`).
  * Halten Sie alle anderen Standardeinstellungen und klicken Sie auf **OK**.
* **Save*** das **boundaries**-Objekt, indem Sie auf die Festplatte <img src="../img/telemac/bk-sym-save.png">symbol klicken und das Überschreiben `boundaries.bc2` (d.h. klicken Sie auf **Ja**) bestätigen.

```{figure} ../img/telemac/bk-bm-boundary-ds.png
:alt: bluekenue boundary conditions conlim create upstream prescribed discharge depth flow
:name: bk-boundary-ds

Die nachgeschaltete Grenzdefinition. Doppelklicken Sie auf einen Knoten an einer Bank, dann halten Sie den **Shift** Schlüssel und doppelklicken Sie auf einen Knoten an der anderen Bank, um die Ausfluss (purple) Linie hervorzuheben. Beachten Sie, dass BOTTOM BC mit dem Namen *boundaries* erscheinen könnte, wenn das Objekt als *boundaries.bc2* gespeichert wurde.
```
````
`````

```{admonition} Number of nodes
:class: important

Stellen Sie sicher, dass jede Flüssigkeitsgrenze mindestens 5-10 Knoten aufweist und dass jede Anzahl von Zuflussknoten etwa gleich der Anzahl von Abflussknoten (in Summe) ist, auch bei der Definition mehrerer Zufluss-/Ausflussgrenzen. Lesen Sie mehr Tipps zum Ziehen von Grenzen im Fokus auf {ref}`boundary conditions <tm-foc-draw-bc>`.
```


Letztlich benötigt TELEMAC eine **`.cli`(*Conlim Table*)**, die von
* das **-Freunde (LIHBOR)**-Eintrag des **-Freunde** (oder BOTTOM BC)-Objekts im **Data Items**-Baum und
* Drücken der Festplatte <img src="../img/telemac/bk-sym-save.png">symbol (siehe {numref}`Fig. %s <bk-bc-fin>`).

Speichern Sie die Datei Grenzen, zum Beispiel als **boundaries.cli**.

```{figure} ../img/telemac/bk-bc-fin.png
:alt: bluekenue liquid boundary conditions conlim upstream inflow outflow downstream cli
:name: bk-bc-fin

Die abschließenden Randbedingungen werden in einer `.cli`-Datei gespeichert, indem das **boundaries (LIHBOR)** Eintrag des **boundaries* (oder BOTTOM BC)-Objekts im **Data Items**-Baum hervorgehoben wird.
```

```{admonition} Troubles with creating and defining the liquid boundaries?
:class: tip
Download the **boundaries** (BOTTOM_BC) BlueKenue<sup>TM</sup> and TELEMAC boundaries (LIHBOR)-CLI objects from the supplemental materials repository:

* [Download boundaries.bc2](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.bc2);
* [Abrufgrenzen.cli](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/boundaries.cli).
```

Die hier erstellten Selafin/Serafin (`*.slf`) und Randbedingungen (`*.cli`) Dateien sind die wichtigsten Produkte, die für die Durchführung jeder anderen SELAFIN-basierten TELEMAC Tutorial in diesem eBook benötigt werden. Das {ref}`steady 2d <telemac2d-steady>` tutorial ordnet eine konstante Entladung an der vorgeschalteten (Einfluss) und eine konstante Entladung plus konstante Tiefe an den nachgeschalteten (Ausfluss) Grenzen zu. Um eine unruhige Berechnung durchzuführen, können die stetigen Durchflussraten durch eine Textdatei `*.qsl` ASCII ersetzt werden. Zu diesem Zweck lässt sich die `.cli`-Datei jederzeit später mit einer Basis {ref}`text editor <npp>` einfach anpassen.
