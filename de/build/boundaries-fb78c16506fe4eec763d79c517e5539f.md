---
description: Leitfaden zur Einrichtung flüssiger Randbedingungen in TELEMAC, die überbestimmte Grenzen, Phasen-Entladungsverhältnisse, Rauheitskoeffizienten und Spitzen für Flussmodellierung abdecken.
---

(tm-foc-bc)=
# Rahmenbedingungen

```{admonition} Requirements

Dieses Tutorial erfordert keinen laufenden Code, aber wir empfehlen zumindest die Einrichtung eines Telemac-Modells, wie es in der {ref}`steady 2d tutorial <telemac2d-steady>` beschrieben ist, was das Verständnis von Konzepten und Begriffen erleichtert.
```

Die flüssigen Randbedingungen werden überbestimmt, wenn zu viele Parameter vorgegeben sind, die zumindest numerisch konkurrieren. Wenn beispielsweise Entladung und Wassertiefe vorgeschrieben sind, aber mit den definierten Rauheitskoeffizienten nicht erreicht werden kann, versucht Telemac, die Wassertiefe einzuhalten. Diese Wassertiefe entspricht jedoch oft nicht der vorgeschriebenen Entladung und Telemac versucht, die Differenz durch Variation der Längen (Angaben) der Geschwindigkeitsvektoren zu kompensieren. Die Geschwindigkeitsvektoren werden wiederum durch die Rauheitskoeffizienten eingeschränkt. So versucht Telemac, Wassertiefen und Geschwindigkeitsvektoren zu variieren, um eine an der Grenze vorgeschriebene {term}`stage (H)-discharge (Q) relation <Stage-discharge relation>` zu erreichen, was mit der definierten Rauhigkeit unmöglich sein könnte. Ein Workaround wäre die Einstellung von Rauhigkeitskoeffizienten, so dass die definierten Randbedingungen und Rauhigkeitskoeffizienten genau im Gleichgewicht sind. Die Randbedingungen sollten jedoch speziell für mehrere Geländetypen (d.h. {ref}`roughness zones <tm-friction-zones>`) durch Modellkalibrierung mit Messwerten kalibriert und nicht durch Probleme an den Modellgrenzen zur Massenbilanz auferlegt werden. Also, was als nächstes?

Um das Problem der überbestimmten Randbedingungen und Massenungleichgewicht zu bewältigen, geben die nächsten Abschnitte zunächst Tipps, um die Flüssigkeitsgrenzen geometrisch korrekt zu platzieren, dann erinnern Sie sich an die Einrichtung einer Grenzdatei, die Arten von Grenzen (d.h. Werte) und wie sie die Massenbilanz beeinflussen könnten.

```{admonition} Tips for modeling rivers
:class: important

Die in diesem Kapitel dargestellten Workflows und Tipps beziehen sich in erster Linie auf die numerische Modellierung von Flüssen mit Telemac. Ähnliche Bedingungen könnten für Seeschwemmungen gelten, aber andere Umgebungen, wie Küstenregionen, erfordern unterschiedliche Überlegungen zur Festlegung von Randbedingungen.
```

(tm-foc-draw-bc)=
## Zeichnen von flüssigen Brennstoffen

Beim Zeichnen von Flüssigkeitsgrenzen, beispielsweise in BlueKenue, helfen einige geometrische Eigenschaften, die Stabilität und Massenbilanz der späteren Simulation zu verbessern:

* Flüssigkeitsgrenzen sollten mindestens 5-10 Knoten aufweisen.
* Alle Flüssigkeitszuflussgrenzen sollten eine nahezu gleiche Anzahl von Knoten als Summe von Flüssigkeitsabflussgrenzen aufweisen.
* Flüssige Zuflussgrenzen (nach oben) sollten nur am unteren Flussbett definiert werden, niemals an den Flussufern oder Hochwasserbecken (siehe{numref}`Fig. %s <draw-inflow>`).
* Ziehen Sie die Grenzen ausreichend weit vom interessierenden Bereich weg: Auferlegte oder unrealistische Wassertiefen (oder Wasseroberflächenerhöhungen) im Zusammenhang mit den Strömungsraten werden sonst den interessierenden Bereich stark beeinflussen. In der Regel sollte bei einer 2d-Simulation die vor- und nachgeschalteten Grenzen mindestens 800 bis 1000 m vom interessierenden Bereich entfernt sein.

