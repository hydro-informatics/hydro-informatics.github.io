---
description: Guide des logiciels géospatials pour l'ingénierie des ressources en eau, y compris l'installation et l'utilisation de QGIS sur Windows, Linux et macOS pour la visualisation et l'analyse des données SIG.
---

(chpt-geo-software)=
# Logiciel géospatial

Les analyses (ou analyses) géospatiales utilisent, manipulent et illustrent les données des systèmes d'information géographique (SIG). Les données SIG contiennent des informations géographiques et spatiales explicites concernant par exemple les stations de jaugeage, l'altitude du terrain ou l'utilisation du sol. Le traitement efficace des données géospatiales implique des méthodes de programmation, où *Python* est un outil efficace. Cette page présente un logiciel de bureau pour les analyses géospatiales manuelles et l'illustration des données géospatiales. Pour la programmation géospatiale, veuillez consulter le chapitre {ref}`sec-geo-python`.

(qgis-install)=
## QGIS
Pour la visualisation des fichiers géodonnées (`.shp` et `.tif`), un logiciel SIG est nécessaire et les analyses décrites sur ces pages renvoient à l'utilisation de [QGIS](https://www.qgis.org). Ce livre électronique utilise le QGIS dans les sections sur {ref}`geospatial programming with Python <sec-geo-python>` et la modélisation numérique avec le logiciel [BASEMENT](../numerics/basement/basement)] de l'ETH Zurich.

### Installer QGIS sur Windows
Téléchargez et installez la dernière version de [QGIS](https://qgis.org/download/) pour Windows. Même si les développeurs recommandent d'installer QGIS à travers *OSGeo4W*, cette voie d'installation n'est pas recommandée pour travailler avec le eBook *hydro-informatique* (nombreuses erreurs de plugin et dépendances de bibliothèque dépassées). Par conséquent, ** télécharger de préférence et utiliser le dernier QGIS Standalone Installer**.

### Installer QGIS sur Linux (via Flatpak)

Les développeurs QGIS fournissent des instructions détaillées d'installation pour plusieurs distributions *Linux*, mais les instructions ne satisfont pas à toutes les exigences relatives à l'utilisation de QGIS décrites dans ce livre électronique. Une des façons les plus fonctionnelles d'installer QGIS sur *Linux* est d'utiliser [Flatpak](https://flathub.org/apps/details/org.qgis.qgis), qui nécessite une certaine préparation du système. Sur les plateformes *Debian* (par exemple, toutes sortes de *Ubuntu* comme *Lubuntu* ou *Mint*) ouvertes *Terminal* et tap (la deuxième ligne n'est nécessaire que si vous utilisez *GNOME*):

```
sudo apt install flatpak
sudo apt install gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

Redémarrez le système et ouvrez l'application *Software Manager*. Il mettra à jour et ajoutera la repo flathub. Une fois la mise à jour réussie, recherchez QGIS et cliquez sur *Installer* (patience - l'installation peut prendre un certain temps).

The *QGIS Flatpak* installation will most likely not include the important *scipy* module. To fix this issue, open  *Terminal* (standard Linux application) and type:
<br>`flatpak run --command=pip3 org.qgis.qgis install scipy --user`

Cette solution a été testée sur *Linux Ubuntu* et *Linux Mint*. Il peut également fonctionner avec *Red Hat*, *openSUSE*, *macOS*, *Arch*, *Fedora*, *Android*, *Debian*, *Kubuntu* et bien d'autres (lire les guides d'installation sur le site Web du responsable](https://flatpak.org/setup/)). Pour en savoir plus sur l'installation *QGIS Flatpak* sur le [QGIS website](https://qgis.org/download/).

### Installer QGIS sur macOS

```{admonition} macOS and BASEMENT
:class: attention
Si vous prévoyez d'utiliser BASE pour la modélisation numérique: BASE ne fonctionnera pas sur macOS.
```

Téléchargez et installez la dernière version de [QGIS](https://qgis.org/download/) pour macOS. L'intégrité de l'utilisation de macOS pour les applications de cet ebook n'a pas encore été testée. Le dépannage possible avec *Python* est fourni par exemple par [kyngchaos.com](https://www.kyngchaos.com/software/qgis/).

### Apprendre le QGIS
Travailler avec des éditeurs de données géospatiales implique des tâches complexes qui nécessitent des connaissances de base avant que la compréhension intuitive soit possible. Les développeurs de QGIS fournissent des [tutoriels] composés sur leur site Web](https://docs.qgis.org/latest/en/docs/training_manual/index.html) ([également disponible dans d'autres langues, y compris le français, l'allemand et le portugais](https://docs.qgis.org/latest/)).
Ce livre électronique utilise occasionnellement le système QGIS pour tracer et créer des données géoréférencées (par exemple, les chapitres sur {ref}`sec-geo-python` et {ref}`numerical modeling <qgis-prepro-bm>`). À cette fin, ce livre électronique accompagne un tutoriel sur les analyses géospatiales avec QGIS (lire et faire le {ref}`qgis-tutorial`).

(qgis-conda-install)=
### Installer QGIS conda Environnement

Dans {ref}`Anaconda Prompt <anaconda>`, vous pouvez créer un nouvel environnement pour utiliser spécifiquement les fonctionnalités QGIS (c.-à-d. les outils et les scripts) y compris sa calculatrice raster. L'environnement est présenté par *Open Data Cube* ([lire plus](https://datacube-qgis.readthedocs.io/en/latest/installation.html)) et peut être installé comme suit:

```
conda create  -c conda-forge -n qgiscube python=3.11 qgis datacube
conda activate qgiscube
```

(agis)=
## ArcGIS

```{admonition} Windows only
:class: attention
ArcGIS est conçu pour Windows et ne fonctionnera pas sur macOS ou Linux. En outre, une licence doit être achetée.
```

Le logiciel propriétaire *ArcGIS Pro* représente un outil puissant pour toute analyse géospatiale, y compris les applications web. *ArcGIS Pro* est maintenu par [esri](https://www.esri.com/) et est livré avec un propre {ref}`conda-env`. Avec l'accent de ce livre électronique sur les logiciels librement disponibles, l'utilisation de *ArcGIS Pro* et de son environnement *Python*, y compris le paquet `arcpy`, vient d'être mentionnée sur ce site.

(others)=
## Autres
Il y a beaucoup d'autres outils pour les analyses géospatiales, qui méritent tous bien plus que d'être mentionnés ici. Hélas, pour des raisons pratiques, ce site se concentre sur l'utilisation de QGIS. C'est pourquoi il n'y a qu'une liste absolument incomplète d'autres outils SIG :

* [SAGA (Système pour les analyses géoscientifiques automatisées)](http://www.saga-gis.org/en/index.html)
* [Mapline](https://mapline.com/)
* [Mapbox](https://www.mapbox.com/)
* [uDig](http://udig.refractions.net/)

## Analyses géospatiales

Les analyses géospatiales impliquent des pratiques de code efficaces (par exemple, avec *Python*) et c'est pourquoi des descriptions détaillées du traitement des données géospatiales sont intégrées au chapitre {ref}`sec-geo-python` de ce livre électronique.
