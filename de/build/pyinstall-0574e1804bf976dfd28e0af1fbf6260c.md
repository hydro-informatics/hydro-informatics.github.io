---
description: Cross-platform Python Installationsanleitung mit conda, mamba, pip und venv, mit Anweisungen zur Einrichtung reproduzierbarer Umgebungen für geospatiale und wissenschaftliche Berechnung.
---

(install-python)=
# Python (Installation)

> "Der zen der florierenden Python-Projekte im Jahr 2025 ist *ein Dolmetscher pro Projekt* und *ein Werkzeug-Kette pro Aufgabe*. Master virtuelle Umgebungen zuerst; der Rest folgt natürlich."

Python 2 reached end‑of‑life in **January 2020** and is no longer shipped by mainstream Linux distributions or Windows installers. Today every actively maintained package—scientific, geospatial, or otherwise—supports **CPython ≥ 3.9**, with most libraries now testing against **Python 3.13**. Multiple interpreters can still coexist on the same machine (QGIS / ArcGIS Pro embeds its own 3.11, Nvidia CUDA ships one for PyTorch, etc.), but the modern way to insulate projects is through *lightweight* virtual environments created by `venv`, **pipx**, or *conda/mamba*.

Dieses Kapitel destilliert einen Workflow, der den in diesem E‐Book verwendeten Rechenstapel zuverlässig baut, unabhängig von der Plattform. Sie betont

* **`conda`/`mamba`** as a smooth cross-platofrm default solution,
* **`pip` + `venv`** for Linux/macOS (alternative; preferably use `mamba`),
* recent improvements in binary wheels for GDAL/Fiona/Shapely (pip on Windows is finally painless!), and
* sustainable ways to keep environments reproducible.

--

