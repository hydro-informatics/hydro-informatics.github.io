---
description: Tutorial für den Betrieb von OpenFOAM Mehrphasen-Flowcase-Setup.
---

# Fallaufstellung

Beim Einrichten des Fallordners müssen die folgenden Dateien bearbeitet werden:

* Im *Constant* Ordner: die verschiedenen Eigenschaften Dateien und die Begrenzungsdatei im *polyMesh* Ordner.
* Im *System* Ordner: die setFieldsDict, fvSchemes, fvSolution und controlDict Dateien.
* Im *0* Ordner: alle enthaltenen Dateien.

# *Constant* Unterverzeichnis

Nach dem Kopieren des *polyMesh*-Ordners aus den *snappyHexMesh*-Ergebnissen ist es notwendig, den Typ der verschiedenen komponierenden Elemente in der **boundary**-Datei korrekt zu definieren. So wurde im folgenden Beispiel das *Gravel-Bottom*-Element als *wall* definiert, während das *Inlet* als *patch* definiert wurde.

```
FoamFile
{
    format      ascii;
    class       polyBoundaryMesh;
    location    "constant/polyMesh";
    object      boundary;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

...
 
    Gravel-bottom
    {
        type            wall;
        inGroups        List<word> 1(wall);
        nFaces          132062;
        startFace       5105689;
    }
    Inlet
    {
        type            patch;
        inGroups        List<word> 1(wall);
        nFaces          288;
        startFace       5237751;
    }
    
 ...
```

Verschiedene Patch-Typen sind in OpenFOAM verfügbar. Für eine ausführliche Erläuterung siehe die [boundaries](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.2-boundaries)s.de des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/).

* * *patch*: generisches Patch
* *symmetriePlane*: Symmetrieebene
* * empty*: aus und hinter Ebenen einer 2D-Geometrie
* Weide*: Keil vorne und hinten für axisymmetrische Geometrie
* *zyklisch*: zyklische Ebene
* * Wand*: verwendet, um Wandfunktionen im turbulenten Fluss zu definieren
* *Prozessor*: Zwischenprozessorgrenze

Die folgenden Dateien müssen zur Definition der Gehäuseeigenschaften zusammen mit einer Liste von Immobiliendateien für den vorliegenden Fall hinzugefügt werden.

```{figure} ../../img/openfoam/interFoam/cases/constant-folder.png
:alt: openfoam 
:name: if-constant-folder

Inhalt des konstanten Ordners.
```

In den *turbulenceProperties* Dateien wird das Turbulenzmodell definiert. OpenFOAM unterstützt folgende Arten von Turbulenzmodellen:

* {term}`Reynolds Averaged (Navier-Stokes) <RANS>` Simulation ((Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen, genannt RAS in OpenFOAM),
* Detached Eddy Simulation (DES) und
* Große Eddy Simulation (LES)

```
simulationType  RAS;

RAS
{
    RASModel        kEpsilon;

    turbulence      on;

    printCoeffs     on;
}
```

Die *transportProperties*-Datei definiert die Eigenschaften der beiden im vorliegenden Fall betrachteten Phasen (Luft und Wasser) und die Oberflächenspannung zwischen den beiden Phasen.

```
phases (water air);

water
{
    transportModel  Newtonian;
    nu              [0 2 -1 0 0 0 0] 1e-06;
    rho             [1 -3 0 0 0 0 0] 1000;
    CrossPowerLawCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 1e-06;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        m               m [ 0 0 1 0 0 0 0 ] 1;
        n               n [ 0 0 0 0 0 0 0 ] 0;
    }

    BirdCarreauCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 0.0142515;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        k               k [ 0 0 1 0 0 0 0 ] 99.6;
        n               n [ 0 0 0 0 0 0 0 ] 0.1003;
    }
}

air
{
    transportModel  Newtonian;
    nu              [0 2 -1 0 0 0 0] 1.48e-05;
    rho             [1 -3 0 0 0 0 0] 1;
    CrossPowerLawCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 1e-06;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        m               m [ 0 0 1 0 0 0 0 ] 1;
        n               n [ 0 0 0 0 0 0 0 ] 0;
    }

    BirdCarreauCoeffs
    {
        nu0             nu0 [ 0 2 -1 0 0 0 0 ] 0.0142515;
        nuInf           nuInf [ 0 2 -1 0 0 0 0 ] 1e-06;
        k               k [ 0 0 1 0 0 0 0 ] 99.6;
        n               n [ 0 0 0 0 0 0 0 ] 0.1003;
    }
}

sigma           [1 0 -2 0 0 0 0] 0.072;
```

Bei der Auswahl des RAS Turbulenzmodells müssen auch die Subdiktionäre *RASproperties* hinzugefügt werden. Diese Datei enthält die Schlüsselwörter, die den Namen des RAS-Turbulenzmodells definieren, die Option, entweder die Turbulenzmodellierung ein- oder ausschalten zu lassen, und einen Schalter, um die Modellkoeffizienten an das Terminal beim Simulationsstart zu drucken.

```
RASModel        kEpsilon;
turbulence      on;
printCoeffs     on;
```

Das *momentumTransport* Wörterbuch wird von jedem Soldat gelesen, der Turbulenzmodellierung beinhaltet. Die in diesem Unterdiktionär definierten Keywords sind die gleichen wie die oben beschriebenen.

```
simulationType  RAS;

RAS
{
    model           kEpsilon;
    turbulence      on;
    printCoeffs     on;
}
```

Turbulence-Modelle können mit der Option *-listMomentumTransportModels* aufgelistet werden:

```
user@user123:~/OpenFOAM-9/channel/$ interFoam -listMomentumTransportModels
```

Schließlich definiert der Subdiktionär *g* einfach die Schwerkraftbeschleunigung und die verwendeten Einheiten.

```
dimensions      [ 0 1 -2 0 0 0 0 ];
value           ( 0 0 -9.8065 );
```

***

# Das *System* Verzeichnis

Der *System Folder* enthält die Parameter, die dem Lösungsverfahren selbst zugeordnet sind. Die obligatorischen Dateien für den Ablauf der Simulation sind die *controlDict*, in der die laufenden Steuerungsparameter eingestellt werden und die für die Datenausgabe; insbesondere die *fvSchemes*, in denen die in der Lösung verwendeten Diskretierungsschemata ausgewählt werden können, und die *fvSolution*, in der die Gleichungslöser, Toleranzen und andere Algorithmussteuerungen eingestellt sind. Zusätzlich wird der *setFieldsDict* hinzugefügt, der es dem Benutzer ermöglicht, Werte auf einem ausgewählten Satz von Zellen/Patch-faces einzustellen.

In der *controlDict*-Datei können mehrere Steuerparameter wie beispielsweise die Start- und Endzeiten und der Zeitschritt dT der Simulation eingestellt werden. Insbesondere bei einer Kaltstartsimulation (d.h. einem Fall, bei dem der Kanal zunächst trocken ist), sollte der Zeitschritt auf *einstellbar* eingestellt werden, wodurch die Einstellung des Zeitschritts gemäß maximaler {term}`CFL`bedingung in der transienten Simulation ermöglicht wird. Zusätzlich sollte der Maximalwert der {term}`CFL`bedingung *maxCo* und der Maximalwert an der Schnittstelle *maxAlphaCo* zugewiesen werden.

```
application     interFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         3600;
deltaT          0.1;
writeControl    adjustableRunTime;
writeInterval   1;
purgeWrite      0;
writeFormat     binary;
writePrecision  6;
writeCompression uncompressed;
timeFormat      general;
timePrecision   6;

runTimeModifiable yes;
adjustTimeStep  yes;

maxCo           1.0;
maxAlphaCo      1.0;
maxDeltaT       1.0;
```

Das *fvSchemes* Wörterbuch im Systemverzeichnis stellt die numerischen Schemata für die in der Anwendung erscheinenden Begriffe fest. Für die Zeitpläne *ddtSchemes* sind neben dem genauen Euler-Schema der ersten Ordnung noch weitere Optionen verfügbar, wie z.B. den Crank-Nicholson- und Rückwärtsplan. Die Gradientenstufen *gradSchemes* werden dann definiert. Die verfügbaren Systeme sind das Gradientenschema von Gauss und das Gradientenschema von Least-Squares. Das Interpolationsschema kann entweder zellbasierte lineare (lineare) oder punktbasierte lineare (pointLinear) oder zumindest quadratische (leastSquares) sein. Das zu verwendende Divergenzschema kann mit dem Stichwort *divSchemes* definiert werden. Detaillierte Informationen zu den verfügbaren Optionen und der entsprechenden Syntax finden Sie im Abschnitt [Divergence-Schema](https://www.openfoam.com/documentation/guides/latest/doc/guide-schemes-divergence.html) des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/). Für die *laplacianSchemes* basieren alle Optionen auf der Anwendung des Gauss-Theorems und erfordern somit ein Interpolationsschema, um die Koeffizienten von Zellwerten auf die Flächen zu transformieren, und ein oberflächennormales Gradientenschema. Die *interpolationSchemes* werden benötigt, um zellzentrierte Größen in Gesichtszentren zu transformieren. Es stehen mehrere Interpolationsschemata zur Verfügung, von denen, die einzigartig auf der Geometrie basieren, bis zum Beispiel {term}`convection <Convection>`-Systeme, die eine Funktion des lokalen Flusses sind.

```
ddtSchemes
{    default         Euler;}

gradSchemes
{    default         Gauss linear;}

divSchemes
{
    div(rhoPhi,U)   Gauss linearUpwind grad(U);
    div(phi,alpha)  Gauss interfaceCompression vanLeer 1;
    div(phi,k)      Gauss upwind;
    div(phi,epsilon) Gauss upwind;
    div(((rho*nuEff)*dev2(T(grad(U))))) Gauss linear;
}

laplacianSchemes
{    default         Gauss linear corrected;}

interpolationSchemes
{    default         linear;}

snGradSchemes
{    default         corrected;}

wallDist
{    method meshWave;}
```

Die *fvSolution*-Dateien enthalten eine Reihe von Unterdiktionen, die für den ausgeführten Solvenz spezifisch sind. Zusätzlich gibt es eine Reihe von Standard-Unterdiktionen, darunter die *solver*, *relaxationFactors*, *PISO* und *SIMPLE*, die die meisten der von den Standard-Lösern verwendeten umfassen. Ein Beispiel für die für den InterFoam-Löser benötigten Einträge finden Sie in dem [Fallordner](https://github.com/hydro-informatics/openfoam.git)(*Simulation*-Ordner). Einen ausführlichen Überblick über alle verfügbaren Optionen finden Sie im [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/) ([Lösung und Algorithm Control](https://www.openfoam.com/documentation/user-guide/6-solving/6.3-solution-and-algorithm-control)).

Mit dem *setFieldsDict* kann der Benutzer einen bestimmten Wert einem ausgewählten Satz von Zellen/Patch-faces zuordnen. Für das vorliegende Tutorial wurde dieses Wörterbuch verwendet, um dem Einlass des Modells einen anfänglichen Wasserstand zuzuordnen. Für die Auswahl der interessierenden Zellen stehen mehrere Optionen zur Verfügung. Im unten dargestellten Beispiel wurde die *boxToCell* Option gewählt, die alle Zellen auswählt, deren Zellenzentrum sich innerhalb der angegebenen Begrenzungsbox befindet.

```
defaultFieldValues
(
    volScalarFieldValue alpha.water 0
);

regions    // Select based on surface
(
    boxToCell
    {
        box (-3.6 5.1 -2.5) (0.4 -4.0 1.2);
        fieldValues
        (
            volScalarFieldValue alpha.water 1
        );
    }
);
```

Alternativ können andere Quellen verwendet werden, wie z.B. *fieldToCell*, die alle Zellen auswählt, die sich durch einen Feldwert im ausgewählten Bereich auszeichnen [min; max]. Eine sehr nützliche Option bei der Einstellung des Anfangswasserspiegels ist auch die *oberflächeToCell* Quelle, die die Zellen mit einer Oberfläche auswählt, basierend auf einer importierten {term}`STL`Oberfläche. In diesem Fall würde das Wörterbuch aussehen:

```
defaultFieldValues
(
    volScalarFieldValue alpha.water 0
);

regions    // Select based on surface
(
  surfaceToCell
      {
          file            "./constant/triSurface/water.stl";
          outsidePoints   ((x y z));
          includeCut      true;
          includeInside   true;
          includeOutside  false;
          nearDistance    -1;
          curvature       -100;
          fieldValues
          (
              volScalarFieldValue alpha.water 1
          );
      }
 );
```

Das *outsidePoints* Keyword definiert die Außenseite der Oberfläche. *IncludeCut*, *includeInside* und *IncludeOutside* sind Booleane, die bestimmen, ob bei der Auswahl die von der Oberfläche geschnittenen Zellen, die Zellen innerhalb der Oberfläche bzw. außerhalb der Oberfläche enthalten sollen. Das *nearDistance* Keyword ist ein Skalar, der bestimmt, welche Zellen mit dem Zentrum in der Nähe der Oberfläche enthalten. Schließlich enthält *Kurvature* die Zellen nahe einer starken Krümmung auf der Oberfläche.

Eine vollständige Liste aller verfügbaren Quellen finden Sie im Abschnitt *TopoSet* in der [OpenFOAM Wiki](https://openfoamwiki.net/index.php/TopoSet).

# *0* Verzeichnis
Das *0*-Verzeichnis ist das Zeitverzeichnis mit den Dateien, die die Anfangsbedingungen der Simulation beschreiben. Innerhalb dieses Verzeichnisses ist für den ausführbaren InterFoam-Löser eine Textdatei für jedes Feld erforderlich. Im vorliegenden Fall umfassen diese Dateien: $U$ für die Strömungsgeschwindigkeit, *p-rgh* für den dynamischen Druck, *nut* für die turbulente Viskosität, $k$ für die {term}`turbulent kinetic energy <Turbulent kinetic energy>`, $\epsilon$ für die Dissipation turbulenter kinetischer Energie und *alpha.water.orig* für die Anfangsphasen. Der vollständige Satz der Dateien, die für dieses Tutorial verwendet werden, finden Sie im [Fall-Ordner](https://github.com/hydro-informatics/openfoam.git).


# Variable Wahlen

## U-Feld Wörterbuch

Dieses Wörterbuch definiert die Randbedingungen und die anfängliche Einrichtung für das $U$ Vektorfeld. Für die *internalField* wurden einheitliche Ausgangsbedingungen mit einem Wert von (0 0 0) eingestellt. Für alle übrigen Wände und Patches wurden folgendes zugeordnet:

* **Luft-Patch** : *DruckInletOutletVelocity* Zustand, der dem Ausströmen der Domäne eine Null-Gradienten-Bedingung und eine auf dem Fluss in der Patch-Normalrichtung basierende Geschwindigkeit in die Domäne zuordnet.
* **Krektseiten, Gravel-Botten- und Obstacle-Patches*: *noSlip* Zustand. Die Patchgeschwindigkeit wird auf (0 0 0) eingestellt
* **Inlet patch**: ein *flowRateInletVelocity*-Zustand wurde gewählt. Dies ermöglicht es, den Volumen- oder Massendurchsatz am Einlass-Patch zu definieren.
* * * * * * * Outlet patch*: ein *zeroGradient* Randzustand wurde eingestellt. Die internen Werte werden daher auf die Grenzfläche extrapoliert.

```
dimensions      [0 1 -1 0 0 0 0]; //kg m s K mol A cd
internalField   uniform (0 0 0);

boundaryField
{
     Air
        {
        	type            pressureInletOutletVelocity;
         	value           uniform (0 0 0);
        }

     Concrete-sides
        {
        	type            noSlip;
        }

     Gravel-bottom
        {
        	type            noSlip;
        }

     Inlet
        {
        	type            flowRateInletVelocity;
        	volumetricFlowRate constant 0.5;
	}

     Obstacle
        {
        	type            noSlip;
        }

     Outlet
        {
                type            zeroGradient;
        }
}
```

## p-rgh Feldwörterbuch

Dieses Wörterbuch definiert die Randbedingungen und die Anfangseinstellung für das in Pa exprimierte Dimensionsfeld p-rgh. Das *internalField* wurde mit einem 0-Wert in der gesamten Domäne initialisiert. Die übrigen Felder wurden wie folgt festgelegt:

* **Air-Patch*: Die *totalPressure* wurde zugewiesen. Diese Bedingung stellt den statischen Druck auf dem Patch basierend auf der Spezifikation des Gesamtdrucks fest und ermöglicht eine ausreichende Darstellung des Atmosphärendrucks.
* **Alle anderen Patches**: Die verwendete Bedingung war eine *fixedFluxPressure* Grenze. Diese Randbedingung wird alternativ zu *zeroGradient* genutzt, in den Fällen, in denen auch die Schwerkraft und Oberflächenspannung in den Lösungsgleichungen vorhanden sind.

```
dimensions      [1 -1 -2 0 0 0 0];//kg m s K mol A cd
internalField   uniform 0;//initially atmospheric pressure in the entire domain

boundaryField
{
     Air
        {
        	type            totalPressure;
        	p0              uniform 0;
        }

     Concrete-sides
        {
        	type            fixedFluxPressure;
        	value           uniform 0; 
        }

     Gravel-bottom
        {
        	type            fixedFluxPressure;
        	value           uniform 0;
        }

     Inlet
        {
        	type            fixedFluxPressure;
        	value           uniform 0;
	}

     Obstacle
        {
        	type            fixedFluxPressure;
        	value           uniform 0;
        }

     Outlet
        {
                type            fixedFluxPressure;
        	value           uniform 0;
        }
}
```

## Muttersprache Wörterbuch

Dieses Wörterbuch definiert die Randbedingungen und die anfängliche Einrichtung der turbulenten Viskositätsnuß, ausgedrückt in m$^2$/s. Das *internalField* wurde mit einem 0-Wert in der gesamten Domain initialisiert. Die übrigen Felder wurden wie folgt festgelegt:

**Air, Inlet and Outlet Patch*: Die Bedingung wurde auf *berechnet* gesetzt, was bedeutet, dass kein Wert vorgeschrieben ist und dass es aus dem hier verwendeten {term}`RANS` turbulence Modell und den Werten für $k$ ({term}`turbulent kinetic energy <Turbulent kinetic energy>`) und $\epsilon$ in diesem Fall berechnet wird.
** Alle übrigen Wände**: die *nutkRoughWallFunction* Randbedingung wurde angewendet.

Diese Randbedingung sorgt für eine Wandkonstrate auf der turbulenten Viskosität. Dies ermöglicht es, die Auswirkungen der Rauhigkeit zu berücksichtigen. Die Realisierung der verschiedenen im Modell vorhandenen Materialien erfolgte durch die Festlegung der unterschiedlichen Rauhigkeitshöhen ks (z.B. 0,0052 für die Betonwände).

```
dimensions      [0 2 -1 0 0 0 0];
internalField   uniform 0;

boundaryField
{

    Air
    {
      type            calculated;
      value           uniform 0;
    }

    Concrete-sides
    {
      type            nutkRoughWallFunction;
      Ks              uniform 0.0052;
      Cs              uniform 0.5;
      value           uniform 0;
    }

    Gravel-bottom
    {
      type            nutkRoughWallFunction;
      Ks              uniform 0.15;
      Cs              uniform 0.5;
      value           uniform 0;
    }

    Inlet
    {
      type            calculated;
      value           uniform 0;
    }

    Obstacle
    {
      type            nutkRoughWallFunction;
      Ks              uniform 0.0052;
      Cs              uniform 0.5;
      value           uniform 0;
    }

    Outlet
    {
        type            calculated;
        value           uniform 0;
    }
}
```

## k feld Wörterbuch

This dictionary defines the boundary conditions and initial setup for the {term}`turbulent kinetic energy <Turbulent kinetic energy>` $k$, expressed in m$^2$/s. The *internalField* was initialized with a uniform value in the entire domain. The remaining fields were set as follows:

```{aside} Meaning of letters
*q* für die quadratische Basis der turbulenten kinetischen Energie und *R* für den Reynolds Stress Tensor (mehr im Glossareintrag auf {term}`turbulent kinetic energy <Turbulent kinetic energy>`.
```

* **Luft- und Auslass-Patch*: *inletOutlet*, die einem *zeroGradient*-Zustand entspricht, mit Ausnahme des Falles, in dem der Geschwindigkeitsvektor neben der Grenze innerhalb der Domäne gerichtet ist. Im letzteren Fall schaltet es auf einen *fixedValue* Zustand.
* **Inlet patch**: *fixedValue*. Der entsprechende Wert war der dem *internalField* zugeordnet.
**Alle übrigen Wände*: *kqRWallFunction*. Diese Randbedingung sorgt für eine einfache Umhüllung um den Nullgradienten Zustand.


```
dimensions      [0 2 -2 0 0 0 0];
internalField   uniform 1.22e-03;

boundaryField
{
    Air
  {
      type            inletOutlet;
      inletValue      $internalField;
      value           $internalField;
  }

  Concrete-sides
  {
    type            kqRWallFunction;
    value           $internalField;
  }

  Gravel-bottom
  {
    type            kqRWallFunction;
    value           $internalField;
  }

  Inlet
  {
    type            fixedValue;
    intensity       0.05;
    value           $internalField;
  }

  Obstacle
  {
    type            kqRWallFunction;
    value           $internalField;
  }

  Outlet
  {
      type            inletOutlet;
      inletValue      $internalField;
      value           $internalField;
  }
}
```

## epsilon feld Wörterbuch

This dictionary defines the boundary conditions and initial set up for the rate of dissipation $\epsilon$ of {term}`turbulent kinetic energy <Turbulent kinetic energy>`, expressed in m$^2~$s$^{-3}$. The *internalField* was initialized with a uniform value in the entire domain. The remaining fields were set as shown below:

* **Air and Outlet Patch*: *inletOutlet*, wie oben beschrieben für $k$.
* **Inlet patch**: *fixedValue*, entsprechend dem internenField-Wert.
**Alle übrigen Wände**: *epsilonWallFunction*. Diese Randbedingung bietet eine Wandbeschränkung auf die turbulente kinetische Energiedissipation Rate $\epsilon$ und die turbulente kinetische Energie $k$Produktionsbeitrag für niedrige und hohe Reynolds Anzahl Turbulenzmodelle.

```
dimensions      [0 2 -3 0 0 0 0];
internalField   uniform 3.20e-05;

boundaryField
{
    Air
    {
        type            inletOutlet;
        inletValue      $internalField;
        value           $internalField;
    }

    Concrete-sides
    {
      type            epsilonWallFunction;
      value           $internalField;
    }

    Gravel-bottom
    {
      type            epsilonWallFunction;
      value           $internalField;
    }

    Inlet
    {
      type            fixedValue;
      value           $internalField;
    }

    Obstacle
    {
      type            epsilonWallFunction;
      value           $internalField;
    }

    Outlet
    {
        type            inletOutlet;
        inletValue      $internalField;
        value           $internalField;
    }
}
```

## alpha.water field Wörterbuch

Dieses Wörterbuch definiert die Randbedingungen und Ausgangsbedingungen für das nicht-dimensionale Feld alpha.water. Das *internalField* wurde mit einem einheitlichen Wert gleich 0 in der gesamten Domäne initialisiert, d.h. kein Wasser ist in der Domäne zum Zeitpunkt 0 vorhanden. Das Wasser wird dann mit den im entsprechenden Wörterbuch definierten Einstellungen mit dem Befehl *setFields* initialisiert. Die übrigen Felder wurden wie folgt festgelegt:

* **Air-Patch*: *inletOutlet*, die die Möglichkeit des Zurückfließens von Wasser in die Domäne vermeidet. In dem Fall, in dem die Strömung austritt, wird ein *zeroGradient*-Zustand angelegt, und in ähnlicher Weise, wenn die Strömung einen Wert zurückgibt, der dem als *inletValue* definierten Wert entspricht.
* **Inlet patch**: *fixedValue*, entsprechend einem einheitlichen Wert von 1, d.h. der gesamte Patch besteht nur aus Wasser (keine Luftphase vorhanden).
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * Dabei werden die internen Werte auf die Grenzfläche extrapoliert.

```
dimensions      [0 0 0 0 0 0 0];

internalField   uniform 0;

boundaryField
{
  Air
  {
    type            inletOutlet;
    inletValue      uniform 0;
    value           uniform 0;
  }

  Concrete-sides
  {
    type            zeroGradient;
  }

  Gravel-bottom
  {
    type            zeroGradient;
  }

  Inlet
    {
        type            fixedValue;
        value           uniform 1;
    }

  Obstacle
  {
    type            zeroGradient;
  }

    Outlet
  {
    type            zeroGradient;
  }
}
```

