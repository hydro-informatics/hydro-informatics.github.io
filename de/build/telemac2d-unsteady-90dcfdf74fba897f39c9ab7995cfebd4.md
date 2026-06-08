---
description: Tutorial zur Modellierung von unruhigen (quasi-steady) Entladung und Flut Hydrographen mit Telemac2d, diskretisierende zeitverändernde Ströme für 2D Fluss hydraulische Simulationen.
---

(chpt-unsteady)=
# Unsteady 2d

```{admonition} Requirements
Dieses Tutorial ist für ** erweiterte Modellierer** konzipiert und vor dem Tauchen in dieses Tutorial sorgen Sie dafür, die {ref}`TELEMAC pre-processing <slf-prepro-tm>` und {ref}`Telemac2d steady hydrodynamic modeling <telemac2d-steady>` Tutorials zu vervollständigen.

Der in diesem Tutorial vorgestellte Fall wurde mit folgender Software erstellt:
* ein Texteditor wie {ref}`Notepad++ <npp>` (jeder andere Texteditor wird den Job machen).
* Telemac v8p2r0 oder neuer ({ref}`standalone installation <modular-install>`).
* {ref}`QGIS <qgis-install>`.
* Debian Linux 11 installiert auf einer virtuellen Maschine (weiterlesen unter {ref}`software chapter <chpt-vm-linux>`).
```

## Erste Schritte

Die {ref}`steady 2d tutorial <telemac2d-steady>` hypothesisiert, dass die Entladung eines Flusses im Laufe der Zeit konstant ist. Allerdings ist die Entladung eines Flusses nie wirklich konstant (d.h. nie stabil) und variiert leicht von Sekunde zu Sekunde, auch in kontrollierten Flüssen. Um die inhärent unruhigen Flüsse zu modellieren, können wir die zeitabhängige Entladung (z.B. ein Flut-Hydrograph) in einem numerischen Modell als eine Reihe von stetigen Entladungen diskretisieren. {numref}`Figure %s <unsteady-hydrograph>` illustriert die Diskretierung einer natürlichen Flut-Hydrographie in Stufen von stetigen Strömungen, die in diesem Kapitel verwendet werden. Beachten Sie, dass der Hydrograph ** mit Time = 15000** beginnt, was das Ergebnis der trocken-initialisierten stationären2d-Simulation ist.

```{figure} ../../img/telemac/unsteady-hydrograph.png
:alt: unsteady flow discharge quasi steady telemac telemac2d hydrodynamic
:name: unsteady-hydrograph

Die Diskretierung eines kontinuierlichen Hydrographen in Stufen von stetigen Strömen (qualitative Hydrograph für dieses Tutorial).
```

This chapter features the implementation of a quasi-steady discharge hydrograph into a hydrodynamic Telemac2d simulation through the definition of an inflow sequence (red circles in {numref}`Fig. %s <unsteady-hydrograph>`). The tutorial builds on the steady simulation of a discharge of 35 m$^3$/s and requires the following data from the {ref}`pre-processing <slf-prepro-tm>` and {ref}`steady2d <telemac2d-steady>` tutorials, which can be downloaded by clicking on the filenames:

* Das Rechennetz [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/bk-slf/qgismesh.slf)(verwendet **EPSG:32633* - ETRS 89 / UTM-Zone 33N).
* Die Randdefinitionen [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli)file.
* The results file [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) of the {ref}`dry initialized steady 2d simulation <tm2d-init-dry>` ending at `t=15000` for 35 m$^3$/s.

Betrachten Sie das Speichern der Dateien in einem neuen Ordner, wie `/unsteady2d-tutorial/`.

```{admonition} Unsteady simulation file repository
The simulation files used in this tutorial are available at [https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/](https://github.com/hydro-informatics/telemac/tree/main/unsteady2d-tutorial/).
```

(prepro-unsteady)=
## Modellanpassungen

Die Implementierung von unruhigen Strömen erfordert die Anpassung von Schlüsselwörtern und zusätzlichen Schlüsselwörtern (z.B. für die Verknüpfung von flüssigen Grenzdateien) in der Steuerungsdatei (`.cas`) aus dem stationären Tutorial ([download stationär2d.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d.cas)).

