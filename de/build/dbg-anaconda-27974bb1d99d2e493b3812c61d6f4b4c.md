---
description: Behebt gemeinsame Anaconda- und Conda-Probleme, einschließlich Umwelterstellung hängt, Paketinstallationsausfälle und Abhängigkeitskonflikte in Python-Umgebungen.
---

# Debugging Anaconda

Manchmal werden Pakete nicht wie gewünscht installiert (Ergebnis bei Importfehlern, *Anaconda Navigator* ist nicht wie erwartet oder startet überhaupt nicht. Diese Seite fasst Abhilfe für solche Probleme zusammen.

## Conda Umwelt Schöpfung nie beendet

**Phenomenon**: Die Schaffung einer conda-Umgebung mit und Umweltdatei (`conda env create -f environment.yml`) führt zu quasi-eterner Belastung, ohne dass die Umwelt auch nach mehreren Stunden installiert wird.

**Fix**: Before creating the environment, set the installation priority to strict (answer adapted from [https://stackoverflow.com/questions/63734508/stuck-at-solving-environment-on-anaconda](https://stackoverflow.com/questions/63734508/stuck-at-solving-environment-on-anaconda)):


```
conda config --set channel_priority strict
```


## Conda-Paketinstallation versagt

**Phenomenon**: Installation einer Python-Bibliothek oder eines Pakets durch Anaconda Prompt scheitert.

**Fix*: Mehrere Gründe können dazu führen, dass die Installation neuer Pakete in *Anaconda Prompt* oder *Linux* / *macOS* *Terminal* ausfällt:

* Stellen Sie sicher, alle *Python*-abhängigen Anwendungen (z.B. *Jupyter* oder *PyCharm*) vor der Installation zu schließen.
* Konfliktlösung aktiviert:
- Warten Sie, bis Konflikte beschnitten werden (und gelöst)
- Geben Sie `conda update conda`
- Geben Sie `conda update anaconda`
- Neustart *Terminal* oder *Anaconda Prompt*
- Versuchen Sie, das Paket neu zu installieren.



## *Anaconda Navigator* startet nicht

Die häufigsten Probleme für *Anaconda*, die nicht gestartet werden, sind in der [developer's docs](https://docs.anaconda.com/anaconda/navigator/troubleshooting/) aufgeführt und beinhalten:

* Löschen einer möglicherweise beschädigten `.condarc`-Datei. Öffnen Sie dazu *Anaconda Prompt* (auf *Windows*) oder *Terminal* (auf *Linux* oder *macOS*) und geben Sie Folgendes ein:
- `conda info` um zu erfahren, wo sich die `.condarc`-Datei befindet (auf *Windows* typischerweise `C:\Users\Username`),
- Öffnen Sie das angezeigte Verzeichnis (z.B. in *Windows* Explorer),
- Löschen Sie die `.condarc`-Datei.
* Starten Sie *Anaconda Navigator* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) durch Eingabe von `anaconda-navigator`.
* Fehlerbehebung durch Löschen des `.continuum`-Verzeichnisses:
- *Windows*: Öffnen Sie *Anaconda Prompt* und führen Sie `rd /s .continuum`
- *Linux* / *macOS*: Öffnen Sie *Terminal* und führen Sie `rm -rf ~/.continuum`
* Update *Anaconda Navigator* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) durch Eingabe von `conda update anaconda-navigator`
* Re-installieren *Anaconda Navigator* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) durch Laufen:
- `conda remove anaconda-navigator`
- `conda install anaconda-navigator`
* Zurücksetzen *Anaconda Navigator* Konfiguration von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) durch Laufen `anaconda-navigator --reset` (Beachtung: das kann destruktiv sein).

Andere, Bug-fixes, nicht auf der oben genannten Entwickler-Website aufgeführt sind:
* Re-initialize *conda* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) von run`conda init`. Dann schließen und wieder öffnen *Anaconda Prompt* (oder *Terminal*).
* Update *conda* und *Anaconda Navigator* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*) als root:
- `activate root`
- `conda update -n root conda`
- `conda update --all`
-`conda update anaconda-navigator`
* Reinstallieren *PyQt5* von *Anaconda Prompt* (oder *Linux* / *macOS* *Terminal*):
- `pip uninstall PyQt5`
- `pip install PyQt5`
- `pip install pyqtwebengine`


## Große Speichergröße von *Anaconda*

Die *Anaconda* *base* Umgebung kommt mit vielen vorinstallierten Paketen und kann in der Größenordnung vieler Gigabyte sehr lagerstark sein. Jede neue Umgebung, die produziert wird, kann die gleiche Größe und mehrere *conda* Umgebungen können Ihre Festplatte versperren. Auch hier gibt es einige Lösungen:

* Erstellen Sie leichte Umgebungen mit [*Miniconda*](https://docs.conda.io/en/latest/miniconda.html).
* Clean tarballs eine unnötige Paketinstallationsdateien mit *Anaconda Prompt* oder *Linux* / *macOS* *Terminal*:
+ Aggressive Aufräumung: `conda clean --all` (weitere Informationen finden Sie in der [developer's docs](https://docs.conda.io/projects/conda/en/latest/commands/clean.html)).
+ Konservative Reinigung: `conda clean -tipsy`


## Kann nicht finden... Pfad

In *Anaconda Prompt* oder *Linux* / *macOS* *Terminal* laufen `conda init` und starten Sie die Anwendung neu.
