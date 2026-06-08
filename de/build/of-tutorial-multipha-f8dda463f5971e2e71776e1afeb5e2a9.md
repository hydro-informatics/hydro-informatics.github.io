---
description: Geometrie-Generation und Meshing für OpenFOAM Mehrphasen-Wassersimulationen.
---

# Geometrie und Mesh Generation

Das Netz ist ein wesentlicher Bestandteil der numerischen Lösung und muss bestimmte Kriterien erfüllen, um eine gültige und präzise Lösung zu erzeugen. Der folgende Abschnitt beschreibt die [snappyHexMesh Utility](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.4-mesh-generation-with-the-snappyhexmesh-utility) zur Erstellung von 3d Maschen, die Hexaedral- und Split-Hexedralzellen aus triangulierten Oberflächengeometrien enthalten.

Weitere Einzelheiten zu den Netzspezifikationen und Gültigkeitsbeschränkungen finden Sie unter [Kapitel 4](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.1-mesh-description#x11-290004.1) des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/). Um SnappyHexMesh zu betreiben, sind neben einem vorhandenen Geometrie-Basisnetz die folgenden Dateien erforderlich:

```{figure} ../../img/openfoam/snappyHexMesh/folder-structure.png
:alt: openfoam 
:name: of-folder-structure

Case-Verzeichnis mit den Dateien, die erforderlich sind, um SnappyHexMesh auszuführen.
```

In den folgenden Abschnitten werden die zu verfolgenden Schritte beschrieben.

## Erstellung des Hintergrunds Hex Mesh

Bevor Sie *snappyHexMesh* ausführen können, muss ein von hexahedralen Zellen charakterisiertes Hintergrundnetz erstellt werden. Dieses Netz muss die gesamte Region enthalten, die mit *snappyHexMesh* kämmt werden sollte, wie in der Abbildung unten gezeigt.

```{figure} ../../img/openfoam/snappyHexMesh/block-mesh-init.jpg
:alt: openfoam 
:name: of-block-mesh-init

Hintergrundgitter mit BlockMesh, die die zu netzende Struktur enthält.
```

In der Datei *blockMeshDict* müssen folgende Elemente hinzugefügt werden:

* der Skalierungsfaktor für die Scheitelkoordinaten

```
   convertToMeters 1;
```
  
* Koordinaten der Wirbel des Hintergrundnetzes

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

*  Koordinaten der Vertiken nach der unten angegebenen Reihenfolge

```{figure} ../../img/openfoam/snappyHexMesh/block-mesh-vertexorder.png
:alt: openfoam 
:name: of-block-mesh-vertexorder

Hintergrundnetz, das die Reihenfolge angibt, in der die Vertiken in der Block-meshDict-Datei geschrieben werden.
```

* eine geordnete Liste von Vertex-Etiketten und Maschengröße

```
    blocks
        (
            hex (0 1 2 3 4 5 6 7)   // vertex numbers
            (400 200 200)   // number of cells in each direction
            simpleGrading (1 1 1) // cell expansion ratios
        );
```

Für weitere Details zum blockMesh-Dienstprogramm siehe [blockMesh](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.3-mesh-generation-with-the-blockmesh-utility) in der [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/).
***

## OberflächeFeaturesDict

Die OberflächeFeaturesDict extrahiert und schreibt alle Oberflächenmerkmale einer Datei. In dieser Datei müssen alle im Ordner triSurface gespeicherten {term}`STL` Dateien wie folgt hinzugefügt werden:

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

Die komplette Version der OberflächeFeaturesDict für das aktuelle Tutorial wird im Fallordner gespeichert.

***

## Das ist nicht möglich.

Der decomposeParDict wird verwendet, um ein Netz und Felder eines Gehäuses für die parallele Ausführung zu zersetzen. Bei Parallellauf muss die Geometrie zunächst in einzelne Geometrien für jeden [MPI (Message Passing Interface, Standard für Parallel Computing)](https://www.mpi-forum.org/)Prozess segmentiert werden. Der Eintrag *numberOfSubdomains* ist obligatorisch und der *Method* definiert den Zersetzungstyp. Es stehen mehrere Zersetzungsverfahren zur Verfügung. Daher stellt die unten angezeigte *decomposeParDict*-Datei nur eine beispielhafte Option dar.

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

***

## Und was?

Das SnappyHexMeshDict Wörterbuch enthält eine Reihe von Befehlen, die die verschiedenen Schritte des Meshing-Prozesses steuern. Die wichtigsten sind:

* *castellatedMesh* ermöglicht die Schaffung eines kastellierten (d.h. raffinierten) Netzes.
* *snap* ermöglicht die Oberflächenschnappstufe.
* *addLayers* ermöglicht das Einführen der Oberflächenschicht.
* *geometry* ist ein Unterdiktionär aller verwendeten Oberflächengeometrien.
* *castellatedMeshControls* ist ein Unterdiktionär von Steuerungen für kastelliertes Netz.
* *snapControls* ist ein Unterdiktionär von Steuerungen für das Oberflächenschnappen.
* *addLayersControls* ist ein Unterdiktionär für die Schichtzugabe.
* *meshQualityControls* ist ein Unterdiktionär für die Netzqualität.
* *mergeTolerance* ist die MergeToleranz* als Bruchteil des anfänglichen Grenzgewebes.

Die wichtigsten Schritte bei der Ausführung von SnappyHexMesh sind:

1. {ref}`Castellation <of-mesh-castel>`: Die Zellen, die über eine durch einen vorgegebenen Punkt definierte Region hinausgehen, werden entfernt.
1. {ref}`Snapping <of-mesh-snap>`: rekonstruiert die Zellen, um die Kanten von innerhalb der Region auf die erforderliche Grenze zu bewegen.
1. {ref}`Layering <of-mesh-layer>`: schafft zusätzliche Schichten in der Grenzregion.
1. {ref}`Mesh quality <of-mesh-quality>`: Kontrolle und Überprüfung der Qualität des Netzes.

Für dieses Beispiel wurde die *add Layers*-Option, die den Zusatz von viskosen Schichten ermöglicht, auf `false` gesetzt.

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

Das **GEOMETRY Subdictionary** listet alle von SnappyHexMeshDict verwendeten Oberflächen auf, mit Ausnahme der blockMesh Geometrie. Darüber hinaus definiert es einen Namen, für den jeder von ihnen als Referenz verwendet wird, wie im folgenden Beispiel gezeigt.

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

Die **CastellatedMeshControls**-Einstellungen ermöglichen dann die Definition der Netzverfeinerung. Die Verfeinerung kann in den Abschnitten *features*, *refinementSurfaces* und *refinementRegions* eingestellt werden. Ausgehend von der Ebene 0, die keiner Verfeinerung entspricht, teilt jede nachfolgende Verfeinerungsebene die Zelle in 4 Teilen.

```{figure} ../../img/openfoam//snappyHexMesh/refinement-levels.png
:alt: openfoam 
:name: of-refinement-levels

Beispiel für unterschiedliche Maschenveredelungsstufen.
```

Zusätzlich werden die folgenden Artikel eingestellt:

* *maxGlobalCells*: definiert die Gesamtzahl der Zellen.
* *maxLocalCells*: Diese Einstellung wird bei Parallellauf verwendet und definiert die maximale Anzahl der Zellen für jeden Prozessor.
* *nCellsBetweenLevels*: Vermeidet plötzliche Zellgrößenänderungen, d.h. aufeinanderfolgende Veredelungsebenenänderungen schließen zusammen.
  
Weitere Einzelheiten zu diesen Einstellungen finden Sie in der Rubrik [castellation and refine](https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh-castellation.html#meshing-snappyhexmesh-global-castellation)] des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/).

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

In dem im obigen Beispiel dargestellten Abschnitt *RefinementSurfaces* wurden für jedes Bestandteilelement unterschiedliche Verfeinerungsstufen eingestellt. Nachfolgend wird ein detailliertes Beispiel für die sich ergebende Verfeinerung für die Kiesboden- und Hinderniselemente gezeigt.

```{figure} ../../img/openfoam/snappyHexMesh/obstacle-refinement.jpg
:alt: openfoam 
:name: of-obstacle-refinement

Ergebnisende Verfeinerung für die Elemente **Obstacle** und **Gravel-Bottom****, die das Netz komponieren.
```

Sobald der Funktions- und Oberflächenspaltvorgang abgeschlossen ist, erfolgt der Zellabtrag. Letzteres erfordert einen oder mehrere Bereiche, die vollständig von einer Begrenzungsfläche des Domänens umhüllt sind. Um die Region anzugeben, in der die Zellen gehalten werden müssen, muss das Schlüsselwort *locationInMesh* definiert werden. Dieser Vektor definiert einfach den Bereich, der zurückgehalten werden will.
 
```
locationInMesh (43.359 5 2.5803);  // to decide which side of mesh to keep **
```

(of-mesh-snap)=
### Schnappen

Nach beendeter Zellteilung und Zellabspaltung kann der **Snapping**-Prozess stattfinden. Diese Aufgabe beschäftigt sich mit dem Bewegen der Zell-Schnittpunkte auf der Oberfläche, um ein konformes Netz zu schaffen, was die Eingangsgeometrie entspricht. Hier eine Liste der Keywords, die gesetzt werden sollen:

* *nSmoothpatch*: definiert die Anzahl der glättenden Iterationen entlang der Oberfläche.
* *Toleranz*: Gibt den Bereich entlang der Oberfläche an, in dem die Punkte von der Oberfläche angezogen werden.
* *nSolverIter*: definiert die Anzahl der Mesh-Verschiebungen.
* *nRelaxIter*: definiert die Anzahl der Entspannungs Iterationen während des Snappings.
* *nFeatureSnapIter*: definiert die Anzahl der Entspannungs Iterationen, die zum Aufschnappen auf die Features verwendet werden.
* *implicitFeatureSnap*: Wenn aktiviert, aktiviert die implizite Feature-Spezifikation.
* *explicitFeatureSnap*: Wenn aktiviert, schnappt es das Netz auf die in den *eMesh*-Dateien definierten Funktionen.
* *multiRegionFeatureSnap*: Wenn auch *explicitFeatureSnap* aktiviert ist, werden die Eigenschaften zwischen mehreren Oberflächen erfasst.

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
### Schichtung

Falls in dem mit der Schnappstufe erhaltenen Mesh einige unregelmäßige Zellen entlang der Grenzen vorhanden sind, können zusätzliche Schichten aus hexahedralen Zellen entlang der Grenze eingebracht werden. Diese Stufe beinhaltet das Schrumpfen des vorhandenen Netzes, um die Zellenschicht einzufügen.

Benutzer können zwischen 4 verschiedenen Schichtdickenparametern wählen: *expansionRatio*, *finalLayerThickness*, *firstLayerThickness*, *thickness*. Geben Sie in diesem Beispiel nur zwei an, um eine Überspezifikation des Problems zu vermeiden. Die einzustellenden Parameter haben folgende Bedeutungen:

* *expansionRatio*: notwendig, um die relative Größe auf die vorgeschriebene Dicke der ersten oder letzten Schicht zu berechnen.
* *minThickness*: zeigt die Mindestdicke der Schicht an.
* *featureAngle*: stellt den Wert dar, über dem das Netz nicht extrudiert wird.
* *nRelaxIter*: gibt die Anzahl der Entspannungsschritte an.
* *minMedialAxisAngle*: Zeigt den minimalen Winkel an, um die medialen Achsenpunkte auszuwählen


Weitere Einzelheiten finden Sie im Abschnitt [layer add](https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh-layers.html#snappyhexmesh-layers-relativeSizes) des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/).


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
### Mesh Qualitätskontrollen

The final part of the *snappyHexMeshDict* file deals with the **Mesh Quality**. In this section, the values of the extrema encountered during the meshing process are defined. The purpose is to ensure an adequate quality of the resulting mesh. A comprehensive overview on the meaning of the mesh quality parameters can be found at [https://simscale.com/docs](https://www.simscale.com/docs/simulation-setup/meshing/mesh-quality/). The OpenFOAM keywords defining mesh quality parameters are (with <span style="color: #f2003c ">***highlighting of the most important***</span>, and <span style="color: #e68a19 ">***somewhat important***</span> parameters):
 
* <span style="color: #f2003c ">***maxNonOrtho****</span>: Maximaler Gesichts-Nichtorthogonalitätswinkel, berechnet als normalisiertes Punktprodukt des Oberflächenvektors einer Zelle $i$ und des controid-to-centroid Vektors zweier benachbarter Zellen $i$ und $j$.
* <span style="color: #e68a19 ">***maxBoundarySkewness***</span>: Maximale Grenzgeschwindigkeit.
* <span style="color: #e68a19 ">***maxInternalSkewness***</span>: maximale innere Gesichtskewness.
* <span style="color: #e68a19 ">***maxConcave***</span>: Maximale Zellkonkavität, um das Gesicht der Innenwinkel zu überprüfen.
* <span style="color: #f2003c ">****minVol**</span>: Mindestzellpyramidvolumen, berechnet als Punktprodukt des Zelloberflächenvektors und des Zellzentrums zum Pyramidenspitzenvektor.
* <span style="color: #e68a19 ">****minArea**</span>: Mindestfläche.
* <span style="color: #e68a19 ">****minTetQuality***</span>: Mindestqualität von Tetraeder, ein kleiner positiver Wert, um sicherzustellen, dass die Zellkontrollen erfolgreich verlaufen.
* *minTwist*: normalisiertes Punktprodukt des Vektors zwischen zwei benachbarten Zellzentren mit ihrem dreieckigen Flächenvektor.
* <span style="color: #f2003c ">****minDeterminant**</span>: Mindestzelldeterminant.
* <span style="color: #f2003c ">***minFaceWeight***</span>: Mindestflächeninterpolationsgewicht, berechnet als Minimum der projizierten Entfernungen $d_{prj}$ zwischen zwei benachbarten Zellen $i$ und $j$, insbesondere $\min (d_{prj, i}, d_{prj, j}) / (d_{prj, i} + d_{prj, j})$
* <span style="color: #f2003c ">***minVolRatio***</span>: ratio of the minimum and maximum of volumes $V$ of neighboring cells $i$ and $j$; that is, $\min(V_i, V_j) / \max(V_i, V_j)$.
* *minTriangleTwist*: das Punktprodukt der Einheit Normalen von benachbarten dreieckigen Elementen.
* *nSmoothScale*: Glätten Iterationen.
* *errorReduction*: Fehlerreduktion.


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
***



## Meshing starten (blockMesh)

Nachdem die erforderlichen Keywords in den erforderlichen Wörterbüchern definiert wurden, besteht der letzte Schritt in **running-Befehlen** im Terminal in folgender Reihenfolge:

* Führen Sie den Befehl `blockMesh` aus, um das Hintergrundnetz zu erstellen:

```
user@user123:~/OpenFOAM-9/channel/Mesh$ blockMesh
```

* Führen Sie den Befehl `surfaceFeatures` aus, um die *.obj* und *.eMesh*-Dateien aus den ursprünglich importierten {term}`STL`-Dateien zu erstellen. Diese Dateien werden im Ordner *extendedFeatureEdgeMesh* (channel/constant/extendedFeatureEdgeMesh) gespeichert.
```
user@user123:~/OpenFOAM-9/channel/Mesh$ surfaceFeatures
```

* Für Parallelläufe verwenden Sie den `decomposePar` Befehl, um die Geometrie in einzelne Geometrien für jeden MPI-Prozess zu zerlegen.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ decomposePar
```

* Führen Sie den Befehl `snappyHexMesh` aus, um das Netz zu erzeugen:

    * Für Parallelläufe (Substitute "x" mit der Anzahl der Kerne):

```
user@user123:~/OpenFOAM-9/channel/Mesh$ mpirun -np x snappyHexMesh -parallel
```

Alternativ:

```
user@user123:~/OpenFOAM-9/channel/Mesh$ snappyHexMesh
```

* Für Parallelläufe verwenden Sie den `reconstructParMesh` Befehl, um die Geometrie zu rekonstruieren.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ reconstructParMesh -constant
```

* Schließlich kann die Qualität des erzeugten Netzes durch Eingabe von `checkMesh` analysiert werden.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ checkMesh
```

* Eine erfolgreiche Mesh-Generation liefert folgende (oder ähnliche):

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

* Das generierte Mesh kann in ParaView durch Eingabe von `paraFoam` im Terminal visualisiert werden.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ paraFoam
```


## Mesh Visualisierung

Um das generierte Mesh in ParaView zu visualisieren, wählen Sie im Abschnitt *Properties* die *Apply* Option.

```{figure} ../../img/openfoam/snappyHexMesh/paraFoam-mesh.png
:alt: openfoam snappyHexMesh paraFoam
:name: of-paraFoam-mesh

Visualisierung des resultierenden Netzes in ParaView.
```

Das Bild unten zeigt einige Features, die erforderlich sind, um das erstellte Mesh angemessen zu visualisieren. Speziell zur Analyse der Zellen ist es möglich, die Option *Surface with Edges* auszuwählen. Die verschiedenen Elemente, die das Netz zusammensetzen, können dann ausgewählt/entwickelt werden, um bestimmte Teile im Detail zu analysieren. Schließlich können sie in dem Fall, in dem der Mesh Check Fehler zurückgegeben hat, z.B. Gesichter mit hoher Skewness durch Auswahl der *Include Sets* Option visualisiert werden.


```{figure} ../../img/openfoam/snappyHexMesh/paraFoam-mesh-cells.png
:alt: openfoam snappyHexMesh paraFoam
:name: of-paraFoam-mesh-cells

Visualisierung des resultierenden Meshs in ParaView, das die erstellten Zellen hervorhebt.
```
