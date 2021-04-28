# Debugging Jupyter

## Install Jupyter on Linux

On *Linux* install *nodejs* and *Jupyter*:

```
sudo apt-get install nodejs
sudo apt-get install jupyter
```

## Issues starting Jupyter Lab

For some reasons, the `jupyter lab` command does not work in another *conda* environment than *base*, or on *Linux* environments. In these cases, open *Anaconda Prompt* (and activate the concerned environment), or *Linux Terminal* and tap:

```
python -m pip install jupyterlab
```

Alternatively, `pip install jupyterlab` (or `pip3 install jupyterlab`) works just as well.

Try to run `jupyter lab` or `jupyterlab`. If it still does not work, try (on *Linux*):

```
/usr/bin/env python /home/USER-NAME/.local/python3.X/site-packages/jupyterlab
```

Make sure to replace `USER-NAME` with your local user name and `python3.X` with the installed version of *Python* (e.g., `python3.7`).

