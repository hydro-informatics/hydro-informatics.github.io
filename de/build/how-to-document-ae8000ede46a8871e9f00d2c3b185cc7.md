---
description: Leitfaden zur Dokumentation von Codes und Projekten mit Markdown, Wikis und reStructuredText, einschließlich bester Praktiken für README-Dateien, Codedokumentation und GitHub-Repositories.
---

# Wie Markdown und Dokument

## Dokumentieren Sie Ihre Arbeit
Leonardo Da Vinci benutzte Zeitschriften, um seine Ideen zu skizzieren, zu entwickeln und schließlich weiterzugeben. Alexander von Humboldt dokumentierte viele seiner Reisen in Reisezeitschriften und Marie Skłodowska Curie schrieb die Theorie der "Radioaktivität" mit Stiften und Papieren. Heute haben sich Schreibmedien zu unendlichen digitalen Ozeanen entwickelt, mit ausgeklügelten Werkzeugen zur Dokumentation von Code und Ideen. Auch, wie wir nach und nach Informationen suchen, hat sich von der Suche nach Lexikoneinträgen entwickelt, um Keywords in Suchmaschinen zu verwenden.
Wenn Sie also eine geniale Entdeckung gemacht haben, möchten Sie sicherstellen, dass Sie es gut dokumentieren, damit andere es verstehen und verwenden können. Sie wollen auch sicherstellen, dass andere Ihren Schlag des Genies in digitalen Medien finden. Sie wollen auch sicherstellen, dass andere Ihren Schlag des Genies in digitalen Medien finden. Eine der am weitesten verbreiteten Methoden zur Dokumentierung und Verbreitung von Ideen ist die Verwendung sogenannter Wikis (aus Hawaiian: *fast*), die leicht in Markdown-Sprache geschrieben werden können. *GitHub* bietet umfassende, einfach zu lesende Erläuterungen zu [Projektdokumentation](https://guides.github.com/features/wikis/) mit *Markdown* als Kernelement. Diese Seite stellt die Grundlagen der Markdown-Sprache dar, um Wikis zu nutzen. Darüber hinaus wird die leistungsstarke Alternative zur Verwendung von *reStructuredText* in *Sphinx*-basierten Dokumentationen vorgestellt.


```{tip}
[Die Docs](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/) schreiben bietet umfassende Anleitungen für die Codedokumentation. Nehmen Sie etwa 10 Minuten, um zu lesen, wie man Tage der Arbeit zu speichern.
```


## Was zu Dokumentieren?

Gute Codedokumentation beginnt mit einer qualitativen und präzisen Beschreibung von Software (z.B. einem *Python* Paket) Kapazitäten, Produkten und Anforderungen. Es bietet auch Workflows für die Installation und Nutzung der Software, bestens mit illustrativen Beispielen. Schließlich ermöglicht ein guter Fehlerbehebungsabschnitt den Benutzern, Probleme in ihrer Daten- oder Softwarenutzung zu finden. Um zukünftige Entwicklung und Wartung zu ermöglichen, bietet ein *Contributing* Abschnitt * Good-Practice-Richtlinien* zur Kodierung neuer Softwarekapazitäten.

### Ihre Software oder Ihr Projekt präsentieren

Dieser Abschnitt beabsichtigt, die Vorteile und Kapazitäten der Software zu werben: Benutzer kurz den Zweck der Software, warum es einzigartig ist und was es produziert.

### Anforderungen

Ein Abschnitt der Anforderungen sollte Benutzern oder Interessenvertretern sagen:

* Welche Systemanforderungen werden benötigt?
* Welche Abhängigkeiten hat die Software oder das Projekt (z.B. andere *Python* Pakete wie {ref}`numpy`)?
* Welche Eingabedaten werden benötigt, um die Software auszuführen?

### Installation

Ein Installationsabschnitt sollte die Installation der Software Schritt für Schritt beschreiben (z.B. wie Sie Ihr *Python*-Paket herunterladen und zugreifen können) oder den Workflow eines Projektes. Screenshots können hilfreich sein. Der Abschnitt *Anforderungen* sollte bereits geklärt haben, was Benutzer für die Installation benötigen.

### Verwendung

Ein Abschnitt über die Nutzung sollte beschreiben, wie die Software verwendet werden kann, beginnend mit Grundlagen wie Importieren der Software als *Python* Paket. Darüber hinaus sollten mögliche Behandlungen von Eingabe- und Ausgabedaten (d.h. Vor- und Nachbearbeitung) erwähnt werden. Wenn verfügbar, fügen Sie in logischer Reihenfolge nacheinander komplexere Funktionalitäten hinzu.

Um Ihre Software wirklich nützlich für andere zu machen, fügen Sie eine Fallstudie hinzu. Die meisten Benutzer werden die detaillierte Codedokumentation nicht lesen, bis sie die Software einmal ausführen und sehen, was sie tun kann. Ein Anwendungsfall hilft auch, die Logik Ihres Codes zu überprüfen und gibt den Benutzern die Möglichkeit, fehlerhafte Codedokumentationsabschnitte an ihren Workflow zu überbrücken. Dies kann manchmal notwendig sein, auch wenn Ihr Code ist sicherlich perfekt und die Dokumentation ist töricht.

### Fehlerbehebung

Sicher, Ihr Code und Workflow sind fehlerfrei und natürlich macht nur der Benutzer Fehler. Wie auch immer, zeigen Sie Mitgefühl und integrieren spezifische {ref}`try-except`-Anweisungen in den Quellcode, die mögliche Fehlerquellen zeigen. Diese Fehlermeldungen (und vielleicht sogar Warnung) sollten alle in einem *Troubleshoot* Abschnitt der Codedokumentation aufgeführt werden. Jede Fehlerquelle (Message) sollte in Bezug auf folgende Aspekte dokumentiert werden:

* Ursache: Mögliche Gründe, warum ein Fehler auftritt.
* Remedy: Schritte zur Fehlerbehebung.

### Beitrag

Ihre Software ist brillant. Um die Software noch brillanter, törichter und leistungsfähiger zu machen, ist es eine tolle Idee (wirklich: ein absolutes Muss) um mehr Autoren auf das Entwicklungsteam zu bekommen. Jeder andere Autor hat jedoch wahrscheinlich individuelle Präferenzen, wenn es um Code-Standards geht. Stellen Sie also von Anfang an klare Regeln für andere Beiträge fest. So definieren Sie z.B. klare Code-Konventionen wie im Abschnitt {ref}`chpt-style` erläutert.

(markdown)=
## Markiert

Um eine Dokumentation eines Codes oder Projekts im web-publish-ready Format zu schreiben, ist eine plattformübergreifende Schreibeinstellung erforderlich. Zu diesem Zweck stellt *Markdown* eine gute Wahl dar (u.a. {ref}`reStructuredText <rst>`). *Markdown* wurde 2004 erstellt und ist eine einfache Markup-Sprache, die intuitiv und einfach zu lernen ist. Markup-Sprachen strukturieren den Inhalt von Klartextdokumenten, wie ein Dokument an Endbenutzer angezeigt wird ({term}`Rich Text Format`). Andere beliebte Markup-Sprachen sind beispielsweise [TeX](https://en.wikipedia.org/wiki/TeX) und [XML (Extensible Markup Language)](https://en.wikipedia.org/wiki/XML). *Markdown* wurde ein beliebtes Tool zum Schreiben syntaktisch unterscheidbarer Computertexte, der dann in {term}`Rich Text Format`geschmack übersetzt wird. Hier ist ein Beispiel dafür, wie *Markdown* funktioniert:

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
**Better als Word-ähnliche Rich Texteditore**

*OS*-unabhängige Funktionalität:
- Vermeiden Sie die Formatierung derselben Art von Dingen redundant (und uneinheitlich)
- Rückwärtskompatibilität
- Formel-Handling
- und vieles mehr...

````
`````


### Markdown Editoren (IDEs)

Viele Texteditoren bieten *Markdown* Add-ons und *Markdown*-nur Editoren verlieren ihre Bedeutung immer mehr. Editoren, die gleichzeitig *Markdown* und Programmiersprachen wie *Python* oder *R* unterstützen, sind Stand der Technik und daher empfohlen.

Basistext-Editoren, die *Markdown* unterstützen, sind unter{ref}`here <npp>`. Beliebt und multi-platform *IDE*s for editing *Markdown* (`.md`) Dateien sind {ref}`jupyter` oder {ref}`pycharm`.

### Markdown Befehlsübersicht und Bilddurchführung

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

### Posting (Unnummerierte Listen)

Posted List Abschnitt kann mit `*`, `+` oder `-`-Symbolen mit Registerkarten erstellt werden, die die Listenangabe bestimmen:

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

* Ebene 1 Artikel
- Ebene 2 Artikel
- ein weiteres Level 2 Artikel
+ Ebene 3 Artikel
* nächste Ebene 1 Artikel

````
`````

### Tabellen

Die Tabellenspalten werden durch ein `|`-Zeichen getrennt. Die erste Zeile bestimmt Zeilenüberschriften und die zweite Zeile die Ausrichtung durch die Verwendung von `:` (siehe unten Beispiel).

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

| Obst | Königreich | Genus |
|-------::------:-------::
|Banana | Plantae | Musa
|Jackfruit|Plantae|Artocarpus|

````
`````

Converting complex tables from workbooks (e.g., from *LibreOffice Calc* or *MS Excel*) is possible with many online tools, and here is just one example from Dave Johnson: [https://thisDaveJ.com](https://thisdavej.com/copy-table-in-excel-and-paste-as-a-markdown-table/).

### Mathematische Ausdrücke: Gleichungen

Mathe-Ausdrücke und Gleichungen können mit $-Zeichen, ähnlich *LaTeX* implementiert werden.

## Html - Markdown
* HTML*-Strukturen können in *Markdown* fehlerfrei verwendet werden, was selbst nichts anderes als vereinfacht *html* ist. Daher kann jede *html*-Struktur innerhalb von markdown verwendet werden und die oben gezeigte Gleichungs-Implementierung stellt bereits das erste Beispiel für *html*-Nutzung in einem *Markdown*-Dokument dar. Die folgenden Abschnitte geben einen Überblick über einige mehr oder weniger häufig verwendete *html*-Symbole, die auch mit *Markdown* arbeiten.

### Griechische Briefe

Um griechische Buchstaben in Textzeilen zu verwenden, verwenden Sie *html* Sprache, wobei `&lettername;` das gewünschte *Greek* Buchstabensymbol produziert (z.B. Typ `&delta;` an Ausgabe &delta; oder `&Delta;`, um einen Kapitalbrief &Delta auszugeben;). Die folgende Tabelle gibt einen Überblick über griechische Buchstabensymbole.

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

### Pfeile und Betreiber

Pfeile und Operatoren können auch als *html*-Symbole implementiert werden. Die folgende Tabelle gibt einen Überblick.

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

*Markdown* profitiert von vielen mehr *html*-Symbolen, die in Gleichungen oder anderen Texten verwendet werden können. Die folgende Tabelle gibt einen Überblick über derartige verschiedene Symbole.

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

Während jedes {ref}`git <chpt-git>`-Repository mindestens ein beschreibendes *README.md* enthalten sollte, bieten *wiki*s viel mehr Detail und Anleitung. Wikis sind eine bequeme Möglichkeit, Benutzer mit dauerhaften Sidebars (wie die Menüleiste auf dieser Website), helfen Benutzern, Methoden und Codes zu verstehen, und kollaborative Codierung mit genauen Beschreibungen von Skripten. *GitHub*-Benutzer finden Optionen, um *wiki*s im *Settings*-Tab eines Repository zu aktivieren und die Entwickler verbessern weiterhin *wiki*-Funktionen ([mehr über *GitHub*'s wikis](https://help.github.com/en/github/building-a-strong-community/about-wikis)).

Mehr ausgefeilte *wiki*s sind auf der *Jekyll* Themen-Website (z.B. der [git-wiki Theme](https://jekyll-themes.com/git-wiki/)) erhältlich. Um *Jekyll* Themes zu verwenden, stellen Sie sicher, dass Sie [*GitHub* Seiten](https://help.github.com/en/github/working-with-github-pages/creating-a-github-pages-site) (im Repository *Settings* Tab) für das Repository aktivieren, in dem Sie das *wiki* erstellen möchten (dieses Wiki-Repository ist in der Regel ein anderes Repository zur Beschreibung eines Code-Repository). Dann installieren Sie die *Ruby-Entwicklungsumgebung* und *Jekyll* (siehe [Anweisungen auf ihrer Website](https://jekyllrb.com/docs/), um Hunderte von Themen für Code- und Projektdokumentation zuzugreifen und zu erstellen. Forked und lokal angepasste Themen können dann mit {ref}`git <chpt-git>` an ein entferntes *wiki*-Repository weitergeleitet werden.

```{tip}
Es gibt noch andere Git-Services und Wiki-Hosting-Anbieter, wie [GitLab](https://gitlab.com/pages) oder [plan.io](https://plan.io/knowledge-management/).
```

```{admonition} Exercise
Mit der Übung [markdown und git](../exercises/ex-git)training.
```

(rst)=
## reStructuredText, Sphinx und readthedocs

Eine Alternative zu markdown ist [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html), die die Einbettung von *Python docstrings* (weiterlesen über {ref}`chpt-style`) in jedem Skript mit [*Sphinx*](https://www.sphinx-doc.org).

Ohne *Python* oder Programmierkenntnisse, kann es schwierig sein, mit *Sphinx* zu beginnen. Stellen Sie sicher, *Python* Grundlagen zu verstehen und dokumentieren Sie jeden Code mit *docstrings*, bestens mit [*google style*](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)formatting. Sobald Sie beginnen, Ihr erstes *Python* Paket zu dokumentieren, wird *Google-style* *docstrings* die schnelle Generierung hochwertiger Docs ermöglichen. Derzeit ist eine der besten Optionen für teilweise autogenerierende Codedokumente, für jede Programmiersprache, [*readthedocs*](https://readthedocs.org/), die auf *Sphinx* und *reStructuredText* erstellt.

[wiki]: https://wikipedia.org
