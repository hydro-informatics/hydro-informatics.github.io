---
description: Tutorial zur Vorverarbeitung eines digitalen Aufzugsmodells (Digitales Oberflächenmodell (DOM)) in QGIS zur Erzeugung eines Rechennetzes im SMS 2dm Format für hydrodynamische BASEMENT-Simulationen.
---

(qgis-prepro-bm)=
# Vorverarbeitung mit QGIS

```{admonition} Requirements
:class: attention
Dieses Tutorial ist konzipiert für **Anfänger* und vor dem Tauchen in dieses Tutorial stellen Sie sicher:

* Folgen Sie den Installationsanleitungen für {ref}`qgis-install` in diesem eBook.
* Lesen Sie (oder beobachten) und verstehen Sie das eBook {ref}`qgis-tutorial`.
```

Die ersten Schritte in der numerischen Modellierung eines Flusses mit BASEMENT bestehen in der Umwandlung eines **Digital Elevation Model ({term}`DEM`)* in ein Rechennetz. Dieses Tutorial führt durch die Erstellung eines QGIS-Projekts zur Umwandlung eines {term}`DEM` ({term}`GeoTIFF`) in ein Rechennetz, das mit verschiedenen numerischen Modellierungssoftware in diesem eBook verwendet werden kann. Am Ende dieses Tutorials haben {ref}`chpt-basement`-Nutzer im Format {term}`SMS 2dm` ein Rechennetz generiert.

```{admonition} Platform compatibility
:class: tip
Alle in diesem Tutorial enthaltenen Software-Anwendungen können auf *Linux*, *Windows* und *macOS* (in der Theorie - nicht getestet) Plattformen ausgeführt werden. Beachten Sie, dass {ref}`chpt-basement` selbst nicht an *macOS* Plattformen arbeiten wird.
```

```{admonition} Recall: BASEMENT versions, BASEMD, and BASEHPC
:class: note

Die BASEMENT-Version 2 (v2) wurde mit komplexen Strukturen und einer breiten Palette von Kapazitäten entwickelt, jedoch wurde wenig Fokus auf die Rechenzeit gezogen. BASEMENT Version 3 (v3) vereinfachte den Modellierungsprozess für Anwender erheblich und verfügte über hocheffiziente Rechenoptionen, einschließlich massiver Parallelisierung auf GPUs. Der vereinfachte v3 fehlt jedoch an vielen relevanten Modulen, wie z.B. Mehrschicht-Flussbetten zur Berechnung des topographischen Wandels in Abhängigkeit von Mehrkorngrößen-Bettladungstransportformeln. Die BASEMENT Version 4 (v4) bietet nun sowohl die vielfältigen Kapazitäten von v2 in Form von BASEMD-Setups als auch die Recheneffizienz von v3 in Form von BASEHPC-Setups. Dieses Tutorial erklärt die Einrichtung eines BASEHPC-Modells.

```

(start-qgis)=
## QGIS Setup

### Koordinatenreferenzsystem (Koordinatenreferenzsystem)

Starten Sie QGIS und {ref}`create a new QGIS project <qgis-project>`, um mit diesem Tutorial zu beginnen.
Wie in der {ref}`qgis-tutorial` dargestellt, wurde für das Projekt ein Koordinatenreferenzsystem (Koordinatenreferenzsystem) eingerichtet. Dieses Beispiel verwendet Daten eines Flusses in Bayern (Deutschland-Zone 4), die folgende Koordinatenreferenzsystem erfordert:

* Im QGIS Top-Menü gehen Sie zu **Projekt*****Properties**.
* Aktivieren Sie die Registerkarte **Koordinatenreferenzsystem**.
* Geben Sie `Germany_Zone_4` ein und wählen Sie das Koordinatenreferenzsystem unter {numref}`Fig. %s <qgis-crs>`.
* Klicken Sie auf **Apply** und **OK***.

```{figure} ../img/qgis/inn-crs.png
:alt: qgis set coordinate reference system crs germany zone_4 Inn river
:name: qgis-crs

Define Germany Zone 4 als Projekt Koordinatenreferenzsystem.
```

```{admonition} Save the project...
:class: tip
Speichern Sie das QGIS-Projekt (*Project*****Save As...**), z.B. unter dem Namen **prepro-tutorial.qgz**.
```

(get-basemesh)=
### Erhalten Sie das BASEmesh Plugin

