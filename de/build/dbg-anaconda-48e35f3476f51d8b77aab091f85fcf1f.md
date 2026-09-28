---
description: Beheben Sie häufige Anaconda- und Conda-Probleme, einschließlich Änderungen bei der Umgebungserstellung, Fehler bei der Paketinstallation und Abhängigkeitskonflikte in Python-Umgebungen.
---

# Debugging Anaconda

Manchmal werden Pakete nicht wie gewünscht installiert (was zu Importfehlern führt, *Anaconda Navigator* verhält sich nicht wie erwartet oder startet überhaupt nicht). Diese Seite fasst Heilmittel für solche Probleme zusammen.

## Conda Umwelt Schöpfung nie beendet

**Phänomen**: Das Erstellen einer Conda-Umgebung mit und einer Umgebungsdatei (`conda env create -f environment.yml`) führt zum quasi-ewigen Laden, ohne dass die Umgebung auch nach mehreren Stunden installiert wird.

**Fix**: Before creating the environment, set the installation priority to strict (answer adapted from [https://stackoverflow.com/questions/63734508/stuck-at-solving-environment-on-anaconda](https://stackoverflow.com/questions/63734508/stuck-at-solving-environment-on-anaconda)):


```
conda config --set channel_priority strict
```


## Conda Package Installation fehlschlägt

**Phänomen**: Die Installation einer Python-Bibliothek oder eines Pakets über Anaconda Prompt schlägt fehl.

**Fix**: Mehrere Gründe können dazu führen, dass die Installation neuer Pakete in *Anaconda Prompt* oder *Linux* / *macOS* *Terminal* fehlschlägt:

* Stellen Sie sicher, dass Sie alle * Python *-abhängigen Anwendungen (z. B. * Jupyter * oder *PyCharm *) vor der Installation schließen.
* Konfliktlösung aktiviert:
	- Warten Sie, bis Konflikte analysiert (und gelöst) werden
	- Enter `conda update conda`
	- Enter `conda update anaconda`
	- Neustart *Terminal* oder *Anaconda Prompt*
	- Versuchen Sie, das angeforderte Paket erneut zu installieren.



## *Anaconda Navigator* startet nicht

Die häufigsten Probleme für *Anaconda *, die nicht starten, sind im [Entwickler docs](https://docs.anaconda.com/anaconda/navigator/troubleshooting/)] aufgeführt und umfassen:

* Delete a potentially corrupted `.condarc` file. To do that, open *Anaconda Prompt* (on *Windows*) or *Terminal* (on *Linux* or *macOS*) and enter:
	- `conda info` um zu erfahren, wo sich die `.condarc` Datei befindet (auf *Windows* typischerweise `C:\Users\Username`),
	- Öffnen Sie das angegebene Verzeichnis (z.B. in *Windows* explorer),
	- Löschen Sie die `.condarc`-Datei.
* Versuchen Sie, den *Anaconda Navigator* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) zu starten, indem Sie `anaconda-navigator` eingeben.
* Beheben Sie Perfmissionsprobleme, indem Sie das `.continuum`-Verzeichnis löschen:
	- *Windows*: Öffnen Sie *Anaconda Prompt* und führen Sie `rd /s .continuum`
	- *Linux* / *macOS*: Öffnen Sie *Terminal* und führen Sie `rm -rf ~/.continuum`
* Aktualisieren Sie *Anaconda Navigator* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*), indem Sie `conda update anaconda-navigator`
* *Anaconda Navigator* aus *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) neu installieren, indem Sie:
	- `conda remove anaconda-navigator`
	- `conda install anaconda-navigator`
* Setzen Sie die *Anaconda Navigator*-Konfiguration aus *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) zurück, indem Sie `anaconda-navigator --reset` ausführen (Achtung: dies kann destruktiv sein).

Andere Bug-Fixes, die nicht auf der oben genannten Website des Entwicklers aufgeführt sind, sind:
* *conda* aus *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) neu initialisieren, indem Sie `conda init` ausführen. Dann schließen und wieder öffnen *Anaconda Prompt * (oder *Terminal *).
* Aktualisieren Sie *conda* und *Anaconda Navigator* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) als root:
	- `activate root`
	- `conda update -n root conda`
	- `conda update --all`
	- `conda update anaconda-navigator`
* *PyQt5* aus *Anaconda Prompt* neu installieren (oder *Linux* / *macOS* *Terminal*):
	- `pip uninstall PyQt5`
	- `pip install PyQt5`
	- `pip install pyqtwebengine`


## Große Speichergröße von *Anaconda*

Die *Anaconda* *base*-Umgebung enthält viele vorinstallierte Pakete und kann in der Größenordnung von vielen Gigabyte sehr speicherintensiv sein. Jede neue Umgebung, die produziert wird, kann die gleiche Größe haben und mehrere *conda * -Umgebungen können Ihre Festplatte blockieren. Auch hier gibt es einige Lösungen:

* Erstellen Sie leichte Umgebungen mit [*Miniconda*](https://docs.conda.io/en/latest/miniconda.html)].
* Säubern Sie Tarballs und unnötige Paketinstallationsdateien mit *Anaconda Prompt* oder *Linux* / *macOS* *Terminal*:
    + Aggressive Säuberung: `conda clean --all` (lesen Sie mehr im [Entwickler-Docs](https://docs.conda.io/projects/conda/en/latest/commands/clean.html)].
    + Konservative Säuberung: `conda clean -tipsy`


## Kann nicht finden ... Weg

In *Anaconda Prompt* or *Linux* / *macOS* *Terminal* run `conda init` and restart the application.
