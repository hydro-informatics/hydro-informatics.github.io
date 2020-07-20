---
title: Markdown and Code Documentation
tags: [git, version_control, jupyter, markdown, sharing]
keywords: md markdown document
sidebar: mydoc_sidebar
permalink: hy_documentation.html
folder: get-started
---

## Document your work
Leonardo Da Vinci used journals to sketch, develop and eventually pass on his ideas. Alexander von Humboldt documented many of his journeys in travel journals and Marie Skłodowska Curie wrote down the theory of "radioactivity" using pens and papers. Today,  writing media have evolved into infinite digital oceans with sophisticated tools for documenting code and ideas. Also the way in which we look for and retrieve information has evolved from searching for lexicon entries to using keywords in search engines.
So if you have made an ingenious discovery, you want to make sure you document it well so that others can understand and use it. You also want to make sure that others can find your stroke of genius in digital media. You also want to make sure that others can find your stroke of genius in digital media. One of the most widespread methods for documenting and spreading ideas is the use of so-called wikis (from Hawaiian: *fast*), which can easily be written in markdown language. *GitHub* provides comprehensive, easy-to-read explanations for [project documentation](https://guides.github.com/features/wikis/) with *Markdown* as core element. This page focuses on the basics of the markdown language to leverage wikis.

{% include tip.html content="[*Write the Docs*](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/) provides comprehensive guides for code documentation - just take about 10 minutes to read how to save days." %}

## Markdown 
*Markdown* was created in 2004 and is a simple markup language that is intuitive and easy to learn. Markup languages structure the content of plain text documents regarding the way a document is displayed to end users (<a href="#" data-toggle="tooltip" data-original-title="{{site.data.glossary.richtext}}">rich text</a> format). Other popular markup languages are for example [*TeX*](https://en.wikipedia.org/wiki/TeX) and [*XML* (Extensible Markup Language)](https://en.wikipedia.org/wiki/XML). *Markdown* became a popular tool for writing syntactically distinguishable computer text that is then translated into <a href="#" data-toggle="tooltip" data-original-title="{{site.data.glossary.richtext}}">rich text</a>. Here is an example how *Markdown* works:

```markdown
# Better than Word-like rich text editors 
*OS*-independent functionality:
- Avoid formatting of the same kind of thing redundantly (and inconsistently)
- Backwards compatibility
- Formulae handling 
- ... and many more ... 
```

***

**Better than Word-like rich text editors** <br>
*OS*-independent functionality:
- Avoid formatting of the same kind of thing redundantly (and inconsistently)
- Backwards compatibility
- Formulae handling 
- ... and many more ... 

***

### Markdown Editors (IDEs)

Many text editors provide *Markdown* add-ons and *Markdown*-only editors are loosing their significance more and more. Editors that simultaneously support *Markdown* and programming languages like *Python* or *R* are state of the art and therefore recommended.

Basic text editors that support *Markdown* are listed [here](hy_others.html#npp). Popular and multi-platform *IDE*s for editing *Markdown* (`.md`) files are [*ATOM*](https://atom.io/) (for combination with *JavaScript*, *html*, and *CSS*), and [*Jupyter Lab*](https://jupyter.org) or [*PyCharm*](https://www.jetbrains.com/pycharm/) (for combination with *Python* or *R*), which both are available through [*Anaconda*](https://docs.conda.io/). [Read more about Anaconda and associated *IDE*s on the previous pages.](hy_ide.html)

### Markdown command overview (+images)

The following table and sections provide an overview of basic markdown commands. There is much more options out there, which you can find by using your favorite search engine with the keywords `markdown` `guide`.
  
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
| Image                  | `![ImgName](https://image-address/image.png)` | ![ImgName](https://raw.githubusercontent.com/RiverArchitect/Media/master/images/logo_small.ico)|
| Italic text            | `*italic*`                      |  *italic*        |
| Numbered list item     | `1. numbered item`              | 1. Numbered item |
| Reference (defined)    | `[Defined Reference][wiki]`     |  [Defined Reference][wiki]  |
| Reference (definition) | `[wiki]: https://wikipedia.org` |   *Place at file bottom*               |
| Strikethrough | `~~Strikethrough~~ ` | ~~Strikethrough~~    |

### Itemization (un-numbered list)

Itemized list section can be produced using `*`, `+`, or `-` symbols with tabs that determine the list indentation:
```markdown
* level 1 item
    - level 2 item 
    - another level 2 item
        + level 3 item
* next level 1 item
```

***

* level 1 item
    - level 2 item 
    - another level 2 item
        + level 3 item
* next level 1 item

***

### Tables

Table columns are separated by a `|` sign. The first row determines row headers and the second row the alignment through the use of `:` (see below example).

```markdown
| Fruit | Kingdom | Genus |
|-------|:-------:|------:|
|Banana | Plantae | Musa |
|Jackfruit|Plantae|Artocarpus|
```

***

| Fruit | Kingdom | Genus |
|-------|:-------:|------:|
|Banana | Plantae | Musa |
|Jackfruit|Plantae|Artocarpus|

***

Converting complex tables from workbooks (e.g., from *LibreOffice Calc* or *MS Excel*) is possible with many online tools and here is just one example from Dave Johnson: [https://thisDaveJ.com](https://thisdavej.com/copy-table-in-excel-and-paste-as-a-markdown-table/).

### Math expressions: Equations

Math expressions and equations must be implemented as text in standard *Markdown*. *GitHub*s markdown interpreter does not support many external *TeX*-like equation renderers for reasons of security. However, *GitHub* users can still render *TeX*-like equations with the following code:
```html
<img src="https://render.githubusercontent.com/render/math?math=sin{\alpha} = \sqrt{1-cos^{2}\alpha}">
```
This results in    <img src="https://render.githubusercontent.com/render/math?math=sin{\alpha} = \sqrt{1-cos^{2}\alpha}">

Note that the equation starts after `math&math=`. Thus for using the math snippet in a document, copy and modify the following expression `<img src="https://render.githubusercontent.com/render/math?math=TYPE =  EQUATION HERE">`.

### html - markdown
*html* structures can be flawlessly used in *Markdown*, which itself is nothing else than simplified *html*. Therefore, any *html* structure can be used within markdown and the above-shown equation implementation already represents the first example for *html* usage in a *Markdown* document. The following sections provide an overview of some more or less frequently used *html* symbols that also work with *Markdown*. 

### Math expressions: Greek letters

In order to use greek letters in inline text, use *html* language, where `&lettername;` produces the desired *Greek* letter symbol (e.g., type `&delta;` to output &delta; or `&Delta;` to output a capital letter &Delta;). The following table provides an overview of Greek letter symbols.

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

### Math expressions: Arrows and Operators

Arrows and operators can also be implemented as *html* symbols. The following table provides an overview.

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


### Miscellaneous Symbols 

*Markdown* profits from many more *html* symbols that may be used in equations or other text. The following table provides an overview over such miscellaneous symbols.

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



## Wikis

While every [*git*](hy_git.html) repository should at least contain a descriptive *README.md*, *wiki*s provide much more detail and guidance. Wikis are a convenient way to guide users with permanent side bars (such as the menu bar on this web site), help users to understand methods and codes, and collaborative coding with precise descriptions of scripts. *GitHub* users find options to activate *wiki*s in the *Settings* tab of a repository and the developers continue to improve *wiki* functions ([read more about *GitHub*'s wikis](https://help.github.com/en/github/building-a-strong-community/about-wikis)).

More sophisticated *wiki*s are available on the *Jekyll* themes web site (e.g., the [git-wiki theme](https://jekyll-themes.com/git-wiki/)). In order to use *Jekyll* themes, make sure to enable [*GitHub* pages](https://help.github.com/en/github/working-with-github-pages/creating-a-github-pages-site) (in the repository *Settings* tab) for the repository where you want to establish the *wiki* (this wiki-repository is typically another repository in order to describe a code-repository). Then, install the *Ruby development environment* and *Jekyll* (see [instructions on their web site](https://jekyllrb.com/docs/)) in order to access and build hundreds of themes for code and project documentation. Forked and locally adapted themes can then be *push*ed to a remote *wiki* repository using [git](hy_git.html).
  
{% include tip.html content="There are other git-pages and wiki host providers out there, such as [GitLab](https://gitlab.com/pages) or [plan.io](https://plan.io/knowledge-management/)." %}





[wiki]: https://wikipedia.org