```{admonition} View the unsteady steering file
Um die Integration der unruhigen Simulations-Keywords in der Lenkdatei anzuzeigen, [download unsteady2d.cas](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/unsteady2d.cas).
```

(tm2d-hotstart)=
### Hotstart anfängliche Bedingungen

**Die folgenden Beschreibungen beziehen sich auf Abschnitt 4.1.3 in der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf).**

Um die Berechnungen zu beschleunigen und eine gut konvergierende Basislinie für die quasi-steady Berechnungen bereitzustellen, nutzt dieses Tutorial die Ausgabe der stationären 2d-Simulation mit trockenen Anfangsbedingungen wieder (siehe Abschnitt {ref}`tm2d-init-dry`). Diese Art der Modell-Initialisierung wird auch *hotstart* genannt. Um die Simulation zu starten, muss die stetige Ergebnisdatei [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dsteady.slf) als **PREVIOUS COMPUTATION FILE* definiert werden:

```fortran
COMPUTATION CONTINUED : YES
PREVIOUS COMPUTATION FILE : r2dsteady.slf / results of 35 CMS steady simulation
/ INITIAL TIME SET TO ZERO : 0 / avoid restarting at 15000
```

Ein **INITIAL TIME SET TO ZERO** Keyword kann definiert werden, um die Zeit aus der vorherigen Berechnungsdatei von `15000` an `0` zurückzusetzen. Dieses Tutorial nutzt diese Option jedoch nicht und setzt sich zum Zeitpunkt 15000 fort.

Um mehrdeutige Definitionen von Anfangsbedingungen zu vermeiden, **deaktivieren*** (d.h. Zeilen mit `/` löschen oder herauskommen) das **INITIAL CONDITIONS Keyword**:

```fortran
/ INITIAL CONDITIONS : 'ZERO DEPTH'
```

### Allgemeine Parameter

Um das in {numref}`Fig. %s <unsteady-hydrograph>` dargestellte Hydrograph zu simulieren, muss die Simulation für mindestens weitere 15000 Zeitschritte laufen (d.h. von `t=15000` bis `t=30000`). Da das Ausdrucken (Zwischen-)Ergebnisse eine signifikante Auswirkung auf die Rechenzeit hat, erhöhen Sie den grafischen Ausdruckzeitschritt auf `500` (d.h. verringern Sie die Ausdruckfrequenz im Vergleich zu `200`, die für die stetige Simulation verwendet wird):

```fortran
TIME STEP : 1.
NUMBER OF TIME STEPS : 15000
GRAPHIC PRINTOUT PERIOD : 500
LISTING PRINTOUT PERIOD : 500
```

(tm2d-liq-file)=
### Open Bounding

Dieser Abschnitt enthält die Implementierung von quasi-steady (unsteady) Strömungsbedingungen an den offenen Flüssigkeitsgrenzen mit einem zeitabhängigen Zufluss-Hydrograph und einem nachgeschalteten {term}`stage-discharge relation <Stage-discharge relation>` (erfasst die Rationalitäten hinter der Wahl von Randtypen von der {ref}`pre-processing tutorial <bk-liquid-bc>`).


```{admonition} Boundary conditions and mass balance

Die Randbedingungseinstellungen beeinflussen die Massenbilanz, was ein entscheidendes Kriterium für ein klingendes numerisches Modell ist. Lesen Sie mehr im Spotlight Kapitel über die Einrichtung {ref}`boundary conditions for mass balance <foc-mass-bc>`.
```


--

**Ein Quasi-Stand Hydrograph definieren*

Mit dem trocken-initialisierten Modell, das unter $t$=15000 endet, muss der Hydrograph unter `15000` beginnen, obwohl der Modellstart die Zeit *Null* der unruhigen Simulation darstellen wird. Um den dreieckigen Hydrograph in {numref}`Fig. %s <unsteady-hydrograph>` zu implementieren, erstellen Sie im Simulationsordner eine neue Datei namens `inflows.liq`**. Öffnen Sie die neue `inflows.liq`-Datei in einem Texteditor und fügen Sie die rot umkreisten Punkte in {numref}`Fig. %s <unsteady-hydrograph>` als zeitabhängige Flussinformationen an den **upstream (1)* und **downstream (2)* offenen (liquid) Grenzen hinzu. In dieser Datei:

