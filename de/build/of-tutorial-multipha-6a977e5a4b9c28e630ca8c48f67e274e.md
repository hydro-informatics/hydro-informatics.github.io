---
description: Tutorial zum Ausführen von OpenFOAMs interFoam für Wassersimulationen.
---

# Multiphase Solver (interFoam Tutorial)

In diesem Tutorial lösen wir das Problem eines 50 m langen geraden Kanals mit zwei Becken, einem kleineren am Einlass und einem größeren am Auslass und einem Hindernis in der Mitte.

```{figure} ../../img/openfoam/blender/study-area.jpg
:alt: openfoam 
:name: of-study-area

3D-Ansicht der analysierten Struktur.
```

In this case, we will use the multiphase solver interFoam coupled with a {term}`k <Turbulent kinetic energy>` - $\epsilon$ (epsilon) turbulence model. interFoam identifies the water-air interface based on the Volume of Fluid (VOF) method, which solves the transport equations for a single or multiple phase fractions alpha, where alpha is 0.5 at the interface between the fluids (see [OpenFOAM Standard Solvers](https://www.openfoam.com/documentation/user-guide/a-reference/a.1-standard-solvers)). Additionally, we will focus on the implementation of multiple roughness zones related to the engineered and nature-oriented elements present in the model, and we will apply a specific roughness height. 

```{figure} ../../img/openfoam/blender/channel-view2-final.jpg
:alt: openfoam 
:name: of-channel-view2-final

3D-Ansicht der analysierten Struktur in Strömungsrichtung unter Hervorhebung der zugeordneten Materialien.
```

Der Fallordner mit allen notwendigen Dateien kann heruntergeladen werden [hier](https://github.com/hydro-informatics/openfoam.git)].

******
## Dateiimport
Der erste Abschnitt dieses Tutorials befasst sich mit dem Import der ursprünglich erstellten Geometrie. Alle Dateien wurden mit Blender erstellt, einem kostenlosen und Open-Source-Tool für 3D-Computergrafiksoftware. Die Geometrie wurde anhand ihres Zusammensetzungsmaterials und nach den im Verzahnungsprozess zu verfeinernden Bereichen in einzelne Elemente unterteilt. Daher wurden für das vorliegende Beispiel die folgenden Elemente als STL-Dateien exportiert:

* Air.stl
* Concrete-sides.stl
* Gravel-bottom.stl
* Inlet.stl
* Obstacle.stl
* Outlet.stl

```{figure} ../../img/openfoam/blender/elements-structure.png
:alt: openfoam 
:name: of-elements-structure

Bestandteile des Kanals.
```

Wenn Sie die STL-Dateien aus Blender exportieren, wählen Sie die Option *Ascii* und schließen Sie nur das ausgewählte Objekt ein, wie unten gezeigt.

```{figure} ../../img/openfoam/blender/exportSTL.png
:alt: openfoam 
:name: of-exportSTL

Einstellungen für den Export der STL-Dateien aus Blender.
```

Bevor Sie mit der Mesh-Generierung fortfahren, müssen die exportierten STL-Dateien mit einem Texteditor geöffnet und die erste und letzte Zeile wie folgt geändert werden:

* Ersatz

```
solid Exported from Blender-2.93.3
...
endsolid Exported from Blender-2.93.3
```

* mit dem Namen der STL-Dateien, mit denen Sie sich befassen, zum Beispiel:

```
solid Gravel-bottom
...
endsolid Gravel-bottom
```

Schließlich können alle exportierten und bearbeiteten STL-Dateien im Ordner *triSurface* gespeichert werden, der im nächsten Abschnitt ausführlicher beschrieben wird.

