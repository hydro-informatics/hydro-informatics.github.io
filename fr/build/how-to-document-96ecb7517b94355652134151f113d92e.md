---
description: Guide pour documenter le code et les projets avec Markdown, wikis et reStructuredText, y compris les meilleures pratiques pour les fichiers README, la documentation de code et les dépôts GitHub.
---

# Comment marquer et documenter

## Documenter votre travail
Leonardo Da Vinci a utilisé des revues pour dessiner, développer et finalement transmettre ses idées. Alexander von Humboldt a documenté plusieurs de ses voyages dans des journaux de voyage et Marie Skłodowska Curie a écrit la théorie de la "radioactivité" à l'aide de stylos et de papiers. Aujourd'hui, les médias écrits sont devenus des océans numériques infinis avec des outils sophistiqués pour documenter le code et les idées. De plus, la façon dont nous recherchons et récupérons des informations est passée de la recherche d'entrées de lexique à l'utilisation de mots clés dans les moteurs de recherche.
Donc, si vous avez fait une découverte ingénieuse, vous voulez vous assurer que vous documentez bien afin que les autres puissent comprendre et utiliser. Vous voulez également vous assurer que d'autres peuvent trouver votre coup de génie dans les médias numériques. Vous voulez également vous assurer que d'autres peuvent trouver votre coup de génie dans les médias numériques. L'une des méthodes les plus répandues pour documenter et diffuser des idées est l'utilisation de wikis (d'Hawaï : *fast*), qui peuvent facilement être écrits en langage balisage. *GitHub* fournit des explications complètes et faciles à lire pour [documentation de projet](https://guides.github.com/features/wikis/) avec *Markdown* comme élément de base. Cette page présente les bases du langage de balisage pour tirer parti des wikis. En outre, la puissante alternative à l'utilisation de *reStructuredText* dans les documents basés sur *Sphinx* est introduite.


```{tip}
[Écrire le document Docs](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/) fournit des guides détaillés pour la documentation du code. Prenez environ 10 minutes pour lire comment économiser des jours de travail.
```


## Quoi documenter ?

Une bonne documentation de code commence par une description qualitative et concise des capacités, des produits et des exigences des logiciels (p. ex., un paquet *Python*). Il fournit également des flux de travail pour installer et utiliser le logiciel, au mieux avec des exemples. Enfin, une bonne section de dépannage permet aux utilisateurs de trouver des problèmes dans leur configuration de données ou l'utilisation de logiciels. Pour permettre le développement et la maintenance futurs, une section *Contribution* fournit * des lignes directrices sur les bonnes pratiques* pour le codage de nouvelles capacités logicielles.

### Présentez votre logiciel ou projet

Cette section vise à faire connaître les avantages et les capacités du logiciel : Dites brièvement aux utilisateurs le but du logiciel, pourquoi il est unique et ce qu'il produit.

### Exigences

Une section sur les exigences devrait indiquer aux utilisateurs ou aux intervenants :

* Quelles sont les exigences du système?
* Quelles sont les dépendances du logiciel ou du projet (p. ex., d'autres paquets *Python* tels que {ref}`numpy`)?
* Quelles données d'entrée sont nécessaires pour exécuter le logiciel?

### Installation

Une section d'installation doit décrire étape par étape l'installation du logiciel (par exemple, comment télécharger et accéder à votre paquet *Python*) ou le déroulement d'un projet. Les captures d'écran peuvent être utiles. La section *Requirements* devrait déjà avoir clarifié ce dont les utilisateurs ont besoin pour l'installation.

### Utilisation

Une section sur l'utilisation doit décrire comment le logiciel peut être utilisé, en commençant par des bases telles que l'importation du logiciel comme paquet *Python*. En outre, il devrait mentionner les traitements possibles des données d'entrée et de sortie (c.-à-d., pré-traitement et post-traitement, respectivement). Si disponible, ajoutez des fonctionnalités plus complexes consécutivement dans un ordre logique.

Pour vraiment rendre votre logiciel utile aux autres, ajoutez une étude de cas. La plupart des utilisateurs ne liront pas la documentation de code détaillée avant d'obtenir le logiciel à exécuter une fois et voir ce qu'il peut faire. Un cas d'utilisation aide également à vérifier la logique de votre code et donne aux utilisateurs la possibilité de relier des sections de documentation de code imparfaites à leur flux de travail. Cela peut parfois être nécessaire, même si votre code est certainement parfait et que la documentation est infaillible.

### Dépannage

Bien sûr, votre code et votre workflow sont exempts d'erreurs et bien sûr, seul l'utilisateur fait des erreurs. Quoi qu'il en soit, montrez de la compassion et intégrez des énoncés spécifiques {ref}`try-except` dans le code source, ce qui indique les sources d'erreurs possibles. Ces messages d'erreur (et peut-être même d'avertissement) devraient tous être listés dans une section *Troubleshoot* de la documentation du code. Toute source d'erreur (message) doit être documentée sur les aspects suivants :

* Cause : Raisons possibles pour lesquelles une erreur se produit.
* Réparation: Étapes pour résoudre une erreur.

### Contribution

Ton logiciel est génial. Pour rendre le logiciel encore plus brillant, infaillible et puissant, c'est une bonne idée (en fait : un must absolu) d'obtenir plus d'auteurs dans l'équipe de développement. Cependant, tout autre auteur a probablement des préférences individuelles en ce qui concerne les normes de code. Assurez-vous donc d'établir des règles claires pour les autres contributeurs dès le début. Par exemple, définissez des conventions de code claires comme expliqué dans la section {ref}`chpt-style`.

(markdown)=
## Marquage

Pour rédiger une documentation d'un code ou d'un projet dans un format prêt à publier sur le Web, il est nécessaire d'établir un type de plate-forme croisée. À cette fin, *Markdown* représente un bon choix (entre autres, comme {ref}`reStructuredText <rst>`). *Markdown* a été créé en 2004 et est un langage de balisage simple qui est intuitif et facile à apprendre. Les langues de balisage structurent le contenu des documents en texte clair concernant la façon dont un document est affiché aux utilisateurs finaux ({term}`Rich Text Format`). D'autres langues de balisage populaires sont par exemple [TeX](https://en.wikipedia.org/wiki/TeX) et [XML (Extensible Markup Language)](https://en.wikipedia.org/wiki/XML). *Markdown* est devenu un outil populaire pour l'écriture syntaxique de texte d'ordinateur distinguable qui est ensuite traduit en {term}`Rich Text Format` saveur. Voici un exemple du fonctionnement de *Markdown*:

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
**Mieux vaut que les éditeurs de texte riches en Word**

Fonctions indépendantes de l'OS* :
- Évitez de formater le même genre de chose de façon redondante (et incohérente)
- Compatibilité arrière
- Manipulation des préparations
- ... et beaucoup d'autres ...

````
`````


### Éditeurs de marquage (IDE)

De nombreux éditeurs de texte fournissent *Markdown* add-ons et *Markdown*-seulement les éditeurs perdent de plus en plus leur signification. Les éditeurs qui prennent simultanément en charge *Markdown* et les langages de programmation comme *Python* ou *R* sont à la fine pointe et donc recommandés.

Les éditeurs de texte de base qui supportent *Markdown* sont listés {ref}`here <npp>`. Les fichiers populaires et multi-plateformes *IDE* pour l'édition *Markdown* (`.md`) sont {ref}`jupyter` ou {ref}`pycharm`.

### Aperçu de la commande Markdown et mise en œuvre de l'image

Le tableau et les sections suivants donnent un aperçu des commandes de base. Il ya beaucoup plus d'options là-bas, que vous pouvez trouver en utilisant votre moteur de recherche préféré avec les mots clés `markdown` `guide`.

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

### Itemisation (listes non numérotées)

Une section de liste détaillée peut être produite en utilisant `*`, `+`, ou `-` symboles avec des onglets qui déterminent l'indentation de la liste:

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

* Niveau 1 poste
    - Niveau 2 poste
    - un autre article de niveau 2
        + Poste de niveau 3
* prochain point de niveau 1

````
`````

### Tableaux

Les colonnes de tableau sont séparées par un signe `|`. La première ligne détermine les en-têtes de lignes et la deuxième ligne l'alignement par l'utilisation de `:` (voir l'exemple ci-dessous).

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

Royaume des fruits
- C'est quoi ?
Massa
Jackfruits Plantae Artocarpus

````
`````

Converting complex tables from workbooks (e.g., from *LibreOffice Calc* or *MS Excel*) is possible with many online tools, and here is just one example from Dave Johnson: [https://thisDaveJ.com](https://thisdavej.com/copy-table-in-excel-and-paste-as-a-markdown-table/).

### Expressions mathématiques : équations

Les expressions et équations mathématiques peuvent être implémentées en utilisant des signes $, semblables à *LaTeX*.

## Html - Marquage
*html* structures peuvent être utilisés sans faille dans *Markdown*, qui n'est rien d'autre que simplifié *html*. Par conséquent, toute structure *html* peut être utilisée dans le balisage et l'implémentation de l'équation ci-dessus représente déjà le premier exemple d'utilisation *html* dans un document *Markdown*. Les sections suivantes donnent un aperçu de certains symboles *html* plus ou moins fréquemment utilisés qui fonctionnent également avec *Markdown*.

### Lettres grecques

Pour utiliser les lettres grecques dans le texte en ligne, utilisez la langue *html*, où `&lettername;` produit le symbole de la lettre souhaitée *Greek* (par exemple, tapez `&delta;` à sortie &delta; ou `&Delta;` pour produire une lettre majuscule &Delta;). Le tableau suivant donne un aperçu des symboles grecs.

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

### Flèches et opérateurs

Les flèches et les opérateurs peuvent également être implémentés sous forme de symboles *html*. Le tableau suivant donne un aperçu.

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


### Symboles divers

*Markdown* bénéficie de beaucoup plus de symboles *html* qui peuvent être utilisés dans des équations ou d'autres textes. Le tableau suivant donne un aperçu de ces symboles divers.

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

Alors que chaque dépôt {ref}`git <chpt-git>` devrait au moins contenir un descriptif *README.md*, *wiki* fournit beaucoup plus de détails et de conseils. Les Wikis sont une façon pratique de guider les utilisateurs avec des sidebars permanents (comme la barre de menus sur ce site), aider les utilisateurs à comprendre les méthodes et les codes, et le codage collaboratif avec des descriptions précises des scripts. *Les utilisateurs de GitHub* trouvent des options pour activer *wiki*s dans l'onglet *Settings* d'un dépôt et les développeurs continuent d'améliorer les fonctions de *wiki* ([en savoir plus sur les wikis de *GitHub*](https://help.github.com/en/github/building-a-strong-community/about-wikis)).

Des *wiki* plus sophistiqués sont disponibles sur le site Web des thèmes *Jekyll* (p. ex., le thème [git-wiki](https://jekyll-themes.com/git-wiki/)). Pour utiliser les thèmes *Jekyll*, assurez-vous d'activer [*GitHub* pages](https://help.github.com/en/github/working-with-github-pages/creating-a-github-pages-site) (dans le dépôt *Settings* onglet) pour le dépôt où vous voulez établir le *wiki* (ce dépôt wiki est généralement un autre dépôt pour décrire un dépôt de code). Ensuite, installez l'environnement de développement *Ruby* et *Jekyll* (voir [instructions sur leur site](https://jekyllrb.com/docs/) pour accéder et construire des centaines de thèmes pour la documentation de code et de projet. Des thèmes fourrés et adaptés localement peuvent alors être *poussés* vers un dépôt *wiki* distant en utilisant {ref}`git <chpt-git>`.

```{tip}
Il y a d'autres fournisseurs de services git-services et de wiki, comme [GitLab](https://gitlab.com/pages) ou [plan.io](https://plan.io/knowledge-management/).
```

```{admonition} Exercise
Faites de la pratique avec l'exercice [markdown and git](../exercises/ex-git).
```

(rst)=
## reStructuredText, Sphinx et readthedocs

Une alternative au balisage est [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html) qui permet d'intégrer *Python docstrings* (en savoir plus sur {ref}`chpt-style`) dans n'importe quel script avec [*Sphinx*](https://www.sphinx-doc.org).

Sans *Python* ou connaissance de programmation, il pourrait être difficile de commencer avec *Sphinx*. Assurez-vous donc de comprendre les bases de *Python* et de documenter tout code avec *docstrings*, au mieux en utilisant [*google style*](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) formating. Une fois que vous commencez à documenter votre premier paquet *Python*, *Google-style* *docstrings* permettra la génération rapide de documents de haute qualité. À l'heure actuelle, l'une des meilleures options pour la production partielle de documentation de code, pour tout langage de programmation, est [*readthedocs*](https://readthedocs.org/), qui s'appuie sur *Sphinx* et *reStructuredText*.

[wiki] : https://wikipedia.org
