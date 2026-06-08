---
description: Definieren Sie räumlich verteilte Reibungs- und Rauheitszonen in TELEMAC2d unter Verwendung von QGIS und BlueKenue, wobei Manning- oder Strickler-Koeffizienten verschiedenen Flussbettmaterialtypen zugeordnet werden.
---

```{admonition} Contributors
:class: tip
This chapter was co-written and developed by [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/) <img src="../../img/authors/federica.jpg" alt="Federica Scolari" width="25" height="25"> and [Sebastian Schwindt](https://sebastian-schwindt.org) <img src="../../img/authors/sebastian.jpg" alt="Sebastian Schwindt" width="25" height="25">.
```

(tm-friction-zones)=
# Friktion (Roughness) Zonen

Ähnlich wie bei der Zuordnung mehrerer Reibungskoeffizienten zu mehreren Modellregionen, die in der {ref}`BASEMENT tutorial <bm-geometry>` enthalten sind, bietet Telemac2d Routinen für Domänen (d.h. zonale) Reibflächendefinitionen in der Geometrie (`.slf`) mesh-Datei. Insbesondere, wenn der Studienbereich durch Bereiche unterschiedlicher Rauheit gekennzeichnet ist, reicht es nicht aus, die globale Reibung durch ein `FRICTION COEFFICIENT` Schlüsselwort in der Lenkungsdatei (`.cas`) zu definieren. Die Definition von Rauheitszonen in der Mesh-Datei (`.slf`) erfordert eine zusätzliche Schicht unter dem Namen `BOTTOM FRICTION` oder `FRIC_ID` oben auf der`BOTTOM`-Höhe. Zu diesem Zweck können Rauhigkeitswerte in einer mit QGIS ({ref}`recommended <tm-friction-qgis>`) erstellten Rauhigkeitsdatei `.xyz` oder *Closed Lines* `.i2s` erstellt mit BlueKenue ({ref}`see the meshing section <bk-import-friction>`) definiert werden. Während QGIS empfohlen wird, die Rauhigkeitszonen mit korrekten und möglicherweise präzisen Georeferenzen abzugrenzen, ist BlueKenue für die Interpolation der Rauhigkeit aus der Datei `.xyz` oder `.i2s` in der Datei `.slf` im letzten Schritt erforderlich.


```{admonition} Requirements

* Geospatiale Datenformate verstehen und wissen, mit QGIS zu arbeiten (siehe {ref}`QGIS tutorial <qgis-tutorial>`).
* Füllen Sie die {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>`.
* Installation von {ref}`BlueKenue (also works on Linux, see the installation guide) <bluekenue>` und {ref}`Telemac <telemac-install>`.
```

```{admonition} Roughness versus friction

Roughness beschreibt die Unebenheiten oder die Robustheit fester Oberflächen, wie Flussbetten. Die Überschwemmung erhöht die Fließfestigkeit, was zu Reibung und Verlangsamung der Wasserbewegung führt.
```


(tm-friction-qgis)=
## Roughness.XYZ mit QGIS (empfohlen)

Der erste Schritt zur Delineierung von Rauheitszonen in QGIS ist die Einrichtung des Koordinatenreferenzsystems und die Speicherung des Projekts analog zu den {ref}`QGIS pre-processing tutorial <tm-qgis-prepro>`:

* Öffnen Sie QGIS und im oberen Menü gehen Sie zu **Projekt******Properties**.
* Aktivieren Sie die Registerkarte **Koordinatenreferenzsystem***.
* Stellen Sie den Koordinatenreferenzsystem fest, dass Ihre {ref}`basemap <basemap>` /{term}`DEM`-Datennutzung; Geben Sie hierzu z.B. `UTM zone 33N` ein und wählen Sie *UTM-Zone 33N (WGS84)* (EPSG 32633), die aufgrund seiner geringen Präzision keine große Wahl ist, aber es wird den Job für dieses Tutorial tun.
* Klicken Sie auf **Apply* und **OK**.
* Speichern Sie das Projekt in einen neuen Ordner, in dem alle Dateien für dieses Tutorial gespeichert werden.

Es wird wichtig sein, Überschneidungen zu vermeiden, die zu mehrdeutigen oder fehlenden Definitionen von Regionen führen würden. Aktivieren Sie daher Snapping:

* Activate the *Snapping Toolbar*: **View** > **Toolbars** > **Snapping Toolbar**
* In the **Snapping toolbar** > **Enable Snapping** <img src="../../img/qgis/snapping-horseshoe.png">
* Enable snapping for
  * **Vertex**, **Segment**, and **Middle of Segments** <img src="../../img/qgis/snapping-vertex-segments.png">.
  * **Snapping on Intersections** <img src="../../img/qgis/snapping-intersection.png">.
  * **Self Snapping** <img src="../../img/qgis/sym-self-snapping.png">.

Dieses Tutorial nimmt das Beispiel von der {ref}`Telemac QGIS pre-processing tutorial <slf-prepro-tm>` an, um Polygone entlang der [breaklines](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) und [liquid-boundaries](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) formfiles. Die Reibungszonen werden von einem {ref}`Google Satellite basemap <basemap>` abgeleitet und Reibungsattribute werden qualitativ geschätzt, was für ein Tutorial gut ist. In der Praxis empfehlen wir dringend, Felderhebungen über Korngrößenverteilungen mit hochpräzisen Differential GPS (DGPS)-Systemen durchzuführen, um Rauheitszonen vor Ort, unterstützt durch Drohnenbilder, abzugrenzen.

```{admonition} AI can be more efficient (though less effective)
:class: tip
:name: ai-image-recognition-numerics

