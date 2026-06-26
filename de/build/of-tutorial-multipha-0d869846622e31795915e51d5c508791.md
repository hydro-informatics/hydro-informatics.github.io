---
description: Tutorial für OpenFOAMs InterFoam für Wassersimulationen.
---

# Mehrphasiger Solver (interFoam Tutorial)

In diesem Tutorial lösen wir ein Problem eines 50-m langen geraden Kanals mit zwei Becken, eine kleinere am Einlass, und eine größere am Auslass, und ein Hindernis in der Mitte.

```{figure} ../../img/openfoam/blender/study-area.jpg
:alt: openfoam 
:name: of-study-area

3D Ansicht der analysierten Struktur.
```

In this case, we will use the multiphase solver interFoam coupled with a {term}`k <Turbulent kinetic energy>` - $\epsilon$ (epsilon) turbulence model. interFoam identifies the water-air interface based on the Volume of Fluid (VOF) method, which solves the transport equations for a single or multiple phase fractions alpha, where alpha is 0.5 at the interface between the fluids (see [OpenFOAM Standard Solvers](https://www.openfoam.com/documentation/user-guide/a-reference/a.1-standard-solvers)). Additionally, we will focus on the implementation of multiple roughness zones related to the engineered and nature-oriented elements present in the model, and we will apply a specific roughness height. 

```{figure} ../../img/openfoam/blender/channel-view2-final.jpg
:alt: openfoam 
:name: of-channel-view2-final

3D Ansicht der analysierten Struktur in Strömungsrichtung, die die zugeordneten Materialien hervorhebt.
```

Der Fallordner mit allen notwendigen Dateien kann heruntergeladen werden [here](https://github.com/hydro-informatics/openfoam.git).

***
## Dateiimport
Der erste Abschnitt dieses Tutorials beschäftigt sich mit dem Import der zunächst erstellten Geometrie. Alle Dateien wurden mit Blender erstellt, die ein kostenloses und Open-Source 3D-Computergrafik-Software-Tool-Set ist. Die Geometrie wurde in einzelne Elemente auf Basis ihres komponierenden Materials und nach den im Meshprozess zu verfeinernden Bereichen unterteilt. Daher wurden für das vorliegende Beispiel die folgenden Elemente als STL-Dateien exportiert:

* Luft.stl
* Betonseiten.stl
* Gravel-Bottom.stl
* Inlet.stl
* Obstacle.stl
* Ausverkauf

```{figure} ../../img/openfoam/blender/elements-structure.png
:alt: openfoam 
:name: of-elements-structure

Bestandteile des Kanals.
```

Wenn Sie die STL-Dateien aus Blender exportieren, wählen Sie die Option *Ascii* und beinhalten nur das ausgewählte Objekt, wie unten gezeigt.

```{figure} ../../img/openfoam/blender/exportSTL.png
:alt: openfoam 
:name: of-exportSTL

Einstellungen für den Export der STL-Dateien aus Blender.
```

Als nächstes müssen die exportierten STL-Dateien vor der Mesh-Generierung mit einem Texteditor geöffnet und die erste und letzte Zeile wie folgt geändert werden:

* Stellvertreter

```
solid Exported from Blender-2.93.3
...
endsolid Exported from Blender-2.93.3
```

* mit dem Namen der STL-Dateien, mit denen Sie es zu tun haben, zum Beispiel:

```
solid Gravel-bottom
...
endsolid Gravel-bottom
```

Schließlich können alle exportierten und bearbeiteten STL-Dateien im Ordner *triSurface* gespeichert werden, der im nächsten Abschnitt näher beschrieben wird.

