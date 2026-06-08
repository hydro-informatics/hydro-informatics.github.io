---
description: Tutorial zur Verarbeitung von Drohnen (UAV) Luftbildern mit Agisoft Metashape, um Digitale Höhenmodelle (DEMs) und Orthopädie für Fluss- und Geländebefragungen zu erstellen.
---

# Process Drone (UAV) Imagery

```{admonition} This tutorial exceptionally requires proprietary software
:class: important


Dieser Abschnitt enthält die Datenextraktion mit der proprietären *Metashape* Software von *Agisoft* (Professional Edition). Für pädagogische Test- und Testzwecke [Download Agisoft Metashape](https://www.agisoft.com/downloads/installer/) mit der 30-tägigen Testlizenz. Die Software funktioniert unter Windows, macOS und Linux. Beachten Sie, dass dieses Tutorial auf Metashape Version 1.8.3.
```

## Aerial Drone Images erwerben

Durch autopilotgesteuerte Drohnen ist das Sammeln von Luftbildern erstaunlich einfach geworden. Heute kommen die meisten Drohnen mit Programmen zum Drehen von Luftbild und Structure-from-Motion (SfM)-basierten digitalen Höhenmodellen ({term}`DEM`s). Da die Drohnensteuerung modellabhängig ist (z.B. verwenden wir eine [dji Phantom 4 RTK](https://dl.djicdn.com/downloads/phantom_4_rtk/20200721/Phantom_4_RTK_User_Manual_v2.4_EN.pdf) drone für Luftumfragen), beschreibt dieses Tutorial nur grundlegende Einstellungen für die Aufnahme von Luftbild und konzentriert sich auf die Bildverarbeitung zur Erstellung von DEMs.

Empfehlungen für Umfrageflüge mit Drohnen:

* Verwenden Sie vordefinierte terrestrische Erhebungsmodi für ausreichende Überlappung
* Vorzugsweise arbeiten Sie mit der Orthoimagery; verwenden Sie nur 3d-Modus, wenn starke Winde bläst
* Konto für ca. 20-30 Minuten Flugzeit pro Batterie (ca. 2 Stunden Nachladung), was bedeutet, dass 8 Batterien eine reibungslose Mapping ermöglichen
* Bodenkontrollpunkte können entfallen, wenn RTK-Daten zur Verfügung stehen, aber wir empfehlen die Nutzung von Bodenkontrollpunkten

Darüber hinaus kann ein bildbasiertes Digitales Oberflächenmodell (DOM) auch für flache, klare Gewässer (d.h. Badymetrien) gebaut werden, andere Messtechniken (z.B. {term}`Lidar` oder {term}`Sonar`) sind für tiefere Gewässer (> 0,5 m Wassertiefe) erforderlich. Auch sollte die bildbasierte Badymetrie mit lokalen DGPS oder Totalstationsmessungen validiert oder korrigiert werden.


## Metashare

Die folgende Figur zeigt die Metashape-Schnittstelle am Programmstart, bereit für das Spielen mit Drohnenbildern und SfM.


```{figure} ../img/drone/metashape-startup.png
:alt: metashape agisoft gui interface
:name: meta-startup

Die erste Metashape-Schnittstelle.
```


### Neues Projekt erstellen

Um loszuwerden, **create** ein **new project** und **save** es (als `.psx`-Datei) vorzugsweise eine Ordnerebene über dem Bilderverzeichnis. Als nächstes, vertraut mit der Schnittstelle und erkunden Sie die zahlreichen Workflows im **Workflow*-Menü.


```{admonition} Metashape workflows
:class: tip

Metashape verfügt über mehrere integrierte Workflows, die es uns ermöglichen, intuitiv durch die Erstellung von bildhaften SfM-Produkten zu navigieren. Einige dieser Workflows werden wir im Folgenden nutzen, um eine {term}`DEM` abzuleiten.
```

### Bilder laden

Bilder können von einem ganzen Verzeichnis geladen werden. Um ein Verzeichnis (d.h. Ordner) mit Luftbild aus einer Einkamera-Drohne hinzuzufügen, gehen Sie in das **Workflow*-Menü > ** Ordner hinzufügen** > **Select Ordner mit Bildern****Single Kameras***.


### Align Images

Wenn die Drohne über Gelände fliegt, muss sie manchmal ihre Richtung oder Position ändern, aber sie weiß immer*, wo sie (absolut oder relativ zu einer Bodenstation) ist, wenn RTK-GPS-Daten verfügbar sind. Dadurch können die Bilder unter unterschiedlichen Winkeln und unterschiedlichen Positionen aufgenommen worden sein. Um die Bilder in ein großes Bild des Geländes zu verschmelzen, müssen die Bilder durch Anpassungspunkte ausgerichtet werden, die auf mehreren Bildern sichtbar sind. Das große Bild kann mit Metashapes Ausrichtungswerkzeug erstellt werden: gehen Sie zu **Workflow*** **Align Fotos** und beachten Sie die folgenden Einstellungen im Popup-Fenster (siehe Abbildung unten) mit dem **Advanced** Rahmen erweitert:

* Setzen Sie die **Accuracy** auf **high** für ein akzeptables Gleichgewicht von Auflösung und Rechenzeit. Beachten Sie, dass jede zusätzliche Erhöhung der Genauigkeit in einer Größenordnung längere Rechenzeiten führt.
* In **Referenzvorwahl** Wählen Sie **Quelle** aus und stellen Sie sicher, dass Sie GPS-Daten verwenden.
* **Erweitert** Rahmen:
    * Die **Key Point Limit** Option ermöglicht die Definition von **Kennpunkten*** (d.h. Punkte, die der Ausrichtungsalgorithmus auf mehreren Bildern eindeutig identifizieren kann): stellen Sie sicher, dass 10.000 bis 40.000 charakteristische Punkte identifiziert werden können.
    * die **Tie-Punktgrenze** definiert eine Mindestzahl für Bindepunkte (d.h. Punkte, die der Ausrichtungsalgorithmus auf zwei benachbarten Bildern identifiziert): stellen Sie sicher, dass mindestens 1.000 bis 5.000 Bindepunkte identifiziert werden können.
    * Verwenden Sie die **-fähige Ausschluss von stationären Punkten**-Option, die sicherstellt, dass Pixel, die die gleichen (Farben) Eigenschaften auf allen Bildern (d.h. stationär) haben, von der Ausrichtungserkennung ausgeschlossen sind. So werden beispielsweise Schmutzflecken auf der Kameralinse als Richttastenpunkte ausgeschlossen.
    * Aktivieren Sie **Adaptive Kamera-Fitting-Modell* für unkorrigierte Kameraverzerrung.
* Lassen Sie ** alle anderen Standard ** Felder as-is und klicken Sie auf **OK**, um die Ausrichtung zu starten. Je nach Anzahl und Größe der Bilder sowie der Berechnungskapazität Ihres Computers dauert die Ausrichtung 5-30 Minuten.

```{figure} ../img/drone/metashape-align.png
:alt: metashape align fotos images pictures
:name: meta-align

Das align fotos Popup-Fenster in Metashape.
```

Wenn die Ausrichtung erreicht ist, erzeugen Sie eine **Koarse Punktwolke** (Auswahl aus dem **Tools** Menü). Eine qualitativ gute Grobpunktwolke zeichnet sich durch mindestens 100 Bindepunkte pro m$^2$ oder mehr als 50.000 Bindepunkte pro 100 Bilder aus (mit einer Auflösung von 4605x3227). Darüber hinaus **verify Fehler** mit einem Klick auf das **Reference** Band (typischerweise unten links im Metashape-Fenster). Der Longitude/Latitude-Fehler sollte $\leq$ 2 cm sein.


### Erstellen dichter Punkt Cloud

Wenn die Qualität ausreicht und der Fehler akzeptabel niedrig ist, gehen Sie mit dem Aufbau einer **dense Punktwolke*** fort (Auswahl aus dem **Workflow** Menü). Im dichten Punkt-Cloud-Popup-Fenster (siehe auch Abbildung unten), machen Sie die folgenden Einstellungen:

* ** Qualität*** auf **high** einstellen
* Wählen Sie ** Tiefe Füllung** in Abhängigkeit von Vegetationsdichte:
    * wenn nicht zu wenig Vegetation, wählen Sie **moderate / agressiv**
    * wenn Vegetation vorhanden ist, kann eine gute Leistung (Punktwolkenqualität vs. Rechenzeit) durch die Wahl der **mild** Option erreicht werden
    * bei sehr dichter Vegetation kann die Tiefenfüllung ** deaktiviert** sein, was zu ** sehr langen Rechenzeiten** führen kann.
* Klicken Sie auf **OK**, um die dichte Punktwolke zu erstellen (kann wieder 5-30 Minuten dauern)

```{figure} ../img/drone/metashape-dense-cloud.png
:alt: metashape dense point cloud
:name: meta-dense-cloud

Der dichte Punkt Cloud Popup Dialog in Metashape.
```

Die ** Qualität** der dichten Punktwolke kann als gut angesehen werden, wenn der Prozess gefunden wird:

* Mindestens 20 bis 30 Nachbarn.
* Ca. 10 Millionen Punkte pro 100 Bilder (mit einer Auflösung von 4605x3227).


### Digitales Oberflächenmodell (DOM) erstellen

Die dichte oder grobe Punktwolke kann mit vielen anderen Workflows verwendet werden und die Erstellung einer {term}`DEM` ist nur eine Option. Um eine Digitales Oberflächenmodell (DOM) zu erstellen, gehen Sie zu **Workflow** > **Build Digitales Oberflächenmodell (DOM)*** und beachten Sie folgende Aspekte im Aufbau-Digitales Oberflächenmodell (DOM)-Popupfenster (siehe Abbildung unten):

* Projekt:
    * Verwenden Sie einen **geographic**-Typ für Projektion auf einen {term}`GeoTIFF`raster, der mit der meisten GIS-Software kompatibel ist, wie z.B. {ref}`QGIS <qgis-tutorial>`.
    * Die Standardprojektion von Metashape ist `EPSG:4326` (weiter lesen Sie im Abschnitt unter {ref}`projections in this eBook <prj>`), was der Projektion entspricht, die häufig mit aerialen Bildoberflächen verwendet wird (z.B. *GoogleEarth*).
* Quellendaten:
    * Die **tie-Punkte**-Option führt zur **niedrigsten Auflösung**.
    * Die **Tiefe Karten** Option ist ein ** guter Kompromiss** zwischen Auflösung und Rechenzeit.
    * Die **dense Cloud*-Option führt zur **besten Qualität**, aber auch zu einer sehr langen Rechenzeit.
* Erweiterter Rahmen: automatisch vorgeschlagene Werte beibehalten, um Konsistenz zu gewährleisten.

Die **OK**-Taste startet die Digitales Oberflächenmodell (DOM)-Kreation, die wieder 5-30 Minuten dauern kann.

```{figure} ../img/drone/metashape-dem.png
:alt: metashape dem dgm digital elevation model geotiff
:name: meta-dem

Der Digitales Oberflächenmodell (DOM)-Erstellungs-Popup-Dialog in Metashape.
```

Schließlich exportieren Sie die Digitales Oberflächenmodell (DOM) mit einem **-Rechtsklick*** auf dem **Digitales Oberflächenmodell (DOM)** im **Workspace*** (wenn die Digitales Oberflächenmodell (DOM) nicht sichtbar ist, erweitern Sie den **Chunk 1**-Eintrag - oder welchen Namen es hat - im Workspace) und wählen Sie **Export Digitales Oberflächenmodell (DOM)...** Wir empfehlen, das Digitales Oberflächenmodell (DOM) im Format {term}`GeoTIFF` (*.tif**) zu speichern, das mit {ref}`QGIS <qgis-tutorial>` kompatibel ist. Wenn `.tif` ausgewählt wurde, öffnet sich ein Popup-Fenster zum Export der Digitales Oberflächenmodell (DOM). Im Popup-Fenster, überprüfen Sie die **export Weltdatei** Option und halten alle anderen Standardeinstellungen (optional erstellen Sie eine `.kml` Datei für die Arbeit mit *GoogleEarth*). Die Weltdatei wird für QGIS (und jede andere GIS-Software) wichtig sein, um zu wissen, wo sich die Digitales Oberflächenmodell (DOM) in Bezug auf die ausgewählte Projektion geographisch befindet.


### Erstellen Sie ein Mesh

Ähnlich wie beim Digitales Oberflächenmodell (DOM)-Workflow bietet Metashape einen Workflow zur Erstellung eines Netzes (**Workflow**********) in Form eines triangulierten unregelmäßigen Netzwerks ({ref}`TIN <tin>`). Die **Source-Daten**-Optionen sind ähnlich wie die im Digitales Oberflächenmodell (DOM)-Workflow, mit einer zusätzlichen Möglichkeit, die Digitales Oberflächenmodell (DOM) für das Meshing zu verwenden. Auch für ein Netz, **High** Qualität und Face Counts führen zu der besten Darstellung des Geländes und hohen Rechenkosten. Wenn das Ziel der Mesh-Generierung ist seine Verwendung mit einem numerischen Modell, niedrigere Qualität und Gesichtszahl könnte eine gute Wahl, um die Zeit für den Betrieb des numerischen Modells niedrig zu halten. Die Mesh-Generation dauert wieder 5-30 Minuten.

```{figure} ../img/drone/metashape-mesh.png
:alt: metashape mesh creation stl numerical model
:name: meta-mesh

Die Mesh-Erstellung Popup-Dialog in Metashape.
```

Sobald die Mesh-Erstellung beendet ist, kann sie mit einem Rechtsklick auf den **3D Model**-Eintrag im **Workspace** und einem linken Klick auf **Export Model...** exportiert werden. Wenn das 3D-Modell im Workspace nicht sichtbar ist, erweitern Sie den Eintrag **Chunk 1** (oder welchen Namen es hat). Für den Einsatz mit einem numerischen Modell (z.B. OpenFOAM) ist das Format STL (`.stl`) eine gute Wahl.


```{admonition} Take advantage of Metashapes Python bindings
:class: tip

Metashape kommt mit Python-Skript, als die Automatisierung von Anrufen zu Workflows mit unterschiedlichen Parametern zu ermöglichen. Um mit Python zu beginnen, schauen Sie sich die {ref}`Python tutorials <about-python>` in diesem eBook und Agisofts [Python reference guide](https://www.agisoft.com/pdf/metashape_python_api_1_5_0.pdf).
```
