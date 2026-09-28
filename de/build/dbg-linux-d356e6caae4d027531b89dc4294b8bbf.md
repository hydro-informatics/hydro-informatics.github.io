---
description: Beheben von Debian Linux- und Ubuntu-Leistungsproblemen, einschließlich Batterieverbrauch, Speicherplatzverwaltung und Systemoptimierungstipps für Benutzer virtueller Maschinen.
---

# Debug & Verbesserung der Erfahrung

Debian Linux ist in einem umfassenden [wiki](https://wiki.debian.org/)] mit Beschreibungen für die Einrichtung des Systems, die Installation von Software (Paketen) und Tutorials für die Fehlersuche dokumentiert. Diese Seite bietet eine Anleitung zu Problemen, die insbesondere bei der Installation von Debian Linux auf einer virtuellen Maschine (VM) auftreten können.

## Energiemanagement (Batterielebensdauer)

Die Arbeit mit Linux auf einem Laptop entleert oft den Akku schnell, besonders wenn man mit reinem Debian arbeitet. Um die Energieeffizienz zu erhöhen, sollten Sie leichte Ubuntu (Derivate) installieren, dh **Mate ** Editionen. Auch das folgende Tool kann dazu beitragen, die Akkulaufzeit auf Ubuntu (Derivate) zu verbessern:

```
sudo add-apt-repository ppa:linrunner/tlp 
sudo apt update 
sudo apt install tlp tlp-rdw 
```

Alternativ werden [Fedora](https://fedoraproject.org/) oder [Arch](https://archlinux.org/)] als energieeffizient bezeichnet. Arch kann jedoch für Linux-Neulinge schwierig sein.


## Besondere Probleme

### Root Drive läuft aus Disk Space

```{tip}
Lesen Sie diesen gesamten Abschnitt, bevor Sie Maßnahmen ergreifen. Andernfalls riskieren Sie, unnötig Speicherplatz zuzuweisen.
```

Im Allgemeinen halten Sie das System sauber, nachdem Sie es aktualisiert haben, indem Sie *Terminal* eingeben:

```
sudo apt clean
sudo apt autoclean
sudo apt autoremove
sudo apt autoremove --purge
sudo apt autoremove
```

Subversion (SVN)-Repositories können auch alte und unnötige Teile enthalten, die entfernt werden können (z. B. aus einem lokalen TELEMAC-MASCARET-Repository) mit (das zweite Argument ist das SVN-Verzeichnis):

```
svn cleanup ~/telemac/v8p1 --non-interactive
```

Wenn die Root-Partition der virtuellen Festplatte leer ist, fordert Debian eine Warnmeldung auf * Das Root-Laufwerk ist leer [...]*. Es gibt viele Möglichkeiten, um Platz durch das Löschen von veralteten oder unnötigen Paketen freizugeben, aber dieses Problem kann auftreten, obwohl nur absolut notwendige Pakete auf einer zu kleinen virtuellen Festplatte installiert sind.

Wenn das Problem mit der Speicherplatzbeschränkung auf einer virtuellen Festplatte auftritt, die mit *VirtualBox* erstellt wurde, öffnen Sie *VirtualBox*, markieren Sie die VM, die dem Problem ausgesetzt ist (z. B. *Debian Linux*). Stellen Sie sicher, dass die VM ausgeschaltet ist. Suchen Sie in *VirtualBox* das Dropdown-Menü *Datei* (oben links), klicken Sie darauf und öffnen Sie den *Virtual Media Manager*. Markieren Sie die virtuelle Festplatte, auf der Debian Linux installiert ist, und erhöhen Sie die *Size *. Klicken Sie auf *Apply* und *Close* den *Virtual Media Manager*.

Eine Vergrößerung des virtuellen Festplattenspeichers allein reicht nicht aus, da der freie Festplattenspeicher der Root-Partition zugewiesen werden muss. Dazu:

* Starten Sie Debian Linux (z.B. in *VirtualBox*, klicken Sie auf *Start*).
*Once Debian Linux started, go to *Activities* and type `gparted` in the search box. Find the *Gparted* software and click on it. If not yet installed, install and open *Gparted*.
* Suchen Sie in *Gparted* nach der `ext4`-Partition (normalerweise `/dev/sda2`) und markieren Sie die Partition direkt hinter dieser Partition (normalerweise `/dev/sda3`).
* Right-click on `/dev/sda3` (the partition behind the root partition) and click on *Swapoff*.
* Right-click again on `/dev/sda3` and click on *Resize/Move*.
    + In the *Free space preceding (MiB):* box, enter a reasonable size to free up disk space for the root partition (e.g., `2000`).
    + Stellen Sie sicher, dass die Felder *Neue Größe * und *Freier Speicherplatz nach * mit dem verfügbaren Speicherplatz übereinstimmen, insbesondere wenn Sie gerade die Größe der virtuellen Festplatte erhöht haben.
    + Klicken Sie auf * Resize/Move*.
* Klicken Sie mit der rechten Maustaste auf die Root-Partition (`/dev/sda2`) und klicken Sie auf *Größe/Bewegung*.
    + Increase the partition size by the amount of disk space free-ed up from the following partition (e.g. increase `6667` MiB to `8667` MiB).
    + Stellen Sie sicher, dass kein *freier Speicherplatz folgt * und dass das Feld mit dem verfügbaren Speicherplatz nach der Root-Partition kohärent ist.
    + Klicken Sie auf * Größe ändern *.
* Finden Sie das grüne Häkchen im oberen Menü von *Geteilt * und klicken Sie darauf. Diese Aktion wird die Änderungen anwenden. Höchstwahrscheinlich informiert eine Warnmeldung über mögliche Probleme beim Neustart des Systems mit der neuen Partitionskonfiguration (Klicken Sie auf OK - das Erhöhen der Stammplatte ist nicht problematisch, wenn dies auf Kosten einer leeren Partition geschieht).
* Nach erfolgreicher Repartitionierung klicken Sie mit der rechten Maustaste auf die Partition nach der Root-Partition (`/dev/sda3`) und stellen Sie sicher, dass sie sich wieder im *Swapoff*-Modus befindet. Wenn dies nicht der Fall ist (d.h. Sie können *Swapoff* im Kontextmenü nicht finden und nur *Swapon* ist sichtbar), klicken Sie auf *Swapon*.

```{tip}
Um unerwünschte Änderungen im Neupartitionierungsplan rückgängig zu machen (bevor Sie auf das Anbringen-Prüfzeichen klicken), klicken Sie auf den gelben Rückkehrpfeil neben dem grünen Anbringen-Prüfzeichen.
```


### Halten Sie System und Software auf dem neuesten Stand

Lesen Sie mehr auf der [Website des Entwicklers](https://www.debian.org/doc/manuals/debian-faq/uptodate.en.html)].


(dbg-permissions)=
### Erlaubnis verweigerte Nachrichten

**Permission denied** Nachrichten können aufgrund des ausfallsicheren Designs von Debian auftreten, aber verweigerte Lese- und Schreibrechte können schnell lästig werden, insbesondere wenn Sie für die Installation von Softwarepaketen zwischen normalen und Superuser-Konten wechseln müssen.

```{admonition} Potentially harmful operation
:class: warning
Never modify the access rights for folders in the `ROOT/` directory. Modifying permissions for folders such as `ROOT/etc/` or `ROOT/root/` may cause unrepairable system damage.
```

So entsperren Sie alle Lese- und Schreibrechte für ein Verzeichnis:

```
sudo chmod a+rwx /directory
```

Oder für alle Unterverzeichnisse:

```
sudo chmod a+rwx /directory/*
```

Oder für alle Dateien in einem Verzeichnis:

```
sudo chmod a+rwx /directory/*.*
```

Oder für alle Unterverzeichnisse und Dateien in diesen Verzeichnissen:

```
sudo chmod a+rwx /directory/*/*.*
```

Dies hebt alle Einschränkungen aus einem Verzeichnis für alle Benutzer, alle seine Unterordner und Dateien enthalten (und Unter-Unterordner und Unter-Unter-Dateien enthalten, und so weiter) - ** Dies kann eine sehr schädliche irreversible Operation sein, wenn sie auf Systemverzeichnisse angewendet wird! **:

```
sudo chmod -R 777 /directory/
```

## Python

### tkinter Imports Fail (Kein Modul namens Tkinter)

`tkinter` ist manchmal nur für * Python2* auf * Linux* installiert, während wir es mit * Python3* verwenden möchten. Um sicherzustellen, dass `tkinter` für * Python3* installiert ist, installieren Sie über * Terminal *:

 * `sudo apt install python3-tk` oder
 * `sudo apt install python3.X-tk` (ersetzen Sie `X` durch Ihre *Python*-Version) oder
 * `sudo apt install tk8.6-dev` to install the library only (this should be sufficient).

 If the above comments do not work, make sure that the `tkinter` repository is available to your system: `sudo add-apt-repository ppa:deadsnakes/ppa` (the repository address may change and depends on your *Linux* and *Python* versions).

## Wein (Windows Apps)

### Allgemeine Weinfragen (Wiedereinbau)

Wenn *wein* nicht wie gewünscht funktioniert, entfernen Sie die aktuelle Installation über *Terminal*:

```bash
sudo apt remove wine wine32 wine64 libwine libwine:i386 fonts-wine
sudo apt remove --purge wine* 
sudo apt autoremove
```

Als nächstes entfernen Sie das Weinpräfix und alle Restkonfigurationsdateien:

```bash
rm -rf ~/.wine
rm -rf ~/.local/share/applications/wine
``` 

Bereiten Sie nun das System für eine saubere Weininstallation vor. Insbesondere benötigt Wine oft 32-Bit-Bibliotheken, selbst wenn ein 64-Bit-Präfix erstellt wird:

```bash
sudo dpkg --add-architecture i386
sudo apt update
```

Wenn noch nicht fertig, fügen Sie die neueste stabile Wine-Version hinzu, um das WineHQ-Repository zu verwenden. Laden Sie zuerst den Repository-Schlüssel herunter und fügen Sie ihn hinzu:

```bash
wget -nc https://dl.winehq.org/wine-builds/winehq.key
sudo apt-key add winehq.key
```


Fügen Sie dann das Repository hinzu. Wenn Ihre Linux Mint-Version beispielsweise auf Ubuntu 20.04 (Focal) basiert:
```bash
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main'
sudo apt update
```

Wenn Ihre Linux Mint auf einer anderen Ubuntu-Version basiert, passen Sie das Repository entsprechend an.

````{admonition} Fix Key Storage DEPRECATION Warning

The warning message `https://dl.winehq.org/wine-builds/ubuntu/dists/focal/InRelease: Key is stored in legacy trusted.gpg keyring (/etc/apt/trusted.gpg), see the DEPRECATION section in apt-key(8) for details.` can be fixed with the following workflow:

1. Download and save the WineHQ Key in a new location: Run the following command to download the key, dearmor it, and save it into the recommended location (e.g., `/usr/share/keyrings/winehq-archive.key`):

```bash
wget -qO- https://dl.winehq.org/wine-builds/winehq.key | gpg --dearmor | sudo tee /usr/share/keyrings/winehq-archive.key
```

Dieser Befehl holt den Schlüssel und konvertiert ihn in ein Format, das apt direkt verwenden kann.

2. Aktualisierung der Repository-Konfiguration

Modify the WineHQ repository entry to reference the new key file. This is typically found in a file like `/etc/apt/sources.list.d/winehq.list` (sometimes also in `/etc/apt/sources.list.d/additional-repositories.list` or `/etc/apt/sources.list` if added manually). Open the file to edit it with your preferred text editor. First, locate the line that looks similar to:

```bash
deb https://dl.winehq.org/wine-builds/ubuntu/ focal main
```

Second, modify it by adding the `signed-by` option so it reads:
```bash
deb [signed-by=/usr/share/keyrings/winehq-archive.key] https://dl.winehq.org/wine-builds/ubuntu/ focal main
```

Speichern Sie die Datei und verlassen Sie den Editor.

3. Aktualisieren Sie die Paketlisten:

```bash
sudo apt update
```

Wenn alles korrekt konfiguriert ist, sollte die Warnung bezüglich des Legacy trusted.gpg Keyrings nicht mehr angezeigt werden.

````

Installieren Sie nun das stabile Wine Release:

```bash
sudo apt install --install-recommends winehq-stable
```

Erwägen Sie auch, Winetricks zu installieren, was die Installation vieler Laufzeitbibliotheken und Frameworks vereinfacht:
```bash
sudo apt install winetricks
```

### 64-Bit-Anwendung funktioniert nicht

If a 64-bit *msi* or other installer / application is not working as desired, try to adapt the `WINEPREFIX`. First, remove any old prefix if necessary:

```bash
rm -rf ~/.wine
```
Dann zwingen Sie Wine, ein 64-Bit-Präfix zu erstellen:
```bash
WINEARCH=win64 winecfg
```
Das Weinkonfigurationsfenster wird angezeigt. Setzen Sie auf der Registerkarte "Anwendungen" die Windows-Version auf ** Windows 10**. Klicken Sie auf **Apply** und **OK**.


### Installation von .NET Framework

Wine kann Winetricks verwenden, um verschiedene Versionen von .NET Framework zu installieren. Abhängig von den Anforderungen einer Windows-Anwendung benötigen Sie möglicherweise eine bestimmte Version. Um beispielsweise .NET Framework 4.8 zu installieren, verwenden Sie Winetricks (siehe oben), um ein neues Präfix zu erstellen:

```bash
WINEPREFIX=~/.wine winetricks dotnet48
```

Der Installationsprozess kann eine Weile dauern und kann mehrere Neustarts von Wine erfordern. Befolgen Sie die Anweisungen auf dem Bildschirm sorgfältig.

Some users find that certain .NET versions install more reliably in a 32‑bit prefix—even when targeting Windows 10 apps. If you encounter issues, you may try creating a 32‑bit prefix by omitting the `WINEARCH=win64` environment variable (or explicitly using `WINEARCH=win32`). However, note that truly 64‑bit Windows applications require a 64‑bit environment.


## QGIS

### GPG-Fehler - Public Key nicht verfügbar (APT UPDATE)

Gelegentlich (buchstäblich ...) wird der GPG-Schlüssel der QGIS-Repositories ungültig, was zu einem Fehler bei der Verwendung führt:

```
sudo apt update

[...]

W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: https://ubuntugis.qgis.org/ubuntugis focal InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY D155B8E6A419C5BE

W: Failed to fetch https://qgis.org/ubuntugis/dists/focal/InRelease  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY D155B8E6A419C5BE

[...]
```

To troubleshoot this error, note the unavailable key (i.e., `D155B8E6A419C5BE` in the above example) and then update the unavailable key:


```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D155B8E6A419C5BE
```

Um zu testen, ob das Schlüsselupdate funktioniert hat, tippen Sie `sudo apt update`

### Kein Modul namens OpenGL

Wenn QGIS die Fehlermeldung `ModuleNotFoundError: No module named 'OpenGL'` ausgibt, installieren Sie *Mesa* wie folgt auf Ubuntu (d. H. Debian Linux) basierenden Betriebssystemen (einschließlich Mint und Lubuntu).

Bringen Sie `apt` und `pip` auf den neuesten Stand:

```
sudo apt update
python -m install --upgrade pip
```

Installieren Sie die folgenden Systempakete (falls noch nicht fertig):

```
sudo apt install build-essential freeglut3 freeglut3-dev mesa-common-dev binutils-gold libglew-dev libglm-dev python-pyqt5
```

Installieren Sie die folgenden Python-Pip-Pakete:

```
python -m pip install pyOpenGL
python -m pip install pyOpenGL_accelerate
python -m pip install PyQt5
python -m pip install PyQt5-sip
python -m pip install PyQtWebEngine
```

A system restart (or just reload the user environment with `source ~/.bashsrc`) may be necessary for QGIS to work now without the OpenGL error.


### SCHÜCKEL

To get LAStools working in QGIS on Ubuntu (make sure to have {ref}`wine` installed):

* Laden Sie die LAStools (ZIP) von http://rapidlasso.com/LAStools herunter und extrahieren Sie die ZIP-Datei
* Bearbeiten Sie in QGIS die Verarbeitungsoptionen (Anbieter > Tools für LiDAR-Daten):
  * LasTools-Ordner: Geben Sie hier den Pfad zum Ordner ein, in dem die extrahierten ZIP-Dateien leben (`/dir/to/LAStools/`)
  * Wine folder: enter the path to the {ref}`wine` binary (typically `/usr/bin/`). Alternatively, find where Wine lives with the `whereis wine` command
* Bei Bedarf: Bearbeiten Sie `LidarToolsAlgorithmProvider.py` (zwei Dateien können vorhanden sein):
Zeile 145: if (True):
Zeile 168: if (True):
Zeile 188: if (True):

Um eine LAStools-Installation in QGIS zu beheben, lesen Sie [diesen Vorschlag auf rapidlasso.com](https://rapidlasso.com/2013/09/29/how-to-install-lastools-toolbox-in-qgis/)].

Lesen Sie mehr über das Laufen [LAStools auf Ubuntu](https://gis.stackexchange.com/questions/138149/wine-lastools-in-qgis-2-8-1-ubuntu-14-04)].

## 3D Grafiktreiber

GPU-intensive Software, die eine starke Grafikleistung erfordert, wie die Unreal Engine, erfordert neueste Grafikkarten und Treiber. Die Standardgrafiktreiber sind möglicherweise nicht in der Lage, die Anforderungen an solche Geräte zu erfüllen. Neueste Versionen von Grafiktreibern können über proprietäre Treiber installiert werden (z. B. die proprietären Treiber von nVidia, um Nouveau-Treiber zu ersetzen).

Hier ist eine Option zum Aktualisieren von nVidia-Grafiktreibern, obwohl Sie sich bewusst sind, dass diese Aktion Ihrem System erheblich schaden kann (es wird möglicherweise nicht neu gestartet), wenn Sie kein Ubuntu Linux (Derivat) mit einer entsprechenden nVidia-Grafikkarte ausführen. Wenn Sie mit dieser Warnung einverstanden sind:

* Offenes Terminal
* Finden Sie den passenden Treiber für Ihr System mit `sudo apt search nvidia-driver` (ODER suchen Sie nach einem Treiberpaket: `apt-cache search nvidia-driver`)
* Überprüfen Sie die neuesten Treiber Releases
  * bei nvidia-Fahrern:

```
sudo apt-cache search 'nvidia-driver-' | grep '^nvidia-driver-[[:digit:]]*'
```

  * in dkm:

```
sudo apt-cache search 'nvidia-dkms-' | grep '^nvidia-dkms-[[:digit:]]*'
```

```
[...]
nvidia-dkms-470 - NVIDIA DKMS package
nvidia-dkms-470-server - NVIDIA DKMS package
nvidia-dkms-495 - Transitional package for nvidia-dkms-510
nvidia-dkms-510 - NVIDIA DKMS package
nvidia-dkms-510-server - NVIDIA DKMS package
nvidia-dkms-515 - NVIDIA DKMS package
nvidia-dkms-515-server - NVIDIA DKMS package
```

  * In diesem Beispiel ist der neueste Treiber `nvidia-driver-515` (mit `nvidia-dkms-515`), den wir notieren, um sie zwei Schritte später zu installieren

* Aktualisieren Sie die Paketinformationen und Ihr System:

```
sudo apt update
sudo apt full-upgrade
```

* Installieren Sie den neuesten Treiber mit:
```
sudo apt install nvidia-driver-515 nvidia-dkms-515
```
* Starten Sie Ihr System neu:
```
sudo shutdown -r now
```
* Überprüfen Sie die Installation im Terminal:
```
nvidia-smi
```

## Mac OS Apps (DMG File Handling)

MacOS-Anwendungen werden oft als DMG-Dateien verteilt. Obwohl Linux keine DMG-Dateien nativ unterstützt, können sie in eine mountbare IMG-Datei konvertiert werden, um dann ein ISO-Image zu erstellen, das einfacher zu mounten und mit Linux zu arbeiten ist.

### Konvertieren Sie das DMG in ein IMG

Installieren Sie zunächst das `dmg2img`-Tool:

```bash
sudo apt install dmg2img
```

Konvertieren Sie die DMG-Datei durch Ausführen:

```bash
dmg2img /path/to/file.dmg
```

Dieser Befehl erstellt eine IMG-Datei mit dem gleichen Basisnamen wie die DMG, formatiert mit Apples HFS + Dateisystem.

### Mounten Sie die IMG-Datei

Da die IMG-Datei das HFS + -Dateisystem verwendet, laden Sie das folgende Kernelmodul:

```bash
sudo modprobe hfsplus
```

Create a mount point (tpyically, in `/media`):

```bash
sudo mkdir -p /media/user/appname
```

Mounten Sie die IMG-Datei mit einem Loop-Gerät:

```bash
sudo mount -t hfsplus -o loop /path/to/file.img /media/user/appname
```

### Erstellen Sie eine ISO aus dem montierten IMG

Während es möglich ist, direkt mit dem montierten IMG zu arbeiten, verbessert die Umwandlung in eine ISO die Linux-Kompatibilität. Eine Möglichkeit, dies zu tun, ist Brasero, ein grafisches Werkzeug zum Brennen von Scheiben zum Erstellen von ISO-Images. Daher installieren Sie zuerst Brasero:

```bash
sudo apt install brasero
```

Folgen Sie diesen Schritten:

1. **Brasero** starten, indem Sie es aus dem Systemmenü öffnen (normalerweise unter **Sound & Video**) oder danach suchen.
2. Starten Sie ein neues Poject mit einem Klick auf **Data project**.
3. **Fügen Sie Dateien mit einem Klick auf das Plus-Symbol hinzu (normalerweise oben links) und wählen Sie den Ordner aus, in dem die IMG-Datei gespeichert ist (`/media/user/appname`).
4. Klicken Sie auf **Burn**, wählen Sie ein Ausgabeverzeichnis und ändern Sie optional den Ausgabebildnamen.
5. Klicken Sie auf **Bild erstellen**, um die ISO-Datei zu generieren.

### Befestigen Sie das ISO-Bild

ISO-Images werden nativ von Ubuntu unterstützt. Um die neue ISO zu montieren:

1. **(Optional) laden Sie das HFS+ Modul:**
Wenn die ISO weiterhin HFS+ verwendet (dies ist bei Standard-ISO-Bildern ungewöhnlich), führen Sie Folgendes aus:
   
   ```bash
   sudo modprobe hfsplus
   ```

2. **Erstellen Sie einen Befestigungspunkt für die ISO:**

   ```bash
   sudo mkdir -p /media/user/appnameISO
   ```

3. **Mount die ISO:**
Wenn die ISO HFS + verwendet, montieren Sie sie mit:

   ```bash
   sudo mount -t hfsplus -o loop /path/to/file.iso /media/user/appnameISO
   ```

Andernfalls verwenden Sie für ein Standard-ISO 9660-Dateisystem einfach:

   ```bash
   sudo mount -o loop /path/to/file.iso /media/user/appnameISO
   ```

Jetzt sind alle Inhalte der ISO (ursprünglich aus dem DMG/IMG) im Verzeichnis `/media/user/appnameISO` zugänglich.


```{admonition} Uncertain filesystem and other ISO creation tools
:class: note

Wenn Probleme auftreten oder der Dateisystemtyp unsicher ist, möchten Sie möglicherweise versuchen, ihn zu montieren, ohne einen Typ anzugeben, mit dem Ubuntu ihn automatisch erkennen kann.

There are also command-line tools (like `mkisofs` or `genisoimage`) available for ISO creation if you prefer a non-GUI approach.
```


### Starten der Anwendung von der montierten ISO

Der Inhalt der montierten ISO kann erforscht werden, um die Anwendung zu lokalisieren und zu starten. Beachten Sie, dass macOS-Anwendungen unter Linux noch nicht nativ ausführbar sind. Eine Kompatibilitätsschicht wie [Darling](https://www.darlinghq.org/) kann erforderlich sein].

####  Suchen Sie das Anwendungsbündel

MacOS apps are typically packaged as `.app` bundles. Here is how to find them:

- **Browsen Sie im Mounted Directory:**
  Open the file manager or use the terminal to navigate to the mount point (e.g., `/media/user/appnameISO`).

- **Identify the `.app` bundle:**  
  Look for directories ending with `.app` (for example, `MyApp.app`).

#### Finden Sie die ausführbare Datei innerhalb des Bundles

- **Öffne das App-Bundle:**
Navigieren Sie im Verzeichnis `.app` zum Ordner `Contents`.
  
- ** Lokalisieren Sie den Binär: **
  Within `Contents`, the `MacOS` subdirectory typically stores the executable file. For isntance, the full path might be:
  ```
  /media/user/appnameISO/MyApp.app/Contents/MacOS/MyApp
  ```

#### Starten Sie die Anwendung

`````{tab-set}
````{tab-item} Use Darling (macOS Compatibility Layer)

Da macOS-Binärdateien nicht nativ unter Linux laufen, besteht eine Option darin, [Darling](https://www.darlinghq.org/)] zu verwenden, das eine Übersetzungsschicht für macOS-Apps bereitstellt.

1. **Install Darling:**
Befolgen Sie die Anweisungen auf der [Darling website](https://www.darlinghq.org/)], um es auf dem System zu installieren.

2. ** Starten Sie eine Darling-Shell und starten Sie die App: **

   ```bash
   darling shell
   cd /media/user/appnameISO/MyApp.app/Contents/MacOS
   ./MyApp
   ```

Beachten sie, dass darling immer noch experimentell ist, so dass nicht alle apps einwandfrei laufen.
````

````{tab-item} Run a Cross-Platform App

Wenn die App in einer plattformübergreifenden Sprache (wie Java) geschrieben ist oder ein Launch-Skript enthält:

1. ** Überprüfen Sie nach Startskripten oder Dokumentationen:**
   Sometimes the ISO will contain a README or a script (e.g., `launch.sh`) that explains how to run the app on Linux.

2. ** Führen Sie das Skript oder den Befehl aus:**
Befolgen Sie die angegebenen Anweisungen, um die Anwendung zu starten.

````
`````

#### Überprüfung und Fehlerbehebung


Wenn die App startet, sollte sich ihre GUI öffnen oder es sollte eine Bestätigungsnachricht im Terminal geben.

f die Anwendung nicht gestartet wird, stellen Sie sicher, dass:
* die erforderlichen Kompatibilitätsschichten (z. B. Darling) installiert sind.
* Alle erforderlichen Abhängigkeiten sind verfügbar.
* you have permission to execute the file (you might need to run `chmod +x /path/to/executable`).


```{admonition} Read the docs!
:class: tip

Konsultieren Sie immer alle bereitgestellten Dokumentationen in der ISO für anwendungsspezifische Anweisungen oder zusätzliche Abhängigkeiten. Dies kann Aufschluss darüber geben, ob die App nur für macOS ausgelegt ist oder ob ein Workaround für Linux existiert.

```

