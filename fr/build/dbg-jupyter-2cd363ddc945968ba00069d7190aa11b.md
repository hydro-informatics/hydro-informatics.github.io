---
description: Dépannage des problèmes d'installation et de démarrage de Jupyter et JupyterLab sur les environnements Linux, macOS et conda, y compris les corrections communes pour les échecs de lancement.
---

# Déboguer Jupyter

## Installez Jupyter sur Linux

Sur *Linux* installer *nodejs* et *Jupyter*:

```
sudo apt-get install nodejs
sudo apt-get install jupyter
```

## Questions de démarrage Jupyter Lab

Pour certaines raisons, les commandes `jupyter lab` ou `jupyter-lab` ne fonctionnent pas dans un autre environnement *conda* que *base* ou sur des environnements *Linux*. Dans ces cas, ouvrir *Anaconda Prompt* (et activer l'environnement concerné), ou *Linux Terminal* et taper:

```
python -m pip install jupyter-lab
```


Alternativement, `pip install jupyterlab` (ou `pip3 install jupyterlab`) fonctionne aussi bien.

Essayez de lancer `jupyter lab` ou `jupyterlab`. Si cela ne fonctionne toujours pas, essayez (sur *Linux*):

```
/usr/bin/env python /home/USER-NAME/.local/python3.X/site-packages/jupyterlab
```

Assurez-vous de remplacer `USER-NAME` par votre nom d'utilisateur local et `python3.X` par la version installée de *Python* (par exemple, `python3.7`).


## Jupyter ne reconnaît pas les paquets installés dans Conde Env


Si vous lancez Jupyter à partir d'un environnement conda et que les cahiers jupyter ne peuvent pas importer les paquets installés dans l'environnement, vous devrez installer le **ipykernel** pour l'environnement particulier, aussi. Par exemple, cette erreur s'applique lorsque l'importation `from osgeo import gdal` dans un portable de jupyter Python code cellule a commencé à partir de l'environnement actif `flussenv` résultats dans un `ImportError`. Pour résoudre cette erreur :

* Arrêt Jupyter (Lab)
* Dans l'invite Anaconda, assurez-vous que l'environnement cible est activé (par exemple, `conda activate flussenv`)
* Vérifier si `ipykernel` est installé en tapant `conda list`
* Si `ipykernel` n'est pas installé, tapez `conda install -c anaconda ipykernel` pour l'installer
* Ajouter un nouveau noyau avec :
	* `ipython kernel install --user --name=KERNEL_NAME`
	* Remplacer `KERNEL_NAME` par le nom que vous souhaitez utiliser (par exemple, `fluss_kernel`)
* Re-run `jupyter-lab` pour sélectionner le nouveau noyau dans le menu supérieur (**Kernel** > **Change Kernel...**)