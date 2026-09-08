---
description: Beheben Sie häufige TELEMAC-Fehler, einschließlich der Wiederherstellung der abgestürzten Parallelsimulation, der Tools zum Zusammenführen von GRETEL und PARTEL und der Rekonstruktion der SELAFIN-Ergebnisdatei.
---

# Debugging TELEMAC

Seit seiner frühen Entwicklung hat sich TELEMAC zu einem robusten und zuverlässigen Werkzeug für die numerische Modellierung von offenen Oberflächenströmungen entwickelt. Dennoch gibt es ein paar kleine Herausforderungen und diese ständig wachsende Seite bietet einige Antworten.

```{admonition} Keyword-research the TELEMAC docs
:class: tip
Um die Referenz, Implementierung und / oder Bedeutung einer Variablen, Klasse, Skript, Datei oder eines Moduls nachzuschlagen, besuchen Sie die [TELEMAC doxydocs (stale - siehe opentelemac.org)](https://www.opentelemac.org/index.php/modules/18-news-general/85-doxygen-documentation).
```

## Abgestürzte Simulationsdateien wiederherstellen

Wenn ein parallel ausgeführter Telemac (unter Verwendung mehrerer Kerne) abstürzt oder wenn Sie teilweise Ausgabedateien aus jeder Subdomain in eine einzelne Datei rekombinieren müssen, bieten die Postprocessing-Tools von Telemac Optionen zum Zusammenführen (oder "Nähen") der Submesh-Ergebnisse. Es stehen zwei Hauptwerkzeuge zur Verfügung:

1. **GRETEL (das dedizierte Merging-Tool) **
   - GRETEL nimmt die partiellen (Subdomain-) Ergebnisdateien von jedem Kern und führt sie zu einer einzigen SELAFIN / MED-Datei für die gesamte Domain zurück.
   - Dies ist in der Regel der **go-to-Ansatz **, wenn Ihre Simulation teilweise abgestürzt ist, aber Sie immer noch visualisieren oder analysieren möchten, welche Teilergebnisse gespeichert wurden.

2. **PARTEL (im Merge-Modus)**
   - PARTEL wird typischerweise zur Partitionierung von Maschen für parallele Läufe verwendet, hat aber auch eine Merge-Fähigkeit. Einige Versionen oder Workflows verwenden PARTEL sowohl zum Partitionieren als auch zum Zusammenführen.
   - Für die meisten modernen Telemac-Konfigurationen ist **GRETEL** jedoch tendenziell das schlankere oder standardmäßig zusammengeführte Tool.

### Wie man GRETEL benutzt

1. Wenn Sie Ihre Simulation parallel ausgeführt haben und sie abgestürzt ist (oder abgeschlossen ist, aber Sie müssen Subdomains nur manuell kombinieren), suchen Sie die Teilergebnisdateien mit dem Namen:
   ```
   T3DRES00000-00001.slf
   T3DRES00000-00002.slf
   …
   ```
   or, for each subdomain, the corresponding files typically ending in `-0000X.slf`.

2. Sie können sie zusammenführen, indem Sie GRETEL von der Befehlszeile aus ausführen, zum Beispiel:
   ```
   runcode.py gretel -c <your_config> -f <your_config_file> --merge --ncsize <number_of_subdomains>
   ```
   
Passen Sie die Flags und Dateinamen nach Bedarf an. Wenn Sie Telemac3d verwenden:
   
   ```
   runcode.py telemac3d <steering_file> --merge -w <folder_path>
   ```

   Replace `<folder_path>` with the directory that contains the output parts.   
   

Die genaue Syntax kann abhängig von Ihrer Version von Telemac variieren. Einige Installationen haben ein dediziertes Python-Skript oder einen Launcher für GRETEL.

3. Sobald GRETEL fertig ist, gibt es eine **single 3D SELAFIN** (oder MED) Datei mit allen neu zusammengesetzten Subdomains aus. Sie können dann die Verarbeitung der zusammengeführten Datei in Ihrer bevorzugten Nachbearbeitungsumgebung (z. B. Blue Kenue, Paraview, QGIS) visualisieren oder fortsetzen.

