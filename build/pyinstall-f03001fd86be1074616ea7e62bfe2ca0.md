(install-python)=
# Python (Installation)

> "The zen of thriving Python projects in 2025 is *one interpreter per project* and *one tool‑chain per task*. Master virtual environments first; the rest follows naturally."

Python 2 reached end‑of‑life in **January 2020** and is no longer shipped by mainstream Linux distributions or Windows installers. Today every actively maintained package—scientific, geospatial, or otherwise—supports **CPython ≥ 3.9**, with most libraries now testing against **Python 3.13**. Multiple interpreters can still coexist on the same machine (QGIS / ArcGIS Pro embeds its own 3.11, Nvidia CUDA ships one for PyTorch, etc.), but the modern way to insulate projects is through *lightweight* virtual environments created by `venv`, **pipx**, or *conda/mamba*.

This chapter distils a workflow that reliably builds the computational stack used throughout this e‑book, regardless of platform. It emphasises

* **`conda`/`mamba`** as a smooth cross-platofrm default solution,
* **`pip` + `venv`** for Linux/macOS (alternative; preferably use `mamba`),
* recent improvements in binary wheels for GDAL/Fiona/Shapely (pip on Windows is finally painless!), and
* sustainable ways to keep environments reproducible.

---

**Before you continue**, a fast-track, cross-platform workable Python installation including GDAL can be installed using our [project template](https://github.com/sschwindt/python-project-template/):

1. Install [mamba](https://mamba.readthedocs.io) for your platform.
2. Download our [environment.yml](https://github.com/sschwindt/python-project-template/blob/main/environment.yml).
3. Open a terminal (command promptline), navigate to the directory where the downloaded *environment.yml* lives, and create the environment:
   ```bash
   mamba env create -f environment.yml
   ```
4. Activate the environment and run Python:
   ```bash
   mamba activate wrr-proj
   (wrr-proj) user@computer:$ python
   ```
5. Check if the installation of geopackages worked (no error message should occur):
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
### Quick start (Linux Mint/Ubuntu 22.04 LTS or later)

#### Install newest interpreter
```
$ sudo apt update && sudo apt install python3 python3-venv python3-dev build-essential libgdal-dev gdal-bin
```

Modern Debian/Ubuntu repositories already package CPython 3. The extra *dev* headers are needed for wheels that still compile C‑extensions at install time.

#### Create & activate an environment

```bash
$ python3 -m venv ~/venvs/vflussenv
$ source ~/venvs/vflussenv/bin/activate
```

A `venv` inherits nothing from the system except the interpreter binary.


#### Upgrade core tools

```bash
(vflussenv) $ python -m pip install --upgrade pip wheel setuptools
```

`pip 24.x` bundles the new *repair wheel* feature that fixes many‑linux and macOS wheels on the fly.


#### Install requirements

For data analysis [without the geospatial GDAL library, download this requirements.txt file](https://github.com/sschwindt/sample-data/blob/main/python-env/requirements.txt). Otherwise, to [include libraries for geospatial data analysis, download this requirements.txt](https://github.com/Ecohydraulics/flusstools-pckg/raw/refs/heads/main/requirements.txt). Install the requirements.txt file into a new environment called `vflussenv' as follows.

```bash
(vflussenv) $ pip install -r requirements.txt
```

Binary wheels for GDAL, Rasterio, Fiona, and Shapely have been available on PyPI since **2024‑10**, so no external PPA is required anymore.

```{admonition} python vs. python3
:class: note
All mainstream distros now point the `python` symlink to Python3. If `python --version` still prints *Python 2.x* you are on an outdated system; always call the full `python3` binary instead.
```

#### Install flusstools


```bash
(vflussenv) $ pip install flusstools
```

Test it:

```bash
(vflussenv) $ python
>>> import flusstools as ft
```

---

(conda-env)=
## `conda` / `mamba` - recommended on Windows 11 & cross‑platform data science

```{admonition} Choose *mamba* for speed
:class: hint
[`mamba`](https://github.com/mamba-org/mamba) is a drop‑in replacement for `conda` written in C++; it resolves environments 10-100x faster.
```

(pip-vs-conda)=
### 2025 status of GDAL on Windows

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
3. Activate `flussenv` and install flusstools, which is a purely PyPi-hosted package:
    ```bash
    conda activate flussenv
    pip install flusstools
    ```
4. Add a Jupyter kernel:
    ```bash
    ipython kernel install --user --name fluss_kernel
    ```

---

(install-pckg)=
## Install extra packages with `pip`

More than **500 000** projects live on *PyPI* today. Basic syntax:

````{tab-set}
```{tab-item} Linux/macOS (venv)
(vflussenv) $ pip install seaborn
```
```{tab-item} Windows (conda env)
(flussen v) > pip install seaborn
```
`````

```{note}
Do **not** use the `--user` flag inside a virtual or conda environment; it bypasses the environment and pollutes your home directory.
```

### Bulk install

E‑book examples rely on the following scientific stack (already included in the provided *requirements.txt*):

* numpy, pandas, scipy, matplotlib, seaborn
* geopandas, shapely, rasterio, rasterstats, laspy
* networkx, openpyxl, tabulate

Install them manually with:

```bash
(vflussenv) pip install numpy pandas geopandas rasterio rasterstats laspy networkx openpyxl tabulate
```

---

(ipython-config)=
## Install Jupyter kernel

```bash
(vflussenv) pip install ipykernel jupyterlab
(vflussenv) python -m ipykernel install --user --name vfluss_kernel
```
Select **vfluss_kernel** from *Kernel > Change kernel* inside JupyterLab.


---

## Update environments

### Update virtual environment (venv)

nice—virtualenv makes this straightforward. here’s a **robust in-place upgrade** flow that keeps your current venv (`vflussenv`) and focuses on **JupyterLab** + **Jupyter Book**. no conda, no YAML edits.

**1. Activate & snapshot for easy rollback**

```bash
# activate your venv if not already
source vflussenv/bin/activate

# snapshot current state for rollback
pip freeze > requirements-$(date +%Y%m%d).txt
```

**2. Make sure the build toolchain is current**

```bash
pip install -U pip setuptools wheel
```

**3. Preview outdated packages**

```bash
pip list --outdated
```

**4. Upgrade all packages (two options)**

`````{tab-set}
````{tab-item} Option A -- safe loop (exhaustive)

Upgrades every *pip-managed* package except direct VCS/URL installs.

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


**5. Optionally, pin the new set**

```bash
pip freeze > requirements-upgraded-$(date +%Y%m%d).txt
```

**6. Verify**

```bash
jupyter lab --version
jupyter-book --version
python -c "import sys; print(sys.version)"
```

**7. Clean up**

Clean old build caches to save disk space:

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

I you used `mamba`, prefer the `mamba` commands -- they are *drop-in*.
```

**1. Create a snapshot of the current state (easy rollback)**

```bash
# exact conda specs
conda list --explicit > conda-specs-$(date +%Y%m%d).txt
# pip packages (if any were installed via pip)
python -m pip freeze > pip-freeze-$(date +%Y%m%d).txt
```

**2. Optional but recommended: keep your current Python minor version**

This prevents an unexpected Python jump that can cause conflicts. Adjust `3.11.*` to whatever `python --version` shows:

```bash
python --version
# pin to current minor while updating other deps
conda install "python=3.11.*" -c conda-forge
```

**3. Make sure your solver is up-to-date**

```bash
# update conda itself (and mamba if you have it) in base
conda activate base
conda update -n base -c conda-forge conda
# optional: if you use mamba
conda install -n base -c conda-forge mamba
conda activate vflussenv
```

**4. Update all conda packages**

Use strict conda-forge for consistency (to not modify your YAML).

```bash
# with mamba (faster)
mamba update --all -c conda-forge --yes

# or with conda
conda update --all -c conda-forge --yes
```

**5. If you used *pip* for some packages, upgrade those too**

Only do this **after** the conda update. This keeps conda in charge of core libraries.

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

**6. Clean caches**

```bash
conda clean -a -y
```

**7. Verify versions**

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
## Using the environment in IDEs

### JupyterLab

```bash
(vflussenv) jupyter lab
```

Point your browser to `https://hydro-informatics.com/lab`. Switch kernels via the *Kernel* menu.

### PyCharm

* **File > Settings > Python Interpreter > Add > Existing** > pick `~/venvs/vflussenv/bin/python` (Linux) or `%USERPROFILE%\mambaforge\envs\flussenv\python.exe` (Windows).
* Enable *Sync Python packaging tools* so that `pip install` inside PyCharm’s terminal updates the interpreter list.

---

(remove-env)=
## Deleting environments

* **venv**: `rm -rf ~/venvs/vflussenv`
* **conda**: `conda env remove -n flussenv`

---

(install-python-summary)=
## Installation bottom line

* Use **`python -m venv`** (`pipx` for CLI tools) unless a package *requires* C/C++ libraries that your OS can’t satisfy—then reach for **conda‑forge**.
* Windows users no longer *need* conda for GDAL, but conda remains the easiest path for a full geospatial data‑science stack.
* Pin exact package versions for archival projects; use `>=` pins for living research code.
* Never install packages with `sudo pip`; always work inside an isolated environment.
