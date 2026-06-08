---
description: Leitfaden für laufende TELEMAC-GAIA morphodynamische Simulationen und Analyse von Sedimenttransportergebnissen einschließlich Bettlast, Schwebelastung und Bettentwicklung.
---

(gaia-run)=
# Laufen und analysieren

## Laufen Sie Gaia

Stellen Sie sicher, dass der Simulationsordner (z.B. `/gaia2d-tutorial/`) mindestens die folgenden Dateien enthält (oder ähnlich, je nach Simulationsfall):

* Ein Rechennetz beispielsweise in Form von [qgismesh.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/qgismesh.slf).
* Eine hydrodynamische Begrenzungsdefinitionsdatei, z.B. in Form von [boundaries.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries.cli).
* Eine Gaia-Grenzedefinition beispielsweise in Form von [boundaries-gaia.cli](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/boundaries-gaia.cli).
* Eine Ergebnisdatei einer Telemac2d/3d-Simulation für eine Hotstart-Initialisierung, z.B. für 35 m$^3$/s in Form von [r2dsteady.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady.slf) (Ergebnis der {ref}`dry-initialized steady run <tm2d-init-dry>` ending at`t=15000`).
* Eine Telemac2d-Lenkdatei, wie [steady2d-gaia.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/steady2d-gaia.cas).
* Eine Gaia-Lenkungsdatei, wie [gaia-morphodynamics.cas](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/gaia-morphodynamics.cas).

````{dropdown} Expand to review the Gaia steering file **gaia-morphodynamics.cas**
```fortran
/------------------------------------------------------------------/
/ Gaia in TELEMAC
/ GAIA STEERING FILE
/ file name: gaia-morphodynamics.cas
/
/------------------------------------------------------------------/
/                    COMPUTATION ENVIRONMENT
/------------------------------------------------------------------/
/
BOUNDARY CONDITIONS FILE : boundaries.cli
GEOMETRY FILE : qgismesh.slf
RESULTS FILE : rGaia-steady2d.slf
VARIABLES FOR GRAPHIC PRINTOUTS : B,E,M,MU,N,P,QSBL,TOB
MASS-BALANCE : YES
/
/ NUMERICAL OPTIONS
/------------------------------------------------------------------/
FINITE VOLUMES : NO
/------------------------------------------------------------------/
/
/------------------------------------------------------------------/
/ RIVERBED COMPOSITION
/------------------------------------------------------------------/
/
/ SEDIMENT
CLASSES TYPE OF SEDIMENT : NCO;NCO;NCO / CO-cohesive or NCO-non-cohesive
CLASSES SEDIMENT DIAMETERS : 0.0005;0.02;0.1 / in m
CLASSES SEDIMENT DENSITY : 2680;2680;2680 / in kg per m3
/
/ RIVERBED LAYERS - manual section 3.2.1
ACTIVE LAYER THICKNESS : 0.3 / multiple of D90 - default is 10000
NUMBER OF LAYERS FOR INITIAL STRATIFICATION : 3 / default is 1
LAYERS INITIAL THICKNESS : 1.5 / m - default is 100
/
/------------------------------------------------------------------/
/ BEDLOAD
/------------------------------------------------------------------/
/
/ BOUNDARIES
PRESCRIBED SOLID DISCHARGES : 10.;0.
/
BED LOAD FOR ALL SANDS : YES / deactivate with NO
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1 / MPM - see table for more
CLASSES SHIELDS PARAMETERS : 0.047;0.047;0.047
MPM COEFFICIENT : 8
/
/ BEDLOAD DIRECTION - manual sec. 3.1.4-3.1.7
SLOPE EFFECT : YES / default is YES - set to NO to disable
FORMULA FOR DEVIATION : 1 / use 2 for talmon-1995 approach
FORMULA FOR SLOPE EFFECT : 1 / default is 1 (koch-flokstra) change to 2 for soulsby
BETA : 1.3 / only with koch-flokstra - default is 1.3
/
/ SECONDARY CURRENTS - manual sec. 3.1.7
SECONDARY CURRENTS : YES / default is NO
SECONDARY CURRENTS ALPHA COEFFICIENT : 0.8 / default is 1.
/
/ FRICTION
SKIN FRICTION CORRECTION : 1 / set 0 to disable correction in shallow waters
RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER : 3. / default is 3.
/
/------------------------------------------------------------------/
/ SUSPENDED LOAD
/------------------------------------------------------------------/
/
SUSPENSION FOR ALL SANDS : YES / deactivate with NO
/
SUSPENSION TRANSPORT FORMULA FOR ALL SANDS : 1
/
/ NUMERICAL PARAMETERS
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14
/
/ ADDITIONAL SEDIMENT - manual section 4.2
CLASSES SETTLING VELOCITIES : -9;-9;-9 / use Gaia defaults
CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION : 1000;1000;1000 / N per m2
LAYERS PARTHENIADES CONSTANT : 1.E-03 / in kg per m2 per s - default is 1.E-03
```
````

