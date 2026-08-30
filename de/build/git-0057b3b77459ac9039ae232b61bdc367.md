---
description: Umfassendes Git-Versionskontroll-Tutorial für Installation, Repositories, Verzweigung, Committing, Push und kollaborative Workflows für Ingenieure und Wissenschaftler.
---

(chpt-git)=
# Versionskontrolle: git

## Das Konzept

**git ist ein schnelles, skalierbares, verteiltes Revisions- (Versions-) Kontrollsystem**, das ursprünglich von *Linus Torvalds* entwickelt wurde ([lesen Sie mehr über den git kernel](https://git.kernel.org/)]. *git* ermöglicht die Koordination der Arbeit zwischen Mitarbeitern über die Programmierung hinaus in beliebigen Dateien. Die Unterstützung von nichtlinearen Workflows, Geschwindigkeit und Datenintegrität macht git zu einem unverzichtbaren Werkzeug in vielen Branchen und in der Forschung. Bevor Sie mit dem Lesen dieses *git* Tutorials beginnen, werfen Sie einen Blick auf die schematische Funktionsweise von Repositories, die mit *git* gehostet werden.

```{figure} ../img/git-scheme.png
:alt: git-scheme

Das Konzept von Git und Grundvokabular. Der REMOTE-Rahmen ist online (dh der Computer einer anderen Person) und der LOCAL-Rahmen ist das, was auf einem Personal Computer passiert, der mit dem Internet verbunden ist. Repositories können aus der Ferne neu erstellt oder gegabelt werden. Remote-Repositories können lokal geklont, lokal geändert und lokale Änderungen in ein Remote-Repository verschoben werden. Mitarbeiter möchten sicherstellen, dass regelmäßig Änderungen an einem entfernten Repository vorgenommen werden. Die Arbeit mit und an verschiedenen Zweigen wird mit der Anzahl der Entwickler immer wichtiger (siehe den Abschnitt über Zusammenarbeit und Zweige unten) und im Moment müssen wir uns nur daran erinnern, dass wir im Hauptzweig arbeiten (dh Upstream Origin / HEAD = Main).
```

(dl)=
## Installieren git
Die mit diesem eBook bereitgestellten Materialien werden am besten mit *git*-fähigen Umgebungen heruntergeladen und aktualisiert (Vermeiden Sie das Herunterladen von Materialien als *zip*-Datei).

`````{tab-set}
````{tab-item} Linux
Obwohl Git ein integrales Merkmal der meisten Linux-Distributionen ist, müssen Debian-Benutzer es möglicherweise noch installieren. Zu diesem Zweck öffnen Terminal und tippen:
```
sudo apt install git
```
````

````{tab-item} Windows
Laden Sie [Git Bash](https://git-scm.com/downloads)] herunter und installieren Sie es zusammen mit einer IDE wie [PyCharm's Community Edition](https://www.jetbrains.com/pycharm/) oder [VS Code](https://code.visualstudio.com/)].
````

````{tab-item} macOS
macOS-Benutzer können [Homebrew](https://brew.sh/)] für die Installation von git verwenden, aber es gibt andere Optionen wie [Xcode](https://developer.apple.com/xcode/)].

Um Homebrew für die Installation von git zu verwenden, beginnen Sie mit der Installation von Homebrew über das [macOS Terminal](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac)]:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Die Installation von Homebrew kann eine Weile dauern. Stellen Sie nach der Installation sicher, dass Sie die erforderliche PATH-Variable exportieren (Zeilenweise kopieren):

```
echo 'eval $(/opt/homebrew/bin/brew shellenv)' >> /Users/$USER/.zprofile
eval $(/opt/homebrew/bin/brew shellenv)
```

Es kann möglich sein, dass die Pfade in den oben genannten Befehlen an die Verzeichnisse angepasst werden müssen, die der Homebrew-Installer am Ende seiner Installation anfordert.

Installieren Sie schließlich Git mit Homebrew:

```
brew install git
```

Letztendlich bietet Homebrew viele weitere Pakete, die für Entwickler von grundlegender Bedeutung sind, wie [ruby](https://formulae.brew.sh/formula/ruby) oder [React](https://formulae.brew.sh/formula/react-native-cli)] (Gehen Sie zur vollständigen Paketliste](https://formulae.brew.sh/formula/)).

Read more installation instructions and about options for git on macOS at [https://git-scm.com/download/mac](https://git-scm.com/download/mac).

````
`````

Die Repositories für diesen Kurs werden hauptsächlich auf *GitHub* gehostet. Es gibt viele andere *git * Dienstleister da draußen, wie [GitLab](https://gitlab.com/), [plan.io](https://plan.io/knowledge-management/), oder [BitBucket](https://bitbucket.org/)].


## Erstellen Sie ein Repository

Um ein *git*-Repository zu erstellen, stellen Sie sicher, dass Sie Zugriff auf einen *git*-Anbieter haben. Der beliebteste Weg, um Zugang zu einem *git*-fähigen Server zu erhalten, ist die Registrierung bei einem auf der langen Liste der beliebten *git*-Anbieter.

```{admonition} Students of the University of Stuttgart
:class: note
Students of the University of Stuttgart may use *GitHub* using their institutional ID (e.g., `st9009133` ) through the [TIK's GitHub account and login page](https://github.tik.uni-stuttgart.de/login).
```

## Clone (Download) ein Repository

*GitHub* bietet detaillierte Beschreibungen und Standardprozeduren für die Arbeit mit ihren Repositories ([lesen Sie mehr](https://help.github.com/en/articles/cloning-a-repository)]. Der folgende "Rezept" führt durch den erstmaligen Download von *git* Materialien:

1. Öffnen Sie Ihre favorisierte *git*-fähige Kommandozeile:
    * *Windows* Optionen: *PowerShell*, *Git Bash* oder *Command Prompt*
    * *Linux*: *Terminal*
1. Clone the course repository (change materials according to the course attended):<br> `git clone https://github.com/hydro-informatics/materials`  (or whatever repository you want to clone)

Geschehen.

(update)=
## Pull (Update/Re-Download) ein lokales Repository

*git* (innerhalb von *Git Bash*, *PyCharm* oder *Terminal*) ist die einzige Option, um lokale Kopien eines Remote-Repositorys konsistent zu aktualisieren. Öffnen Sie dazu eine der oben genannten *git*-fähigen Befehlszeilen und führen Sie Folgendes aus:

1. Go to the local directory of the repository with the [`cd`](https://en.wikipedia.org/wiki/Cd_(command)) command (e.g., `materials`):<br> `cd "D:/Python/materials/"` (or wherever `materials` was cloned).
1. `git status` - shows the modifications made.
1. Merge conflicts may occur when changes were made in the local copy. To keep the local history linear, type: <br> `git pull --rebase` - if locally edited files were modified remotely since the last pull, *git* will highlight problematic (conflicting) sections with `<<<<<<<`, `=======`, and `>>>>>>>` markers. Manually open the concerned files, resolve the conflicts, and delete the invalid conflict markers. Then mark the files as resolved with `git add FILENAME` and finalize with `git rebase --continue`.

Geschehen.


(push)=
## Aktualisieren eines Remote-Repositorys (Push Local Changes)

Nachdem Sie Dateien in einem Repository lokal bearbeitet haben, *add* - *commit* - *push* (in dieser Reihenfolge) Ihre Bearbeitungen in die Remotekopie des Repository mit Versionskontrolle. Um lokale Änderungen an einem Remote-Repository hinzuzufügen * - * zu übertragen * - * zu drücken *, stellen Sie sicher, dass Sie der Eigentümer des Remote-Repositorys oder ein Mitwirkender sind. Öffnen Sie dann ein *git*-fähiges Terminal und geben Sie ein:
1. `git status` - this shows the modifications made.
1. If the status only lists consciously made changes, type `git add .` <br>Alternatively, if only single files were changed, use `git add filename.py` instead. Best practice: exclude files that should never be tracked (e.g., temporary or large binary files) with a local [.gitignore file](https://help.github.com/en/github/using-git/ignoring-files).
1. Commit the changes with `git commit -m "Leave a message"` - leave a significant and precise short message (e.g., `"fix typos in flow calculator"`).
1. `git pull --rebase` - Wenn lokal bearbeitete Dateien seit dem letzten Zug aus der Ferne geändert wurden, hebt *git* problematische (widersprüchliche) Abschnitte mit `<<<<<<<`, `=======` und `>>>>>>>`markern hervor. Manuelles Öffnen der betroffenen Dateien, lösen Sie die Konflikte, löschen Sie die ungültigen Konfliktmarker und führen Sie dann `git add FILENAME` und `git rebase --continue` aus.
1. `git push`

````{admonition} Summary for updating a repository
:class: tip
Tap the following in Terminal or GitBash to upload all modifications in a local repository to the remote repository (make sure to know in which folder your repository is located on your computer - this defines what you need to enter for `/change-directory-to/repository/`):

```
cd /change-directory-to/repository/
git status
git add .
git commit -m "Leave a commit message"
git pull --rebase
git push
```
````

Wenn ein Fehler auftritt, lesen Sie sorgfältig, warum der Fehler aufgetreten ist, und befolgen Sie die Anweisungen zur Fehlerbehebung (z. B. zum Einrichten Ihrer Benutzerkonfiguration mit [git config --global user.email "email@example.com"](https://docs.github.com/en/github/setting-up-and-managing-your-github-user-account/managing-email-preferences/setting-your-commit-email-address#setting-your-commit-email-address-in-git)]. Sie können Warnmeldungen bezüglich Zeilenendformaten (*WARNUNG ... LF-Endungen ...*) für die meisten in diesem eBook vorgestellten Anwendungen ignorieren.

(collaboration)=
## Zusammenarbeit & Branchen

As soon as more than one person works on a repository (or one person works on more than one feature), committing everything directly to the `main` branch becomes error-prone. Best practice is to keep `main` always in a working state and to develop new features, fixes, or experiments on dedicated **branches**. A branch is an independent line of development that starts as a copy of another branch (typically `main`) and can later be merged back.

### Erstellen Sie einen Branch

Um einen neuen Branch zu erstellen und zu diesem zu wechseln, öffnen Sie ein *git*-fähiges Terminal im lokalen Repository und geben Sie Folgendes ein:

1. `git switch main` - stellen Sie sicher, dass Sie vom `main`-Zweig aus starten (ältere *git*-Versionen erfordern `git checkout main`).
1. `git pull` - Aktualisieren Sie den lokalen `main` Branch, um zu vermeiden, dass ein veralteter Zustand abgezweigt wird.
1. `git switch -c fix-hydraulics-chapter` - erstellen und direkt zu einem neuen Branch wechseln (hier `fix-hydraulics-chapter`; ältere *git* Versionen erfordern `git checkout -b fix-hydraulics-chapter`). Verwenden Sie kurze, beschreibende Zweignamen wie `fix-typos-git-chapter` oder `feature-sediment-transport`.

`git branch` lists all local branches and marks the currently active branch with a `*`. Switch between existing branches with `git switch BRANCH-NAME`.

### Ändern (arbeiten an) einem Branch

Die Arbeit an einem Branch ist genau derselbe *add* - *commit* - *push* Workflow wie im {ref}`push`-Abschnitt beschrieben, mit einem Unterschied: Der erste Push muss dem entfernten Repository den neuen Branch mitteilen. Somit:

1. Bearbeiten Sie Dateien, dann `git status` und `git add .` (oder `git add filename.py`).
1. `git commit -m "Leave a message"` - Begehen Sie kleine, kohärente Arbeitseinheiten anstelle eines riesigen Begehens am Ende.
1. `git push -u origin fix-hydraulics-chapter` - das `-u` (Upstream)-Flag verbindet den lokalen Zweig mit dem entfernten Zweig, so dass alle späteren Updates nur ein einfaches `git push` erfordern.

Um einen langlebigen Branch mit den laufenden Entwicklungen in `main` auf dem Laufenden zu halten, geben Sie regelmäßig ein (mit aktivem Feature Branch):

```
git fetch origin
git merge origin/main
```

Resolve possible conflicts as described in the {ref}`update` section (here, conclude with `git commit` rather than `git rebase --continue`).

### Kommentar und Review (Pull Requests)

Die direkte Zusammenführung einer eigenen Niederlassung ohne Review funktioniert für Solo-Projekte, aber in einem Team besteht Best Practice darin, eine **Pull-Anfrage zu öffnen (genannt * Merge Request* auf *GitLab*). Eine Pull Request ist ein Vorschlag, einen Branch in einen anderen zu verschmelzen und stellt den zentralen Ort für den Kommentar zum Code dar:

1. Drücken Sie den Branch zum Remote-Repository (siehe oben).
1. Auf *GitHub* schlägt die Repository-Seite **Compare & Pull Request** für kürzlich geschobene Branchs vor. Alternativ gehen Sie auf die Registerkarte *Pull Requests* und klicken Sie auf **New Pull Request**, dann wählen Sie `main` als *base* und den Feature Branch (z.B. `fix-hydraulics-chapter`) als *vergleichen*.
1. Geben Sie der Pull-Anfrage einen genauen Titel und beschreiben Sie **was ** geändert wurde und **warum **. Fordern Sie eine Bewertung von einem oder mehreren Mitarbeitern an (rechtes Menü auf *GitHub*).
1. Rezensenten können die Pull-Anfrage als Ganzes (*Konversation*-Tab) oder einzelne Codezeilen kommentieren (*Akten geändert*-Tab, bewegen sich über eine Zeile und klicken auf das `+`-Symbol). Zeilenkommentare können auch zu einer formellen Überprüfung mit den Urteilen *Kommentar *, *Genehmigen * oder *Anforderungsänderungen * zusammengefasst werden.
1. Um Review-Kommentare zu bearbeiten, müssen Sie einfach neue Änderungen an demselben Branch vornehmen und verschieben. Die Pull-Anfrage wird automatisch aktualisiert, und gelöste Diskussionen können als solche mit dem **Resolve conversation**-Button markiert werden.

### Zusammenführung eines Entwicklungszweigs in Main

Sobald die Pull-Anfrage genehmigt wurde (und automatisierte Überprüfungen bestehen, falls konfiguriert), wenden Sie die neuen Entwicklungen auf `main` an, indem Sie auf die Schaltfläche **Merge Pull Request** auf *GitHub* klicken. Darüber hinaus bietet *GitHub* *Squash und Merge* an (kombiniert alle Branch-Commits zu einem einzigen Commit, der die Historie von `main` ordentlich hält) und *Rebase und Merge*. Nach dem Zusammenführen löschen Sie den Branch aus der Ferne (*GitHub* schlägt eine **Abzweig**-Taste vor) und lokal:

```
git switch main
git pull
git branch -d fix-hydraulics-chapter
```

Ohne eine *git* Provider-Schnittstelle (z.B. für ein rein lokales Repository) kann ein Branch auch manuell zusammengeführt werden:

1. `git switch main` - Wechsel zum Zielzweig.
1. `git pull` - stellen Sie sicher, dass die lokale `main`-Niederlassung auf dem neuesten Stand ist (überspringen Sie für rein lokale Repositorys).
1. `git merge fix-hydraulics-chapter` - Fügen Sie den Entwicklungszweig zu `main` zusammen. Lösen Sie mögliche Konflikte (siehe {ref}`update`), dann `git add` die gelösten Dateien und `git commit`.
1. `git push` - veröffentlichen Sie den aktualisierten `main` Zweig.
1. `git branch -d fix-hydraulics-chapter` - delete the merged branch (*git* refuses to `-d`-delete branches with unmerged changes, which is a useful safety net).

Geschehen.

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
Practice *git* with the {ref}`markdown and git <git-exercise>` exercise.
```
