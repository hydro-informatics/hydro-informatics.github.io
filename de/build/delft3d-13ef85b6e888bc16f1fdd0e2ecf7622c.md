---
title: Native Compilation von Delft3D-FLOW auf Ubuntu und Linux Mint
subtitle: "A Jupyter Book Usage Note for `install-delft3d-flow-native.sh`"
author: "Prepared for hydraulic-engineering computational workflows"
date: "2026-07-02"
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: "0.13"
    jupytext_version: "1.16"
kernelspec:
  display_name: Bash
  language: bash
  name: bash
---

# Delft3D-FLOW

This section describes a native installation procedure for compiling the Delft3D 4 hydrodynamic kernel on Ubuntu- and Linux Mint-based systems without using Docker. The procedure is implemented in the shell script `install-delft3d-flow-native.sh`. The script clones the Deltares Delft3D source repository, installs a local Python/Conan build environment, installs and configures Intel oneAPI compilers, initializes the open-source Conan dependency workflow, builds the Delft3D 4 suite or the `flow2d3d` target, copies the resulting installation tree to a user-defined prefix, and runs a smoke test with the standard Delft3D 4 example. The procedure should be regarded as an experimental host build because the documented Linux build procedure for Delft3D is container-based. The intended use is reproducible local experimentation, code inspection, and command-line execution of Delft3D-FLOW test cases on non-containerized engineering workstations.

```{warning}
Dieses Dokument beschreibt einen nativen Build-Versuch. Es ersetzt nicht die offizielle Linux-Build-Anleitung von Deltares. Deltares dokumentiert die Linux-Compilation hauptsächlich über containerisierte Umgebungen, während dieses Skript versucht, die erforderliche Toolchain direkt auf einem Ubuntu- oder Linux Mint-basierten Host zu reproduzieren. Überprüfen Sie das Skript, bevor Sie es ausführen: Es fügt das Intel oneAPI APT-Repository hinzu, installiert Systempakete mit `sudo`, lädt und kompiliert Quellcode von Drittanbietern und schreibt Dateien unter `$HOME`. Verwenden Sie es auf eigene Gefahr und führen Sie es nicht auf Produktions-, geteilten oder institutionellen Systemen ohne Autorisierung und Backups aus.
```

## Machen Sie sich bereit

The Delft3D repository contains source code for both Delft3D 4 and Delft3D FM. Delft3D-FLOW is part of the Delft3D 4 suite, for which the relevant build configuration is `d3d4-suite`. Within that suite, the principal Delft3D-FLOW binaries are `d_hydro` and `flow2d3d`. The build system also exposes `flow2d3d` as an individual configuration; however, the suite-level configuration is the more conservative target for a first installation because it preserves the expected Delft3D 4 runtime context.

Das Skript ist für folgende Betriebsbedingungen vorgesehen:

- Der Benutzer benötigt die Befehlszeile Delft3D-FLOW-Ausführung unter Linux;
- Docker oder eine andere Containerlaufzeit ist unerwünscht;
- Lokale Kompilierungszeit (etwa ein bis mehrere Stunden) und Festplattennutzung (etwa 25 GB für oneAPI, Quellen und Build Trees) sind akzeptabel;
- Der Host ist ein Ubuntu- oder Linux Mint-abgeleitetes System mit `apt`;
- Intel oneAPI compilers can be installed under `/opt/intel/oneapi`;
- der Benutzer akzeptiert, dass das Verfahren außerhalb des von Deltares beschriebenen Haupttest-Linux-Pfads liegt.

Die Prozedur ist nicht dazu gedacht, die grafische Benutzeroberfläche von Windows Delft3D zu installieren oder auszuführen. Es installiert nur Befehlszeilenkernel und Laufzeitdateien.

