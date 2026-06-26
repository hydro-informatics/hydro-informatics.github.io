---
description: Tutoriel pour l'exécution de l'interFoam OpenFOAM pour les simulations d'eau.
---

# Solveur multiphasé (tutoriel interfoam)

Dans ce tutoriel nous allons résoudre un problème de 50 m de long canal droit avec deux bassins, un plus petit à l'entrée, et un plus grand à la sortie, et un obstacle situé au milieu.

```{figure} ../../img/openfoam/blender/study-area.jpg
:alt: openfoam 
:name: of-study-area

Vue 3D de la structure analysée.
```

Dans ce cas, nous utiliserons l'interFoam de résolution multiphase couplé avec un modèle de turbulence {term}`k <Turbulent kinetic energy>` - $\epsilon$ (epsilon). interFoam identifie l'interface eau-air basée sur la méthode du volume de liquide (VOF), qui résout les équations de transport pour une seule ou plusieurs fractions de phase alpha, où alpha est 0,5 à l'interface entre les fluides (voir [OpenFOAM Standard Solvers](https://www.openfoam.com/documentation/user-guide/a-reference/a.1-standard-solvers)). En outre, nous nous concentrerons sur la mise en place de zones de rugosité multiples liées aux éléments techniques et axés sur la nature présents dans le modèle, et nous appliquerons une hauteur de rugosité spécifique.

```{figure} ../../img/openfoam/blender/channel-view2-final.jpg
:alt: openfoam 
:name: of-channel-view2-final

Vue en 3D de la structure analysée dans la direction du flux en mettant en évidence les matériaux assignés.
```

Le dossier contenant tous les fichiers nécessaires peut être téléchargé [ici](https://github.com/hydro-informatics/openfoam.git).

****
## Importation de fichier
La première section de ce tutoriel traitera de l'importation de la géométrie initialement créée. Tous les fichiers ont été créés à l'aide de Blender, qui est un logiciel 3D gratuit et open source. La géométrie a été divisée en éléments individuels basés sur leur matériau de composition et selon les zones à affiner dans le processus de maillage. Par conséquent, pour le présent exemple, les éléments suivants ont été exportés comme fichiers STL:

* A.R.L.
* Côté béton.stl
* Gravel-bottom.stl
* Inlet.stl
* Obstacle.stl
* Déplacement.stl

```{figure} ../../img/openfoam/blender/elements-structure.png
:alt: openfoam 
:name: of-elements-structure

Éléments constitutifs du canal.
```

Lorsque vous exportez les fichiers STL de Blender, sélectionnez l'option *Ascii* et n'incluez que l'objet sélectionné, comme indiqué ci-dessous.

```{figure} ../../img/openfoam/blender/exportSTL.png
:alt: openfoam 
:name: of-exportSTL

Paramètres pour l'exportation des fichiers STL de Blender.
```

Ensuite, avant de procéder à la génération de maillage, les fichiers STL exportés doivent être ouverts avec un éditeur de texte et la première et dernière ligne doit être modifiée comme suit:

* Suppléant

```
solid Exported from Blender-2.93.3
...
endsolid Exported from Blender-2.93.3
```

* avec le nom des fichiers STL auxquels vous avez affaire, par exemple:

```
solid Gravel-bottom
...
endsolid Gravel-bottom
```

Enfin, tous les fichiers STL exportés et édités peuvent être enregistrés dans le dossier *triSurface* qui sera décrit plus en détail dans la section suivante.

