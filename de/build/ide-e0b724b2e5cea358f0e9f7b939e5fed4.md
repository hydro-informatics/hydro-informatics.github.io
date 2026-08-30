---
description: Überblick über Python IDEs und APIs für die Wasserressourcentechnik, einschließlich PyCharm, JupyterLab und Anaconda, mit Anleitung zur Auswahl der richtigen Entwicklungsumgebung.
---

(sec-ide)=
# Integrierte Entwicklungsumgebungen (IDE)

Die Lehrinhalte für die Programmierung in diesem eBook erfordern sogenannte *Application Programming Interface*s (**API**s) und *Integrated Development Environment*s (**IDE**s).

Ein **API** stellt eine Computerschnittstelle dar, die Interaktionen zwischen mehreren Software-Intermediären ermöglicht. Modulare Programmierung wird mit einer API einfach, weil sie systematisch komplexe Informationen verbirgt, die nicht unbedingt benötigt werden, um Code nach Industriestandards zu schreiben. Zum Beispiel kann eine API die Schnittstelle zwischen einer Anwendung (wie Python oder *Word*) und einem **Betriebssystem** (**OS**) wie *Windows*, *Linux* oder *macOS* (auch als **Plattform** bezeichnet) definieren.

Ein **IDE** ermöglicht die Definition eines Projekts, das beispielsweise eine bestimmte Python-Umgebung verwendet, und es ermöglicht eine robuste Codierung, indem es Probleme direkt im Code aufzeigt, noch bevor es zum ersten Mal ausgeführt wird. Leistungsstarke IDEs gehen noch weiter und helfen, den Code mit Markdown (*.md* Dateien) zu dokumentieren und direkt in *git* zu pipen (siehe {ref}`chpt-git`).

```{admonition} Which IDE to choose?
:class: tip
Die Antwort auf diese Frage hängt von der Plattform ab, die Sie verwenden (z. B. * Windows * oder * Linux *), Ihren persönlichen Vorlieben und Ihren Zielen.

For writing Python software itself, {ref}`PyCharm <pycharm>` is a powerful solution. In addition, {ref}`Jupyter <jupyter>` is a great tool for writing word-office-like documents with functional code examples. To test and run Python code (software) locally,  for ***Windows* users, the installation of {ref}`anaconda` is almost indispensable**. *Linux* users will be mostly fine with their system setup without the need to install *Anaconda*.

For code documentation, examples, and the best learning experience in the Python courses featured in this eBook, consider installing {ref}`jupyter` locally. *Windows* users find instructions in the {ref}`install-jupyter-windows` section. *Linux* users find instructions in the {ref}`install-jupyter-linux` section.

**Sobald Sie eine IDE installiert haben, lesen Sie sorgfältig die {ref}`instructions for installing Python <install-python>`.**
```

(anaconda)=
# Anaconda

***Anaconda* ist ein leistungsstarkes Tool zum Verwalten von Python-Umgebungen unter Windows. Linux-Benutzer nutzen virtuelle Umgebungen besser** (lesen Sie mehr im Kapitel {ref}`installing Python <install-python>`).

## Anaconda Navigator

