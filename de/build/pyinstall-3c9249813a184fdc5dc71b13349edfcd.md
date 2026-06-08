---
description: Cross-platform Python Installationsanleitung mit conda, mamba, pip und venv, mit Anweisungen zur Einrichtung reproduzierbarer Umgebungen für geospatiale und wissenschaftliche Berechnung.
---

(install-python)=
# Python (Installation)

> "Der zen der florierenden Python-Projekte im Jahr 2025 ist *ein Dolmetscher pro Projekt* und *ein Werkzeug-Kette pro Aufgabe*. Master virtuelle Umgebungen zuerst; der Rest folgt natürlich."

Python 2 erreichte End‐of-life in **Januar 2020** und wird nicht mehr von Mainstream Linux Distributionen oder Windows-Installatoren versendet. Heute unterstützt jedes aktiv gepflegte Paket –wissenschaftlich, geospatial oder anderweitig – **CPython ≥ 3.9**, wobei die meisten Bibliotheken nun gegen **Python 3.13** testen. Mehrere Dolmetscher können noch auf der gleichen Maschine koexistieren (QGIS / ArcGIS Pro embeds seine eigenen 3.11, Nvidia CUDA Schiffe ein für PyTorch, etc.), aber die moderne Art, Projekte zu isolieren ist durch * leichte* virtuelle Umgebungen erstellt von `venv`, **pipx*, oder *conda/mamba*.

Dieses Kapitel destilliert einen Workflow, der den in diesem E‐Book verwendeten Rechenstapel zuverlässig baut, unabhängig von der Plattform. Sie betont

* **`conda`/`mamba`** als glatte Cross-Pultofrm-Standardlösung,
* **`pip` + `venv`** für Linux/macOS (alternativ; vorzugsweise unter`mamba`)
* jüngste Verbesserungen bei binären Rädern für GDAL/Fiona/Shapely (Pip unter Windows ist endlich schmerzlos) und
* nachhaltige Möglichkeiten, die Umwelt reproduzierbar zu halten.

--

