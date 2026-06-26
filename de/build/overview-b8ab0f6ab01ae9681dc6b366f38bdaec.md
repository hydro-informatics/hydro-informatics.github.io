---
description: Überblick über Vorträge, Übungen und Open-Access-Videokurse über Hydroinformatik, Python, numerische Modellierung und Geospatialanalyse an der Universität Stuttgart.
---

# Vorträge und Übungen

## Vorträge

Die meisten Kurse finden vor einem Bildschirm in Form von Videokonferenzen, Videostreaming, Wiki-ähnlichen Dokumentationen oder interaktiven Übungen statt.
In pandemisch-freien Zeiten stehen den Studierenden direkt am Campus der Universität Stuttgart Computer zur Verfügung. Um unabhängige Arbeitskapazitäten zu verbessern, ist es jedoch sehr empfehlenswert, dass die Schüler lernen, eine effiziente Arbeitsumgebung auf einem Laptop oder Desktop-Computer einzurichten.

```{tip}
Studierende der Universität Stuttgart können das [TIK GitHub-Konto und Login page](https://github.tik.uni-stuttgart.de/login) (verwenden Sie Ihre institutionelle ID, z.B. `st9009133`), um die Zusammenarbeit mit Code zu nutzen.
```

Das {ref}`software`-Kapitel führt durch die Installation relevanter Software für Vorträge.

Â Open Access Videos