```{figure} ../../img/telemac/cross-section-sx.png
:alt: draw bluekenue liquid boundary conditions conlim upstream inflow
:name: draw-inflow

Der rote hervorgehobene Teil dieses qualitativen Querschnitts sollte als Zufluss (nach oben) Randbedingung definiert werden. Mesh-Knoten an den Flussufern und an den Flutplainen sollten nicht enthalten sein.
```


(tm-foc-unpack-bc)=
## Die Struktur der Grenzen. Cli

Die stetigen 2d, unsteady 2d und Tutorials zeigen die unterschiedlichen Arten von Grenzen unter Verwendung der vorgeschriebenen Entladung (`Q`) und/oder Wassertiefe (`H`), die in eine Begrenzung `.cli`-Datei aus 13 Raum (tab) implementiert werden - getrennte Kolonen:

````{admonition} Example of a hydrodynamics boundaries.cli file (first 3 rows)
:class: note
```
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000         138           1
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9836           2
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9838           3
...
```
````

Die 13 Raum (tab) - getrennte Kolonen entsprechen 13 Grenzvariablen, die in {numref}`Table %s <tab-bc-overview>` für eine hydrodynamische Telemac2d/3d (siehe [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli)) und eine Gaia Grenzbedingungen Datei aufgeführt sind.


```{list-table} Meaning of columns in a Boundary.Cli file for Telemac2d/3d and Gaia.
:header-rows: 1
:name: tab-bc-overview

* - Spalte Nr.<br>
  - Familiäre<br>
  - Telemac2d/3d<br>
<small>*parameter*</small>
  - Gaia<br>
<small>*parameter*</small>

* - 1
  - Grenzart
  - LIHBOR<br>
<small>*Wassertiefe*</small>
  - LIHBOR<br>
<small>*Wassertiefe*</small>

* - 2.
  - Grenzart
  - LIUBOR<br>
    <small>*$x$-flowrate or $u$*</small>
  - LIQBOR<br>
<small>*sediment load*</small>

* - 3
  - Grenzart
  - LIVBOR<br>
    <small>*$y$-flowrate or $v$*</small>
  - LIVBOR<br>
<small>*velocity*</small>

* - ANHANG
  - Bezeichnung
  - HBOR<br>
<small>*Wassertiefe*</small>
  - Q2BOR<br>
<small>*sediment load*</small>

* - 5.
  - Bezeichnung
  - UBOR<br>
    <small>*$x$-flowrate or $u$*</small>
  - UBOR<br>
    <small>*$x$-flowrate or $u$*</small>

* - 6
  - Bezeichnung
  - VBOR<br>
    <small>*$y$-flowrate or $v$*</small>
  - VBOR<br>
    <small>*$y$-flowrate or $v$*</small>

* - 7
  - Bezeichnung
  - AUBOR<br>
<small>*Wandreibung*</small>
  - AUBOR<br>
<small>*Wandreibung*</small>

* - 8)
  - Grenzart
  - LITBOR<br>
<small>*tracer*</small>
  - LIEBOR (LICBOR)<br>
    <small>*flowrate* (*concentration*)</small>

* - ANHANG
  - Bezeichnung
  - TBOR<br>
<small>*tracer*</small>
  - EBOR (CBOR)<br>
<small>*Unterstützung*</small>

* - 10.
  - Bezeichnung
  - ATBOR<br>
<small>*Wärmeflüsse*</small>
  - ATBOR<br>
<small>*Wärmeflüsse*</small>

* - 11)
  - Bezeichnung
  - BTBOR<br>
<small>*Wärmeflüsse*</small>
  - BTBOR<br>
<small>*Wärmeflüsse*</small>

* - 12
  - Global Node ID
  - N<br>
<small>*Selafin mesh*</small>
  - N<br>
<small>*Selafin mesh*</small>

* - 13)
  - Lokale Node-ID
  - K <br><small>*boundary file*</small>
  - K <br><small>*boundary file*</small>

```