**Before you continue**, a fast-track, cross-platform workable Python installation including GDAL can be installed using our [project template](https://github.com/sschwindt/python-project-template/):

1. Install [mamba](https://mamba.readthedocs.io) for your platform.
2. Download our [environment.yml](https://github.com/sschwindt/python-project-template/blob/main/environment.yml).
3. Open a terminal (command promptline), navigate to the directory where the downloaded *environment.yml* lives, and create the environment:
   ```bash
   mamba env create -f environment.yml
   ```
4. Aktivieren Sie die Umwelt und führen Sie Python:
   ```bash
   mamba activate wrr-proj
   (wrr-proj) user@computer:$ python
   ```
5. Überprüfen Sie, ob die Installation von Geopaketen funktioniert (keine Fehlermeldung sollte auftreten):
   ```bash
   >>> from osgeo import gdal
   ```

6. Optionnally, if the check succeeded worked, exit python and pip-install flusstools within this `wrr-project` environment:
   ```bash
   >>> exit()
   (wrr-proj) user@computer:$ pip install flusstools
   ```

--

(pip-env)=
`pip`@ + `venv`

```{admonition} The advantage of virtual environments over system‑wide Python installations
:class: tip
Der *system-Interpreter* treibt Kern-Desktop-Tools an; das Ändern kann Ihr Betriebssystem brechen. Ein `venv` lebt ganz in Ihrem Heimatverzeichnis, wiegt < 50 MB und verschwindet mit einer einzigen `rm -rf`. Auch neuere Betriebssysteme, wie Linux Mint 22.1 oder jünger, lassen Sie keinen Benutzer `pip` in der systemweiten python-Umgebung installieren.
```


(pip-quick)=
### Schnellstart (Linux Mint/Ubuntu 22.04 LTS oder später)

Installation neuer Dolmetscher
```
$ sudo apt update && sudo apt install python3 python3-venv python3-dev build-essential libgdal-dev gdal-bin
```

Moderne Debian/Ubuntu-Repositories Paket CPython 3. Die zusätzlichen *dev*-Header werden für Räder benötigt, die noch C‐Erweiterungen zu installieren Zeit kompilieren.

Erstellen & Aktivieren einer Umgebung

```bash
$ python3 -m venv ~/venvs/vflussenv
$ source ~/venvs/vflussenv/bin/activate
```

Ein `venv` erbt nichts vom System außer dem Dolmetscher binär.


Kernwerkzeuge aufrüsten

```bash
(vflussenv) $ python -m pip install --upgrade pip wheel setuptools
```

`pip 24.x` bundles the new *repair wheel* feature that fixes many‑linux and macOS wheels on the fly.


• Anforderungen installieren

For data analysis [without the geospatial GDAL library, download this requirements.txt file](https://github.com/sschwindt/sample-data/blob/main/python-env/requirements.txt). Otherwise, to [include libraries for geospatial data analysis, download this requirements.txt](https://github.com/Ecohydraulics/flusstools-pckg/raw/refs/heads/main/requirements.txt). Install the requirements.txt file into a new environment called `vflussenv' as follows.

```bash
(vflussenv) $ pip install -r requirements.txt
```

Binäre Räder für GDAL, Rasterio, Fiona und Shapely sind seit **2024‐10* auf PyPI verfügbar, so dass keine externe PPA mehr benötigt wird.

```{admonition} python vs. python3
:class: note
All mainstream distros now point the `python` symlink to Python3. If `python --version` still prints *Python 2.x* you are on an outdated system; always call the full `python3` binary instead.
```

flusstools installieren


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
Â `conda` / `mamba` - empfohlen unter Windows 11 & plattformübergreifende Datenwissenschaft

```{admonition} Choose *mamba* for speed
:class: hint
[`mamba`](https://github.com/mamba-org/mamba) is a drop‑in replacement for `conda` written in C++; it resolves environments 10-100x faster.
```

(pip-vs-conda)=
### 2025 Status von GDAL unter Windows

* 2024‑10: **gdal‑3.9.0‑cp311‑win_amd64.whl** landed on PyPI > pure‑`pip` installs finally work on Windows.
* However, large geospatial stacks (Proj, GEOS, HDF5, NetCDF) are still easier via the **conda‑forge** channel.
* Use `pip` only when you *must* keep the environment minimal.

(conda-quick)=
### Quick guide (Anaconda / Miniforge)

1. Install **Miniforge 4** (lighter than Anaconda, defaults to conda‑forge) -- refer to the installation instructions on the developer's [website](https://conda-forge.org/download/).
2. Get the flusstools [environment.yml](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/refs/heads/main/environment.yml) and use it to create the conda `flussenv` (takes a couple of minutes):
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
## Install extra packages with `pip`

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
Do **not** use the `--user` flag inside a virtual or conda environment; it bypasses the environment and pollutes your home directory.
```

### Bulk install

E‐Book-Beispiele stützen sich auf den folgenden wissenschaftlichen Stack (bereits in den bereitgestellten *quirements.txt* enthalten):

* numpy, pandas, scipy, matplotlib, seaborn
* geopandas, formell, rasterio, rasterstats, laspy
* networkx, openpyxl, tabulate

Installieren Sie sie manuell mit:

```bash
(vflussenv) pip install numpy pandas geopandas rasterio rasterstats laspy networkx openpyxl tabulate
```

--

(ipython-config)=
Installieren Sie Jupyter Kernel

```bash
(vflussenv) pip install ipykernel jupyterlab
(vflussenv) python -m ipykernel install --user --name vfluss_kernel
```
Wählen Sie **vfluss kernel** aus *Kernel > Kernel* innerhalb von JupyterLab ändern.


--

/ Umgebungen aktualisieren

### Virtuelle Umgebung aktualisieren (venv)

nice—virtualenv makes this straightforward. here’s a **robust in-place upgrade** flow that keeps your current venv (`vflussenv`) and focuses on **JupyterLab** + **Jupyter Book**. no conda, no YAML edits.

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

* Start by upgrading the **roots** (e.g., `pip install -U jupyterlab jupyter-book nbclient nbconvert`) and retry.
* If the error names a specific pin in your `requirements.txt`, relax **just that** one (or delete the line) and rerun.
* If you mixed editable/VCS installs, upgrade them individually: `pip install -U git+https://...`.
* Worst case: roll back to your snapshot:

  ```bash
  pip install -r requirements-YYYYMMDD.txt
  ```
````


### Update conda env

```{admonition} Conda vs. mamba
:class: note

If you used `mamba`, prefer the `mamba` commands -- they are *drop-in*.
```

**1. Erstellen Sie einen Snapshot des aktuellen Zustands (easy rollback)**

```bash
# exact conda specs
conda list --explicit > conda-specs-$(date +%Y%m%d).txt
# pip packages (if any were installed via pip)
python -m pip freeze > pip-freeze-$(date +%Y%m%d).txt
```

**2. Optional aber empfohlen: halten Sie Ihre aktuelle Python-Mollversion**

Dies verhindert einen unerwarteten Pythonsprung, der Konflikte verursachen kann. Adjust `3.11.*` an was auch immer `python --version`@ zeigt:

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

* Try a targeted update first for big libraries (e.g., `mamba update pandas numpy scipy -c conda-forge`), then `--all`.
* If you really need to upgrade Python, do it explicitly (e.g., `conda install python=3.12.* -c conda-forge`) and then `update --all`.
* If you mixed pip/conda heavily and get conflicts, consider keeping scientific stack (NumPy/SciPy/PyTorch/etc.) on conda-forge and apps/utilities via pip.

```


(ide-setup)=
Verwendung der Umwelt in IDEs

### JupyterLab

```bash
(vflussenv) jupyter lab
```

Geben Sie Ihren Browser an `https://hydro-informatics.com/lab`. Schalten Sie Kernel über das *Kernel* Menü.

### PyCharm

* **File > Settings > Python Interpreter > Add > Existing** > pick `~/venvs/vflussenv/bin/python` (Linux) or `%USERPROFILE%\mambaforge\envs\flussenv\python.exe` (Windows).
* Enable *Sync Python packaging tools* so that `pip install` inside PyCharm’s terminal updates the interpreter list.

--

(Remove-env)=
Umwelt entleeren

* **venv***: `rm -rf ~/venvs/vflussenv`
**conda***: `conda env remove -n flussenv`

--

(install-python-summary)=
/ Installation unter der Linie

* Use **`python -m venv`** (`pipx` for CLI tools) unless a package *requires* C/C++ libraries that your OS can’t satisfy—then reach for **conda‑forge**.
* Windows users no longer *need* conda for GDAL, but conda remains the easiest path for a full geospatial data‑science stack.
* Pin exact package versions for archival projects; use `>=` pins for living research code.
* Never install packages with `sudo pip`; always work inside an isolated environment.
