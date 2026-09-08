---
description: Tutorial für die Verarbeitung von Drohnen (UAV) Luftbildern mit Agisoft Metashape zur Erstellung von digitalen Höhenmodellen (DEMs) und Orthobildern für Fluss- und Geländevermessungen.
---

# Bildmaterial für Prozessdrohne (UAV)

```{admonition} This tutorial exceptionally requires proprietary software
:class: important


Dieser Abschnitt bietet Datenextraktion mit *Agisoft * proprietärer *Metashape * Software (Professional Edition). Für pädagogische Test- und Testzwecke, [download Agisoft Metashape](https://www.agisoft.com/downloads/installer/) mit der 30-Tage-Testlizenz]. Die Software funktioniert unter Windows, macOS und Linux. Beachten Sie, dass dieses Tutorial auf Metashape Version 1.8.3 aufbaut.
```

## Übernahme von Aerial Drone Imagery

Das Sammeln von Luftbildern ist dank autopilotgesteuerter Drohnen erstaunlich einfach geworden. Heute sind die meisten Drohnen mit Programmen für Luftaufnahmen und SfM-basierte digitale Höhenmodelle ({term}`Digitales Oberflächenmodell <DEM>`s) ausgestattet. Da die Drohnensteuerung modellabhängig ist (z. B. verwenden wir eine [dji Phantom 4 RTK](https://dl.djicdn.com/downloads/phantom_4_rtk/20200721/Phantom_4_RTK_User_Manual_v2.4_EN.pdf)Drohne für Luftaufnahmen), beschreibt dieses Tutorial nur grundlegende Einstellungen für die Aufnahme von Luftbildern und konzentriert sich auf die Bildverarbeitung zur Erstellung von DEMs.

Empfehlungen für Umfrageflüge mit Drohnen:

* Verwenden Sie vordefinierte terrestrische Vermessungsmodi für ausreichende Überlappungen
* Arbeiten Sie vorzugsweise mit Orthobildern; Verwenden Sie nur den 3D-Modus, wenn starker Wind weht
* Berücksichtigen Sie etwa 20-30 Minuten Flugzeit pro Batterie (ca. 2 Stunden Aufladen), was bedeutet, dass 8 Batterien eine reibungslose Zuordnung ermöglichen
* Bodenkontrollpunkte können weggelassen werden, wenn RTK-Daten verfügbar sind, aber wir empfehlen die Verwendung von Bodenkontrollpunkten

In addition, an imagery-based DEM can also be built for shallow, clear waters (i.e., bathymetries) but other measurement techniques (e.g., {term}`Lidar` or {term}`Sonar`) are required for deeper waters (> 0.5 m water depth). Also, imagery-based bathymetry should be validated or corrected with local DGPS or total station measurements.


## Metaform

Die folgende Abbildung zeigt die Metashape-Schnittstelle beim Start des Programms, bereit zum Spielen mit Drohnenbildern und SfM.


```{figure} ../img/drone/metashape-startup.png
:alt: metashape agisoft gui interface
:name: meta-startup

Die erste Metashape-Schnittstelle.
```


### Erstellen Sie ein neues Projekt

To get started, **create** a **new project** and **save** it (as `.psx` file) preferably one folder level above the images directory. Next, familiarize with the interface and explore the numerous workflows provided in the **Workflow** menu.


```{admonition} Metashape workflows
:class: tip

Metashape has multiple built-in workflows that enable us to intuitively navigate through the creation of imagery-based SfM products. We will use some of these workflows in the following to derive a {term}`Digitales Oberflächenmodell <DEM>`.
```

### Ladebilder

Bilder können dateiweise oder viel einfacher aus einem gesamten verzeichnis geladen werden. Um ein Verzeichnis (d. H. Ordner) mit Luftbildern von einer Drohne mit einer einzigen Kamera hinzuzufügen, gehen Sie zum Menü **Workflow** > **Ordner hinzufügen** > **Ordner auswählen, der Bilder enthält** > **Einzelkameras**.


### Bilder ausrichten

Wenn die Drohne über Gelände fliegt, muss sie manchmal ihre Richtung oder Position ändern, aber sie weiß immer, wo sie sich befindet (absolut oder relativ zu einer Bodenstation), wenn RTK-GPS-Daten verfügbar sind. Dadurch können die Bilder unter unterschiedlichen Winkeln und unterschiedlichen Positionen aufgenommen worden sein. Um die Bilder zu einem großen Bild des Geländes zusammenzuführen, müssen die Bilder durch übereinstimmende Punkte ausgerichtet werden, die auf mehreren Bildern sichtbar sind. Das große Bild kann mit dem Ausrichtungswerkzeug von Metashape erstellt werden: gehen Sie zu **Workflow** > ** Fotos** ausrichten und die folgenden Einstellungen im Popup-Fenster (siehe Abbildung unten) mit dem erweiterten **Advanced**-Frame berücksichtigen:

* Stellen Sie die **Accuracy** auf **high** für ein akzeptables Gleichgewicht von Auflösung und Rechenzeit. Beachten Sie, dass jede zusätzliche Erhöhung der Genauigkeit zu einer Größenordnung längeren Berechnungszeiten führt.
* In **Referenzvorauswahl** wählen Sie **Quelle** und stellen Sie sicher, dass Sie GPS-Daten verwenden.
* **Erweiterter** Frame:
    * Die Option **Key Point Limit** ermöglicht die Definition **charakteristischer Punkte** (d.h. Punkte, die der Ausrichtungsalgorithmus auf mehreren Bildern eindeutig identifizieren kann): Stellen Sie sicher, dass die Identifizierung von 10.000 bis 40.000 charakteristischen Punkten möglich ist.
    * Die **Tie-Punkt-Grenze** definiert eine Mindestanzahl für Bindepunkte (d.h. Punkte, die der Ausrichtungsalgorithmus auf zwei benachbarten Bildern identifiziert): Stellen Sie sicher, dass die Identifizierung von mindestens 1.000 bis 5.000 Bindepunkten ermöglicht wird.
    * Verwenden Sie die Option **enable exclusion of stationary points**, die sicherstellt, dass Pixel mit den gleichen (Farb-) Eigenschaften auf allen Bildern (d.h. die stationär sind) von der Ausrichtungskennung ausgeschlossen werden. So werden beispielsweise Schmutzflecken auf dem Kameraobjektiv als Ausrichtschlüsselpunkte ausgeschlossen.
    * Aktivieren Sie **adaptives Kameraanpassungsmodell** für unkorrigierte Kameraverzerrungen.
* Lassen Sie alle anderen Standard-Felder unverändert und klicken Sie auf **OK**, um die Ausrichtung zu starten. Abhängig von der Menge und Größe der Bilder sowie der Berechnungskapazität Ihres Computers dauert die Ausrichtung 5-30 Minuten.

```{figure} ../img/drone/metashape-align.png
:alt: metashape align fotos images pictures
:name: meta-align

Die Ausrichtung Fotos Popup-Fenster in Metashape.
```

When the alignment is accomplished, produce a **coarse point cloud** (select from the **Tools** menu). A qualitatively good coarse point cloud is characterized by at least 100 tie points per m$^2$ or more than 50.000 tie points per 100 images (with a resolution of 4605x3227). In addition, **verify errors** with a click on the **Reference** ribbon (typically at the bottom left of the Metashape window). The longitude/latitude error should be $\leq$ 2 cm.


### Dense Point Cloud erstellen

Wenn die Qualität ausreichend ist und der Fehler akzeptabel niedrig ist, erstellen Sie eine ** dichte Punktwolke ** (wählen Sie aus dem ** Workflow ** Menü). Führen Sie im dichten Wolken-Popupfenster (siehe auch Abbildung unten) die folgenden Einstellungen aus:

* Stellen Sie die **Qualität ** hoch **
* Wählen Sie **Tiefenfüllung** als Funktion der Vegetationsdichte:
    * wenn nein zu sehr wenig Vegetation, wählen Sie ** moderat / agressiv **
    * Wenn Vegetation vorhanden ist, kann eine gute Leistung (Punktwolkenqualität vs. Rechenzeit) durch die Wahl der Option **mild** erreicht werden.
    * bei sehr dichter Vegetation kann die Tiefenfüllung ** deaktiviert ** werden, obwohl dies zu ** sehr langen Rechenzeiten ** führen kann
* Klicken Sie auf **OK**, um die dichte Punktwolke zu erstellen (kann wieder 5-30 Minuten dauern)

```{figure} ../img/drone/metashape-dense-cloud.png
:alt: metashape dense point cloud
:name: meta-dense-cloud

Der dichte Punktwolken-Popup-Dialog in Metashape.
```

Die **Qualität** der dichten Punktwolke kann als gut angesehen werden, wenn der Prozess gefunden wird:

* Mindestens 20 bis 30 Nachbarn.
* Etwa 10 Millionen Punkte pro 100 Bilder (mit einer Auflösung von 4605x3227).


### Digitales Oberflächenmodell (DOM) schaffen

The dense or coarse point cloud can be used with many other workflows and the creation of a {term}`Digitales Oberflächenmodell <DEM>` is only one option. To create a DEM, go to **Workflow** > **Build DEM** and consider the following aspects in the build DEM popup window (see figure below):

* Projektion:
    * use a **geographic** type for projection onto a {term}`GeoTIFF` raster, which is compatible with most GIS software, such as {ref}`QGIS <qgis-tutorial>`.
    * Metashape's default projection is `EPSG:4326` (read more in the section on {ref}`projections in this eBook <prj>`), which corresponds to the projection commonly used with aerial imagery interfaces (e.g., *GoogleEarth*).
* Quellendaten:
    * Die Option **tie points** führt zur **niedrigsten Auflösung**.
    * Die Option **Tiefenkarten** ist ein **guter Kompromiss** zwischen Auflösung und Rechenzeit.
    * Die Option **dense cloud** führt zu der **besten Qualität**, aber auch zu einer sehr langen Rechenzeit.
* Erweiterter Frame: Halten Sie automatisch vorgeschlagene Werte, um Konsistenz zu gewährleisten.

Der **OK**-Button startet die Digitales Oberflächenmodell (DOM)-Erstellung, die wiederum 5-30 Minuten dauern kann.

```{figure} ../img/drone/metashape-dem.png
:alt: metashape dem dgm digital elevation model geotiff
:name: meta-dem

Der Digitales Oberflächenmodell (DOM) Creation Popup Dialog in Metashape.
```

Exportieren Sie die Digitales Oberflächenmodell (DOM) schließlich mit einem **Rechtsklick** auf die **Digitales Oberflächenmodell (DOM)** im **Workspace** (wenn die Digitales Oberflächenmodell (DOM) nicht sichtbar ist, erweitern Sie den **Chunk 1** Eintrag - oder welchen Namen sie auch immer hat - im Workspace) und wählen Sie **Export Digitales Oberflächenmodell (DOM)...**. Wir empfehlen, das Digitales Oberflächenmodell (DOM) im Format {term}`GeoTIFF` (**.tif**) zu speichern, das mit {ref}`QGIS <qgis-tutorial>` kompatibel ist. Wenn `.tif` ausgewählt wurde, öffnet sich ein Popup-Fenster zum Exportieren des Digitales Oberflächenmodell (DOM). Aktivieren Sie im Popup-Fenster die Option **Weltdatei exportieren** und behalten Sie alle anderen Standardeinstellungen bei (optional erstellen Sie eine `.kml`-Datei zum Arbeiten mit *GoogleEarth*). Die Weltdatei wird für QGIS (und jede andere GIS-Software) wichtig sein, um zu wissen, wo sich die Digitales Oberflächenmodell (DOM) geografisch in Bezug auf die ausgewählte Projektion befindet.


### Erstellen Sie ein Mesh

Ähnlich wie der Digitales Oberflächenmodell (DOM)-Workflow bietet Metashape einen Workflow zum Erstellen eines Meshs (**Workflow** > **Build Mesh**) in Form eines triangulierten unregelmäßigen Netzwerks ({ref}`TIN <tin>`). Die **Source-Daten**-Optionen ähneln denen im Digitales Oberflächenmodell (DOM)-Workflow, mit einer zusätzlichen Option, die Digitales Oberflächenmodell (DOM) für das Meshing zu verwenden. Auch für ein Mesh ergeben **High** Qualität und Gesichtszahlen die beste Darstellung des Geländes und hohe Rechenkosten. Wenn das Ziel der Mesh-Generation die Verwendung mit einem numerischen Modell ist, können geringere Qualität und Gesichtszahlen eine gute Wahl sein, um die Zeit für die Ausführung des numerischen Modells niedrig zu halten. Die Mesh-Generierung dauert wieder 5-30 Minuten.

```{figure} ../img/drone/metashape-mesh.png
:alt: metashape mesh creation stl numerical model
:name: meta-mesh

Der Mesh Creation Popup Dialog in Metashape.
```

Sobald die Mesh-Erstellung abgeschlossen ist, kann sie mit einem Rechtsklick auf den Eintrag **3D Model** im **Workspace** und einem Linksklick auf **Export Model...** exportiert werden. Wenn das 3D-Modell im Arbeitsbereich nicht sichtbar ist, erweitern Sie den Eintrag **Chunk 1** (oder welchen Namen er auch immer hat). Für die Verwendung mit einem numerischen Modell (z. B. OpenFOAM) ist das Format STL (`.stl`) eine gute Wahl.


```{admonition} Take advantage of Metashapes Python bindings
:class: tip

Metashape comes with Python script than enable automation of calls to workflows with varying parameters. To get started with Python, have a look at the {ref}`Python tutorials <about-python>` in this eBook and Agisoft's [Python reference guide](https://www.agisoft.com/pdf/metashape_python_api_1_5_0.pdf).
```
