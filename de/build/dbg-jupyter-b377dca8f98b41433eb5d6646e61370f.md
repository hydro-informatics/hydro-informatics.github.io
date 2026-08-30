---
description: Fehlerbehebung bei der Installation und dem Start von Jupyter und JupyterLab unter Linux, macOS und Conda-Umgebungen, einschließlich gemeinsamer Korrekturen für Startfehler.
---

# Debugging Jupyter

## Jupyter unter Linux installieren

Auf *Linux* installieren *nodejs* und *Jupyter*:

```
sudo apt-get install nodejs
sudo apt-get install jupyter
```

## Probleme beim Start von Jupyter Lab

Aus einigen Gründen funktionieren die Befehle `jupyter lab` oder `jupyter-lab` nicht in einer anderen *conda*-Umgebung als *base* oder in *Linux*-Umgebungen. Öffnen Sie in diesen Fällen *Anaconda Prompt* (und aktivieren Sie die betreffende Umgebung) oder *Linux Terminal* und tippen Sie auf:

```
python -m pip install jupyter-lab
```


Alternativ funktioniert `pip install jupyterlab` (oder `pip3 install jupyterlab`) genauso gut.

Try to run `jupyter lab` or `jupyterlab`. If it still does not work, try (on *Linux*):

```
/usr/bin/env python /home/USER-NAME/.local/python3.X/site-packages/jupyterlab
```

Make sure to replace `USER-NAME` with your local user name and `python3.X` with the installed version of *Python* (e.g., `python3.7`).


## Jupyter erkennt installierte Pakete in Conda Env nicht


If you launch Jupyter from within a conda environment and the jupyter notebooks are not able to import the packages installed in the environment, you will need to install the **ipykernel** for the particular environment, too. For instance, this error applies when the import `from osgeo import gdal` in a jupyter notebook Python code cell started from the active `flussenv` environment results in an `ImportError`. To troubleshoot this error:

* Shutdown Jupyter(Lab)
* Stellen Sie in Anaconda prompt sicher, dass die Zielumgebung aktiviert ist (z.B. `conda activate flussenv`)
* Überprüfen Sie, ob `ipykernel` installiert ist, indem Sie `conda list` eingeben
* Wenn `ipykernel` nicht installiert ist, geben Sie `conda install -c anaconda ipykernel` ein, um es zu installieren
* Hinzufügen eines neuen Kernels mit:
	* `ipython kernel install --user --name=KERNEL_NAME`
	* Ersetzen Sie `KERNEL_NAME` durch den Namen, den Sie verwenden möchten (z. B. `fluss_kernel`)
* Führen Sie `jupyter-lab` erneut aus, um den neuen Kernel aus dem oberen Menü auszuwählen (**Kernel** > **Kernel ändern...**)