---
description: Plattformübergreifendes Python-Installationshandbuch mit conda, mamba, pip und venv mit Anweisungen zum Einrichten reproduzierbarer Umgebungen für geospatiales und wissenschaftliches Computing.
---

(install-python)=
# Python (Installation)

„Das Zen blühender Python-Projekte im Jahr 2025 ist *ein Interpreter pro Projekt* und *eine Werkzeugkette pro Aufgabe*. Beherrsche zuerst virtuelle Umgebungen; der Rest folgt natürlich.

Python 2 erreichte das Ende der Lebensdauer im Januar 2020 und wird nicht mehr von Mainstream-Linux-Distributionen oder Windows-Installationsprogrammen ausgeliefert. Heute unterstützt jedes aktiv gepflegte Paket - wissenschaftlich, geospatial oder anderweitig - **CPython ≥ 3.9**, wobei die meisten Bibliotheken jetzt gegen **Python 3.13** testen. Mehrere Interpreter können immer noch auf derselben Maschine koexistieren (QGIS / ArcGIS Pro bettet seine eigene 3.11, Nvidia CUDA liefert eine für PyTorch, etc.), aber die moderne Art, Projekte zu isolieren, ist durch *leichte * virtuelle Umgebungen, die von `venv`, **pipx** oder *conda/mamba* erstellt wurden.

Dieses Kapitel destilliert einen Workflow, der den in diesem E-Book verwendeten Rechenstapel unabhängig von der Plattform zuverlässig erstellt. Er betont:

* **`conda`/`mamba`** als glatte Cross-Platofrm Standardlösung,
* **`pip` + `venv`** für Linux/macOS (Alternative; vorzugsweise `mamba` verwenden),
* jüngste Verbesserungen bei Binärrädern für GDAL / Fiona / Shapely (Pip unter Windows ist endlich schmerzlos!) und
* nachhaltige Wege, um Umgebungen reproduzierbar zu halten.

---

