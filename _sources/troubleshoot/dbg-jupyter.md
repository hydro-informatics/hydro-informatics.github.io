# Debugging Jupyter

## Install Jupyter on Linux

On *Linux* install *nodejs* and *Jupyter*:

```
sudo apt-get install nodejs
sudo apt-get install jupyter
```

## Issues Starting Jupyter Lab

For some reasons, the `jupyter lab` or `jupyter-lab` commands do not work in another *conda* environment than *base*, or on *Linux* environments. In these cases, open *Anaconda Prompt* (and activate the concerned environment), or *Linux Terminal* and tap:

```
python -m pip install jupyter-lab
```


Alternatively, `pip install jupyterlab` (or `pip3 install jupyterlab`) works just as well.

Try to run `jupyter lab` or `jupyterlab`. If it still does not work, try (on *Linux*):

```
/usr/bin/env python /home/USER-NAME/.local/python3.X/site-packages/jupyterlab
```

Make sure to replace `USER-NAME` with your local user name and `python3.X` with the installed version of *Python* (e.g., `python3.7`).


## Jupyter Does not Recognize Installed Packages in Conda Env


If you launch Jupyter from within a conda environment and the jupyter notebooks are not able to import the packages installed in the environment, you will need to install the **ipykernel** for the particular environment, too. For instance, this error applies when the import `from osgeo import gdal` in a jupyter notebook Python code cell started from the active `flussenv` environment results in an `ImportError`. To troubleshoot this error:

* Shutdown Jupyter(Lab)
* In Anaconda prompt, make sure the target environment is activated (e.g., `conda activate flussenv`)
* Verify if `ipykernel` is installed by typing `conda list`
* If `ipykernel` is not installed, type `conda install -c anaconda ipykernel` to install it
* Add a new kernel with:
	* `ipython kernel install --user --name=KERNEL_NAME`
	* Replace `KERNEL_NAME` with the name you want to use (e.g., `fluss_kernel`)
* Re-run `jupyter-lab` to select the new kernel from the top menu (**Kernel** > **Change Kernel...**)