Öffnen Sie mit diesen Dateien *Terminal*, gehen Sie in den Konfigurationsordner TELEMAC (z.B. `~/telemac/v9.0.0/configs/`) und laden Sie die Umgebung (z.B. `pysource.openmpi.sh` - verwenden Sie die gleiche wie für die Erstellung von TELEMAC).

```
cd ~/telemac/v9.0.0/configs
source pysource.openmpi.sh
```

```{admonition} Environment loading varies by installation
:class: note, dropdown

Der genaue Befehl zum Laden der TELEMAC-Umgebung hängt von Ihrer Installationskonfiguration ab. Zu den allgemeinen Varianten gehören:

* **Standardinstallation**: `source pysource.openmpi.sh` oder `source pysource.gfortran.sh`
* **Intel Compiler**: `source pysource.intel.sh`
* **Kundenspezifische Konfigurationen*: Überprüfen Sie Ihren `configs/`-Ordner für verfügbare `pysource.*.sh` Dateien

Wenn Sie Modul-Lastfehler auftreffen, überprüfen Sie, ob alle erforderlichen Abhängigkeiten (Python, MPI, Compiler) ordnungsgemäß installiert und konfiguriert sind. Für die Fehlerbehebung wenden Sie sich an die {ref}`TELEMAC installation guide <modular-install>`.
```

Mit der geladenen TELEMAC-Umgebung wechseln Sie in das Verzeichnis, in dem die TELEMAC Gaia-Simulation lebt (z.B. `/home/telemac/v9.0.0/mysimulations/gaia2d-tutorial/`) und die `*.cas`-Datei ausgeführt wird, indem sie mit dem Skript **telemac2d.py** aufgerufen wird (es wird automatisch wissen, dass es Gaia verwenden muss, wenn es die Zeile `COUPLING WITH : 'GAIA'` liest).

```
cd ~/telemac/v9.0.0/mysimulations/gaia2d-tutorial/
telemac2d.py steady2d-gaia.cas
```

````{admonition} Speed up with parallel computing
Mit {ref}`parallelism <tm-system-wide-opts>` aktiviert, beschleunigen Sie die Berechnung mit mehreren Kernen über die `--ncsize=N`-Flagge. Die folgende Zeile führt z.B. die Simulation auf `N=4` Kernen aus:

```
telemac2d.py steady2d-gaia.cas --ncsize=4
```

**Leitlinien für die Auswahl `ncsize`:**
* Starten Sie mit `ncsize` gleich der Anzahl der physischen CPU-Kerne (nicht Hyperthreads)
* Bei kleinen Maschen (< 10.000 Knoten) kann die Parallelisierung über Kopf überwiegende Vorteile
* Für große Maschen (> 100.000 Knoten) sind signifikante Beschleunigungen erreichbar
* Überwachen Sie die CPU-Nutzung während der Laufzeiten, um `ncsize` für Ihr System zu optimieren

** Zusätzliche nützliche Flaggen:**
* `--nctile=N`: Anzahl der Sub-Domains für Domänenzersetzung (Standard gleich `ncsize`)
* `--ncnode=N`: Anzahl der Rechenknoten für Cluster-Läufe
* `-s` oder `--sortie`: Nur den Verschmelzungsschritt erneut ausführen (verwendend, wenn Simulation abgeschlossen, aber Verschmelzung gescheitert ist)
* `-c` oder `--compileonly`: Nur kompilieren Benutzer Fortran Dateien ohne Laufen
* `--clean`: Entfernen Sie temporäre Dateien vor dem Start
````

```{admonition} Common runtime errors and solutions
:class: warning, dropdown

**Fehler: "STOP CALLED - INCREASE ARRAY SIZE"*
* Ursache: Unzureichende Speicherzuordnung für das Netz oder Variablen
* Lösung: Reduzieren Sie die Maschengröße oder erhöhen Sie den verfügbaren Speicher; überprüfen Sie die Netzqualität Probleme

**Fehler: "NEGATIVE WATER DEPTH"**
* Ursache: Numerische Instabilitäten, oft aus zu großer Zeit oder schlechter Netzqualität
* Lösung: Reduce `TIME STEP`, Enable `TREATMENT OF NEGATIVE DEPTHS : 2`, Verbesserung der Netzqualität in Problembereichen

**Fehler: "SOLVER NOT CONVERGED"**
* Ursache: Linearer Soldat konnte kein Konvergenzkriterium erreichen
* Lösung: Erhöhen Sie `MAXIMUM NUMBER OF ITERATIONS FOR SOLVER`, entspannen Sie `SOLVER ACCURACY` oder überprüfen Sie Randbedingungen

**Fehler: "FLOATING POINT EXCEPTION"*
* Ursache: Division durch Null oder Überlauf, oft aus sehr kleinen Wassertiefen
* Lösung: Erhöhen `MINIMAL VALUE OF THE WATER HEIGHT`, check initial conditions

**Gaia-spezifische: "NEGATIVE KONZENTRATION"*
* Ursache: Numerische Instabilitäten im Advektionssystem
* Lösung: Verwenden Sie Schema `14` oder `15` für suspendierte Sedimente, reduzieren Sie Zeitschritt, überprüfen Sie die Randbedingungen für suspendierte Last
```

