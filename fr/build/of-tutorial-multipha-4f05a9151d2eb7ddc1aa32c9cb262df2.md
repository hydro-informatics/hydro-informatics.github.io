---
description: Génération de géométrie et maillage pour des simulations d'eau multiphases OpenFOAM.
---

# Géométrie et génération de mesh

Le maillage est une partie essentielle de la solution numérique et doit répondre à certains critères afin de générer une solution valable et précise. La section suivante décrit l'utilitaire [snappyHexMesh](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.4-mesh-generation-with-the-snappyhexmesh-utility) pour créer des mailles 3d contenant des cellules hexaédriques et hexaédriques fractionnées à partir de géométries de surface triangulées.

Pour plus de détails sur les caractéristiques du maillage et les contraintes de validité, veuillez consulter le [Chapitre 4](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.1-mesh-description#x11-290004.1) du [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/). Pour exécuter snappyHexMesh, en plus d'un maillage de base de géométrie existant, les fichiers suivants sont requis:

```{figure} ../../img/openfoam/snappyHexMesh/folder-structure.png
:alt: openfoam 
:name: of-folder-structure

Répertoire de cas contenant les fichiers nécessaires pour exécuter snappyHexMesh.
```

Les sections suivantes décrivent les étapes à suivre.

## Création du fond Hex Mesh

Avant de pouvoir exécuter *snappyHexMesh*, il faut créer un maillage de fond caractérisé par des cellules hexaédriques. Ce maillage doit contenir toute la région qui doit être enroulée avec *snappyHexMesh*, comme le montre la figure ci-dessous.

```{figure} ../../img/openfoam/snappyHexMesh/block-mesh-init.jpg
:alt: openfoam 
:name: of-block-mesh-init

Mesh de fond créé avec blockMesh contenant la structure à mélanger.
```

Dans le fichier *blockMeshDict*, les éléments suivants doivent être ajoutés:

* le facteur d'échelle pour les coordonnées du vertex

```
   convertToMeters 1;
```
  
* coordonnées des sommets du maillage de fond

```
    vertices
        (
            ( -30.0 -25.0 -25.0 )   //vertex number 0
            ( 70.0 -25.0 -25.0 )   //vertex number 1
            ( 70.0 25.0 -25.0 )   //vertex number 2
            ( -30.0 25.0 -25.0 )   //vertex number 3
            ( -30.0 -25.0 25.0 )   //vertex number 4
            ( 70.0 -25.0 25.0 )   //vertex number 5
            ( 70.0 25.0 25.0 )   //vertex number 6
            ( -30.0 25.0 25.0 )   //vertex number 7
        );
```

*  coordonnées des sommets, suivant l'ordre indiqué ci-dessous

```{figure} ../../img/openfoam/snappyHexMesh/block-mesh-vertexorder.png
:alt: openfoam 
:name: of-block-mesh-vertexorder

Mesh de fond indiquant l'ordre dans lequel les sommets sont écrits dans le fichier block-meshDict.
```

* une liste ordonnée d'étiquettes vertex et de maillage

```
    blocks
        (
            hex (0 1 2 3 4 5 6 7)   // vertex numbers
            (400 200 200)   // number of cells in each direction
            simpleGrading (1 1 1) // cell expansion ratios
        );
```

Pour plus de détails concernant l'utilitaire blockMesh, voir [blockMesh](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.3-mesh-generation-with-the-blockmesh-utility) dans le [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/).
****

## Caractéristiques de surfaceDict

La surfaceCaractéristiquesDict extrait et écrit toutes les caractéristiques de surface dans un fichier. Dans ce fichier, tous les fichiers {term}`STL` qui ont été enregistrés dans le dossier triSurface doivent être ajoutés comme suit:

```
    Air
    {
        surfaces
            ("Air.stl");
        includedAngle   180;

    // Write features to obj format for postprocessing
        writeObj                yes;
    }
```

La version complète de la surfaceCaractéristiquesDict pour le tutoriel actuel est enregistrée dans le dossier de cas.

****

## décomposéParDict

La décompositionParDict est utilisée pour décomposer un maillage et des champs d'un boîtier pour l'exécution parallèle. Lors d'une exécution parallèle, la géométrie doit d'abord être segmentée en géométries individuelles pour chaque processus [MPI (Message Passing Interface, une norme pour l'informatique parallèle)](https://www.mpi-forum.org/). L'entrée *number OfSubdomains* est obligatoire, et la méthode *Method* définit le type de méthode de décomposition. Plusieurs méthodes de décomposition sont disponibles. Par conséquent, le fichier *decomposerParDict* ci-dessous ne présente qu'une option exemplaire.

```
    numberOfSubdomains 8;
    method          simple;

    simpleCoeffs
    {
        n               (2 2 2);
        delta           0.001;
    }

    hierarchicalCoeffs
    {
        n               (1 1 1);
        delta           0.001;
        order           xyz;
    }

    manualCoeffs
    {
        dataFile        "";
    }

    distributed     no;

    roots           ( );
```

****

## SnappyHexMesh

Le dictionnaire snappyHexMeshDict contient une série de commandes qui contrôlent les différentes étapes du processus de maillage. Les principales sont les suivantes:

* *castellatedMesh* permet la création d'un maillage castellé (c.-à-d. raffiné).
* *snap* permet de casser la surface.
* *addLayers* permet l'insertion de la couche de surface.
* *géométrie* est une sous-diction de toute géométrie de surface utilisée.
* *castellatedMeshControls* est une sous-diction de contrôles pour les mailles castellées.
* *snapControls* est un sous-dictionnaire de contrôles pour les chocs de surface.
* *addLayersControls* est une sous-diction de contrôles pour l'addition de couches.
* *meshQualityControls* est une sous-diction des contrôles pour la qualité du maillage.
* *mergeTolérance* est la tolérance à la fusion en fraction du maillage initial.

Les étapes clés impliquées lors de l'exécution de snappyHexMesh sont:

1. {ref}`Castellation <of-mesh-castel>`: les cellules qui sont au-delà d'une région définie par un point prédéfini sont supprimées.
1. {ref}`Snapping <of-mesh-snap>`: reconstruit les cellules pour déplacer les bords de l'intérieur de la région à la limite requise.
1. {ref}`Layering <of-mesh-layer>`: crée des couches supplémentaires dans la région limite.
1. {ref}`Mesh quality <of-mesh-quality>`: contrôlez et vérifiez la qualité du maillage.

Pour cet exemple, l'option *add Layers*, qui permet l'ajout de couches visqueuses, a été définie à `false`.

```
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2.2.0                                 |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    object      snappyHexMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

// Which of the steps to run
castellatedMesh true;    // make basic mesh 
snap            true;    // decide to snap back to surface 
addLayers       false;   // decide to add viscous layers 
```

La sous-diction **GEOMETRY** énumère toutes les surfaces utilisées par snappyHexMeshDict, à l'exception de la géométrie blockMesh. En outre, il définit un nom pour chacun d'eux à utiliser comme référence comme indiqué dans l'exemple ci-dessous.

```
geometry // Load all the STL files here
{
  Air.stl {type triSurfaceMesh; name Air;}
  Concrete-sides.stl {type triSurfaceMesh; name Concrete-sides;}
  Gravel-bottom.stl {type triSurfaceMesh; name Gravel-bottom;}
  Inlet.stl {type triSurfaceMesh; name Inlet;}
  Obstacle.stl {type triSurfaceMesh; name Obstacle;}
  Outlet.stl {type triSurfaceMesh; name Outlet;}
};
```

(of-mesh-castel)=
### Castellation (Refinement)

Les paramètres **CastellatedMeshControls** permettent ensuite de définir le raffinement du maillage. Le niveau de raffinement peut être défini dans les sections *caractéristiques*, *raffinementSurfaces* et *raffinementRégions*. À partir du niveau 0, qui ne correspond à aucun raffinement, chaque niveau de raffinement ultérieur divise la cellule en 4 parties.

```{figure} ../../img/openfoam//snappyHexMesh/refinement-levels.png
:alt: openfoam 
:name: of-refinement-levels

Exemple de différents niveaux de raffinement des mailles.
```

En outre, les éléments suivants sont définis:

* *maxGlobalCells* : définit le nombre total de cellules limites.
* *maxLocalCells*: ce paramètre est utilisé en cas de fonctionnement parallèle et définit le nombre maximal de cellules pour chaque processeur.
* *nCellsBetweenLevels*: évite d'avoir des changements soudains de la taille des cellules, ce qui signifie que les changements consécutifs de niveau de raffinement se rapprochent.
  
Pour plus de détails sur ces paramètres, veuillez consulter la section [castellation et raffinement](https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh-castellation.html#meshing-snappyhexmesh-global-castellation) [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/).

```
castellatedMeshControls
{
    maxLocalCells 50000000;   // max cells per CPU core
    maxGlobalCells 500000000; // max cells to use before mesh deletion step
    minRefinementCells 0;     // was 0 - zero means no bad cells are allowed during refinement stages
    nCellsBetweenLevels 3;    // expansion factor between each high & low refinement zone

    // Explicit feature edge refinement
    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    features // taken from STL from each .eMesh file created by "SurfaceFeatureExtract" command
    (
      {file "Air.eMesh"; level 0;}
      {file "Concrete-sides.eMesh"; level 0;}
      {file "Gravel-bottom.eMesh"; level 0;}
      {file "Inlet.eMesh"; level 0;}
      {file "Obstacle.eMesh"; level 0;}
      {file "Outlet.eMesh"; level 0;}
    );

    // Surface based refinement
    // ~~~~~~~~~~~~~~~~~~~~~~~~

    refinementSurfaces // Surface-wise min and max refinement level
    {
      Air {level (0 0);}
      Concrete-sides {level (1 3);}
      Gravel-bottom {level (2 3);}
      Inlet {level (1 3);}
      Obstacle {level (3 3);}
      Outlet {level (2 3);}
    }

    resolveFeatureAngle 30;  // Resolve sharp angles // Default 30
    refinementRegions        // In descending levels of fineness
    allowFreeStandingZoneFaces true;
}
```

Dans la section *affinementSurfaces* de l'exemple ci-dessus, différents niveaux de raffinement ont été fixés pour chaque élément constitutif. On trouvera ci-après un exemple détaillé du raffinement qui en résulte pour les éléments de fond de gravier et d'obstacle.

```{figure} ../../img/openfoam/snappyHexMesh/obstacle-refinement.jpg
:alt: openfoam 
:name: of-obstacle-refinement

Raffinement résultant pour les éléments **Obstacle** et **Gravel-Bottom** composant le maillage.
```

Une fois que la fonctionnalité et le processus de fractionnement de surface sont terminés, le processus de suppression des cellules a lieu. Cette dernière nécessite une ou plusieurs régions entièrement enveloppées par une surface limite appartenant au domaine. Pour spécifier la région dans laquelle les cellules doivent être conservées, le mot clé *locationInMesh* doit être défini. Ce vecteur définit simplement la région qui veut être retenue.
 
```
locationInMesh (43.359 5 2.5803);  // to decide which side of mesh to keep **
```

(of-mesh-snap)=
### Snappage

Après avoir terminé les processus de division cellulaire et de suppression cellulaire, le processus **Snapping** peut avoir lieu. Cette tâche concerne le déplacement des points du vertex cellulaire sur la surface pour créer un maillage conforme, ce qui signifie que la géométrie d'entrée est conforme. Voici une liste des mots clés à définir:

* *nSmoothpatch*: définit le nombre d'itérations lissantes sur la surface.
* *Tolérance*: spécifie la région à l'intérieur de laquelle les points sont attirés par la surface.
* *nSolverIter*: définit le nombre d'itérations de déplacement de maillage.
* *nRelaxIter*: définit le nombre d'itérations de relaxation pendant le claquage.
* *nCaractéristiquesSnapIter*: définit le nombre d'itérations de relaxation utilisées pour se casser sur les fonctionnalités.
* *implicitFeatureSnap*: si activé, active la spécification implicite de la fonctionnalité.
* *explicitFeatureSnap* : si activé, il s'enclenche sur les fonctionnalités définies dans les fichiers *eMesh*.
* *MultiRégionCaractéristiquesSnap*: si également *expliciteCaractéristiquesSnap* est activé, les caractéristiques entre plusieurs surfaces seront capturées.

```
// Settings for the snapping.
snapControls
{
    nSmoothPatch    3;
    // nSmoothInternal $nSmoothPatch;
    tolerance       1.0;
    nSolveIter      600;
    nRelaxIter      5;

    // Feature snapping

        nFeatureSnapIter 10; // default is 10
        implicitFeatureSnap false; // default is false - detects without doing surfaceFeatureExtract
        explicitFeatureSnap true; // default is true
        multiRegionFeatureSnap true; // default is false - detects features between multiple surfaces
}
```

(of-mesh-layer)=
### Calibrage

Dans le cas où certaines cellules irrégulières sont présentes le long des limites du maillage obtenu avec l'étape de rupture, il est possible d'introduire des couches supplémentaires composées de cellules hexaédriques le long de la limite. Cette étape comprend le rétrécissement du maillage existant afin d'insérer la couche de cellules.

Les utilisateurs peuvent choisir entre 4 paramètres d'épaisseur de couche différents : *extensionRatio*, *finaleLayerThickness*, *premièreLayerThickness*, *épaisseur*. Dans cet exemple, n'en spécifiez que deux pour éviter une sur-spécification du problème. Les paramètres à définir ont les significations suivantes:

* *ExtensionRatio*: nécessaire pour calculer la taille relative à l'épaisseur prescrite de la première ou de la dernière couche.
* *minEpaisseur*: indique l'épaisseur minimale de la couche.
* *featureAngle*: représente la valeur au-dessus de laquelle le maillage n'est pas extrudé.
* *nRelaxIter*: indique le nombre d'étapes de relaxation.
* *minAxe médialAngle*: indique l'angle minimum pour sélectionner les points d'axe médial


Pour de plus amples renseignements, consulter la section [ajout de couche](https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh-layers.html#snappyhexmesh-layers-relativeSizes)] du [Guide de l'utilisateur OpenFOAM](https://doc.cfd.direct/openfoam/user-guide/).


```
// Settings for the layer addition.

addLayersControls 
//add the PATCH names from inside the STL file so STLpatchName-insideSTLName
 {
    relativeSizes false; 
    layers
    {
    }

    expansionRatio 1.0;
    finalLayerThickness 0.3; 
    minThickness 0.25; 
    nGrow 0; 

    // Advanced settings

    featureAngle 150;
    nRelaxIter 3;
    nSmoothSurfaceNormals 50;
    nSmoothNormals 3;
    nSmoothThickness 10; 
    maxFaceThicknessRatio 0.5; 
    maxThicknessToMedialRatio 0.3; 
    minMedianAxisAngle 90; 
    nBufferCellsNoExtrude 0;   
    nLayerIter 50; 
    NnRelaxedIter 20;
 }
```

(of-mesh-quality)=
### Contrôles de qualité du mesh

The final part of the *snappyHexMeshDict* file deals with the **Mesh Quality**. In this section, the values of the extrema encountered during the meshing process are defined. The purpose is to ensure an adequate quality of the resulting mesh. A comprehensive overview on the meaning of the mesh quality parameters can be found at [https://simscale.com/docs](https://www.simscale.com/docs/simulation-setup/meshing/mesh-quality/). The OpenFOAM keywords defining mesh quality parameters are (with <span style="color: #f2003c ">***highlighting of the most important***</span>, and <span style="color: #e68a19 ">***somewhat important***</span> parameters):
 
* <span style="color: #f2003c ">***maxNonOrtho***</span>: angle maximal de non-orthogonalité de la face, calculé comme le produit à point normalisé du vecteur de surface d'une cellule $i$ et le vecteur controïde à centroïde de deux cellules voisines $i$ et $j$.
* <span style="color: #e68a19 ">***maxBoundarySkewness***</span>: limite maximale skewness.
* <span style="color: #e68a19 ">***maxInternalSkewness***</span>: maximum de skewness interne face.
* <span style="color: #e68a19 ">***maxConcave***</span>: concavité cellulaire maximale pour vérifier le visage des angles intérieurs.
* <span style="color: #f2003c ">***minVol***</span>: volume minimal de pyramide cellulaire, calculé comme produit de point du vecteur de surface cellulaire et du centre cellulaire du vecteur de pic pyramidal.
* <span style="color: #e68a19 ">***minArea***</span>: zone minimale.
* <span style="color: #e68a19 ">***minTetQualité***</span>: qualité minimale du tétraèdre, une petite valeur positive pour assurer le succès des contrôles cellulaires.
* *minTwist*: produit à point normalisé du vecteur entre deux centres cellulaires voisins avec leur vecteur triangulaire de la surface du visage.
* <span style="color: #f2003c ">***minDeterminant***</span>: déterminant cellulaire minimum.
* <span style="color: #f2003c ">***minFaceWeight***</span>: poids minimal d'interpolation du visage, calculé comme le minimum des distances projetées $d_{prj}$ entre deux cellules voisines $i$ et $j$, notamment $\min (d_{prj, i}, d_{prj, j}) / (d_{prj, i} + d_{prj, j})$
* <span style="color: #f2003c ">***minVolRatio***</span>: rapport du minimum et maximum des volumes $V$ des cellules voisines $i$ et $j$; c'est-à-dire $\min(V_i, V_j) / \max(V_i, V_j)$.
* *minTriangleTwist*: le produit point de l'unité normale des éléments triangulaires voisins.
* *nSmoothScale*: lisser les itérations.
* *corrorReduction*: réduction des erreurs.


```
// Generic mesh quality settings

meshQualityControls
{
    maxNonOrtho 65;         // consider to set a limit of 45 deg
    maxBoundarySkewness 20; 
    maxInternalSkewness 4;  // however, skewness should not exceed 0.5
    maxConcave 80;
    minVol 1e-13;
    minTetQuality 1e-15;
    minArea -1;
    minTwist 0.02;
    minDeterminant 0.001;
    minFaceWeight 0.05;
    minVolRatio 0.01;
    minTriangleTwist -1;

    // Advanced
    nSmoothScale 4;
    errorReduction 0.75;
}

debug 0;

mergeTolerance 1E-6;
```
****



## Exécutez Meshing (BlockMesh)

Une fois que les mots-clés nécessaires ont été définis dans les dictionnaires requis, l'étape finale consiste en **commandes de lancement** dans le terminal dans l'ordre suivant:

* Exécutez la commande `blockMesh` pour créer le maillage de fond :

```
user@user123:~/OpenFOAM-9/channel/Mesh$ blockMesh
```

* Exécutez la commande `surfaceFeatures` pour créer les fichiers *.obj* et *.eMesh* des fichiers initialement importés {term}`STL`. Ces fichiers sont stockés dans le dossier *extensionFeatureEdgeMesh* (canal/constante/extensionFeatureEdgeMesh).
```
user@user123:~/OpenFOAM-9/channel/Mesh$ surfaceFeatures
```

* Pour les parcours parallèles, utilisez la commande `decomposePar` pour décomposer la géométrie en géométries individuelles pour chaque processus MPI.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ decomposePar
```

* Exécutez la commande `snappyHexMesh` pour générer le maillage :

    * Pour les parcours parallèles (suppléter "x" avec le nombre de carottes):

```
user@user123:~/OpenFOAM-9/channel/Mesh$ mpirun -np x snappyHexMesh -parallel
```

Sinon:

```
user@user123:~/OpenFOAM-9/channel/Mesh$ snappyHexMesh
```

* Pour les parcours parallèles, utilisez la commande `reconstructParMesh` pour reconstruire la géométrie.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ reconstructParMesh -constant
```

* Enfin, la qualité du maillage généré peut être analysée en tapant `checkMesh`.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ checkMesh
```

* Une génération réussie de mailles renvoie les données suivantes (ou similaires):

```
  Checking topology...
    Boundary definition OK.
    Cell to face addressing OK.
    Point usage OK.
    Upper triangular ordering OK.
    Face vertices OK.
    Number of regions: 1 (OK).

  Checking patch topology for multiply connected surfaces...
                   Patch    Faces   Points                  Surface topology
                     Air    12879    13927  ok (non-closed singly connected)
          Concrete-sides   103621   109304  ok (non-closed singly connected)
           Gravel-bottom   132062   136819  ok (non-closed singly connected)
                   Inlet      288      339  ok (non-closed singly connected)
                Obstacle    27076    27416  ok (non-closed singly connected)
                  Outlet    20610    21252  ok (non-closed singly connected)

  Checking geometry...
    Overall domain bounding box (-2.5 -1e-06 -1) (56.7409 10 6.2461)
    Mesh has 3 geometric (non-empty/wedge) directions (1 1 1)
    Mesh has 3 solution (non-empty) directions (1 1 1)
    Boundary openness (-5.71676e-15 7.42351e-15 8.33816e-16) OK.
    Max cell openness = 4.76547e-16 OK.
    Max aspect ratio = 7.03771 OK.
    Minimum face area = 3.89097e-05. Maximum face area = 0.0910262.  Face area magnitudes OK.
    Min volume = 2.62118e-06. Max volume = 0.0180894.  Total volume = 2271.44.  Cell volumes OK.
    Mesh non-orthogonality Max: 47.7783 average: 6.72481
    Non-orthogonality check OK.
    Face pyramids OK.
    Max skewness = 3.12739 OK.
    Coupled point location match (average 0) OK.

  Mesh OK.

  End
```

* Le maillage généré peut être visualisé dans ParaView en tapant `paraFoam` dans le terminal.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ paraFoam
```


## Visualisation des meshs

Pour visualiser le maillage généré dans ParaView, sélectionnez l'option *Appliquer* dans la section *Propriétés*.

```{figure} ../../img/openfoam/snappyHexMesh/paraFoam-mesh.png
:alt: openfoam snappyHexMesh paraFoam
:name: of-paraFoam-mesh

Visualisation du maillage résultant dans ParaView.
```

L'image ci-dessous met en évidence certaines fonctionnalités nécessaires pour visualiser adéquatement le maillage créé. Plus précisément, pour analyser les cellules, il est possible de sélectionner l'option *Surface avec Edge*. Les différents éléments composant le maillage peuvent ensuite être sélectionnés/désélectionnés pour analyser des parties spécifiques en détail. Enfin, dans le cas où le Mesh Check a retourné des erreurs, par exemple, des visages à haute inclinaison, ils peuvent être visualisés en sélectionnant l'option *Inclure les ensembles*.


```{figure} ../../img/openfoam/snappyHexMesh/paraFoam-mesh-cells.png
:alt: openfoam snappyHexMesh paraFoam
:name: of-paraFoam-mesh-cells

Visualisation du maillage résultant dans ParaView, mettant en évidence les cellules créées.
```
