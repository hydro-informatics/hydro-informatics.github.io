---
description: Configurer le transport de sédiments en charge de fond en TELEMAC-GAIA en utilisant la formule Meyer-Peter et Müller, le paramètre Shields et la contrainte de cisaillement de lit sans dimension pour la modélisation morphodynamique de la rivière 2D.
---

(gaia-bl)=
# Charge de fond


```{admonition} Bedload basics
:class: important

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/e6lk2pk72Gc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>Bedload traveling in a lab flume by jumping, rolling, and sliding (under water footage). Source: Sebastian Schwindt<a href="https://www.youtube.com/@hydroinformatics">@ Hydro-Morphodynamics channel on YouTube</a>.</p>


Pour une meilleure expérience d'apprentissage, le {ref}`glossary` aide à expliquer les termes {term}`Transport solide <Sediment transport>`, (dimensionless) {term}`charge de fond <Bedload>` transport $\Phi_b$, {term}`Cisaillement adimensionel <Dimensionless bed shear stress>` $\tau_{x}$, et le {term}`Shields parameter` $\tau_{x,cr}$ (dans cet ordre).
```

```{admonition} Sediment replenishment, gravel augmentation, bedload addition (etc.)
:class: tip

Le placement de sédiments plus grossiers pour la restauration du transport de la charge de fond peut prendre de nombreuses formes différentes et est décrit par un large éventail de termes. Dans TELEMAC, la meilleure option pour simuler ces efforts de restauration de la charge de fond est le module [**Nestor**](http://www.opentelemac.org/index.php/modules-list/163-dredgesim-modeling-dredging-operations-in-the-river-bed) qui nécessite Gaia (ou SISYPHE). En savoir plus dans le plus récent [Manuel du Nestor](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/nestor/user/nestor_user_9.0.pdf).
```

(bl-principles)=
## Principes

Le calcul du transport {term}`charge de fond <Bedload>` nécessite des connaissances spécialisées sur l'écosystème modélisé pour déterminer si le système est limité par l'offre de sédiments ou par la capacité de transport limitée {cite:p}`church_morphodynamics_2015`.

L'approvisionnement en sédiments est limité
: Une rivière limitée à l'approvisionnement en sédiments se caractérise par des tendances d'incision clairement visibles indiquant que le débit pourrait potentiellement transporter plus de sédiments que ce qui est disponible dans la rivière. Les sections fluviales limitées se trouvent généralement en aval des barrages, qui constituent une barrière insurmontable pour les sédiments. Ainsi, dans un cours d'eau limité à l'approvisionnement, la compétence **de débit** (force hydrodynamique ou capacité de transport**) est insuffisante pour mobiliser un lit de rivière généralement grossier, mais elle est suffisante pour transporter l'approvisionnement externe en sédiments.