**Bevor Sie fortfahren**, kann eine schnelle, plattformübergreifende Python-Installation einschließlich GDAL mit unserer [Projektvorlage](https://github.com/sschwindt/python-project-template/)] installiert werden:

1. Installieren Sie [mamba](https://mamba.readthedocs.io) für Ihre Plattform].
2. Laden Sie unsere [environment.yml](https://github.com/sschwindt/python-project-template/blob/main/environment.yml)] herunter.
3. Öffnen Sie ein Terminal (Befehlsaufforderung), navigieren Sie zum Verzeichnis, in dem die heruntergeladene * Umgebung angezeigt wird. yml* lebt und schafft die Umwelt:
   ```bash
   mamba env create -f environment.yml
   ```
4. Aktivieren Sie die Umgebung und führen Sie Python aus:
   ```bash
   mamba activate wrr-proj
   (wrr-proj) user@computer:$ python
   ```
5. Überprüfen Sie, ob die Installation von Geopaketen funktioniert hat (es sollte keine Fehlermeldung auftreten):
   ```bash
   >>> from osgeo import gdal
   ```

6. Optionnally, if the check succeeded worked, exit python and pip-install flusstools within this `wrr-project` environment:
   ```bash
   >>> exit()
   (wrr-proj) user@computer:$ pip install flusstools
   ```

---

(pip-env)=
## `pip` + `venv`

```{admonition} The advantage of virtual environments over system‑wide Python installations
:class: tip
The *system interpreter* drives core desktop tools; changing it can break your OS. A `venv` lives entirely in your home directory, weighs <50 MB, and vanishes with a single `rm -rf`. Also, newer OS, like Linux Mint 22.1 or younger, do not let a user `pip` install anything in the system-wide python environment.
```


(pip-quick)=
### Schnellstart (Linux Mint/Ubuntu 22.04 LTS oder höher)

#### Installieren Sie den neuesten Interpreter
```
$ sudo apt update && sudo apt install python3 python3-venv python3-dev build-essential libgdal-dev gdal-bin
```

Moderne Debian/Ubuntu-Repositories verpacken bereits CPython 3. Die zusätzlichen *dev*-Header werden für Räder benötigt, die C‐Erweiterungen zum Zeitpunkt der Installation noch kompilieren.

#### Erstellen und Aktivieren einer Umgebung

```bash
$ python3 -m venv ~/venvs/vflussenv
$ source ~/venvs/vflussenv/bin/activate
```

A `venv` inherits nothing from the system except the interpreter binary.


#### Upgrade Core Tools

```bash
(vflussenv) $ python -m pip install --upgrade pip wheel setuptools
```

`pip 24.x` bundles the new *repair wheel* feature that fixes many‑linux and macOS wheels on the fly.


#### Einbauvorschriften

Für die Datenanalyse [ohne die geospatial GDAL-Bibliothek, laden Sie diese requirements.txt file](https://github.com/sschwindt/sample-data/blob/main/python-env/requirements.txt) herunter. Andernfalls, um [Bibliotheken für die Geodatenanalyse einschließen], laden Sie diese requirements.txt](https://github.com/Ecohydraulics/flusstools-pckg/raw/refs/heads/main/requirements.txt) herunter. Installieren Sie die requirements.txt-Datei wie folgt in einer neuen Umgebung namens "vflussenv".

```bash
(vflussenv) $ pip install -r requirements.txt
```

Binärräder für GDAL, Rasterio, Fiona und Shapely sind seit **2024-10** auf PyPI verfügbar, so dass kein externes PPA mehr erforderlich ist.

```{admonition} python vs. python3
:class: note
All mainstream distros now point the `python` symlink to Python3. If `python --version` still prints *Python 2.x* you are on an outdated system; always call the full `python3` binary instead.
```

#### Fließwerkzeuge installieren


```bash
(vflussenv) $ pip install flusstools
```

Testen Sie es:

```bash
(vflussenv) $ python
>>> import flusstools as ft
```

---

(conda-env)=
## `conda` / `mamba` - empfohlen unter Windows 11 & plattformübergreifende Datenwissenschaft

```{admonition} Choose *mamba* for speed
:class: hint
[`mamba`](https://github.com/mamba-org/mamba) is a drop‑in replacement for `conda` written in C++; it resolves environments 10-100x faster.
```

(pip-vs-conda)=
### 2025 Status von GDAL unter Windows

* 2024‐10: **gdal‐3.9.0‐cp311‐win amd64.whl** landete auf PyPI > pure‐`pip`installationen funktionieren endlich unter Windows.
* Große Geospatial Stacks (Proj, GEOS, HDF5, NetCDF) sind jedoch noch einfacher über den **conda‐forge** Kanal.
* Use `pip` only when you *must* keep the environment minimal.

(conda-quick)=
### Quick Guide (Anaconda / Miniforge)

1. Installieren Sie **Miniforge 4** (leichter als Anaconda, standardmäßig auf conda-forge) - lesen Sie die Installationsanweisungen auf der Website des Entwicklers [website](https://conda-forge.org/download/)].
2. Holen Sie sich die flusstools [environment.yml](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/refs/heads/main/environment.yml)] und verwenden Sie es, um die conda `flussenv` zu erstellen (dauert ein paar Minuten):
    ```bash
    conda env create -f environment.yml
    ```
3. Aktivieren Sie `flussenv` und installieren Sie flusstools, ein rein PyPi-gehostetes Paket:
    ```bash
    conda activate flussenv
    pip install flusstools
    ```
4. Füge einen Jupyter-Kernel hinzu:
    ```bash
    ipython kernel install --user --name fluss_kernel
    ```

---

(install-pckg)=
## Install extra packages with `pip`

Mehr als **500 000** Projekte leben heute auf *PyPI*. Basissyntax:

````{tab-set}
```{tab-item} Linux/macOS (venv)
(vflussenv) $ pip install seaborn
```
```{tab-item} Windows (conda env)
(flussenv) > Pip install seaborn
```
`````

```{note}
Verwenden Sie das `--user`-Flag nicht in einer virtuellen oder Conda-Umgebung; es umgeht die Umgebung und verschmutzt Ihr Heimverzeichnis.
```

### Großanlage

E-Book-Beispiele beruhen auf dem folgenden wissenschaftlichen Stack (bereits in der bereitgestellten *requirements.txt* enthalten):

* numpy, pandas, scipy, matplotlib, seeborn.
* Geopandas, formbar, rasterio, rasterstats, laspy
* networkx, openpyxl, tabellarisch

Installieren Sie sie manuell mit:

```bash
(vflussenv) pip install numpy pandas geopandas rasterio rasterstats laspy networkx openpyxl tabulate
```

---

(ipython-config)=
## Installieren Sie Jupyter Kernel

```bash
(vflussenv) pip install ipykernel jupyterlab
(vflussenv) python -m ipykernel install --user --name vfluss_kernel
```
Wählen Sie **vfluss kernel** aus *Kernel > Kernel ändern* innerhalb von JupyterLab.


---

## Aktualisierung von Umgebungen

### Aktualisieren der virtuellen Umgebung (venv)

schön - virtualenv macht das einfach. Hier ist ein **robuster Upgrade-Flow, der Ihren aktuellen Venv (`vflussenv`) behält und sich auf **JupyterLab** + **Jupyter Book** konzentriert. keine Conda, keine YAML-Bearbeitungen.

**1. Aktivieren & Snapshot für einfaches Rollback**

```bash
# activate your venv if not already
source vflussenv/bin/activate

# snapshot current state for rollback
pip freeze > requirements-$(date +%Y%m%d).txt
```

**2. Stellen Sie sicher, dass die Build-Toolchain aktuell ist**

```bash
pip install -U pip setuptools wheel
```

**3. Alte Pakete anzeigen**

```bash
pip list --outdated
```

**4. Aktualisieren Sie alle Pakete (zwei Optionen)**

`````{tab-set}
````{tab-item} Option A -- safe loop (exhaustive)

Aktualisiert jedes * Pip-verwaltete * Paket, außer direkte VCS / URL-Installationen.

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

This option preserves a backup and handles macOS/Linux `sed` differences.

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


**5 Optional das neue Set anheften**

```bash
pip freeze > requirements-upgraded-$(date +%Y%m%d).txt
```

**6. Verifizieren**

```bash
jupyter lab --version
jupyter-book --version
python -c "import sys; print(sys.version)"
```

**7 Aufräumen**

Reinigen Sie alte Build-Caches, um Speicherplatz zu sparen:

```bash
pip cache purge
```


````{admonition} Conflicts / "ResolutionImpossible"
:class: note

* Beginnen Sie mit dem Upgrade der **roots** (z.B. `pip install -U jupyterlab jupyter-book nbclient nbconvert`) und wiederholen Sie es.
* If the error names a specific pin in your `requirements.txt`, relax **just that** one (or delete the line) and rerun.
* Wenn Sie editierbare/VCS-Installationen gemischt haben, aktualisieren Sie sie einzeln: `pip install -U git+https://...`.
* Worst case: rollen Sie zurück zu Ihrem Snapshot:

  ```bash
  pip install -r requirements-YYYYMMDD.txt
  ```
````


### Update conda env

```{admonition} Conda vs. mamba
:class: note

Wenn Sie `mamba` verwendet haben, bevorzugen Sie die `mamba`-Befehle - sie sind *drop-in *.
```

**1. Erstellen Sie eine Momentaufnahme des aktuellen Zustands (einfaches Rollback)**

```bash
# exact conda specs
conda list --explicit > conda-specs-$(date +%Y%m%d).txt
# pip packages (if any were installed via pip)
python -m pip freeze > pip-freeze-$(date +%Y%m%d).txt
```

**2. Optional, aber empfohlen: Behalten Sie Ihre aktuelle Python-Moll-Version **

Dies verhindert einen unerwarteten Python-Sprung, der Konflikte verursachen kann. Passen Sie `3.11.*` an was auch immer `python --version` zeigt:

```bash
python --version
# pin to current minor while updating other deps
conda install "python=3.11.*" -c conda-forge
```

**3. Stellen Sie sicher, dass Ihr Solver auf dem neuesten Stand ist**

```bash
# update conda itself (and mamba if you have it) in base
conda activate base
conda update -n base -c conda-forge conda
# optional: if you use mamba
conda install -n base -c conda-forge mamba
conda activate vflussenv
```

**4. Aktualisieren Sie alle Conda-Pakete**

Verwenden Sie strenge Conda-Schmiede für Konsistenz (um Ihre YAML nicht zu ändern).

```bash
# with mamba (faster)
mamba update --all -c conda-forge --yes

# or with conda
conda update --all -c conda-forge --yes
```

**5. Wenn Sie *pip* für einige Pakete verwendet haben, aktualisieren Sie diese auch**

Tun Sie dies nur **nach ** dem Conda-Update. Dies hält conda verantwortlich für Kernbibliotheken.

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

**6. Reine Caches**

```bash
conda clean -a -y
```

**7. Versionen überprüfen**

```bash
jupyter lab --version
jupyter-book --version
python -c "import sys, jupyterlab; print('py', sys.version);"
```

```{admonition} If the solver struggled...
:class: tip

* Versuchen Sie zuerst ein gezieltes Update für große Bibliotheken (z.B. `mamba update pandas numpy scipy -c conda-forge`), dann `--all`.
* Wenn Sie Python wirklich aktualisieren müssen, tun Sie es explizit (z.B. `conda install python=3.12.* -c conda-forge`) und dann `update --all`.
* Wenn Sie Pip / Conda stark gemischt haben und Konflikte bekommen, sollten Sie wissenschaftliche Stacks (NumPy / SciPy / PyTorch / etc.) auf Conda-Forge und Apps / Utilities über Pip halten.

```


(ide-setup)=
## Nutzung der Umwelt in IDEs

### JupyterLabor

```bash
(vflussenv) jupyter lab
```

Point your browser to `https://hydro-informatics.com/lab`. Switch kernels via the *Kernel* menu.

### PyCharm

* **Datei > Einstellungen > Python Interpreter > Add > Existing** > pick `~/venvs/vflussenv/bin/python` (Linux) oder `%USERPROFILE%\mambaforge\envs\flussenv\python.exe` (Windows).
* Aktivieren Sie *Sync Python Packaging Tools*, damit `pip install` im Terminal von PyCharm die Interpreterliste aktualisiert.

---

(remove-env)=
## Umgebungen löschen

* **venv**: `rm -rf ~/venvs/vflussenv`
* **conda**: `conda env remove -n flussenv`

---

(install-python-summary)=
## Installationsgrundlinie

* Verwenden Sie **`python -m venv`** (`pipx` für CLI-Tools), es sei denn, ein Paket *erfordert* C/C++-Bibliotheken, die Ihr Betriebssystem nicht erfüllen kann, und greifen Sie dann nach **conda‐forge**.
* Windows-Benutzer brauchen keine Conda mehr für GDAL, aber Conda bleibt der einfachste Weg für einen vollständigen geospatialen Data-Science-Stack.
* Pin exact package versions for archival projects; use `>=` pins for living research code.
* Installieren Sie niemals Pakete mit `sudo pip`; arbeiten Sie immer in einer isolierten Umgebung.