**Bevor Sie fortfahren*, eine schnelle, plattformübergreifende, funktionsfähige Python-Installation inklusive GDAL kann mit unserem [Projekt Template](https://github.com/sschwindt/python-project-template/):

1. Installieren Sie [mamba](https://mamba.readthedocs.io) für Ihre Plattform.
2. Laden Sie unsere [environment.yml](https://github.com/sschwindt/python-project-template/blob/main/environment.yml).
3. Öffnen Sie ein Terminal (Befehlsaufforderung), navigieren Sie in das Verzeichnis, in dem das heruntergeladene *Umgebung. yml* lebt und schafft die Umgebung:
   ```bash
   mamba env create -f environment.yml
   ```
4. Aktivieren Sie die Umwelt und führen Sie Python:
   ```bash
   mamba activate wrr-proj
   (wrr-proj) user@computer:$ python
   ```
5. Prüfen Sie, ob die Installation von Geopaketen funktioniert hat (keine Fehlermeldung sollte auftreten):
   ```bash
   >>> from osgeo import gdal
   ```

6. Optional, wenn die Prüfung erfolgreich funktioniert, verlassen python und pip-install flusstools in dieser `wrr-project`Umgebung:
   ```bash
   >>> exit()
   (wrr-proj) user@computer:$ pip install flusstools
   ```

--

(pip-env)=
## `pip` + `venv` 

```{admonition} The advantage of virtual environments over system‑wide Python installations
:class: tip
Der *system-Interpreter* treibt Kern-Desktop-Tools an; das Ändern kann Ihr Betriebssystem brechen. Ein `venv` lebt ganz in Ihrem Heimatverzeichnis, wiegt < 50 MB und verschwindet mit einer einzigen `rm -rf`. Auch neuere Betriebssysteme, wie Linux Mint 22.1 oder jünger, lassen Sie keinen Benutzer `pip` in der systemweiten python-Umgebung installieren.
```


(pip-quick)=
### Schnellstart (Linux Mint/Ubuntu 22.04 LTS oder später)

#### Neueste Dolmetscher installieren
```
$ sudo apt update && sudo apt install python3 python3-venv python3-dev build-essential libgdal-dev gdal-bin
```

Moderne Debian/Ubuntu-Repositories Paket CPython 3. Die zusätzlichen *dev*-Header werden für Räder benötigt, die noch C‐Erweiterungen zu installieren Zeit kompilieren.

#### Erstellen & aktivieren einer Umgebung

```bash
$ python3 -m venv ~/venvs/vflussenv
$ source ~/venvs/vflussenv/bin/activate
```

Ein `venv` erbt nichts vom System außer dem Dolmetscher binär.


#### Kernwerkzeuge aktualisieren

```bash
(vflussenv) $ python -m pip install --upgrade pip wheel setuptools
```

`pip 24.x`bündelt das neue *Reparaturrad*-Feature, das viele‐linux- und macOS-Räder auf der Fliege fixiert.


#### Anforderungen an die Installation

Für die Datenanalyse [ohne die geospatiale GDAL-Bibliothek, laden Sie diese Anforderungen.txt file](https://github.com/sschwindt/sample-data/blob/main/python-env/requirements.txt). Ansonsten, um [inklusive Bibliotheken für die Geospatial-Datenanalyse, laden Sie diese Anforderungen.txt](https://github.com/Ecohydraulics/flusstools-pckg/raw/refs/heads/main/requirements.txt). Installieren Sie die Requirements.txt-Datei in eine neue Umgebung namens `vflussenv' wie folgt.

```bash
(vflussenv) $ pip install -r requirements.txt
```

Binäre Räder für GDAL, Rasterio, Fiona und Shapely sind seit **2024‐10* auf PyPI verfügbar, so dass keine externe PPA mehr benötigt wird.

```{admonition} python vs. python3
:class: note
Alle Mainstream Distros weisen nun den `python` symlink auf Python3 hin. Wenn `python --version` noch gedruckt *Python 2.x* Sie sind auf einem veralteten System; immer rufen Sie die volle `python3` Binär statt.
```

#### flusstools installieren


```bash
(vflussenv) $ pip install flusstools
```

Testen Sie es:

```bash
(vflussenv) $ python
>>> import flusstools as ft
```

--

(conda-env)=
## `conda` / `mamba` - empfohlen unter Windows 11 & plattformübergreifende Datenwissenschaft

```{admonition} Choose *mamba* for speed
:class: hint
[`mamba`](https://github.com/mamba-org/mamba) is a drop‑in replacement for `conda` written in C++; it resolves environments 10-100x faster.
```

(pip-vs-conda)=
### 2025 Status von GDAL unter Windows

* 2024‐10: **gdal‐3.9.0‐cp311‐win amd64.whl** landete auf PyPI > pure‐`pip` installiert schließlich unter Windows.
* Über den **conda‐forge** Kanal sind jedoch große geospatiale Stacks (Proj, GEOS, HDF5, NetCDF) noch einfacher.
* Verwenden Sie `pip` nur, wenn Sie *must* die Umgebung minimal halten.

(conda-quick)=
### Quick guide (Anaconda / Miniforge)

1. Installieren Sie **Miniforge 4** (heller als Anaconda, defaults to conda‐forge) -- verweisen Sie auf die Installationsanweisungen des Entwicklers [website](https://conda-forge.org/download/).
2. Holen Sie sich die flusstools [environment.yml](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/refs/heads/main/environment.yml) und erstellen Sie die conda `flussenv` (wird ein paar Minuten gebraucht):
    ```bash
    conda env create -f environment.yml
    ```
3. Aktivieren Sie `flussenv` und installieren Sie flusstools, das ist ein rein PyPi-hosted Paket:
    ```bash
    conda activate flussenv
    pip install flusstools
    ```
4. Fügen Sie einen Jupyter Kernel hinzu:
    ```bash
    ipython kernel install --user --name fluss_kernel
    ```

--

(install-pckg)=
## Installieren Sie zusätzliche Pakete mit `pip`

Mehr als **500 000** Projekte leben heute auf *PyPI*. Basissyntax:

````{tab-set}
```{tab-item} Linux/macOS (venv)
(vflussenv) $ pip install seaborn
```
```{tab-item} Windows (conda env)
(flussenv) > pip install seaborn
```
`````

```{note}
Verwenden Sie die `--user`-Flag innerhalb einer virtuellen oder conda-Umgebung, um die Umgebung zu umgehen und Ihr Home-Verzeichnis zu verschmutzen.
```

### Bulk install

E‐Book-Beispiele stützen sich auf den folgenden wissenschaftlichen Stack (bereits in den bereitgestellten *quirements.txt* enthalten):

* numpy, pandas, scipy, matplotlib, seaborn
* geopandas, formell, rasterio, rasterstats, laspy
* Networkx, openpyxl, tabulate

Installieren Sie sie manuell mit:

```bash
(vflussenv) pip install numpy pandas geopandas rasterio rasterstats laspy networkx openpyxl tabulate
```

--

(ipython-config)=
## Jupyter Kernel installieren

```bash
(vflussenv) pip install ipykernel jupyterlab
(vflussenv) python -m ipykernel install --user --name vfluss_kernel
```
Wählen Sie **vfluss kernel** aus *Kernel > Kernel* innerhalb von JupyterLab ändern.


--

## Umgebungen aktualisieren

### Virtuelle Umgebung aktualisieren (venv)

schön-virtualenv macht das einfach. Hier ist ein **robust-in-place-Upgrade**-Stream, der Ihren aktuellen venv (`vflussenv`) hält und sich auf **JupyterLab* + **Jupyter Book** konzentriert. no conda, no YAML edits.

**1. Aktivieren und Snapshot für einfaches Rollback**

```bash
# activate your venv if not already
source vflussenv/bin/activate

# snapshot current state for rollback
pip freeze > requirements-$(date +%Y%m%d).txt
```

**2. Stellen Sie sicher, dass die Build-Toolchain aktuell ist*

```bash
pip install -U pip setuptools wheel
```

**3. Vorausschau veraltete Pakete**

```bash
pip list --outdated
```

**4. Upgrade aller Pakete (zwei Optionen)**

`````{tab-set}
````{tab-item} Option A -- safe loop (exhaustive)

Upgradet jedes *pip-managed*-Paket mit Ausnahme direkter VCS/URL-Installationen.

```bash
python - <<'PY'
```

```python
import json, subprocess, sys
# get outdated packages in JSON
out = subprocess.check_output(
    [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
    text=True
)
# take just the package names
names = [pkg["name"] for pkg in json.loads(out)]

# optional: don't re-upgrade the bootstrap tools every loop
skip = {"pip", "setuptools", "wheel"}
for name in names:
    if name in skip:
        continue
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", name])
PY
```

````

````{tab-item} Option B -- "requirements with >="

Diese Option bewahrt ein Backup und behandelt macOS/Linux `sed`.

```bash
# start from a clean freeze
pip freeze > requirements.txt

# Linux:
sed -i 's/==/>=/' requirements.txt
# macOS (BSD sed):
# sed -i '' 's/==/>=/' requirements.txt

# upgrade per the relaxed pins
pip install --upgrade -r requirements.txt

````
`````


**5. Optional das neue Set **

```bash
pip freeze > requirements-upgraded-$(date +%Y%m%d).txt
```

**6. Verify*

```bash
jupyter lab --version
jupyter-book --version
python -c "import sys; print(sys.version)"
```

**7. Aufräumen**

Saubere alte Build-Caches, um Speicherplatz zu sparen:

```bash
pip cache purge
```


````{admonition} Conflicts / "ResolutionImpossible"
:class: note

* Beginnen Sie mit dem Upgrade der **roots* (z.B. `pip install -U jupyterlab jupyter-book nbclient nbconvert`) und Retry.
* Wenn der Fehler einen bestimmten Pin in Ihrem `requirements.txt`, entspannen Sie ** just that** ein (oder löschen Sie die Zeile) und rerun.
* Wenn Sie Editable/VCS-Installationen gemischt haben, aktualisieren Sie diese individuell: `pip install -U git+https://...`.
* Worst Case: Zurück zu Ihrem Snapshot:

  ```bash
  pip install -r requirements-YYYYMMDD.txt
  ```
````


### Update conda env

```{admonition} Conda vs. mamba
:class: note

Wenn Sie `mamba` verwendet haben, bevorzugen Sie die `mamba`-Befehle -- sie sind *drop-in*.
```

**1. Erstellen Sie einen Snapshot des aktuellen Zustands (easy rollback)**

```bash
# exact conda specs
conda list --explicit > conda-specs-$(date +%Y%m%d).txt
# pip packages (if any were installed via pip)
python -m pip freeze > pip-freeze-$(date +%Y%m%d).txt
```

**2. Optional aber empfohlen: halten Sie Ihre aktuelle Python-Mollversion**

Dies verhindert einen unerwarteten Pythonsprung, der Konflikte verursachen kann. Adjust `3.11.*` an was auch immer `python --version` zeigt:

```bash
python --version
# pin to current minor while updating other deps
conda install "python=3.11.*" -c conda-forge
```

**3. Stellen Sie sicher, dass Ihr Soldat aktuell ist**

```bash
# update conda itself (and mamba if you have it) in base
conda activate base
conda update -n base -c conda-forge conda
# optional: if you use mamba
conda install -n base -c conda-forge mamba
conda activate vflussenv
```

**4. Alle Conda-Pakete aktualisieren**

Verwenden Sie strenge conda-forge für Konsistenz (um Ihren YAML nicht zu ändern).

```bash
# with mamba (faster)
mamba update --all -c conda-forge --yes

# or with conda
conda update --all -c conda-forge --yes
```

**5. Wenn Sie *pip* für einige Pakete verwendet haben, aktualisieren Sie diese auch**

Nur dies tun **nach** das Conda-Update. Dies hält conda für Kernbibliotheken verantwortlich.

```bash
# show what’s outdated (pip-managed only)
python -m pip list --outdated

# upgrade all pip-managed packages (safer loop than xargs)
python - <<'PY'
import subprocess, sys
out = subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated", "--format=freeze"], text=True)
pkgs = [line.split("==")[0] for line in out.splitlines() if "@" not in line]
for p in pkgs:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", p])
PY
```

**6. Saubere Kälber**

```bash
conda clean -a -y
```

**7. Versionen überprüfen*

```bash
jupyter lab --version
jupyter-book --version
python -c "import sys, jupyterlab; print('py', sys.version);"
```

```{admonition} If the solver struggled...
:class: tip

* Probieren Sie zuerst ein gezieltes Update für große Bibliotheken (z.B. `mamba update pandas numpy scipy -c conda-forge`), dann `--all`.
* Wenn Sie wirklich Python aktualisieren müssen, tun Sie es explizit (z.B. `conda install python=3.12.* -c conda-forge`) und dann `update --all`.
* Wenn Sie pip/conda stark gemischt und Konflikte erhalten, halten Sie wissenschaftliche Stacks (NumPy/SciPy/PyTorch/etc.) auf conda-forge und apps/utilities per pip.

```


(ide-setup)=
## Nutzung der Umwelt in IDEs

### JupyterLab

```bash
(vflussenv) jupyter lab
```

Geben Sie Ihren Browser an `https://hydro-informatics.com/lab`. Schalten Sie Kernel über das *Kernel* Menü.

### PyCharm

* **File > Einstellungen > Python Interpreter > Add > Existing** > Pick `~/venvs/vflussenv/bin/python` (Linux) oder `%USERPROFILE%\mambaforge\envs\flussenv\python.exe` (Windows).
* Aktivieren Sie *Sync Python Verpackungstools*, so dass `pip install` innerhalb des Terminals von PyCharm die Dolmetscherliste aktualisiert.

--

(remove-env)=
## Löschen von Umgebungen

* **venv***: `rm -rf ~/venvs/vflussenv`
* **conda***: `conda env remove -n flussenv`

--

(install-python-summary)=
## Installation unter der Linie

* Verwenden Sie **`python -m venv`* (`pipx` für CLI-Tools) es sei denn, ein Paket * benötigt* C/C++-Bibliotheken, die Ihr Betriebssystem nicht erfüllen kann – dann erreichen Sie **conda‐forge***.
* Windows-Benutzer nicht mehr *notiert* conda für GDAL, aber conda bleibt der einfachste Weg für einen vollen Geospatial Data‐science Stack.
* Pin genaue Paketversionen für Archivprojekte; verwenden Sie `>=`pins for living research code.
* Installieren Sie niemals Pakete mit `sudo pip`; arbeiten Sie immer in einer isolierten Umgebung.