Rivières à capacité limitée (alluviale)
: Une rivière à capacité limitée de transport se caractérise par l'abondance des sédiments où le débit est trop faible pour transporter tous les sédiments disponibles pendant une inondation. Les accumulations de sédiments (c.-à-d. l'alluvium) sont présentes et le canal tend à se tresser à {term}`anabranches <Anabranch>` (ou à l'anastomose dans des environnements fins/dominés par les sables). Ainsi, la compétence **flow** (ou **capacité de transport**) est insuffisante pour transporter la totalité des sédiments disponibles (approvisionnement externe et lit de rivière).

```{admonition} Limitation types vary in space and in time
:class: important
Les types de chenal peuvent varier fortement dans l'espace entre les sections ou les segments de rivière et dans le temps. Par exemple, la même section de rivière qui semble être limitée par l'offre en raison d'une compétence insuffisante en matière de débit peut se transformer en section limitée par la capacité de transport lors d'une inondation lorsque les débits élevés exercent des contraintes de cisaillement élevées sur le lit de la rivière. La variation spatio-temporelle des types de limitation du transport est particulièrement marquée dans les écosystèmes riverains sains proches du recensement, qui s'ajustent perpétuellement à un équilibre morphodynamique.
```

Les chiffres ci-dessous illustrent les tronçons de la rivière limitée à l'approvisionnement en sédiments et la portée de la rivière limitée à la capacité de transport.

`````{tab-set}
````{tab-item} Artificially sediment supply-limited
```{figure} ../../img/nature/doubs-capacity-2015.JPG
:height: 350px
:alt: channel doubs france sediment supply transport limited
:name: doubs-2015

Le Doubs en Franche-Comté (France) lors d'une petite inondation. L'approvisionnement en sédiments est interrompu par une cascade de barrages en amont avec la conséquence d'un chenal monotone droit avec une croissance importante de la plante le long des rives. Le lit de rivière se compose principalement de blocs qui sont immobiles la plupart du temps. Ainsi, la section fluviale peut être qualifiée de limite artificielle de l'approvisionnement en sédiments (photo : Sebastian Schwindt 2015).
```
````

````{tab-item} Naturally sediment supply-limited
```{figure} ../../img/nature/krimmler-ache-2010.jpg
:height: 350px
:alt: naturally channel krimmler ache austria sediment supply transport limited
:name: krimml-2010
:class: with-shadow

Le Krimmler Ache en Autriche lors d'une petite inondation. Même si le bassin versant a une haute {term}`Apport solide <Sediment yield>`, la capacité de transport de l'eau dans cette section de rivière est si élevée que le lit de rivière est principalement constitué de gros blocs. Ainsi, la section de la rivière peut être qualifiée de limite naturelle d'approvisionnement en sédiments (photo: Sebastian Schwindt 2010).
```
````

````{tab-item} Capacity-limited
```{figure} ../../img/nature/jenbach-alluvial-2020.jpg
:height: 350px
:alt: alluvial channel jenbach sediment supply transport limited
:name: jenbach-2020

Le Jenbach dans les Alpes bavaroises (Allemagne) après une intense approvisionnement en sédiments naturels dans une portée en amont sous forme de glissement de terrain. La section fluviale peut être qualifiée de capacité de transport limitée (photo: Sebastian Schwindt 2020).
```
````
`````

**Pourquoi la différenciation entre l'approvisionnement en sédiments et la capacité de transport limitée des rivières est-elle importante pour la modélisation numérique?**

Gaia fournit différentes formules pour le calcul du transport de la charge de fond, qui sont partiellement dérivées d'expériences de laboratoire avec un approvisionnement infini en sédiments (par exemple, la formule {cite:t}`meyer-peter_formulas_1948` et ses dérivés, voir {ref}`below <gaia-mpm>`) ou de mesures sur le terrain dans des rivières partiellement limitées en capacité de transport (par exemple, {cite:t}`wilcock_critical_1993`). Les formules qui tiennent compte de l'approvisionnement limité en sédiments impliquent souvent un facteur de correction pour le {term}`Shields parameter`.

## Formules et paramètres

{term}`charge de fond <Bedload>` est généralement désigné par $q_b$ (en kg$\cdot$s$^{-1}\cdot$m$^{-1}$ i.e. poids par unité temps et largeur) et tient compte du transport des particules sous forme de déplacement de laminage, de glissement et/ou de saut de particules grossières. Dans l'hydraulique fluviale, le soi-disant {term}`Cisaillement adimensionel <Dimensionless bed shear stress>`, également appelé {term}`Shields parameter` {cite:p}`shields_anwendung_1936`, est souvent utilisé comme valeur seuil pour la mobilisation des sédiments du lit de rivière. TELEMAC et Gaia s'appuient sur une expression sans dimension de l'intensité de transport de la charge de fond selon {cite:t}`einstein_bed-load_1950`:

$$
\Phi_b = \frac{q_b}{\rho_{s} \sqrt{(s - 1) g D^{3}_{pq}}}
$$ (eq-phi-gaia)

où $\rho_{s}$ est la densité des grains de sédiments; $s$ est le rapport entre la densité des grains de sédiments et celle de l'eau (typiquement 2,68) {cite:p}`schwindt_hydro-morphological_2017`; $g$ est l'accélération gravitationnelle; et $D_{pq}$ est le diamètre caractéristique des grains de la classe des sédiments (cf. {ref}`gaia-sed`). Notez que l'expression sans dimension $\Phi$ et l'expression dimensionnelle $q_{b}$ représentent la charge de fond unitaire (c.-à-d. la charge de fond normalisée par une unité de largeur). **Les sorties Gaia sont dimensionnelles et correspondent à $q_{b}$** (rappelez les définitions **VARIABLES POUR PRINTOUTS GRAPHIQUES** dans le {ref}`General Parameters section <gaia-gen>`) où l'unité de largeur correspond à la longueur de bord d'une cellule de maille numérique sur laquelle les flux de masse sont calculés.

```{admonition} Gaia computes bedload in mass transport rate
:class: note
Contrairement au SISYPHE, Gaia calcule les flux de charge de fond en termes de vitesse de transport (sec) en masse par unité de largeur, sans pores. Le calcul numérique des flux de sédiments en termes de masse sèche minimise l'erreur d'arrondi, en particulier pour les algorithmes de transfert de masse utilisés pour le modèle de couche de lit.
```

```{admonition} Comment on the Original Einstein (1950) Expression
:class: dropdown
L'équation originale pour $\Phi_b$ se trouve à la page 34 (équation 42) à {cite:t}`einstein_bed-load_1950`. Cette formule implique une division supplémentaire par l'accélération gravitationnelle $g$, qui n'apparaît pas dans les références ultérieures à l'expression d'Einstein $\Phi_b$ et n'entraînerait pas non plus un terme sans dimension. Pour cette raison, l'équation {eq}`eq-phi-gaia` est adaptée ici.
```

L'équation {eq}`eq-phi-gaia` n'exprime que la conversion dimensionnelle pour le transport par charriage (c.-à-d. la façon dont les dimensions sont enlevées ou ajoutées au transport des sédiments). En fait, ce n'est que la première étape pour résoudre l'autre côté d'une équation de charge de fond à l'aide d'une formule empirique (semi-). Pour calculer $\Phi_{b}$, Gaia fournit un ensemble de formules empiriques (semi-) qui peuvent être modifiées avec les fichiers de Fortran de l'utilisateur et définies dans le fichier de pilotage de Gaia avec la formule **BED-LOAD TRANSPORT FOR ALL SANDS** `integer` mot clé. {numref}`Table %s <tab-gaia-bl-formulae>` liste les entiers possibles pour le mot clé pour définir une formule de transport de charge de fond, y compris les références aux publications originales, les gammes d'applications de formule, et les noms des fichiers source Fortran pour les modifications.

```{csv-table} *Bedload transport formulae implemented in Gaia with application limits regarding the grain diameter $D$, **cross section-averaged** Froude number $Fr$, slope $S$, water depth $h$, and flow velocity $u$. The Fortran files live in the /telemac/sources/gaia/ directory.*
:header: Gaia, Author(s), $D$, "*{term}`Fr <Froude number>`*; $S$; $h$; and $u$", User Fortran
:header-rows: 1
:name: tab-gaia-bl-formulae
 "(no.)", "(ref.)", "(10$^{-3}$m)", "(-); (-); (m); (m/s)", "(file name)"
 `1`, "{cite:t}`meyer-peter_formulas_1948`", 0.4 $<D_{50}<$28.6, "10$^{-4}<Fr<$639<br> 0.0004$<S<$0.02<br>0.01$<h<$1.2<br>0.2$<u$", bedload_meyer.f
 `2`, "{cite:t}`einstein_bed-load_1950`-{cite:t}`brown1949`", 0.25$<D_{35}<$32, "", bedload_einst.f
 `3`, "{cite:t}`engelund_monograph_1967` + {cite:t}`chollet1979`", 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", bedload_engel_cc.f
 `7`, {cite:t}`van_rijn_sediment_1984`, 0.6$<D_{50}<$2.0, "0.5$<h$<br>0.2$<u$", bedload_vanrijn.f
 `10`, {cite:t}`wilcock2003`,"0.063 $\lesssim D_{pq}$", "", bedload_wilcock_crowe.f
 `30`, "{cite:t}`engelund_monograph_1967`", 0.15$<D_{50}<$5.0, "0.1$<Fr<$10", bedload_engel.f
```

**Note** que les formules Engelund-Hansen (options `3` et `30`) calculent ** transport total des sédiments**, c'est-à-dire la somme de la charge de fond et de la charge en suspension. Ainsi, lorsque vous utilisez ces formules, n'activez pas en outre la modélisation de charge en suspension pour éviter le double comptage.

Pour utiliser la formule {cite:t}`meyer-peter_formulas_1948` (`1` selon {numref}`Tab. %s <tab-gaia-bl-formulae>`) dans ce tutoriel, **ajouter la ligne suivante au fichier de pilotage gaia-morphdynamique.cas** :

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
/
BED LOAD FOR ALL SANDS : YES / deactivate with NO
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1
```

Les sections suivantes fournissent plus de détails sur la façon dont $\Phi_{b}$ est calculé avec les formules prédéfinies énumérées à {numref}`Tab. %s <tab-gaia-bl-formulae>`.

```{admonition} User-defined Bedload transport formulae in a specific Fortran file
:class: tip
Les utilisateurs peuvent ajouter plus de formules de transport de charge en ajoutant une copie modifiée d'un modèle de fichier FORTRAN. Le [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) explique la procédure à suivre pour ajouter une nouvelle formule de charge de fond définie par l'utilisateur en détail à la section 6.3.
```

```{admonition} User Fortran Files
:class: note, dropdown
Pour implémenter un fichier utilisateur Fortran, copiez le fichier original TELEMAC Fortran du répertoire `/telemac/sources/` (p. ex., `/telemac/sources/gaia/bedload_einst.f`) au répertoire du projet (p. ex., `/telemac/simulations/gaia-tutorial/user_fortran/bedload_einst.f`). Enfin, indiquez à TELEMAC où chercher les fichiers Fortran utilisateurs en définissant le mot clé suivant dans un fichier de direction (par exemple, à `gaia-morphodynamics.cas`):

`FORTRAN FILE : 'user_fortran'`
```

(gaia-mpm)=
### Meyer-Peter et Müller (1948)

```{admonition} Recall the validity range for the MPM formula (1)
:class: warning
Réviser {numref}`Tab. %s <tab-gaia-bl-formulae>` pour s'assurer que l'application est dans la gamme de paramètres applicable correspondant aux conditions dans lesquelles la formule a été développée.
```

La formule {cite:t}`meyer-peter_formulas_1948` a été publiée en 1948 par les chercheurs suisses Eugen Meyer-Peter, professeur à [ETH Zurich](https://ethz.ch/en.html) et fondateur du laboratoire hydraulique de l'école (le célèbre [VAW](https://vaw.ethz.ch/)] de Zurich) et Robert Müller. Leur formule empirique est le résultat de plus d'une décennie de collaboration et l'élaboration a commencé un an après la création de la VAW en 1931 lorsque Robert Müller a été nommé assistant d'Eugen Meyer-Peter. Les deux scientifiques ont également travaillé avec Henry Favre et Hans-Albert Einstein qui ont trouvé une autre approche pour calculer la charge de fond. Une première version de la formule {cite:t}`meyer-peter_formulas_1948` a été publiée en 1934 et c'est la base de nombreuses autres formules qui font référence à une formule critique {term}`Cisaillement adimensionel <Dimensionless bed shear stress>` (i.e., {term}`Shields parameter`). Il est important de se rappeler que la formule est basée sur des données provenant d'expériences de flume en laboratoire avec un apport élevé de sédiments. C'est pourquoi le transport par charriage calculé avec la formule {cite:t}`meyer-peter_formulas_1948` correspond au {ref}`hydraulic transport capacity <bl-principles>` d'un canal alluvial. Ainsi, la formule {cite:t}`meyer-peter_formulas_1948` a tendance à surestimer le transport de la charge de fond** et elle est conçue de manière intrinsèque pour estimer la charge de fond ** sur la base d'un hydraulique simplifié à la moyenne de la section 1d** (voir aussi la formule {ref}`Python sediment transport exercise <ex-py-sediment>`). On peut s'attendre à de bons résultats lorsque les débits d'inondation sont simulés dans une section de rivière alluviale.

Finalement, le côté gauche de l'équation {eq}`eq-phi-gaia` ($\Phi_b$) peut être calculé avec la formule {cite:t}`meyer-peter_formulas_1948` comme suit:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x,cr} > \tau_{x} \\ f_{mpm} \cdot (\tau_{x} - \tau_{x,cr})^{3/2} & \mbox{ if } \tau_{x,cr} \leq \tau_{x}\end{cases}
$$ (eq-mpm)

où $f_{mpm}$ est le coefficient MPM (par défaut 8), $\tau_{x,cr}$ indique le {term}`Shields parameter` ($\approx$ 0.047 et jusqu'à 0,07 dans les rivières de montagne), et $\tau_{x}$ est le {term}`Cisaillement adimensionel <Dimensionless bed shear stress>`. Lorsque vous utilisez la formule {cite:t}`meyer-peter_formulas_1948` avec Gaia, la cohérence avec les publications originales est ** assurée en définissant $\tau_{x,cr}$ et $f_{mpm}$ dans le dossier de pilotage**:

```fortran
/ continued: gaia-morphodynamics.cas
/
/ BEDLOAD
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 1 / see above
CLASSES SHIELDS PARAMETERS : 0.047;0.047;0.047
MPM COEFFICIENT : 8
```

````{admonition} Wong-Parker correction of the MPM formula
La correction de Wong-Parker {cite:p}`wong_reanalysis_2006` pour la formule {cite:t}`meyer-peter_formulas_1948` se réfère à une ré-analyse statistique des ensembles de données expérimentaux originaux et s'applique aux sections {term}`Plane bed` River. À cette fin, la correction de Wong-Parker donne des valeurs de transport de charge de fond plus faibles et exclut la correction de glisser de forme de la formule originale avec l'expression suivante : $\Phi_{b} \approx 3.97 \cdot (\tau_{x} - 0.0495)^{3/2}$. Ainsi, pour mettre en œuvre la correction Wong-Parker dans Gaia utiliser:

```fortran
CLASSES SHIELDS PARAMETERS : 0.0495;0.0495;0.0495
MPM COEFFICIENT : 3.97
```
````

**Pour continuer directement avec le tutoriel en utilisant la formule {cite:t}`meyer-peter_formulas_1948`, sautez à la section {ref}`correction factors <c-factors>`.**

(gaia-einstein)=
### Einstein-Brown (1942-49)

```{admonition} Recall the validity range for the Einstein-Brown formula (2)
:class: warning
Réviser {numref}`Tab. %s <tab-gaia-bl-formulae>` pour s'assurer que l'application est dans la gamme de paramètres applicable correspondant aux conditions dans lesquelles la formule a été développée.
```

Hans Albert Einstein, fils du célèbre Albert Einstein, était un pionnier des analyses basées sur la probabilité du transport des sédiments. En particulier, il a émis l'hypothèse que le début et la fin du mouvement des sédiments peuvent être exprimés en termes de probabilités. De plus, Einstein a supposé que le mouvement des sédiments est une série de déplacements progressifs suivis de périodes de repos et que la distance moyenne d'un déplacement des particules est environ cent fois le diamètre des particules (grains). De plus, pour tenir compte des observations qu'il a faites dans des expériences de flume en laboratoire, Einstein a introduit des coefficients de correction de cache et de levage {cite:p}`einstein1942`.

The Einstein formula differs from any {cite:t}`meyer-peter_formulas_1948`-based formula in that it does not imply a threshold for incipient motion of sediment. However, despite or because Einstein's sediment transport theory is more complex than many other bedload transport formulae, it did not become very popular in engineering applications. Today, Gaia enables the user-friendly application of Einstein's formula, which was similarly presented by {cite:t}`brown1949` at an engineering hydraulic conference in 1949. According to {cite:t}`einstein1942`-{cite:t}`brown1949`, the left side of Equation {eq}`eq-phi-gaia` ($\Phi_b$) is calculated as follows:

$$
\Phi_b = \begin{cases} 0 & \mbox{ if } \tau_{x} < 0.0025 \\ F_{eb}\cdot 2.15 \cdot \exp{(-0.391/\tau_{x})} & \mbox{ if } 0.0025 \leq \tau_{x} \leq 0.2\\ F_{eb} \cdot  40 \cdot \tau_{x}^{3} & \mbox{ if } \tau_{x} > 0.2\end{cases}
$$ (eq-einstein-brown)

où

$$
F_{eb} = \left(\frac{2}{3} + \frac{36}{D_x}\right)^{0.5} - \left(\frac{36}{D_x}\right)^{0.5}
$$ (eq-f-eb)

$D_x$ est le diamètre des particules sans dimension calculé comme suit:

$$
D_x = \left[\frac{(s-1)\cdot g}{\nu^2}\right]^{1/3}\cdot D_{pq}
$$ (eq-d-dimless)

où $s$ est le rapport entre le grain de sédiments et la densité de l'eau (typiquement 2,68); $g$ est l'accélération gravitationnelle; et $\nu$ est la viscosité cinématique de l'eau ($\approx$10$^{-6}$m$^{2}$ s$^{-1}$) {cite:p}`schwindt_hydro-morphological_2017`.

To use the {cite:t}`einstein1942`-{cite:t}`brown1949` formulae in Gaia use:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 2
```

```{admonition} Consider adapting bedload_einst.f
The application thresholds as a function of $\tau_{x}$ stem from the Gaia Fortran file `bedload_einst.f` in `/telemac/sources/gaia/`. However, the original {cite:t}`einstein1942`-{cite:t}`brown1949` publications suggest a threshold of $\tau_{x}$=0.182 (rather than 0.2) for switching the formula cases.
```


(gaia-engelund)=
### Engelund-Hansen (1967) / Chollet-Cunge

```{admonition} Recall the validity range for the Engelund-Hansen formulae (3 and 30)
:class: warning
Réviser {numref}`Tab. %s <tab-gaia-bl-formulae>` pour s'assurer que l'application est dans la gamme de paramètres applicable correspondant aux conditions dans lesquelles la formule a été développée. Notez que ces formules calculent ** transport total des sédiments** (charge de fond + charge en suspension).
```

La formule {cite:t}`engelund_monograph_1967` comptabilise le transport total des sédiments, y compris {term}`charge de fond <Bedload>` et {term}`charge en suspension <Suspended load>`. À partir de l'approche de la puissance de Bagnold {cite:p}`bagnold_approach_1966,bagnold_empirical_1980`, la formule {cite:t}`engelund_monograph_1967` a été développée pour les calculs du transport des sédiments sur les lits des canaux de dunes. L'approche tient compte des pertes d'énergie nécessaires à la montée des particules sur les dunes du lit de la rivière. La théorie {cite:t}`bagnold_approach_1966` considère le cisaillement total comme la somme du cisaillement transmis entre les grains et le fluide, et le cisaillement transmis par les changements d'impulsion causés par les collisions intergranulaires. Ainsi, l'érosion a lieu tant que le {term}`Cisaillement adimensionel <Dimensionless bed shear stress>` est supérieur ou égal à sa valeur critique (c.-à-d. le {term}`Shields parameter`). Gaia implémente le {cite:t}`engelund_monograph_1967` en calculant le côté gauche de l'équation {eq}`eq-phi-gaia` ($\Phi_b$) comme suit :

$$
\Phi_b = 0.1\cdot \frac{\tau_{x}^{2.5}}{c_f}
$$ (eq-engelund)

où $c_f$ est un coefficient de frottement dimensionnel et $\tau_x$ est le numéro Shields sans le facteur de correction de frottement de la peau. En savoir plus sur la friction cutanée dans la section {ref}`correction factors <c-friction>`. Pour utiliser la formule originale {cite:t}`engelund_monograph_1967` dans Gaia utiliser:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 30
```

En outre, {cite:t}`chollet1979` a introduit une fonction par étapes pour le calcul d'un paramètre Shields modifié $\tau^*_x$ qui tient compte de différents régimes de transport:

$$
\tau^*_x = \begin{cases} 0 & \mbox{ if } \tau_{x} \leq 0.06 & \mbox{ (no transport)}\\ [2.5 (\tau_{x} - 0.06)]^{0.5} & \mbox{ if } 0.06 < \tau_{x} < 0.384  & \mbox{ (dune regime)} \\ 1.066\cdot \tau_{x}^{0.176} & \mbox{ if } 0.384 < \tau_{x} < 1.08  & \mbox{ (transition regime)} \\ \tau_{x} & \mbox{ if } 1.08 \leq \tau_{x}  & \mbox{ (sheet flow)} \end{cases}
$$ (eq-f-eh)

Pour appliquer la modification {cite:t}`chollet1979` de la formule {cite:t}`engelund_monograph_1967` utiliser:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 3
```

(gaia-rijn)=
### (1984)

```{admonition} Recall the validity range for the van-Rijn formula (7)
:class: warning
Réviser {numref}`Tab. %s <tab-gaia-bl-formulae>` pour s'assurer que l'application est dans la gamme de paramètres applicable correspondant aux conditions dans lesquelles la formule a été développée.
```

La formule de transport des sédiments de Leo van Rijn {cite:p}`van_rijn_sediment_1984` s'inspire des théories de {cite:t}`bagnold_empirical_1980`, {cite:t}`einstein1942`, et {cite:t}`ackers_sediment_1973`. Les formules {cite:t}`van_rijn_sediment_1984` supposent que la charge de fond est dominée par la gravité tandis que le transport de charge en suspension est contrôlé par la turbulence selon {cite:t}`bagnold_empirical_1980`. À cette fin, les formules {cite:t}`van_rijn_sediment_1984` calculent le transport de charge de fond comme {cite:t}`ackers_sediment_1973` où les taux de transport dépendent des vitesses de frottement. Pour étalonner son modèle de transport solide près du lit (charge de fond), {cite:t}`van_rijn_sediment_1984` a utilisé des données d'expériences sur des canaux à lit plat (pente zéro) avec un diamètre moyen de grain de sédiments de 1,8 mm. {cite:t}`van_rijn_sediment_1984` a mené des expériences supplémentaires pour vérifier les résultats de son modèle contre différents diamètres de grain entre 0,2 et 2 mm. En outre, {cite:t}`van_rijn_sediment_1984` a établi des critères de suspension des sédiments basés sur des expériences en laboratoire avec des diamètres de grains inférieurs à 0,5 mm et en simplifiant empiriquement les paramètres d'étalonnage. Alors que la formule originale {cite:t}`van_rijn_sediment_1984` comptabilise le transport total des sédiments (c.-à-d., {term}`charge de fond <Bedload>` et {term}`charge en suspension <Suspended load>`), les explications suivantes pour la mise en œuvre à Gaia sont limitées à {term}`charge de fond <Bedload>` seulement.

Selon {cite:t}`van_rijn_sediment_1984`, le côté gauche de l'équation {eq}`eq-phi-gaia` ($\Phi_b$) est calculé comme suit :

$$
\Phi_b = \frac{0.053}{D_{x}^{0.3}} \cdot \left(\frac{\tau_{x} - \tau_{x,cr}}{\tau_{x,cr}}\right)^{2.1}
$$ (eq-rijn)

Explanations of the {term}`Cisaillement adimensionel <Dimensionless bed shear stress>` $\tau_{x}$, its critical value $\tau_{x,cr}$ (i.e., the {term}`Shields parameter`), and the dimensionless grain diameter $D_{x}$ are provided in the above sections on the {ref}`Meyer-Peter and Müller <gaia-mpm>` and the {ref}`Einstein-Brown <gaia-einstein>` formulae.

Pour utiliser la formule {cite:t}`van_rijn_sediment_1984` dans Gaia utiliser:

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 7
```

(gaia-wilcock)=
### Wilcock-Crowe (2003)

```{admonition} Applicability of the Wilcock-Crowe formula (10)
:class: warning
La formule de transport multi-fraction de la charge de fond de {cite:t}`wilcock2003` n'indique pas des plages de validité particulières, mais les auteurs limitent leur approche des sédiments sable-gravel-cobble d'un diamètre minimum de 0,063 mm. Les explications de cette section se limitent au fond de l'application de l'approche {cite:t}`wilcock2003`. L'ensemble complexe d'équations est expliqué en détail dans le [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) (section 3.1.2) et par {cite:t}`cordier2019,cordier2020`.
```

L'approche {cite:t}`wilcock2003` est un modèle de transport de sédiments à plusieurs fractions qui s'applique principalement aux sections de rivières blindées pour la modélisation de l'aggradation ou de la dégradation du lit. Le modèle est basé sur des études de surface et est particulièrement adapté pour prédire les conditions transitoires de l'armure de lit. Elle tient compte de la répartition de la surface du lit (des sables les plus fins aux graviers les plus grossiers) et a été étalonnée à l'aide d'un total de 49 expériences de flume avec des rejets de petites à grandes eaux et cinq mélanges de sédiments différents.

L'approche reprend l'idée de {cite:t}`parker1990` sur l'application d'une contrainte de cisaillement de référence à laquelle on peut observer une vitesse de transport solide faible mais constante. La contrainte de cisaillement de référence est proche, mais un peu plus grande que le {term}`Shields parameter` $\tau_{x,cr}$. À cette fin, {cite:t}`wilcock2003` implémenter un taux de transport de référence de 0,002 comme proposé par {cite:t}`parker1990`.

De plus, le modèle multifraction {cite:t}`wilcock2003` utilise la distribution complète de la taille du grain de sédiments de la surface du lit de rivière et calcule le transport de la charge de fond pour chacune des classes de taille du grain spécifiées. Le modèle de transport des sédiments s'appuie sur les expériences de flume de {cite:t}`proffitt1983` et {cite:t}`parker1990`, et il explique les effets de cache/exposition sur le transport du gravier en fonction de la fraction de sable dans le lit de la rivière. La fonction de cache-exposition est conçue pour résoudre les divergences observées lors d'expériences antérieures, y compris l'effet de cache-exposition de la teneur en sable sur le transport de gravier pour des valeurs faibles à élevées de la teneur en sable en vrac.

En bref, le modèle {cite:t}`wilcock2003` représente un développement ultérieur de la formule {cite:t}`meyer-peter_formulas_1948`, reprend l'implémentation d'un taux de transport de référence {cite:p}`parker1990`, et il est étalonné pour cacher/exposer les effets en fonction de la fraction de sable.

Pour utiliser la formule {cite:t}`wilcock2003` dans Gaia, définissez plusieurs {ref}`sediment classes <gaia-sed>` et utilisez :

```fortran
BED-LOAD TRANSPORT FORMULA FOR ALL SANDS : 10
```

(c-factors)=
## Facteurs de correction

Des facteurs de correction pour le transport des sédiments peuvent être nécessaires pour tenir compte de la pente du chenal transversal, des courants secondaires ou de la correction du frottement cutané.

(c-friction)=
### Correcteurs de friction

La friction est souvent envisagée avec des approches simplifiées qui assemblent la friction de la peau et forment la traînée, mais dans un modèle bidimensionnel, seule la friction de la peau affecte la charge de fond. {cite:t}`einstein_bed-load_1950` compte pour la friction cutanée avec un facteur de correction $\mu$ pour la contrainte de cisaillement (dimensionnelle) du lit $\tau$:

$$
\tau' = \mu \cdot \tau
$$ (eq-tau-fr)

```{admonition} How Telemac2d calculates $\tau$
Telemac2d uses the length of the $x$-$y$ velocity vectors to calculate $\tau$ with the user-defined `FRICTION COEFFICIENT` $c_{f}$: $\tau = 0.5\cdot \rho_{w}\cdot c_{f}\cdot (U^2 + V^2)$.
```

Le facteur de correction $\mu$ est défini comme le rapport entre le coefficient de frottement de la peau uniquement $c'_{f}$ et le coefficient de frottement global $c_{f}$ (c.-à-d., frottement de la peau grumelé et traînée):

$$
\mu = \frac{c'_{f}}{c_{f}}
$$ (eq-f-fr)

Le coefficient de frottement de la peau est calculé comme suit:

$$
c'_{f} = 2\cdot \left(\frac{\kappa}{\log(12 h/ k'_{s})}\right)^{2}
$$ (eq-cf-skin)

où $\kappa$ est la constante {cite:t}`von_karman_mechanische_1930` (0.4), $h$ est la profondeur de l'eau, et $k'_{s}$ est la longueur de rugosité représentative calculée comme $k'_s = \alpha_{ks} \cdot D_{50}$, où $\alpha_{ks}$ est un paramètre d'étalonnage (lire la section sur {ref}`bedload calibration <bl-calibration>`).

`````{tab-set}
````{tab-item} Skin Friction
Gaia utilise par défaut le coefficient de correction du frottement cutané qu'il dérive du solvant hydrodynamique (c.-à-d. Telemac2d/3d). Dans les eaux très peu profondes, ce comportement peut provoquer des instabilités. Par conséquent, le mot clé **SKIN FRICTION CORRECTION** peut être défini dans Gaia pour contrôler le calcul du facteur de correction:

* `0`: désactive la correction, le réglage $\mu = 1$ (la contrainte totale de cisaillement du lit de l'hydrodynamique est utilisée directement)
* `1`: permet la correction du frottement de peau (**par défaut**), le calcul $\mu$ selon les équations {eq}`eq-f-fr` et {eq}`eq-cf-skin`
* `2`: permet un prédicteur litforme qui comptabilise les ondulations lors du calcul $\mu$

Pour désactiver la correction de frottement de la peau (c.-à-d., définir $\mu$ à 1), ajouter ce qui suit au fichier de direction Gaia (non utilisé dans ce tutoriel):

```fortran
SKIN FRICTION CORRECTION : 0 / default is 1 to enable skin friction correction
```

Le coefficient $\alpha_{ks}$ (rapport entre la rugosité de la peau et le diamètre moyen) peut être modifié avec le mot-clé **RATIO ENTRE LA FRICTION DE LA PEAU ET LE DIAMETRE MEAN** (par défaut, 3.0). Pour en savoir plus à la section 3.1.8 du [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
````

````{tab-item} Bedform Roughness
Plus les sédiments du lit de la rivière sont fins, plus la turbulence créée par la forme du lit devient importante. Par exemple, la friction cutanée calculée sur la base d'un multiple du diamètre de la rugosité caractéristique du grain de sable $k'_{s}$ est très petite. Cependant, le sable a tendance à façonner le lit de la rivière en ondulations ou en dunes, ce qui provoque d'autres turbulences *bedform*, comme le montre la vidéo ci-dessous.

<iframe width="701" height="394" src="https://www.youtube-nocookie.com/embed/q4eRwyeLKfA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<p>by Sebastian Schwindt<a href="https://www.youtube.com/channel/UCGOMSGRrW5eLHiMn5Dfp7WQ">@ Hydro-Morphodynamics channel on YouTube</a>.</p>

Par défaut, Gaia ne tient pas compte des turbulences (c'est-à-dire des effets de rugosité) des formes de lit, mais il peut être activé en réglant le mot-clé **COMPUTE BED ROUGNESS AU SEDIMENT SCALE** à `YES` (par défaut est `NO`). Ensuite, l'une des options suivantes pour le mot-clé **BED ROUGHNESS PREDICTOR OPTION** peut être définie:

* `1` pour l'hypothèse d'un lit plat en utilisant l'approche par défaut de $k_s = \alpha_{ks} \cdot D_{50}$ (modifiée par **RATIO ENTRE LA FRICTION DE LA PEAU ET LE DIAMÈTRE MEAN**).
* `2` pour les formes de lit en ondulation. Pour les courants seulement, la rugosité est fonction du numéro de mobilité. Pour les ondes et les courants d'ondes combinés, les dimensions de la forme de lit sont calculées en fonction des paramètres d'onde suivant {cite:t}`wiberg1994`.
* `3` pour {cite:t}`rijn2007` prédire la rugosité totale du lit (courants seulement). La rugosité totale est décomposée en rugosité des grains, en rugosité à petite échelle, en composants méga-rapides et en rugosité des dunes.

Le [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) (section 3.1.9) résume l'ensemble des équations qui entrent dans le calcul de l'OPTION DE PRÉDICTEUR DE ROUTE **.

````
`````

(gaia-dir)=
### Direction et grandeur (intensité)

Natural rivers are characterized by non-straight lines of the {term}`talweg <Thalweg>`, which involves that water and sediment are subjected to curve effects. However, water and sediment behave differently in a curve because sediment has greater inertia than water {cite:p}`mosselman_five_2016`. Gaia accounts for the inertia of sediment transport as a function of water depth, curve radius, a spiral flow coefficient (`A`), and the depth-averaged, 2d velocities *U* and *V*. In addition, sediment transport reacts more inert to horizontal (transversal) channel slope and can be considered in $x$ and $y$ directions (see also the explanation of the {term}`Équation de Exner <Exner equation>`). To this end, Gaia calculates the slope-corrected unit bedload transport $q_{b,sc}$ as follows:

$$
q_{b,sc} = q_{b} \left[1 + \beta \left(\cos \alpha  \frac{\partial z_{b}}{\partial x} + \sin \alpha \frac{\partial z_{b}}{\partial y} \right)\right]
$$ (eq-qb-corr)

où $\alpha$ est l'angle entre l'axe longitudinal ($x$) et le vecteur de transport de la charge de fond (voir aussi {term}`Équation de Exner <Exner equation>`), $\beta$ est un facteur empirique de correction de l'intensité de la charge de fond de {cite:t}`koch1980`, et $z_{b}$ est l'élévation de la charge de fond de rivière.

Le degré de déviation de la charge de fond (via $\alpha$) et le facteur $\beta$ peuvent être définis en Gaia avec les mots-clés **FORMULA FOR DEVIATION** et **FORMULA FOR SLOPE EFFECT** (horizontal). Pour utiliser un ou les deux mots clés, le mot clé **SLOPE EFFECT** doit être défini à `YES` (par défaut est `YES`).

Le mot-clé **FORMULA FOR DEVIATION** peut prendre les valeurs entières suivantes pour définir une formule particulière pour la fonction de forme de sédiments (cf. section 3.1.4 dans [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)):

* `1` pour le calcul du niveau de lit selon {cite:t}`koch1980` (**par défaut**).
* `2` pour l'approche {cite:t}`talmon1995` basée sur des expériences en laboratoire, qui doivent être utilisées avec le mot-clé **PARAMETER FOR DEVIATION** pour définir le paramètre `BETA2` (son par défaut est `PARAMETER FOR DEVIATION : 0.85`, mais un optimum a été trouvé avec `1.6` {cite:p}`mendoza2017`).
* `3` pour l'approche {cite:t}`apsley2008bedload` basée sur le paramètre critique Shields et l'angle de frottement du sédiment, qui doit être utilisé avec le mot clé **FRICTION ANGLE DU SEDIMENT** (par défaut `40.`).

Le mot-clé **FORMULA FOR SLOPE EFFECT** affecte non seulement la direction du transport des sédiments, mais aussi la magnitude du lit (ou l'intensité) et peut prendre les valeurs suivantes:

* `1` pour le calcul du niveau de lit selon {cite:t}`koch1980` (**default** et similaire à FORMULA FOR DEVIATION). Le paramètre `1` permet de définir le facteur de correction de pente de lit empirique $\beta$ dans l'équation {eq}`eq-qb-corr` à travers le mot-clé **BETA** (par défaut `BETA : 1.3`).
  - Pour augmenter le changement d'élévation du lit, augmenter **BETA**.
  - Pour diminuer le changement d'élévation du lit, diminuer **BETA**.
* `2` pour la correction des pentes dans les rivières de sable basé sur une approche de {cite:t}`soulsby1997`, qui applique une correction de la {term}`Shields parameter` en fonction de l'angle de friction du sédiment et de la pente du lit de rivière. L'angle de frottement peut être défini avec le mot clé supplémentaire ** ANGLE DE LA FRICTION DU SEDIMENT** (par défaut `40.`).
* `3` pour l'approche {cite:t}`apsley2008bedload`, qui modifie à la fois le paramètre critique Shields et la contrainte de cisaillement efficace sans dimension. Utilisez le mot-clé **FRICTION ANGLE DU SEDIMENT**.

```{admonition} Sediment sliding
:class: tip
Si la pente de fond dépasse une pente critique (généralement l'angle de repos), les sédiments peuvent être déplacés en raison de processus géomécaniques. Gaia implémente le glissement des sédiments avec le mot clé **SEDIMENT SLIDE**:
* `0`: pas de glissement (**par défaut**)
* `1`: simple lissage de masse-conservateur des pentes de fond jusqu'à l'angle de repos
* `2`: formule d'avalanching de {cite:t}`apsley2008bedload`

Utilisez le mot-clé **FRICTION ANGLE DU SEDIMENT**.
```

(gaia-secondary)=
### Courants secondaires

Des courants secondaires peuvent se produire dans les chenaux incurvés (c.-à-d. dans la plupart des rivières naturelles proches du recensement) où l'eau se déplace comme un gyroscope à travers les virages des rivières. Plus précisément, les débits secondaires sont des mouvements hélicoïdaux dans lesquels l'eau près de la surface est conduite vers le virage extérieur, tandis que l'eau près du lit de la rivière est conduite vers le virage intérieur. Ainsi, les flux secondaires sont un phénomène 3d qui ne peut être représenté dans les modèles 2d qu'avec des approches auxiliaires. Pour le transport {term}`charge de fond <Bedload>`, le courant près du lit vers le virage intérieur est particulièrement important, car il favorise l'érosion au virage extérieur et peut conduire au dépôt au virage intérieur.

Par défaut, Telemac2d et Gaia ne considèrent pas les courants secondaires, mais une approche basée sur {cite:t}`engelund1974` peut être activée en définissant le mot-clé **CURRENTS SECONDAIRES** à `YES` (par défaut est `NO`). Dans Gaia, le coefficient de flux spirale $A$ est fixé à 7 (valeur d'Engelund). Le mot-clé **CURRENTS SECONDAIRES ALPHA COEFFICIENT** peut être utilisé pour modifier ce coefficient en fonction de la rugosité du bas du canal:

* `SECONDARY CURRENTS ALPHA COEFFICIENT : 0.75` pour une rivière très accidentée
* `SECONDARY CURRENTS ALPHA COEFFICIENT : 1.0` pour un lit de rivière lisse (**par défaut**)

Pour **cette utilisation du tutoriel**:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SECONDARY CURRENTS : YES
SECONDARY CURRENTS ALPHA COEFFICIENT : 0.8
```

(gaia-bc-bl)=
## Conditions limites

The {ref}`Gaia Basis section on boundary conditions <gaia-bc>` explains the geometric definition of open liquid boundaries in the `*.cli` files. To prescribe a bedload transport of **10 kg$\cdot$s$^{-1}$** (total solid discharge without pores) across the upstream (`LIEBOR=5`) boundary and free outflow at the downstream (`LIEBOR=4`) boundary, **add the PRESCRIBED SOLID DISCHARGES keyword to the Gaia steering file (gaia-morphodynamics.cas)**:

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
PRESCRIBED SOLID DISCHARGES : 10.;0.
```

Rappelons que les première et deuxième valeurs de la liste des rejets solides prescrits se rapportent aux première et deuxième limites ouvertes énumérées dans le `boundaries-gaia.cli`, respectivement (c.-à-d., en amont et en aval dans cet ordre).

```{admonition} Units for PRESCRIBED SOLID DISCHARGES
:class: important
Le mot-clé **PRESCRIBED SOLID DISCHARGES** spécifie la décharge totale solide en **kg/s** (masse par temps, pas par unité de largeur). C'est le flux de masse sèche sans tenir compte des pores. Lorsqu'une valeur est donnée par ce mot-clé, la colonne `Q2BOR` dans le fichier des conditions limites sert uniquement de forme de profil (les valeurs doivent être > 0 pour un profil constant, généralement défini à 1.0).
```

```{admonition} Distributing solid discharge among sediment classes
:class: tip
Lorsque de multiples classes de sédiments sont définies, le rejet solide peut être réparti entre elles en utilisant le mot clé **CLASSES IMPOSÉES DISTRIBUTION SOLIDE** (séquence des valeurs réelles séparées par des points-virgules, une par classe, somme à 1,0). Si ce mot-clé n'est pas utilisé, la décharge est répartie selon les rapports de sable calculés par Gaia.
```

Gaia can be run with liquid boundary files for assigning time-dependent solid discharges (the outflow should be kept in equilibrium). Solid discharge time series can be implemented using `455`-`5` boundary definitions, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. For more guidance, have a look at the *yen-2d* example (`telemac/examples/gaia/yen-2d`) featuring a quasi-steady bedload simulation at the Rhine River. In addition, more background information about the definition of bedload boundary conditions can be found in sections 3.1.10-3.1.12 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

## Exemples de demandes

Des exemples pour la mise en œuvre de bedload viennent avec l'installation TELEMAC (dans le répertoire `/telemac/examples/gaia/`). Les exemples suivants dans le calcul de la charge de fond `gaia/` dossier (pur) :

* Application du {ref}`Wilcock-Crowe formula <gaia-wilcock>` (classes de sédiments multiples) : **wilcock rowne-t2d/**
* Charge de fond dans un virage du Rhin avec des conditions d'écoulement quasi stables (non stables): **yen-2d/**
* Charge de fond couplée avec Telemac3d: **bosse-t3d/**
* Modèle de lit de rivière blindé (stratifié) : **guenter-t2d/**
* Transport côtier de sable (charge de fond) couplé au module de propagation des vagues Tomawac: **littoral-t2d-tom/**
* Couplage avec le module de dragage Nestor: **nestor dig test-t2d/**
* Résolveur de volume final avec décharge solide dépendante du temps dans un `*.liq`: **flume bc-t2d/**