---
description: Configurer le transport des sédiments en suspension dans TELEMAC-GAIA à l'aide d'équations advection-diffusion, de concentrations de traceurs et de fermetures de flux d'érosion-déposition pour la modélisation des particules fines.
---

(gaia-sl)=
# Charge suspendue

{term}`Suspended load` refers to fine particle ($\lesssim$ 1-2 mm) displacement in the water column, where particles are maintained in temporary suspension by the action of upward-moving turbulent eddies. The TELEMAC software suite uses the hydrodynamic Telemac2d/3d models to simulate {term}`Suspended load` by solving the {term}`Advection`-{term}`Diffusion` equations with tracer concentrations. This is why suspended load modeling requires an open boundary `LICBOR` type for tracers (e.g., `4` or `5`) as described in the {ref}`setup of the boundaries-gaia.cli <gaia-bc>` file.

Pour activer la simulation de la charge suspendue, ajouter ce qui suit au fichier de direction de Gaia :

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ SUSPENDED LOAD
SUSPENSION FOR ALL SANDS : YES
```

(gaia-sl-theory)=
## Contexte théorique

L'équation qui régit le transport des sédiments en suspension est l'équation advection-diffusion (ADE), qui décrit la conservation en masse des sédiments en suspension dans la colonne d'eau :

$$
\frac{\partial (hC)}{\partial t} + \frac{\partial (hUC)}{\partial x} + \frac{\partial (hVC)}{\partial y} = \frac{\partial}{\partial x}\left(\varepsilon_s h \frac{\partial C}{\partial x}\right) + \frac{\partial}{\partial y}\left(\varepsilon_s h \frac{\partial C}{\partial y}\right) + E - D
$$ (eq-ade-2d)

où $C$ est la concentration de sédiments en suspension moyenne de profondeur (Gaia l'exprime en g/l, numériquement égale à kg m$^{-3}$), $h$ est la profondeur d'eau (m), $U$ et $V$ sont les composantes de vitesse moyenne de profondeur (m s$^{-1}$), $\varepsilon_s$ est le coefficient de diffusion des sédiments (m$^2$ s$^{-1}$), $E$ est le flux d'érosion du lit (kg m$^{-2}$ s$^{-1}$), et $D$ est le flux de dépôt vers le lit (kg m$^{-2}$ s$^{-1}$).

```{admonition} 2D vs. 3D suspended load modeling
:class: note
Dans 2d (combinaison Telemac2d-Gaia), l'équation advection-diffusion est intégrée à la profondeur et résolue pour les concentrations moyennes de profondeur. Les concentrations à proximité du lit sont dérivées de formules d'équilibre. Dans 3d (combinaison Telemac3d-Gaia), l'équation complète 3d advection-diffusion est résolue, permettant des profils de concentration verticale (par exemple, le profil {cite:t}`rouse_analysis_1939`). L'approche 3d est recommandée lorsque la stratification verticale des sédiments est importante, par exemple dans les estuaires profonds ou les réservoirs. En savoir plus sur la charge suspendue 3d dans la section 2.2 du [Manuel Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

La diffusion des sédiments $\varepsilon_s$ est liée à la viscosité turbulente de l'eddy $\nu_t$ par:

$$
\varepsilon_s = \frac{\nu_t}{\sigma_s}
$$ (eq-diff-sed)

où $\sigma_s$ est le numéro Schmidt, que Gaia corrige à $\sigma_s = 1.0$ (c.-à-d., la diffusion des sédiments est égale à la viscosité turbulente de l'eddy). Une diffusion constante supplémentaire peut être définie avec le mot clé **COEFFICIENT POUR LA DIFFUSION DES SEDIMENTS SUPPLÉMENTAIRES** (réel, par défaut `1.E-6` m$^2$ s$^{-1}$).

(gaia-sl-sed)=
## Paramètres supplémentaires des sédiments

Les mélanges de sédiments fins impliquant des particules très fines et cohésives (moins de 0,06-0,1 mm) sont appelés **mud** dans Gaia et les mots clés dans les paragraphes suivants. La distinction entre le sable non cohésif et la boue cohésive est importante parce que leurs comportements d'érosion et de dépôt diffèrent fondamentalement. Pour plus d'informations sur les mots-clés liés à la boue, voir la section 4.2 du [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

### Paramètres de dépôt

Pour la charge en suspension, la définition des propriétés additionnelles des sédiments pour chaque classe de sédiments est requise (ou activée).

Les vitesses de décantation des particules $w_{s}$ peuvent être définies avec le mot-clé **CLASSES DÉFINITION DES VÉLOCITÉS** pour calculer le flux de dépôt $D$. La formule de dépôt classique {cite:t}`krone1962` est :

$$
D = w_{s} \cdot C \cdot \left(1 - \frac{\tau}{\tau_{cd}} \right) \quad \text{if } \tau < \tau_{cd}
$$ (eq-gaia-dep)

où $C$ est la concentration de sédiments en suspension (g/l), $\tau$ est la contrainte de cisaillement du lit (N m$^{-2}$), et $\tau_{cd}$ est la contrainte de cisaillement critique pour le dépôt (N m$^{-2}$). Si $\tau \geq \tau_{cd}$, aucun dépôt ne se produit parce que la turbulence est trop forte pour permettre aux particules de se déposer.

```{admonition} Critical shear stress vs. critical shear velocity
:class: note
Le mot-clé **CLASSES CRITIQUES STRESS POUR DÉPÔT MUD** est fourni sous la forme d'un stress à N m$^{-2}$** (par défaut `1000.`). En interne, Gaia le convertit en une vitesse de cisaillement critique ** $u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$ pour la formule de dépôt. La grande valeur par défaut de `1000` N m$^{-2}$ désactive efficacement la limite de résistance au cisaillement (c.-à-d. que le dépôt se produit toujours si $w_s > 0$), ce qui est approprié pour les sédiments non cohésifs.
```

Si le mot-clé **CLASSES DÉFINITIONS** est omis (ou défini à `-9`), Gaia calcule $w_s$ pour chaque classe de sédiments en interne, en sélectionnant l'une des trois formules dépendantes de la taille du grain :

* Pour les particules très fines ($D_{50} < 10^{-4}$ m), {cite:t}`stokes1850` loi s'applique:

$$
w_{s} = \frac{(s-1) \cdot g \cdot D_{50}^2}{18 \nu}
$$ (eq-ws-stokes)

* Pour les tailles intermédiaires ($10^{-4} \leq D_{50} < 10^{-3}$ m), la formule Rubey--{cite:t}`zanke1977` est utilisée :

$$
w_{s} = \frac{10\nu}{D_{50}}\left(\sqrt{1 + \frac{(s-1) \cdot g \cdot D_{50}^3}{100\nu^2}} - 1\right)
$$ (eq-ws-zanke)

* Pour les particules grossières ($D_{50} \geq 10^{-3}$ m), on utilise une relation constante traînée-coefficient :

$$
w_{s} = 1.1\sqrt{(s-1) \cdot g \cdot D_{50}}
$$ (eq-ws-coarse)

où $s$ est la densité relative des sédiments (typiquement 2.65), $g$ est l'accélération gravitationnelle, $D_{50}$ est le diamètre du grain, et $\nu$ est la viscosité cinématique de l'eau ($\approx$10$^{-6}$ m$^{2}$ s$^{-1}$). Les trois régimes passent d'un comportement visqueux ($Re_p \ll 1$, Stokes) à un comportement complètement turbulent ($Re_p \gg 1$, drag constant) de règlement {cite:p}`dey_fluvial_2014`.


Pour profiter des routines intégrées de Gaia pour calculer $w_{s}$, soit ne pas utiliser le mot-clé CLASSES DE DÉFINITION DES VÉLOCITÉS dans le fichier de pilotage de Gaia, soit régler ses valeurs par classe à `-9` (qui déclenche le calcul automatique). Des renseignements détaillés sur le calcul des vitesses de décantation pour des cas particuliers (p. ex., calcul de la charge en suspension pour d'autres matières en suspension que les sédiments minéraux) peuvent être trouvés, par exemple, à {cite:t}`dey_fluvial_2014` (section 1.7 du livre). L'algorithme de vitesse de règlement de Gaia est situé dans le fichier `settling_vel.f` dans le répertoire `/telemac/sources/gaia/`.

La contrainte de cisaillement critique $\tau_{cd}$ pour le dépôt de boue peut être définie avec le mot-clé **CLASSES CRITIQUES POUR DÉPÔT MUD** (par défaut `1000.` N m$^{-2}$, qui désactive efficacement le seuil de dépôt; Gaia le convertit en interne à la vitesse de cisaillement critique $u_{*,cd} = \sqrt{\tau_{cd}/\rho_w}$).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
CLASSES SETTLING VELOCITIES : -9;-9;-9
CLASSES CRITICAL SHEAR STRESS FOR MUD DEPOSITION : 1000;1000;1000 / N per m2
```

```{admonition} Hindered settling for high concentrations
:class: tip
À de fortes concentrations de sédiments en suspension (généralement > 10 g/l), les interactions particule-particules réduisent la vitesse de décantation efficace. Ce phénomène, connu sous le nom de *hindered settlement*, peut être activé en Gaia avec le mot-clé **HINDERED SETTLING** défini à `YES` (par défaut est `NO`). La formulation en difficulté suit {cite:t}`richardson1954sedimentation`:

$$
w_{s,h} = w_s \cdot (1 - \phi)^n
$$

où $\phi$ est la concentration de sédiments volumétriques et $n$ est un exposant empirique (généralement 4,65 pour les sédiments fins). Ceci est particulièrement important pour simuler les débits hyperconcentrés ou la sédimentation du réservoir.
```

### Paramètres d'érosion

Pour **cohesive (mud)** sédiments, Gaia calcule les flux d'érosion $E$ en utilisant la formule {cite:t}`partheniades1965`, qui est l'approche classique pour les sédiments cohésifs:

$$
E = \begin{cases} M\cdot \left(\frac{\tau}{\tau_{ce}} - 1\right) & \mbox{ if } \tau > \tau_{ce} \\ 0 & \mbox{ if } \tau \leq \tau_{ce}\end{cases}
$$ (eq-gaia-erosion)

where $M$ denotes the {cite:t}`krone1962`--{cite:t}`partheniades1965` erosion constant (in kg m$^{-2}$ s$^{-1}$), which can be defined in Gaia with the **LAYERS PARTHENIADES CONSTANT** keyword (default value: `1.E-03`). Moreover, $\tau_{ce}$ (critical shear stress for erosion) can be defined with the **LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD** keyword (default is `0.01;0.02;0.03;...` for successive layers) in N m$^{-2}$.

```{admonition} Non-cohesive sand uses an equilibrium-concentration closure
:class: note
The Partheniades formula above applies to **cohesive mud**. For **non-cohesive sand** (the case used in this tutorial), Gaia does not use the Partheniades constant. Instead, the net bed exchange flux is computed from the equilibrium near-bed concentration $C_{eq}$ obtained from the chosen {ref}`suspension formula <gaia-sl-formulae>` following the {cite:t}`celik1988` approach: $E - D = w_s \, (C_{eq} - C_{z_{ref}})$, where $C_{z_{ref}}$ is the actual near-bed concentration derived from the depth-averaged concentration assuming a {cite:t}`rouse_analysis_1939` profile. Erosion ($E = w_s C_{eq}$) dominates when the bed is under-saturated, and deposition ($D = w_s C_{z_{ref}}$) dominates when it is over-saturated.
```

```{admonition} Erosion vs. deposition thresholds
:class: note
L'énergie de départ (initialisation) pour l'érosion est plus élevée que pour le dépôt parce que les particules doivent surmonter les forces interparticules et être levées du lit. Par conséquent, la contrainte critique de cisaillement pour l'érosion ($\tau_{ce}$) est généralement plus grande que la contrainte critique de cisaillement pour le dépôt ($\tau_{cd}$). Pour les sédiments non cohésifs, le seuil d'érosion est souvent exprimé en termes de formulation {term}`Shields parameter` plutôt que de Partheniades.
```

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
LAYERS PARTHENIADES CONSTANT : 1.E-03 / in kg per m2 per s
/ LAYERS CRITICAL EROSION SHEAR STRESS OF THE MUD : 0.01;0.1;0.1 / in N per m2
```

```{admonition} Sand-mud mixtures
:class: tip
Pour les sédiments mixtes contenant des fractions de sable et de boue, Gaia applique différentes formulations d'érosion selon la teneur en boue de la couche active:

* ** Teneur en eau < 30 %**: Le comportement non cohésif domine; l'érosion suit l'approche de concentration d'équilibre pour les sables.
* **Contenance moyenne 30-50%**: Régime transitoire; interpolation linéaire entre les formulations non cohésives et cohésives.
* **Mud contenu > 50 %**: Le comportement cohésif domine; l'érosion suit la formulation {cite:t}`partheniades1965`.

Ce comportement est automatique dans Gaia quand plusieurs classes de sédiments avec différentes tailles de grains sont définies. En savoir plus sur les mélanges sable-mud dans la section 4 du [Manuel Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
```

(gaia-sl-formulae)=
## Formules de charge suspendues

Les formules de transport des sédiments pour la modélisation des charges en suspension peuvent être définies avec le mot-clé **SUSPENSION TRANSPORT FOR ALL SANDS**, qui accepte un nombre entier définissant une formule pour le calcul de la concentration d'équilibre près du lit $C_{eq}$ en **g/l** (l'unité Gaia utilise en interne pour toutes les concentrations de sédiments en suspension). La concentration d'équilibre représente la concentration de sédiments à un niveau de référence près du lit dans des conditions d'équilibre (c.-à-d. lorsque l'érosion équivaut au dépôt). Les valeurs calculées $C_{eq}$ s'alignent sur les valeurs ultérieures {ref}`definition of initial and boundary conditions <gaia-ic-sl>` pour la charge suspendue.

Les nombres entiers suivants peuvent être utilisés pour le calcul de $C_{eq}$ avec le mot-clé SURPENSION TRANSPORT FOR ALL SANDS:

* `1` pour la formule {cite:t}`zyserman1994` (**par défaut** et **utilisée dans ce tutoriel**):
  - Formule empirique basée sur des données expérimentales de {cite:t}`guy1966summary`
  - Utilise une correction de frottement de peau (cf. {ref}`bedload corrections <c-friction>`) pour le {term}`Shields parameter`
  - Applicable aux sédiments non cohésifs dans les milieux fluviaux
  - Référence (près du lit) élévation $z_{ref} = \alpha_{k_s} \cdot D_{50}$ (par défaut $3.0 \cdot D_{50}$, modifiable avec **RATIO ENTRE LA FRICTION DE LA PEAU ET LE DIAMÈTRE MEAN**)
  - Définie dans `/telemac/sources/gaia/suspension_fredsoe.f`
  - Formule : $C_{eq} = \frac{0.331 \cdot (\theta' - \theta_{cr})^{1.75}}{1 + 0.72 \cdot (\theta' - \theta_{cr})^{1.75}}$ où $\theta' = \mu\theta$ est le paramètre skin-friction Shields et $\theta_{cr}$ est le paramètre critique Shields

* `2` for the {cite:t}`bijker1992` formula:
  - Calcule la concentration de charge en suspension en fonction de la charge en lit et d'une élévation de référence de la friction cutanée
  - Exige que {ref}`bedload calculation <gaia-bl>` soit activé (`BED LOAD FOR ALL SANDS : YES`)
  - Convient pour les calculs combinés de charge en suspension
  - Élévation de référence $z_{ref} = k_{sr}$ (la rugosité du lit déchiré)
  - Définie dans `/telemac/sources/gaia/suspension_bijker.f`

* `3` for the {cite:t}`van_rijn_suspension_1984` formula:
  - Contrepartie du {ref}`van Rijn bedload formula <gaia-rijn>`
  - Utilise une correction de frottement de peau (cf. {ref}`bedload corrections <c-friction>`) pour le {term}`Shields parameter`
  - Altitude de référence $z_{ref} = 0.5 \cdot k_s$ où $k_s$ est la rugosité totale (à partir du dossier de direction hydrodynamique)
  - A l'origine développé pour le transport de sable dans les rivières et les estuaires
  - Définie dans `/telemac/sources/gaia/suspension_vanrijn.f`

* `4` for the {cite:t}`soulsby1997`-{cite:t}`rijn2007` formula:
  - Utilisation de la vitesse orbitale des vagues (c.-à-d. application suggérée : régions côtières/marines)
  - Combine les effets du courant et des vagues sur la suspension des sédiments
  - En savoir plus sur la charge en suspension et les vagues dans la section 5.1 du [Manuel Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf)
  - Définie dans `/telemac/sources/gaia/suspension_sandflow.f`

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SUSPENSION TRANSPORT FORMULA FOR ALL SANDS : 1
```

```{admonition} User-defined suspension formulae
:class: tip
Les utilisateurs peuvent implémenter des formules de transport de suspension personnalisées en modifiant les fichiers source Fortran. La procédure suit la même approche que pour {ref}`user-defined bedload formulae <gaia-bl>`: copiez le fichier source pertinent vers un répertoire `user_fortran/` et référez-le dans le fichier de direction avec `FORTRAN FILE : 'user_fortran'`. Le [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf) fournit des conseils détaillés à la section 6.3.
```

(gaia-ic-sl)=
## Conditions initiales et limites

Gaia permet une définition par classe des concentrations initiales pour la charge en suspension suivant l'ordre de {ref}`sediment class definitions <gaia-sed>`. La définition de la liste suivante définit la concentration initiale pour la classe de sédiments de 0,5 mm ({ref}`recall its definition <gaia-sed>`) à 0,6 **g/l** et 0,0 g/l pour les classes de tailles de sédiments de 0,02 m et 0,1 m. La définition des concentrations initiales de sédiments en suspension peut être dépassée en 2d aux nœuds limites en fixant le mot-clé **CIRCENTRATION DE L'INFLOW DE L'ÉQUILIBRE** à `YES` (qui exige que le {ref}`tracer boundary <gaia-bc>` soit réglé à `5`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
INITIAL SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0.
```

```{admonition} Concentration units in Gaia
:class: warning
Gaia s'attend à **toutes** concentrations de sédiments en suspension dans **g/l** (grammes de sédiments secs par litre), y compris les VALEURS DE CONCENTRATION DES SÉDIMENTS SUPPLÉMENTAIRES INITIAUX**, **LES VALEURS DE CONCENTRATION DES SÉDIMENTS SUPPLÉMENTAIRES PRESCRIBÉES**, et la colonne `CBOR` du fichier limite. La concentration massique en g/l est numériquement identique à kg/m3:
* 1 g/l = 1 kg/m3
* 1 mg/l = 0,001 g/l = 0,001 kg/m3

Ainsi, l'exemple ci-dessus définit `0.6` g/l = 0,6 kg/m3 = 600 mg/l pour la première classe de sédiments. Si vous avez besoin d'une concentration en volume $C_v$, convertissez en post-traitement avec $C_v = C_m / \rho_s$, où $C_m$ est la concentration en masse (g/l) et $\rho_s$ est la densité de sédiments (kg/m3).
```

Pour en savoir plus sur la définition des conditions initiales à la section 2.1.1 du [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

(gaia-bc-sl)=
## Prescriptions concernant la frontière

The per-sediment class suspended load concentrations can be prescribed similar to the initial concentrations with the **PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES** keyword. Alternatively, the **EQUILIBRIUM INFLOW CONCENTRATION** keyword may be used to automatically compute the inflow concentration based on the equilibrium formula (option `1`-`4` defined above). **None of these keywords is used in this tutorial** because the model starts with a defined initial concentration and allows the system to evolve.

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
/ PRESCRIBED SUSPENDED SEDIMENTS CONCENTRATION VALUES : 0.6;0.;0. / g/l
/ EQUILIBRIUM INFLOW CONCENTRATION : YES / not used in this tutorial
```

```{admonition} Treatment of boundary fluxes
:class: tip
Le mot-clé **TREATMENT DES FLUX AUX ORGANES** contrôle la façon dont les concentrations prescrites sont traitées aux limites ouvertes:

* `1` (**par défaut**): Priorité à la valeur prescrite dans l'étape de diffusion. Cela peut créer des flux artificiels aux frontières.
* `2`: Priorité au flux prescrit. Le flux réel de sédiments est égal au débit d'eau multiplié par la concentration prescrite. Cette option est recommandée pour les simulations de masse-conservateur avec des schémas d'advection distributive (`3`, `4`, `5`, `13`, `14`).

Pour les applications de bilan de masse critique, utilisez l'option `2` avec le schéma d'advection `14` ou `15`.
```

Gaia can be run with liquid boundary files for assigning time-dependent suspended load fluxes (the outflow should be kept in equilibrium). Solid flux time series can be implemented using the already applied `455`-`5` upstream boundary type, analogous to the descriptions of the {ref}`Telemac2d unsteady boundary setup <tm2d-liq-file>`. More information about suspended load boundary conditions can be found in section 2.1.2 in the [Gaia manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).


## Paramètres numériques

La plupart des paramètres numériques pour la modélisation de charge suspendue dépendent des définitions de fichiers de direction Telemac2d/3d. D'autres mots clés ayant une incidence directe sur la simulation de la charge en suspension doivent être déclarés dans le dossier de direction de Gaia.

Par exemple, les mots-clés **CHEME POUR ADVECTION ...** pour la modélisation des vitesses, des traceurs et des turbulences sont définis avec le fichier de direction d'hydrodynamique (Telemac2d/3d) {ref}`general numerical parameters for finite elements <tm2d-fe>`. De plus, le schéma d'advection pour la charge suspendue peut être défini dans le fichier de direction de Gaia avec le mot-clé **CHEME POUR ADVECTION DES SEDIMENTS SUSPENDUS** qui accepte l'un des mots-clés entiers suivants (pour 2d seulement):

* `1` pour le schéma de caractéristiques* inconditionnellement stable, non-conservateur, mais diffusif (pour de petits pas dans le temps).
* `2` pour le régime non-conservateur *Streamline Upwind Petrov Galerkin* (SUPG) qui utilise le régime {term}`CFL` et est moins diffus que le régime *Caractéristiques* (`1`).
* `3` ou `4` pour le conservateur *N-scheme* (distributif) avec réduction du temps basée sur la condition {term}`CFL`. L'option `4` inclut la musculation pour améliorer la stabilité. Ces options ne doivent pas être utilisées en présence d'appartements à marée (utiliser `13` ou `14`).
* `5` pour le système de distribution de masse *PSI* (**default**), qui corrige les flux en fonction des concentrations de traceur et est moins diffus que `4` ou `14`. Le temps de calcul avec `5` est plus long qu'avec `4` ou `14`. Cette option doit **ne pas être utilisée en présence de plates-formes de marée.
* `13` et `14` pour le N-scheme* (NERD) basé sur Edge, qui est similaire à `3` et `4`, mais adapté aux appartements de marée. **Option `14` est utilisée dans ce tutoriel** selon la recommandation dans le [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).
* `15` pour le système de masse-conservateur *ERIA* qui fonctionne avec les plates-formes de marée.

Les options `4` et `14` peuvent être définies avec la définition de mot clé `CORRECTION ON CONVECTION VELOCITY : YES` (logique, par défaut `NO`) qui modifie la vitesse de convection moyenne de profondeur pour tenir compte des gradients verticaux de vitesse et de concentration. Ce réglage évite la surestimation de la charge en suspension, en particulier dans les eaux profondes, mais il n'est pas utilisé dans ce tutoriel.

L'option **CHEME POUR L'AVOCAT DES SEDIMENTS SUPPLÉMENTAIRES** peut également être définie en utilisant un formulaire **strong (par défaut de `1`)** ou **faible (`2`)** pour l'avis. Une forme faible diminue numériquement {term}`Diffusion`, est plus conservatrice, et augmente le temps de calcul (lisez plus dans le {ref}`Telemac2d steady section <tm2d-fe>`).

```fortran
/ continued: gaia-morphodynamics.cas
/ ...
SCHEME FOR ADVECTION OF SUSPENDED SEDIMENTS : 14
/ CORRECTION ON CONVECTION VELOCITY : YES / use when SCHEME is 4 or 14 for deep water
```

```{admonition} Diffusion of suspended sediment
:class: tip
Le terme de diffusion de l'équation advection-diffusion est régi par la viscosité turbulente du résolveur hydrodynamique ainsi qu'une diffusion de fond constante qui peut être réglée dans le fichier de direction de Gaia:

* **COEFFICIENT FOR DIFFUSION OF SUSPENDED SEDIMENTS** (real, default `1.E-6` m$^2$ s$^{-1}$): constant diffusivity added in 2d (in 3d use **COEFFICIENT FOR HORIZONTAL DIFFUSION OF SUSPENDED SEDIMENTS** and **COEFFICIENT FOR VERTICAL DIFFUSION OF SUSPENDED SEDIMENTS**).

Pour la plupart des applications fluviales, la valeur par défaut est adéquate parce que la diffusion turbulente domine sur le terme de fond constant.
```

Pour en savoir plus sur la définition des paramètres numériques à la section 2.1.5 du [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf).

## Couplage morphologique

Lorsque la charge en suspension est activée en même temps que l'évolution du lit, les flux d'érosion et de dépôt contribuent au bilan massique du lit à travers le {term}`Exner equation`. Le flux net (érosion moins dépôt) modifie l'élévation du lit à chaque étape.

```{admonition} Morphological factor for suspended load
:class: tip
Pour les simulations à long terme où les échelles de temps morphologiques sont beaucoup plus longues que les échelles de temps hydrodynamiques, un FACTEUR MORPHOLOGIQUE** peut être appliqué pour accélérer l'évolution du lit. Ce facteur multiplie le flux net d'érosion/deposition, permettant des simulations morphologiques pluriannuelles avec des temps de calcul raisonnables. Cependant, utiliser avec prudence : des facteurs morphologiques supérieurs à 10-20 peuvent entraîner des résultats irréalistes. Le mot clé est défini dans le fichier de direction de Gaia:

```fortran
MORPHOLOGICAL FACTOR : 10. / accelerate bed evolution 10x
```
```

## Exemples de demandes

Examples for the implementation of suspended load come along with the TELEMAC installation (in the `/telemac/examples/gaia/` directory). The following examples in the `gaia/` folder feature (pure) suspended load calculations:

* Modèle 2d de transport combiné en suspension cohésif et non cohésif: **hippodrome-t2d/**
* Modèle 2d de conservation de la masse de boue cohésive: **mud conservation-t2d/**
* Modèle 3d de transport combiné en suspension cohésif et non cohésif: **hippodrome-t3d/**
* Modèle 3d de transport suspendu non cohésif avec correction du frottement cutané: **lyn-t3d/**
* Modèle 3d de transport suspendu cohésif avec profil vertical de Rouse (cf. [Manuel de Gaia](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/raw/v9.0.0/documentation/gaia/user/gaia_user_9.0.pdf), section 2.1.2) : **rousse-t3d/**
* Modèle 3d d'une flume marémotrice avec sédiment cohésif : **tidal flats-t3d/**
* Couplage avec ondes: **sandpit-t2d/**

```{admonition} Recommended workflow for suspended load simulations
:class: note
1. **Démarrer avec l'hydrodynamique**: S'assurer que le modèle hydrodynamique (Telemac2d/3d) est étalonné et produit des champs d'écoulement raisonnables avant de se coupler avec Gaia.
2. **Définir les classes de sédiments**: Préciser les dimensions de grain appropriées pour le site. Les sédiments fins ($D < 0.063$ mm) sont généralement cohésifs; les sédiments plus grossiers ne sont pas cohésifs.
3. **Choisissez la formule de suspension** : Choisissez en fonction de l'environnement (fluvial : `1` ou `3`; littoral avec vagues : `4`).
4. **Préciser les conditions initiales**: Utiliser les concentrations mesurées ou estimées de sédiments en suspension.
5. **Choisissez le schéma d'advection**: Utilisez `14` pour la robustesse avec les plates-formes de marée, ou `5` pour une meilleure précision dans les canaux profonds.
6. **Érosion/déposition du calibrage**: Ajuster la constante de Parthéniades $M$, les contraintes critiques de cisaillement, et les vitesses de réglage pour correspondre aux concentrations observées.
7. ** Balance massique des valeurs**: Activer `MASS-BALANCE : YES` dans le fichier de pilotage hydrodynamique pour surveiller la conservation des sédiments.
```