* Fügen Sie einen Datei-Header mit `#`-Zeichen hinzu (Kommentierte Zeilen TELEMAC ignoriert).
* Ergänzen Sie 2 Spalten für die Zeit **T* ($t$) und stromaufwärts **Q(1)**.
* Trennen Sie die Spalten mit *spaces*.
* Die erste Spalte muss Zeit `T` mit streng monoton steigenden Werten sein und der letzte Zeitwert muss größer oder gleich dem letzten Simulations-Zeitschritt sein.

```{admonition} How does Telemac count open (liquid) boundaries?
Diese und weitere Informationen zur Definition von Grenzen finden Sie im Scheinwerferkapitel unter {ref}`boundary conditions <tm-foc-bc>`.
```

So sollte die [inflows.liq](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/inflows.liq)-Datei ähnlich aussehen:

```python
# Inflow hydrograph
#
T	Q(1)
s	m3/s
15000	35
16000	35
17000	50
19000	1130
22000	101
25000	35
99000	35
```

Die ursprüngliche *boundaries.cli*-Datei beschreibt die nachgeschaltete Grenze mit *prescribed Q und H* (Typ `5 5 5`). In der unruhigen Berechnung muss `Q` jedoch frei sein (anders muss Q(2) in `inflows.liq` mit einer zusätzlichen Spalte definiert werden) und deshalb erfordert die `boundaries.cli`-Datei einige Anpassungen:

* **Open** die bereitgestellte [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/boundaries.cli)-Datei mit einem Texteditor (z.B. {ref}`npp` unter Windows).
* Verwenden Sie Find-and-Replace (z.B. `CTRL` + `H`keys in {ref}`Notepad++ <npp>` oder `CTRL` +`F` in anderen Texteditoren):
  * **Find*** `5 5 5`
  * ** Ersetzen*** mit `4 5 5`
  * Klicken Sie auf ** Ersetzen** alle stromaufwärts liegenden Knoten.
* **Save*** die Datei als **boundaries-unsteady.cli** und schließen sie.

Um die richtigen Einstellungen zu überprüfen [Randgrenzen-unsteady.cli](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/boundaries-unsteady.cli) für die unsteady Simulation herunterladen.

In der **steering-Datei** passen Sie den **-Dateinamen für die Randbedingungen** an und fügen Sie den Link zu **inflows.liq* hinzu:

```
BOUNDARY CONDITIONS FILE : boundaries-unsteady.cli
/ ...
LIQUID BOUNDARIES FILE : inflows.liq
```

--

**Rating Curve (Stage-Discharge Relation)**
Um die Nutzung einer {term}`stage-discharge relation <Stage-discharge relation>` für eine offene (flüssige) Grenze zu aktivieren, muss das Schlüsselwort **STAGE-DISCHARGE CURVES** der Lenkdatei hinzugefügt werden. Dieses Stichwort erfordert eine Liste bestehend aus den folgenden Zahlen:

* `0` ist der **default**, der die Nutzung einer Phasenentladungskurve deaktiviert.
* `1` gilt als Funktion des berechneten Durchflusses (Entladung).
* `2` gilt als Funktion der berechneten Höhe für vorgegebene Durchflussraten (Entladung).

Das **STAGE-DISCHARGE CURVES** Schlüsselwort ist eine Liste, die einer der drei Ganzzahlen (d.h. entweder `0`, `1`, oder `2`) den offenen (liquid) Grenzen zuordnet. In diesem Tutorial aktiviert die Einstellung `STAGE-DISCHARGE CURVES : 0;1` die Nutzung einer {term}`Stage-discharge relation` für die nachgeschaltete Grenze nur dann, wenn die **upstream open border number 1* an `0` und die **downstream open limit number 1** an `0` gesetzt ist.

Das Formular (Kurve) der {term}`Stage-discharge relation` muss in einer Phase-Decharge-Datei definiert werden ({term}`ASCII` Textformat). Solche Dateien gelten typischerweise für die stromabwärtige Begrenzung eines Modells an Kontrollabschnitten (z.B. einem freien Überlaufwehr). Dieses Tutorial verwendet die folgende Beziehung, die in einer Datei namens [ratingcurve.txt (download)](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/ratingcurve.txt) gespeichert ist:

```
# Downstream ratingcurve.txt
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
```


````{admonition} How to assign different stage-discharge curves at multiple boundaries?
:class: tip, dropdown