To continue, [download the installer script `install-delft3d-flow-native.sh`](https://raw.githubusercontent.com/Ecohydraulics/numerical-software-installers/main/delft3d-installer/install-delft3d-flow-native.sh).

## Nachweis des Verfahrens

The script follows the repository-level build sequence used by Deltares' own helper tools. Third-party dependencies are managed with Conan 2, while `run_conan.py` performs one-time Conan configuration and `build.py` drives dependency installation, CMake configuration, compilation, and installation. For external users without access to the Deltares Nexus package server, the relevant initialization mode is:

```bash
python run_conan.py initialize external
```

Der entsprechende First-Time Build kompiliert alle Abhängigkeiten Dritter lokal:

```bash
python build.py --config d3d4-suite --build --build-type Release --build-dependencies
```

Das native Skript automatisiert diese Vorgänge und fügt die Vorbereitungsschritte auf Host-Ebene hinzu, die normalerweise vom Deltares-Build-Container bereitgestellt werden:

- Es installiert die Intel oneAPI-Toolchain an die vom Deltares-Container und Conan-Profil verwendeten Versionen: C / C ++ und Fortran-Compiler 2024.2, Intel MPI 2021.13 und MKL 2024.2. Wenn diese angehefteten Pakete aus dem Intel-Repository verschwinden, greift das Skript auf die neuesten Versionen zurück und patcht die Conan-Konfiguration, um die erkannte Compiler-Version zu akzeptieren.
- It creates a Python virtual environment inside the source tree with `conan ~= 2.29` and a current CMake, because the Delft3D build requires CMake 3.30 or newer, which Ubuntu 24.04 and Linux Mint 22 do not ship.
- Es exportiert die Compiler-Umgebung, die im Deltares-Container verwendet wird (`CC=mpiicx`, `CXX=mpicxx`, `FC=mpiifx`), so dass CMake Delft3D selbst mit der gleichen Toolchain wie die von Conan erstellten Abhängigkeiten konfiguriert.

```{important}
Das Skript hält das Deltares Conan-Profil bewusst in der Nähe seines Upstream-Formulars und patchet nur die lokalen Intel-Compilerpfade und gegebenenfalls die Compilerversion. Das Upstream-Linux-Profil ist nach einer AlmaLinux 8- und Intel oneAPI 2024-Umgebung benannt. Das Ändern der Verteilungsidentität im Profil kann Conan-Paketidentitäten verändern und die Reproduzierbarkeit verringern.
```

## Installation

### Dateiplatzierung

Platzieren Sie das Skript in einem Arbeitsverzeichnis, in dem die Ausführung von Shells zulässig ist. Das folgende Layout wird empfohlen:

```bash
mkdir -p "$HOME/src/delft3d-native-installer"
cd "$HOME/src/delft3d-native-installer"

# copy or move the script here
ls -l install-delft3d-flow-native.sh
```

Machen Sie das Skript ausführbar:

```bash
chmod +x install-delft3d-flow-native.sh
```

### Standardinstallation

The default invocation builds the Delft3D 4 suite in release mode, copies the resulting installation tree to `$HOME/opt/delft3d-flow`, and runs the standard example as a smoke test:

```bash
./install-delft3d-flow-native.sh
```

The script asks for the `sudo` password when it installs system packages. The default values are summarized in {numref}`default-options`.

```{list-table} Default script options
:name: default-options
:header-rows: 1

* - Option
  - Ausfall
  - Funktion
* - `--src-dir`
  - `$HOME/src/delft3d`
  - Standort des geklonten Delft3D-Quellarchivs.
* - `--prefix`
  - `$HOME/opt/delft3d-flow`
  - Endgültige Installation/Kopienbestimmung.
* - `--config`
  - `d3d4-suite`
  - Delft3D 4 Suite Build, einschließlich Delft3D-FLOW.
* - `--build-type`
  - `Release`
  - Optimierter CMake Build-Typ.
* - `--jobs`
  - `nproc`
  - Parallel Build Level (`CMAKE_BUILD_PARALLEL_LEVEL` und `MAKEFLAGS`).
* - `--tag`
  - nicht eingestellt
  - Verwendet den Standardzweig, es sei denn, ein Zweig, Tag oder Commit ist angegeben.
* - `--no-test`
  - nicht eingestellt
  - Überspringt den Rauchtest mit dem Standardbeispiel.
```

### Reproduzierbare Installation

Für Studien zur Hydrauliktechnik sollte die Quellenrevision festgelegt werden. Ein Branch Tip ist keine reproduzierbare Modellabhängigkeit. Verwenden Sie einen Release-Tag oder Commit Hash, wenn möglich.

```bash
./install-delft3d-flow-native.sh \
  --tag <Delft3D-tag-or-commit> \
  --config d3d4-suite \
  --build-type Release \
  --prefix "$HOME/opt/delft3d-flow"
```

```{note}
Ersetzen Sie `<Delft3D-tag-or-commit>` durch einen Tag oder Commit, der aus dem Deltares-Repository ausgewählt wurde. Das Skript schreibt keine spezifische Version vor, da die entsprechende Überarbeitung vom Modellarchiv, dem Validierungsfall oder den Projektanforderungen des Benutzers abhängt.
```

### Minimal FLOW-orientierter Build

If the objective is only to evaluate the `flow2d3d` build target, the script may be invoked as follows:

```bash
./install-delft3d-flow-native.sh --config flow2d3d
```

For first-time users, `d3d4-suite` remains the preferred trial because it is the suite-level target associated with Delft3D 4. The smaller `flow2d3d` target is more suitable after the host toolchain has already been shown to work.

### Installation von Skipping Packages

Auf verwalteten Universitäts- oder Institutsarbeitsplätzen möchte der Benutzer möglicherweise nicht, dass das Skript Systempakete ändert. Es sind zwei reduzierte Modi vorgesehen.

Überspringen Sie nur den Intel oneAPI Installationsschritt:

```bash
./install-delft3d-flow-native.sh --skip-oneapi-install
```

Überspringen Sie alle `apt` Aktivitäten:

```bash
./install-delft3d-flow-native.sh --no-apt
```

Diese Modi setzen voraus, dass die erforderlichen Compiler und Build-Tools bereits installiert sind. Insbesondere müssen nach der oneAPI-Initialisierung folgende Befehle aufgelöst werden:

```bash
source /opt/intel/oneapi/setvars.sh --force
which icx icpx ifx mpiicx mpiifx mpicxx
```

Wenn die vorinstallierte oneAPI-Version von 2024.2 abweicht, patchet das Skript das Conan-Profil und die erlaubten Compiler-Versionen automatisch, aber eine solche Abweichung entfernt den Build weiter von der Deltares-Basislinie.

```{warning}
A reduced invocation is not a portable solution by itself. It merely prevents package-manager actions. If `git`, Python, the Intel C/C++ and Fortran compilers, or the Intel MPI wrappers are absent or not discoverable, the build will fail at the corresponding diagnostic check.
```

## Start und Test Delft3D-FLOW

### Laufzeitumgebung

After a successful build, the installation tree resides in the selected prefix (default `$HOME/opt/delft3d-flow`) and contains, among others, `bin/run_dflow2d3d.sh`, `bin/d_hydro`, and the `flow2d3d` shared libraries. The script writes an environment file to the prefix. Source this file in every new shell before running Delft3D-FLOW:

```bash
source "$HOME/opt/delft3d-flow/env.sh"
```

This command reinitializes the Intel oneAPI runtime, sets `DELFT3D_HOME`, and puts the Delft3D binaries and libraries on `PATH` and `LD_LIBRARY_PATH`.

### Test mit dem Standardbeispiel

The installer already runs this test at the end of the build unless `--no-test` was given. To repeat it manually, use the standard Delft3D 4 example distributed with the repository (a tidal test case on the `f34` curvilinear grid):

```bash
source "$HOME/opt/delft3d-flow/env.sh"

cd "$HOME/src/delft3d/examples/delft3d4/01_standard"
run_dflow2d3d.sh
```

`run_dflow2d3d.sh` lokalisiert die Installation relativ zu ihrem eigenen Pfad und liest die Modellkonfigurationsdatei `config_d_hydro.xml` aus dem aktuellen Arbeitsverzeichnis. Der Lauf dauert Sekunden. Betrachten Sie den Test als erfolgreich, wenn alle folgenden Bedingungen erfüllt sind:

1. Die Konsolenausgabe endet ohne Fehlermeldungen und das Skript gibt den Exit-Code 0 zurück.
2. Die History- und Map-Ergebnisdateien `trih-f34.dat`, `trih-f34.def`, `trim-f34.dat` und `trim-f34.def` wurden in das Beispielverzeichnis geschrieben.
3. Die Diagnosedatei `tri-diag.f34` enthält keine Zeilen mit `*** ERROR`.

Eine schnelle Überprüfung:

```bash
ls -l trih-f34.* trim-f34.*
grep -i error tri-diag.f34 || echo "no errors in tri-diag.f34"
```

Eine erfolgreiche Ausführung zeigt an, dass die Binär-, Laufzeitbibliotheken und das Kommandozeilen-Startskript auf dem Host gegenseitig konsistent sind. Es stellt keine wissenschaftliche Gültigkeit für ein Projektmodell her. Die Validierung des hydrodynamischen Modells bleibt fallspezifisch und sollte Gitter-, Bathymetrie-, Randbedingungs-, Rauheits-, Prozesskopplungs- und Kalibrierungsprüfungen umfassen.

### Führen Sie Ihr eigenes Modell

Um ein Projektmodell auszuführen, legen Sie die Delft3D-FLOW-Eingabedateien (z. B. `*.mdf`, Raster-, Bathymetrie- und Randdateien) zusammen mit einer `config_d_hydro.xml`-Konfigurationsdatei in ein Arbeitsverzeichnis und starten Sie dann:

```bash
source "$HOME/opt/delft3d-flow/env.sh"

cd /path/to/my-model
run_dflow2d3d.sh                 # uses config_d_hydro.xml
run_dflow2d3d.sh my_config.xml   # or an explicit configuration file
```

Die `config_d_hydro.xml`-Datei von `examples/delft3d4/01_standard` dient als Vorlage; passen Sie den `<mdfFile>`-Eintrag an den Namen der Projektdatei `.mdf` an. Für Parallelläufe mit Intel MPI bietet die Installation auch `run_dflow2d3d_parallel.sh` an, was die Anzahl der Prozesse akzeptiert und ansonsten den gleichen Konventionen folgt.

## Logfiles

Jeder Installerlauf schreibt eine zeitgestempelte Protokolldatei unter:

```bash
$HOME/.cache/delft3d-native-build
```

Wenn der Build fehlschlägt, prüfen Sie den letzten Teil des Protokolls:

```bash
tail -n 120 "$HOME/.cache/delft3d-native-build"/build-*.log
```

Für eine deterministische Diagnoseaufzeichnung kopieren Sie das Protokoll in den Modell- oder Softwareherkunftsordner:

```bash
mkdir -p provenance/software
cp "$HOME/.cache/delft3d-native-build"/build-*.log provenance/software/
```

## Häufige Fehlermodi

```{list-table} Diagnostic interpretation
:name: diagnostics
:header-rows: 1

* - Symptom
  - Wahrscheinliche Ursache
  - Korrekturmaßnahmen
* - `ifx not found` oder `mpiifx not found`
  - Intel oneAPI-Compiler oder MPI-Pakete fehlen oder `setvars.sh` wurde nicht beschafft.
  - Installieren Sie den oneAPI-Compiler und die `intel-oneapi-mpi-devel`-Pakete neu oder überprüfen Sie `/opt/intel/oneapi/setvars.sh`.
* - `CMake 3.30 or higher is required`
  - Das System CMake beschattet die virtuelle Umgebung CMake.
  - Rerun the script; it installs CMake into `$HOME/src/delft3d/.venv` and activates that environment itself.
* - Conan meldet `Invalid setting` für `compiler.version`.
  - The installed oneAPI version is not whitelisted in `conan/config/settings_user.yml`.
  - Lassen Sie das Skript das Profil und die Einstellungen patchen, oder installieren Sie die angehefteten oneAPI 2024.2 Pakete.
* - Fehlendes Drittanbieterpaket während der Conan-Installation.
  - Externe Benutzer müssen Abhängigkeiten lokal aufbauen.
  - Ensure the build command includes `--build-dependencies`; this is the script default.
* - Die CMake-Konfiguration schlägt nach der Abhängigkeitsinstallation fehl.
  - Host-Bibliotheken oder Compiler-Konfiguration unterscheiden sich von der Deltares Linux Container-Baseline.
  - Überprüfen Sie den ersten CMake-Fehler, nicht nur die endgültige Build-Zusammenfassung.
* - `run_dflow2d3d.sh` startet, kann aber keine freigegebene Bibliothek laden.
  - Der Laufzeitbibliothekspfad ist unvollständig.
  - Quelle `<prefix>/env.sh` und bestätigen `LD_LIBRARY_PATH` enthält `<prefix>/lib`.
* - Build ist erfolgreich, aber die Ergebnisse unterscheiden sich von einer anderen Workstation.
  - Source-Revision, Compiler-Version, Dependency Build oder Laufzeitkonfiguration unterscheidet sich.
  - Notieren Sie die Git-Revision, das Skriptprotokoll, die oneAPI-Version und die Modelleingabedateien.
```

## Interpretation des Erfolgs

Die Anlage sollte als erfolgreich angesehen werden, wenn alle folgenden Bedingungen erfüllt sind:

1. `run_conan.py initialize external` completes without remote-credential errors.
2. `build.py` vervollständigt die CMake Build- und Installationsphasen.
3. Das ausgewählte Präfix enthält `bin/run_dflow2d3d.sh`.
4. The standard Delft3D 4 example runs from a clean shell after `env.sh` is sourced and writes the `trih-f34.*` and `trim-f34.*` result files without errors in `tri-diag.f34`.
5. Das Build-Log, die Git-Revision und die Compiler-Versionen werden archiviert.

Für die Computerhydraulik entspricht die binäre Verfügbarkeit nicht der Modellvalidierung. Eine vertretbare Delft3D-FLOW-Studie sollte die Softwarerevision, Compiler-Umgebung, Gitterschematisierung, physikalische Prozessschalter, Boundary Forcing, Kalibrierungsdaten und Akzeptanzmetriken melden.

## Nichtverwertung

Das Skript installiert standardmäßig Dateien im Benutzerbereich. Um die resultierende Installation zu entfernen und den Cache zu erstellen:

```bash
rm -rf "$HOME/opt/delft3d-flow"
rm -rf "$HOME/src/delft3d/build_d3d4-suite_release"
rm -rf "$HOME/src/delft3d/.venv"
rm -rf "$HOME/.conan2"
```

Um den geklonten Quellbaum vollständig zu entfernen:

```bash
rm -rf "$HOME/src/delft3d"
```

System packages installed by `apt`, including the Intel oneAPI packages and the Intel APT repository entry in `/etc/apt/sources.list.d/oneAPI.list`, are not removed automatically. This is intentional because compilers, CMake, Python, Git, and oneAPI components may be shared by other numerical models.

## Empfohlener Citation Record für Berichte

Eine kurze Erklärung zur Reproduzierbarkeit kann in die Projektdokumentation aufgenommen werden:

Delft3D-FLOW wurde nativ auf einem Ubuntu/Linux Mint-Host mit `install-delft3d-flow-native.sh` kompiliert. Das Skript initialisierte den Delft3D externen Conan-Workflow mit Intel oneAPI 2024.2 Compilern und Intel MPI 2021.13, baute die `d3d4-suite`-Konfiguration im `Release`-Modus auf und installierte die Befehlszeilenlaufzeit unter einem Benutzerraumpräfix. Die Delft3D Git-Revision, die Intel oneAPI-Compiler-Version und das Build-Log wurden mit den Modellherkunftsdateien archiviert.

## Referenzen

Deltares. 2026: "Compiling Delft3D on Linux." Delft3D GitHub Repository Dokumentation. https://github.com/Deltares/Delft3D/blob/main/doc/compiling_Linux.md

Deltares. 2026. "Beginn mit der Code-Kompilation und -Entwicklung." Delft3D GitHub Repository Dokumentation. https://github.com/Deltares/Delft3D/blob/main/doc/development.md

Deltares. 2026. "`build.py`." Delft3D GitHub Repository. https://github.com/Deltares/Delft3D/blob/main/build.py

Deltares. 2026. "`delft3d_alma8_intel_2024`Conan profile." Delft3D GitHub Repository. https://github.com/Deltares/Delft3D/blob/main/conan/config/profiles/delft3d_alma8_intel_2024

Deltares. 2026. "`buildtools.Dockerfile`." Delft3D GitHub Repository. https://github.com/Deltares/Delft3D/blob/main/ci/dockerfiles/linux/buildtools.Dockerfile

Intel. 2026. "Installieren mit APT." Intel oneAPI Toolkit Installationshandbuch für Linux. https://www.intel.com/content/www/us/en/docs/oneapi-toolkit/installation-guide-linux/latest/install-oneapi-toolkit-with-apt.html

Intel. 2024. "Verwenden Sie die Setvars und oneapi-vars Scripts mit Linux." Intel oneAPI Programming Guide. https://www.intel.com/content/www/us/en/docs/oneapi/programming-guide/2024-2/use-the-setvars-and-oneapi-vars-scripts-with-linux.html

MyST Markdown. 2026. "Rufe und Ermahnungen." https://mystmd.org/guide/admonitions

Jupyter Book, 2026. "MyST Markdown Übersicht." https://jupyterbook.org/v1/content/myst.html
