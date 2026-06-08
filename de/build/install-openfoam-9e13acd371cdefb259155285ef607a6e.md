---
description: Schritt für Schritt OpenFOAM-Installationsführer für Ubuntu, Debian und andere Linux-Plattformen, die CFD- und Flow-Struktur-Interaktionssimulationen ohne Docker-Overhead ermöglichen.
---

(openfoam-install)=
# OpenFOAM (Installation)

Dieses Tutorial führt durch die Installation von [OpenFOAM](https://openfoam.org/) [Ubuntu Linux](https://ubuntu.com/) und {ref}`openfoam-debian`. Für die Installation von OpenFOAM auf vielen anderen Plattformen (auch *Windows*) besuchen Sie die [developer's website](https://openfoam.org).

```{admonition} Learn OpenFOAM
OpenFOAM stellt ein leistungsstarkes Modellierungstool dar, das hier zur Modellierung von Strömungs-Struktur-Interaktion empfohlen wird. OpenFOAM Entwickler bieten detaillierte Dokumentationen mit qualitativ hochwertigen Tutorials auf ihrer Website. Besonders ihr 3-wöchiges Tutorial ist ein sehr guter Start in die OpenFOAM-Modellierung für Doktoranden oder Ingenieure.
```

```{admonition} Max out computation power
Auf Debian Linux / Ubuntu / Mint installieren Sie vorzugsweise OpenFOAM aus dem Ubuntu-Repository anstatt OpenFOAM in einem *Docker*-Container zu installieren. Der Grund dafür ist, dass ein Docker-Container eine virtuelle Umgebung ist, die es OpenFOAM nicht ermöglicht, direkt auf die volle physische Kapazität Ihres Computers zuzugreifen.
```

## Ubuntu (inkl. Mint und Lubuntu)

Die Installation auf *Ubuntu Linux* oder einer seiner Derivate ist wahrscheinlich eine der einfachsten und nachhaltigsten Möglichkeiten, mit OpenFOAM zu arbeiten.

### OpenFOAM installieren

Die Installation auf jeder *Ubuntu Linux*-Plattform ist unkompliziert und kann wie auf der [developer's website](https://openfoam.org/download/13-ubuntu/)] beschrieben durchgeführt werden. Im Einzelnen umfassen diese Schritte:

1. Download and add the *gpg key* <br> `sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"`
1. Add the repository to *sources.list* <br> `sudo add-apt-repository http://dl.openfoam.org/ubuntu`
1. Update the `apt` package list <br> `sudo apt update`
1. Install OpenFOAM along with a tailored version of ParaView: <br> `sudo apt -y install openfoam13`

Optional installieren Sie *gedit*, die häufig in der Dokumentation und für Anweisungen zur Einstellung von Umgebungsvariablen verwendet wird:

```
sudo apt install gedit
```

```{tip}
Auch wenn die Installationsanweisungen des Entwicklers unter `apt-get update` / `install` andeuten, verwenden Sie vorzugsweise `apt update` /`install`.
```

### Update OpenFOAM

Die OpenFOAM-Entwickler aktualisieren (recompile) neue Versionen von `openfoam13`. Um diese neuesten Versionen laufen zu lassen:

```
sudo apt update
sudo apt install --only-upgrade openfoam13
```

### Benutzerkonfiguration einrichten

OpenFOAM verwendet eine Reihe von Umgebungsvariablen, die Hilfe beim Aufrufen des Programms und seiner Helfer. Um Umgebungsvariablen zu definieren, muss jeder OpenFOAM - *Ubuntu*-Benutzer die *.bashrc*-Datei ändern, die im */home/USER/*-Verzeichnis lebt:

* Open the user *.bashrc* file: <br> `gedit ~/.bashrc`
* On the bottom of the *.bashrc* file add: <br> `source /opt/openfoam13/etc/bashrc`
* Save and close the user *.bashrc* file.

Öffne ein neues *Terminal* (oder, um sicher, re-login auf *Ubuntu*) und teste, ob das System die OpenFOAM-Umgebungsvariablen erkennt:

```
simpleFoam -help
```

Verwendung simpleFoam [Optionen]
...


Wenn korrekt eingerichtet, *Terminal* gibt eine Reihe von Optionen für den Betrieb von OpenFOAM zurück.

### Prüflauf

Erstellen Sie mit den definierten Umgebungsvariablen ein neues Verzeichnis für OpenFOAM-Projekte:

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
```

Kopieren Sie das *pitzDaily* OpenFOAM-Tutorial unter Verwendung der `$FOAM_[...]`Umgebungsvariablen ([full list](https://openfoamwiki.net/index.php/Environment_variables)):

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Führen Sie den *blockMesh* (pre), den *simpleFoam* (main) und den *paraFoam* (post) Prozessoren aus:

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

Um mit OpenFOAM zu beginnen, lesen Sie bitte den *User Guide* von [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).

(openfoam-debian)=
## Debian (via Docker)

### Voraussetzungen

Debian-Benutzer müssen *curl* und *docker* installieren, um OpenFOAM installieren zu können. Stellen Sie zunächst sicher, jede veraltete Version von *docker* loszuwerden (wenn dies einen Fehler gibt, das ist kein Problem):

```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

Installieren Sie *docker* Abhängigkeiten:

```
sudo apt install apt-transport-https ca-certificates curl gnupg
```

*docker*'s *GPG* Schlüssel hinzufügen:

```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Fügen Sie das stabile *docker* Repository hinzu:

```
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

*apt* aktualisieren und *docker* installieren:

```
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

Überprüfen Sie die erfolgreiche Installation von *docker*:

```
sudo docker run hello-world
```

Bis hier ist *docker* nur für Sudoers installiert. Um *docker* und OpenFOAM für jeden Benutzer zu aktivieren, muss der *USERNAME* der Systemgruppe `docker` hinzugefügt werden. ** hat daher jeden *docker* und OpenFOAM-Nutzer an die `docker`-Gruppe** (erforderlich für jeden **USERNAME**):

```
sudo usermod -aG docker USERNAME
```

Mit *docker* ist das System bereit für die Installation von OpenFOAM auf *Debian*.

Stellen Sie auf einem Remote-Desktop-Computer oder einer virtuellen Maschine sicher, auch *X11* und *Xrdp* zu installieren, zum Beispiel für einen *Xfce*-Desktop:

```
sudo apt install xorg dbus-x11 x11-xserver-utils
sudo apt install xfce4 xfce4-goodies xrdp
```

### OpenFOAM (v13) installieren

Laden Sie das neueste OpenFOAM-Paket für *docker* herunter:

```
sudo sh -c "wget http://dl.openfoam.org/docker/openfoam13-linux -O /usr/bin/openfoam13-linux"
```

Machen Sie das heruntergeladene Skript `openfoam13-linux` ausführbar:

```
sudo chmod 755 /usr/bin/openfoam13-linux
```

### Starten (First-time Launch)

Erstellen Sie ein neues Verzeichnis (z.B. */home/OpenFoam13/*) und starten Sie die `openfoam13-linux`-Umgebung:

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
openfoam13-linux
```

Die *docker*-Umgebung sollte jetzt in *Terminal* gestartet werden. Um OpenFOAM zu testen, kopieren Sie die *pitzDaily* OpenFOAM-Tutorial unter Verwendung der Umweltvariablen [**FOAM**](https://openfoamwiki.net/index.php/Environment_variables):

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Führen Sie den *blockMesh* (pre), den *simpleFoam* (main) und den *paraFoam* (post) Prozessoren aus:

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

Um *docker* zu beenden, tippen Sie auf `exit`. Das Installationsverfahren wird im Detail auf der [developer's website](https://openfoam.org/download/13-linux/).

### Übliches Startverfahren

Mit der Installation von *docker* und OpenFOAM kann jeder Benutzer der `docker`-Gruppe (siehe obige Anleitungen zum Hinzufügen von Benutzern an den Docker`group`) OpenFOAM durch *Terminal* starten, indem er Folgendes eingibt:

```
openfoam13-linux
```

Um den Programmhahn zu beenden (in *Terminal*/*docker*):

```
exit
```

Um mit OpenFOAM zu beginnen, lesen Sie bitte den *User Guide* von [*CFD Direct*](https://cfd.direct/openfoam/user-guide/).


## Utilities (Pre- & Post-Prozessoren)


### SALOME

Um SALOME zu installieren, lesen Sie bitte die TELEMAC Installationsanweisung {ref}`here <salome-install>`.

(freecad-install)=
### FreeCAD

*FreeCAD* ist für die meisten gängigen Plattformen (Betriebssysteme) einschließlich *Windows*, *Linux* und *macOS* erhältlich. Die neueste Version und Installationsanleitung finden Sie auf der [developer's website](https://www.freecad.org/).
