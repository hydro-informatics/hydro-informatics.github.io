---
description: Introduction à la programmation de Python géospatial pour l'hydrologie, couvrant les bibliothèques ouvertes et commerciales, la manipulation de données raster et vectorielle, et la conversion de fichiers géospatials.
---

(sec-geo-python)=
# Python géospatial

Python est connecté à plusieurs bibliothèques fournissant de nombreuses fonctions open-source et commerciale (propriétaire) pour l'analyse des données géospatiales. Cette section présente à la fois les sources ouvertes et la bibliothèque commerciale `arcpy`. Le but de cette section est de fournir une compréhension de la façon dont les données géospatiales peuvent être utilisées et manipulées avec le code Python. La manipulation des fichiers implique des opérations logiques et algébriques, et la conversion à partir et vers d'autres formats de fichiers géospatials.

```{admonition} Requirements
:class: important

Assurez-vous de comprendre les bases de Python, en particulier {ref}`var`, {ref}`sec-pyerror`, {ref}`chpt-functions`, et de travailler avec {ref}`sec-pypckg` externe.
```

```{admonition} Maximize learning success
:class: tip

* Utilisez le paquet [flusstools](https://flusstools.readthedocs.io) pour faciliter le travail avec les tutoriels fournis avec ce livre électronique.
* Comprendre {ref}`geospatial-data`, qui sont les fondements de toute analyse géospatiale.
* Utilisez {ref}`qgis-install` pour afficher les données géospatiales et créer des cartes en format *PDF* ou image (p. ex., *tif*, *png*, *jpg*).
```

Les descriptions des paquets open source pour le traitement des données géospatiales s'appuient sur les explications de [Michael Diener's Python Geospatial Analysis Cookbook](https://github.com/mdiener21/python-geospatial-analysis-cookbook) (accès ouvert sous licence MIT). Par conséquent, si vous voulez en savoir plus sur les informations fournies ici, jetez un oeil à ce livre électronique complet.

Une autre excellente source d'inspiration avec de nombreux exemples open-source est [*pcjericks* Dépôt GitHub *py-gdalogr-cookbook*](https://pcjericks.github.io/py-gdalogr-cookbook/).

```{admonition} How to use PyQGIS (QGIS Python environment)
:class: tip, dropdown

Pour activer le travail avec les commandes QGIS dans les scripts Python autonomes via `from qgis.core import *`, regardez le {ref}`PyQGIS section <pygis>` au bas du tutoriel QGIS dans ce livre électronique.
```