*Anaconda* ist eine Python- und *R*-Distribution, die die Verwendung einiger IDEs wie [PyCharm](https://www.jetbrains.com/pycharm/), [Spyder](https://www.spyder-ide.org/) oder [JupyterLab (Notebook)](https://jupyter.org/)] ermöglicht.

Der erste Schritt, um mit Anaconda zu beginnen, besteht darin, [Anaconda](https://www.anaconda.com/download)] herunterzuladen und zu installieren, wo Studenten die individuelle Lizenz für Bildungszwecke verwenden können (beachten Sie, dass eine kommerzielle Lizenz für gemeinnützige Organisationen erworben werden muss). Unter Windows sollte Anaconda im Benutzerordner *LOCAL* installiert sein (z. B. *C:\users\<your-user-name>\AppData\Local*). *Linux* oder *macOS* Benutzer finden Download- und Installationsanweisungen direkt auf der Website des Entwicklers, die auf ihre spezifische Verteilung zugeschnitten sind, auch wenn sie mit {ref}`virtual environments <pip-env>` besser dran sind.

Nach der erfolgreichen Installation von *Anaconda* können IDEs für die Python-Programmierung oder *Markdown*-Bearbeitung direkt installiert werden, indem der **Anaconda-Navigator** gestartet wird. **`conda`**-Umgebungen können später erstellt werden. Erfahren Sie mehr über die Installation von Anaconda (mit Python) und das Support-Paket dieses eBooks mit dem Namen [flusstools](https://flusstools.readthedocs.io) im {ref}`Python conda quick guide <conda-quick>`-Bereich und im Video unten].

```{admonition} Python Anaconda Installation Video on YouTube
:class: tip, dropdown
<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/cbIPRGOUAVA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@hydroinformatics on YouTube</a>.</p>
```

## Miniconda

*Anaconda* kann große Umgebungen verursachen, die mehrere Gigabyte Speicherplatz erfordern. Um leichte Umgebungen zu installieren, verwenden Sie [Miniconda](https://docs.anaconda.com/miniconda/). *Miniconda* enthält nicht *Anaconda Navigator* und aktivieren Sie das Arbeiten mit *Jupyter* Notebooks (in *Windows*):

1. Klicken Sie auf *Start*.
1. Geben Sie `Anaconda Prompt` ein und drücken Sie Enter (verwenden Sie *Miniconda3*). Ein *Terminal* Fenster (schwarzer Hintergrund) öffnet sich.
1. In *Anaconda prompt * geben Sie `conda install jupyter` ein und bestätigen Sie mit `y`, wenn das *Terminal* `Proceed ([y]/n)?` fragt.

Um mit *Jupyter* Notizbüchern zu arbeiten (öffnen, erstellen oder ändern), geben Sie `jupyter lab` (oder `jupyter notebook`) in *Anaconda Prompt (Miniconda3)* ein und drücken Sie *Enter*. Die *JupyterLab*-Anwendung wird im Standard-Webbrowser geöffnet.

(pycharm)=
## PyCharm

*Jetbrains* [*PyCharm*](https://www.jetbrains.com/pycharm/)] ist eine leistungsstarke, aber proprietäre IDE. Seine Nutzung ist immer noch kostenlos für nicht-kommerzielle Nutzung in der Bildung. Alternativen sind [*Spyder IDE*](https://www.spyder-ide.org/) (für Python) oder [*RStudio*](https://posit.co/products/open-source/rstudio/) (*R* und Python). Vor dem Start eines Projekts in einer IDE ist jedoch die Installation eines Interpreters (z. B. Python oder *R*) erforderlich (siehe Kapitel unter {ref}`Python installation <install-python>`).

Get PyCharm from the [developer's website](https://www.jetbrains.com/pycharm/download/) or use it through Anaconda. For the educative training purposes provided in this eBook, you may be eligible to use the free education license. To use PyCharm with Anaconda, visit [https://docs.anaconda.com](https://docs.anaconda.com/free/anaconda/ide-tutorials/pycharm/).

(jupyter)=
# JupyterLabor

*Jupyter* ist ein Spin-off von [IPython](https://ipython.org/), was "eine reiche Architektur für interaktives Computing" ist. *JupyterLab* ist ein Produkt der gemeinnützigen Organisation [*Project Jupyter*](https://jupyter.org/)], die "Open-Source-Software, offene Standards und Dienste für interaktives Computing in Dutzenden von Programmiersprachen" entwickelt. Ein *Jupyter*-Notebook (*.ipynb*-Datei) ermöglicht die Kombination von Markdown-Textblöcken mit ausführbaren Codeblöcken. Im Wesentlichen ist ein Jupyter Notebook eine *JavaScript Object Notation * ([JSON](https://www.json.org/json-en.html) Datei]. Die Struktur von JSON-Dateien ermöglicht den einfachen Export von *.ipynb*-Notebooks in viele andere offene Standard-Ausgabeformate wie HTML, [LaTeX](https://latex-project.org/), *Markdown*, Python, Präsentationsfolien oder *PDF*. Die **Jupyter**-Kernel unterstützen die drei Kernprogrammiersprachen **Ju**lia, **Pyt**hon und **R** und viele weitere *Jupyter*-Kernel (weit über 100) für andere Programmiersprachen existieren.


```{admonition} Working with Jupyter
:class: tip
Get familiar with *JupyterLab*, by creating files, adding new *Markdown* or Python cells, and running cells. The essentials of *markdown* are explained in the {ref}`Markdown <markdown>` section (short read). Learning Python is more than a short read and the {ref}`Python Basics chapter <about-python>` provides some insights (takes time).
```

(install-jupyter-windows)=
## Jupyter auf Windows

Anaconda Navigator bietet alternativ die Anwendung Jupyter Notebook. *JupyterLab* ist jedoch die Benutzeroberfläche der nächsten Generation von *Project Jupyter*, die flexibler und leistungsfähiger ist. Aus diesem Grund bezieht sich diese Website eher auf JupyterLab als auf die Jupyter Notebook App. In den folgenden Abschnitten wird erläutert, wie Sie es auf Ihrem Windows-Computer installieren, entweder mithilfe der grafischen Benutzeroberfläche von Anaconda Navigator oder der Befehlszeile conda prompt (empfohlen).

### Über Anaconda Navigator

1. Öffnen Sie Anaconda Navigator und stellen Sie sicher, dass Sie sich auf der Registerkarte *Home* befinden.
1. Suchen Sie nach JupyterLab und klicken Sie auf die Schaltfläche *Installieren* (falls bereits installiert, ist nur eine Schaltfläche *Launch* sichtbar).
1. Öffnen Sie nach erfolgreicher Installation JupyterLab, indem Sie auf den Button *Launch* klicken.
1. JupyterLab wird im Standard-Webbrowser geöffnet, in dem Jupyter-Notebooks (*.ipynb*) oder Python-Dateien erstellt und bearbeitet werden können.


### Via Anaconda Prompt (empfohlen)

Öffnen Sie die Anaconda Prompt, die ein Terminalfenster mit schwarzem Hintergrund und einem blinkenden Cursor darstellt.

If you are working with *Miniconda*, install the Jupyter Notebook app by typing `conda install jupyter` and confirm with `y` when Anaconda Prompt asks `Proceed ([y]/n)?`.

Um JupyterLab zu starten und Jupyter-Notebooks zu öffnen, zu erstellen oder zu ändern, geben Sie Folgendes ein:

```
jupyter lab
```

Wenn der Befehl fehlschlägt, versuchen Sie entweder `jupyter-lab` oder starten Sie das Jupyter-Notebook, indem Sie `jupyter notebook` eingeben. Die *Jupyter Notebook * Anwendung wird im Standard-Webbrowser geöffnet.

### Erweiterungen und Spellchecker

Modern *JupyterLab* (version 4 and newer) supports prebuilt extensions that install directly with `pip` or `conda`. The old `jupyter labextension install` command and the `jupyter_contrib_nbextensions` package are deprecated and no longer work with current *JupyterLab* and *Notebook 7* releases (they also no longer require a separate *nodejs* build step).

Wenn Sie die Python-Tutorials auf dieser Website durchlesen, werden Sie wahrscheinlich den einen oder anderen Rechtschreibfehler finden (bitte <a href="mailto:sebastian.schwindt[AT]iws.uni-stuttgart.de?subject=hydroinformatics%20spelling%20mistake">Berichtsfehler!</a>). Insbesondere können die Python-Abschnitte betroffen sein, weil sie mit JupyterLab erstellt wurden, wo kein Rechtschreibprüfer vorinstalliert ist. Um zumindest die unangenehmsten Fehler zu vermeiden, können Sie eine Rechtschreibprüfung installieren. Eine bequeme Option ist [jupyterlab-spellchecker](https://github.com/jupyterlab-contrib/spellchecker), die nach einem Neustart von JupyterLab funktioniert (keine *nodejs* oder manueller Umbau erforderlich):

```
conda install -c conda-forge jupyterlab-spellchecker
```

Die Rechtschreibprüfung verwendet [Typo.js](https://github.com/cfinke/Typo.js)] als Wörterbuch und hebt falsch geschriebene Wörter in Markdown- und Codezellen hervor (ohne Korrekturen vorzuschlagen).

(install-jupyter-linux)=
## Jupyter auf Linux

Um JupyterLab unter Linux zu installieren, öffnen Sie das Terminal und stellen Sie sicher, dass `pip`/`pip3` installiert ist:

```
sudo apt install python3 python3-pip python3-venv
```

Exportieren Sie die Benutzerebene `bin` in die `PATH`-Umgebung und installieren Sie JupyterLab im Benutzerbereich mit den folgenden Befehlen:

```
export PATH="$HOME/.local/bin:$PATH"
pip install --user jupyterlab
```

```{note}
It might be necessary to replace `pip` with `pip3` (depending on the *Linux* distribution).
```

Zum Starten von JupyterLab tap:

```
jupyter-lab
```

Der Befehl `jupyter-lab` startet einen Localhost-Server, der JupyterLab ausführt und sich in einem Webbrowser wie eine interaktive Website öffnet.

```{warning}
Durch das Schließen von *Terminal* wird auch der localhost beendet, der JupyterLab ausführt. Schließen Sie das Terminal daher nicht, solange Sie mit JupyterLab arbeiten, insbesondere wenn nicht gespeicherte Bücher vorhanden sind.
```

## Ein Debugger für Jupyter

Um Codeabstürze besser zu verstehen und zu beheben, stellt ein Debugger eine große Erleichterung dar. Leider kann das Debuggen in Jupyter Kopfschmerzen verursachen, wenn kein inhärentes Debugging-Tool vorhanden ist. Um einen Debugger dazu zu bringen, mit Jupyter zu arbeiten, lesen Sie [diesen Blogeintrag von Jupyter Project](https://blog.jupyter.org/a-visual-debugger-for-jupyter-914e61716559)].


(install-sublime)=
# Sublim

Sublime ist einer der beliebtesten Editoren für mehrere (Computer-) Sprachen. Es handelt sich jedoch um kommerzielle Software, die nur während eines Bewertungszeitraums ohne zeitliche Begrenzung frei verwendet werden kann. Lesen Sie mehr darüber unter [sublimetext.com](https://www.sublimetext.com)].

Um es auf Debian Linux-Plattformen zu installieren, öffnen Sie Terminal und tippen Sie darauf (Quelle: https://www.sublimetext.com/docs):

```
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/sublimehq-archive.gpg
```

Wählen Sie dann den stabilen Kanal (der Dev-Kanal hat mehr Funktionen, aber auch mehr Bugs):

```
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
```

Finally, update `apt` and install Sublime:

```
sudo apt update
sudo apt install sublime-text
```

Wenn eine Fehlermeldung auftritt, stellen Sie sicher, dass `apt` mit `https` Quellen funktioniert:

```
sudo apt install apt-transport-https
```

When working with sublime, consider using an advanced spell check package, such as [LanguageTool](https://packagecontrol.io/packages/LanguageTool). More useful packages for sublime can be found at [packagecontrol.io](https://packagecontrol.io). Packages can also be found by hitting the `CTRL` + `Shift` + `P` keys (in Sublime) to open *Package Control*. Then, type `install` and enter the name of the package you are looking for in the box.

To enable modification of user settings, go to **Preferences** (top menu bar) > **Settings** and save the opening settings file either as `~./config/sublime-text/Packages/Default/Preferences.sublime-settings` (recommended for first-time saving) or  `~./config/sublime-text/Packages/User/Preferences.sublime-settings`. Then, edit the desired settings: for instance, look for `spell_check` and set it to `true` to default-enable spell checking. Save the `.sublime-settings` file to apply changes.

