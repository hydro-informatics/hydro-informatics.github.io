---
description: Tutoriel pour post-traitement des simulations OpenFOAM avec ParaView.
---

# Traitement après

Le post-traitement est une étape cruciale dans la compréhension et l'analyse des résultats des simulations {term}`CFD`, en particulier pour les scénarios de flux multiphasés. Ce tutoriel est conçu pour vous guider à travers les étapes essentielles de l'extraction des informations significatives des simulations OpenFOAM, en mettant l'accent sur la visualisation et l'analyse avec ParaView (ParaFoam). Sur cette page, vous apprendrez à utiliser efficacement des outils comme ParaView pour interpréter les résultats de simulation, manipuler et traiter les sorties OpenFOAM.

`````{admonition} Visualization software: ParaView and alternatives
:class: tip

OpenFOAM post-traitement peut être accompli avec paraFoam, un module logiciel qui expédie avec OpenFOAM. ParaFOAM est une version spécialisée de ParaView configurée pour traiter directement les fichiers de données OpenFOAM sans plugins supplémentaires. ParaView est un outil général de visualisation open-source pour analyser et visualiser les grands ensembles de données. ParaFOAM est adapté pour les utilisateurs d'OpenFOAM avec compatibilité intégrée, tandis que ParaView nécessite des étapes supplémentaires pour lire les formats d'OpenFOAM, mais prend en charge une plus large gamme de types de données et de pipelines d'analyse.

Pour travailler directement avec ParaView au lieu de paraFOAM, exécutez l'utilitaire `foamToVTK` fourni par OpenFOAM pour convertir les résultats de simulation en fichiers compatibles VTK que ParaView peut lire nativement, ou utilisez des plugins ParaView. Par exemple, le plugin **OpenFOAM Reader** permet de charger un fichier `.foam` (généralement créé dans le répertoire des cas de simulation en ajoutant un fichier vide nommé `<case>.foam`) et ParaView analysera le cas en utilisant le plugin.

Les logiciels alternatifs incluent des outils comme [VisIt](https://visit-dav.github.io/visit-website/index.html), qui fournit des capacités de visualisation similaires à ParaView. VisIt est également un logiciel de visualisation open-source et dispose d'une interface intuitive.

````{admonition} Enable VisIt for OpenFOAM
:class: note, dropdown

Pour utiliser VisIt pour analyser la sortie de simulation OpenFOAM, suivez les étapes suivantes :

1. Téléchargez et installez VisIt à partir de https://visit-dav.github.io/visit-website/index.html (assurez que vous avez les dépendances système requises).

2. Depuis VisIt ne lit pas nativement les fichiers OpenFOAM, convertir les données de simulation dans un format compatible avec VisIt, comme VTK. Pour ce faire, utilisez l'utilitaire `foamToVTK` fourni par OpenFOAM :

   ```bash
   foamToVTK
   ```

Cela générera des fichiers VTK dans un répertoire `VTK` dans votre dossier de simulation.

3. Pour charger les données dans VisIt, (ouvrir VisIt) naviguez vers le répertoire `VTK` créé par `foamToVTK`, et chargez les fichiers VTK cibles. Sélectionnez les champs pertinents tels que la vitesse, la pression, ou d'autres quantités pour la visualisation.

4. Pour explorer les données, utilisez les outils de visualisation VisIt, tels que le découpage, le contour, le tracé vectoriel et la visualisation de l'évolution temporelle pour des simulations dynamiques.

L'analyse personnalisée peut être mise en œuvre en tirant parti des capacités de script de VisIt ou en utilisant des filtres avancés pour effectuer des analyses spécifiques, telles que l'intégration de quantités de flux, l'exportation de données ou la visualisation d'interactions complexes dans vos résultats.

````

`````

## Récupérer les données de simulation

