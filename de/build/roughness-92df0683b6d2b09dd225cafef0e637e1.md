---
description: Definieren Sie räumlich verteilte Reibungs- und Rauheitszonen in TELEMAC2d unter Verwendung von QGIS und BlueKenue, wobei Sie Manning- oder Strickler-Koeffizienten verschiedenen Flussbettmaterialtypen zuweisen.
---

```{admonition} Contributors
:class: tip
This chapter was co-written and developed by [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/) <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="25" height="25"> and [Sebastian Schwindt](https://sebastian-schwindt.org) <img src="../../img/authors/sebastian.jpg" alt="Sebastian Schwindt" width="25" height="25">.
```

(tm-friction-zones)=
# Reibungszonen

Similar to the assignment of multiple friction coefficient values to multiple model regions featured in the {ref}`BASEMENT tutorial <bm-geometry>`, Telemac2d provides routines for domain-wise (i.e., zonal) friction area definitions in the geometry (`.slf`) mesh file. Specifically, if the study domain is characterized by regions of different roughness, it is not sufficient to define global friction through a `FRICTION COEFFICIENT` keyword in the steering (`.cas`) file. Defining roughness zones in the mesh (`.slf`) file requires an additional layer called `BOTTOM FRICTION` or `FRIC_ID` on top of the `BOTTOM` elevation. To this end, roughness values can be defined in a roughness `.xyz` file created with QGIS ({ref}`recommended <tm-friction-qgis>`) or *Closed Lines* `.i2s` created with BlueKenue ({ref}`see the meshing section <bk-import-friction>`). While QGIS is recommended to delineate roughness zones with correct and possibly precise georeferences, BlueKenue is still required for interpolating the roughness from the `.xyz` or `.i2s` file on the `.slf` file in the last step.


```{admonition} Requirements

* Understand geospatial data formats and know to work with QGIS (see the {ref}`QGIS tutorial <qgis-tutorial>`).
* Füllen Sie {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>` aus.
* Installation von {ref}`BlueKenue (also works on Linux, see the installation guide) <bluekenue>` und {ref}`Telemac <telemac-install>`.
```

```{admonition} Roughness versus friction

