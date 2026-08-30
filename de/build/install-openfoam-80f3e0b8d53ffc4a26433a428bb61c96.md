---
description: Schritt-für-Schritt-OpenFOAM-Installationshandbuch für Ubuntu, Debian und andere Linux-Plattformen, das CFD- und Flussstruktur-Interaktionssimulationen ohne Docker-Overhead ermöglicht.
---

(openfoam-install)=
# OpenFOAM (Installation)

Dieses Tutorial führt durch die Installation von [OpenFOAM](https://openfoam.org/) auf [Ubuntu Linux](https://ubuntu.com/) und {ref}`openfoam-debian`]. Für die Installation von OpenFOAM auf vielen anderen Plattformen (auch *Windows*) besuchen Sie die [Website des Entwicklers](https://openfoam.org)].

```{admonition} Learn OpenFOAM
OpenFOAM stellt ein leistungsstarkes Modellierungswerkzeug dar, das hier zur Modellierung der Fluss-Struktur-Interaktion empfohlen wird. OpenFOAM-Entwickler bieten detaillierte Dokumentationen mit hochwertigen Tutorials auf ihrer Website. Insbesondere ist ihr 3-wöchiges Tutorial ein sehr guter Start in die OpenFOAM-Modellierung für Doktoranden oder Ingenieure.
```

```{admonition} Max out computation power
Unter Debian Linux / Ubuntu / Mint sollten Sie OpenFOAM vorzugsweise aus dem Ubuntu-Repository installieren, anstatt OpenFOAM in einem *Docker*-Container zu installieren. Der Grund dafür ist, dass ein Docker-Container eine virtuelle Umgebung ist, die es OpenFOAM nicht ermöglicht, direkt auf die volle physische Kapazität Ihres Computers zuzugreifen.
```

## Ubuntu (einschließlich Mint und Lubuntu)

Die Installation auf *Ubuntu Linux* oder einem seiner Derivate ist wahrscheinlich eine der einfachsten und nachhaltigsten Möglichkeiten, mit OpenFOAM zu arbeiten.

### OpenFOAM installieren

Die Installation auf einer beliebigen *Ubuntu Linux*-Plattform ist unkompliziert und kann wie auf der [Website des Entwicklers](https://openfoam.org/download/13-ubuntu/)] beschrieben durchgeführt werden. Im Detail umfassen diese Schritte:

1. Download and add the *gpg key* <br> `sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"`
1. Fügen Sie das Repository zu *sources.list* <br> `sudo add-apt-repository http://dl.openfoam.org/ubuntu` hinzu
1. Update the `apt` package list <br> `sudo apt update`
1. Install OpenFOAM along with a tailored version of ParaView: <br> `sudo apt -y install openfoam13`

Optional installieren Sie *gedit*, das häufig in der Dokumentation und für Anweisungen zum Einstellen von Umgebungsvariablen verwendet wird:

```
sudo apt install gedit
```

```{tip}
Even though the developer's installation instructions suggest using `apt-get update` / `install`, preferably use `apt update` / `install`.
```

### Update OpenFOAM

Die OpenFOAM-Entwickler aktualisieren (rekompilieren) regelmäßig neue Versionen von `openfoam13`. Um diese neuesten Versionen laufen zu lassen:

```
sudo apt update
sudo apt install --only-upgrade openfoam13
```

### Benutzerkonfiguration einrichten

OpenFOAM verwendet eine Reihe von Umgebungsvariablen, die den Aufruf des Programms und seiner Helfer unterstützen. Um Umgebungsvariablen zu definieren, muss jeder OpenFOAM - *Ubuntu*-Benutzer die *.bashrc*-Datei ändern, die im Verzeichnis */home/USER/* gespeichert ist:

* Open the user *.bashrc* file: <br> `gedit ~/.bashrc`
* Auf der Unterseite der *.bashrc* Datei hinzufügen: <br> `source /opt/openfoam13/etc/bashrc`
* Speichern und schließen Sie die Benutzer *.bashrc * Datei.

Öffnen Sie ein neues *Terminal* (oder melden Sie sich sicher bei *Ubuntu* erneut an) und testen Sie, ob das System die OpenFOAM-Umgebungsvariablen erkennt:

```
simpleFoam -help
```

Verwendung simpleFoam [Optionen]
...


Wenn es richtig eingerichtet ist, gibt *Terminal* eine Reihe von Optionen zum Ausführen von OpenFOAM zurück.

### Prüflauf

Erstellen Sie mit den definierten Umgebungsvariablen ein neues Verzeichnis für OpenFOAM-Projekte:

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
```

Kopieren Sie das *pitzDaily* OpenFOAM-Tutorial mithilfe der `$FOAM_[...]` Umgebungsvariablen ([vollständige Liste](https://openfoamwiki.net/index.php/Environment_variables)]):

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Führen Sie den *blockMesh* (pre), den *simpleFoam* (main) und den *paraFoam* (post) Prozessor aus:

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

Um mit OpenFOAM zu beginnen, lesen Sie den *User Guide* von [*CFD Direct*](https://cfd.direct/openfoam/user-guide/)].

(openfoam-debian)=
## Debian (über Docker)

### Voraussetzungen

Debian-Benutzer müssen *curl* und *docker* installieren, um OpenFOAM installieren zu können. Stellen Sie zunächst sicher, dass Sie eine veraltete Version von *docker* loswerden (wenn dies einen Fehler zurückgibt, ist das kein Problem):

```
sudo apt-get remove docker docker-engine docker.io containerd runc
```

*docker* Abhängigkeiten installieren:

```
sudo apt install apt-transport-https ca-certificates curl gnupg
```

Fügen Sie *docker*s *GPG*-Schlüssel hinzu:

```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Fügen Sie das stabile *docker* Repository hinzu:

```
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Aktualisieren Sie *apt* und installieren Sie *docker*:

```
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

Überprüfen Sie die erfolgreiche Installation von *docker*:

```
sudo docker run hello-world
```

Bis hier ist *docker* nur für Sudoer installiert. Um *docker* und OpenFOAM für jeden Benutzer ausführen zu können, muss der *USERNAME* des Benutzers der `docker`-Gruppe des Systems hinzugefügt werden. Daher **fügen Sie jeden *Docker* und OpenFOAM-Benutzer zur `docker`-Gruppe** hinzu (für jeden **USERNAME** erforderlich):

```
sudo usermod -aG docker USERNAME
```

Wenn *docker* installiert ist, ist das System bereit für die Installation von OpenFOAM auf *Debian*.

Stellen Sie auf einem Remote-Desktop-Computer oder einer virtuellen Maschine sicher, dass Sie auch *X11* und *Xrdp* installieren, beispielsweise für einen *Xfce*-Desktop:

```
sudo apt install xorg dbus-x11 x11-xserver-utils
sudo apt install xfce4 xfce4-goodies xrdp
```

### Installieren Sie OpenFOAM (v13)

Laden Sie das neueste OpenFOAM-Paket für *docker* herunter:

```
sudo sh -c "wget http://dl.openfoam.org/docker/openfoam13-linux -O /usr/bin/openfoam13-linux"
```

Machen Sie das heruntergeladene `openfoam13-linux`Script ausführbar:

```
sudo chmod 755 /usr/bin/openfoam13-linux
```

### Get Started (Erstmaliger Launch)

Erstellen Sie ein neues Verzeichnis (z. B. */home/OpenFoam13/*) und starten Sie die `openfoam13-linux`-Umgebung:

```
cd ~
mkdir OpenFoam13
cd OpenFoam13
openfoam13-linux
```

Die *Docker*-Umgebung sollte nun in *Terminal* gestartet werden. Um OpenFOAM zu testen, kopieren Sie den *pitzDaily* OpenFOAM Tutorial mithilfe der [**FOAM** Umgebungsvariablen](https://openfoamwiki.net/index.php/Environment_variables)]:

```
mkdir -p $FOAM_RUN
cd $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily .
```

Führen Sie den *blockMesh* (pre), den *simpleFoam* (main) und den *paraFoam* (post) Prozessor aus:

```
cd pitzDaily
blockMesh
simpleFoam
paraFoam
```

To quit *docker*, tap `exit`. The installation procedure is described in detail on the [developer's website](https://openfoam.org/download/13-linux/).

### Normales Startverfahren

Wenn *docker* und OpenFOAM installiert sind, kann jeder Benutzer der `docker`-Gruppe (siehe oben Anweisungen zum Hinzufügen von Benutzern zum Docker `group`) OpenFOAM über *Terminal* starten, indem er Folgendes eingibt:

```
openfoam13-linux
```

Um den Programmtipp zu beenden (in *Terminal*/*docker*):

```
exit
```

Um mit OpenFOAM zu beginnen, lesen Sie den *User Guide* von [*CFD Direct*](https://cfd.direct/openfoam/user-guide/)].


## Versorgungsunternehmen (Pre- & Postprozessoren)


### SALOME

Um SALOME zu installieren, lesen Sie bitte die TELEMAC-Installationsanweisung {ref}`here <salome-install>`.

(freecad-install)=
### FreeCAD

*FreeCAD* ist für die meisten gängigen Plattformen (Betriebssysteme) verfügbar, darunter *Windows*, *Linux* und *macOS*. Finden Sie die neueste Version und Installationsanweisungen auf der [Website des Entwicklers](https://www.freecad.org/)].
