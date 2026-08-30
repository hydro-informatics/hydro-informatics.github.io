---
description: Lösungen für häufige Fehler des numerischen BASEMENT-Modells, einschließlich XDMF-Ausgabeimportproblemen und Simulationsverzeichnisproblemen in der QGIS-Nachverarbeitung.
---

# Entschuldungsgrundlage

Seit seiner frühen Entwicklung ist *BASEMENT* ein robustes und zuverlässiges Werkzeug für die numerische Modellierung von Flüssen geworden. Dennoch gibt es ein paar kleine Herausforderungen und diese Seite bietet einige Antworten (in Entwicklung).

(dbg-bm-xdmf)=
## Import von XDMF Model Output fehlschlägt


### XDMF-Fehler falscher Versionen

Depending on the system environment, the header of `results.xmdf` may not be readable for QGIS. The two below tabs show the wrong and correct header lines. To fix the issue, open `results.xmdf` in a text editor (e.g., {ref}`Notepad++ <npp>` on Windows), replace the wrong with the correct header, and save the corrected `results.xmdf`.

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

### XDMF-Fehler falscher Simulationsverzeichnisse
Der `results.xdmf` enthält geospatially explizite Daten (z.B. von Strömungsgeschwindigkeit und Wassertiefe), die theoretisch direkt in *QGIS* mit dem *Crayfish* Plugin importiert werden können (lesen Sie mehr im {ref}`BASEMENT post-processing <qgis-imp-steps>` Abschnitt). Es gibt jedoch ein kleines Problem: QGIS kann aufgrund eines ungültigen Verzeichnisses abstürzen. Um es zu beheben:

1. Open `results.xdmf` in a text editor (e.g., {ref}`Notepad++ <npp>` on Windows).
1. Verwenden Sie das Find-and-Replace-Tool (`CTRL` + `H` Schlüssel in Notepad++), um Dateipfade vor `results_aux.h5` zu entfernen.
    * Search the `results_aux.h5` string and identify the path written in front of it (e.g., `C:\temp\`).
    * Find and replace that user path, for example: `Find` = `C:\temp\results_aux.h5` and `Replace with` = `results_aux.h5`.
1. Nachdem Sie alle Pfadereignisse im Dokument entfernt haben, speichern und schließen Sie `results.xdmf`.


Dieses Thema wird auch im [BASEMENT User Forum](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?id=5261)] diskutiert.
