---
description: Installation von OpenCFD OpenFOAM v2406, Olsen Sedimentlöser, BAW-Ausgangsgrenzbedingungen, ParaView und VisIt auf Debian, Ubuntu und Windows über WSL2.
---

(openfoam-install)=
# OpenFOAM (Installation)

Dieser Abschnitt erklärt die Installation von [OpenCFD OpenFOAM v2406](https://dl.openfoam.com/source/v2406/) mit einem plattformübergreifenden Auto-Installer-Skript, das das Programm neben sediment-transport und ausgangsgebundenen Komponenten sowie ParaView und VisIt-DAV für die Nachbearbeitung zusammenstellt.

| Komponente | Funktion |
: :
| `sediDriftFoam` | Olsen et al. (2023) fest-mesh suspendiert-sedimentlöser. |
| `sediDriftFoam2` | Olsen (2025) Sedimentlöser mit Betthöhe und freier Oberflächeneinstellung. |
| `sediDriftFoam2Rating` | Neue experimentelle Erweiterung von `sediDriftFoam2` für eine Phase-Discharge-Beziehung. |
| BAW `HydBCsForOF` | Boundary-Bedingungs-Bibliothek, einschließlich einer Bühnen-Entladung für Wasser-Luft-Simulationen mit `interFoam`. |

Die Original-Löser werden von [Nils Reidar Olsen](https://www.pvv.ntnu.no/~nilsol/sediDriftFoam2/) dokumentiert; die native Ausgangsgrenzbedingung wird in [BAW's repository](https://github.com/baw-de/HydBCsForOF)] dokumentiert.

```{admonition} OpenFOAM Distribution
:class: important

Diese Anweisungen zielen auf die OpenCFD Release v2406, nicht OpenFOAM Foundation Releases (z.B. v9 oder v13). Die standardmäßige Installation kompiliert die Juni 2024-Quellenfreigabe und die passenden ThirdParty-Quellen in einem separaten Benutzerverzeichnis. Vorhandene OpenFOAM-Installationen und Shell-Startdateien werden beibehalten. Kombinieren Sie keine Bibliotheken, die gegen verschiedene OpenFOAM Distributionen oder Versionen kompiliert sind.
```

## Anforderungen und Installationsdateien

Der Installer unterstützt x86-64 Systeme mit Debian 12, Ubuntu 22.04 oder Ubuntu 24.04. Derivate müssen eine entsprechende unterstützte Basisverteilung verwenden. Windows baut im Windows Subsystem für Linux 2 (WSL2), nicht als native Windows-Executables.

Die Installation erfordert eine gute und stabile Internetverbindung, Python 3.10 oder später, und ein Benutzerkonto mit `sudo`zugriff für Systempakete. Erlauben Sie etwa 20 GiB freien Speicherplatz und mindestens 8 GiB RAM; die Source-Build-Check erfordert mindestens 15 GiB frei. Der Abschluss kann mehrere Stunden dauern. Die grafische Nachbearbeitung erfordert einen Linux-Desktop oder WSLg.

Der Installateur wird im [`OpenFOAM-installer`subfolder](https://github.com/Ecohydraulics/numerical-software-installers/tree/main/OpenFOAM-installer) des `Ecohydraulics/numerical-software-installers` Repository aufrechterhalten. Mit Git installiert, Klonen Sie das Repository und geben Sie diesen Unterordner ein:

```bash
git clone --depth 1 https://github.com/Ecohydraulics/numerical-software-installers.git
cd numerical-software-installers/OpenFOAM-installer
```

Diese Befehle funktionieren auch in PowerShell. Geben Sie für einen vorhandenen Checkout das `OpenFOAM-installer`-Verzeichnis ein, anstatt erneut zu klonen. Alternativ verwenden Sie **Code → Download ZIP** auf der [Repository-Seite](https://github.com/Ecohydraulics/numerical-software-installers), extrahieren Sie das Archiv und geben Sie `numerical-software-installers-main/OpenFOAM-installer` ein.

Erhalten Sie den kompletten Installer-Unterordner; `install.py` allein ist unzureichend. Das Repository enthält Installer-Dateien, nicht die Software-Distributionen; diese werden während der Installation heruntergeladen. Führen Sie die folgenden Befehle von `OpenFOAM-installer` aus, die `install.py` und `install.ps1` enthält.

(openfoam-debian)=
## Debian und Ubuntu

### Kompilieren und installieren

Wenn Python abwesend ist, installieren Sie es zuerst:

```bash
sudo apt update
sudo apt install python3
```

Vorschau der Installation, dann kompilieren und installieren:

```bash
python3 install.py --dry-run
python3 install.py --install-system-packages --examples --smoke-test
```

Führen Sie den Installer als normaler Benutzer aus, ohne ihn mit `sudo` vorzufixieren. Die `--install-system-packages`-Option erlaubt die Installation von Build-Abhängigkeiten, grafischen Laufzeitabhängigkeiten und ParaView über `sudo apt-get`. VisIt-DAV 3.5.0 wird als Prüfsummenverifizierter Binär auf das Betriebssystem abgestimmt heruntergeladen. ParaView folgt der von den konfigurierten Distributions-Repositories verfügbaren Version.

```{admonition} APT Commands
:class: note

Der Installer verwendet `apt-get`, die rückwärtskompatible Schnittstelle für Skripte empfohlen. Die oben genannten `apt`-Befehle sind für die interaktive Nutzung bestimmt. Keine Schnittstelle ist veraltet; siehe [Debian APT manual](https://manpages.debian.org/bookworm/apt/apt.8.en.html#SCRIPT_USAGE_AND_DIFFERENCES_FROM_OTHER_APT_TOOLS).
```

Die `--examples`-Option lädt Nils Reidar Olsens grober Fall A herunter. Die `--smoke-test`-Option läuft eine kurze serielle `interFoam`-Fall, um die BAW-Bibliothek zu überprüfen. Ein Trockenlauf druckt den Plan ohne Prüfungsvoraussetzungen oder Erstellungscode.

```{admonition} Distribution Derivatives
:class: note

Wenn ein Derivate nicht erkannt wird, überprüfen Sie seine Debian- oder Ubuntu-Basis, bevor Sie `--visit-platform debian12`, `--visit-platform ubuntu22` oder `--visit-platform ubuntu24` auswählen. Das Override wählt die VisIt binär aus; es stellt keine Kompatibilität mit einem nicht unterstützten Betriebssystem fest.
```

### Wiederverwenden einer bestehenden OpenCFD v2406 Installation

Anstatt den OpenFOAM-Kern zu kompilieren, geben Sie die bestehende v2406 Aktivierungsdatei an. Verwenden Sie für die Debian-Paketinstallation unter `/usr/lib/openfoam/openfoam2406`:

```bash
python3 install.py --install-system-packages \
  --reuse-openfoam /usr/lib/openfoam/openfoam2406/etc/bashrc \
  --examples --smoke-test
```

Dies ist eine Alternative zum vorhergehenden Quell-build-Befehl. Die Sedimentlöser und die BAW-Bibliothek werden noch in das neue Benutzerverzeichnis zusammengestellt. Die bestehende Installation muss Entwicklungs-Header, `wmake`, und einen Arbeitskompilator umfassen. Seine API muss 2406 sein; ihre Patch-Ebene kann von der Standard-Source-Version abweichen.

## Windows durch WSL2

In einem Administrator PowerShell installieren Sie Ubuntu 24.04 für WSL:

```powershell
wsl --install -d Ubuntu-24.04
```

Starten Sie Windows, wenn gewünscht. Starten Sie Ubuntu einmal und erstellen Sie ein normales Linux-Benutzerkonto. Bestätigen Sie, dass die Distribution WSL2 verwendet:

```powershell
wsl --list --verbose
```

Wenn seine Version 1 ist, führen Sie `wsl --set-version Ubuntu-24.04 2`. WSLg unterstützt grafische Anwendungen unter Windows 11 und Windows 10 bauen 19044 oder später; siehe die [Microsoft Installation Requirements](https://learn.microsoft.com/windows/wsl/tutorials/gui-apps).

Wählen Sie aus dem `OpenFOAM-installer`-Verzeichnis des Projektarchivs ein normales PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -InstallSystemPackages -Examples -SmokeTest
```

Der Launcher ruft den gleichen Python-Installer in WSL2 an. Die Installer-Dateien können auf dem Windows-Dateisystem bleiben, aber Kompilieren und Fälle sollten auf dem Linux-Dateisystem, nicht unter `/mnt/c`. ParaView und VisIt laufen als Linux-Anwendungen durch WSLg angezeigt.

Für eine initialisierte WSL-Distribution namens `Debian`, die Debian 12, add `-Distro Debian`. Überprüfen Sie seine Veröffentlichung vor der Installation; eine neu heruntergeladene Debian-Distribution muss nicht Debian 12 sein. Um OpenCFD v2406 wiederzuverwenden, fügen Sie `-ReuseOpenfoam`, gefolgt von seinem Linux`etc/bashrc`pfad.

## Installationsverzeichnis und Überprüfung

Das Standard-Installationsverzeichnis ist `~/.local/openfoam-sediment-v2406` im Heimverzeichnis des Linux-Benutzers. Geben Sie einen anderen dedizierten Linux-Pfad mit `--prefix /home/USER/path` oder Windows `-Prefix /home/USER/path` an; der Pfad darf keinen Whitespace enthalten. Beschränken Sie die Compilation Concurrency mit `--jobs 4` oder `-Jobs 4`, falls erforderlich. Die Standardeinstellung ist nicht mehr als acht Compilation-Prozesse, reduziert nach System RAM.

Geben Sie in einem Linux- oder WSL-Terminal die installierte Umgebung ein:

```bash
source ~/.local/openfoam-sediment-v2406/activate.sh
```

Dieser Befehl öffnet eine neue, isolierte interaktive Shell. Es ändert nicht `.bashrc` oder fusioniert eine frühere OpenFOAM-Umgebung. Es werden nur die OpenFOAM-Präferenzen auf Projektebene geladen; bestehende Benutzer/Gruppeneinstellungen sind ausgeschlossen. Geben Sie `exit` ein, um zur vorherigen Shell zurückzukehren. Für ein benutzerdefiniertes Installationsverzeichnis verwenden Sie stattdessen die `activate.sh`.

Überprüfen Sie die Installation in dieser neuen Shell:

```bash
foamEtcFile -show-api
foamEtcFile -show-patch
printf '%s\n' "$WM_PROJECT_DIR" "$WM_OPTIONS"
command -v sediDriftFoam sediDriftFoam2 sediDriftFoam2Rating
sediDriftFoam -help
sediDriftFoam2 -help
sediDriftFoam2Rating -help
```

The API output must be `2406`. Solver help must load without missing-library errors. The installation directory contains compilation logs and `environment-probe.log` in `logs/`, build details in `build-environment.txt`, and source and installation records in `receipt.json`. The BAW runtime-test output is stored in `runs/baw-smoke/`.

```{admonition} Scope of Verification
:class: warning

Die erfolgreiche Zusammenstellung und der BAW-Laufzeittest stellen weder die Gültigkeit einer Sedimentsimulation noch die Genauigkeit der experimentellen Ratingkurvenerweiterung fest. Der Installateur führt Olsens Fall A nicht aus. Vor der wissenschaftlichen Nutzung überprüfen Sie die Netzqualität, Erhaltung, hydraulische Randbedingungen und Übereinstimmung mit geeigneten Referenzergebnissen. Halten Sie die Build-Daten mit den Simulationseingängen fest.
```

Wenn die Installation ausfällt, inspizieren Sie `logs/` vor dem Neulauf. Interrupted Builds speichern Downloads und Protokolle. Entfernen Sie keine bestehende OpenFOAM-Installation, um einen Versionskonflikt zu lösen. Wählen Sie beim Ändern von Quellpins, Installer-Code oder der Compiler-Umgebung ein neues Installationsverzeichnis statt alte und neue Binaries zu mischen.

```{admonition} Archive Verification
:class: warning

Ein Schecksalber zeigt an, dass die empfangenen Bytes nicht mit dem gepinnten Archiv übereinstimmen; es stellt selbst nicht fest, dass die Freigabe geändert wurde. Der Downloader lehnt Teil- und HTML-Antworte ab und meldet die erwarteten und empfangenen SHA256-Werte, Byte Count, Content Type und Mirror-Pfad. Halten Sie die vollständige Fehlerausgabe bei Ausfall der Überprüfung fest. Ändern Sie die Prüfsumme nicht oder deaktivieren Sie die Überprüfung. Rejected temporäre Downloads werden entfernt; verifizierte Archive werden gespeichert.
```

Wenn das Installationsverzeichnis oder sein Protokoll unerwartet fehlt, finden Sie das Verzeichnis vor dem Wiederaufbau. Ein Baum, der im Desktop-Trash gefunden wird, muss auf seinen aufgezeichneten ursprünglichen Pfad wiederhergestellt werden, ohne aktiv zu bauen und kein bestehendes Ziel überschrieben. Das Finden des Baumes in Müll stellt nicht fest, wann oder warum es bewegt. Die mitgelieferten Rückgewinnungsanweisungen beschreiben die Log-Inspektion und Restaurierung; nicht innerhalb von Müll kompilieren.

````{admonition} Recovery from a Failed Installation
:class: note

Frühere Installateure lehnten den gültigen Linux-Dateinamen `jouleHeatingSource:V` ab oder scheiterten während der Umweltbelastung mit `/bin/bash: cannot execute binary file` oder `pop_var_context`. Der korrigierte Loader isoliert Befehlsargumente und suspendiert strenge Shell-Modi während der OpenFOAM Initialisierung, überprüft dann das ausgewählte Projekt, API und ABI vor der Compilation. Reservieren Sie das gescheiterte Verzeichnis und wählen Sie ein neues Installations-Prefix; nicht umgangen sein Eigentums-Marker. Retry ohne vorherige Cache:

```bash
python3 install.py --install-system-packages \
  --prefix "$HOME/.local/openfoam-sediment-v2406-initfix" \
  --examples --smoke-test
```

Der Installer lädt und überprüft Archive im neuen Präfix. Cache reuse ist optional: Verwenden Sie `--source-cache` nur mit einem verifizierten vorhandenen Verzeichnis. Ein `Archive cache directory not found`-Fehler vor Änderungen des Zielvorgabe- oder Systempakets; überlassen Sie diese Option und retry mit dem gleichen Präfix. Verwenden Sie unter Windows `-Prefix` mit einem Linux-Pfad. Nach Erfolg aktivieren Sie das neue Präfix `activate.sh`. Eine Benutzer-Installation zu verschieben, ändert sich das APT-Paket nicht. Die [Recovery-Anweisungen](https://github.com/Ecohydraulics/numerical-software-installers/blob/main/OpenFOAM-installer/docs/RECOVERY.md) beschreiben erstattungsfähige Rollback- und Pakettransaktionsüberprüfung.
````

## Sediment-Fälle und -ableitungen

Mit `--examples` werden die Olsen-Eingangsdateien unter dem Installationsverzeichnis unter `cases/olsen-upstream/cylinder9_case_A/` gespeichert. Arbeiten Sie an einer schreibbaren Kopie. Inspizieren Sie das Mesh, bevor Sie den ausgewählten Sole ausführen:

```bash
cd /path/to/case-copy
checkMesh -constant -allTopology -allGeometry
```

Lösen Sie Netzfehler vor der Simulation auf. Für den mitgelieferten Fall A, rufen Sie `sediDriftFoam2` explizit aus dem Fallverzeichnis an; die veröffentlichte `controlDict` darf noch `simpleFoam` heißen. Der Festmasch `sediDriftFoam` erfordert einen separat vorbereiteten kompatiblen Fall, da seine Sedimentdiktionseinträge unterschiedlich sind. Führen Sie die Olsen-Löser seriell aus. Die Gleitbettnetz- und Ausgangsalgorithmen sind für die MPI-Zersetzung nicht geeignet. Sowohl `sediDriftFoam2` als auch `sediDriftFoam2Rating` overwrite `scour.txt` beim Start; archivieren Sie es vor dem Neustart.

### BAW-Ausgang für interFoam

Der Installer bereitet `cases/baw-interFoam/` vor und kompiliert die freigegebene Bibliothek `lib_BAW_public_BCs_v2412_20260813.so` gegen die ausgewählte v2406 Installation. Der Text `v2412` ist Teil des vorgeschalteten Dateinamens, nicht der OpenFOAM-Version von build. Diese Bibliothek wird vom Fall über den `libs`-Eintrag in `system/controlDict` geladen; sie erfordert keine Recompiling `interFoam`.

Für eine ortsspezifische Bewertungskurve konfigurieren Sie die gepaarten `waterLevel_alpha_prgh` Auslasseinträge in `p_rgh` und `alpha.water` unter Verwendung des in [BAW's document](https://github.com/baw-de/HydBCsForOF)] beschriebenen `ratingCurveTable`-Modus. Verwenden Sie den vorbereiteten Fall als Konfigurationsbeispiel, nicht als kalibrierte hydraulische Daten.

### Experimentalauslass für Olsens Wanderbettlöser

Geben Sie in einer Einweg-Fallkopie die mitgelieferte `examples/ratingCurveProperties`-Datei in `constant/ratingCurveProperties`. Ersetzen Sie den illustrativen Tisch mit ortsspezifischem Austritt in m3/s und Wasser-Oberflächen-Höhe in m, ausgedrückt im vertikalen Datum des Netzes. Entladewerte müssen streng ansteigen, und Erhebungen dürfen nicht abnehmen. Setzen Sie `outletPatch` an den eigentlichen Ausgang, überprüfen Sie die Tiefen- und Höhengrenzen und ändern Sie `enabled false` an `enabled true`. Führen Sie `sediDriftFoam2Rating` explizit aus. Ohne diese Konfiguration ist die Erweiterung inaktiv.

```{admonition} Distinct Boundary-Condition Formulations
:class: warning

BAWs nativer Zustand nutzt die Wasser-Luftfelder `alpha.water` und hydrostatisch reduzierten Druck `p_rgh` in Pa. Es kann nicht direkt dem Olsen einphasigen kinematischen Druck `p` in m2/s2 zugewiesen werden. Die separate Rating-Erweiterung passt die geometrische freie Oberfläche in einer seriellen, quasi-steady Berechnung; es ist keine validierte transiente oder konservative willkürliche Lagrangian-Eulerian-Formulierung. Es hält die Olsen-Hexedral, das ist vertikal geordnet Netz Einschränkungen. Der Festmasch `sediDriftFoam` hat keine bewegliche freie Oberfläche.
```

Ergänzen Sie die Tests in der gelieferten [Rating-Curve Validierungsanweisungen](https://github.com/Ecohydraulics/numerical-software-installers/blob/main/OpenFOAM-installer/docs/RATING_CURVE.md), bevor Sie die Erweiterung für Forschung oder Design verwenden.

## Utilities (Vor- und Nachprozessoren)

### In den Warenkorb

Aktivieren Sie die installierte Umgebung, öffnen Sie dann den Simulationsfall mit dem integrierten OpenFOAM-Reader von ParaView:

```bash
cd /path/to/case-copy
touch case.foam
paraview case.foam
```

Wählen Sie `internalMesh` und die entsprechenden Grenzfelder aus, einschließlich `bedWall` und `freeSurface`, wo vorhanden. Aktivieren Sie `Conc`, `U` und `p`, dann wählen Sie **Apply**. Wählen Sie das angezeigte Feld und verwenden Sie die Animationssteuerungen, um die Zeitreihe zu überprüfen. Bei BAW-Wasser-Luftfällen inspizieren Sie `alpha.water` und `p_rgh`. Es ist kein OpenFOAM-verknüpftes ParaView-Reader-Plugin erforderlich; siehe das [OpenFOAM-Reader-Dokumentation](https://www.paraview.org/paraview-docs/v5.12.0/python/paraview.simple.OpenFOAMReader.html).

### VisIt-DAV

Exportieren Sie den Fall in das Vermächtnis VTK und erzeugen Sie Zeitreihen manifestiert sich in der aktivierten Shell:

```bash
python3 ~/.local/openfoam-sediment-v2406/postprocess.py /path/to/case-copy
visit
```

Für ein benutzerdefiniertes Installationsverzeichnis, justieren Sie den Skriptpfad. In VisIt öffnen Sie eine der gedruckten `.visit`-Dateien, fügen Sie ein **Pseudocolor***-Plot von `Conc` oder einem anderen verfügbaren Skalar hinzu, wählen Sie **Draw*** und verwenden Sie die Animationssteuerungen. Offenes Volumen, Bett und freier Oberfläche manifestiert sich separat. Der Exporteur behält zeitabhängige Mesh-Koordinaten und nimmt OpenFOAM-Zeitwerte aus Metadaten auf, anstatt die Zeit von Dateinamen zu vernachlässigen; siehe die [VisIt-Dateiserien-Dokumentation](https://visit-sphinx-github-user-manual.readthedocs.io/en/v3.5.0/using_visit/WorkingWithFiles/Supported_File_Types.html#creating-visit-files).

Halten Sie alle exportierten Zeitschritt-Dateien. OpenFOAM-Zeitwerte müssen nicht gleich der beschleunigten morphodynamischen Zeit sein, die von Olsens Solvater aufgezeichnet wurde. Konstruieren Sie parallel `interFoam` Felder und Maschen vor dem seriellen Export. Um Manifeste nach zusätzlichen Zeitschritten zu regenerieren, bewegen Sie früher `.visit` Dateien beiseite; unterschiedliche bestehende Manifeste werden nicht überschrieben.

```{admonition} Remote or Headless Computers
:class: note

Auf einem Server ohne Grafik-Desktop übertragen Sie den Fall oder seinen VTK-Export in eine Visualisierungs-Workstation. Die Optionen `--skip-visualization` und Windows`-SkipVisualization` verweisen auf beide Zuschauer, wenn eine Build-only-Installation erforderlich ist. Verwenden Sie die Installateure `paraview` und `visit` Launcher, um Konflikte zwischen OpenFOAM-Bibliotheken und Viewer-Bibliotheken zu vermeiden.
```

### SALOME

SALOME wird von diesem Skript nicht installiert. Die Installation ist in den TELEMAC-Anweisungen beschrieben: {ref}`salome-install`.

(freecad-install)=
### FreeCAD

FreeCAD wird nicht von diesem Skript installiert. Windows-, Linux- und macOS-Pakete und Installationsanweisungen sind von der [FreeCAD project](https://www.freecad.org/).