Installieren Sie *BASEMENT*'s *BASEmesh* Plugin (Anweisungen aus dem *BASEMENT* Systemhandbuch):

* Laden Sie den *QGIS* Plugin Manager: **Plugins* Menü > **Verwalten und Installieren von Plugins**.
* Gehen Sie zur Registerkarte **Einstellungen**.
* Scrollen Sie nach unten (**Plugin Repositories** Listbox in {numref}`Fig. %s <qgis-plugins2>`), klicken Sie auf **Add...**.
* Geben Sie im Popup-Fenster ein:
  * einen Namen für das neue Projektarchiv, zum Beispiel `BASEmesh Plugin Repository`
  * the repository address: [https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml](https://people.ee.ethz.ch/~basement/qgis_plugins/qgis_plugins.xml)
  * alle anderen Voreinstellungen beibehalten.
* Klicken Sie auf **OK**. Das neue Repository sollte nun im Listenfeld **Plugin Repositories** sichtbar sein. Wenn die Verbindung **OK* ist.

```{figure} ../img/qgis/bm-plugin.png
:alt: qgis basement plugins
:name: qgis-plugins2

Fügen Sie das BASEMENT-Repository zum QGIS-Plugins-Manager hinzu.
```

* Noch im **Plugins** Popup-Fenster gehen Sie zurück auf den **All* Tab und geben Sie im Suchfeld `basemesh` ein.
* Finden Sie das **newest BASEmesh** (d.h. ** Verfügbare Version** >= 2.0.0) Plugin und klicken Sie auf **Install Plugin**.
* Nach der erfolgreichen Installation **Close** das **Plugins** Popup-Fenster.
* Vergewissern Sie sich, dass das *BASEmesh 2* Plugin jetzt im Menü QGIS' **Plugins** verfügbar ist (siehe {numref}`Fig. %s <qgis-pluggedin>`).

```{figure} ../img/qgis/bm-pluggedin.png
:alt: qgis basement plugins
:name: qgis-pluggedin

Das BASEmesh 2 Plugin ist nach der erfolgreichen Installation im QGIS Plugins Menü verfügbar.
```


(get-dem)=
## Digitales Oberflächenmodell (DOM)

This tutorial uses an application-ready {term}`DEM` in {term}`GeoTIFF` {ref}`raster` format that stems from a {term}`Lidar` point cloud. The {term}`DEM` raster provides height (Z) information from a section of a gravel-cobble bed river in South-East Germany, which constitutes the baseline for the computational grids featured in the next sections. To get the provided DEM in the *QGIS* project:

* [** Laden Sie das Beispiel Digitales Oberflächenmodell (DOM) GeoTIFF*](https://github.com/hydro-informatics/materials-bm/raw/main/rasters/dem.tif) herunter und speichern Sie es im gleichen Ordner (`/Project Home/` oder Unterverzeichnis) wie das oben erstellte **qgz**-Projekt.
* Fügen Sie die heruntergeladene Digitales Oberflächenmodell (DOM) als neue Rasterschicht in *QGIS* hinzu:
  * In *QGIS*' **Browser** finden Sie das **Project Home**-Verzeichnis, in dem Sie das Digitales Oberflächenmodell (DOM) *tif* heruntergeladen haben.
  * Ziehen Sie den Digitales Oberflächenmodell (DOM) *tif* aus dem **Projekt Home* Ordner in das QGIS' **Layer* Panel.
* Um später die Abgrenzung bestimmter Regionen des Flussökosystems zu erleichtern, fügen Sie eine {ref}`satellite imagery basemap <basemap>` (XYZ-Fliese) unter der {term}`DEM` hinzu und passen Sie die Layer-Symbologie an.

```{admonition} What are QGIS panels again?
:class: tip
Erfahren Sie mehr im *QGIS* Tutorial unter {ref}`qgis-tbx-install`.
```

Die Digitales Oberflächenmodell (DOM) sollte nun auf der Karte angezeigt werden (wenn nicht: mit der rechten Maustaste auf die Digitales Oberflächenmodell (DOM)-Schicht und klicken Sie auf **Zoom auf Layer(s)* im Kontextmenü) wie unter {numref}`Fig. %s <qgis-dem-basemap>` dargestellt.

```{figure} ../img/qgis/dem-basemap.png
:alt: qgis import raster DEM basemap
:name: qgis-dem-basemap

Die importierte Digitales Oberflächenmodell (DOM) auf einer Google-Satelliten-Bildungsbasiskarte (Quelle: Google / GeoBasis-DEBKG 2019). Die Strömungsrichtung ist von links nach rechts nach dem Pfeil **Q**.
```


(make-2dm)=
## 2dm Mesh erstellen

Die Generation einer {term}`SMS 2dm` nutzt die {ref}`QGIS BASEmesh plugin <get-basemesh>` und erfordert die Zeichnung

* {ref}`Line Shapefile <create-line-shp>` mit Modellgrenzen und internen Bruchlinien zwischen Modellregionen mit unterschiedlichen Eigenschaften (Abschnitt {ref}`boundary`);
* {ref}`Line Shapefile <create-line-shp>` mit Modellgrenzen für die Zuweisung von Zu- und Abflussbedingungen (Abschnitt {ref}`liquid-boundary`) und a
* {ref}`Point Shapefile <create-point-shp>` mit Markern für die Definition von Merkmalen der Modellregionen (Abschnitt {ref}`regions`).

Diese Shapefiles ermöglichen die Erzeugung einer {ref}`Quality Mesh <qualm>`. Letztendlich sind Höheninformationen {ref}`interpolated to the quality mesh <qualm-interp>` und das resultierende Mesh wird als {term}`SMS 2dm`-Datei gespeichert. Die nächsten Abschnitte gehen Schritt für Schritt durch den Verfahrensschritt mit detaillierten Erläuterungen. Weitere Materialien und Zwischenprodukte werden im ergänzenden Datenrepository ([materials-bm](https://github.com/hydro-informatics/materials-bm)) für dieses Tutorial bereitgestellt.


(boundary)=
### Modell Boundary und Breaklines

The model boundary defines the model extent and can be divided into regions with different characteristics (e.g., roughness values) through breaklines. Breaklines indicate, for instance, channel banks and the riverbed (main channel), and need to be inside the DEM extents. Boundary lines and breaklines are stored in a {ref}`Line Shapefile <create-line-shp>` that BASEmesh uses to find both model boundaries and internal breaklines between model regions. For this purpose, {ref}`create-line-shp` with **one Text Field** called **LineType** and call it **breaklines.shp** (**Layer** > **Create Layer** > **New Shapefile Layer**). Click on QGIS' **Layers** menu > **Create Layer** > **New Shapefile Layer...** (see {numref}`Fig. %s <qgis-new-lyr>`). Make sure to select `ESRI: 31494 - Germany_Zone_4` as {term}`CRS` <img src="../img/qgis/sym-crs.png">.

```{figure} ../img/qgis/create-shp-layer.png
:alt: qgis new layer basemesh
:name: qgis-new-lyr

Erstellen Sie eine neue Formdatei aus dem QGIS' Layers Menü.
```

Es ist wichtig, dass sich die Linien nicht überschneiden, um mehrdeutige oder fehlende Definitionen von Regionen zu vermeiden und sicherzustellen, dass alle Grenzlinien geschlossene Bereiche (Flächen) bilden. Aktivieren Sie daher Snapping:

* Aktivieren Sie die *Snapping Toolbar*: **View****** **Toolbars*********
* **Snapping toolbar*****Enable Snapping***<img src="../img/qgis/snapping-horseshoe.png">
* Ermöglichen Sie Schnappen für
  * **Vertex**, **Segment** und **Middle of Segments**<img src="../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections*<img src="../img/qgis/snapping-intersection.png">.

Als nächstes bearbeiten Sie **breaklines.shp** mit einem Klick auf den gelben Stift<img src="../img/qgis/yellow-pen.png"> und zeichnen Sie die in {numref}`Fig. %s <breaklines>` angegebenen Zeilen durch Aktivierung **Add Line Feature**<img src="../img/qgis/sym-add-line.png">.

* **Boundäre des** Modells links und rechts **Boodplaingrenzen**:
  * Delineieren Sie die äußeren Grenzen der Flutplaine.
  * Stellen Sie sicher, dass alle Punkte und Zeilen innerhalb der {ref}`DEM layer <get-dem>` sind.
  * Überqueren Sie nicht den Fluss (eingebettet durch die Satellitenbildkarte angezeigt).
  * **Finalize*** jede Zeile mit **Rechtsklick***.
  * Für das Feld **LineType** verwenden Sie Textwerte wie **boundary Left/right floodplain**.
  * Siehe die **red Zeilen in {numref}`Fig. %s <breaklines>`**.
* **Breaklines der linken Bank (LB) und der rechten Bank (RB)*:
  * Zeichnen Sie Linien entlang des benetzten Hauptkanals in der Satellitenbildarchiv-Basiskarte angezeigt.
  * Stellen Sie sicher, dass die Linie perfekt mit den vorkonstruierten Überschwemmungsgrenzlinien übereinstimmt (das ist, wo Snapping hilft); so müssen die harten Bruchlinien des Hauptkanals und die Überschwemmungsgrenzlinien die Überschwemmungen ohne Lücke zwischen den Leitungen umschließen.
  * Für das Feld **LineType** verwenden Sie Textwerte wie **hardline LB/RB**.
  * Beziehen Sie sich auf die **yellow-orange Linien in {numref}`Fig. %s <breaklines>`** (Anmerken Sie die Abgrenzung der kleinen Nebenflüsse in der oberen linken Ecke der linken Bank und unten rechts an der rechten Bank).
* **Großbritannien**:
  * Zeichnen Sie Linien entlang der Kiesbanken, die in der Satellitenbildkarte im Hauptkanal sichtbar sind.
  * Stellen Sie sicher, dass die Linie mit den vorgefertigten Hauptkanalbruchlinien (Hardlines) perfekt zusammenfällt; so müssen die harten Bruchlinien des Hauptkanals und die Kiesbankbruchlinien die Kiesbanken ohne Lücke zwischen den Linien umschließen.
  * Für das Feld **LineType** verwenden Sie Textwerte wie **hardline Kiesbank**.
  * **grüne Linien in {numref}`Fig. %s <breaklines>`**.
* Optional: **Breaklines of block ramps*:
  * Finden Sie die groben Blockrampen (abstoßende Gewässer) in der Satellitenbildarchiv-Basiskarte und delineieren Sie sie durch Linien über den benetzten Hauptkanal.
  * Stellen Sie sicher, dass die Linie perfekt mit den Hauptkanalbruchlinien zusammenfällt; so müssen die harten Bruchlinien des Hauptkanals und die Blockrampenbruchlinien die Blockrampen ohne Spalt zwischen den Leitungen umschließen.
  * For the **LineType** field use text values such as **hardline sss** (or anything else - the example refers to the German word <u>S</u>chütt<u>s</u>tein<u>s</u>chwelle).
  * **blaue Linien in {numref}`Fig. %s <breaklines>`**.
* Optional: **Breakline einer Sandbank*:
  * Finden Sie die Sandbank-Lagerung in der oberen linken Ecke in {numref}`Fig. %s <breaklines>` auf der Satellitenbildkarte und delineieren Sie sie durch eine glatt gekrümmte Linie.
  * Stellen Sie sicher, dass die Linie endet perfekt mit den Hauptkanalbrüchen zusammenfallen und einen geschlossenen Bereich ohne Lücke zwischen den Linien umschließen.
  * Für das Feld **LineType** verwenden Sie Textwerte wie **hardline sand**.
  * Referentin **** in der oberen linken Ecke **in{numref}`Fig. %s <breaklines>`**.

Zu **richtige Zeichnungsfehler** verwenden Sie das **Vertex Tool**<img src="../img/qgis/sym-vertex-tool.png">. Schließlich speichern Sie die neuen Zeilen (Angaben von **breaklines.shp**), indem Sie auf das **Save Layer Edits**<img src="../img/qgis/sym-save-edits.png">symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.

```{figure} ../img/qgis/breaklines.png
:alt: qgis basement basemesh draw breaklines boundaries
:name: breaklines

Überwundene und Brechlinien, um **breaklines.shp** zu zeichnen. In Strömungsrichtung (**Q* Pfeil) werden linke und rechte Banken und Flutplaine ausgerichtet.
```

```{admonition} Troubles with drawing boundaries and breaklines?
:class: tip
Laden Sie das in der obigen Abbildung gezeigte [zipped breaklines formfile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/breaklines.zip) herunter und entpacken Sie es in den Projektordner, zum Beispiel `/Project Home/shapefiles/breaklines.[SHP]`.
```

Der Standardschichtstil ist **Single Symbol**. Für eine bessere Darstellung, doppelklicken Sie auf die Breaklines-Schicht, gehen Sie auf die **Symbology*-Tab und wählen Sie **Kategorisiert* (oder **Graduiert**) anstelle von **Single Symbol*** (an der Spitze des **Layer Properties*-Fensters). Im Feld **Value** wählen Sie **LineType**, klicken Sie dann auf die **Klassifikation*** Taste unten im Fenster **Layer Properties**. Die Listbox zeigt nun die *LineType* Werte an.

```{admonition} Draw boundaries of complex DEMs...
:class: tip
Die Zuggrenzen manuell rund um große {term}`DEM`s können sehr zeitaufwendig sein, insbesondere wenn die Rohdaten eine Punktwolke sind und noch nicht in eine {ref}`raster` umgewandelt werden.

Wenn Sie es mit einer Punktwolke zu tun haben, verwenden Sie *QGIS* [Convex Hull tool](https://docs.qgis.org/3.16/en/docs/training_manual/vector_analysis/spatial_statistics.html?highlight=convex%20hull#basic-fa-create-a-test-dataset), das ein eng begrenztes Polygon um Punkte zieht.

Wenn Sie sich mit einem großen {term}`GeoTIFF` beschäftigen, beachten Sie die Verwendung von QGIS' [Raster an Vector](https://docs.qgis.org/3.16/en/docs/training_manual/complete_analysis/raster_to_vector.html)tool.
```


(liquid-boundary)=
### Flüssige (Hydraulik)

Die Flüssigkeitsgrenzen definieren, wo hydraulische Bedingungen, wie eine gegebene Ableitungs- oder Phasenentladungsbeziehung, am Modellzufluss (Upstream) und Abfluss (downstream) Grenzen gelten. So benötigt ein funktionelles Flussmodell mindestens eine Zuflussgrenze (Linie), in der der Massenstrom in das Modell und eine Abflussgrenze (Linie), in der Massenflüsse das Modell verlassen. Zu diesem Zweck rufen {ref}`create-line-shp` **liquid-boundaries.shp** an und definieren ** zwei Textdatenfelder** mit dem Namen **type* und **stringdef***. Stellen Sie sicher, dass **snapping* noch **deabled** ist (wie oben im Abschnitt {ref}`boundary`) und **Toggle (Start) Editing**<img src="../img/qgis/yellow-pen.png"> die neuen **liquid-boundaries.shp**. Dann zwei Linien ziehen:

* Aktivieren Sie **Add Line Feature**<img src="../img/qgis/sym-add-line.png">.
* Eine Zuflussgrenze zeichnen (siehe auch {numref}`Fig. %s <inflow-boundary>`):
  * Zoomen Sie in den Zuflussbereich der Digitales Oberflächenmodell (DOM)-Grenze, wo zwischen** die oben erstellten **-Flottplain-Grenzlinien** liegen.
  * Starten Sie eine Linie auf der linken Bank (linke Seite der untenstehenden Figur) und zogen nach Osten (d.h. nach rechts), um sieben weitere Punkte über den Fluss zu machen.
  * Der **siebte Punkt** muss **coincide*** mit dem Ende der rechten Bank ** Floodplain Grenzlinie**.
  * So kommt der stromaufwärtige Fluss von der rechten Seite der Zuflussgrenzlinie (d.h. die stromaufwärts gerichtete Strömungsrichtung wird `right` für das numerische Modell sein).
  * **Finalize*** die Zeile mit einem **right-click***, und geben Sie `Inflow` im **type*-Feld und `inflow` im **stringdef**-Feld ein.
  * Zu **richtige Zeichnungsfehler** verwenden Sie das **Vertex Tool**<img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/inflow-boundary.png
:alt: qgis basemesh draw inflow boundary line
:name: inflow-boundary

Die Zulaufgrenzlinie wird von links nach rechts gezogen (d.h. der Vorstrom kommt von der rechten Seite der Zulaufgrenzlinie). Die Reihenfolge der zu verwendenden Tasten wird durch die roten Boxen hervorgehoben.
```

* Dann ziehen Sie eine Abflussgrenze (siehe auch {numref}`Fig. %s <outflow-boundary>`):
  * Zoomen Sie in den Abflussbereich der Digitales Oberflächenmodell (DOM)-Grenze, wo zwischen** die oben erstellten **Flottplain-Grenzlinien** liegen.
  * Starten Sie eine Linie auf der linken Bank (oben der unteren Figur) und bewegen Sie Südwesten (d.h. nach unten), um sieben weitere Punkte über den Fluss zu machen.
  * Der **siebte Punkt** muss **coincide*** mit dem Ende der rechten Bank ** Floodplain Grenzlinie**.
  * So kommt der stromaufwärtige Fluss von der rechten Seite der Abflussgrenzlinie (d.h. die stromaufwärts gerichtete Strömungsrichtung wird `right` für das numerische Modell sein).
  * **Finalize*** die Zeile mit einem **right-click***, und geben Sie `Outflow` im **type*-Feld und `outflow` im **stringdef**-Feld ein.
  * Zu **richtige Zeichnungsfehler** verwenden Sie das **Vertex Tool**<img src="../img/qgis/sym-vertex-tool.png">.

```{figure} ../img/qgis/outflow-boundary.png
:alt: qgis basemesh draw outflow boundary line
:name: outflow-boundary

Die Abflussgrenzlinie wird von oben nach unten gezogen (d.h. der stromaufwärtige Strom kommt von der rechten Handseite der Abflussgrenzlinie).
```

```{admonition} Constraints of inflow and outflow boundaries
:class: important
Die Zu- und Abfluss-Grenzlinien müssen die gleiche Anzahl von Knoten (hier 7 plus 1) aufweisen und keine flüssige Grenzlinie mehr als 40 Knoten aufweisen.
```

Schließlich speichern Sie die flüssigen Grenzlinien (Angaben von **liquid-boundaries.shp**), indem Sie auf das **Save Layer Edits**<img src="../img/qgis/sym-save-edits.png">symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol.

```{admonition} Troubles with drawing the liquid boundary lines?
:class: tip
Laden Sie das [zipped liquid-boundaries formfile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/liquid-boundaries.zip) herunter und entpacken Sie es in den Projektordner, zum Beispiel `/Project Home/shapefiles/liquid-boundaries.[SHP]`.
```

```{admonition} stringdefs
:class: note
Die Feldwerte *stringdefs* können direkt mit {ref}`chpt-basement` verwendet werden, wobei den hier definierten georeferenzierten Zu- und Abflussgrenzungslinien hydraulische Daten (z.B. Entladung, Wassertiefe oder Phasen-Entladungsverhältnisse) zugeordnet werden können.
```

(regions)=
### Landmarken

Regionenmarker werden innerhalb von Bereichen platziert, die durch Randlinien und Bruchlinien definiert sind. Jeder Bereichsmarker (d.h. ein Punkt irgendwo im Bereich) weist beispielsweise eine Materialkennung (MATIDs) und einen maximalen Netzzellenbereich zu. Letztere Option ermöglicht es, kleine Netzzellen (mesh-Bereiche) im aktiven Kanalbett zu definieren und kann größere Zellbereiche in den Flutplainbereichen. {ref}`create-point-shp` named **raster-points.shp** mit folgenden Definitionen (siehe auch {numref}`Fig. %s <qgis-reg-lyr>`):

* Definieren Sie den **Dateinamen* als **region-points.shp*** (oder ähnlich)
* Stellen Sie sicher, dass der **Geometrietyp** *** ist
* The {term}`CRS` <img src="../img/qgis/sym-crs.png"> corresponds to Germany Zone 4 ({ref}`see project CRS <start-qgis>`)
* Fügen Sie drei **Neue Felder**s hinzu (Zusätzlich zum Standard **Integer*** Typ ** Feld):
  * **max area** = **Dezimalzahl*** (**Länge** = 10, **Präzision* = 3)
  * ****** = *****************=***=*****=*************=**************=*****=******************=*************=**********************************=**********************************************************************************************************************
  * **Typ** = **Textdaten** (** Länge** = 20)
* Klicken Sie auf **OK**, um die neue Punktformdatei zu erstellen.

```{figure} ../img/qgis/bm-region-pts-create.png
:alt: basement mesh qgis region layer points
:name: qgis-reg-lyr

Definitionen und Felder, die der Region-Punkte-Formdatei hinzugefügt werden.
```

Betrachten Sie ** Deaktivieren Sie Snapping** zum Zeichnen der Region Marker, um zu vermeiden, dass Region Marker mit jeder Zeile zusammenfallen. Dann **Toggle (Start) Editing**<img src="../img/qgis/yellow-pen.png"> die neue **region-points.shp**-Datei und aktivieren **Add Point Feature***<img src="../img/qgis/sym-add-point.png">. Zeichnen Sie einen Punkt in jedem Bereich, der von Bruchlinien und (flüssigen) Begrenzungslinien eingeschlossen ist. Abhängig vom scheinbaren Flächentyp aus der Satellitenbildarchiv-Basiskarte, ordnen Sie eine der fünf Regionen unter {numref}`Tab. %s <region-defs>` an jeden Punkt.

```{list-table} Region names and their **max_area**, **MATID**, and **type** field values.
:header-rows: 1
:name: region-defs

* - Region
  - Flussbett
  - Blockrampen
  - Gravel Banken
  - Floodplas
  - Sand
* - **max area*
  -  25.0
  -  20.0
  -  25.0
  -  80,0
  -  20.0
* - ** MATID**
  - 1
  - 2.
  - 3
  - ANHANG
  - 5.
* - ** Typ**
  - Flussbett
  - Block-Rampe
  - Kroatisch
  - Flutpla
  - sand deposit
```

Nach dem Zeichnen eines Punktes in jedem geschlossenen Bereich, speichern Sie die Region Punktmarker (Angaben von **region-points.shp**), indem Sie auf das **Save Layer Edits**<img src="../img/qgis/sym-save-edits.png">symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../img/qgis/yellow-pen.png"> Symbol. {numref}`Figure %s <qgis-reg-pts>` zeigt ein Beispiel für Region Markerpunkte innerhalb der von den Breaklines delineierten Bereiche.

```{figure} ../img/qgis/bm-region-pts-map.png
:alt: basemesh region points
:name: qgis-reg-pts

Beispiel für Bereichspunktmarker in den Projektgrenzen.
```

```{admonition} Troubles with drawing the region marker points?
:class: tip
Laden Sie die [zipped region-points formfile](https://github.com/hydro-informatics/materials-bm/raw/main/shapefiles/region-points.zip) herunter und entpacken Sie sie in den Projektordner, z.B. `/Project Home/shapefiles/region-points.[SHP]`.
```

(qualm)=
### Erstellen eines Qualitäts-Mesh

Das hochwertige Mesh-Tool von *BASEmesh* schafft ein rechnerisch effizientes dreieckiges Mesh basierend auf {cite:t}`shewchuk1996` und innerhalb der oben definierten Modellgrenzen. Das Tool verbindet Mesh-Eigenschaften mit der Region Shapefile ([siehe oben Abschnitt unter {ref}`regions`), aber es enthält keine Elevationsdaten. Nach dem Erzeugen eines Qualitätsnetzes müssen also Höheninformationen hinzugefügt werden. Dieser Abschnitt erklärt die Qualitätsmaschenerzeugung und der nächste Abschnitt zeigt die Interpolation der unteren Erhebungen.

Im Menü QGIS' **Plugins** klicken Sie auf **BASEmesh 2****** **QUALITY MESHING**, um das Qualitätsmaschenwerkzeug zu öffnen. Geben Sie im Popup-Fenster folgende Einstellungen ein (siehe auch {numref}`Fig. %s <qgis-qualm>`):

* Triangulation Zwänge Rahmen:
  * **Breaklines** = **Breaklines*** (siehe {ref}`boundary`)
  * Halten Sie alle anderen Standardeinstellungen.
* Rahmen der Regionen:
  * **Aktivieren Sie das Kontrollkästchen Regionen**.
  * **Regionsmarkerschicht** = **Regionen-Punkte** (siehe {ref}`regions`).
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
  * Klicken Sie auf den **Browse...* Button und definieren Sie einen Dateinamen **2dm** im `/Project Home/`-Verzeichnis, wie **prepro-tutorial quality-mesh.2dm***.
* Klicken Sie auf die Schaltfläche **Run**, um das Qualitätsmaschen zu erstellen.


```{figure} ../img/qgis/bm-quality-meshing-success.png
:alt: basement qgis quality mesh tin
:name: qgis-qualm

Definitionen in BASEmeshs Qualitätsmaschenwerkzeug.
```

Qualität Meshing kann Zeit nehmen. Nach einer erfolgreichen Mesh-Generierung wurde die Datei **prepro-tutorial quality-mesh-interp.2dm** erzeugt.

(qualm-interp)=
### Interpolate Bottom Elevation to Quality Mesh

The *BASEmesh* plugin's **Interpolation** tool projects bottom elevation data onto the quality mesh by interpolation from another mesh or a {term}`DEM` {ref}`raster`. Here, we use the {ref}`above-introduced DEM GeoTIFF <get-dem>`. To run the interpolation, open *BASEmesh*'s **Interpolation** tool (*QGIS* **Plugins** menu > **BASEmesh 2** > **Interpolation**) and make the following settings (see also {numref}`Fig. %s <qgis-qualm-interp>`):

* In der **Mesh-Schicht zum Interpolieren**-Rahmen, wählen Sie **prepro-tutorial quality-mesh**.
* In der Registerkarte **Basic** finden Sie den **Elevationsquelle** Rahmen und aktivieren Sie die **Aktivierung über Digitales Oberflächenmodell (DOM) (Raster)** Funktaste.
* Wählen Sie **dem.tif** GeoTIFF (siehe {ref}`get-dem` Sektion) als **Rasterschicht**.
* Im **Output**-Rahmen klicken Sie auf die **Browse**-Taste, um einen Ausgabenetznamen im `/Project Home/`-Verzeichnis zu definieren, z.B. **prepro-tutorial quality-mesh-interp.2dm***
* Klicken Sie auf ****, um das höheninterpolierte Mesh zu erstellen.

```{admonition} Error with BASEmesh v2.0.9 - Interpolation via DEM not working
:class: error

Seit BASEmesh v2.0.9 erkennt das **Interpolation**-Fenster keine **Rasterschicht*** (Nichts kann aus dem Dropdown-Menü ausgewählt werden). Ein funktionaler Work-around ist es, den Digitales Oberflächenmodell (DOM)-Raster in eine Mesh-Datei zu konvertieren:

1. Konvertieren Sie die Digitales Oberflächenmodell (DOM) in eine Punktformdatei (**raster zu Vektor**) und stellen Sie sicher, dass die Attributtabelle des Punktes mit Erhebungen gefüllt ist.
2. Verwenden Sie das **TIN Mesh Creation** Tool, um ein TIN-Höhengitter mit Höhendaten zu erzeugen.
3. Wählen Sie im BASEmesh's **Interpolation**-Tool die Option **Interpolation über Elevation Mesh** aus und wählen Sie das zuvor erstellte TIN Elevationsmaschen aus.
4. Klicken Sie auf **Run**, um mit dem Tutorial fortzufahren.

Um die oben genannten Konvertierungstools zu finden, gehen Sie zum QGIS **Processing* Top-Menü > **Toolbox** und geben Sie die Werkzeugnamen im Feld *search...* ein.

```

```{figure} ../img/qgis/bm-mesh-interpolation.png
:alt: qgis quality mesh interpolation basement
:name: qgis-qualm-interp

BASEmesh's Z-Wert (Höhe) Interpolation Tool und Setup, um unteren Höhenwerte dem Qualitätsmaschen zuzuordnen.
```

Nach der Erhebungsinterpolation überprüfen Sie, ob die Erhebungen korrekt zugeordnet sind (d.h. die **Bed Elevation** sollte Werte zwischen **367* und **387** m a.s.l) genommen haben. Um die Schichtvisualisierung (Symbology) zu ändern, doppelklicken Sie auf das neue **prepro-tutorial quality-mesh-interp* und gehen Sie zum **Symbology** Band. Wählen Sie **Graduiert** an der Spitze des Fensters, setzen Sie die **Value** auf Z, **Method* auf COLOR, wählen Sie eine Farbrampe und klicken Sie auf die **Klassifikation** unten (unterer Teil des Fensters). Klicken Sie auf **Apply** und **OK**, um die Symbologieeinstellungen zu schließen. {numref}`Figure %s <qgis-verify-qualm>` zeigt ein Beispiel für die Visualisierung des höheninterpolierten Netzes.

```{figure} ../img/qgis/bm-mesh-interp-success.png
:alt: basemesh verify interpolated quality mesh
:name: qgis-verify-qualm

Verifizieren Sie die Höheninterpolation mit abgestuften Farbrampen.
```

(qgis4bm)=
## Verwendung mit BASEMENT

Die in diesem Tutorial erstellte 2dm mesh-Datei kann direkt mit {ref}`chpt-basement` verwendet werden, wobei wie später erläutert nur die Definition von Eigenschaften der geometrischen (z.B. Rauheitskoeffizienten) und Flüssigkeit (z.B. Entladungen) erforderlich ist.
