---
description: Tutoriel pour le traitement de l'imagerie aérienne de drone (UAV) avec Agisoft Metashape pour créer des modèles d'élévation numérique (Modèle numérique de terrain (MNT)) et de l'orthoimagerie pour les relevés fluviaux et terrestres.
---

# Imagerie du drone de procédé (UAV)

```{admonition} This tutorial exceptionally requires proprietary software
:class: important


Cette section propose l'extraction de données avec le logiciel propriétaire *Metashape* d'Agisoft* (édition professionnelle). Pour des essais et des essais éducatifs, [téléchargez Agisoft Metashape](https://www.agisoft.com/downloads/installer/) avec la licence d'essai de 30 jours. Le logiciel fonctionne sous Windows, macOS et Linux. Notez que ce tutoriel s'appuie sur la version 1.8.3.
```

## Acquérir une image de drone aérien

La collecte d'images aériennes est devenue incroyablement facile grâce aux drones contrôlés par pilote automatique. Aujourd'hui, la plupart des drones sont équipés de programmes de tournage d'images aériennes et de modèles numériques d'élévation basés sur la structure-from-Motion (SfM) ({term}`Modèle numérique de terrain <DEM>`s). Comme le contrôle des drones est dépendant du modèle (p. ex., nous utilisons un [dji Phantom 4 RTK](https://dl.djicdn.com/downloads/phantom_4_rtk/20200721/Phantom_4_RTK_User_Manual_v2.4_EN.pdf) drone pour les levés aériens), ce tutoriel ne décrit que les paramètres de base pour la prise d'images aériennes et se concentre sur le traitement d'images pour créer des Modèle numérique de terrain (MNT).

Recommandations pour les vols d'arpentage avec drones:

* Utiliser des modes de relevés terrestres prédéfinis pour un chevauchement suffisant
* Travaillez de préférence avec l'orthoimagerie; utilisez seulement le mode 3d lorsque des vents forts soufflent
* Compter environ 20-30 minutes de vol par batterie (environ 2 heures de recharge), ce qui signifie que 8 batteries permettent une cartographie en douceur
* Les points de contrôle au sol peuvent être omis si les données RTK sont disponibles, mais nous recommandons d'utiliser les points de contrôle au sol

De plus, on peut aussi construire un Modèle numérique de terrain (MNT) basé sur l'imagerie pour les eaux peu profondes et claires (c.-à-d. les bathymétries), mais d'autres techniques de mesure (p. ex. {term}`Lidar` ou {term}`Sonar`) sont nécessaires pour les eaux plus profondes (> 0,5 m de profondeur d'eau). De plus, la bathymétrie à base d'images devrait être validée ou corrigée au moyen de mesures DGPS locales ou de stations totales.


## Métaforme

La figure ci-dessous montre l'interface Metashape au démarrage du programme, prêt à jouer avec l'imagerie de drone et SfM.


```{figure} ../img/drone/metashape-startup.png
:alt: metashape agisoft gui interface
:name: meta-startup

L'interface Metashape initiale.
```


### Créer un nouveau projet

Pour commencer, **create** a **new project** and **save** it (sous forme de fichier `.psx`) de préférence un niveau de dossier au-dessus du répertoire des images. Ensuite, familiarisez-vous avec l'interface et explorez les nombreux workflows fournis dans le menu **Workflow**.


```{admonition} Metashape workflows
:class: tip

Metashape a plusieurs workflows intégrés qui nous permettent de naviguer intuitivement dans la création de produits SfM basés sur l'imagerie. Nous utiliserons certains de ces flux de travail dans les éléments suivants pour dériver un {term}`Modèle numérique de terrain <DEM>`.
```

### Chargement des images

Les images peuvent être chargées fichier par fichier, ou beaucoup plus facilement, à partir d'un répertoire entier. Pour ajouter un répertoire (c.-à-d. dossier) contenant des images aériennes d'un drone monocaméra, allez dans le menu **Workflow** > **Ajouter un dossier** > **Choisissez un dossier contenant des images** > **Cameras uniques**.


### Alignez les images

Lorsque le drone survole des terrains, il doit parfois changer de direction ou de position, mais il *sait toujours* où il se trouve (absoluement ou par rapport à une station au sol) si les données RTK-GPS sont disponibles. Par conséquent, les images peuvent avoir été prises à des angles et des positions différents. Pour fusionner les images en une seule grande image du terrain, les images doivent être alignées par des points correspondants visibles sur plusieurs images. L'image peut être créée avec l'outil d'alignement de Metashape : allez à **Workflow** > **Alignez Fotos** et considérez les paramètres suivants dans la fenêtre contextuelle (voir la figure ci-dessous) avec le cadre **Avancé** élargi:

* Régler le **Accuracy** à **high** pour un équilibre acceptable de résolution et de temps de calcul. Notez que toute augmentation supplémentaire de la précision donne lieu à un ordre de grandeur plus long de calculs.
* Dans **Présélection de référence** sélectionnez **Source** et assurez-vous d'utiliser les données GPS.
* ** Cadre avancé** :
    * l'option **Key point limit** permet de définir **points caractéristiques** (c'est-à-dire des points que l'algorithme d'alignement peut clairement identifier sur plusieurs images): assurez-vous de permettre l'identification de 10.000 à 40.000 points caractéristiques.
    * la limite **Tie point** définit un nombre minimum pour les points de liaison (c.-à-d. des points que l'algorithme d'alignement identifie sur deux images voisines): assurez-vous de permettre l'identification d'au moins 1.000 à 5.000 points de liaison.
    * utiliser l'option **enable exclusion des points stationnaires**, ce qui permet de s'assurer que les pixels ayant les mêmes caractéristiques (couleur) sur toutes les images (c.-à-d. qui sont stationnaires) sont exclus de l'identification d'alignement. Ainsi, par exemple, les taches de saleté sur l'objectif de la caméra seront exclues comme points clés d'alignement.
    * Activer **module de montage de caméra adapté** pour une distorsion de caméra non corrigée.
* Laissez **tous les autres champs par défaut** comme-est et cliquez sur **OK** pour démarrer l'alignement. Selon la quantité et la taille des images ainsi que la capacité de calcul de votre ordinateur, l'alignement prend 5-30 minutes.

```{figure} ../img/drone/metashape-align.png
:alt: metashape align fotos images pictures
:name: meta-align

La fenêtre popup fotos aligne dans Metashape.
```

Lorsque l'alignement est effectué, produire un nuage de **point grossier** (choisir dans le menu **Outils**). Un nuage grossièrement bon se caractérise par au moins 100 points de liaison par m$^2$ ou plus de 50 000 points de liaison par 100 images (avec une résolution de 4605x3227). De plus, **vérifier les erreurs** en cliquant sur le ruban **Référence** (généralement en bas à gauche de la fenêtre Metashape). L'erreur de longitude/latitude doit être $\leq$ 2 cm.


### Construire un nuage de point dense

Lorsque la qualité est suffisante et que l'erreur est acceptablement faible, procédez à la construction d'un nuage **point dense** (choisir dans le menu **Workflow**). Dans la fenêtre popup nuage point dense (voir aussi la figure ci-dessous), effectuez les réglages suivants:

* Régler la qualité **** à **haut**
* Choisissez **remplissage en profondeur** en fonction de la densité de végétation:
    * si non à très peu de végétation, sélectionnez **modéré / agressif**
    * si la végétation est présente, une bonne performance (qualité du nuage par rapport au temps de calcul) peut être obtenue en choisissant l'option **mild**
    * dans le cas d'une végétation très dense, le remplissage en profondeur peut être **désactivé**, bien que cela puisse entraîner **des temps de calcul très longs**
* Cliquez sur **OK** pour créer le nuage point dense (peut prendre encore 5-30 minutes)

```{figure} ../img/drone/metashape-dense-cloud.png
:alt: metashape dense point cloud
:name: meta-dense-cloud

Le dialogue de nuage point dense dans Metashape.
```

La qualité **** du nuage de points denses peut être considérée comme bonne si le processus trouvé:

* Au moins 20 à 30 voisins.
* Environ 10 millions de points pour 100 images (avec une résolution de 4605x3227).


### Créer Modèle numérique de terrain (MNT)

Le nuage point dense ou grossier peut être utilisé avec beaucoup d'autres workflows et la création d'un {term}`Modèle numérique de terrain <DEM>` n'est qu'une option. Pour créer un Modèle numérique de terrain (MNT), allez à **Travail** > **Construire Modèle numérique de terrain (MNT)** et considérer les aspects suivants dans la fenêtre contextuelle de build Modèle numérique de terrain (MNT) (voir figure ci-dessous):

* Projection:
    * utiliser un type **géographique** pour la projection sur un raster {term}`GeoTIFF`, qui est compatible avec la plupart des logiciels SIG, comme {ref}`QGIS <qgis-tutorial>`.
    * La projection par défaut de Metashape est `EPSG:4326` (en savoir plus dans la section {ref}`projections in this eBook <prj>`), ce qui correspond à la projection couramment utilisée avec les interfaces d'imagerie aérienne (par exemple, *GoogleEarth*).
* Source:
    * l'option **tie points** conduit à la résolution **la plus basse**.
    * l'option **cartes approfondies** est un **bon compromis** entre résolution et temps de calcul.
    * l'option **dense Cloud** conduit à la **meilleure qualité** mais aussi à un temps de calcul très long.
* Cadre avancé : conservez automatiquement les valeurs proposées pour assurer la cohérence.

Le bouton **OK** lance la création Modèle numérique de terrain (MNT), qui peut prendre encore 5-30 minutes.

```{figure} ../img/drone/metashape-dem.png
:alt: metashape dem dgm digital elevation model geotiff
:name: meta-dem

Le dialogue popup création Modèle numérique de terrain (MNT) dans Metashape.
```

Enfin, exportez le Modèle numérique de terrain (MNT) avec un ** clic droit** sur le **Modèle numérique de terrain (MNT)** dans l'espace de travail** (si le Modèle numérique de terrain (MNT) n'est pas visible, étendez l'entrée **Chunk 1** - ou quel que soit le nom qu'il a - dans l'espace de travail) et sélectionnez **Exporter Modèle numérique de terrain (MNT)...**. Nous vous recommandons de sauvegarder le Modèle numérique de terrain (MNT) au format {term}`GeoTIFF` (**.tif**), qui est compatible avec {ref}`QGIS <qgis-tutorial>`. Si `.tif` a été sélectionné, une fenêtre contextuelle pour exporter le Modèle numérique de terrain (MNT) s'ouvre. Dans la fenêtre contextuelle, vérifiez l'option **exporter le fichier mondial** et gardez toutes les autres valeurs par défaut (en option, créez un fichier `.kml` pour travailler avec *GoogleEarth*). Le fichier mondial sera important pour QGIS (et tout autre logiciel SIG) pour savoir où se trouve le Modèle numérique de terrain (MNT) géographiquement par rapport à la projection sélectionnée.


### Créer un Mesh

Comme pour le workflow Modèle numérique de terrain (MNT), Metashape fournit un workflow pour créer un maillage (**Workflow** > **Build Mesh**) sous la forme d'un réseau irrégulier triangulé ({ref}`TIN <tin>`). Les options **Source data** sont similaires à celles du workflow Modèle numérique de terrain (MNT), avec une option supplémentaire d'utilisation du Modèle numérique de terrain (MNT) pour le maillage. Aussi pour un maillage, **La qualité élevée** et les comptes de visage se traduisent par la meilleure représentation du terrain et des coûts de calcul élevés. Si l'objectif de la génération de mailles est son utilisation avec un modèle numérique, la qualité inférieure et le nombre de visages pourraient être un bon choix pour garder le temps pour exécuter le modèle numérique bas. La génération de mailles prend encore 5-30 minutes.

```{figure} ../img/drone/metashape-mesh.png
:alt: metashape mesh creation stl numerical model
:name: meta-mesh

Le dialogue popup de création de maillage dans Metashape.
```

Une fois la création du maillage terminée, elle peut être exportée avec un clic droit sur l'entrée **3D Model** dans le **Workspace** et un clic gauche sur **Export Model...**. Si le modèle 3D n'est pas visible dans l'espace de travail, étendez l'entrée **Chunk 1** (ou quel que soit le nom qu'il possède). Pour une utilisation avec un modèle numérique (p. ex. OpenFOAM), le format STL (`.stl`) est un bon choix.


```{admonition} Take advantage of Metashapes Python bindings
:class: tip

Metashape est livré avec le script Python que de permettre l'automatisation des appels aux flux de travail avec différents paramètres. Pour commencer avec Python, consultez le {ref}`Python tutorials <about-python>` dans ce livre électronique et le [Guide de référence Python](https://www.agisoft.com/pdf/metashape_python_api_1_5_0.pdf)].
```