### Zusätzliche Hinweise und Tipps

- **Checkpoint/Hotstart**: If you need to restart a run from a particular time step, you can often use the partial subdomain files directly as a hotstart by setting the proper keywords in the steering file (e.g., `RESTART FILE` / `RESTART = YES`). In that case, you do not necessarily need to merge first: Telemac can read the subdomain files in a parallel restart.  
- **Teilschreiben**: Wenn der Lauf mitten im Schreiben abgestürzt ist oder eine Dateikorruption vorliegt, kann GRETEL (oder PARTEL) nicht zusammengeführt werden. Sie müssten normalerweise die beschädigten Dateien entfernen oder beheben oder von einem früheren gültigen Checkpoint neu starten.
- **Batch/Automatische Fusion**: In vielen Telemac-Skripten oder Workflows geschieht das Zusammenführen automatisch am Ende einer Simulation. Wenn Sie die Zusammenführung selbst dann benötigen, wenn die Simulation abgestürzt ist, ist das manuelle Ausführen von GRETEL oder PARTEL im Zusammenführungsmodus normalerweise die beste Lösung.


## Rückverfolgungsfehler

Wenn eine Simulation abstürzt und nicht klar ist, warum das Debuggen mit dem *GNU Project Debugger * [GDB](http://www.gdbtutorial.com)] eine gute Option ist. Dazu installieren Sie zuerst GDB:

```
sudo apt install gdb
```

Starten Sie dann die Steuerungsdatei im Debugging-Modus wie folgt:

```
telemac2d.py -w tmp simulation_file.cas --split
telemac2d.py -w tmp simulation_file.cas -x
cd tmp
gdb ./out_telemac2d
```

In *gdb* tap:

```
(gdb) run
```

Zum Ende *gdb* tap:

```
(gdb) quit
```

Dieser Ansatz funktioniert auch mit * Telemac3d * (und anderen Modulen).

### Fehlermeldung Quickfixes

In diesem Abschnitt werden schnelle Korrekturen für einige häufige Fehlermeldungen aufgeführt.

RANDVERKEHR
Wenn TELEMAC aus scheinbar zufälligen Gründen abstürzt, stellen Sie sicher, dass:

  * Keine Linie in der Lenkungsdatei hat mehr als 72 (aktive Eigenschaften). Beispielsweise:

  `````{tab-set}
  ````{tab-item} Too long line (bad)
  ```fortran
  CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION = 0.011; 0.011; 0.011; 0.011
  ```
  ````
  ````{tab-item} Correct line break (good)
  ```fortran
  CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION = 0.011; 0.011
  ; 0.011; 0.011
  ```
  ````

## Lenkungsdateien (CAS)

* Lieber `:` als `=`
* Legen Sie alle Modelldateien in den gleichen Ordner und verwenden Sie **nur Dateinamen ** ohne die Verzeichnisse der Dateien.



## Mesh-Datei

### Feine hochauflösende Maschen
*Dieser Abschnitt wurde von [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*] mitverfasst.

Um sehr feine Maschen mit einer Gittergröße kleiner als 1,0 m zu erstellen, sollte eine Geometriedatei mit Selafin (`*.slf`) im doppelten Präzisionsformat (SERAFIND) gespeichert werden. Andernfalls können Modellbegrenzungskanten im Rechennetz nicht gut dargestellt werden. {numref}`Figure %s <mesh-precision>` veranschaulicht den Verlust an Grenzgenauigkeit, wenn Einzelpräzision (a) anstelle von Doppelpräzision (b) verwendet wird.

```{figure} ../img/telemac/single-double-precision-mesh.png
:alt: telemac slf selafin single double precision serafind
:name: mesh-precision

Die Verlustgrenzenpräzision in einem Einfachpräzision-Selafin-Netz (a) im Vergleich zu einem Doppelpräzision-Selafin-Netz (b).
```


### Integrierte Mesh Konsistenzprüfung

```{hint}
A 3d simulation may crash when it is used with the parameter `CHECKING THE MESH : YES`. Thus, **in 3d, favorably use `CHECKING THE MESH : NO`**.
```

Um zu überprüfen, ob TELEMAC das Mesh lesen kann, laden Sie die TELEMAC-Umgebung (z.B. `source pysource.openmpi.sh`) und gehen Sie zu dem Verzeichnis, in dem das zu überprüfende Mesh lebt, und führen Sie `mdump` aus, zum Beispiel:

```
cd ~/telemac/studies/test-case/
mdump mesh-to-test.med
```

Until the time of writing this tutorial, `mdump` asks for input variables in *French*, which mean the following:
* *Mode d'affichage de noeuds?* was in <br>English bedeutet: **Node display mode?**
    + Option `1`: Interlaced-Modus
    + Option `2`: Nicht-interlaced Modus
* *Connectivité des éléments?* was in <br>English bedeutet: **Element connectivity?**
    + Option `1`: Nodal
    + Option `2`: Absteigend
* *Il y a 1 maillage(s) de type local dans ce fichier. Lequel voulez-vous lire (0 pour tous|1|2|3|...|n)?* was in <br>English bedeutet: **Es gibt 1 lokales Mesh(es) in dieser Datei. Welches möchten Sie lesen (0 für alle oder |1|2|3|...|n)?**
    + Option `0`: Lesen Sie alle
    + Option `i`: Lesen Sie die Mesh-Nummer `i`

Eine Standard-Antwortkombination von `1` - `1` - `0` führt zu einem Konsolendruck aller Knoten und Verbindungen zwischen den Knoten im Mesh, da TELEMAC die Mesh-Datei lesen kann. Beginnend mit:

```
(**********************************************************)
(* INFORMATIONS GENERALES SUR LE MAILLAGE DE CALCUL N°01: *)
(**********************************************************)

- Nom du maillage : <<Mesh_Hn_1>>
- Dimension du maillage : 2
- Type du maillage : MED_NON_STRUCTURE
- Description associee au maillage :

(**********************************************************************************)
(* MAILLAGE DE CALCUL |Mesh_Hn_1| n°01 A L'ETAPE DE CALCUL (n°dt,n°it)=(-01,-01): *)
(**********************************************************************************)
- Nombre de noeuds : 243
- Nombre de mailles de type MED_SEG2 : 80
- Nombre de mailles de type MED_TRIA3 : 404
- Nombre de familles : 15

[...]
```

**What this output means:** If `mdump` can read the mesh, the mesh file itself is OK and potential calculation errors stem from other files such as the steering file or the boundary conditions. Otherwise, revise the mesh file and resolve any potential issue.

## Grenzen

*Dieser Abschnitt wurde von [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*] mitverfasst.

### Kein Wasser im Modell
Erroneous simulations where **no water is entering or exiting** the domain have most likely improperly defined boundary conditions. For instance, consider the open  boundaries shown in {numref}`Fig. %s <dbg-bc-bk>` with `prescribed Q (4 5 5)` upstream and `prescribed H (5 4 4)` downstream.

```{figure} ../img/telemac/dbg-bc-bk.png
:alt: debugging boundary conditions cli bluekenue
:name: dbg-bc-bk

The definition of open (liquid) boundaries with `prescribed Q (4 5 5)` upstream and `prescribed H (5 4 4)` downstream.
```

Intuitively, you may think that the upstream boundary is number (1) and the downstream boundary is number (2). However, the order of boundary numbering depends on the definition order during the setup of the boundaries (e.g., described in the {ref}`BlueKenue pre-processing tutorial <bk-bc>`). If you do not remember the definition order, it can be read in the boundary (`*.cli`) file at any time. For instance, the boundary file for the above-shown mesh ({numref}`Fig. %s <dbg-bc-bk>`) looks like the representation in {numref}`Fig. %s <dbg-boundaries>` where the **Outlet** is defined **above** the **Inlet**. Therefore, the **downstream (Outlet) open boundary is number (1)** and the **upstream (Inlet) open boundary is number (2)** in this simulation.

```{figure} ../img/telemac/dbg-boundaries.png
:alt: debugging boundary conditions cli bluekenue
:name: dbg-boundaries

Beispielhafte Definition einer stromabwärts (Outlet) und einer stromaufwärts (Inlet) offenen Grenze in einer Grenze. cli-Datei entsprechend {numref}`Fig. %s <dbg-bc-bk>`.
```

Daher müssen diese beiden Grenzen in der Steuerungsdatei (`*.cas`) wie folgt referenziert werden, um eine Flussrate `Q` (z. B. 10 m$^3$/s) an der stromaufwärtigen und eine Tiefe `H` (z. B. 0,75 m) an der stromabwärtigen Grenze festzulegen:

```fortran
PRESCRIBED FLOWRATES : 0.;10
PRESCRIBED DEPTHS : 0.75;0.
```

### Problem mit der Grenznummer (Simulationsstopp)

Dieser Abschnitt führt durch Debugging-Fehlermeldungen wie:

```fortran
DEBIMP_2D: PROBLEM ON BOUNDARY NUMBER       2
        GIVE A VELOCITY PROFILE
        IN THE BOUNDARY CONDITIONS FILE
        OR CHECK THE WATER DEPTHS
        OTHER POSSIBLE CAUSE:
        SUPERCRITICAL ENTRANCE WITH FREE DEPTH
```

To get a better appreciation of the cause of the error (e.g., to figure out if supercritical flow conditions at the entrance are the cause), add the {term}`Froude-Zahl <Froude number>` to the output variables in the steering (`*.cas`) file. To this end, add `F` to the output variable keyword:

```fortran
VARIABLES FOR GRAPHIC PRINTOUTS : U,V,H,S,Q,F
```

Mit einer genaueren der Ursache für den Fehler, versuchen Sie eine der folgenden Optionen:

Supercritical boundaries at the entrance
:	For supercritical flow conditions at the entrance, make sure that a `prescribed Q and H` boundary also gets a discharge and a depth assigned in the steering file. For instance, if the Inlet in Figures {numref}`%s <dbg-bc-bk>` and {numref}`%s <dbg-boundaries>` was `5 5 5` (`prescribed Q and H`) instead of `4 5 5`, the steering file needs to prescribe flowrates and depths. For instance, add a depth of `0.9` for the Inlet as follows:

  ```fortran
  PRESCRIBED FLOWRATES : 0.;10
  PRESCRIBED DEPTHS : 0.75;0.9
  ```

Change the (vertical) velocity profile
: The definition of a `VELOCITY PROFILE` keyword in the steering file is explained in the {ref}`steady2d tutorial <tm2d-bounds>` in this eBook. The addition `VERTICAL` applies to 3d models only (read more in the {ref}`Telemac 3d (SLF) section <tm3d-slf-boundaries>`).

3d models with supercritical boundaries
: Too many vertical layers may result in very thin 3d mesh elements that cause supercritical flows locally. Thus, consider reducing the {ref}`NUMBER OF HORIZONTAL LEVELS <tm3d-slf-vertical>` in the steering file to satisfy the {term}`CFL-Zahl <CFL>` condition.

## Gaia (Morphodynamik)

### VORAUSSETZUNGEN FÜR UNBEKANNTE LÄNDER

TELEMAC-Gaia may interrupt with an error message such as `KEYWORD:` [...] `UNKNOWN BOUNDARY CONDITIONS FILE ...`. This message means that the boundary condition type in the `*.cli` file does not match the boundary conditions defined in the `*.cas` file. For instance, if the tracer (suspended load) boundary column (`9` in the Gaia `*.cli` file for `CBOR`) is set to `5`, try using `EQUILIBRIUM INFLOW CONCENTRATION : YES` or double-check the numbers defined for the **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES** keyword.

Read more about setting up boundary condition files for Gaia in the {ref}`Gaia Basics section <gaia-bc>`. The definition of boundary types in the Gaia steering file are described separately for {ref}`bedload <gaia-bc-bl>` and {ref}`suspended load <gaia-bc-sl>`.

## BlueKenue

*Dieser Abschnitt wurde von [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*] mitverfasst.

BlueKenue kann Fehler auslösen oder beim Arbeiten mit 3D-Meshes nicht korrekt angezeigt werden. Einige der Probleme können mit der neuesten Version von BlueKenue (v3.12.2-alpha zum Zeitpunkt der Bearbeitung dieses Artikels) behoben werden.

**OnFileOpendata(): ERROR: auf Activate()**
: **Ursachen:** Die Fehlermeldung tritt typischerweise bei parallelisierten Modellläufen auf, wenn Telemac3d / PARTEL das Mesh am Ende der Simulation nicht korrekt zusammengeführt hat.

**Lösung:** Erzwingen Sie TELEMAC, den temporären Simulationsordner nicht zu löschen (ein Ordner, der standardmäßig nur während der Ausführung einer Simulation im Simulationsverzeichnis sichtbar ist). Das Führen des temporären Berechnungsverzeichnisses wird durch Hinzufügen eines `-t`-Flags am Ende des Simulationsablaufbefehls erreicht. Tippen Sie beispielsweise auf Folgendes, um den Simulationsordner für eine Telemac3d-Simulation beizubehalten (lesen Sie mehr in Anhang A des [Telemac3d-Handbuchs](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/telemac3d/user/telemac3d_user_9.0.pdf)]):

  ```
  telemac3d.py steering-file.cas -t
  ```
  
  The temporary folder contains T3DRES (mesh partition) files that can be merged and then opened in BlueKenue. To merge the T3DRES files run the following command (make sure the TELEMAC environment is still activated with `source pysource.YOUR-ENV.sh`):
  
  ```
  runcode.py --merge -w temp_directory/ telemac3d file.cas
  ```
  
Um Hilfe beim Ausführen dieses Befehls zu erhalten, lesen Sie [dieses TELEMAC Forum entry](http://opentelemac.co.uk/index.php/assistance/forum5/21-telemac-3d/7221-continue-computation-from-temporary-file)].
  
Für ** Updates zu dieser Nachricht ** folgen Sie dem [BlueKenue-Thread im TELEMAC Forum](http://www.openmascaret.org/index.php/assistance/forum5/blue-kenue/13278-issue-with-geometry-file?start=10#38837) für die Fehlerbehebung bei Updates zu diesem Fehler].

## PostTelemac Plugin

Some versions of QGIS may throw a Python error (yellow frame in the top region of the map viewport) and a click on **Stack** reveals an error message. At the bottom of the error message, it might be written `import error: no module named gdal`. The error probably stems from an import statement in one of the PostTelemac plugin's Python scripts. To troubleshoot the gdal import error, find the Python script that is raising the error message. For instance, the script `posttelemac_hdf_parser.py` may cause the error through its `import gdal` statement. To troubleshoot, open it, and on Windows, you may find it in the following directory:

```
C:\Users\USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\PostTelemac\meshlayerparsers\posttelemac_hdf_parser.py
```

In der geöffneten Datei:

* Öffnen Sie die betreffende Datei, die hier ist: **`posttelemac_hdf_parser.py`**
* Find the `import gdal` statement and **replace it with `from osgeo import gdal` (i.e.,  <s>`import gdal`</s> and write `from osgeo import gdal`)
* Speichern und schließen Sie die Python-Datei.

Versuchen Sie erneut, das PostTelemac-Plugin zu starten. Es sollte jetzt ohne Probleme laufen.


## SALOMEHYDRO

(salome-dbg)=
### SALOME-HYDRO startet nicht (**Kernel/Session**)

If an error message is raised by `Kernel/Session` in the `Naming Service`, it will typically ends up in 
```
$ [Errno 3] No such process ... 
   RuntimeError: Process NUMBER for Kernel/Session not found
```

Es gibt mehrere mögliche Ursprünge solcher Fehler, die teilweise in potenziell fest codierten Bibliotheksversionen des Installers verwurzelt sind. Die folgenden Optionen zur Fehlerbehebung existieren, aber diese erfordern eine sorgfältige Prüfung, da sie das Betriebssystem beschädigen könnten:

* Erstellen Sie manuell Kopien neuerer Bibliotheken mit Namen älterer Versionen. Zum Beispiel:
  + In the 4th line after running `./salome`, `Kernel/Session` may prompt

```
$ error while loading [...] libSOMETHING.so.20 cannot open [...] No such file or directory
```

  + Identify the version installed with `whereis libSOMETHING.so.20` (replace `libSOMETHING.so.20` with the missing library); for example, this command may output

```
$ /usr/lib/x86_64-linux-gnu/libSOMETHING.so.40
```

  + Erstellen Sie eine Kopie der neueren Bibliothek und benennen Sie die Kopie nach Bedarf von SALOME um; z. B. tippen

```
sudo cp /usr/lib/x86_64-linux-gnu/libSOMETHING.so.40 usr/lib/x86_64-linux-gnu/libSOMETHING.so.20
```

  + Höchstwahrscheinlich müssen die folgenden Dateien kopiert werden:

```
sudo cp /usr/lib/x86_64-linux-gnu/libmpi.so.40 /usr/lib/x86_64-linux-gnu/libmpi.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libicui18n.so.63 /usr/lib/x86_64-linux-gnu/libicui18n.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicuuc.so.63 /usr/lib/x86_64-linux-gnu/libicuuc.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libicudata.so.63 /usr/lib/x86_64-linux-gnu/libicudata.so.57
sudo cp /usr/lib/x86_64-linux-gnu/libnetcdf.so.13 /usr/lib/x86_64-linux-gnu/libnetcdf.so.11
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempif08.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_java.so.40 /usr/lib/x86_64-linux-gnu/libmpi_java.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.40 /usr/lib/x86_64-linux-gnu/libmpi_cxx.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.40 /usr/lib/x86_64-linux-gnu/libmpi_mpifh.so.20
sudo cp /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.40 /usr/lib/x86_64-linux-gnu/libmpi_usempi_ignore_tkr.so.20
```

* Überschreiben Sie die interne Version von *Qt* von SALOME-HYDRO:
  + Kopie

```
/usr/lib/x86_64-linux-gnu/libQtCore.so.5
```
  + Paste in (confirm replacing `libQtCore.so.5`)

```
/Salome-V2_2/prerequisites/Qt-591/lib/
``` 


(qt-dbg)=
### GUI/Qt5-Unterstützung (Kompatibilität der GTK-Version)

With the newer versions of the *Qt platform* any menu entry in *SALOME-HYDRO* will not show up. To fix this issue, install and configure `qt5ct` styles:


```
sudo apt install qt5-style-plugins libnlopt0 qt5ct
```

Dann:

* Konfigurieren Sie `qt5ct` ( tippen Sie einfach auf `qt5ct` in *Terminal*)
  + Gehen Sie zum Tab *Erscheinung *
  + *Style* auf `gtk2` und *Standarddialoge* auf `GTK2`
  + Klicken Sie auf *Apply* und *OK*
* Open the file `~/.profile` (e.g. use the file browser, go to the `Home` folder and press `CTRL` + `H` to toggle viewing hidden files) and add at the very bottom of the file:

```
export QT_STYLE_OVERRIDE=gtk2
export QT_QPA_PLATFORMTHEME=qt5ct
```

* Save and close `.profile` and reboot (or just re-login).

```{note}
Wenn eine Datei mit dem Namen `~/.bash_profile` (oder `~/.bash_login`) existiert, sollten die oben genannten Zeilen an `~/.bash_profile`/`~/.bash_login` geschrieben werden, da in diesem Fall `.profile` beim Einloggen nicht gelesen wird.
```

Erfahren Sie mehr über *Qt* unter [archlinux.org](https://bbs.archlinux.org/viewtopic.php?id=214147&p=3) und im [arch wiki](https://wiki.archlinux.org/index.php/Uniform_look_for_Qt_and_GTK_applications#QGtkStyle)].
