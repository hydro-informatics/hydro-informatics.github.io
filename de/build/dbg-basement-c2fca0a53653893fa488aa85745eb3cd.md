---
description: Lösungen für gängige BASEMENT numerische Modellfehler, einschließlich XDMF Ausgabe Import Probleme und Simulation Verzeichnis Probleme in der QGIS-Nachbearbeitung.
---

# Debugging BASEMENT

Seit seiner frühen Entwicklung ist *BASEMENT* ein robustes, zuverlässiges Werkzeug für die numerische Modellierung von Flüssen geworden. Dennoch gibt es ein paar kleine Herausforderungen und diese Seite gibt einige Antworten (unter Entwicklung).

(dbg-bm-xdmf)=
## Import von XDMF Modell-Ausgangsfehlern


### XDMF Fehler falscher Versionen

Je nach Systemumgebung kann der Header von `results.xmdf` für QGIS nicht lesbar sein. Die beiden unteren Tabs zeigen die falschen und korrekten Header-Linien. Um das Problem zu beheben, öffnen Sie `results.xmdf` in einem Texteditor (z.B. {ref}`Notepad++ <npp>` unter Windows), ersetzen Sie das Unrecht mit dem richtigen Header und speichern Sie das korrigierte `results.xmdf`.

`````{tab-set}
````{tab-item} Wrong header
```html
<?xml version="1.0"?>
<Xdmf Version="3.0">
```
````

````{tab-item} Correct header
```html
<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
```
````
`````

### XDMF Fehler falscher Simulationsverzeichnisse
Die `results.xdmf` enthält geospatial explizite Daten (z.B. Strömungsgeschwindigkeit und Wassertiefe), die theoretisch direkt in *QGIS* mit dem *Crayfish*-Plugin importiert werden können (lesen Sie mehr im Abschnitt {ref}`BASEMENT post-processing <qgis-imp-steps>`). Es gibt jedoch ein kleines Problem: QGIS kann wegen eines ungültigen Verzeichnisses abstürzen. Um es zu beheben:

1. Öffnen Sie `results.xdmf` in einem Texteditor (z.B. {ref}`Notepad++ <npp>` unter Windows).
1. Verwenden Sie das Find-and-Replace-Tool (`CTRL` + `H`keys in Notepad++), um Dateipfade vor `results_aux.h5` zu entfernen.
    * Suchen Sie die `results_aux.h5`-String und identifizieren Sie den davor geschriebenen Pfad (z.B. `C:\temp\`).
    * Finden und ersetzen Sie diesen Benutzerpfad, zum Beispiel: `Find` = `C:\temp\results_aux.h5` und `Replace with` = `results_aux.h5`.
1. Nachdem alle Pfadereignisse im Dokument entfernt wurden, speichern und schließen Sie `results.xdmf`.


Diese Ausgabe wird auch im [BASEMENT User Forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?id=5261)] diskutiert.