Einige Inhalte dieser Website werden von öffentlichen Videos begleitet, die auf *YouTube* gehostet werden. Erfahren Sie mehr über den Besuch der [@Hydroinformatik (Hydro-Morphodynamik) YouTube Channel](https://www.youtube.com/@hydroinformatics).

## Übungen

Übungen sind integraler Bestandteil dieses eBooks und zusätzliche Materialien werden auf externen Git-Repositories bereitgestellt, wie:

* Zuweisungshinweise,
* Codevorlagen und
* Datendateien.

Der Link zu jedem Übungs-Git-Repository ist oben auf jeder Übungsseite vorgesehen.

(pywrm)=
## Python Programmierung für Wasserressourcen Engineering und Forschung

### Über uns
Dieser Kurs führt die Versionssteuerung git und die Programmiersprache Python 3 ein. Die Studierenden lernen, Programmiermethoden für Engineering-Aufgaben, Datenverarbeitung einschließlich grundlegender statistischer Auswertungen und geospatialer Analysen zu verwenden. Praxisorientierte Übungen mit kleinem Heimwerkerführer durch die programmatische Lösung zu typischen Herausforderungen in der Wasserressourcen-Engineering und Forschung, wie Ökohydraulische und Sedimenttransportanalysen. Die Kommunikation zwischen effizienten Algorithmen und verschiedenen Datentypen (z.B. *JSON* oder *xlsx* Arbeitsmappen) ist auch Teil der Vorträge und Übungen. Letzterer Teil des Kurses führt geospatiale Programmiermethoden und Datenanalysen ein.

Interaktive Vorlesungen vertrauten Studenten mit Versionskontrolle über git, Markdown-Sprache für Dokumentation und *Python* Programmierung. Der Kurs wird von der [IWS-LW-Abteilung](https://www.iws.uni-stuttgart.de/en/lww/) an der [Universität Stuttgart](https://www.uni-stuttgart.de/) in Wintersemester für das [Water Resources Engineering and Management (WAREM)](https://www.warem.uni-stuttgart.de/)-Programm] organisiert. Der Kurs baut auf internen und externen Open Access-Materialien auf, die als Referenzführer und Unterstützung für unabhängige Studien dienen.


### Anforderungen

Die Grundvoraussetzung ist die Bereitschaft, regelmäßig Zeit in die Vorlesungen zu investieren, da dieser Kurs mehr ist als nur eine Prüfung zu bestanden: Studenten werden neue Fähigkeiten erwerben.

Vorherige Programmiererfahrung ist nicht notwendig und der Kurs richtet sich auch und explizit an Studierende, die noch nicht Programmierwerkzeuge verwendet haben.

Verschiedene Softwarelösungen arbeiten für den Kurs und den Abschnitt unter {ref}`sec-ide` führt durch ihre Installation:

Mindestinstallation
: Alle Studenten benötigen ein Minimum an Software, um am Kurs teilzunehmen. Die Mindestsoftware beinhaltet:

  - {ref}`qgis-install`
  - Ein grundlegender Texteditor (jede Lösung funktioniert); *Windows* Benutzer können {ref}`npp` verwenden.
  - *Windows* Benutzer müssen auch {ref}`dl`.
  - Ein Rich Text Office-Datei-Editor, wie {ref}`lo`, wird auch sehr nützlich sein.

Die Installation von Anaconda ermöglicht die Nutzung verschiedener IDEs, die sogenannte *conda*-Umgebungen für Python verwenden. Dies ist die *all-inclusive* Option in Bezug auf Funktionalität, aber es ist ziemlich schwer in Bezug auf Speicher- und Systemressourcenverbrauch. Diese Full-Stack-Lösung muss Folgendes installieren:

  - Hauptsächlich {ref}`anaconda` mit *Anaconda Navigator* und *Anaconda Prompt* Schnittstellen, die die Installation von IDEs erleichtern.
  - Entweder {ref}`pycharm` (externer Inteface) oder *Spyder* (direkt erhältlich in *Anaconda*) IDE.
  - Optionally {ref}`jupyter` for editing and running jupyter notebooks (alternatively, use the [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hydro-informatics/hydro-informatics.github.io/main?filepath=jupyter) buttons that enable running jupyter notebooks online)



### Lernziele

Die Studierenden erwerben grundlegende und fortgeschrittene Fähigkeiten in der Python-Programmierung, Git-Versionskontrolle, Datenhandling und Geospatialanalysen. Der engagierte Lernende vertieft die Fähigkeit, logisch zu denken und Arbeitsprozesse in strukturierte, objektorientierte Algorithmen zu übersetzen. Durch die Anwendung von Open-Access-Software und Git werden die Studierenden in der Lage sein, jedes Team der Welt effektiv zu unterstützen und jedes Projekt zu fördern. Die praxisorientierten Übungen übertragen zusätzliche Kenntnisse, wie man Herausforderungen im Wasserressourcenmanagement nutzt.

(irme)=
## Integrierte Flutschutzplanung (IFP2)

### Über uns


Die hier zur Verfügung gestellten Materialien unterstützen die Labore und Projektarbeit. Jenseits der Beschreibungen, die in den Dokumenten zusammen mit den Laboren und Übungen zur Verfügung gestellt werden, werden diese Beschreibungen auch hier zur Verfügung gestellt, um Online-Arbeiten zu erleichtern, die aufgrund neuer Ereignisse eine rasch wachsende Bedeutung erlangt haben.

### Anforderungen

Achten Sie darauf, die folgenden Programme zu installieren (oder auf jedem zugänglichen Computer installiert haben):

* {ref}QGIS <qgis-tutorial>` Hilfe bei der Visualisierung und Modifizierung (Bearbeiten) geospatialer Datensätze.
* {ref}`Notepad++ <npp>`, um Randbedingungen und textähnliche Datendateitypen zu ändern.
* [ParaView](https://www.paraview.org/) ist ein leistungsstarkes Visualisierungstool für Modellausgänge (nicht zwingend).
* {ref}`Libre Office <lo>` (oder jede andere Software), um Arbeitsmappen zu bearbeiten (nicht zwingend).


### Online-Material

Das bereitgestellte Online-Material führt durch die numerischen Simulationsübungen. Die Anleitung beschreibt:

- Vorprozessdaten: Von Punktwolken bis hin zu Rechennetzen
- Aufbau und Ausführung einer numerischen Simulation
- Simulationsergebnisse nach dem Prozess: Visualisieren, verstehen und analysieren Sie die Modellausgabe.
- Kalibrierung & Validierung wird hier als integraler Bestandteil der numerischen Studien erwähnt.
