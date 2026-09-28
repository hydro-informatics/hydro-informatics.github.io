---
description: Tutorial zum Ausführen von OpenFOAM Multiphase Flow Case Setup.
---

# Fallaufbau

Beim Einrichten des Fallordners müssen die folgenden Dateien bearbeitet werden:

* Im Ordner *Constant*: die verschiedenen Eigenschaftsdateien und die Begrenzungsdatei im Ordner *polyMesh*.
* Im Ordner *System*: die Dateien setFieldsDict, fvSchemes, fvSolution und controlDict.
* Im Ordner *0*: alle enthaltenden Dateien.

# Das *Constant* Unterverzeichnis

Nachdem Sie den Ordner *polyMesh* aus den *snappyHexMesh*-Ergebnissen kopiert haben, müssen Sie den Typ der verschiedenen Kompositionselemente in der **boundary**-Datei korrekt definieren. Im Beispiel unten wurde das Element *Gravel-bottom* als *wall* definiert, während der *Inlet* als *patch* definiert wurde.

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

Verschiedene Patch-Typen sind in OpenFOAM verfügbar. Für eine ausführliche Erklärung siehe [boundaries](https://www.openfoam.com/documentation/user-guide/4-mesh-generation-and-conversion/4.2-boundaries)] Abschnitt des [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/)].

* *Patch*: Generisches Patch
* *symmetryPlane*: Symmetrieebene
* *leer*: von und zurück Ebenen einer 2D-Geometrie
* *Keil*: Keil vorne und hinten für eine axisymmetrische Geometrie
* *zyklisch*: zyklische Ebene
* *wall*: wird verwendet, um Wandfunktionen in turbulenter Strömung zu definieren
* *Prozessor*: Grenze zwischen Prozessor

Die folgenden Dateien müssen hinzugefügt werden, um die Falleigenschaften zusammen mit einer Liste von Eigenschaftsdateien für den vorliegenden Fall zu definieren.

```{figure} ../../img/openfoam/interFoam/cases/constant-folder.png
:alt: openfoam 
:name: if-constant-folder

Inhalt des konstanten Ordners.
```

In den *turbulenceProperties* Dateien ist das Turbulenzmodell definiert. OpenFOAM unterstützt die folgenden Arten von Turbulenzmodellen:

* {term}`Reynolds Averaged (Navier-Stokes) <RANS>` Simulation ((Osborne) Reynolds-gemittelte Navier-Stokes-Gleichungen, in OpenFOAM als RAS bezeichnet),
* Detached Eddy Simulation (DES) und
* Large Eddy Simulation (LES)

```
simulationType  RAS;

RAS
{
    RASModel        kEpsilon;

    turbulence      on;

    printCoeffs     on;
}
```

Die Datei *transportProperties* definiert die Eigenschaften der beiden hier betrachteten Phasen (Luft und Wasser) und die Oberflächenspannung zwischen den beiden Phasen.

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

Bei der Auswahl des RAS-Turbulenzmodells muss auch das *RASproperties*-Unterwörterbuch hinzugefügt werden. Diese Datei enthält die Schlüsselwörter, die den Namen des RAS-Turbulenzmodells, die Option zum Ein- oder Ausschalten der Turbulenzmodellierung und einen Schalter zum Drucken der Modellkoeffizienten auf das Terminal beim Start der Simulation definieren.

```
RASModel        kEpsilon;
turbulence      on;
printCoeffs     on;
```

Das *momentumTransport*-Wörterbuch wird von jedem Solver gelesen, der eine Turbulenzmodellierung enthält. Die in diesem Unterwörterbuch definierten Schlüsselwörter sind die gleichen wie die oben beschriebenen.

```
simulationType  RAS;

RAS
{
    model           kEpsilon;
    turbulence      on;
    printCoeffs     on;
}
```

Turbulenzmodelle können aufgelistet werden, indem ein Solver mit der Option *-listMomentumTransportModels * ausgeführt wird:

```
user@user123:~/OpenFOAM-9/channel/$ interFoam -listMomentumTransportModels
```

Schließlich definiert das *g*-Unterwörterbuch einfach die Gravitationsbeschleunigung und die verwendeten Einheiten.

```
dimensions      [ 0 1 -2 0 0 0 0 ];
value           ( 0 0 -9.8065 );
```

******

# Das *System* Verzeichnis

Der *Systemordner* enthält die Parameter, die mit der Lösungsprozedur selbst verbunden sind. Die obligatorischen Dateien für die Ausführung der Simulation sind die * controlDict *, in denen die Betriebssteuerparameter und die für die Datenausgabe festgelegt sind; insbesondere die * fvSchemes *, in denen die in der Lösung verwendeten Diskretisierungsschemata ausgewählt werden können, und die * fvSolution *, in der die Gleichungslöser, Toleranzen und andere Algorithmussteuerungen festgelegt sind. Zusätzlich wird der *setFieldsDict* hinzugefügt, der es dem Benutzer ermöglicht, Werte für einen ausgewählten Satz von Zellen / Patch-Gesichtern festzulegen.

In the *controlDict* file, several control parameters can be set as, for instance, the start & end times, and time step dT of the simulation. In particular, when running a cold start simulation (i.e., a case in which the channel is initially dry), the time step should be set to *adjustable* enabling the adjustment of the time step according to maximum {term}`CFL-Zahl <CFL>` condition in the transient simulation. Additionally, the maximum value of the {term}`CFL-Zahl <CFL>` condition *maxCo* and the maximum value at the interface *maxAlphaCo* should be assigned.

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

The *fvSchemes* dictionary in the system directory sets the numerical schemes for the terms that appear in the application that is being run. For the time schemes *ddtSchemes*, apart from the first-order accurate Euler scheme, other options are available, such as the second-order Crank-Nicholson and backward schemes. The gradient schemes *gradSchemes* are then defined. The available schemes are the Gauss gradient scheme and the Least-squares gradient scheme. The interpolation scheme can be either cell-based linear (linear) or point-based linear (pointLinear) or least squares (leastSquares). The divergence scheme to be used can be defined with the *divSchemes* keyword. Detailed information regarding the available options and corresponding syntax can be found in the [divergence schemes](https://www.openfoam.com/documentation/guides/latest/doc/guide-schemes-divergence.html) section of the [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/). For the *laplacianSchemes*, all options are based on the application of the Gauss theorem, requiring thus an interpolation scheme to transform the coefficients from cell values to the faces, and a surface-normal gradient scheme. The *interpolationSchemes* are required to transform cell-center quantities to face centers. Several interpolation schemes are available, from the ones based uniquely on the geometry to, for example, {term}`Konvektion <Convection>` schemes that are a function of the local flow.

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

Die *fvSolution*-Dateien enthalten eine Reihe von Unterwörterbüchern, die spezifisch für den ausgeführten Solver sind. Darüber hinaus gibt es eine Reihe von Standard-Unterwörterbüchern, einschließlich der * Solver*, *RelaxationFactors*, *PISO* und *SIMPLE*, die die meisten der von den Standard-Solvern verwendeten abdecken. Ein Beispiel für die Menge von Einträgen, die für den interFoam-Solver erforderlich sind, finden Sie in diesem eBook [Fallordner](https://github.com/hydro-informatics/openfoam.git) (*Simulation* Ordner). Eine detaillierte Übersicht über alle verfügbaren Optionen finden Sie im [OpenFOAM User Guide](https://doc.cfd.direct/openfoam/user-guide/)] ([Lösung und Algorithm Control](https://www.openfoam.com/documentation/user-guide/6-solving/6.3-solution-and-algorithm-control)).

Mit *setFieldsDict* kann der Benutzer einem ausgewählten Satz von Zellen/Patchfaces einen bestimmten Wert zuweisen. Für das vorliegende Tutorial wurde dieses Wörterbuch verwendet, um dem Einlass des Modells einen anfänglichen Wasserstand zuzuweisen. Mehrere Optionen stehen zur Auswahl der Zellen von Interesse zur Verfügung. In dem unten gezeigten Beispiel wurde die Option *boxToCell* ausgewählt, die alle Zellen auswählt, deren Zellenzentrum sich innerhalb der angegebenen Begrenzungsbox befindet.

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

Alternatively, other sources can be used, such as *fieldToCell*, which selects all cells characterized by a field value within the selected range [min; max]. A very useful option when setting the initial water level is also the *surfaceToCell* source that selects the cells using a surface, based on an imported {term}`STL` surface. In this case the dictionary would look like:

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

Das Schlüsselwort *outsidePoints* definiert die Außenseite der Oberfläche. *IncludeCut*, *includeInside* und *IncludeOutside* sind Booleen, die bestimmen, ob sie die von der Oberfläche geschnittenen Zellen, die Zellen innerhalb der Oberfläche bzw. außerhalb der Oberfläche in die Auswahl einbeziehen sollen. Das Schlüsselwort *nearDistance* ist ein Skalar, der bestimmt, welche Zellen mit dem Zentrum in der Nähe der Oberfläche enthalten sind. Schließlich *Krümmung * umfasst die Zellen in der Nähe einer starken Krümmung auf der Oberfläche.

Eine vollständige Liste aller verfügbaren Quellen finden Sie unter [OpenFOAM Wiki](https://openfoamwiki.net/index.php/TopoSet) im Abschnitt *TopoSet*].

# Das *0* Verzeichnis
The *0* directory is the time directory containing the files describing the initial conditions of the simulation. Inside this directory, one text file for each field is required for the interFoam solver executable. In the present case, these files include: $U$ for the flow velocity, *p-rgh* for the dynamic pressure, *nut* for the turbulent viscosity, $k$ for the {term}`turbulent kinetic energy <Turbulent kinetic energy>`, $\epsilon$ for the rate of dissipation of turbulent kinetic energy, and  *alpha.water.orig* for the initial phases. The complete set of the files used for this tutorial can be found in the [case folder](https://github.com/hydro-informatics/openfoam.git).


# Variable Wörterbücher

## U-Feld Wörterbuch

This dictionary defines the boundary conditions and initial set up for the $U$ vector field. For the *internalField* uniform initial conditions with a value of (0 0 0) were set. For all remaining walls and patches, the following were assigned:

* **Air Patch** : *pressureInletOutletVelocity* Bedingung, die dem Fluss aus der Domäne eine Nullgradientenbedingung und eine Geschwindigkeit basierend auf dem Fluss in der Patch-Normalrichtung dem Fluss in die Domäne zuweist.
* **Beton-Seiten, Gravel-bottom und Hindernis Patches **: *noSlip * Bedingung. Die Patch-Geschwindigkeit wird auf (0 0 0) eingestellt
* **Inlet Patch**: eine *flowRateInletVelocity*-Bedingung wurde gewählt. Dies ermöglicht es, den Volumen- oder Massenstrom am Einlasspflaster zu definieren.
* **Outlet-Patch**: eine *zeroGradient*-Grenzbedingung wurde gesetzt. Die internen Werte werden daher auf die Grenzfläche extrapoliert.

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

## p-rgh-Feldwörterbuch

Dieses Wörterbuch definiert die Randbedingungen und den initialen Aufbau für das Dimensionsfeld p-rgh, ausgedrückt in Pa. Der *internalField* wurde mit einem 0-Wert in der gesamten Domäne initialisiert. Die übrigen Felder wurden wie folgt gesetzt:

* **Air Patch**: der *totalPressure* wurde zugewiesen. Diese Bedingung stellt den statischen Druck am Patch basierend auf der Spezifikation des Gesamtdrucks ein und ermöglicht es, den atmosphärischen Druck angemessen darzustellen.
* **Alle anderen Patches**: Die verwendete Bedingung war eine *fixedFluxPressure* Grenze. Diese Randbedingung wird als Alternative zu *nullGradient* genutzt, in den Fällen, in denen auch die Schwerkraft und Oberflächenspannung in den Lösungsgleichungen vorhanden sind.

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

## Mutterfeld Wörterbuch

Dieses Wörterbuch definiert die Randbedingungen und die anfängliche Einrichtung für die turbulente Viskositätsmutter, ausgedrückt in m$^2$/s. Der *internalField* wurde mit einem 0-Wert in der gesamten Domain initialisiert. Die übrigen Felder wurden wie folgt gesetzt:

* **Air, Inlet und Outlet Patch**: Die Bedingung wurde auf *berechnet* gesetzt, was bedeutet, dass kein Wert vorgeschrieben ist und dass er aus dem hier verwendeten {term}`RANS` Turbulenzmodell und den Werten für $k$ ({term}`turbulent kinetic energy <Turbulent kinetic energy>`) und $\epsilon$ in diesem Fall berechnet wird.
* **Alle übrigen Wände**: Die *nutkRoughWallFunction* Randbedingung wurde angewendet.

Diese Randbedingung sorgt für eine Wandbeschränkung der turbulenten Viskosität. Dies ermöglicht es, die Auswirkungen der Rauheit zu berücksichtigen. Die Implementierung der verschiedenen im Modell vorhandenen Materialien erfolgte durch Definition der unterschiedlichen Rauhigkeitshöhen ks (z. B. 0,0052 für die Betonwände).

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

## k Feld Wörterbuch

This dictionary defines the boundary conditions and initial setup for the {term}`turbulent kinetic energy <Turbulent kinetic energy>` $k$, expressed in m$^2$/s. The *internalField* was initialized with a uniform value in the entire domain. The remaining fields were set as follows:

```{aside} Meaning of letters
*q* für die Quadratwurzel der turbulenten kinetischen Energie und *R* für den Reynolds-Stresstensor (lesen Sie mehr im Glossareintrag unter {term}`turbulent kinetic energy <Turbulent kinetic energy>`).
```

* **Air- und Outlet-Patch**: *inletOutlet*, was einer Bedingung *zeroGradient* entspricht, mit Ausnahme des Falles, in dem der Geschwindigkeitsvektor neben der Grenze innerhalb der Domäne gerichtet ist. Im letzteren Fall wechselt es zu einer Bedingung *fixedValue *.
* **Inlet Patch**: *fixedValue*. Der entsprechende Wert war der dem *internalField* zugeordnete Wert.
* **Alle übrigen Wände**: *kqRWallFunction*. Diese Randbedingung bietet eine einfache Umhüllung um den Nullgradientenzustand.


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

## epsilon-Feld Wörterbuch

This dictionary defines the boundary conditions and initial set up for the rate of dissipation $\epsilon$ of {term}`turbulent kinetic energy <Turbulent kinetic energy>`, expressed in m$^2~$s$^{-3}$. The *internalField* was initialized with a uniform value in the entire domain. The remaining fields were set as shown below:

* **Air und Outlet Patch**: *inletOutlet*, wie oben für $k$ beschrieben.
* **Inlet-Patch**: *fixedValue*, entsprechend dem internen Feldwert.
* **All remaining walls**: *epsilonWallFunction*. This boundary condition provides a wall constraint on the turbulent kinetic energy dissipation rate $\epsilon$ and the turbulent kinetic energy $k$ production contribution for low and high Reynolds number turbulence models.

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

## alpha.Wasserfeld Wörterbuch

Dieses Wörterbuch definiert die Randbedingungen und Anfangsbedingungen für das nichtdimensionale Feld alpha.water. Der *internalField* wurde mit einem einheitlichen Wert gleich 0 in der gesamten Domäne initialisiert, was bedeutet, dass zum Zeitpunkt 0 kein Wasser in der Domäne vorhanden ist. Das Wasser wird dann mit dem Befehl *setFields* mit den im entsprechenden Wörterbuch definierten Einstellungen initialisiert. Die übrigen Felder wurden wie folgt gesetzt:

* **Air Patch**: *inletOutlet*, das die Möglichkeit vermeidet, dass Wasser in die Domäne zurückfließt. In dem Fall, in dem der Fluss austritt, wird eine Bedingung * zeroGradient * angewendet, und in ähnlicher Weise, wenn der Fluss einen Wert zurückgibt, der dem Wert entspricht, der als * inletValue * definiert ist.
* **Inlet Patch**: *fixedValue*, entsprechend einem einheitlichen Wert von 1, d.h. der gesamte Patch besteht nur aus Wasser (keine Luftphase vorhanden).
* **Outlet Patch und alle übrigen Wände**: *zeroGradient*. Dabei werden die internen Werte auf die Grenzfläche extrapoliert.

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

