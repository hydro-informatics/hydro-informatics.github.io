(install-python)=

# Python (Installation)

> "The zen of thriving Python projects in 2025 is *one interpreter per project* and *one tool‑chain per task*. Master virtual environments first; the rest follows naturally."

Python 2 reached end‑of‑life in **January 2020** and is no longer shipped by mainstream Linux distributions or Windows installers. Today every actively maintained package—scientific, geospatial, or otherwise—supports
**CPython ≥ 3.9**, with most libraries now testing against **Python 3.13**. Multiple interpreters can still coexist on the same machine (QGIS / ArcGIS Pro embeds its own 3.11, Nvidia CUDA ships one for PyTorch, etc.), but the modern way to insulate projects is through *lightweight* virtual environments created by `venv`, **pipx**, or *conda/mamba*.

This chapter distils a workflow that reliably builds the computational stack used throughout this e‑book, regardless of platform. It emphasises

* **`pip` + `venv`** on Linux/macOS (preferred),
* **`conda`/`mamba`** on Windows or when you need complex compiled dependencies,
* recent improvements in binary wheels for GDAL/Fiona/Shapely (pip on Windows is finally painless!), and
* sustainable ways to keep environments reproducible.

---

(pip-env)=
## `pip` + `venv` recommended on Linux/macOS

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
[`mamba`](https://github.com/mamba-org/mamba) is a drop‑in replacement for `conda` written in C++; it resolves environments 10–100 × faster.
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
## Installing extra packages with `pip`

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
## Jupyter kernel

```bash
(vflussenv) pip install ipykernel jupyterlab
(vflussenv) python -m ipykernel install --user --name vfluss_kernel
```
Select **vfluss_kernel** from *Kernel > Change kernel* inside JupyterLab.


---

## Updating environments

```bash
(vflussenv) pip install -U pip setuptools wheel
(vflussenv) pip list --outdated           # preview
(vflussenv) pip install -U "numpy>=2.3"  # upgrade selectively
```

Full upgrade:

```bash
pip freeze > requirements.txt             # pin current versions
sed -i 's/==/>=/' requirements.txt        # allow newer releases (Linux), or edit manually
pip install -r requirements.txt --upgrade
```

If `pip` reports **ResolutionImpossible**, relax or delete the offending version pins and rerun.

---

(ide-setup)=
## Using the environment in IDEs

### JupyterLab

```bash
(vflussenv) jupyter lab
```

Point your browser to `http://localhost:8888/lab`. Switch kernels via the *Kernel* menu.

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