Eine erfolgreiche Berechnung sollte mit folgenden Zeilen (oder ähnlichen) in *Terminal* enden:

```fortran
[...]
                    *************************************
                    *    END OF MEMORY ORGANIZATION:    *
                    *************************************

CORRECT END OF RUN

ELAPSE TIME :
                             1  HOURS
                             4  MINUTES
                            34  SECONDS
... merging separated result files

... handling result files
       moving: r2dsteady-gaia.slf
       moving: rGaia-steady2d.slf
       moving: r-control-sections.txt
... deleting working dir

My work is done
```

TELEMAC wird die Dateien *r2dsteady-gaia.slf*, *rGaia-steady2d.slf* und *r-control-sections.txt* im Simulationsordner schreiben. Diese Ergebnisdateien sind auch in dem Modellierungs-Repository dieses eBooks für das Nachbearbeitungs-Tutorial verfügbar:

* [Download r2dsteady-gaia.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r2dsteady-gaia.slf) (Ergebnisse der Hydrodynamik)
* [Download rGaia-steady2d.slf](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/rGaia-steady2d.slf) (Ergebnisse der Morphodynamik)
* [Download r-control-sections.txt](https://github.com/hydro-informatics/telemac/raw/main/gaia2d-tutorial/r-control-sections.txt) (Kontrollabschnitt Flussläufe)

```{admonition} Understanding the output files
:class: note

**r2dsteady-gaia.slf* enthält die in der Telemac2d-Lenkdatei definierten hydrodynamischen Größen (z.B. Geschwindigkeit, Wassertiefe, freie Oberflächenerhebung). Diese werden von Telemac2d mit dem Bett Evolution Feedback von Gaia berechnet.

**rGaia-steady2d.slf** enthält die in der Gaia-Lenkungsdatei definierten morphodynamischen Größen (z.B. Bodenhöhe, Bettlasttransportraten, Sedimentkonzentrationen). Die Variablen entsprechen dem **VARIABLES FOR GRAPHIC PRINTOUTS** Keyword in `gaia-morphodynamics.cas`.

**r-control-sections.txt** enthält Zeitreihen von Flußmitteln über die definierten Steuerabschnitte. Jede Zeile stellt einen Zeitschritt mit Spalten für den integrierten Fluss jedes Abschnitts dar.
```

## Nachbearbeitung

### Kontrollbereich Fluxen

Die {ref}`control sections <tm-control-sections>` ermöglichen Einblicke in die korrekte Anpassung des Flusses an die vor- und nachgelagerten Grenzen (nur vorbeschrieben Q). {numref}`Figure %s <gaia-hydrograph>` zeigt die modellierten Durchflussraten, bei denen die *Inflow boundary* und *Outflow boundary*-Kurven nach ca. 10000 Zeitschritten konvergieren. Beachten Sie, dass die Grafik absolute Zahlen zeigt, während die ursprüngliche Ausgabe in *r-control-sections.txt* aufgrund der Reihenfolge der Knotendefinitionen in *control-sections.txt* negativ ist. Die {ref}`hotstart <gaia-hotstart>` Initialisierung macht aus, dass die Flußmittel von Anfang an um den vorgeschriebenen Zufluss von 35 m$^{3}$/s schwanken. Der *Outflow boundary* Flussratenzuwachs zum Ende der Simulation kann auf die Sedimenterosion und den nachgeschalteten freien Fluss (`544-4`) zurückgeführt werden.

```{figure} ../../img/telemac/gaia-hydrograph.png
:alt: result flow discharge telemac2d morphodynamic gaia inflow outflow control sections
:name: gaia-hydrograph

Die simulierten Ströme fließen über die vorgeschalteten *Inflow boundary* und die nachgeschalteten *Outflow boundary* Steuerabschnitte.
```

```{admonition} How to distinguish water fluxes at inflow and outflow control sections from sediment transport rates?
Mit den beiden {ref}`boundary files for Telemac2d and Gaia <gaia-bc>` ist es möglich, verschiedene Randtypen in den hydrodynamischen (*steady2d-gaia.cas*) und morphodynamischen (*gaia-morphodynamics.cas*) Lenkdateien zu verwenden. So können Wasservolumenflüsse am Zulauf und den Abflussabschnitten durch `455`-Grenzen (nur vorbeschrieben Q) in den hydrodynamischen Lenk- und/oder Begrenzungsdateien verschrieben werden. So passen Sie z.B. mit `455`-Typ vor- und nachgeschalteten hydrodynamischen Grenzen das **PRESCRIBED FLOWRATES* Schlüsselwort an `35.;35` in der hydrodynamischen Lenkdatei (*steady2d-gaia.cas*) an, ohne die Morphodynamik (Gaia)-Grenz und Lenkdateien zu ändern.
```

```{admonition} Sediment mass balance verification
:class: tip
Um den Sedimentmassenschutz zu überprüfen, aktivieren Sie in der Gaia-Lenkungsdatei `MASS-BALANCE : YES`. Die Auflistungsleistung wird dann die Sedimentmassenbilanzinformation in jeder Ausdruckperiode beinhalten:

* **Initialmasse**: Gesamte Sedimentmasse zu Simulationsbeginn
* ** Endmasse**: Gesamte Sedimentmasse zum aktuellen Zeitpunkt
* **Mass Flußmittel*: Sediment betreten/verlassen durch Grenzen
* **Fehler**: Relative Massenbilanzfehler (sollte bei gut konfigurierten Simulationen < 1% betragen)

Große Massenbilanzfehler (> 5%) zeigen mögliche Probleme mit Randbedingungen, Advektionsplänen oder numerischen Instabilitäten.
```

### Visualisierung mit QGIS

The results of the Gaia simulation can be visualized and time snapshots exported to raster (e.g., {term}`GeoTIFF`) or shapefile formats by using the PostTelemac plugin in QGIS the same way as explained in the {ref}`steady2d tutorial <tm2d-post-export>`. The latest QGIS releases additionally enable loading of a Selafin (results) mesh file (here: *r2dsteady-gaia.slf*) as QGIS mesh layer, which can then be visualized in the viewport and exported to a video with the Crayfish plugin. To this end, **launch QGIS**, **set the {ref}`project CRS <qgis-project>` to EPSG:25833** (ETRS89 / UTM zone 33N), and save the new project in the `gaia2d-tutorial/` folder (or where ever the Gaia simulation files live). In QGIS' **Browser** panel, find the **Project Home** folder, expand it, and drag-and-drop the two simulation results meshes (*r2dsteady-gaia.slf* and *rGaia-steady2d.slf*) to the **Layers** panel.

Doppelklicken Sie auf *r2dsteady-gaia.slf* oder *rGaia-steady2d.slf*, um ihre **Mesh Layer Properties* zu öffnen, dann gehen Sie auf die **Source** Tab, um hydrodynamische (z.B. *Wassertiefe* oder *Scalar Flowrate m2s*) oder morphodynamische Gaia (z.B. *qs bedload) {numref}`Figure %s <qgis-gaia-mesh-properties>` zeigt das Fenster QGIS mesh Layer Properties des *rGaia-steady2d.slf*-Simulationsergebnisses Geometrie, in dem rote Boxen Schritte zum Anbinden von Ausgabevariablen und Visualisierungs-Zeitschritten hervorheben. Darüber hinaus bietet die Registerkarte **Symbology* Optionen für Wertfarbskala oder Vektordarstellungen (z.B. für Geschwindigkeitsvektoren in *r2dsteady-gaia.slf*).

```{figure} ../../img/telemac/qgis-gaia-mesh-properties.png
:alt: qgis telemac2d gaia morphodynamics solid discharge bedload results slf
:name: qgis-gaia-mesh-properties

Das Fenster Mesh Layer Properties mit der Registerkarte Source zur Auswahl von Gaia Ausgabevariablen. Der Screenshot zeigt Schritte zur Visualisierung von *qs Bettlast* bei der Simulationsendzeit (rote Boxen). Darüber hinaus können Plot-Farbbereiche in der Symbology-Tab (gestrichelte rote Box) angepasst werden.
```

```{admonition} rGaia-steady2d.slf (results file) not correctly showing in QGIS
:class: error, dropdown

Ist die Ergebnisdatei `rGaia-steady2d.slf` nicht in QGIS angezeigt? Stellen Sie sicher, dass es mit seiner richtigen Georeferenz importiert wird: **EPSG:25833** (ETRS 89 / UTM-Zone 33N). Wenn das Netz an der falschen Stelle oder mit verzerrter Geometrie erscheint, überprüfen Sie Folgendes:

1. Das Projekt Koordinatenreferenzsystem entspricht dem Netz Koordinatenreferenzsystem (EPSG:25833)
2. Bei Verwendung eines anderen Projekts ist eine Neuprojektion auf dem Flugplatz möglich.
3. Die ursprüngliche Geometriedatei verwendete das korrekte Koordinatenreferenzsystem

Um die Schicht Koordinatenreferenzsystem manuell einzustellen: Rechtsklicken Sie auf die Schicht → **Set Koordinatenreferenzsystem* → **Set Layer Koordinatenreferenzsystem...** → Suche nach EPSG:25833.
```

Beachten Sie, dass nur Parameter, die mit den **VARIABLES FOR GRAPHIC PRINTOUTS** Schlüsselwörtern in den hydrodynamischen ({ref}`steady2d-gaia.cas <tm2d-gen>`) und morphodynamischen ({ref}`gaia-morphodynamics.cas <gaia-gen>`) Lenkdateien definiert sind, in QGIS eingetragen werden können.

```{admonition} Key Gaia output variables for visualization
:class: tip
Für die Analyse morphodynamischer Simulationen sind insbesondere folgende Variablen nützlich:

| Variable | Beschreibung | Einheit |
|----------------------------
| `B` | Tiefenansicht
| `E` | Bottom Evolution (Auswahl) | m |
| `QSBL` | Beladungstransportrate (pro Stückbreite) | kg/(m·s) |
| `QS` | Vollständige Entladung | kg/s |
| `TOB` Belastung des Bettes | N/m2 |
| `MU` | Reibungskorrekturfaktor | - |
| `CS*` | Sedimentkonzentration (pro Klasse) | g/l |
| `ES*` | Schichtdicke (pro Schicht) | m |
| `A*`, `R*` | Sediment-Klassenanteile in der aktiven Schicht | - |

Fügen Sie diese in **VARIABLES FOR GRAPHIC PRINTOUTS** ein, um die Visualisierung zu ermöglichen.
```

Um ein Video der Simulationsergebnisse zu exportieren, verwenden Sie das *Crayfish* Plugin:

* In QGIS stellen Sie sicher, dass das Crayfish-Plugin installiert ist (Recall the {ref}`QGIS instructions <qgis-tbx-install>`).
* Im **Layer**-Panel wählen Sie **rGaia-steady2d** (oder *r2dsteady-gaia*).
* Mit *rGaia-steady2d* (oder *r2dsteady-gaia*) ausgewählt, gehen Sie zu **Mesh** (Dropdownmenü oben) > ** Krebs** > **Export Animation ...** (wenn die Schicht nicht hervorgehoben wird, erscheint eine Fehlermeldung: *Bitte wählen Sie eine Mesh Layer für den Export*).
* Im Fenster **Export Animation** gehen Sie auf die Registerkarte **General** und definieren einen Ausgabedateinamen, indem Sie auf die Schaltfläche **...** klicken (z.B. `velocity-video.avi`).
* Optional die Einstellungen *Layout* und *Video* anpassen.
* Klicken Sie auf **OK**, um den Videoexport zu starten.

Das erste Mal, dass ein Video exportiert wird, erfordert Crayfish die Definition eines **FFmpeg Video-Encoder* und führt durch die Installation (falls erforderlich). Folgen Sie den Anweisungen und starten Sie erneut das Video exportieren. Das folgende Video wurde mit Crayfish exportiert, um Geschwindigkeitsvektoren zu visualisieren:

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/jFgwiAsElH0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Video: Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Beachten Sie, wie sich die Geschwindigkeitsvektoren über die Zeit entwickeln und dass hohe Strömungsgeschwindigkeiten an Rampen/Schillen im Flussabschnitt auftreten (z.B. die beiden transversalen Maxima nahe der stromaufwärtigen Grenze oder das transversale Maximum nahe der stromabwärtigen Grenze). Dementsprechend sollte auch der Bettlasttransport an den Rampen ausgesprochen werden. Das folgende Video zeigt *qs Bettlast*, um zu überprüfen, ob das Modell die physische Verbindung zwischen Strömungsgeschwindigkeit und Bettlast rechts bekam.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/BUaqvWZ_AVk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> <p>Video: Sebastian Schwindt <a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Nach dem Video-Beobachten kann geschlossen werden, dass die Beziehung zwischen Strömungsgeschwindigkeiten und Bettlast ungefähr korrekt ist, aber das Modell kann eine Korrektur durch Anpassung {ref}`magnitude and direction parameters <gaia-dir>` verlangen. Der nächste Abschnitt veranschaulicht beispielhaft, wie die physikalische Klanglichkeit des Modells analysiert und verbessert werden kann.


(bl-plausability)=
## Plausibilität

Die oben dargestellten Ergebnisse verfügen über eine stationäre Beladung und einen hängenden Lasttransport in einer Armored-Bett-Fluss-Sektion bei einer niedrigen Basisstromentladung von 35 m$^{3}$/s. Der Vergleich der Strömungsgeschwindigkeit und der Sedimenttransportvideos deutet darauf hin, dass bei hoher Strömungsgeschwindigkeit auch die höchsten Sedimenttransportraten auftreten. Drei Sedimentgrößenklassen wurden in der {ref}`Basic Setup of Gaia <gaia-sed>` mit durchschnittlichen Korndurchmessern von 0,0005 m, 0,02 m und 0,1 m definiert. Die Simulation prognostiziert, dass sich nur die feinste Korngrößenklasse im Basisstrom bewegen wird (z.B. in der Konsolenausgabe während der Simulation). Diese feine Sedimentklasse von 0,5 mm Durchmesser (Sand) wird in Form von Bettlast und in Suspension ohne messbare Wirkung auf Betthöhe transportiert. So kann das Modell im Wesentlichen physikalisch sinnvoll angenommen werden, insbesondere wenn man bedenkt, dass trotz des lokalen Sedimenttransportmaximums für feines Sediment nahezu keine Veränderung der Flussbetthöhe modelliert wird. Um die physikalische Plausibilität eines morphodynamischen Modells zu überprüfen, sollten höhere (Flut) Entladungen testsimuliert werden. Dann sollten sich auch die gröberen Korngrößen von 0,02 m (Griff) und 0,1 m (Kies) bewegen.

```{admonition} A physical plausibility check is not a model validation
Die physikalische Plausibilitätsprüfung dient der Überprüfung, ob die Simulationsergebnisse physikalisch klingen. Physikalisch nicht-meaningful Ergebnisse wären beispielsweise dann, wenn die Wassertiefe in einer stetigen Simulation permanent ansteigt, wenn Wasser über Flutplaine am Basisstrom fließt oder das Modell an undefinierten Grenzknoten verlässt, oder wenn sich kein Sediment bei hoher Entladung (z.B. eine 100-jährige Flut) über ein alluviales Flussbett bewegt. Die Modellvalidierung erfolgt nach der Kalibrierung (siehe nächster Abschnitt).
```

Auch Wassertiefe, Strömungsgeschwindigkeit (Vektoren) und {term}`Topographic change` ist zu analysieren (in QGIS oder BlueKenue), da Gaia Flussbetthöhen verändert. Wenn das Modell z.B. {term}`Topographic change` in Form von 10-m tiefen Erosion (Scour) am Basisflow prognostiziert, sollten die Stichwortdefinitionen für die {ref}`riverbed <gaia-active-lyr>` überarbeitet werden. Ebenso sollten hydromorphodynamische relevante Parameter wie {ref}`friction <c-friction>` oder {ref}`direction and magnitude (bedload) <gaia-dir>` Korrektoren überprüft werden.

```{admonition} Plausibility checklist for morphodynamic simulations
:class: tip

Vor der Kalibrierung überprüfen Sie Folgendes:

**Hydrodynamik:**
- [ ] Wassertiefen sind physikalisch vernünftig (keine negativen Tiefen, keine unrealistische Flut)
- [
- [ ] Zu- und Abfluss-Massenbilanz wird geschlossen (Kontrollstrecken)
- [ ] Keine Störschwingungen oder Instabilitäten im Geschwindigkeitsfeld

**Morphodynamik:**
- [
- [ ] Belastungsrichtung richtet sich nach Hauptströmungsrichtung (mit erwarteten Kurvenabweichungen)
- [ ] Bed Evolution Größe ist plausibel (keine 10-m-Spierlöcher am Basisstrom)
- [
- [

**Auslastung (falls aktiviert):**
- [ ] Konzentrationen liegen in physikalisch vernünftigen Bereichen (typischerweise < 10 g/l für Flüsse)
- [ ] Vertikale Verteilung folgt erwartetem Rouse-Profil (für 3D-Simulationen)
- [
- [ ] Keine negativen Konzentrationen
```

Wenn ein Modell schließlich und annähernd körperlich aussagekräftig ist, kann das Modell mit Beobachtungsdaten {ref}`calibrated <bl-calibration>` sein. Der nächste Abschnitt enthält eine Liste von Keywords, die für die Kalibrierung von {term}`Bedload` und/oder {term}`Suspended load`-Simulationen mit Gaia verwendet werden können.


(gaia-calibration)=
## Kalibrierung

```{dropdown} Recall: How to calibrate?
Die Kalibrierung beinhaltet die schrittweise Anpassung von Modelleingangsparametern, um eine möglicherweise beste (statistische) Passform von Modell- und Messdaten zu liefern. Bei der Modellkalibrierung sollte nur ein Parameter zu einem Zeitpunkt um 10 bis 20 % Abweichungen von seinem Standardwert geändert werden. Wenn der Standard z.B. `BETA : 1.3` ist, kann die Kalibrierung auf `BETA : 1.2`, dann `BETA : 1.1` und so weiter testen, um letztlich herauszufinden, welcher Wert für **BETA*** die Modellergebnisse am nächsten an Beobachtungsdaten bringt.

Darüber hinaus vergleicht eine Sensitivitätsanalyse stufenweise Modifikationen mehrerer Parameter (noch: ein zu einem Zeitpunkt) und deren Auswirkungen auf Modellergebnisse. Wenn beispielsweise eine 10 %ige Variation von **BETA** eine 5 %ige Veränderung der globalen Wassertiefe ergibt, während eine 10 %ige Variation eines Reibungskoeffizienten eine 20 %ige Veränderung der globalen Wassertiefe ergibt, kann geschlossen werden, dass die Modellempfindlichkeit gegenüber dem Reibungskoeffizienten höher ist als bei **BETA***. Solche Schlussfolgerungen erfordern jedoch sorgfältige Überlegungen in multiparametrischen, komplexen Modellen von Flussökosystemen.
```

Dieser Abschnitt geht davon aus, dass das Modell bereits hydrodynamisch kalibriert ist (z.B. bezüglich Reibung), wie in der {ref}`steady modeling section <tm2d-calibration>` beschrieben. Gaia kann dann zur Modellierung eines Flut-Hydrographen mit einem {ref}`unsteady (quasi-steady) simulation <chpt-unsteady>` verwendet werden. Die Kalibrierung erfordert, dass Flussbett-Elevationsmessungen von vor und nach der Flut verfügbar sind (d.h. eine ereignisspezifische {term}`Topographic change`Karte).

```{admonition} Calibration data requirements
:class: note

Ideale Kalibrierdaten für morphodynamische Modelle umfassen:
* ** Vorbeugende Digitales Oberflächenmodell (DOM)*: Hochauflösende Badymetrie/Topographie vor der modellierten Veranstaltung
* **Post-event Digitales Oberflächenmodell (DOM)*: Hochauflösende Badymetrie/Topographie nach dem modellierten Ereignis
* **Hydrograph**: Zeitreihe der Entlastung während des Ereignisses
* ** suspendierte Sedimentkonzentrationen*: Gemessene SSC-Zeitreihen an Messstationen (falls verfügbar)
* **Geschiebetransport-Messungen** Sampler- oder Falldaten (selten, aber wertvoll)

Der Unterschied zwischen Vor- und Nachevent DEMs ergibt die **topographische Änderungskarte* (oder DoD - Digitales Oberflächenmodell (DOM) of Difference), die als primäres Kalibrierziel für morphodynamische Modelle dient.
```

(bl-calibration)=
### Belastungskalibrierungsparameter

Für die Kalibrierung der Bettlast in Gaia können folgende Parameterliste berücksichtigt werden:

* **Representative roughness length** $k'_{s}$ (cf. Equation {eq}`eq-cf-skin`) with the keyword **RATIO BETWEEN SKIN FRICTION AND MEAN DIAMETER** $\alpha_{ks}$ (default: $\alpha_{ks}$=`3.`). Note that this keyword is a multiplier of the mean grain diameter $D_{50}$; thus: $k'_{s}= \alpha_{ks} \cdot D_{50}$ (goes into Equation {eq}`eq-cf-skin`):
  * Um diesen Kalibrierparameter zu nutzen, stellen Sie sicher, dass `SKIN FRICTION CORRECTION : 1`.
  * On dune-form sand riverbeds, start with $\alpha_{ks}$=`37.` {cite:p}`mendoza2017`.
  * In alternating bar riverbeds, start with $\alpha_{ks}$=`3.6` {cite:p}`mendoza2017`.
  * Die Erhöhung $\alpha_{ks}$ erhöht die Reibung der Haut und damit die Transportrate.

* Bei Modellen auf Basis der Formel {ref}`Meyer-Peter and Müller <gaia-mpm>` (d.h. unter Verwendung eines {term}`Shields parameter` für incipient sediment motion) kann das Schlüsselwort **CLASSES SHIELDS PARAMETERS** geändert werden:
  * Wenn die Erosion überbewertet wird, erhöhen Sie **CLASSES SHIELDS PARAMETERS**.
  * Wenn die Erosion unterschätzt wird, reduzieren Sie **CLASSES SHIELDS PARAMETERS**.
  * Typischer Bereich: 0,03-0.06 für gleichmäßige Sedimente, bis zu 0,07 für gepanzerte Betten.

* Der **MPM COEFFICIENT** kann angepasst werden (Standard: `8`):
  * Original Meyer-Peter und Müller Wert: `8`
  * Wong-Parker-Korrektur für Planbetten: `3.97` (mit `CLASSES SHIELDS PARAMETERS : 0.0495`)
  * Reduzieren Sie, um die gesamten Bettlast-Transportraten zu verringern.

* Mit der Piste-Korrektur aktiviert und mithilfe der {cite:t}`koch1980`Korrektur-Formel das **BETA** Keyword von Equation {eq}`eq-qb-corr` (Standard ist `BETA : 1.3`):
  * Wenn die Erosion in gekrümmten Kanalabschnitten übervorhergesagt ist, verringern Sie **BETA**.
  * Wird die Erosion in gekrümmten Kanalabschnitten unterschätzt, erhöhen Sie **BETA**.
  * Typische Reichweite: 1.0-2.0.

* Um das Abscheidungs- und Erosionsmuster in Kurven (Riverbends) anzupassen, aktivieren Sie das **SECONDARY CURRENTS* Schlüsselwort und ändern Sie den **SECONDARY CURRENTS ALPHA COEFFICIENT*** Wert (vgl. {ref}`Secondary Currents <gaia-secondary>`):
  * Standard: `1.0` (glänzendes Bett)
  * Für raue Betten: `0.75`
  * Wendelstromstärke und damit laterale Sedimentumverteilung.

* Das **HIDING FACTOR FORMULA*** Keyword (für mehrstufiges Sediment) steuert, wie feinere Partikel von gröberen versteckt werden:
  * `0`: konstanter Versteckfaktor (**default**), der die per-Klasse-Werte mit dem **CLASSES HIDING FACTOR*** Schlüsselwort angegeben werden muss
  * `1`
  * `2`
  * `4`: Karim, Holly & Yang Formel
  * Ändert die relative Beweglichkeit verschiedener Sedimentklassen.

```{admonition} Recommended calibration sequence for bedload
:class: tip

1. **Erste***: Gesamttransportgröße mit **CLASSES SHIELDS PARAMETERS** oder **MPM COEFFICIENT*
2. **Second**: Raumverteilung mit **BETA** und **SECONDARY CURRENTs ALPHA COEFFICIENT* anpassen
3. **Third**: Feinabstimmung mit **RATIO BETWEEN SKIN FRICTION UND MEAN DIAMETER*
4. **Letzte**: Verbergungs-/Expositionseffekte für mehrstufige Modelle mit **HIDING FACTOR FORMULA***

Vergleichen Sie simulierte topographische Veränderung mit gemessener DoD (Digitales Oberflächenmodell (DOM) of Difference) mit statistischen Metriken wie RMSE, Nash-Sutcliffe Effizienz oder Brier Skill Score.
```

### Aufgehängte Lastkalibrierungsparameter

Die folgende Parameterliste kann für die Kalibrierung des hängenden Lasttransports und des Abscheidungsmusters in Gaia berücksichtigt werden:

* **{ref}`CLASSES SETTLING VELOCITIES <gaia-sl-sed>`**:
  - Reduzierung der Transportlänge und Verringerung der Ablagerungsraten
  - Erhöhung der Transportwege und Verbesserung der Ablagerung
  - Setzen Sie auf `-9`, um die automatische Berechnung von Gaia basierend auf der Korngröße zu verwenden

* **{ref}`CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION <gaia-sl-sed>`**:
  - Reduzieren, um das Sediment in der Suspension länger zu halten (Bestimmung nur bei geringeren Scherbelastungen)
  - Erhöhung der Abscheidung bei höheren Scherspannungen
  - Standard von `1000` N/m2 deaktiviert die Abscheideschwelle effektiv

* **LACHTER TEILNEHMER** (Eisenkurs konstant $M$):
  - Erhöhung der Erosionsraten
  - Verringerung der Erosionsraten
  - Typischer Bereich: 1.E-04 bis 1.E-02 kg/(m2·s)

* ** RECHTSGRUNDLAGE DES MUD**:
  - Erhöhung der Erosion (höhere Schwelle)
  - Verringerung der Erosion (untere Schwelle)
  - Varianten mit Sedimentkonsolidierung; typischer Bereich: 0,01-1,0 N/m2

* **COEFFICIENT FÜR DIFFUSION VON SUSPENDED SEDIMENTS** (oder auf Turbulenzmodell angewiesen; default`1.E-6`m2/s):
  - Höhere Werte erhöhen die seitliche Ausbreitung des suspendierten Sediments
  - Niedrigere Werte Konzentrat sediment plums

```{admonition} Recommended calibration sequence for suspended load
:class: tip

1. **Erste***: Passende Sedimentkonzentrationen an Messstationen durch Einstellen von **LAYERS PARTHENIADES CONSTANT** (erosion) und **CLASSES SETTLING VELOCITIES** (deposition)
2. **Second*: Anpassen ** RECHTSSACHE CRITICAL EROSION SHEAR STRESS OF THE MUD**, um zu kontrollieren, wo Erosion initiiert
3. **Third**: Feinabstimmung **CLASSES CRITICAL SHEAR STRESS FÜR MUD DEPOSITION** zur Anpassung von Abscheidungsmustern
4. **Letzte**: Anpassen **COEFFICIENT FÜR DIFFUSION VON SUSPENDED SEDIMENTS*, wenn die Klempneraufweitung falsch erscheint

Vergleichen Sie simulierte SSC-Zeitreihen mit Messungen mit RMSE- oder Nash-Sutcliffe-Effizienz.
```

**What next?**
: The calibrated model will also require validation. The validation requires another set of riverbed elevation measurements from before and after another flood (i.e., an additional event-specific {term}`Topographic change` map). Alas, {term}`Topographic change` maps are expensive and it is rare to have at least three {term}`DEM`s from different points in time for a river section, which would enable the creation of two {term}`Topographic change` maps. For this reason, the calibration dataset is often split in practice. For instance, 2/3 of a {term}`Topographic change` map may be used for model calibration and 1/3 for model validation. However, such splitting makes that the two datasets are not statistically independent and the validation quality figures will be biased.

```{admonition} Model validation approaches
:class: note

Wenn unabhängige Validierungsdatensätze nicht verfügbar sind, beachten Sie:

* **Spatial Split**: Kalibrieren auf stromaufwärts, validieren auf stromabwärts (oder umgekehrt)
* **Temporal Split**: Calibrate auf der ersten Hälfte des Ereignisses, gültig auf der zweiten Hälfte
* **Cross-validation*: k-fache Aufteilung der verfügbaren Daten
* **Process-basierte Validierung*: Überprüfen Sie, ob das Modell bekannte physikalische Verhaltensweisen korrekt wiedergibt (z.B. Punkt-Bar-Bildung in Mäandern, Pool-Riffle-Sequenzen)
* **Sensitivitätsanalyse*: Dokumentmodellantwort auf Parametervariationen, um Unsicherheit zu charakterisieren

Melden Sie sich bei der Veröffentlichung oder Anwendung von Modellergebnissen immer transparent an.
```