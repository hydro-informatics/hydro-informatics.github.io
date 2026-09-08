---
description: Leitfaden zur Dokumentation von Code und Projekten mit Markdown, Wikis und reStructuredText, einschließlich Best Practices für README-Dateien, Codedokumentation und GitHub-Repositories.
---

# Wie Markdown und Dokument

## Dokumentieren Sie Ihre Arbeit
Leonardo Da Vinci benutzte Zeitschriften, um seine Ideen zu skizzieren, zu entwickeln und schließlich weiterzugeben. Alexander von Humboldt dokumentierte viele seiner Reisen in Reisezeitschriften und Marie Skłodowska Curie schrieb die Theorie der "Radioaktivität" mit Stiften und Papieren auf. Heute haben sich Schreibmedien zu unendlichen digitalen Ozeanen mit ausgeklügelten Werkzeugen zur Dokumentation von Code und Ideen entwickelt. Auch die art und weise, wie wir nach informationen suchen und abrufen, hat sich von der suche nach lexikoneinträgen zur verwendung von keywords in suchmaschinen entwickelt.
Wenn Sie also eine geniale Entdeckung gemacht haben, möchten Sie sicherstellen, dass Sie sie gut dokumentieren, damit andere sie verstehen und verwenden können. Sie möchten auch sicherstellen, dass andere Ihren Geniestreich in digitalen Medien finden können. Sie möchten auch sicherstellen, dass andere Ihren Geniestreich in digitalen Medien finden können. Eine der am weitesten verbreiteten Methoden zur Dokumentation und Verbreitung von Ideen ist die Verwendung von sogenannten Wikis (von Hawaiianisch: *fast*), die leicht in Markdown-Sprache geschrieben werden können. *GitHub* bietet umfassende, leicht lesbare Erklärungen für [Projektdokumentation](https://guides.github.com/features/wikis/) mit *Markdown* als Kernelement]. Diese Seite präsentiert die Grundlagen der Markdown-Sprache, um Wikis zu nutzen. Darüber hinaus wird die leistungsstarke Alternative zur Verwendung von *reStructuredText* in *Sphinx*-basierten Dokumentationen eingeführt.


```{tip}
[Schreiben Sie die Docs](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/) bietet umfassende Anleitungen für die Code-Dokumentation.] Nehmen Sie sich etwa 10 Minuten Zeit, um zu lesen, wie Sie Arbeitstage sparen können.
```


## Was zu dokumentieren?

Eine gute Codedokumentation beginnt mit einer qualitativen und prägnanten Beschreibung der Softwarekapazitäten, -produkte und -anforderungen (z. B. eines *Python*-Pakets). Es bietet auch Workflows für die Installation und Verwendung der Software, bestenfalls mit illustrativen Beispielen. Schließlich ermöglicht ein guter Abschnitt zur Fehlerbehebung Benutzern, Probleme bei der Dateneinrichtung oder der Softwarenutzung zu finden. Um zukünftige Entwicklung und Wartung zu ermöglichen, enthält ein *Beitragen*-Abschnitt * Good-Practice-Richtlinien* für die Codierung neuer Softwarekapazitäten.

### Präsentieren Sie Ihre Software oder Projekt

In diesem Abschnitt sollen die Vorteile und Kapazitäten der Software bekannt gemacht werden: Sagen Sie den Benutzern kurz den Zweck der Software, warum sie einzigartig ist und was sie produziert.

### Anforderungen

Ein Abschnitt über Anforderungen sollte den Nutzern oder Interessengruppen mitteilen:

* Welche Systemanforderungen sind erforderlich?
* Welche Abhängigkeiten hat die Software oder das Projekt (z.B. andere *Python*-Pakete wie {ref}`numpy`)?
* Welche Eingabedaten werden für den Betrieb der Software benötigt?

### Installation

Ein Installationsabschnitt sollte Schritt für Schritt die Installation der Software (z. B. das Herunterladen und Zugreifen auf Ihr *Python*-Paket) oder den Workflow eines Projekts beschreiben. Screenshots können hilfreich sein. Der Abschnitt *Anforderungen* sollte bereits geklärt haben, was Benutzer für die Installation benötigen.

### Nutzung

Ein Abschnitt über die Verwendung sollte beschreiben, wie die Software verwendet werden kann, beginnend mit Grundlagen wie dem Importieren der Software als * Python * Paket. Darüber hinaus sollten mögliche Behandlungen von Input- und Outputdaten (d. h. Vor- und Nachverarbeitung) erwähnt werden. Wenn verfügbar, fügen Sie komplexere Funktionalitäten nacheinander in einer logischen Reihenfolge hinzu.

Um Ihre Software wirklich nützlich für andere zu machen, fügen Sie eine Fallstudie hinzu. Die meisten Benutzer werden die detaillierte Codedokumentation nicht lesen, bis sie die Software einmal laufen lassen und sehen, was sie tun kann. Ein Anwendungsfall hilft auch, die Logik Ihres Codes zu überprüfen und gibt Benutzern die Möglichkeit, unvollkommene Codedokumentationsabschnitte mit ihrem Workflow zu verbinden. Dies kann manchmal notwendig sein, auch wenn Ihr Code sicherlich perfekt ist und die Dokumentation narrensicher ist.

### Fehlerbehebung

Sure, your code and workflow are error-free and of course, only the user makes mistakes. Anyway, show compassion and integrate specific {ref}`try-except` statements in the source code, which point out possible error sources. These error (and maybe even warning) messages should all be listed in a *Troubleshoot* section of the code documentation. Any source of error (message) should be documented regarding the following aspects:

* Ursache: Mögliche Gründe, warum ein Fehler auftritt.
* Abhilfe: Schritte zur Fehlerbehebung.

### Beitrag

Your software is brilliant. To make the software even more brilliant, foolproof, and powerful, it is a great idea (actually: an absolute must) to get more authors on the development team. However, any other author likely has individual preferences when it comes to code standards. So make sure to set up clear rules for other contributors from the beginning. For example, define clear code conventions as explained in the {ref}`chpt-style` section.

(markdown)=
## Markdown

Um eine Dokumentation eines Codes oder Projekts im Web-Publish-ready-Format zu schreiben, ist ein plattformübergreifender Schriftsatz erforderlich. Zu diesem Zweck stellt *Markdown* eine gute Wahl dar (unter anderem {ref}`reStructuredText <rst>`). *Markdown* wurde 2004 erstellt und ist eine einfache Auszeichnungssprache, die intuitiv und einfach zu erlernen ist. Markup-Sprachen strukturieren den Inhalt von Klartextdokumenten in Bezug auf die Art und Weise, wie ein Dokument für Endbenutzer angezeigt wird ({term}`Rich Text Format`). Andere beliebte Auszeichnungssprachen sind zum Beispiel [TeX](https://en.wikipedia.org/wiki/TeX) und [XML (Extensible Markup Language)](https://en.wikipedia.org/wiki/XML)]. *Markdown* wurde zu einem beliebten Werkzeug, um syntaktisch unterscheidbaren Computertext zu schreiben, der dann in {term}`Rich Text Format` Geschmack übersetzt wird. Hier ist ein Beispiel dafür, wie *Markdown* funktioniert:

`````{tab-set}
````{tab-item} Raw Markdown
```markdown
# Better than Word-like rich text editors
*OS*-independent functionality:
- Avoid formatting of the same kind of thing redundantly (and inconsistently)
- Backwards compatibility
- Formulae handling
- ... and many more ...
```
````

````{tab-item} Rendered
** Besser als Word-like Rich Text Editoren **

*OS*-unabhängige Funktionalität:
- Vermeiden Sie Formatierung der gleichen Art von Sache redundant (und inkonsistent)
- Rückwärtskompatibilität
- Formelhandling
- ... und viele mehr ...

````
`````


### Markdown Editoren (IDEs)

Viele Text-Editoren bieten *Markdown* Add-ons und *Markdown*-nur Editoren verlieren ihre Bedeutung mehr und mehr. Editoren, die gleichzeitig *Markdown* und Programmiersprachen wie *Python* oder *R* unterstützen, sind State of the Art und werden daher empfohlen.

Basic text editors that support *Markdown* are listed {ref}`here <npp>`. Popular and multi-platform *IDE*s for editing *Markdown* (`.md`) files are {ref}`jupyter` or {ref}`pycharm`.

### Markdown Command Übersicht und Image Implementierung

The following table and sections provide an overview of basic markdown commands. There are much more options out there, which you can find by using your favorite search engine with the keywords `markdown` `guide`.

| Feature                | Code                            | Example          |
|:-----------------------|:--------------------------------|:-----------------|
| Blockquote             | `|     A quote`                 | `|`      A quote |
| Bold text              | `**Bold**`                      |   **Bold**       |
| Code block (inline)    | `inline` `` `code`  ``          | inline `` `code`  `` |
| Heading 1              | `# Heading 1`                   |  **Heading 1**   |
| Heading 2              | `## Heading 2`                  |  **Heading 2**   |
| Heading 3              | `### Heading 3`                 | ***Heading 3***  |
| Horizontal rule        | `***` or `===`                  |  -------         |
| Hyperlink              | `[Link](https://fruitsinfo.com)`|[Link](https://fruitsinfo.com)|
| Hyperlink to section   | `[Link](https://fruitsinfo.com)#apples` | [Link to apple-section](https://fruitsinfo.com) |
| Image                  | `![ImgName](https://image-address/image.png)` | ![ImgName](../img/icons/icon2small.jpg)|
| Italic text            | `*italic*`                      |  *italic*        |
| Numbered list item     | `1. numbered item`              | 1. Numbered item |
| Reference (defined)    | `[Defined Reference][wiki]`     |  [Defined Reference][wiki]  |
| Reference (definition) | `[wiki]: https://wikipedia.org` |   *Place at file bottom*               |
| Strikethrough | `~~Strikethrough~~ ` | ~~Strikethrough~~    |

### Itemisierung (nicht nummerierte Listen)

Eingeteilter Listenabschnitt kann mit `*`, `+` oder `-` Symbolen mit Registerkarten erstellt werden, die die Listeneinrückung bestimmen:

`````{tab-set}
````{tab-item} Raw Markdown
```markdown
* level 1 item
    - level 2 item
    - another level 2 item
        + level 3 item
* next level 1 item
```
````

````{tab-item} Rendered

* Stufe 1
    - Stufe 2
    - ein weiterer Level 2-Posten
        + Stufe 3
* Next Level 1 Posten

````
`````

### Tabellen

Table columns are separated by a `|` sign. The first row determines row headers and the second row the alignment through the use of `:` (see below example).

`````{tab-set}
````{tab-item} Raw Markdown
```markdown
| Fruit | Kingdom | Genus |
|-------|:-------:|------:|
|Banana | Plantae | Musa  |
|Jackfruit|Plantae|Artocarpus|
```
````

````{tab-item} Rendered

Obst | Königreich | Genus
|----------------------------------------------------------
Banane, Plantae, Musa
|Jackfruit|Plantae|Artocarpus

````
`````

Converting complex tables from workbooks (e.g., from *LibreOffice Calc* or *MS Excel*) is possible with many online tools, and here is just one example from Dave Johnson: [https://thisDaveJ.com](https://thisdavej.com/copy-table-in-excel-and-paste-as-a-markdown-table/).

### Mathe-Ausdrücke: Gleichungen

Mathematikausdrücke und Gleichungen können mit $-Zeichen implementiert werden, ähnlich wie *LaTeX *.

## Html — Markdown
*html*-Strukturen können in *Markdown* einwandfrei verwendet werden, was selbst nichts anderes ist als vereinfacht *html*. Daher kann jede *html * -Struktur innerhalb von Markdown verwendet werden, und die oben gezeigte Gleichungsimplementierung stellt bereits das erste Beispiel für die *html * -Nutzung in einem *Markdown * -Dokument dar. Die folgenden Abschnitte geben einen Überblick über einige mehr oder weniger häufig verwendete *html*-Symbole, die auch mit *Markdown* funktionieren.

### Griechische Briefe

To use greek letters in inline text, use *html* language, where `&lettername;` produces the desired *Greek* letter symbol (e.g., type `&delta;` to output &delta; or `&Delta;` to output a capital letter &Delta;). The following table provides an overview of Greek letter symbols.

| Letter    | Code        | letter    | code        |
|-----------|-------------|-----------|-------------|
| &Alpha;   | `&Alpha;`   | &alpha;   | `&alpha;`   |
| &Beta;    | `&Beta;`    | &beta;    | `&beta;`    |
| &Gamma;   | `&Gamma;`   | &gamma;   | `&gamma;`   |
| &Delta;   | `&Delta;`   | &delta;   | `&delta;`   |
| &Epsilon; | `&Epsilon;` | &epsilon; | `&epsilon;` |
| &Zeta;    | `&Zeta;`    | &zeta;    | `&zeta;`    |
| &Eta;     | `&Eta;`     | &eta;     | `&eta;`     |
| &Theta;   | `&Theta;`   | &theta;   | `&theta;`   |
| &Iota;    | `&Iota;`    | &iota;    | `&iota;`    |
| &Kappa;   | `&Kappa;`   | &kappa;   | `&kappa;`   |
| &Lambda;  | `&Lambda;`  | &lambda;  | `&lambda;`  |
| &Mu;      | `&Mu;`      | &mu;      | `&mu;`      |
| &Nu;      | `&Nu;`      | &nu;      | `&nu;`      |
| &Xi;      | `&Xi;`      | &xi;      | `&xi;`      |
| &Omicron; | `&Omicron;` | &omicron; | `&omicron;` |
| &Pi;      | `&Pi;`      | &pi;      | `&pi;`      |
| &Rho;     | `&Rho;`     | &rho;     | `&rho;`     |
| &Sigma;   | `&Sigma;`   | &sigma;   | `&sigma;`   |
| &Tau;     | `&Tau;`     | &tau;     | `&tau;`     |
| &Upsilon; | `&Upsilon;` | &upsilon; | `&upsilon;` |
| &Phi;     | `&Phi;`     | &phi;     | `&phi;`     |
| &Chi;     | `&Chi;`     | &chi;     | `&chi;`     |
| &Psi;     | `&Psi;`     | &psi;     | `&psi;`     |
| &Omega;   | `&Omega;`   | &omega;   | `&omega;`   |

### Pfeile und Operatoren

Pfeile und Operatoren können auch als *html* Symbole implementiert werden. Die folgende Tabelle gibt einen Überblick.

|         | Arrows    |   |          | Operators (1) |   |          | Operators (2) |   |         | Operators (3) |
|---------|-----------|---|----------|---------------|---|----------|---------------|---|---------|---------------|
| &larr;  | `&larr;`  |   | &forall; | `&forall;`    |   | &lowast; | `&lowast;`    |   | &sim;   | `&sim;`       |
| &uarr;  | `&uarr;`  |   | &part;   | `&part;`      |   | &radic;  | `&radic;`     |   | &cong;  | `&cong;`      |
| &rarr;  | `&rarr;`  |   | &exist;  | `&exist;`     |   | &prop;   | `&prop;`      |   | &asymp; | `&asymp;`     |
| &darr;  | `&darr;`  |   | &empty;  | `&empty;`     |   | &infin;  | `&infin;`     |   | &ne;    | `&ne;`        |
| &harr;  | `&harr;`  |   | &nabla;  | `&nabla;`     |   | &ang;    | `&ang;`       |   | &equiv; | `&equiv;`     |
| &crarr; | `&crarr;` |   | &isin;   | `&isin;`      |   | &and;    | `&and;`       |   | &le;    | `&le;`        |
| &lArr;  | `&lArr;`  |   | &notin;  | `&notin;`     |   | &or;     | `&or;`        |   | &ge;    | `&ge;`        |
| &uArr;  | `&uArr;`  |   | &ni;     | `&ni;`        |   | &cap;    | `&cap;`       |   | &sub;   | `&sub;`       |
| &rArr;  | `&rArr;`  |   | &prod;   | `&prod;`      |   | &cup;    | `&cup;`       |   | &sup;   | `&sup;`       |
| &dArr;  | `&dArr;`  |   | &sum;    | `&sum;`       |   | &int;    | `&int;`       |   | &nsub;  | `&nsub;`      |
| &hArr;  | `&hArr;`  |   | &minus;  | `&minus;`     |   | &sdot;   | `&sdot;`      |   | &perp;  | `&perp;`      |


### Verschiedene Symbole

*Markdown* profitiert von vielen weiteren *html* Symbolen, die in Gleichungen oder anderem Text verwendet werden können. Die folgende Tabelle gibt einen Überblick über solche verschiedenen Symbole.

|          | Symbols (1) |  |          | Symbols (2) |  |           | Symbols (3) |
|----------|-------------|--|----------|-------------|--|-----------|-------------|
| &quot;   | `&quot;`    |  | &ndash;  | `&ndash;`   |  | &oline;   | `&oline;`   |
| &amp;    | `&amp;`     |  | &mdash;  | `&mdash;`   |  | &frasl;   | `&frasl;`   |
| &lt;     | `&lt;`      |  | &lsquo;  | `&lsquo;`   |  | &sigmaf;  | `&sigmaf;`  |
| &gt;     | `&gt;`      |  | &rsquo;  | `&rsquo;`   |  | &image;   | `&image;`   |
| &OElig;  | `&OElig;`   |  | &sbquo;  | `&sbquo;`   |  | &real;    | `&real;`    |
| &oelig;  | `&oelig;`   |  | &ldquo;  | `&ldquo;`   |  | &trade;   | `&trade;`   |
| &Scaron; | `&Scaron;`  |  | &rdquo;  | `&rdquo;`   |  | &alefsym; | `&alefsym;` |
| &scaron; | `&scaron;`  |  | &bdquo;  | `&bdquo;`   |  | &lceil;   | `&lceil;`   |
| &Yuml;   | `&Yuml;`    |  | &dagger; | `&dagger;`  |  | &rceil;   | `&rceil;`   |
| &circ;   | `&circ;`    |  | &Dagger; | `&Dagger;`  |  | &lfloor;  | `&lfloor;`  |
| &tilde;  | `&tilde;`   |  | &permil; | `&permil;`  |  | &rfloor;  | `&rfloor;`  |
| &ensp;   | `&ensp;`    |  | &lsaquo; | `&lsaquo;`  |  | &lang;    | `&lang;`    |
| &emsp;   | `&emsp;`    |  | &rsaquo; | `&rsaquo;`  |  | &rang;    | `&rang;`    |
| &thinsp; | `&thinsp;`  |  | &euro;   | `&euro;`    |  | &loz;     | `&loz;`     |
| &zwnj;   | `&zwnj;`    |  | &bull;   | `&bull;`    |  | &spades;  | `&spades;`  |
| &zwj;    | `&zwj;`     |  | &hellip; | `&hellip;`  |  | &clubs;   | `&clubs;`   |
| &lrm;    | `&lrm;`     |  | &prime;  | `&prime;`   |  | &hearts;  | `&hearts;`  |
| &rlm;    | `&rlm;`     |  | &Prime;  | `&Prime;`   |  | &diams;   | `&diams;`   |


(docs-wikis)=
## Wikis

While every {ref}`git <chpt-git>` repository should at least contain a descriptive *README.md*, *wiki* s provide much more detail and guidance. Wikis are a convenient way to guide users with permanent sidebars (such as the menu bar on this website), help users to understand methods and codes, and collaborative coding with precise descriptions of scripts. *GitHub* users find options to activate *wiki*s in the *Settings* tab of a repository and the developers continue to improve *wiki* functions ([read more about *GitHub*'s wikis](https://help.github.com/en/github/building-a-strong-community/about-wikis)).

Ausgefeiltere *Wikis sind auf der *Jekyll*-Themen-Website verfügbar (z. B. das [git-wiki theme](https://jekyll-themes.com/git-wiki/)]. Um *Jekyll*-Themen zu verwenden, stellen Sie sicher, dass Sie [*GitHub* pages](https://help.github.com/en/github/working-with-github-pages/creating-a-github-pages-site)] (im Repository *Einstellungen*) für das Repository aktivieren, in dem Sie das *wiki* einrichten möchten (dieses Wiki-Repository ist normalerweise ein anderes Repository, um ein Code-Repository zu beschreiben). Installieren Sie dann die *Ruby-Entwicklungsumgebung * und *Jekyll * (siehe [Anweisungen auf ihrer Website](https://jekyllrb.com/docs/), um auf Hunderte von Themen für Code- und Projektdokumentation zuzugreifen und diese zu erstellen). Forkierte und lokal angepasste Themes können dann *push* in ein entferntes *Wiki*-Repository mit {ref}`git <chpt-git>` geschickt werden.

```{tip}
Es gibt andere Git-Services und Wiki-Host-Anbieter, wie [GitLab](https://gitlab.com/pages) oder [plan.io](https://plan.io/knowledge-management/)].
```

```{admonition} Exercise
Übung im Markdown mit der [Markdown und git](../exercises/ex-git) Übung].
```

(rst)=
## reStructuredText, Sphinx und readthedocs

Eine Alternative zum Markdown ist [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html), die das Einbetten von * Python-Dokumentstrings* (lesen Sie mehr über {ref}`chpt-style`) in jedes Skript mit [*Sphinx*](https://www.sphinx-doc.org)] ermöglicht.

Without any *Python* or programming knowledge, it might be hard to get started with *Sphinx*. So make sure to understand *Python* basics and document any code with *docstrings*, at best using [*google style*](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) formatting. Once you start documenting your first *Python* package, *Google-style* *docstrings* will enable the fast generation of high-quality docs. Currently, one of the best options for partially auto-generating code documentations, for any programming language, is [*readthedocs*](https://readthedocs.org/), which builds on *Sphinx* and *reStructuredText*.

[Wiki]: https://wikipedia.org