Dieses Tutorial zeigt, wie man manuell Polygone zeichnen kann, die bestimmte Rauheitszonen wie *sand*, *gravel* oder *vegetation* beschreiben. Künstliche Intelligenz (KI) hat sich jedoch bereits bewährt, bei der automatischen Erkennung ähnlicher Gelände-Patches für die konsequente Erkennung von Rauheitszonen einen großen Job zu leisten. Beispiele finden Sie unter {cite:t}`diazgomez_mapping_2022` oder [Kenny Larrieu's Implementierung von Segment Everything EO tools](https://github.com/klarrieu/segment-anything-eo).

Was Sie brauchen ist:

* eine moderne Drohne (nicht mehr zu teuer)
* Bodenwahrheit: Daten über Korngrößenverteilungen (> Kies: Kieszählungen, Sand zu Kies: Sack & Sieb, sehr feines Sediment: Gefrierkern/Platte & Sieb), Objekt-Etiketten (d.h., DGPS Punkte Markierung *vegetation/Typen*, *Holz*, *verstärkte Banken*, *Straßen*, etc.)
* ein Algorithmus, der jedes Drohnenbild klassifiziert, nachdem wir auf der Grundwahrnehmung trainiert wurden; wir arbeiten derzeit daran und stellen es hier vor - bleiben Sie dran.
```

### Delineate Roughness Zone Polygone

Die Rauheitszonen können durch Attribute einer Polygonformdatei beschrieben werden. Um eine neue Polygon-Formdatei zu erstellen, gehen Sie zu **Layer******Create Layer*******Neue Shapefile Layer...** (siehe {numref}`Fig. %s <new-qgis-lyr-rough>`).

```{figure} ../../img/telemac/qgis-add-lyr.png
:alt: create polygon shapefile roughness zones telemac
:name: new-qgis-lyr-rough

Erstellen Sie eine neue Polygon-Formdatei.
```

Geben Sie im Popup-Fenster die folgenden Definitionen ein:

***Dateiname**: drücken Sie auf **...*, navigieren Sie in den Projektordner und tippen Sie auf `friction-polygons`.
* **File encoding*: Standard halten (Beispieldateien verwenden `UTF-8`).
**Geometrie Typ**: `Polygon`
* Unterhalb der *Zusätzliche Dimensionen* (nicht erforderlich), finden und klicken Sie auf die **Koordinatenreferenzsystem*-Taste, um das oben definierte Projektkoordinatensystem auszuwählen (Beispieldateien: `EPSG:32633`).
**Neues Feld** hinzufügen:
**Name***: `dMean`
**Typ**: `Decimal (double)`
**Length***: `10`
**Präzision***: `5`
* Klicken Sie auf **Zu Feldliste hinzufügen*
* Fügen Sie ein weiteres **Neues Feld** hinzu:
**Name***: `fricID`
**Typ**: `Integer (32 bit)`
**Length***: `5`
* Klicken Sie auf **Zu Feldliste hinzufügen*
* Drücken Sie **OK**, um die neue Formdatei zu erstellen.

Um diesem Tutorial zu folgen, importieren Sie die [Frühzeilen (download als zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/breaklines.zip) und [Liquid-boundaries (download als zip-file)](https://github.com/hydro-informatics/telemac/raw/main/shapefiles/liquid-boundaries.zip) formfiles aus der Telemac-Vorverarbeitung. Polygone zu zeichnen, indem Fiktion-Polygone bearbeitet werden. schmeicheln Sie entlang der Brechlinien und Flüssigkeitsgrenzen, markieren Sie **fiction-polygons** im *Layers*-Panel und ermöglichen Sie die Bearbeitung, indem Sie auf den gelben Stift <img src="../../img/qgis/yellow-pen.png"> klicken. Aktivieren **Add Polygon Feature** und zeichnen Polygone durch Schnappen auf Punkte der *Frühlinien* und *Flüssiggrenzen* Schichten, laut {numref}`Fig. %s <tm-fricID-polygons>`. Um ** jedes Polygon** mit einem ** Rechtsklick auf die Maus* und **enter** die `fricID` und `dMean`-Werte nach {numref}`Tab. %s <tab-tm-fricID-zones>` (qualitative Korngrößen) zu definieren.

Zu **richtige Zeichnungsfehler** verwenden Sie das **Vertex Tool**<img src="../../img/qgis/sym-vertex-tool.png">. Speichern Sie schließlich die neuen Polygone (Eigenschaften von **friction-zones.shp**), indem Sie auf das **Save Layer Edits**<img src="../../img/qgis/sym-save-edits.png">symbol klicken. **Stop (Toggle) Editing** durch erneutes Klicken auf den gelben Stift <img src="../../img/qgis/yellow-pen.png"> Symbol.

**Alternativ fügen Sie die Bruchlinien und Flüssigkeitsgrenzen zusammen und verwenden Sie das *Polygonize* Werkzeug aus der *Processing Toolbox*, um die zusammengeführten Linien in eine Polygon-Formdatei umzuwandeln.** Die Polygonisierung wird jedoch einige Bruchlinien vermissen, die eine Bearbeitung erfordern. Auch die Felder `fricID` und `dMean` müssen noch durch Bearbeitung hinzugefügt werden.

```{figure} ../../img/telemac/fricId-zones-overview.jpeg
:alt: qgis telemac roughness zone polygons
:name: tm-fricID-polygons

Beispiel zur Beschreibung von Rauhigkeitszonen mit Polygonen durch vier Reibungs-IDs (fricID), die (1) das Flussbett, (2) Blockrampen, (3), Kiesstangen und (4) Flutplains abgrenzen. Hintergrundkarte: {cite:t}`googlesat`satellitenbild.
```

```{list-table} Four exemplary friction zones described by integer fricIDs and mean grain size diameters dMean.
:header-rows: 1
:name: tab-tm-fricID-zones

* - Zonenname
- Flussbett
- Blockrampen
- Kieselbanken
- Floodplains
* - fricID
- 1
- 2
- 3
- 4
* - dMean (m)
- 0,080
- 0,300
- 0,032
- 1.000
```

```{admonition} Download the friction-polygons shapefile
:class: tip
Laden Sie das [Reib-Polygons formfile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-polygons.zip) herunter und entpacken Sie es in den Projektordner, z.B. `/ProjectHome/friction-polygons.[SHP]`.
```

### Roughness Points generieren

Der nächste Schritt auf dem Weg zur Erstellung der erforderlichen XYZ-Datei zur Zuordnung von Reibungszonen zu einer selafinen Geometriedatei ist es, (random) Punkte innerhalb der oben erstellten Polygone zu erzeugen. Zu diesem Zweck **enter`random points inside polygons`** im **search**-Feld der **Processing Toolbox**. Geben Sie im **Random Points Inside Polygons** Popup-Fenster ({numref}`Fig. %s <tm-fric-polygons2pts>`) Folgendes ein:

**Eingangsschicht**: `friction-polygons`
**Sampling-Strategie**: `Points density`
* **Punktzahl oder -dichte*: `0.25` - Verwenden Sie einen kleineren/größeren Wert für Fein-/Koarse-Netze, aber beachten Sie möglicherweise sehr große Dateigrößen
* **Minimum-Distanz zwischen Punkten*: `5.0` - Verwenden Sie einen kleineren/größeren Wert für Fein-/Koarnetze
***Random-Punkte**: Klicken Sie auf **...* und definieren Sie einen Zielpunkt-Formdateinamen, wie z.B. `friction-pts.shp`, um im Projektordner gespeichert zu werden.
* Klicken Sie ****, um die Punkte formfile zu erstellen. Dieser Vorgang kann je nach definierter Punktdichte eine Weile dauern.

Die resultierende Punktformdatei wird in {numref}`Fig. %s <tm-fric-pts>` angezeigt.

```{figure} ../../img/telemac/fric-zones-pts.png
:alt: random points polygons qgis telemac roughness zone
:name: tm-fric-polygons2pts

Einstellungen im Random Points Inside Polygons-Tool in QGIS. Wählen Sie vorsichtig die Punktzahl oder -dichte aus, die sehr große Ausgangsdateien verursachen kann. Das Mindestabstandsfeld kann verwendet werden, um die Anzahl der Punkte zu reduzieren.
```

```{figure} ../../img/telemac/fric-pts.jpg
:alt: random points roughness zone
:name: tm-fric-pts

Die Punktformdatei, die sich aus der Verwendung des Random Points Inside Polygons-Tools in QGIS ergibt. Hintergrundkarte: {cite:t}`googlesat`satellitenbild.
```

```{admonition} Download the friction-pts shapefile
:class: tip
Laden Sie die [zipped Friktions-pts formfile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts.zip) herunter und entpacken Sie sie in den Projektordner, z.B. `/ProjectHome/friction-pts.[SHP]`.
```


### Friction Attributes to Points zuweisen

Leider nimmt die Punktgenerierung nicht automatisch die Polygon-Attribute auf, die zu den Punkten interpoliert werden müssen. Je nach dem angestrebten Rauheitsgesetz für den Einsatz mit Telemac können entweder die Friktions-IDs oder direkt Rauheitskoeffizienten der Attributtabelle der Friktionspunktformdatei hinzugefügt werden. In diesem Tutorial wird ein Reibungskoeffizient in Form der Stricklerrauhigkeit interpoliert und mit einer empirischen Formel berechnet. Ein komplexerer Fall zur Berechnung von Rauheitswerten ist in der Fallstudie des BAW (*Danube*) zu finden (in `HOMETEL/examples/telemac2d/donau/`).

Die Übertragung der `dMean` und/oder `fricID`-Attribute der Polygone an die Punkte ist im Wesentlichen eine Interpolation Operation, in der QGIS jeden Punkt betrachtet und ihm die `dMean` und/oder `fricID`-Attribute des nächsten Polygons zuordnet. Zu diesem Zweck klicken Sie auf das **Vector* Top-Menü > **Data Management Tools*********Join Attributes by Location** (siehe {numref}`Fig. %s <fric-data-mgmt-join-attributes>`).


```{figure} ../../img/telemac/fric-data-mgmt-join-attributes.png
:alt: qgis friction points attribute table
:name: fric-data-mgmt-join-attributes


Öffnen Sie die Attribute Join by Location Tool in QGIS.
```


```{figure} ../../img/telemac/fric-join-attributes-by-location.png
:alt: qgis friction join attributes by location
:name: fric-join-attributes-by-location
:width: 75%
:align: right

Öffnen Sie die Attributtabelle der Friktionspunkttabelle.
```

Im *Join Attributes by Location* Popup-Fenster ({numref}`Fig. %s <fric-join-attributes-by-location>`) stellen Sie folgende Einstellungen vor:

* * **Zur Ausstattung*: `friction-pts`
* **Features they (geometrisches Prädikat)*: Überprüfen Sie das Feld `are within`, wählen Sie alle anderen
* **Verglichen mit**: `friction-polygons`
* **Fields to add*: Klicken Sie auf die **...* Schaltfläche, um `fricID` und/oder `dMean` zu wählen
**Join type***: `Take attributes of the first matching feature only (one-to-one)`
**Joined Layer**: Klicken Sie auf den **...* Button > **Save to file** > navigieren Sie in den **Projektordner***** einen Dateinamen, z.B. `friction-pts-at`**
* Klicken Sie auf **Run**.

Die Fehlermeldung *Für die Eingabeschicht existiert kein räumlicher Index, die Leistung wird stark abgebaut* kann für diese Anwendung ignoriert werden. Dennoch, um jede falsche Ausgabe zu überprüfen, könnte es klug sein, auch die Schicht zu definieren **Unjoinable Features von der ersten Schicht**.

Das **friction-pts-at** ist somit im **Layers* Panel erhältlich (siehe {numref}`Fig. %s <fric-pts-open-at>`).

Um die mittleren Korngrößen (`dMean`) in Reibwerte umzuwandeln, öffnen Sie die *Attribute Tabelle* von **right-clicking* auf der **friction-pts-at**-Schicht im **Layers**-Panel > **Open Attributtabelle**.

```{figure} ../../img/telemac/fric-pts-open-at.jpg
:alt: qgis friction points attribute table
:name: fric-pts-open-at


Öffnen Sie die Attributtabelle der Friktionspunkt Shapefile mit Attributtabelle. Hintergrundkarte: {cite:t}`googlesat`satellitenbild.
```


**Beitragstabelle* ({numref}`Fig. %s <fric-pts-at-edit>`):

1. Bearbeiten aktivieren,
1. entfernen Sie unnötige Spalten, wie das Feld `id`, und möglicherweise auch das Feld `fricID` (diese Schaufenster wird nur die Spalte `dMean` verwenden),
1. Öffnen Sie den **Field-Rechner**, den wir im nächsten Schritt verwenden, um Strickler-Rohigkeitswerte abzuleiten.


```{figure} ../../img/telemac/fric-pts-at-edit.png
:alt: friction points edit attribute table
:name: fric-pts-at-edit

Die Attributtabelle der Friktions-pts-at-Schicht mit den hervorgehobenen (roten Rechtecken) Bearbeitung, Spalten entfernen und Feldrechnertasten (von links nach rechts).
```

````{admonition} Optional: derive x and y coordinates with the Field Calculator
:class: dropdown

Im **Field Calculator** fügen Sie die $x$ und $y$-Koordinaten an die *Attribute Tabelle*:

* Überprüfen Sie das Feld **Ein neues Feld erstellen**
* ** Feldname **: `x_coord`
* ** Feldtyp **: `Decimal number (real)`
* **Ausgangsfeldlänge**: `10` und **Präzision**: `10`
* Geben Sie eine Formel ein, indem Sie entweder den x-Wert aus der Geometrie in der Scrollbox auswählen oder direkt im Feld **Expression** eingeben:

```
 x( @geometry ) 
```

**Analog fügen Sie die `y_coord` mit**:

```
 y( @geometry ) 
```

**Save** die Bearbeitungen in der *Attribute Tabelle* durch Klicken auf das Laufwerkssymbol.

````

According to {cite:t}`meyer-peter_formulas_1948`, the {cite:t}`strickler_beitrage_1923` roughness (friction) coefficient can be approximated with $k_{st}$ $\approx$ 26/$D_{90}^{1/6}$ based on the grain size $D_{90}$, where 90% of the surface sediment grains are smaller. In addition, we will assume that $D_{90} \approx 2.25 \cdot D_{mean}$ {cite:p}`rickenmann_evaluation_2011`. Thus, $k_{st} \approx 26 \cdot (2.25 \cdot D_{mean})^{-1/6}$. To run this calculation, go to the **Field Calculator** and (see {numref}`Fig. %s <fric-pts-open-at>`):

* Überprüfen Sie das Feld **Ein neues Feld erstellen**
* ** Feldname **: `k_st`
* ** Feldtyp **: `Decimal number (real)`
* **Ausgangsfeldlänge**: `3` und **Präzision**: `2`
* Geben Sie eine Formel ein, indem Sie entweder `dMean` aus`Fields and Values` in der Scrollbox auswählen oder direkt die Gleichung im Feld **Expression* eingeben:

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

Die abschließende Attributtabelle der Friktions-pts-at-Schicht mit den optionalen x- und y-Koordinaten und den geschätzten Strickler-Rohigkeitskoeffizienten.
```

** Entfernen Sie alle übrigen unnötigen Felder** aus der *Attribute Table* und **save** die Editierungen durch Anklicken des Festplattensymbols und toggle (d.h. deaktivieren) Bearbeitung.

```{admonition} Download the friction-pts-at shapefile
:class: tip
Laden Sie die [zipped Friktions-pts formfile](https://github.com/hydro-informatics/telemac/raw/main/friction/friction-pts-at.zip) herunter und entpacken Sie sie in den Projektordner, z.B. `/ProjectHome/friction-pts-at.[SHP]`.
```

### Export Points nach XYZ

Beginnen Sie mit dem Öffnen des Exportdialogs mit einem rechten Klick auf die Friktion-pts-at-Schicht > Export > Funktionen speichern als... ({numref}`Fig. %s <fric-pts-export-as>`).

```{figure} ../../img/telemac/fric-pts-export-as.png
:alt: export friction points xyz qgis attribute table
:name: fric-pts-export-as
:width: 100%

Öffnen Sie den Exportdialog mit einem rechten Klick auf die Friktions-Tipps-Beschichtung > Export > Funktionen speichern als...
```

In der **Vector Layer speichern als...* Popup-Fenster, machen Sie die folgenden Einstellungen ({numref}`Fig. %s <fric-export-xyz>`):

* **Format**: `Comma Separated Value [CSV`
***Dateiname**: Klicken Sie auf **...*, navigieren Sie in den Projektordner und geben Sie `friction-pts.xyz` für Dateinamen ein ( drücken Sie **Save***).
* **Layer name**: Klar bleiben
**Koordinatenreferenzsystem**: Stellen Sie sicher, dass der Koordinatenreferenzsystem der Friktions-pts-at-Schicht definiert ist (in der Vitrine `EPSG:32633 - WGS 84 / UTM zone 33N`)
* **Encoding**: Standard (in der Vitrine `UTF-8`)
* **Select** alle relevanten **Felder**, d.h. im Schaufenster mindestens `k_st`. Die optionalen Felder `x_coord` und `y_coord` sind nur erforderlich, wenn die Geometrie nicht exportiert wird (aus welchem Grund auch immer).
* **Überprüfung** * **Persist Layer Metadaten**
* **Geometrie Typ*: `Automatic` (meist standardmäßig)
* * **Scroll down* zu den **Layer-Optionen** und:
** GEOMETRY*** an `AS_XY`
**SEPARATOR** an `TAB`
* **Uncheck** die **Add gespeicherte Datei auf Karte** Feld unten im Fenster.
* **Keep alle anderen Standardeinstellungen** und klicken Sie auf **OK**.

```{figure} ../../img/telemac/fric-export-xyz.png
:alt: xyz file export attribute table friction points
:name: fric-export-xyz

Einstellungen in der Speichern Vektorebene als... Popup-Fenster für den Export der Friktionspunkte in eine XYZ (tab-separierte CSV)-Datei.
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

## Alternative: Zeichnen Friction Zones in BlueKenue

Dieses Verfahren ist eine ungenaue Alternative zu der oben beschriebenen `roughness.xyz` Kreation aufgrund der schwachen geospatialen Referenzierungskapazitäten von BlueKenue, weshalb die untere {ref}`instruction box <bk-closed-fric-lines>` nur für Vollständigkeit vorgesehen ist.

````{admonition} Unfold to read this non-recommended alternative
:class: note, dropdown
:name: bk-closed-fric-lines

Beginnen Sie mit der Schaffung neuer geschlossener Linien ({numref}`Fig. %s <bk-new-closed-lines>`), ähnlich wie Polygone, die Rauheitszonen definieren.

```{figure} ../../img/telemac/bk-new-closed-lines.png
:alt: bluekenue create closed line
:name: bk-new-closed-lines
:width: 50%
:align: left

Einstellungen in der Speichern Vektorebene als... Popup-Fenster für den Export der Friktionspunkte in eine XYZ (tab-separierte CSV)-Datei.
```

```{figure} ../../img/telemac/bk-finalize-friction-cl.png
:alt: bluekenue roughness friction closed line
:name: bk-finalize-friction-cl
:width: 100%
:align: right

Dem abgegrenzten Bereich durch die geschlossene Leitung ist ein Reibwert (Roughness) (hier eine Stricklerrauhigkeit von 50) zuzuordnen.
```

Nach dem Ziehen einer *Closed line* wird die Taste `Esc` gedrückt und das Fenster unter {numref}`Fig. %s <bk-finalize-friction-cl>` wird angezeigt, wo ein Rauheitswert zugewiesen werden kann. Im Feld **Value** erhält die Abbildung eine Stricklerrauhigkeit von `50` an eine *Closed line* namens `A-D_substrate`. Geben Sie weiterhin Namen an alle relevanten Rauheitsbereiche zu.

Schließlich **save** die *Closed line* Objekte als `.i2s` / `.i3s` Dateien.
````


(bk-interpolate-fric-zones)=
# Zonal Friction Mesh (BlueKenue)

Dieser Abschnitt geht durch die Interpolation von Reibungswerten auf einer vorhandenen Selefin (`.slf`) Geometriedatei. Das Schaufenster baut auf der `.slf`-Datei auf, die in der {ref}`Telemac pre-processing tutorial <slf-prepro-tm>` erstellt wurde ([download qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf)). Starten Sie mit **opening BlueKenue*** und öffnen Sie die selafin `.slf` Datei: klicken Sie auf **File******** navigieren Sie in das Verzeichnis, in dem die `.slf` gespeichert ist, stellen Sie sicher, dass Sie **Telemac Selafin File (\*.slf)**, Highlight `qgismesh.slf` und drücken **********. Ziehen Sie die `BOTTOM (BOTTOM)`-Schicht aus den Workspace-Datenelementen an **Views*****2D View (1)*, um den korrekten Import des Netzes zu überprüfen und zu visualisieren ({numref}`Fig. %s <fric-bk-slf>`).


```{figure} ../../img/telemac/bk-slf.png
:alt: BlueKenue 2dmesh interpolated elevation
:name: fric-bk-slf

Die Vitrine qgismesh.slf selafin-Datei in BlueKenue geöffnet.
```

(bk-import-friction)=
## Import Friction Zones

Alternativ zur Erstellung von zonalen Reibwerten, die in einer mit QGIS generierten `.xyz`-Datei gespeichert sind, können Zonen auch direkt in BlueKenue durch eine Reihe von *Closed Linien* gezogen werden. Aufgrund der sehr begrenzten Kapazitäten von BlueKenue, um sich mit geospatialen Referenzen und Koordinatensystemen (Koordinatenreferenzsystem) zu befassen, ist ** die bevorzugte Option* für die Erstellung von Friktionszoneneingabe ** die obige Anwendung von **QGIS***.

`````{tab-set}
````{tab-item} Open the .xyz file in BlueKenue
Um die oben erstellte `.xyz`-Datei in BlueKenue zu öffnen:

* click on **File*****Open...*
* navigieren Sie in den Projektordner, in dem die `.xyz`
* Stellen Sie sicher, **Alle Dateien (\*.\*)** neben dem **Dateinamen:** Feld
* Hervorheben `qgismesh.slf`, und drücken Sie **Open**.

```{figure} ../../img/telemac/bk-fric-xyz-properties.png
:alt: bluekenue roughness friction visualize coefficients
:name: bk-fric-xyz-properties
:width: 100%
:align: left

Dem abgegrenzten Bereich durch die geschlossene Leitung ist ein Reibwert (Roughness) (hier eine Stricklerrauhigkeit von 50) zuzuordnen.
```

**Ignorieren** die **warning**-Nachricht (klicken Sie **OK**). Um die importierten Reibungswerte zu überprüfen und zu visualisieren **Rechtsklick** auf der **Friction-pts (X)* Layer > **Properties*** gehen Sie auf die **Data* Tab > **select Z(double)**, drücken Sie **Apply***. Dann gehen Sie zum **ColourScale** Tab, drücken Sie **Reset**, **Apply** und **OK****.

Überprüfen Sie die korrekte Darstellung der Reibwerte, indem Sie die `friction-pts (Z)`-Schicht aus den Arbeitsraumdaten auf **Views*****2D View (1)** ({numref}`Fig. %s <bk-fric-pts>`) ziehen.


```{figure} ../../img/telemac/bk-fric-pts.png
:alt: friction roughness coefficients bluekenue 
:name: bk-fric-pts


Die importierte Friktion-pts.xyz-Datei (erstellt mit QGIS) visualisiert in BlueKenue.
```
````

````{tab-item} Closed lines from BlueKenue
Falls noch nicht erledigt, importieren Sie die *Closed Linien*, die die Rauhigkeitszonen in Form von `.i2s` / `.i3s`-Dateien darstellen.
````
`````

## Interpolate Friction auf dem Mesh

In BlueKenue, go to **File** > **New** > **2D Interpolator**, which will occur in the **Work Space** > **Data Items**. **Drag & drop** either the **friction-pts** `.xyz` points or the *Closed line* objects delineating roughness zones **on the new 2D Interpolator** (see {numref}`Fig. %s <bk-fric-2d-interpolator>`).

```{figure} ../../img/telemac/bk-fric-2d-interpolator.png
:alt: bluekenue 2d interpolator roughness friction
:name: bk-fric-2d-interpolator
:width: 100%


Ziehen Sie auf einem neuen 2D Interpolator in BlueKenue die Friktionsschnitte (oder geschlossene Linien) durch.
```



Als nächstes fügen Sie eine neue Variable zum `qgismesh.slf`Netz hinzu, indem Sie das **Selafin `qgismesh`** Objekt (in **Work Space****Data Items**) und **Rechtsklick** darauf markieren. Klicken Sie auf ** Variable hinzufügen...** und geben Sie im Popup-Fenster ({numref}`Fig. %s <bk-new-slf-variable-fric>` oder {numref}`Fig. %s <bk-new-slf-variable-fricID>`) Folgendes ein, je nachdem, ob Sie mit Reibwerten arbeiten (wie hier mit Strickler Rauheit gezeigt) oder {ref}`friction IDs (see below) <tm-fricID>`:

`````{tab-set}
````{tab-item} BOTTOM FRICTION (Strickler) value
```{figure} ../../img/telemac/bk-new-slf-variable-fric.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fric
:width: 100%
:align: right


Fügen Sie eine neue Variable zum Selafin-Objekt für direkte Reibungswerte hinzu.
```
**Mesh***: `BOTTOM`
* **Name**: `BOTTOM FRICTION` (dieses Beispiel)
* **Units*: klar halten (irrelevantes Feld)
* **Standard-Node-Wert*: `30` (in diesem Beispiel) für einen Standardwert (Strickler) zu verwenden, wenn keine xyz-Friktionspunkte in der Nähe eines Netzknotens gefunden werden können

````

````{tab-item} FRICTION ID
```{figure} ../../img/telemac/bk-new-slf-variable-fricID.png
:alt: selafin add variable bluekenue roughness friction
:name: bk-new-slf-variable-fricID
:width: 100%
:align: right


Fügen Sie eine neue Variable zum Selafin-Objekt für Friktions-IDs hinzu.
```

**Mesh***: `BOTTOM`
* **Name**: `FRIC_ID` (muss eingegeben werden, kann nicht aus der Liste ausgewählt werden)
* **Units*: klar halten (irrelevantes Feld)
**Standard-Node-Wert**: `0` (ID zu verwenden, wenn keine xyz Punkte in der Nähe eines Netzknotens gefunden werden können)

````
`````

Um die Reibwerte auf dem Mesh zu interpolieren, markieren Sie die neue Variable `BOTTOM FRICTION` (oder `FRIC_ID`) des `qgismesh` Objekts in **Work Space**** **Data Items***. Das *Anonymat* der neuen Variablen kann ignoriert werden. Um die neue Variable auf das Netz abzubilden:

* Highlight the new `BOTTOM FRICTION` (oder `FRIC_ID`) mesh variabel (in **Data Items**)
* Gehe zu **Tools*****Map Object...*** (Top-Menü in {numref}`Fig. %s <bk-map-2d-interpolator>`)
* Wählen Sie den **neuen 2D Interpolator** aus und klicken Sie auf **OK**, der das **Processing...* Popup-Fenster öffnet
* Nach Abschluss der Verarbeitung klicken Sie auf **OK**.

```{figure} ../../img/telemac/bk-map-2d-interpolator.png
:alt: map object  2dinterpolator roughness friction bluekenue
:name: bk-map-2d-interpolator
:width: 100%

Zeigen Sie den Reibwert auf dem neuen 2D Interpolator in BlueKenue.
```

```{figure} ../../img/telemac/bk-fric-colourscale.png
:alt: bottom friction colourscale selafin bluekenue
:name: bk-fric-colourscale
:width: 100%
:align: right

Passen Sie die Farbskala für BOTTOM FRICTION an.
```

Überprüfen Sie die richtige Interpolation:

* Definieren Sie eine relevante Farbskala:
* In **Work Space**** **Data Items*********************                                                   
* In den Eigenschaften gehen Sie auf die Registerkarte **ColourScale** und verwenden Sie beispielsweise eine *Linear*-Skala mit `10` *Levels*, ein *Min* von `22` und ein *Interval* von `1.8`. Das vorbildliche Minima und Intervall sind gute Wahlen für das Schaufenster, aber andere Einstellungen können für andere Anwendungen bevorzugt sein (z.B. bevorzugen *Min* von `0`, wenn man Mannings $n_m$ verwendet).
***************
* **Drag & drop** die Variable **BOTTOM FRICTION*** in **Views** > **2D View (1)** zur Überprüfung der korrekten Interpolation von Reibwerten (z.B. siehe {numref}`Fig. %s <bk-fric-on-mesh>` für das Schaufenster).

```{figure} ../../img/telemac/bk-fric-on-mesh.png
:alt: selfin slf mesh bottom friction bluekenue
:name: bk-fric-on-mesh

Die korrekt interpolierte neue BOTTOM FRICTION Variable des qgismesh.slf mesh.
```

Um ***** das selafin **mesh** mit den interpolierten Reibungswerten zu speichern, **right-click** auf dem **qgismesh selafin object*** **Properties*** gehen Sie auf die Registerkarte **Meta Data** und geben Sie einen neuen **Name** ein, z.B. `qgismesh-friction`. Weiter, **highlight the selafin object* (z.B. `qgismesh-friction`) und **click on the disk<img src="../../img/telemac/bk-sym-save.png">symbol**. Wenn die Umbenennung keinen Einfluss auf den Dateinamen hatte, bestätigen Sie, dass die bestehende Datei ersetzt wurde.


```{admonition} Download qgismesh-friction.slf (with BOTTOM FRICTION)
:class: tip
Laden Sie die aktualisierte [qgismesh-friction.slf mit BOTTOM FRICTION](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf).
```


# Telemac Bindings

(zonal-fric-cas)=
## Implementierung in der CAS-Datei

### Friction Schlüsselwörter

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

Fügen Sie den Buchstaben `W` zu den grafischen Ausdrucken hinzu, um den Reibungskoeffizienten in die Ergebnisdatei zu schreiben:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
VARIABLES FOR GRAPHIC PRINTOUTS : 'U,V,H,S,Q,W' / add W for friction coefficient
```


````{admonition} Do you have more than 10 different friction zones?
:class: tip, dropdown

Um die Anzahl der von Telemac erkannten Reibungszonen zu erhöhen, setzen Sie das **MAXIMUM NUMBER OF FRICTION DOMAINS** Schlüsselwort zum Beispiel an `20`:

```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
MAXIMUM NUMBER OF FRICTION DOMAINS : 20 / default is 10
```
````


### Erste Hotstart-Bedingungen (optional)

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 4.1.3 in der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Um die Simulation zu beschleunigen, nutzt dieses Tutorial die Ausgabe des {ref}`steady 2d simulation <telemac2d-steady>` (obwohl mit einer Druckzeit von `2500` Schritten neu erstellt wird). Diese Art der Modell initialization wird auch *hotstart* genannt, hier basierend auf der stetigen Ergebnisdatei [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf), die als **PREVIOUS COMPUTATION FILE* definiert werden muss:

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

Damit diese Randbedingungen wirksam werden, müssen die Flüssigkeitsgrenzen aus der stationären 2d-Simulation geändert werden:

* offen *boundaries.cli* in einem {ref}`text editor <npp>`
* die `5 5 5` (beschrieben Q und H) vorgelagerte Grenze finden und durch `4 5 5` (beschrieben nur Q) ersetzen
* speichern und schließen *boundaries.cli*
* Weitere Informationen finden Sie im Spotlight Kapitel unter {ref}`boundary conditions <tm-foc-bc>`
* alternativ, [download der angepassten Grenzen.cli here](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli).

Schließlich kommentieren Sie alle anfänglichen Bedingungen Keywords in der `.cas`Lenkungsdatei, zum Beispiel:


```fortran
/ steady2d-zonal-ks.cas steering file
/ ...
/ INITIAL CONDITIONS : 'ZERO DEPTH'
/ INITIAL DEPTH : 0.005
```

## Simulation der Friction Zone

Stellen Sie sicher, dass alle benötigten Dateien in einem Simulationsordner platziert werden (z.B. `/HOME/modeling/friction-tutorial/`), insbesondere:

* Die [qgismesh-friction.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/qgismesh-friction.slf)mesh mit `BOTTOM` und `BOTTOM FRICTION`
* berichtigt [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/friction/boundaries.cli)
* die [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction/r2dsteady-t15k.slf)-Ergebnis, um den Hotstart zu aktivieren
* die [steady2d-zonal-ks.cas](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas) Lenkdatei mit aktualisierten Keywords.

Navigate (`cd`) to the Telemac installation directory (`HOMETEL`) to activate (`source`) the Telemac environment in Terminal (use the same environment as for {ref}`compiling Telemac <tm-compile>`):

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
```

Anschließend `cd` in den Simulationsordner und führen Sie die Simulation, möglicherweise mit der `-s`-Flagge, zurück {ref}`flux convergence <tm-convergence>`:

```
cd ~/modeling/friction-tutorial/
telemac2d.py steady2d-zonal-ks.cas -s
```

Der erfolgreiche Simulationslauf wird mit so etwas abgeschlossen sein:

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

Flux-Konvergenz über die beiden Grenzen der Hotstart-Simulation Telemac2d, beginnend zu einer Simulationszeit von 15000 Zeitschritten.
```
````

````{tab-item} Convergence rate
```{figure} ../../img/telemac/convergence-rate-zonal-fric.png
:alt: zonal friction convergence rate fluxes telemac boundaries
:name: tm-friction-convergence-rate

Die Konvergenzrate $\iota$ als Funktion 15000 Simulations-Zeitschritte der hotstarted stationären 2d-Simulation mit Reibzonen.
```
````
`````

Das benötigte [steady2d-zonal-ks.cas 2023-07-28-14h55min04s ist hier](https://github.com/hydro-informatics/telemac/raw/main/friction/steady2d-zonal-ks.cas_2023-07-28-14h55min04s) zur Verwendung mit Anweisungen aus dem Scheinwerferkapitel unter {ref}`convergence <tm-convergence>` erhältlich.

```{admonition} Look at the results in QGIS

Laden Sie die Simulationsergebnisse Datei (`r2dsteady-ks-zonal.slf`) in QGIS ein, um die Korrektheit der verwendeten Bodenreibung zu überprüfen und die leichten Änderungen der Fließgeschwindigkeit und der Wassertiefe, die sich aus den jetzt unterschiedlichen Rauheitswerten (Reibwerte) ergeben, anzuschauen.
```

(tm-fricID)=
# Arbeiten mit Friction-IDs

Die Friktionszonen können auch über Friktions-IDs zugeordnet werden, die dann eine Zonendatei und eine Friktionsdatendatei einrichten müssen, wie sie beispielsweise im Donau-Beispiel (`HOMETEL/examples/telemac2d/donau/`) dargestellt ist.

```{admonition} The Donau zonal friction ID example
:class: tip

Die BAW-Fallstudie lebt in `HOMETEL/examples/telemac2d/donau/` und wurde auf der XX. Telemac-Mascaret-Benutzerkonferenz vorgestellt. Das Konferenzverfahren steht im Rahmen des BAW-Portals [HENRY portal](https://hdl.handle.net/20.500.11970/100418) (Anfragen Sie den Beitrag *Umgekehrtes Engineering von Anfangs- und Randbedingungen mit Telemac und algorithmischer Differenzierung*). Dieser Fall verwendet jedoch eine unnötige Komplikation in Form einer `.bfr`Zonendatei. Das geospatiale Referenzsystem dieses Beispiels ist EPSG 31468 (GK4) (siehe [dieser Beitrag im Telemac Forum](http://opentelemac.org/index.php/kunena/16-telemac-2d/14284-coordinate-reference-systems-and-projections-of-examples-e-g-donau#43037)).
```

Im Schaufenster dieses Tutorials müssen die in {numref}`Tab. %s <tab-tm-fricID-zones>` definierten Friktions-IDs mit Friktionstabellen an die `BOTTOM FRICTION` Variable des `.slf`Netzes vergeben werden. Die entsprechenden Dateien können von unseren Repositories heruntergeladen werden:

* [Reib-mit-IDs.xyz](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction-with-IDs.xyz) für Interpolation in BlueKenue ({ref}`see above <bk-interpolate-fric-zones>` oder direkt
* [get qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) mit `BOTTOM` und `FRIC_ID` statt `BOTTOM FRICTION` Strickler Rauheitskoeffizienten (verwendet Standardreibung ID`0`).

## reibung.tbl & CAS

### Friktion erstellen.tbl

Erstellen Sie eine Friktionstabellendatei namens `friction.tbl` (berücksichtigen Sie diese [friction.tbl template](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl)) mit folgendem Inhalt, wobei die `no`Einträge (hier ab Zeile 36) dem Netz zugewiesenen`FRIC_ID` entsprechen müssen (Recall {numref}`Fig. %s <bk-new-slf-variable-fricID>`):

```{aside} More information

Die Anlage E der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) bietet weitere Erläuterungen zu den tabellarischen Parametern (z.B. `typeB`,`rB` oder `nDefB`) und die Reibungsgesetze (z.B. STRI, NIKU) werden in diesem eBook im stationären-2d {ref}`section on friction <tm2d-friction>` näher erläutert.
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

### Link Reibung.tbl in CAS-Datei

Um die Reibungsdaten zu aktivieren, fügen Sie die folgenden Schlüsselwörter in die Steuerungsdatei `.cas` ein und deaktivieren Sie alle nichtwandbezogenen FRICTION-Keywords:


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

Speichern Sie die `.cas` Lenkdatei.

## Telemac mit Friction-IDs ausführen

Um Telemac mit Friktions-IDs zu betreiben, stellen Sie sicher, dass die oben angegebenen Keywords in der Steuerungsdatei `.cas` aktiviert werden. Die benötigten Dateien umfassen jetzt:

* [qgismesh-frictionIDs.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/qgismesh-frictionIDs.slf) (mesh mit `FRIC_ID`)
* [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/boundaries.cli) oder Hotstart-Bedingungen
* [r2dsteady-t15k.slf](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/r2dsteady-t15k.slf)-Ergebnis, um den Hotstart zu aktivieren
* [steady2d-zonal-ID.cas](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/steady2d-zonal-ID.cas) Lenkdatei aktualisierte Schlüsselwörter
* [friction.tbl](https://github.com/hydro-informatics/telemac/raw/main/friction-with-IDs/friction.tbl) mit Friktionsausweisen

Mit diesen Dateien aktivieren und ausführen Telemac wie üblich:

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
cd ~/modeling/frictionID-tutorial/
telemac2d.py steady2d-zonal-ID.cas
```


# Erweiterte Friktionsroutinen

Änderung des **FRICTION USER** Fortran Unterprogramme ist nicht zwingend für die Arbeit mit Reibzonen, sondern kann nützlich sein, um das Verhalten von Rauheitsgesetzen umzusetzen oder anzupassen. Um z.B. ein FRICTION USER-Unterprogramm zu aktivieren, um die variable Leistungsgleichung von {cite:t}`ferguson_flow_2007`:

* Kopieren Sie die FICTION USER-Unterprogrammvorlage von `HOMETEL/sources/telemac2d/friction_user.f` in einen neuen Ordner Ihres Simulationsverzeichnisses, zum Beispiel:
```
/HOME/modeling/frictionID-tutorial/user_fortran/friction_user.f
```
* Editieren und speichern von `friction_user.f`.
* Sagen Sie der Steuerungsdatei (`.cas`) die modifizierte FRICTION USER Fortran-Datei, indem Sie das Keyword `FORTRAN FILE : 'user_fortran'` hinzufügt, wodurch Telemac2d Fortran-Dateien im Unterordner `/user_fortran/` aufruft.