Rauheit beschreibt die Unebenheit oder Robustheit von festen Oberflächen, wie Flussbetten. Boundary Rougness erhöht den Strömungswiderstand, verursacht Reibung und verlangsamt die Wasserbewegung.
```


(tm-friction-qgis)=
## Roughness.XYZ mit QGIS (empfohlen)

Der erste Schritt zur Abgrenzung von Rauheitszonen in QGIS besteht darin, das Koordinatenreferenzsystem einzurichten und das Projekt analog zum {ref}`QGIS pre-processing tutorial <tm-qgis-prepro>` zu speichern:

* Öffnen Sie QGIS und gehen Sie im oberen Menü zu **Project** > **Properties**.
* Aktivieren Sie den **Koordinatenreferenzsystem**-Tab.
* Set the CRS that your {ref}`basemap <basemap>` / {term}`Digitales Oberflächenmodell <DEM>` data use; for this example, enter `UTM zone 33N` and select *UTM zone 33N (WGS84)* (EPSG 32633), which is not a great choice because of its low precision, but it will do the job for this tutorial.
* Klicken Sie auf **Apply** und **OK**.
* Speichern Sie das Projekt in einem neuen Ordner, in dem alle Dateien für dieses Tutorial gespeichert werden.

Es wird wichtig sein, Überschneidungen zu vermeiden, die zu mehrdeutigen oder fehlenden Definitionen von Regionen führen würden. Aktivieren Sie daher Snapping:

* Aktivieren Sie die *Snapping Toolbar *: **View * > **Snapping Toolbar *
* In der **Snapping-Symbolleiste** > **Snapping** aktivieren <img src="../../img/qgis/snapping-horseshoe.png">
* Ermöglichen Sie Snaping für
  * **Vertex**, **Segment** und **Mitte der Segmente** <img src="../../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../../img/qgis/snapping-intersection.png">.
  * **Self Snapping** <img src="../../img/qgis/sym-self-snapping.png">.

This tutorial picks up the example from the {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>` to draw polygons along the [breaklines](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) and [liquid-boundaries](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles. The friction zones are inferred from a {ref}`Google Satellite basemap <basemap>` and friction attributes are qualitatively estimated, which is just fine for a tutorial. In practice, we strongly recommend performing field surveys on grain size distributions with high-precision differential GPS (DGPS) systems to delineate roughness zones on-site supported by drone imagery.

```{admonition} AI can be more efficient (though less effective)
:class: tip
:name: ai-image-recognition-numerics

This tutorial shows how to manually draw polygons delineating particular roughness zones, such as *sand*, *gravel*, or *vegetation*. However, artificial intelligence (AI) has already been proven to do a great job in automatically recognizing similar terrain patches for consistent recognition of roughness zones. Examples can be found in {cite:t}`diazgomez_mapping_2022` or [Kenny Larrieu's implementation of Segment Anything EO tools](https://github.com/klarrieu/segment-anything-eo).

Was Sie brauchen, ist:

* eine moderne Drohne (nicht mehr zu teuer)
* Ground Truth: Daten über Korngrößenverteilungen (> Kies: Kieszahl, Sand zu Kies: Beutel & Sieb, sehr feines Sediment: Gefrierkern / Platte & Sieb), Objektetiketten (d.h. DGPS-Punktemarkierung *vegetation / types*, *wood*, *reinforced banks*, *roads*, etc.)
* Ein Algorithmus, der jedes Drohnenbild klassifiziert, nachdem er auf der Bodenwahrheit trainiert wurde; wir arbeiten gerade daran und stellen es hier zur Verfügung - bleiben Sie dran.
```

### Abgrenzung von Rauhigkeitszonenpolygonen

Die Rauhigkeitszonen können durch Attribute eines Polygon-Shapefiles beschrieben werden. Um eine neue Polygon-Shapefile zu erstellen, gehen Sie zu **Layer** > **Create Layer** > **New Shapefile Layer...** (siehe {numref}`Fig. %s <new-qgis-lyr-rough>`).

```{figure} ../../img/telemac/qgis-add-lyr.png
:alt: create polygon shapefile roughness zones telemac
:name: new-qgis-lyr-rough

Erstellen Sie ein neues Polygon Shapefile.
```

Geben Sie im Popup-Fenster die folgenden Definitionen ein:

* **Dateiname**: Drücken Sie **...**, navigieren Sie zum Projektordner und tippen Sie auf `friction-polygons`.
* **Dateicodierung**: Standard beibehalten (Probedateien verwenden `UTF-8`).
* **Geometrietyp**: `Polygon`
* Unterhalb der *Zusätzlichen Dimensionen * (nicht erforderlich) finden und klicken Sie auf die Schaltfläche **Koordinatenreferenzsystem **, um das oben definierte Projektkoordinatensystem auszuwählen (Beispieldateien: `EPSG:32633`).
* Fügen Sie ein **neues Feld** hinzu:
  * **Name**: `dMean`
  * **Typ**: `Decimal (double)`
  * **Länge**: `10`
  * **Präzision**: `5`
  * Klicken Sie auf **Add to Fields List**
* Fügen Sie ein weiteres **Neues Feld** hinzu:
  * **Name**: `fricID`
  * **Typ**: `Integer (32 bit)`
  * **Länge**: `5`
  * Klicken Sie auf **Add to Fields List**
* Drücken Sie **OK**, um das neue Shapefile zu erstellen.

To follow this tutorial, import the [breaklines (download as zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) and [liquid-boundaries (download as zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) shapefiles from the Telemac pre-processing. To draw polygons by editing fiction-polygons.shp along the breaklines and liquid boundaries, highlight **fiction-polygons** in the *Layers* panel, and enable editing by clicking on the yellow pen <img src="../../img/qgis/yellow-pen.png">. Activating **Add Polygon Feature** and draw polygons by snapping to points of the *breaklines* and *liquid boundaries* layers, according to {numref}`Fig. %s <tm-fricID-polygons>`. To **finalize each polygon** with a **right-click on the mouse** and **enter** the `fricID` and `dMean` values according to {numref}`Tab. %s <tab-tm-fricID-zones>` (qualitative grain sizes).

To **correct drawing errors** use the **Vertex Tool** <img src="../../img/qgis/sym-vertex-tool.png">. Finally, save the new polygons (edits of **friction-zones.shp**) by clicking on the **Save Layer Edits** <img src="../../img/qgis/sym-save-edits.png"> symbol. **Stop (Toggle) Editing** by clicking again on the yellow pen <img src="../../img/qgis/yellow-pen.png"> symbol.

**Alternatively, merge the breaklines and liquid boundaries, and use the *Polygonize* tool from the *Processing Toolbox* to convert the merged lines into a polygon shapefile.** However, the polygonization will miss some breaklines, which will require editing. Also, the `fricID` and `dMean` fields still need to be added through editing.

```{figure} ../../img/telemac/fricId-zones-overview.jpeg
:alt: qgis telemac roughness zone polygons
:name: tm-fricID-polygons

Beispiel für die Beschreibung von Rauheitszonen (Reibungszonen) mit Polygonen durch vier Reibungs-IDs (fricID), die (1) das Flussbett, (2) Blockrampen, (3) Schotterstäbe und (4) Auen begrenzen. Hintergrundkarte: {cite:t}`googlesat` Satellitenbilder.
```

```{list-table} Four exemplary friction zones described by integer fricIDs and mean grain size diameters dMean.
:header-rows: 1
:name: tab-tm-fricID-zones

* - Zonenbezeichnung
  - Flussbett
  - Blockrampen
  - Grasbanken
  - Überschwemmungsgebiete
* - Fricid
  - 1
  - 2
  - 3
  - 4
* - dMittelwert (m)
  - 0,080
  - 0,300
  - 0,033
  - 1.000
```

```{admonition} Download the friction-polygons shapefile
:class: tip
Laden Sie die [gezippten Friktionspolygone shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-polygons.zip) und entpacken Sie sie in den Projektordner, zum Beispiel `/ProjectHome/friction-polygons.[SHP]`.
```

### Rauhigkeitspunkte erzeugen

Der nächste Schritt auf dem Weg zum Erstellen der erforderlichen XYZ-Datei zum Zuweisen von Reibungszonen zu einer Selafin-Geometrie-Datei besteht darin, (zufällige) Punkte innerhalb der oben erstellten Polygone zu erzeugen. Zu diesem Zweck geben Sie `random points inside polygons`** im Feld **search** der **Processing Toolbox** ein. Im Popup-Fenster **Random Points Inside Polygons** ({numref}`Fig. %s <tm-fric-polygons2pts>`) geben Sie Folgendes ein:

* **Eingabeschicht**: `friction-polygons`
* **Sampling-Strategie**: `Points density`
* **Point count or density**: `0.25`  - use a smaller/larger value for fine/coarse meshes, but beware of potentially very large file sizes
* **Minimum distance between points**: `5.0`  - use a smaller/larger value for fine/coarse meshes
* **Random points**: click on **...** and define a target point shapefile name, such as `friction-pts.shp` to be stored in the project folder.
* Klicken Sie auf **Run**, um die Punkte Shapefile zu erstellen. Dieser Vorgang kann je nach definierter Punktdichte eine Weile dauern.

The resulting point shapefile is shown in {numref}`Fig. %s <tm-fric-pts>`.

```{figure} ../../img/telemac/fric-zones-pts.png
:alt: random points polygons qgis telemac roughness zone
:name: tm-fric-polygons2pts

Einstellungen im Tool Random Points Inside Polygons in QGIS. Wählen Sie sorgfältig die Punktzahl oder Dichte aus, was sehr große Ausgabedateien verursachen kann. Das Mindestabstandsfeld kann verwendet werden, um die Anzahl der Punkte zu reduzieren.
```

```{figure} ../../img/telemac/fric-pts.jpg
:alt: random points roughness zone
:name: tm-fric-pts

Die Punktformdatei, die sich aus der Verwendung des Tools Random Points Inside Polygons in QGIS ergibt. Hintergrundkarte: {cite:t}`googlesat` Satellitenbilder.
```

```{admonition} Download the friction-pts shapefile
:class: tip
Laden Sie die [zipped friction-pts shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts.zip)] herunter und entpacken Sie sie in den Projektordner, zum Beispiel `/ProjectHome/friction-pts.[SHP]`.
```


### Zuweisen von Reibungsattributen zu Punkten

Leider nimmt die Punktgenerierung die Polygonattribute nicht automatisch auf, die auf die Punkte interpoliert werden müssen. Abhängig vom angestrebten Rauheitsgesetz für die Verwendung mit Telemac können entweder die Reibungs-IDs oder direkt Rauheitskoeffizienten zur Attributtabelle des Friktionspunkt-Shapefiles hinzugefügt werden. In diesem Tutorial wird ein Reibungskoeffizient in Form der Strickler-Rauheit interpoliert und mit einer empirischen Formel berechnet. Ein komplexerer Fall für die Berechnung von Rauheitswerten findet sich in der Fallstudie Donau (*Donau*) der BAW (unter `HOMETEL/examples/telemac2d/donau/`).

Die Übertragung der `dMean` und/oder `fricID`-Attribute der Polygone zu den Punkten ist im Wesentlichen eine Interpolationsoperation, bei der QGIS jeden Punkt betrachtet und ihm die `dMean` und/oder `fricID`-Attribute des nächstliegenden Polygons zuweist. Klicken Sie dazu auf das **Vector** Top-Menü > **Data Management Tools** > **Join Attributes by Location** (siehe {numref}`Fig. %s <fric-data-mgmt-join-attributes>`).


```{figure} ../../img/telemac/fric-data-mgmt-join-attributes.png
:alt: qgis friction points attribute table
:name: fric-data-mgmt-join-attributes


Öffnen Sie das Join Attributes by Location Tool in QGIS.
```


```{figure} ../../img/telemac/fric-join-attributes-by-location.png
:alt: qgis friction join attributes by location
:name: fric-join-attributes-by-location
:width: 75%
:align: right

Öffnen Sie die Attributtabelle der Friktionspunkttabelle.
```

Führen Sie im Popup-Fenster ({numref}`Fig. %s <fric-join-attributes-by-location>`) die folgenden Einstellungen durch:

* ** Verbinden Sie sich mit Features in**: `friction-pts`
* **Features they (geometric predicate)**: check the `are within` box, deselect all others
* **Durch Vergleich mit**: `friction-polygons`
* ** Zum Hinzufügen von Feldern**: Klicken Sie auf die Schaltfläche **...**, um `fricID` und/oder `dMean`
* **Join type**: `Take attributes of the first matching feature only (one-to-one)`
* **Joined layer**: Klicken Sie auf die Schaltfläche **...** > **Speichern zur Datei** > Navigieren Sie zum ** Projektordner** > ** Geben Sie einen Dateinamen ein, z. B. `friction-pts-at`**
* Klicken Sie auf **Run**.

Die Fehlermeldung *Kein räumlicher Index existiert für die Eingabeschicht, die Leistung wird stark beeinträchtigt * kann für diese Anwendung ignoriert werden. Um jedoch eine falsche Ausgabe zu überprüfen, ist es möglicherweise ratsam, auch die Schicht **Unverbindliche Merkmale der ersten Schicht ** zu definieren.

Infolgedessen ist das **friction-pts-at** im **Layers**-Panel verfügbar (siehe {numref}`Fig. %s <fric-pts-open-at>`).

Um die mittleren Korngrößen (`dMean`) in Reibungswerte umzuwandeln, öffnen Sie die *Attributtabelle* durch ** Rechtsklick** auf der ** Reibung-pts-at**-Schicht im **Layers**-Panel > **Offene Attributtabelle**.

```{figure} ../../img/telemac/fric-pts-open-at.jpg
:alt: qgis friction points attribute table
:name: fric-pts-open-at


Öffnen Sie die Attributtabelle der Friktionspunkt-Shapefile mit Attributtabelle. Hintergrundkarte: {cite:t}`googlesat` Satellitenbilder.
```


Bearbeiten Sie die **Attributtabelle** ({numref}`Fig. %s <fric-pts-at-edit>`):

1. Editing ermöglichen,
1. remove unnecessary columns, such as the `id` field, and potentially also the `fricID` field (this showcase will only use the `dMean` column),
1. Öffnen Sie den **Feldrechner **, mit dem wir im nächsten Schritt Strickler-Rauheitswerte ableiten werden.


```{figure} ../../img/telemac/fric-pts-at-edit.png
:alt: friction points edit attribute table
:name: fric-pts-at-edit

Die Attributtabelle der Friction-pts-at-Schicht mit den hervorgehobenen (roten Rechtecken) Bearbeiten, Entfernen von Spalten und Feldrechnertasten (von links nach rechts).
```

````{admonition} Optional: derive x and y coordinates with the Field Calculator
:class: dropdown

Fügen Sie im **Feldrechner** die Koordinaten $x$ und $y$ zur *Attributtabelle* hinzu:

* Kontrollieren Sie das Kontrollkästchen **Ein neues Feld erstellen**
* **Ausgabefeldname**: `x_coord`
* **Ausgabefeldtyp**: `Decimal number (real)`
* **Ausgabefeldlänge**: `10` und **Präzision**: `10`
* Geben Sie eine Formel ein, indem Sie entweder den x-Wert aus der Geometrie in der Scrollbox auswählen oder direkt in das Feld **Expression** eingeben:

```
 x( @geometry ) 
```

**In analoger Weise fügen Sie `y_coord` mit** hinzu:

```
 y( @geometry ) 
```

** Speichern Sie die Bearbeitungen in der *Attributtabelle*, indem Sie auf das Festplattensymbol klicken.

````

According to {cite:t}`meyer-peter_formulas_1948`, the {cite:t}`strickler_beitrage_1923` roughness (friction) coefficient can be approximated with $k_{st}$ $\approx$ 26/$D_{90}^{1/6}$ based on the grain size $D_{90}$, where 90% of the surface sediment grains are smaller. In addition, we will assume that $D_{90} \approx 2.25 \cdot D_{mean}$ {cite:p}`rickenmann_evaluation_2011`. Thus, $k_{st} \approx 26 \cdot (2.25 \cdot D_{mean})^{-1/6}$. To run this calculation, go to the **Field Calculator** and (see {numref}`Fig. %s <fric-pts-open-at>`):

* Kontrollieren Sie das Kontrollkästchen **Ein neues Feld erstellen**
* **Ausgabefeldname**: `k_st`
* **Ausgabefeldtyp**: `Decimal number (real)`
* **Ausgabefeldlänge**: `3` und **Präzision**: `2`
* Geben Sie eine Formel ein, indem Sie entweder `dMean` aus `Fields and Values` in der Scrollbox auswählen oder direkt die Gleichung in das Feld **Expression** eingeben:

```
26 / ( ( 2.25 * "dMean" ) ^ ( 1 / 6 ) )
```

```{figure} ../../img/telemac/fric-field-calc-strickler.png
:alt: calculator strickler roughness qgis field attribute table
:name: fric-field-calc-strickler

Schätzen Sie den Strickler-Koeffizienten basierend auf der mittleren Korngröße (dMean) mit dem Feldrechner in QGIS.
```



```{figure} ../../img/telemac/fric-at-final.png
:alt: x_coord y_coord coordinates strickler roughness qgis attribute table
:name: fric-at-final
:width: 100%
:align: left

Die finalisierte Attributtabelle der Friktion-pts-at-Schicht mit den optionalen x- und y-Koordinaten und den geschätzten Strickler-Rauheitskoeffizienten.
```

Schließlich entfernen Sie alle verbleibenden unnötigen Felder** aus der *Attributtabelle* und speichern Sie die Bearbeitungen, indem Sie auf das Festplattensymbol klicken und die Bearbeitung umschalten (d. H. Deaktivieren).

```{admonition} Download the friction-pts-at shapefile
:class: tip
Laden Sie die [zipped friction-pts shapefile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts-at.zip)] herunter und entpacken Sie sie in den Projektordner, zum Beispiel `/ProjectHome/friction-pts-at.[SHP]`.
```

### Exportpunkte nach XYZ

Beginnen Sie mit dem Öffnen des Export-Dialogs mit einem Rechtsklick auf die Friktion-pts-at-Schicht > Export > Funktionen speichern als ... ({numref}`Fig. %s <fric-pts-export-as>`).

```{figure} ../../img/telemac/fric-pts-export-as.png
:alt: export friction points xyz qgis attribute table
:name: fric-pts-export-as
:width: 100%

Öffnen Sie den Exportdialog mit einem Rechtsklick auf die Friction-pts-at-Schicht > Export > Features speichern als...
```

Führen Sie im **Vector Layer als...** Popup-Fenster die folgenden Einstellungen aus ({numref}`Fig. %s <fric-export-xyz>`):

* **Format**: `Comma Separated Value [CSV`
* **Dateiname**: Klicken Sie auf **...**, navigieren Sie zum Projektordner und geben Sie `friction-pts.xyz` für den Dateinamen ein (drücken Sie **Speichern**).
* **Layername**: klar halten
* **Koordinatenreferenzsystem**: Stellen Sie sicher, dass das Koordinatenreferenzsystem der Friction-pts-at-Schicht definiert ist (im Showcase `EPSG:32633 - WGS 84 / UTM zone 33N`)
* **Encoding**: standardmäßig verwenden (im Showcase `UTF-8`)
* **Wählen Sie alle relevanten **Felder ** aus, das heißt im Showcase mindestens `k_st`. Die optionalen Felder `x_coord` und `y_coord` sind nur erforderlich, wenn die Geometrie nicht exportiert wird (aus welchem Grund auch immer).
* **Überprüfen Sie die **Persist-Schicht Metadaten **
* **Geometrietyp**: `Automatic` (meist standardmäßig)
* **Scrollen Sie nach unten** zu den **Layer-Optionen** und:
  * Setzen Sie das **GEOMETRY** auf `AS_XY`
  * Setzen Sie den **SEPARATOR** auf `TAB`
* ** Deaktivieren Sie die **Gespeicherte Datei hinzufügen, um das Feld ** unten im Fenster abzubilden.
* ** Halten Sie alle anderen Standardeinstellungen** und klicken Sie auf **OK**.

```{figure} ../../img/telemac/fric-export-xyz.png
:alt: xyz file export attribute table friction points
:name: fric-export-xyz

Einstellungen im Speichern von Vektorschicht als... Popup-Fenster zum Exportieren der Friktionspunkte in eine XYZ-Datei (tab-separated CSV).
```

QGIS will have exported the file with a `.xyz.csv` ending. **Rename the file** to **remove `.csv`** at the end. **Verify the correct formatting of the `.xyz` file** by opening it in a {ref}`text editor (e.g., Notepad++) <npp>`. For instance, if you calculated and exported the `x_coord` and `y_coord` fields, and additionally the geometry, the `.xyz` file will hold two times the coordinates. In this case, import the `.xyz` file in a spreadsheet editor (i.e., {ref}`office application <lo>`), delete the `x_coord` and `y_coord` columns, and re-export the file as a tab-separated CSV file. Read more about `.xyz` file conversion in the {ref}`QGIS tutorial <make-xyz>`.

````{admonition} Expand to see the correct header of the showcase friction-pts.xyz file
:class: dropdown

```
X Y k_st  
315976.648906296  5345616.71281044  40.30
315992.808134594  5345521.13037269  40.30
315983.283370604  5345655.68430873  40.30
315915.433790676  5345754.82689794  40.30
[...]
```
````

```{admonition} Download the showcase friction-pts.xyz file
:class: tip
Download [`friction-pts.xyz`](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts.xyz) and save it into the project folder, for instance, `/ProjectHome/friction-pts.xyz`.
```

## Alternative: Friktionszonen in BlueKenue zeichnen

Dieses Verfahren ist eine ungenaue Alternative zu der oben beschriebenen `roughness.xyz`-Erstellung aufgrund der schwachen geospatialen Referenzierungskapazitäten von BlueKenue, weshalb das unten stehende {ref}`instruction box <bk-closed-fric-lines>` nur zur Vollständigkeit vorgesehen ist.

````{admonition} Unfold to read this non-recommended alternative
:class: note, dropdown
:name: bk-closed-fric-lines

Beginnen Sie mit dem Erstellen neuer geschlossener Linien ({numref}`Fig. %s <bk-new-closed-lines>`), ähnlich wie Polygone, die Rauheitszonen abgrenzen.

```{figure} ../../img/telemac/bk-new-closed-lines.png
:alt: bluekenue create closed line
:name: bk-new-closed-lines
:width: 50%
:align: left

Einstellungen im Speichern von Vektorschicht als... Popup-Fenster zum Exportieren der Friktionspunkte in eine XYZ-Datei (tab-separated CSV).
```

```{figure} ../../img/telemac/bk-finalize-friction-cl.png
:alt: bluekenue roughness friction closed line
:name: bk-finalize-friction-cl
:width: 100%
:align: right

Weisen Sie dem durch die geschlossene Linie abgegrenzten Bereich einen Reibwert (Rauheit) zu (hier: eine Strickler-Rauheit von 50).
```

After drawing a *Closed line* is finished, press the `Esc` key and the window shown in {numref}`Fig. %s <bk-finalize-friction-cl>` will appear, where a roughness value can be assigned. The exemplary figure assigns a Strickler roughness of `50` in the **Value** field to a *Closed line* named `A-D_substrate`. Continue to assign names to all relevant roughness areas.

Finally, **save** the *Closed line* objects as `.i2s` / `.i3s` files.
````


(bk-interpolate-fric-zones)=
# Zonal Friction Mesh (BlueKenue)

In diesem Abschnitt wird die Interpolation von Reibungswerten in einer vorhandenen Geometriedatei mit Selafin (`.slf`) durchlaufen. Das Schaufenster baut auf der `.slf`-Datei auf, die im {ref}`Telemac pre-processing tutorial <slf-prepro-tm>` erstellt wurde ([download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf)). Beginnen Sie mit ** Öffnen von BlueKenue ** und öffnen Sie die Datei selafin `.slf`: Klicken Sie auf **File ** > **Open...** > Navigieren Sie zu dem Verzeichnis, in dem der `.slf` gespeichert ist, wählen Sie **Telemac Selafin File (\*.slf) ** aus, markieren Sie `qgismesh.slf` und drücken Sie **Open **. Ziehen Sie die Ebene `BOTTOM (BOTTOM)` aus den Workspace-Datenelementen in **Views** > **2D View (1)**, um den korrekten Import des Meshs zu überprüfen und zu visualisieren ({numref}`Fig. %s <fric-bk-slf>`).


```{figure} ../../img/telemac/bk-slf.png
:alt: BlueKenue 2dmesh interpolated elevation
:name: fric-bk-slf

Die Datei qgismesh.slf selafin wurde in BlueKenue geöffnet.
```

(bk-import-friction)=
## Einfuhrfriktionszonen

Als Alternative zur Erstellung von zonalen Reibungswerten, die in einer mit QGIS generierten `.xyz`-Datei gespeichert sind, können Zonen auch direkt in BlueKenue durch eine Reihe von * Geschlossenen Linien * gezeichnet werden. Aufgrund der sehr begrenzten Kapazitäten von BlueKenue, um mit geospatialen Referenzen und Koordinatensystemen (CRSs) umzugehen, ist **die bevorzugte Option ** zum Erstellen von Reibungszoneneingaben ** die oben beschriebene Anwendung von **QGIS **.

`````{tab-set}
````{tab-item} Open the .xyz file in BlueKenue
To open the above-created `.xyz` file in BlueKenue:

* Klicken Sie auf **File** > **Open...**
* Navigieren Sie zum Projektordner, in dem `.xyz` gespeichert ist
* Wählen Sie **Alle Dateien (\*.\*)** neben dem Feld **Dateiname:** aus.
* highlight `qgismesh.slf`, and press **Open**.

```{figure} ../../img/telemac/bk-fric-xyz-properties.png
:alt: bluekenue roughness friction visualize coefficients
:name: bk-fric-xyz-properties
:width: 100%
:align: left

Weisen Sie dem durch die geschlossene Linie abgegrenzten Bereich einen Reibwert (Rauheit) zu (hier: eine Strickler-Rauheit von 50).
```

**Ignoriere** die **Warnung** Nachricht (klicke **OK**). Um die importierten Reibungswerte zu überprüfen und zu visualisieren **Rechtsklick** auf der ** Friction-pts (X)** Schicht > **Eigenschaften** > gehen Sie auf die Registerkarte **Daten** > ** Wählen Sie Z(double)**, drücken Sie **Apply**. Gehen Sie dann zur Registerkarte **ColourScale**, drücken Sie **Reset**, **Apply** und **OK**.

Überprüfen Sie die korrekte Darstellung der Reibungswerte, indem Sie die `friction-pts (Z)`-Schicht aus den Workspace-Datenelementen in **Views** > **2D View (1)** ({numref}`Fig. %s <bk-fric-pts>`) ziehen.


```{figure} ../../img/telemac/bk-fric-pts.png
:alt: friction roughness coefficients bluekenue 
:name: bk-fric-pts


Die importierte Friction-pts.xyz-Datei (erstellt mit QGIS) visualisiert in BlueKenue.
```
````

````{tab-item} Closed lines from BlueKenue
If not yet done, import the *Closed lines* delineating roughness zones in the form of `.i2s` / `.i3s` files.
````
`````

## Interpolationsreibung am Mesh

Gehen Sie in BlueKenue zu **File** > **New** > **2D Interpolator**, der im **Work Space** > **Data Items** auftritt. **Drag & drop** entweder die **friction-pts** `.xyz`-Punkte oder die *Closed line*-Objekte, die Rauheitszonen abgrenzen **auf dem neuen 2D Interpolator** (siehe {numref}`Fig. %s <bk-fric-2d-interpolator>`).

```{figure} ../../img/telemac/bk-fric-2d-interpolator.png
:alt: bluekenue 2d interpolator roughness friction
:name: bk-fric-2d-interpolator
:width: 100%


Ziehen Sie die Reibungspunkte (oder geschlossenen Linien) auf einem neuen 2D-Interpolator in BlueKenue.
```



Als nächstes fügen Sie eine neue Variable zum `qgismesh.slf`-Mesh hinzu, indem Sie das **Selafin `qgismesh`**-Objekt hervorheben (in **Work Space** > **Data Items**) und **Rechtsklick** darauf. Klicken Sie auf **Variable hinzufügen...** und geben Sie im Popup-Fenster Folgendes ein ({numref}`Fig. %s <bk-new-slf-variable-fric>` oder {numref}`Fig. %s <bk-new-slf-variable-fricID>`), je nachdem, ob Sie mit Reibungswerten arbeiten (wie hier mit Strickler-Rauheit dargestellt), oder {ref}`friction IDs (see below) <tm-fricID>`:

`````{tab-set}
````{tab-item} BOTTOM FRICTION (Strickler) value
```{figure} ../../img/telemac/bk-new-slf-variable-fric.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fric
:width: 100%
:align: right


Fügen Sie dem Selafin-Objekt eine neue Variable für direkte Reibungswerte hinzu.
```
* **Mesh**: `BOTTOM`
* **Name: `BOTTOM FRICTION` (dieses Beispiel)
* **Einheiten**: Freihalten (irrelevantes Feld)
* **Standard-Knotenwert**: `30` (in diesem Beispiel) für einen Standardwert (Strickler), der verwendet werden kann, wenn keine xyz-Reibungspunkte in der Nähe eines Mesh-Knotens gefunden werden können

````

````{tab-item} FRICTION ID
```{figure} ../../img/telemac/bk-new-slf-variable-fricID.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fricID
:width: 100%
:align: right


Fügen Sie eine neue Variable zum Selafin-Objekt für Reibungs-IDs hinzu.
```

* **Mesh**: `BOTTOM`
* **Name**: `FRIC_ID` (muss eingegeben werden, kann nicht aus der Liste ausgewählt werden)
* **Einheiten**: Freihalten (irrelevantes Feld)
* **Standard Node Value**: `0` (ID zu verwenden, wenn keine xyz-Punkte in der Nähe eines Mesh-Knotens gefunden werden können)

````
`````

To interpolate the friction values on the mesh, highlight the new variable variable `BOTTOM FRICTION` (or `FRIC_ID`) of the `qgismesh` object in **Work Space** > **Data Items**. The *Anonymous Attribute* of the new variable can be ignored. To map the new variable onto the mesh:

* Hervorheben der neuen `BOTTOM FRICTION` (oder `FRIC_ID`) Mesh-Variablen (in **Datenelemente**)
* Gehen Sie zu **Tools** > **Map Object...** (Top-Menü unter {numref}`Fig. %s <bk-map-2d-interpolator>`)
* Wählen Sie den **neuen 2D-Interpolator** und klicken Sie auf **OK**, wodurch das Popup-Fenster **Processing...** geöffnet wird.
* Nachdem die Verarbeitung abgeschlossen ist, klicken Sie auf **OK**.

```{figure} ../../img/telemac/bk-map-2d-interpolator.png
:alt: map object  2dinterpolator roughness friction bluekenue
:name: bk-map-2d-interpolator
:width: 100%

Karte den Reibungswert auf dem neuen 2D Interpolator in BlueKenue.
```

```{figure} ../../img/telemac/bk-fric-colourscale.png
:alt: bottom friction colourscale selafin bluekenue
:name: bk-fric-colourscale
:width: 100%
:align: right

Passen Sie die Farbskala für Bottom Frederick an.
```

Überprüfen Sie die korrekte Interpolation:

* Definieren Sie eine relevante Farbskala:
  * In **Work Space** > **Data Items** > **qgismesh**, **right-click** auf die neue **BOTTOM FRICTION** Variable > **Eigenschaften**.
  * In the properties, go to the **ColourScale** tab, and use, for example, a *Linear* scale with `10` *Levels*, a *Min* of `22`, and an *Interval* of `1.8`. The exemplary minima and interval are good choices for the showcase, but other settings might be preferable for other applications (e.g., prefer *Min* of `0` when using Manning's $n_m$).
  * Drücken Sie **Apply** > **OK**.
* **Drag & drop** die Variable **BOTTOM FRICTION** in **Views** > **2D View (1)**, um die korrekte Interpolation der Reibungswerte zu überprüfen (z.B. siehe {numref}`Fig. %s <bk-fric-on-mesh>` für das Schaufenster).

```{figure} ../../img/telemac/bk-fric-on-mesh.png
:alt: selfin slf mesh bottom friction bluekenue
:name: bk-fric-on-mesh

Die korrekt interpolierte neue BOTTOM FRICTION-Variable des qgismesh.slf-Meshs.
```

Um den Selafin **mesh ** mit interpolierten interpolierten Reibungswerten zu speichern ** Rechtsklick ** auf das **qgismesh-Selafin-Objekt ** > **Eigenschaften** > gehen Sie auf die Registerkarte **Meta-Daten** und geben Sie einen neuen **Name** ein, z. B. `qgismesh-friction`. Als nächstes markieren Sie das Selafin-Objekt** (z.B. `qgismesh-friction`) und **klicken Sie auf das Symbol <img src="../../img/telemac/bk-sym-save.png">**. Wenn die Umbenennung für den Dateinamen nicht wirksam wurde, bestätigen Sie das Ersetzen der vorhandenen Datei.


```{admonition} Download qgismesh-friction.slf (with BOTTOM FRICTION)
:class: tip
Laden Sie die aktualisierte [qgismesh-friction.slf mit BOTTOM FRICTION](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf) herunter.
```


# Telemac-Bindungen

(zonal-fric-cas)=
## Umsetzung in der CAS-Datei

### Friction Keywords

The updated `qgismesh-friction.slf` mesh can be used just like in the {ref}`steady 2d tutorial <telemac2d-steady>`, but some keywords need to be modified, even though the `BOTTOM FRICTION` values assigned in the `.slf` mesh automatically overwrite the global **FRICTION COEFFICIENT** keyword in the `.cas` steering file. However, we need to make Telemac recognize the newly defined `BOTTOM FRICTION` zones as **Strickler** roughness type. To this end, change the **LAW OF BOTTOM FRICTION** to `3` (instead of `4` pointing to Manning's $n_m$), and set the default **FRICTION COEFFICIENT** to `33` (inverse of $n_m$ = 0.03). The definition of the **FRICTION COEFFICIENT** is for coherence and is not strictly needed as it will be overwritten by the `BOTTOM FRICTION` from the `.slf` mesh.

`````{tab-set}
````{tab-item} New (Strickler)
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ Friction at the bed
LAW OF BOTTOM FRICTION : 3 / 3-Strickler
FRICTION COEFFICIENT : 33  / will be overwritten by zonal friction values
```
````

````{tab-item} Old (Manning from steady 2d)
```fortran
/ steady2d.cas steering file
/ ...
/ Friction at the bed
LAW OF BOTTOM FRICTION : 4  / 4-Manning
FRICTION COEFFICIENT : 0.03 / Roughness coefficient
```
````
`````

Add the letter `W` to the graphic printouts for writing the friction coefficient to the results file:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : 'U,V,H,S,Q,W' / add W for friction coefficient
```


````{admonition} Do you have more than 10 different friction zones?
:class: tip, dropdown

Um die Anzahl der von Telemac erkannten Reibungszonen zu erhöhen, setzen Sie das Schlüsselwort **MAXIMUM NUMBER OF FRICTION DOMAINS**, zum Beispiel auf `20`:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
MAXIMUM NUMBER OF FRICTION DOMAINS : 20 / default is 10
```
````


### Startbedingungen (fakultativ)

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 4.1.3 im [Telemac2d Manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**]

To speed up the simulation, this tutorial re-uses the output of the {ref}`steady 2d simulation <telemac2d-steady>` (though, re-created with a printout period of `2500` steps). This type of model initialization is also called *hotstart*, here, based on the steady results file [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf), which needs to be defined as **PREVIOUS COMPUTATION FILE**:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady-t15k.slf / results of 35 CMS steady simulation after 15000 timesteps
```

Mit den Hotstart-Bedingungen können die Grenzen erleichtert werden:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ Liquid boundaries
PRESCRIBED FLOWRATES  : 35.; 0.
PRESCRIBED ELEVATIONS : 0.; 371.33
```

Damit diese Randbedingungen wirksam werden können, muss die Datei mit flüssigen Grenzen aus der stetigen 2D-Simulation geändert werden:

* open *boundaries.cli* in einem {ref}`text editor <npp>`
* find the `5 5 5` (prescribed Q and H) upstream boundary and replace it with `4 5 5` (prescribed Q only)
* speichern und schließen *boundaries.cli*
* for more information, have a look at the spotlight chapter on {ref}`boundary conditions <tm-foc-bc>`
* alternativ [download der angepassten borders.cli here](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli)].

Finally, comment out any initial conditions keywords in the `.cas` steering file, for instance:


```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ INITIAL CONDITIONS : 'ZERO DEPTH'
/ INITIAL DEPTH : 0.005
```

## Run Friction Zone Simulation

Make sure all required files are placed in a simulation folder (e.g., `/HOME/modeling/friction-tutorial/`), notably:

* die [qgismesh-friction.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf) mesh mit `BOTTOM` und `BOTTOM FRICTION` Informationen]
* korrigiert [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli)]
* die [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf) Results-Datei, um den Hotstart zu aktivieren]
* die [steady2d-zonal-ks.cas](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas) Steering-Datei mit aktualisierten Schlüsselwörtern].

Navigate (`cd`) to the Telemac installation directory (`HOMETEL`) to activate (`source`) the Telemac environment in Terminal (use the same environment as for {ref}`compiling Telemac <tm-compile>`):

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
```

Als nächstes `cd` in den Simulationsordner und führen Sie die Simulation, möglicherweise mit dem `-s` Flag, um {ref}`flux convergence <tm-convergence>` zurückzuverfolgen:

```
cd ~/modeling/friction-tutorial/
telemac2d.py steady2d-zonal-ks.cas -s
```

Der erfolgreiche Simulationslauf wird mit so etwas beendet sein:

````{admonition} Unfold to see the expected Terminal output
:class: note, dropdown

```
================================================================================
 ITERATION    10000    TIME:  6 H 56 MIN  40.0000 S   (    25000.0000 S)
--------------------------------------------------------------------------------

[...]

--------------------------------------------------------------------------------
                       BALANCE OF WATER VOLUME
     VOLUME IN THE DOMAIN :    268926.5     M3
     FLUX BOUNDARY    1:     35.00000     M3/S  ( >0 : ENTERING  <0 : EXITING )
     FLUX BOUNDARY    2:    -34.99963     M3/S  ( >0 : ENTERING  <0 : EXITING )
     RELATIVE ERROR IN VOLUME AT T =       0.2500E+05 S :    0.2327571E-14
--------------------------------------------------------------------------------
                   FINAL BALANCE OF WATER VOLUME

     RELATIVE ERROR CUMULATED ON VOLUME:    0.4112446E-14

     INITIAL VOLUME              :     268899.0     M3
     FINAL VOLUME                :     268926.5     M3
     VOLUME THAT ENTERED THE DOMAIN:     27.48362     M3  ( IF <0 EXIT )
     TOTAL VOLUME LOST             :    0.1105946E-08 M3

 END OF TIME LOOP

 EXITING MPI

                     *************************************
                     *    END OF MEMORY ORGANIZATION:    *
                     *************************************

 CORRECT END OF RUN

 ELAPSE TIME :
                              3  MINUTES
                              3  SECONDS
Note: The following floating-point exceptions are signalling: IEEE_UNDERFLOW_FLAG IEEE_DENORMAL
STOP 0

... merging separated result files

... handling result files

        moving: r2dsteady-ks-zonal.slf
      copying: steady2d-zonal-ks.cas_2030-07-28-14h55min04s.sortie
... deleting working dir



My work is done

```
````

Die resultierenden {ref}`flux convergence <tm-flux-convergence>` und {ref}`convergence rates <tm-calculate-convergence>` sollten ähnlich aussehen:

`````{tab-set}
````{tab-item} Flux convergence
```{figure} ../../img/telemac/flux-convergence-zonal-fric.png
:alt: zonal friction telemac flux convergence pythomac
:name: tm-friction-flux-convergence

Flusskonvergenzkurve über die beiden Grenzen der stationären Telemac2d-Simulation mit Warmstart, beginnend bei einer Simulationszeit von 15000 Zeitschritten.
```
````

````{tab-item} Convergence rate
```{figure} ../../img/telemac/convergence-rate-zonal-fric.png
:alt: zonal friction convergence rate fluxes telemac boundaries
:name: tm-friction-convergence-rate

The convergence rate $\iota$ as a function 15000 simulation timesteps of the hotstarted steady 2d simulation with friction zones.
```
````
`````

Die erforderliche [steady2d-zonal-ks.cas 2023-07-28-14h55min04s ist hier verfügbar](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas_2023-07-28-14h55min04s) für die Verwendung mit Anweisungen aus dem Spotlight-Kapitel unter {ref}`convergence <tm-convergence>`.

```{admonition} Look at the results in QGIS

Laden Sie die Simulationsergebnisdatei (`r2dsteady-ks-zonal.slf`) in QGIS, um die Richtigkeit der verwendeten Bodenreibung zu überprüfen, und betrachten Sie die geringfügigen Änderungen der Strömungsgeschwindigkeit und Wassertiefe, die sich aus den jetzt unterschiedlichen Rauheitswerten ergeben.
```

(tm-fricID)=
# Arbeiten mit Friction IDs

Die Reibungszonen können auch über Reibungs-IDs zugewiesen werden, die dann die Einrichtung einer Zonendatei und einer Reibungsdatendatei erfordern, wie im Donau-Beispiel (`HOMETEL/examples/telemac2d/donau/`) dargestellt.

```{admonition} The Donau zonal friction ID example
:class: tip

The BAW's Donau case study lives in `HOMETEL/examples/telemac2d/donau/` and it was presented at the XXth Telemac-Mascaret user conference. The conference proceedings are available at the BAW's [HENRY portal](https://hdl.handle.net/20.500.11970/100418) (look for the contribution *Reverse engineering of initial & boundary conditions with Telemac and algorithmic differentiation*). However, this case uses an unnecessary complication in the form of a `.bfr` zone file. The geospatial reference system of this example is EPSG 31468 (GK4) (see [this post in the Telemac Forum](http://opentelemac.org/index.php/kunena/16-telemac-2d/14284-coordinate-reference-systems-and-projections-of-examples-e-g-donau#43037)).
```

In the showcase of this tutorial, working with friction tables required assigning the friction IDs defined in {numref}`Tab. %s <tab-tm-fricID-zones>` to the `BOTTOM FRICTION` variable of the `.slf` mesh. The according files can be downloaded from our repositories:

* [Holen Sie sich Friction-with-IDs.xyz](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction-with-IDs.xyz) für Interpolation in BlueKenue ({ref}`see above <bk-interpolate-fric-zones>`) oder direkt
* [get qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) with `BOTTOM` and `FRIC_ID` instead of `BOTTOM FRICTION` Strickler roughness coefficients (uses default friction ID `0`).

## Reibung.tbl & CAS

### Erstellen von friction.tbl

Erstellen Sie eine Friktionstabellendatei mit dem Namen `friction.tbl` (beachten Sie diese [friction.tbl template](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl)]] mit folgendem Inhalt, wobei die `no`-Einträge (hier beginnend in Zeile 36) dem `FRIC_ID` entsprechen müssen, der dem Mesh zugewiesen ist (erinnern Sie sich an {numref}`Fig. %s <bk-new-slf-variable-fricID>`):

```{aside} More information

Anhang E des [Telemac2d Manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) bietet weitere Erklärungen zu den tabellarischen Parametern (z. B. `typeB`, `rB` oder `nDefB`), und die Reibungsgesetze (z. B. STRI, NIKU) werden in diesem eBook im steady-2d {ref}`section on friction <tm2d-friction>` ausführlicher erläutert.
```

```{code-block} fortran
---
name: friction_tbl
linenos: True
caption: |
    Example for a friction(.tbl) ID table.
---
* ----------------------------------------------------------------------------- 
*  EXAMPLE ADAPTED FROM HOMETEL/examples/telemac2d/donau/
*
*  Implemented roughness laws: 
*    NOFR : no friction         (number of values) 
*    HAAL : Haaland   law       (1 value  : rB) 
*    CHEZ : Chezy     law       (1 value  : rB) 
*    STRI : Strickler law       (1 value  : rB) 
*    MANN : Manning   law       (1 value  : rB) 
*    NIKU : Nikuradse law       (1 value  : rB) 
*    LOGW : Log Wall  law       (1 value  : rB) 
*    COWH : Colebrook-White law (2 values : rB, nDef) 
* 
*  no             : FRIC_ID assigned to the SLF mesh
* 
*  Riverbed
*  ------------- 
*  typeB          : roughness law for riverbed
*  rB             : friction value for riverbed
*  nDefB          : Mannings n for shallow flow zones
* 
*  Later walls (only with k-epsilon model) 
*  ----------------------------------------- 
*  typeS          : roughness law for walls          (option) 
*  rS             : friction value for walls         (option) 
*  nDefS          : Mannings n for shallow waters    (option) 
* 
*  Non-submerged Vegetation (if needed) 
*  ------------------------ 
*  dp             : mean diameter                                (option) 
*  sp             : averaged distance between roughness elements (option) 
* 
* ----------------------------------------------------------------------------- 
* no        typeB  rB    NDefB  typeS  rS  NDefS   dp     sp 
* 
  0  STRI   33.0  NULL
  1  STRI   34.6  NULL
  2  STRI   27.7  NULL
  3  STRI   40.3  NULL
  4  STRI   22.7  NULL
END 
```

### Link friction.tbl in der CAS-Datei

To activate the friction data, add the following keywords to the `.cas` steering file, and deactivate any not-wall related FRICTION keywords:


`````{tab-set}
````{tab-item} Keywords to activate
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ ACTIVATE these keywords
FRICTION DATA : YES / default is NO
FRICTION DATA FILE : 'friction.tbl'
MAXIMUM NUMBER OF FRICTION DOMAINS : 20 / consider to increase (default is 10)
```
````
````{tab-item} Keywords to deactivate
```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ DEACTIVATE these keywords
/ LAW OF BOTTOM FRICTION : 3 / 3-Strickler
/ FRICTION COEFFICIENT : 80 / not use with zonal friction
```
````
`````

Save the `.cas` steering file.

## Ausführen von Telemac mit Friction IDs

To run Telemac with friction IDs, make sure the above-indicated keywords are activated in the `.cas` steering file. The required files now embrace:

* [qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) (mesh mit `FRIC_ID`)]
* [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/boundaries.cli) oder Hotstartbedingungen]
* [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/r2dsteady-t15k.slf)Ergebnisdatei zum Aktivieren des Hotstarts]
* [steady2d-zonal-ID.cas](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/steady2d-zonal-ID.cas) Steering-Datei aktualisierte Keywords]
* [friction.tbl](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl) mit Reibungs-IDs]

Aktivieren und Ausführen von Telemac mit diesen Dateien wie gewohnt:

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
cd ~/modeling/frictionID-tutorial/
telemac2d.py steady2d-zonal-ID.cas
```


# Erweiterte Friktionsroutinen

Modifying the **FRICTION_USER** Fortran subroutines is not mandatory for working with friction zones but can be useful for implementing or adapting the behavior of roughness laws. To activate a FRICTION_USER subroutine, for example, to implement the variable power equation from {cite:t}`ferguson_flow_2007`:

* Kopieren Sie die Subroutinevorlage FICTION USER von `HOMETEL/sources/telemac2d/friction_user.f` in einen neuen Ordner Ihres Simulationsverzeichnisses, zum Beispiel:
```
/HOME/modeling/frictionID-tutorial/user_fortran/friction_user.f
```
* Modify and save edits of `friction_user.f`.
* Sagen Sie der Steuerungsdatei (`.cas`), die modifizierte FRICTION USER Fortran-Datei zu verwenden, indem Sie das Schlüsselwort `FORTRAN FILE : 'user_fortran'` hinzufügen, wodurch Telemac2d Fortran-Dateien im `/user_fortran/`-Unterordner nachschlagen lässt.