Die ersten drei Spalten einer `.cli`-Datei bestimmen, ob eine Grenze fest oder flüssig ist, und wenn Flüssigkeit, die Art der Flüssigkeitsgrenzen. Diese drei Spalten (z.B. LIHBOR, LIUBOR und LIVBOR) können folgende Werte annehmen:

* `0`, um eine Nullgeschwindigkeitsgrenze durchzusetzen
* `2` um eine feste (Wand) Grenze mit Reibung anzuzeigen
* `4` um einen freien Flüssigkeitsgrenzwert zu definieren
* `5`, um einen vorgeschriebenen (d.h. bestimmten) Flüssigkeitsgrenztyp zu definieren
* `6` um eine Geschwindigkeit zu verschreiben (nur für LIUBOR/LIVBOR)

Diese Werte können auch der Spalte 8 (LITBOR/LIEBOR) der Datei `.cli` zugeordnet werden. Beachten Sie, dass in einer hydrodynamischen Simulation die Kombination der Spalten 2 und 3 (LIUBOR und LIVBOR) eine effektive Entladungsgrenze ist. Alle anderen Spalten sind *Beschreibungen* und *Keine IDs*. Die *Beschreibungen* können verwendet werden, um beispielsweise einen Strömungsgeschwindigkeitswert (nicht empfohlen) aufzuerlegen. Die *Node IDs* wurden von BlueKenue (oder was auch immer Netzgenerator verwendet wurde) geschrieben und sollten nicht geändert werden. So sind in Bezug auf die Massenbilanz von Wasser die ersten drei Spalten wichtig und sie können die (gemeinsamen) Wertkombinationen zugeordnet werden, die unter {numref}`Tab. %s <bc-defs-tm>` unten aufgeführt sind. Für die Massenbilanz von Tracern kann die Spalte 8 analog definiert werden. Zusätzlich kann eine `.cli`-Datei für den Sedimenttransport mit den ersten drei Spalten ähnlich definiert werden, wie in der {ref}`Gaia tutorial <gaia-bc>` beschrieben.

```{list-table} Value combinations for the first three columns of a hydrodynamic boundaries.cli file affecting the mass balance of water.
:header-rows: 1
:name: bc-defs-tm

* - **Typ**
  - Nummerncode
  - Typische Anwendung
* - Fest
  - `2 2 2`
  - Feste Grenzen
* - Vorgeschrieben Q
  - `4 5 5`
  - {ref}`Upstream liquid <tm2d-bounds>`
* - Vorgeschrieben H
  - `5 4 4`
  - {ref}`Downstream liquid <tm2d-bounds>`
* - Vorgeschrieben H und Q
  - `5 5 5`
  - {ref}`Stream gauges <tm2d-bounds>`
```

(tm-edit-bc)=
## Bearbeiten Sie Boundary. Cli zur Änderung der Bedingungen

Um die Art der Randbedingungen anzuzeigen oder zu bearbeiten, öffnen Sie die `.cli`-Datei mit einem Texteditor (lesen Sie mehr über {ref}`text editors <npp>`). Typischerweise halten die meisten Zeilen die Wertkombination `2 2 2` in den Spalten 1-3, d.h. sie sind feste Grenzen. Die flüssigen Grenzzeilen beginnen mit `4` oder `5`, wie unter {numref}`Tab. %s <bc-defs-tm>` angegeben. Jede Zeile in der `.cli`-Datei stellt einen Knoten des Netzes dar und benachbarte Zeilen stellen benachbarte Netzknoten dar. So befindet sich der in Zeile (Linie) 435 einer `.cli`-Datei beschriebene Knoten direkt zwischen den in den Zeilen 434 und 436 der `.cli`-Datei beschriebenen Grenzknoten. Da die Definitionen in der `.cli`-Datei rein geometrische oder geometrische Attribute sind, müssen zusätzliche hydraulische Attribute in der Steuerung (`.cas`)-Datei verschrieben oder verknüpft werden. So steuert die Telemac-Lenkdatei, wie viel Wasser durch die Flüssigkeitsgrenzen fließt, und/oder die Wassertiefe/Flächenhöhe mit folgenden Keywords:

```fortran
/ Keywords in a .cas steering file
PRESCRIBED ELEVATIONS : 518.20 ; 0
PRESCRIBED FLOWRATES  : 0 ; 118.0
/ PRESCRIBED VELOCITIES : 1.0 ; 1.0 / not use simultaneously with PRESCRIBED FLOWRATES
/ PRESCRIBED DEPTH : 1.0 ; 1.0 / not use simultaneously with PRESCRIBED ELEVATIONS
```

Alternative Nutzungen dieser Schlüsselwörter finden Sie in den {ref}`unsteady 2d <tm2d-liq-file>` und {ref}`Gaia <gaia-bc>` tutorials oder in Abschnitt 4.2 der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf). Beachten Sie, dass jede `PRESCRIBED ...` Zeile Werte für jede Flüssigkeitsgrenze mit einem `;`-Zeichen trennt. Insbesondere gelten die ersten und zweiten Werte für die in der `.cli`-Datei definierten ersten und zweiten Grenzen, die von der Spitze der `.cli`-Datei aus gezählt werden (siehe nächster Absatz). Wenn einer dieser Werte `0` ist (z.B. die zweite ELEVATION und die erste FLOWRATE-Grenze), behandelt Telemac sie als freie (`4`) Flüssigkeitsgrenze.

Die Reihenfolge der Grenzen ist in der `.cli`-Datei zu finden: die erste Knotenfolge, in der Zeilen (Zeilen) entweder mit `4` oder `5` (oder `6`) beginnen, ist die erste flüssige Grenze. Da der Netzgenerator benachbarte Knoten in benachbarte Zeilen platziert, sind auch die Begrenzungslinien in benachbarten Zeilen definiert. Die folgende Box zeigt ein Beispiel für eine nachgeschaltete Grenze zwischen den Knoten 7-12 (globale IDs 144-9818). Weiter unten in der `.cli`-Datei, eine andere flüssige Grenze (z.B. `4 5 5`) könnte gefunden werden, um vorgelagerte Zuflüsse zu definieren. In diesem Fall ist die nachgeschaltete Grenze die Grenze 1 und die vorgeschaltete Grenze die Grenze 2 und beide sind entsprechend in der Lenkungsdatei (`.cas`) vorgeschrieben.

````{admonition} Example of a downstream 5 4 4 (prescribed H) boundary defined in a .cli file
:class: tip
:name: cli-example

```
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9828           6   # 
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000         144           7   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9824           8   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9831           9   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000          89          10   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9817          11   # downstream (144 - 9818)
5 4 4  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        9818          12   # downstream (144 - 9818)
2 2 2  0.000 0.000 0.000 0.000  2  0.000 0.000 0.000        7602          13   # 
```
````


## Grenzen und Konvergenz

Die Verschreibung von `5 4 4` (nur H), `4 5 5` (nur Q) oder `5 5 5` (Q und H) Randbedingungen in der {ref}`above example <cli-example>` kann zu numerischen Instabilitäten einer trocken-initialisierten Simulation oder unsymmetrischen Zu- und Abflüssen führen.

Um die Massenerhaltung zu überprüfen, finden Sie im nächsten Abschnitt unter {ref}`quantitative convergence <tm-convergence>`Analyse von Flußmitteln über (oder durch) die Flüssigkeitsgrenzen.

Um Probleme mit der Massenkonvergenz zu beheben, werfen Sie einen Blick auf unsere {ref}`workflow for mass conservation <tm-foc-mass-workflow>`.
