# Markdown and Code Documentation

## Document your work
Leonardo Da Vinci used journals to sketch, develop and eventually pass on his ideas. Alexander von Humboldt documented many of his journeys in travel journals and Marie Skłodowska Curie wrote down the theory of "radioactivity" using pens and papers. Today,  writing media have evolved into infinite digital oceans with sophisticated tools for documenting code and ideas. Also the way in which we look for and retrieve information has evolved from searching for lexicon entries to using keywords in search engines.
So if you have made an ingenious discovery, you want to make sure you document it well so that others can understand and use it. You also want to make sure that others can find your stroke of genius in digital media. You also want to make sure that others can find your stroke of genius in digital media. One of the most widespread methods for documenting and spreading ideas is the use of so-called wikis (from Hawaiian: *fast*), which can easily be written in markdown language. *GitHub* provides comprehensive, easy-to-read explanations for [project documentation](https://guides.github.com/features/wikis/) with *Markdown* as core element. This page presents the basics of the markdown language to leverage wikis. Moreover, the powerful alternative of using *reStructuredText* in *Sphinx*-based documentations is introduced.



```{tip}
[*Write the Docs*](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/) provides comprehensive guides for code documentation - just take about 10 minutes to read how to save days.
```


## What to document?

A good code documentation starts with a qualitative and concise description of software (e.g., a *Python* package) capacities, products, and requirements. It also provides workflows for installing and using the software, at best with illustrative examples. Finally, a good troubleshooting section enables users to find problems in their data setup or software usage. To enable future development and maintenance, a *Contributing* section provides *good-practice-guidelines* for coding new software capacities.

### Present the software

This section intends to advertise the benefits and capacities of the software: Tell users briefly the purpose of the software, why it is unique and what it produces.

### Requirements

This section should answer the following questions:

* What system requirements are needed?
* Which dependencies does the software have (e.g., other *Python* packages such as *NumPy*)?
* What input data does a user need to run the software?

### Installation

Describe step-by-step the installation of the software (e.g., how to download and access your *Python* package). Screenshots can be helpful here. At best, the *Requirements* section made it clear what users need to proceed with the installation.

### Usage

Describe how the software can be used, starting with basics such as importing the software as *Python* package. Mention possible pre- and post-processing for input and output data, respectively. If available, add more complex functionalities consecutively in a logical order.

To truly make your software useful to others, add a case study. Most users will not read the detailed code documentation until they get the software to run once and see what it can do. A use case also helps to check the logic of your code and gives users the opportunity to bridge imperfect code documentation sections to their workflow. This can sometimes be necessary, even if your code is certainly perfect and the documentation is foolproof.

### Troubleshooting

Sure, your code is error-free and of course only the user makes mistakes. Show compassion and integrate specific *try*-*except* statements (more on the [*Python*<sup>basics</sup>](../python-basics/pyerror.html#try-except) page) in the source code, which point out possible error sources. These error (and maybe even warning) messages should all be listed in a *Troubleshooting* section of the code documentation. Any source of error (message) should be documented regarding the following aspects:

* Cause: Possible reasons for why an error occurs.
* Remedy: Steps for troubleshooting an error.

### Contributing

Your software is brilliant. To make the software even more brilliant, foolproof, and powerful, it is a great idea (actually: an absolute must) to get more authors on the development team. However, it is very likely that any other author has individual preferences when it comes to code standards. So make sure to set up clear rules for other contributors from the beginning. For example, define clear code conventions as explained on the [code style](../python-basics/pystyle) page.


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

Basic text editors that support *Markdown* are listed [here](../get-started/others.html#npp). Popular and multi-platform *IDE*s for editing *Markdown* (`.md`) files are [*ATOM*](https://atom.io/) (for combination with *JavaScript*, *html*, and *CSS*), and [*JupyterLab*](https://jupyter.org) or [*PyCharm*](https://www.jetbrains.com/pycharm/) (for combination with *Python* or *R*), which both are available through [*Anaconda*](https://docs.conda.io/). Read more about Anaconda and associated *IDE*s on the [previous pages](../get-started/ide).

### Markdown Command Overview and Image Implementation

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

### Itemization (Un-numbered Lists)

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
|Banana | Plantae | Musa  |
|Jackfruit|Plantae|Artocarpus|
```

***

| Fruit | Kingdom | Genus |
|-------|:-------:|------:|
|Banana | Plantae | Musa |
|Jackfruit|Plantae|Artocarpus|

***

Converting complex tables from workbooks (e.g., from *LibreOffice Calc* or *MS Excel*) is possible with many online tools and here is just one example from Dave Johnson: [https://thisDaveJ.com](https://thisdavej.com/copy-table-in-excel-and-paste-as-a-markdown-table/).

### Math Expressions: Equations

Math expressions and equations must be implemented as text in standard *Markdown*. *GitHub*s markdown interpreter does not support many external *TeX*-like equation renderers for reasons of security. However, *GitHub* users can still render *TeX*-like equations with the following code:

```html
<img src="https://render.githubusercontent.com/render/math?math=sin{\alpha} = \sqrt{1-cos^{2}\alpha}">
```
This results in <img src="https://render.githubusercontent.com/render/math?math=sin{\alpha} = \sqrt{1-cos^{2}\alpha}">

Note that the equation starts after `math&math=`. Thus for using the math snippet in a document, copy and modify the following expression `<img src="https://render.githubusercontent.com/render/math?math=TYPE =  EQUATION HERE">`.

### Html - Markdown
*html* structures can be flawlessly used in *Markdown*, which itself is nothing else than simplified *html*. Therefore, any *html* structure can be used within markdown and the above-shown equation implementation already represents the first example for *html* usage in a *Markdown* document. The following sections provide an overview of some more or less frequently used *html* symbols that also work with *Markdown*.

### Greek letters

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

### Arrows and Operators

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

While every [git](../get-started/git) repository should at least contain a descriptive *README.md*, *wiki* s provide much more detail and guidance. Wikis are a convenient way to guide users with permanent side bars (such as the menu bar on this web site), help users to understand methods and codes, and collaborative coding with precise descriptions of scripts. *GitHub* users find options to activate *wiki*s in the *Settings* tab of a repository and the developers continue to improve *wiki* functions ([read more about *GitHub*'s wikis](https://help.github.com/en/github/building-a-strong-community/about-wikis)).

More sophisticated *wiki*s are available on the *Jekyll* themes web site (e.g., the [git-wiki theme](https://jekyll-themes.com/git-wiki/)). In order to use *Jekyll* themes, make sure to enable [*GitHub* pages](https://help.github.com/en/github/working-with-github-pages/creating-a-github-pages-site) (in the repository *Settings* tab) for the repository where you want to establish the *wiki* (this wiki-repository is typically another repository in order to describe a code-repository). Then, install the *Ruby development environment* and *Jekyll* (see [instructions on their website](https://jekyllrb.com/docs/) in order to access and build hundreds of themes for code and project documentation. Forked and locally adapted themes can then be *push*ed to a remote *wiki* repository using [git](../get-started/git).

```{tip}
There are other git-pages and wiki host providers out there, such as [GitLab](https://gitlab.com/pages) or [plan.io](https://plan.io/knowledge-management/).
```

```{admonition} Exercise
Get practice in markdown with the [markdown and git](../exercises/ex-git) exercise.
```

## *reStructuredText*, *Sphinx* and readthedocs

An alternative to markdown is [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) that enables embedding *Python docstrings* (read more about [code style conventions](../python-basics/pystyle)) in any script or module with [*Sphinx*](https://www.sphinx-doc.org).

Without any *Python* or programming knowledge, it might be hard to get started with *Sphinx*. So make sure to understand *Python* basics and document any code with *docstrings*, at best using [*google style*](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) formatting. Once you start documenting your first *Python* package, *google-style* *docstrings* will enable the fast generation of high-quality docs. Currently, one of the best options for partially auto-generating code documentations, for any programming language, is [*readthedocs*](https://readthedocs.org/), which builds on *Sphinx* and *reStructuredText*.

[wiki]: https://wikipedia.org