Dans le cas où les simulations ont été effectuées en parallèle, avant le post-traitement des données, la première étape consiste à reconstruire (c'est-à-dire à réassembler) toutes les étapes de la solution du cas analysé. Cela peut être fait pour toutes les étapes ou seulement pour une étape spécifique. Les commandes à taper dans la fenêtre du terminal sont indiquées ci-dessous :

* Pour reconstruire toutes les étapes de la solution :

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar
```
  
* Pour reconstruire une étape de temps spécifique (suppléter "x" avec l'étape de temps):

```
user@user123:~/OpenFOAM-9/channel/Simulation$ reconstructPar -time x
```

## Visualisation avec ParaView (paraFoam)

ParaFoam est une version personnalisée du logiciel de visualisation ParaView qui vient préconfiguré pour lire et traiter les données de simulation OpenFOAM directement. Il simplifie le post-traitement en intégrant des formats de fichiers et des fonctionnalités spécifiques à OpenFOAM, permettant aux utilisateurs de visualiser les champs, d'extraire des informations et d'analyser les résultats sans configuration supplémentaire.

Le travail avec paraFoam exige que le cas de simulation ait été construit (voir la section ci-dessus). Un cas de simulation se réfère à l'ensemble complet de fichiers et de configurations nécessaires pour définir, exécuter et analyser un scénario de simulation spécifique. Elle comprend la géométrie et le maillage du domaine computationnel, les conditions initiales et limites, les paramètres du solveur, les modèles physiques et tout autre paramètre nécessaire à la simulation. Le cas est organisé en répertoires tels que `constant` (propriétés matérielles et maillage), `system` (contrôles de sol), et `0` (conditions initiales), formant un cadre structuré pour les expériences numériques.

### Lancer paraFoam

Une fois le cas reconstruit, comme pour le processus de maillage, la commande suivante peut être utilisée pour visualiser le cas dans le logiciel ParaView:

```
user@user123:~/OpenFOAM-9/channel/Simulation$ paraFoam
```

### Pipelines de visualisation

La chaîne. OpenFOAM* devrait maintenant être présent dans le navigateur Pipeline et pour le visualiser dans la mise en page, appuyez sur le bouton *Apply*. De plus, dans la section *Fields*, les différents champs qui peuvent être visualisés sont affichés et peuvent être sélectionnés/désélectionnés en fonction de l'objet de l'analyse.

```{figure} ../../img/openfoam/interFoam/Paraview/channelOpenFOAM.png
:alt: openfoam 
:name: of-channelOpenFOAM

Visualisation des résultats du cas dans ParaView.
```

Afin de visualiser les phases air et eau, *alpha.water* doit être sélectionné dans le menu déroulant comme indiqué dans l'image ci-dessous.

```{figure} ../../img/openfoam/interFoam/Paraview/view-alpha-water.png
:alt: openfoam 
:name: of-view-alphawater

Permettre le réglage pour observer les phases air et eau dans ParaView.
```

Pour modifier l'étape de temps indiquée, les flèches qui peuvent être vues dans la zone surlignée en rouge peuvent être utilisées.


```{figure} ../../img/openfoam/interFoam/Paraview/final-time-step.png
:alt: openfoam timestep time step
:name: of-final-time-step

Options pour modifier l'étape temporelle à visualiser.
```

Ensuite, pour ne visualiser que la phase d'eau, le filtre *Clip* est utilisé. Ceci peut être trouvé dans la section *Filters* du menu, ou bien le raccourci peut être utilisé. Le *Clip Type* doit être réglé sur *Scalar*, en sélectionnant *alpha.water* comme scalaire et en fixant la valeur à 0,5, ce qui représente l'interface entre l'air et l'eau. Pour voir la phase d'air, l'option *Invert* doit être sélectionnée alors que pour la phase d'eau elle doit être désélectionnée.

```{figure} ../../img/openfoam/interFoam/Paraview/clip-water.png
:alt: openfoam clip water interFoam
:name: of-clip-water


Filtre à clips utilisé pour visualiser la phase d'eau dans ParaView.
```

Enfin, pour ajouter les murs et les correctifs à la vue, le filtre *Extract Block* peut être implémenté (cliquez sur le canal *). Ouvrir le fichier FOAM* avant de l'appliquer).

```{figure} ../../img/openfoam/interFoam/Paraview/extract-block.png
:alt: openfoam 
:name: of-extract-block

Liste des filtres disponibles dans ParaView, surlignement ExtractBlock.
```

Les correctifs d'intérêt peuvent alors être sélectionnés ou désélectionnés, et le *Couleur* peut être réglé sur Solid Color.

```{figure} ../../img/openfoam/interFoam/Paraview/choose-patches.png
:alt: openfoam 
:name: of-choose-patches

Options disponibles pour sélectionner les correctifs et changer la couleur.
```

La vue résultante de la phase d'eau et de l'extraction de blocs est présentée ci-dessous:

```{figure} ../../img/openfoam/interFoam/Paraview/alpha-water.png
:alt: openfoam 
:name: of-alpha-water

Résultats de simulation mettant en évidence la phase eau.
```

Différents paramètres peuvent également être vus, comme la vitesse d'écoulement, et cela peut être fait dans la section *Couleur* en sélectionnant *U*. Le *preset* peut être modifié pour mieux visualiser les résultats en sélectionnant l'icône correspondante (en vert).

```{figure} ../../img/openfoam/interFoam/Paraview/flow-velocity.png
:alt: openfoam 
:name: of-flow-velocity

Résultats de simulation mettant en évidence la vitesse du flux.
```

