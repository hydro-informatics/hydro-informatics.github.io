---
description: Umfassendes Git-Versionskontrolle Tutorial für Installation, Repositories, Verzweigung, Commiting, Pushing und Zusammenarbeit Workflows für Ingenieure und Wissenschaftler.
---

(chpt-git)=
# Versionskontrolle : git

## Das Konzept

**git ist ein schnelles, skalierbares, verteiltes Revisionssystem***, das ursprünglich von *Linus Torvalds* entwickelt wurde ([mehr zum git kernel](https://git.kernel.org/)). *git* ermöglicht die Koordination der Arbeit bei Mitarbeitern über die Programmierung hinaus, in jeder Menge von Dateien. Die Unterstützung nichtlinearer Workflows, Geschwindigkeit und Datenintegrität macht git zu einem unverzichtbaren Werkzeug in vielen Branchen und Forschungen. Bevor Sie beginnen, dieses *git* Tutorial zu lesen, werfen Sie einen Blick auf die schematisierte Funktion von Repositories, die mit *git* gehostet werden.

```{figure} ../img/git-scheme.png
:alt: git-scheme

Das Konzept von Git und Grundvokabular. Der REMOTE-Rahmen ist online (d.h. jemand anderen Computer) und der LOCAL-Rahmen ist das, was auf einem persönlichen Computer passiert, der mit dem Internet verbunden ist. Repositories können neu erstellt oder remote aufgerufen werden. Remote-Repositories können lokal kloniert, lokal verändert und lokale Änderungen können auf ein Remote-Repository verschoben werden. Mitarbeiter wollen sicherstellen, dass regelmäßig Änderungen eines Remote-Repositorys gezogen werden. Die Zusammenarbeit mit und auf verschiedenen Zweigen wird mit der Anzahl der Entwickler immer wichtiger (siehe Abschnitt über Zusammenarbeit und Zweige unten) und im Moment müssen wir uns nur daran erinnern, dass wir in der Hauptbranche (d.h. stromaufwärts / HEAD = main) arbeiten.
```

(dl)=
## Git installieren
Die mit diesem eBook bereitgestellten Materialien werden am besten heruntergeladen und mit *git*-fähigen Umgebungen aktualisiert (vermeiden Sie das Herunterladen von Materialien als *zip*-Datei).

`````{tab-set}
````{tab-item} Linux
Obwohl git eine integrale Funktion der meisten Linux-Distributionen ist, müssen Debian-Benutzer sie möglicherweise noch installieren. Dazu öffnen Sie Terminal und tippen Sie auf:
```
sudo apt install git
```
````

````{tab-item} Windows
Downloaden und installieren Sie [Git Bash](https://git-scm.com/downloads) und verwenden Sie diese zusammen mit einer IDE wie [PyCharms Community Edition](https://www.jetbrains.com/pycharm/) oder [VS Code](https://code.visualstudio.com/).
````

````{tab-item} macOS
macOS-Nutzer können [Homebrew](https://brew.sh/) für die Installation von git, aber es gibt andere Optionen, wie [Xcode](https://developer.apple.com/xcode/).

Um Homebrew für die Installation von git zu verwenden, starten Sie mit der Installation von Homebrew über die [macOS Terminal](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac):

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Die Installation von Homebrew kann eine Weile dauern. Nach der Installation stellen Sie sicher, dass Sie die benötigte PATH-Variable (Copy line-by-line) exportieren:

```
echo 'eval $(/opt/homebrew/bin/brew shellenv)' >> /Users/$USER/.zprofile
eval $(/opt/homebrew/bin/brew shellenv)
```

Möglicherweise müssen die Pfade in den obigen Befehlen an die Verzeichnisse angepasst werden, die der Homebrew-Installer am Ende seiner Installation anfordert.

Schließlich installieren Sie git mit Homebrew:

```
brew install git
```

Letztlich bietet Homebrew viele weitere Pakete, die im Wesentlichen für Entwickler nützlich sind, wie [ruby](https://formulae.brew.sh/formula/ruby) oder [React](https://formulae.brew.sh/formula/react-native-cli)([go to the full package list](https://formulae.brew.sh/formula/)].

Read more installation instructions and about options for git on macOS at [https://git-scm.com/download/mac](https://git-scm.com/download/mac).

````
`````

Die Repositories für diesen Kurs werden hauptsächlich auf *GitHub* gehostet. Es gibt viele andere *git*-Dienstleister, wie [GitLab](https://gitlab.com/), [plan.io](https://plan.io/knowledge-management/), oder [BitBucket](https://bitbucket.org/).


## Erstellen eines Repositorys

Um ein *git*-Repository zu erstellen, stellen Sie sicher, dass Sie Zugriff auf einen *git*-Anbieter haben. Die beliebteste Möglichkeit, Zugriff auf einen *git*-fähigen Server zu erhalten, ist, sich mit einem auf der langen Liste der beliebten *git*-Anbieter zu registrieren.

```{admonition} Students of the University of Stuttgart
:class: note
Studierende der Universität Stuttgart können *GitHub* mit ihrer institutionellen ID (z.B. `st9009133` ) über das [TIK's GitHub-Konto und Login page](https://github.tik.uni-stuttgart.de/login).
```

## Klonen (Download) ein Repository

*GitHub* bietet ausführliche Beschreibungen und Standardverfahren, um mit ihren Repositories zu arbeiten ([mehr](https://help.github.com/en/articles/cloning-a-repository)]). Das folgende "Rezept" führt durch den erstmaligen Download von *git* Materialien:

1. Öffnen Sie Ihren Favoriten *git*-fähige Befehlszeile:
    * *Windows* Optionen: *PowerShell*, *Git Bash* oder *Command Prompt*
    * *Linux*: *Terminal*
1. Clone the course repository (change materials according to the course attended):<br> `git clone https://github.com/hydro-informatics/materials`  (or whatever repository you want to clone)

Fertig.

(update)=
## Pull (Update/Re-Download) a Local Repository

*git* (innerhalb *Git Bash*, *PyCharm* oder *Terminal*) ist die einzige Möglichkeit, lokale Kopien eines Remote-Repositorys konsequent zu aktualisieren. Dazu öffnen Sie eine der oben genannten *git*-fähigen Befehlszeilen und tun Sie die folgenden:

1. Go to the local directory of the repository with the [`cd`](https://en.wikipedia.org/wiki/Cd_(command)) command (e.g., `materials`):<br> `cd "D:/Python/materials/"` (or wherever `materials` was cloned).
1. `git status` - zeigt die Änderungen.
1. Merge conflicts may occur when changes were made in the local copy. To keep the local history linear, type: <br> `git pull --rebase` - if locally edited files were modified remotely since the last pull, *git* will highlight problematic (conflicting) sections with `<<<<<<<`, `=======`, and `>>>>>>>` markers. Manually open the concerned files, resolve the conflicts, and delete the invalid conflict markers. Then mark the files as resolved with `git add FILENAME` and finalize with `git rebase --continue`.

Fertig.


(push)=
## Aktualisieren eines Remote Repository (Push Local Changes)

Nach der Bearbeitung von Dateien in einem Repository lokal, *add* - *commit* - *push* (in dieser Reihenfolge) Ihre Bearbeitungen auf die entfernte Kopie des Repository mit Versionskontrolle. Um *add* - *commit* - *push* lokale Änderungen in einem Remote-Repository, stellen Sie sicher, dass der Remote-Repository-Besitzer oder ein Beitragszahler. Dann öffnen Sie ein *git*-fähiges Terminal und geben Sie:
1. `git status` - dies zeigt die vorgenommenen Änderungen.
1. If the status only lists consciously made changes, type `git add .` <br>Alternatively, if only single files were changed, use `git add filename.py` instead. Best practice: exclude files that should never be tracked (e.g., temporary or large binary files) with a local [.gitignore file](https://help.github.com/en/github/using-git/ignoring-files).
1. Überlassen Sie die Änderungen mit `git commit -m "Leave a message"` - hinterlassen Sie eine signifikante und präzise Kurznachricht (z.B. `"fix typos in flow calculator"`).
1. `git pull --rebase` - Wenn lokal bearbeitete Dateien seit dem letzten Zug remote geändert wurden, wird *git* problematische (conflicting) Abschnitte mit `<<<<<<<`, `=======` und `>>>>>>>`Markern hervorheben. Öffnen Sie die betroffenen Dateien manuell, lösen Sie die Konflikte, löschen Sie die ungültigen Konfliktmarker, führen Sie dann `git add FILENAME` und `git rebase --continue`.
1. `git push`

````{admonition} Summary for updating a repository
:class: tip
Tippen Sie in Terminal oder GitBash auf, um alle Änderungen in einem lokalen Repository in das entfernte Repository hochzuladen (vergewissern Sie sich, in welchem Ordner sich Ihr Repository auf Ihrem Computer befindet - das definiert, was Sie für `/change-directory-to/repository/` eingeben müssen):

```
cd /change-directory-to/repository/
git status
git add .
git commit -m "Leave a commit message"
git pull --rebase
git push
```
````

Wenn ein Fehler auftritt, lesen Sie sorgfältig, warum der Fehler aufgetreten ist und folgen Sie den Anweisungen zur Fehlerbehebung (z.B. zur Einrichtung Ihrer Benutzerkonfiguration mit [git config --global user.email "email@example.com"](https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/managing-email-preferences/setting-your-commit-email-address#setting-your-commit-email-address-in-git)). Sie können Warnmeldungen über Zeilenendformate (*WARNING ... LF endet ...*) für die meisten Anwendungen in diesem eBook ignorieren.

(collaboration)=
## Zusammenarbeit und Branchen

As soon as more than one person works on a repository (or one person works on more than one feature), committing everything directly to the `main` branch becomes error-prone. Best practice is to keep `main` always in a working state and to develop new features, fixes, or experiments on dedicated **branches**. A branch is an independent line of development that starts as a copy of another branch (typically `main`) and can later be merged back.

### Eine Zweigstelle erstellen

Um einen neuen Zweig zu erstellen und darauf zu wechseln, öffnen Sie ein *git*-fähiges Terminal im lokalen Repository und geben Sie:

1. `git switch main` - Stellen Sie sicher, dass Sie von der `main` Filiale starten (ältere *git* Versionen benötigen `git checkout main`).
1. `git pull` - aktualisieren Sie die lokale `main`-Niederlassung, um eine Verzweigung eines veralteten Staates zu vermeiden.
1. `git switch -c fix-hydraulics-chapter` - erstellen und direkt an einen neuen Zweig wechseln (hier heißt `fix-hydraulics-chapter`; ältere *git*-Versionen benötigen `git checkout -b fix-hydraulics-chapter`). Verwenden Sie kurze, beschreibende Zweignamen wie `fix-typos-git-chapter` oder `feature-sediment-transport`.

`git branch` listet alle lokalen Zweige auf und markiert den derzeit aktiven Zweig mit einer `*`. Wechseln Sie zwischen bestehenden Zweigen mit `git switch BRANCH-NAME`.

### Ändern (Work on) a Branch

Die Arbeit an einer Branche ist genau der gleiche *add* - *commit* - *push* Workflow wie im Abschnitt {ref}`push` beschrieben, mit einem Unterschied: Der erste Push muss dem entfernten Repository über die neue Branche erzählen. So:

1. Dateien bearbeiten, dann `git status` und `git add .` (oder `git add filename.py`).
1. `git commit -m "Leave a message"` - begehen kleine, kohärente Arbeitseinheiten statt eines riesigen Auftrags am Ende.
1. `git push -u origin fix-hydraulics-chapter` - Die `-u`(upstream)-Flagge verbindet die lokale Filiale mit der abgelegenen Filiale, sodass alle späteren Updates nur eine einfache `git push` benötigen.

Um einen langjährigen Zweig mit fortschreitenden Entwicklungen in `main` auf dem Laufenden zu halten, geben Sie regelmäßig (mit dem Funktionszweig aktiv):

```
git fetch origin
git merge origin/main
```

Lösung möglicher Konflikte, wie im Abschnitt {ref}`update` beschrieben (hier mit `git commit` anstatt `git rebase --continue`).

### Kommentar und Bewertung (Pull Requests)

Direkte Verschmelzung einer eigenen Filiale ohne Überprüfungsarbeiten für Soloprojekte, aber in einem Team ist die beste Praxis, eine **pull-Anfrage** zu öffnen (*Merge-Anfrage* auf *GitLab*). Ein Pull-Antrag ist ein Vorschlag, einen Zweig in einen anderen zu überführen und stellt den zentralen Platz für die Anmerkung zum Code dar:

1. Drücken Sie den Zweig zum entfernten Repository (siehe oben).
1. Auf *GitHub* schlägt die Repository-Seite **Compare & Pull-Anfrage** für kürzlich geschobene Filialen vor. Alternativ gehen Sie auf die Registerkarte *Pull-Anfragen* und klicken Sie auf **Neue Ziehanforderung**, dann wählen Sie `main` als *base* und den Funktionsbereich (z.B. `fix-hydraulics-chapter`) als *compare*.
1. Geben Sie der Pull-Anfrage einen genauen Titel und beschreiben Sie **what** wurde geändert und **why**. Fordern Sie eine Bewertung von einem oder mehreren Mitarbeitern an (rechtes Menü auf *GitHub*).
1. Die Rezensatoren können die Pull-Anfrage als Ganzes (*Conversation* Tab) oder auf einzelnen Codezeilen (*Files geändert* Tab, Hover über eine Zeile und klicken Sie auf das `+` Symbol). Linienkommentare können auch mit den Urteilen *Comment*, *Approve* oder *Request-Änderungen* in eine formale Überprüfung gebündelt werden.
1. Um Kommentare zu überprüfen, begehen Sie einfach und drücken Sie neue Änderungen in der gleichen Branche. Die Pull-Anforderung aktualisiert sich automatisch, und die aufgelösten Diskussionen können als solche mit der **Resolve Gespräch* Taste markiert werden.

### Verschmelzung einer Entwicklungsabteilung ins Haupt

Sobald die Pull-Anfrage genehmigt ist (und automatisierte Checks passieren, falls konfiguriert), wenden Sie die neuen Entwicklungen an `main` an, indem Sie auf die **Merge Pull-Anfrage** Taste auf *GitHub* klicken. Darüber hinaus bietet *GitHub* *Squash and merge* (kombiniert alle Zweige verpflichtet sich zu einem einzigen Commit, das die Geschichte von `main` tidy) und *Rebase and merge* hält. Nach dem Zusammenfügen, löschen Sie den Zweig remote (*GitHub* schlägt eine **Delete branch** Taste) und lokal:

```
git switch main
git pull
git branch -d fix-hydraulics-chapter
```

Ohne eine *git*-Anbieter-Schnittstelle (z.B. für ein rein lokales Repository) kann ein Zweig auch manuell zusammengeführt werden:

1. `git switch main` - Wechsel in die Zielbranche.
1. `git pull` - stellen Sie sicher, dass die lokale `main`-Niederlassung aktuell ist (Skip für rein lokale Repositories).
1. `git merge fix-hydraulics-chapter` - Zusammenführen der Entwicklungszweig in `main`. Lösung möglicher Konflikte (siehe Abschnitt {ref}`update`), dann `git add` die aufgelösten Dateien und `git commit`.
1. `git push` - veröffentlichen Sie die aktualisierte `main`
1. `git branch -d fix-hydraulics-chapter` - Löschen Sie den vereinigten Zweig (*git* weigert sich an `-d`-delete Filialen mit unerreichten Änderungen, was ein nützliches Sicherheitsnetz ist).

Fertig.

````{admonition} Summary of a branch lifecycle
:class: tip
```
git switch main
git pull
git switch -c feature-name
# edit files, then repeatedly:
git add .
git commit -m "Describe the change"
git push -u origin feature-name
# open a pull request on GitHub, discuss, revise, and merge; finally:
git switch main
git pull
git branch -d feature-name
```
````

```{admonition} Exercise
Praxis *git* mit der {ref}`markdown and git <git-exercise>` Übung.
```
