---
description: Geometriegenerierung und -verzahnung für mehrphasige OpenFOAM-Wassersimulationen.
---

# Geometrie und Mesh Generation

Das Netz ist ein wesentlicher Bestandteil der numerischen Lösung und muss bestimmte Kriterien erfüllen, um eine gültige und präzise Lösung zu erhalten. Der folgende Abschnitt beschreibt die [snappyHexMesh utility](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.4-mesh-generation-with-the-snappyhexmesh-utility)] zum Erstellen von 3D-Netzen, die hexaedrische und geteilt-hexaedrische Zellen aus triangulierten Oberflächengeometrien enthalten.

Weitere Details zu den Mesh-Spezifikationen und Gültigkeitsbeschränkungen finden Sie in [Kapitel 4](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.1-mesh-description#x11-290004.1) des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/)]. Um snappyHexMesh auszuführen, sind zusätzlich zu einem vorhandenen Geometrie-Basis-Mesh folgende Dateien erforderlich:

```{figure} ../../img/openfoam/snappyHexMesh/folder-structure.png
:alt: openfoam 
:name: of-folder-structure

Fallverzeichnis, das die Dateien enthält, die zum Ausführen von snappyHexMesh erforderlich sind.
```

Die folgenden Abschnitte beschreiben die Schritte, die befolgt werden müssen.

## Erstellung des Hintergrunds Hex Mesh

Bevor Sie *snappyHexMesh* ausführen können, muss ein Hintergrundnetz erstellt werden, das durch hexaedrische Zellen gekennzeichnet ist. Dieses Mesh muss die gesamte Region enthalten, die mit * snappyHexMesh * in Eingriff gebracht werden soll, wie in der folgenden Abbildung gezeigt.

```{figure} ../../img/openfoam/snappyHexMesh/block-mesh-init.jpg
:alt: openfoam 
:name: of-block-mesh-init

Hintergrund-Mesh erstellt mit blockMesh enthält die Struktur zu vermaschten.
```

In der Datei *blockMeshDict* müssen die folgenden Elemente hinzugefügt werden:

* Skalierungsfaktor für die Scheitelpunktkoordinaten

```
   convertToMeters 1;
```
  
* Koordinaten der Eckpunkte des Hintergrundgitters

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

*  Koordinaten der Eckpunkte in der nachstehend angegebenen Reihenfolge

```{figure} ../../img/openfoam/snappyHexMesh/block-mesh-vertexorder.png
:alt: openfoam 
:name: of-block-mesh-vertexorder

Hintergrund-Mesh zeigt die Reihenfolge an, in der die Eckpunkte in die Block-MeshDict-Datei geschrieben werden.
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

Für weitere Details zum blockMesh-Dienstprogramm siehe [blockMesh](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.3-mesh-generation-with-the-blockmesh-utility) im [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/)].
******

## SurfaceFeaturesDict

Die surfaceFeaturesDict extrahiert und schreibt alle Oberflächenmerkmale in eine Datei. In dieser Datei müssen alle {term}`STL` Dateien, die im triSurface-Ordner gespeichert wurden, wie folgt hinzugefügt werden:

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

Die vollständige Version des surfaceFeaturesDict für das aktuelle Tutorial wird im Fallordner gespeichert.

******

## decomposeParDict

Der decomposeParDict wird verwendet, um ein Mesh und Felder eines Cases zur parallelen Ausführung zu zerlegen. Beim Parallellauf muss die Geometrie zunächst für jeden [MPI (Message Passing Interface, ein Standard für Parallel Computing)](https://www.mpi-forum.org/)-Prozess in einzelne Geometrien segmentiert werden. Der Eintrag *numberOfSubdomains* ist obligatorisch, und die *Methode* definiert den Typ der Zerlegungsmethode. Es stehen mehrere Zersetzungsverfahren zur Verfügung. Daher stellt die unten gezeigte Datei *decomposeParDict* nur eine beispielhafte Option dar.

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

******

## SnappyHexMesh

Das snappyHexMeshDict Wörterbuch enthält eine Reihe von Befehlen, die die verschiedenen Schritte des Meshing-Prozesses steuern. Die wichtigsten sind die folgenden:

* *castellatedMesh* ermöglicht die Erstellung eines castellierten (d.h. verfeinerten) Netzes.
* *snap* ermöglicht den Surface Snaping Stage.
* *addLayers* ermöglicht das Einfügen der Oberflächenschicht.
* *Geometrie* ist ein Unterwörterbuch aller verwendeten Oberflächengeometrien.
* *castellatedMeshControls* ist ein Unterwörterbuch von Kontrollen für kastrierte Maschen.
* *snapControls* ist ein Sub-Wörterbuch von Steuerelementen für Oberflächen-Snapping.
* *addLayersControls* ist ein Unterwörterbuch von Steuerelementen für das Hinzufügen von Schichten.
* *meshQualityControls* ist ein Unterwörterbuch der Kontrollen für Mesh-Qualität.
* *mergeTolerance* ist die Merge-Toleranz als Bruchteil des ursprünglichen Bounding Mesh.

Die wichtigsten Schritte beim Ausführen von snappyHexMesh sind:

1. {ref}`Castellation <of-mesh-castel>`: Die Zellen, die sich außerhalb einer Region befinden, die durch einen vordefinierten Punkt definiert ist, werden entfernt.
1. {ref}`Snapping <of-mesh-snap>`: rekonstruiert die Zellen, um die Kanten aus dem Inneren der Region an die erforderliche Grenze zu bewegen.
1. {ref}`Layering <of-mesh-layer>`: Erstellt zusätzliche Schichten in der Grenzregion.
1. {ref}`Mesh quality <of-mesh-quality>`: Kontrolle und Überprüfung der Qualität des Netzes.

For this example, the *add Layers* option, which enables the addition of viscous layers, was set to `false`.

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

Das **GEOMETRY-Unterwörterbuch** listet alle von snappyHexMeshDict verwendeten Oberflächen mit Ausnahme der blockMesh-Geometrie auf. Darüber hinaus definiert es einen Namen für jeden von ihnen, der als Referenz verwendet werden soll, wie im folgenden Beispiel gezeigt.

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
### Castellation (Raffination)

Die Einstellungen **CastellatedMeshControls** erlauben dann die Definition der Mesh-Verfeinerung. Der Verfeinerungsgrad kann in den Abschnitten *features*, *refinementSurfaces* und *refinementRegions* festgelegt werden. Ausgehend von Stufe 0, die keiner Verfeinerung entspricht, teilt jede nachfolgende Verfeinerungsebene die Zelle in 4 Teile.

```{figure} ../../img/openfoam//snappyHexMesh/refinement-levels.png
:alt: openfoam 
:name: of-refinement-levels

Beispiel für verschiedene Maschenveredelungsstufen.
```

Zusätzlich werden folgende Elemente festgelegt:

* *maxGlobalCells*: definiert die Gesamtanzahl der Zellen.
* *maxLocalCells*: Diese Einstellung wird im Falle eines Parallellaufs verwendet und definiert die maximale Anzahl von Zellen für jeden Prozessor.
* *nCellsBetweenLevels*: vermeidet plötzliche Änderungen der Zellengröße, d.h. aufeinanderfolgende Änderungen der Verfeinerungsebenen.
  
Weitere Details zu diesen Einstellungen finden Sie im Abschnitt [castellation and refinement](https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh-castellation.html#meshing-snappyhexmesh-global-castellation)] des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/)].

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

In dem im obigen Beispiel gezeigten Abschnitt *refinementSurfaces* wurden für jedes konstituierende Element unterschiedliche Veredelungsstufen festgelegt. Ein detailliertes Beispiel der resultierenden Ausgestaltung für die Schotterboden- und Hinderniselemente ist im Folgenden dargestellt.

```{figure} ../../img/openfoam/snappyHexMesh/obstacle-refinement.jpg
:alt: openfoam 
:name: of-obstacle-refinement

Resultierende Verfeinerung der **Obstacle**- und **Gravel-Bottom**-Elemente, aus denen das Netz besteht.
```

Sobald der Feature- und Oberflächenaufteilungsprozess abgeschlossen ist, findet der Zellentfernungsprozess statt. Letzteres erfordert einen oder mehrere Bereiche, die vollständig von einer zur Domäne gehörenden Begrenzungsfläche umhüllt sind. Um die Region anzugeben, in der die Zellen gehalten werden müssen, muss das Schlüsselwort *locationInMesh* definiert werden. Dieser Vektor definiert einfach die Region, die beibehalten werden möchte.
 
```
locationInMesh (43.359 5 2.5803);  // to decide which side of mesh to keep **
```

(of-mesh-snap)=
### Einrasten

Nach Abschluss der Zellteilung und Zellentfernung kann der **Snapping**-Prozess stattfinden. Diese Aufgabe befasst sich mit dem Bewegen der Zellscheitelpunkte auf der Oberfläche, um ein konformes Netz zu erzeugen, dh die Eingabegeometrie anzupassen. Hier ist eine Liste der zu setzenden Keywords:

* *nSmoothpatch*: definiert die Anzahl der Glättungs-Iterationen entlang der Oberfläche.
* *Toleranz*: gibt die Region entlang der Oberfläche an, in der die Punkte von der Oberfläche angezogen werden.
* *nSolverIter*: definiert die Anzahl der Mesh Displacement Iterationen.
* *nRelaxIter*: definiert die Anzahl der Entspannungs-Iterationen während des Schnappvorgangs.
* *nFeatureSnapIter*: definiert die Anzahl der Entspannungs-Iterationen, die für das Einrasten auf die Funktionen verwendet werden.
* *implicitFeatureSnap*: falls aktiviert, aktiviert die implizite Feature-Spezifikation.
* *explicitFeatureSnap*: Wenn aktiviert, schnappt es das Mesh auf die in den *eMesh*-Dateien definierten Funktionen.
* *multiRegionFeatureSnap*: Wenn auch *explicitFeatureSnap* aktiviert ist, werden die Features zwischen mehreren Flächen erfasst.

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

Für den Fall, daß einige unregelmäßige Zellen entlang der Grenzen in dem mit der Schnappstufe erhaltenen Netz vorhanden sind, ist es möglich, zusätzliche Schichten aus hexaedrischen Zellen entlang der Grenze einzubringen. Diese Phase beinhaltet das Schrumpfen des vorhandenen Netzes, um die Zellschicht einzufügen.

Benutzer können zwischen 4 verschiedenen Schichtdickenparametern wählen: *expansionRatio*, *finalLayerThickness*, *firstLayerThickness*, *dicke*. Geben Sie in diesem Beispielfall nur zwei an, um eine Überspezifikation des Problems zu vermeiden. Die einzustellenden Parameter haben folgende Bedeutung:

* *ExpansionRatio*: notwendig, um die relative Größe zur vorgeschriebenen Dicke der ersten oder letzten Schicht zu berechnen.
* *min Dicke*: zeigt die minimale Dicke der Schicht an.
* *featureAngle*: steht für den Wert, oberhalb dessen das Netz nicht extrudiert wird.
* *nRelaxIter*: gibt die Anzahl der Entspannungsschritte an.
* *minMedialAxisAngle*: Zeigt den Mindestwinkel zur Auswahl der Mittelachsenpunkte an


Weitere Details finden Sie im Abschnitt [Layer addition](https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh-layers.html#snappyhexmesh-layers-relativeSizes)] des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/)].


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
 
* <span style="color: #f2003c ">***maxNonOrtho***</span>: maximaler Gesichtswinkel ohne Orthogonalität, berechnet als normalisiertes Punktprodukt des Oberflächenvektors einer Zelle $i$ und des Controid-zu-Center-Vektors zweier benachbarter Zellen $i$ und $j$.
* <span style="color: #e68a19 ">***maxBoundarySkewness***</span>: maximale Randneigung.
* <span style="color: #e68a19 ">***maxInternalSkewness***</span>: maximale innere Gesichtsneigung.
* <span style="color: #e68a19 ">***maxConcave***</span>: maximale Zellenkonkavität, um die Fläche der Innenwinkel zu überprüfen.
* <span style="color: #f2003c ">***minVol***</span>: minimales Zellpyramidenvolumen, berechnet als Punktprodukt des Zelloberflächenvektors und des Zellzentrums-Peakvektors.
* <span style="color: #e68a19 ">***minArea***</span>: Mindestfläche.
* <span style="color: #e68a19 ">***minTetQuality***</span>: minimale Tetraederqualität, ein kleiner positiver Wert, um sicherzustellen, dass die Zellprüfungen erfolgreich verlaufen.
* *minTwist*: normiertes Punktprodukt des Vektors zwischen zwei benachbarten Zellzentren mit ihrem dreieckigen Flächenvektor.
* <span style="color: #f2003c ">***minDeterminant***</span>: minimale Zelldeterminante.
* <span style="color: #f2003c ">***minFaceWeight***</span>: minimales Flächeninterpolationsgewicht, berechnet als Minimum der projizierten Abstände $d_{prj}$ zwischen zwei benachbarten Zellen $i$ und $j$, insbesondere $\min (d_{prj, i}, d_{prj, j}) / (d_{prj, i} + d_{prj, j})$
* <span style="color: #f2003c ">***minVolRatio***</span>: Verhältnis von minimalem und maximalem Volumen $V$ benachbarter Zellen $i$ und $j$, das heißt $\min(V_i, V_j) / \max(V_i, V_j)$.
* *minTriangleTwist*: das Punktprodukt der Einheitsnormalen benachbarter Dreieckselemente.
* *nSmoothScale*: glättende Iterationen.
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
******



## Run Meshing (blockMesh)

Sobald die notwendigen Schlüsselwörter in den erforderlichen Wörterbüchern definiert sind, besteht der letzte Schritt darin, Befehle** im Terminal in folgender Reihenfolge auszuführen:

* Führen Sie den Befehl `blockMesh` aus, um das Hintergrund-Mesh zu erstellen:

```
user@user123:~/OpenFOAM-9/channel/Mesh$ blockMesh
```

* Führen Sie den Befehl `surfaceFeatures` aus, um die Dateien *.obj* und *.eMesh* aus den ursprünglich importierten {term}`STL`-Dateien zu erstellen. Diese Dateien werden im Ordner *extendedFeatureEdgeMesh* (channel/constant/extendedFeatureEdgeMesh) gespeichert.
```
user@user123:~/OpenFOAM-9/channel/Mesh$ surfaceFeatures
```

* Verwenden Sie für Parallelläufe den Befehl `decomposePar`, um die Geometrie für jeden MPI-Prozess in einzelne Geometrien zu zerlegen.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ decomposePar
```

* Führen Sie den Befehl `snappyHexMesh` aus, um das Mesh zu generieren:

    * Bei Parallelläufen (ersetzen Sie "x" durch die Anzahl der Kerne):

```
user@user123:~/OpenFOAM-9/channel/Mesh$ mpirun -np x snappyHexMesh -parallel
```

Alternativ:

```
user@user123:~/OpenFOAM-9/channel/Mesh$ snappyHexMesh
```

* Verwenden Sie für Parallelläufe den Befehl `reconstructParMesh`, um die Geometrie zu rekonstruieren.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ reconstructParMesh -constant
```

* Finally, the quality of the generated mesh can be analyzed by typing `checkMesh`.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ checkMesh
```

* Eine erfolgreiche Mesh-Generation gibt folgendes (oder ähnliches) zurück:

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

* Das erzeugte Mesh kann in ParaView visualisiert werden, indem man `paraFoam` im Terminal eingibt.

```
user@user123:~/OpenFOAM-9/channel/Mesh$ paraFoam
```


## Mesh Visualisierung

Um das generierte Mesh in ParaView zu visualisieren, wählen Sie im Abschnitt *Eigenschaften* die Option *Anwenden* aus.

```{figure} ../../img/openfoam/snappyHexMesh/paraFoam-mesh.png
:alt: openfoam snappyHexMesh paraFoam
:name: of-paraFoam-mesh

Visualisierung des resultierenden Mesh in ParaView.
```

Das Bild unten zeigt einige Funktionen, die erforderlich sind, um das erstellte Mesh angemessen zu visualisieren. Um die Zellen zu analysieren, ist es insbesondere möglich, die Option *Oberfläche mit Edges * auszuwählen. Die verschiedenen Elemente, aus denen das Netz besteht, können dann ausgewählt / ausgewählt werden, um bestimmte Teile im Detail zu analysieren. Schließlich, in dem Fall, in dem der Mesh Check Fehler zurückgegeben hat, zum Beispiel mit einer hohen Schieflage konfrontiert ist, können sie durch die Auswahl der Option *Include Sets * visualisiert werden.


```{figure} ../../img/openfoam/snappyHexMesh/paraFoam-mesh-cells.png
:alt: openfoam snappyHexMesh paraFoam
:name: of-paraFoam-mesh-cells

Visualisierung des resultierenden Mesh in ParaView, Hervorhebung der erstellten Zellen.
```