Um {term}`stage-discharge relation <Stage-discharge relation>`s an mehreren offenen Grenzen (z.B. an Flussdiversionen oder Nebenflüssen) zu definieren, fügen Sie die Kurven zur gleichen Datei hinzu. TELEMAC erkennt automatisch, wo die Kurven durch die in Klammern angegebene Anzahl nach dem Parameternamen im Spaltenkopf gelten. Zum Beispiel, im obigen Beispiel für dieses Tutorial, sagen die Spaltenüberschriften `Z(2)` und `Q(2)` TELEMAC, diese Werte für die zweite (d.h. hier die nachgeschaltete) offene Grenze zu verwenden. Der Spaltenauftrag ist nicht wichtig, da TELEMAC den Kurventyp (d.h. entweder $Q(Z)$ oder $Z(Q)$) aus dem **STAGE-DISCHARGE CURVES** Schlüsselwort liest.

The following file block would prescribe {term}`Stage-discharge relation`s to the upstream and downstream boundary conditions in this tutorial. However, the file cannot be used here unless the upstream boundary type is changed to `5 5 5` (`prescribed H and Q`) in the `boundaries.cli` file (read more in the {ref}`pre-processing tutorial <bk-liquid-bc>`).
```
#
# Downstream Rating Curve
#
Z(2)	Q(2)
m	m3/s
371.33	35
371.45	50
371.86	101
375.73	1130
379.08	2560
#
# Upstream Rating Curve
#
Q(1)  Z(1)
m3/s  m
35    371.33
50    371.45
101   371.86
1130  375.73
2560  379.08
```
````

Um die Stage-Decharge-Datei zu verwenden, **definieren Sie die STAGE-DISCHARGE ... Keywords in der Lenkdatei*:

```
/ steering.cas
STAGE-DISCHARGE CURVES : 0;1
STAGE-DISCHARGE CURVES FILE : ratingcurve.txt
```

--

**Remove Ambiguous Open Bounding Definition Keywords**

Um mehrdeutige Definitionen der offenen Grenzen zu vermeiden, **deaktivieren*** (d.h. Zeilen mit `/` löschen oder herauskommen) die **PRESCRIBED ...** Schlüsselwörter in der Lenkdatei:

```fortran
/ PRESCRIBED FLOWRATES  : 35.;0.
/ PRESCRIBED ELEVATIONS : 374.80565;371.33
```

### Numerische Parameter

Die mit `3`, `4`, `5` oder `15` definierten Prädiktor-Korrektor-Systeme (*SCHEME FOR ...*** Schlüsselwörter setzen auf einen Parameter, der die Anzahl der Iterationen an jedem Zeitschritt für Konvergenz festlegt (siehe {ref}`steady2d tutorial <telemac2d-steady>`). Für quasi-steady-Simulationen empfehlen Telemac-Entwickler, diesen Parameter an `2` oder etwas größer zu setzen (Abschnitt 7.2.1 in der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf)). **Damit die folgende Zeile in die Lenkdatei*:

```fortran
NUMBER OF CORRECTIONS OF DISTRIBUTIVE SCHEMES : 2
```

(tm-control-sections)=
### Kontrollabschnitte

Eine konsequente Möglichkeit, Flussläufe an offenen Grenzen oder anderen bestimmten Linien (z.B. Nebeneinflüsse oder Diversionen) zu überprüfen, besteht darin, das **CONTROL SECTIONS** Keyword zu verwenden. Ein Steuerabschnitt wird durch eine Folge benachbarter Knotenzahlen definiert. Zum Beispiel, um die Flußmittel über die offenen Grenzen in diesem Tutorial zu überprüfen, überprüfen Sie die Knotenzahlen in der *boundaries.cli* Datei (z.B. 144 bis 32 für die Upstream- und 34 bis 5 für die Downstream-Grenze). Dann erstellen Sie ** eine neue Textdatei** (z.B. **control-sections.txt*) und:

* **Eine Kommentarzeile** mit einigen kurzen Informationen (z.B. `# control sections input file`) hinzufügen. Beachten Sie, dass diese Zeile ** obligatorisch* ist.
* In der **zweiten Zeile** fügen Sie eine **space-separierte Liste von 2 Integer* hinzu, wo
  * die erste ganze Zahl die Anzahl der Querschnitte definiert, und
  * die zweite ganze Zahl definiert, ob Knotennummern (d.h. IDs von *boundaries.cli* oder *qgismesh.slf*) oder Koordinaten definiert werden. Eine negative Zahl ermöglicht den Knoten-ID-Modus und eine positive Zahl ermöglicht den Koordinaten-Modus.
* **Definieren Sie so viele Querschnitte wie mit der ersten Ganzzahl definiert.** Jede Querschnittsdefinition besteht aus zwei Linien:
  * Die erste Zeile ist ein *string* (Text) ohne Leerstellen, die den Querschnitt benennen (z.B. `inflow_cs`).
  * Die zweite Linie besteht aus zwei Zahlen, die die Anfangs- und Endpunkte der Querschnitte definieren. Wenn die zweite ganze Zahl in der Dateizeile negativ ist, stellen Sie zwei platzgetrennte ganze Zahlen zur Verfügung. Wenn die zweite ganze Zahl positiv ist, geben Sie zwei platzgetrennte Koordinatenpaare (Stellen Sie einen Raum zwischen Koordinaten ein).

Beispielsweise kann die folgende *control-sections.txt*-Datei mit der stetigen Simulation in diesem Tutorial verwendet werden ([download control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/control-sections.txt)).

```
# control sections steady2d
2 -1
Inflow_boundary
144 32
Outflow_boundary
34 5
```

````{dropdown} Expand to view an example for coordinate-based control sections
Die folgende Steuerabschnittsdatei verwendet Punktkoordinaten anstatt Knoten-ID-Nummern, um drei Abschnitte zu definieren. Lesen Sie mehr unter {cite:t}`baxter2013` (d.h. Abschnitt 4.1.2 in der [Baxter tutorial](http://www.opentelemac.org/index.php/component/jdownloads/summary/4-training-and-tutorials/185-telemac-2d-tutorial?Itemid=55)).
```
# control section file using coordinates
3 0
affluent_creek
19572355.895577 626823.06664 1952347.2733 626923.9554
main_river_upstream
1946449.824 635349.6070 194.919 635209.807
main_river_downstream
1967737.56993 620784.415608 1967998.16429 620638.17849
```
````

Die zweite Zeile in dieser Datei sagt TELEMAC, `2`Steuerungsabschnitte zu verwenden, die durch Knoten-IDs (`-1`) definiert sind. Um die Steuerungsabschnitte für die Simulation zu verwenden, fügen Sie folgendes zur Lenkdatei hinzu:

```
/ steady2d.cas
/ ...
SECTIONS INPUT FILE :  control-sections.txt
SECTIONS OUTPUT FILE : r-control-flows.txt
```

So wird das Nachlaufen der Simulation die Flussmittel über die beiden definierten Steuerabschnitte in eine Datei namens *r-control-flows.txt* schreiben. Die [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) gibt Erläuterungen in Abschnitt 5.2.2.

## Führen Sie Telemac2d Unsteady

Gehen Sie in den Konfigurationsordner der lokalen TELEMAC-Installation (z.B. `~/telemac/v9.0.0/configs/`) und laden Sie die Umgebung (z.B. `pysource.openmpi.sh` - verwenden Sie die gleiche wie für die Erstellung von TELEMAC).

```
cd ~/telemac/v9.0.0/configs
source pysource.gfortranHPC.sh
```

````{admonition} If you are using the Hydro-Informatics (Hyfo) Mint VM
:class: note, dropdown

Wenn Sie mit der {ref}`Mint Hyfo VM <hyfo-vm>` zusammenarbeiten, laden Sie die TELEMAC-Umgebung wie folgt ein:

```
cd ~/telemac/v8p2/configs
source pysource.hyfo-dyn.sh
```
````

Mit der geladenen TELEMAC-Umgebung wechseln Sie in das Verzeichnis, in dem die unruhige Simulation lebt (z.B. `/home/telemac/v9.0.0/mysimulations/unsteady2d-tutorial/`) und die `*.cas`-Datei mit dem **telemac2d.py**-Skript ausführen.

```
cd ~/telemac/v9.0.0/mysimulations/unsteady2d-tutorial/
telemac2d.py unsteady2d.cas
```

````{admonition} Speed up
Mit {ref}`parallelism <tm-system-wide-opts>` aktiviert (z.B. in der {ref}`Mint Hyfo Virtual Machine <hyfo-vm>`) beschleunigen Sie die Berechnung mithilfe mehrerer Kerne über die `--ncsize=N`-Flagge. So läuft die folgende Zeile auf `N=2` Cores:

```
telemac2d.py unsteady2d.cas --ncsize=2
```
````
Eine erfolgreiche Berechnung sollte mit folgenden Zeilen (oder ähnlichen) in *Terminal* enden:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                            10  MINUTES
                            32  SECONDS
... merging separated result files

... handling result files
       moving: r2dunsteady.slf
       moving: r-control-sections.txt
... deleting working dir

My work is done
```

Telemac2d wird die Dateien *r2dunsteady.slf* und *r-control-sections.txt* schreiben. Beide Ergebnisse sind auch im TELEMAC-Repository dieses eBook verfügbar, um das Nachbearbeitungs-Tutorial zu erreichen:

* [get r2dunsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r2dunsteady.slf) und
* [mit r-control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/unsteady2d-tutorial/r-control-sections.txt).


## Nachbearbeitung

### Open Boundary Flows

Die unruhige Simulation beabsichtigt, zeitvariable Ströme (Grippen) über die vor- und nachgeschalteten Flüssigkeitsgrenzen zu modellieren. Die oben definierten {ref}`control sections <tm-control-sections>` ermöglichen Einblicke in die korrekte Anpassung des Flusses an die stromaufwärtige Zuflussgrenze (*vorgeschrieben Q* durch *inflows.liq*) und die stromabwärtige Abflussgrenze (*vorgeschrieben H* durch *ratingcurve.txt*). {numref}`Figure %s <res-unsteady-hydrograph>` zeigt die modellierten Durchflussraten, bei denen der *Inflow boundary* eine perfekte Übereinstimmung mit *inflows.liq* zeigt und der *Outflow boundary* die Abflachung der Abflusskurve im modellierten mäanderförmigen Schotterbettfluss widerspiegelt.

```{figure} ../../img/telemac/res-unsteady-hydrograph.png
:alt: result unsteady flow discharge telemac2d hydrodynamic inflow outflow control sections
:name: res-unsteady-hydrograph

Die simulierten Ströme fließen über die vorgeschalteten *Inflow boundary* und die nachgeschalteten *Outflow boundary* Steuerabschnitte.
```

Der Spitzenzufluss entspricht den angegebenen 1130 m$^3$/s, während der Abflussspitzenabfluss nur 889 m$^3$/s beträgt und der Peak ca. 1070 Sekunden dauert (Zufluss bei $t$=19000 und Abfluss bei $t\approx$20070), um durch den Abschnitt zu reisen.


````{admonition} Resolve volume balance issues in unsteady simulations
:class: warning, dropdown
Die gesamten Zu- und Abflussmengen in der hier vorgestellten Simulation betragen 3479930.958 m$^3$ und 3430100.437 m$^3$. So gibt es einen Gesamtvolumenfehler von 1.4$\%$. Um solche Probleme zu überwinden, empfiehlt die [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf), einen Mindestwert für die Wassertiefe zu verwenden, um zu definieren, wann eine Zelle nass oder trocken ist. Gleichzeitig empfehlen die Entwickler keine Mindestwassertiefe für die meisten Simulationen und betonen, diese Option nur für unruhige (quasi-steady) Simulationen zu verwenden. Die Festlegung einer Mindestwassertiefe erfordert die Einstellung des Schlüsselworts **TREATMENT OF THE TIDAL FLATS** an `2` (weiterlesen in der {ref}`steady2d tutorial <tm2d-tidal>`), das weder mit Parallelisierungsroutinen kompatibel ist, noch mit den hier verwendeten `SCHEME FOR ADVECTION ... : 14`-Einstellungen. So könnten bessere Ergebnisse, aber lange nicht-parallelisierte quasi-steady Berechnungen mit den folgenden Keywords in der Lenkdatei erhalten werden:

```fortran
OPTION FOR THE TREATMENT OF TIDAL FLATS : 2 / use segment-wise flux control
MINIMUM VALUE OF DEPTH : 0.1 / in meters
```
````

(tm-unsteady-qgis)=
### Visualisierung mit QGIS

Die Ergebnisse der unruhigen Simulation können visualisiert und Snapshots exportiert werden, z.B. {term}`GeoTIFF` oder Shapefile-Formate in QGIS, ähnlich wie in der {ref}`steady2d post-processing <tm2d-post-export>`. Insbesondere die neuesten QGIS-Release ermöglichen es, die Selafin-Ergebnisse mesh-Datei (hier: *r2dunsteady.slf*) als QGIS-Netzschicht zu laden. Daher **launch QGIS**, gehen Sie zum **Layer**-Menü und klicken Sie auf **Add Layer****** ** Hinzufügen von Mesh Layer...* Im Popup-Fenster (*Data Source Manager / Mesh*), **select r2dunsteady.slf**, click **Add**, and **Close**. {numref}`Figure %s <qgis-r2dunsteady-imported>` zeigt die importierte r2dunsteady mesh-Schicht in QGIS mit einer *Softlight*-Mischung (in der *Symbology*) auf Google-Satellitenbild.

```{figure} ../../img/telemac/qgis-r2dunsteady-imported.png
:alt: qgis telemac2d unsteady quasi steady simulation results slf
:name: qgis-r2dunsteady-imported

Die unsteady (quasi-steady) Simulationsergebnisse Datei r2dunsteady.slf importiert als Netzschicht in QGIS und überlagert auf google Satellitenbild {cite:p}`googlesat`.
```

```{admonition} r2dunsteady.slf (results file) not correctly showing in QGIS
:class: error, dropdown

Ist die Ergebnisdatei `r2dunsteady.slf` nicht in QGIS angezeigt? Stellen Sie sicher, dass es mit seiner richtigen Georeferenz importiert wird: **EPSG:32633** (ETRS 89 / UTM-Zone 33N).
```


Die Simulationsausgangsparameter (z.B. `U`, `V`, oder `Q`) an einem ausgewählten Zeitschritt können in den Schichteigenschaften der `r2dunsteady`-Schicht gesteuert werden (Doppelklicken Sie darauf im *Layers*-Panel).

Um ein Video der Simulationsergebnisse** zu erstellen, verwenden Sie den **Time Controller** (siehe Aktivierung unter {numref}`Fig. %s <qgis-time-controller-tm-recall>`). Die Frequenz der Bilder kann durch Klicken auf das Zahnrad des Zeitreglers eingestellt werden, und Bildsequenzen, die durch Klicken in der *Play* Taste gespielt werden. Zusätzlich verwendet {numref}`Fig. %s <qgis-time-controller-tm>` eine Überlagerung von Wassertiefe Pixelfarben (Kontourendiagramm) und Strömungsgeschwindigkeitsvektoren, die im *Layer Styling* Panel definiert sind. Die Nord- und Entladepfeile und der Titel sind *Dekoratoren*, die in **View******Decorators* gefunden werden können.

````{admonition} Expand to see the Time Controller
```{figure} ../../img/telemac/qgis-time-controller.jpg
:alt: time controller qgis telemac
:name: qgis-time-controller-tm-recall

Der aktivierte Zeitregler in QGIS ermöglicht es, sich entlang der Zeitachse der modellierten Größen zu bewegen (Hintergrundkarte: {cite:t}`googlesat`satellitenbild). Die rot beleuchteten Tasten aktivieren den Zeitregler, spielen die Abfolge von Bildern ausgewählter Größen, stellen eine Einstellung zum Abspielen einer Frequenz von Bildern pro Sekunde und ermöglichen das Speichern von Bildern aller Zeitschritte (siehe unten).
```
````

Die exportierte Bildreihe kann in ein Video mit Video-Editing-Software umgewandelt werden, wie z.B. die einfachen und kostenlosen [OpenShot](https://www.openshot.org/)(gut für Windows) oder [kdenlive](https://kdenlive.org/)(gut für Linux)-Tools. Das unten angezeigte Feld verfügt über ein exemplarisches Video, das mit [kdenlive](https://kdenlive.org/)2@ erstellt wurde.

```{admonition} Expand to view the results as video
:class: tip, dropdown
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/UJovUYb_Bo0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Sebastian Schwindt <a href="https://www.youtube.com/@hydroinformatics">@ Hydro-Morphodynamics channel on YouTube</a>.</p>
```
