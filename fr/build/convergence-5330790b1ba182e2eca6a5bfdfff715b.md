---
description: Analyse quantitative de convergence pour les simulations TELEMAC utilisant la sortie du bilan massique et le Python, couvrant le diagnostic du flux et la vérification cumulative du débit pour des modèles de rivière fiables.
---

(tm-convergence)=
# Convergence (Quantitative)

````{admonition} Requirements
:class: important, dropdown

* Compléter le {ref}`Telemac steady 2d tutorial <telemac2d-steady>` (ou une simulation stable équivalente).
* Le fichier de direction (`.cas`) doit contenir les mots-clés `MASS-BALANCE : YES` et/ou `PRINTING CUMULATED FLOWRATES : YES`, ce qui fait que TELEMAC signale les flux de masse au-delà des limites du liquide dans la liste.
* La simulation TELEMAC doit avoir été exécutée avec le drapeau `-s` (détails ci-dessous):

```fortran
telemac2d.py [STUDY-NAME].cas -s
```

* Une installation Python (&geq; 3.9) avec le `numpy`, `pandas`, et `matplotlib` bibliothèques ({ref}`see the Python installation guide <install-python>`); `flusstools` n'est pas nécessaire.

**Tous les fichiers de simulation utilisés dans ce tutoriel peuvent être téléchargés à partir du dépôt [hydro-informatique/télémac sur GitHub](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial) (voir détails ci-dessous).**
````

```{admonition} Goals & purpose
:class: note

Le présent chapitre présente une procédure quantitative pour vérifier la convergence des flux d'une simulation TELEMAC **steady** et pour déterminer la durée minimale de simulation (`NUMBER OF TIME STEPS`) nécessaire pour atteindre un état équilibré en masse. Une telle vérification est recommandée avant qu'un résultat stable ne soit utilisé pour lancer une simulation {ref}`unsteady <chpt-unsteady>` ou {ref}`morphodynamic (sediment transport) <gaia-basics>`, car l'étalonnage ou la poursuite d'un état non convergent propage un biais transitoire dans tous les calculs ultérieurs. La même procédure peut également être appliquée pour comparer les temps de déplacement des vagues d'inondation entre une limite en amont et une limite en aval.

Pour les remèdes à un modèle non convergent, consultez le {ref}`spotlight chapter on mass conservation <tm-foc-mass>` et vérifiez que le {ref}`liquid boundaries are well defined <tm-foc-bc>`.
```

Ce chapitre utilise les fichiers de simulation de {ref}`Telemac steady 2d tutorial <telemac2d-steady>`, avec une définition modifiée de l'étape temporelle et des périodes d'impression:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 10000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

En outre, la simulation a été ré-exécutée avec le drapeau `-s`, qui écrit la liste complète dans un fichier nommé `[FILE-NAME].cas_YEAR-MM-DD-HHhMMminSSs.sortie` dans le répertoire de simulation:

```fortran
telemac2d.py steady2d-conv.cas -s
```

La direction `.cas` et les fichiers `.sortie` peuvent être téléchargés à partir des dépôts hydro-informatiques.com:

* [téléchargez stable2d-conv.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas)
* [télécharger stable2d-conv.cas 2023-07-26-18h41min26s.sortie](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas_2023-07-26-18h41min26s.sortie)

(tm-flux-convergence)=
## Extraire et vérifier les données Flux

```{admonition} Alternative: use control sections

Cette section dérive la convergence de flux (flux) directement de la liste TELEMAC avec Python. Alternativement, les flux limites peuvent être extraits par {ref}`defining control sections (read more in the unsteady tutorial) <tm-control-sections>`.
```

Les modèles de carnets TELEMAC Jupyter (*HOMETEL/notebooks/* > *data manip/extraction/*.ipynb* ou *workshops/exo fluxes.ipynb*) fournissent des indications pour extraire les données des résultats de simulation; toutefois, les modèles ne constituent pas un cadre directement applicable pour évaluer la convergence de masse aux limites en fonction de `NUMBER OF TIME STEPS`. À cette fin, hydro-informatique.com maintient le paquet Python léger [pythomac](https://pythomac.readthedocs.io) (version &geq; 3.0.0 est décrit ici). Le paquet ne nécessite que `numpy`, `pandas` et `matplotlib` ({ref}`see the Python installation guide <install-python>`) et court en dehors de l'environnement Python TELEMAC. Deux options d'installation sont disponibles:

`````{tab-set}
````{tab-item} pip-install pythomac (recommended)

Installez le paquet *pythomac* à partir de l'index Python Package:

```
pip install pythomac
```
````

````{tab-item} editable install from source

Pour le développement, clonez le dépôt *pythomac* de [GitHub](https://github.com/hydro-informatics/pythomac) et installez-le en mode modifiable:

```
git clone https://github.com/hydro-informatics/pythomac.git
pip install -e pythomac
```

Notez que depuis la version 3.0.0, *pythomac* est un paquet Python régulier avec des importations dans le paquet; copier le dossier `pythomac/pythomac/` à côté d'une simulation (le workflow pré-3.0) n'est plus pris en charge.
````
`````

La fonction centrale est `pythomac.extract_fluxes()`. Il localise la liste la plus récente `.sortie` à côté du fichier de pilotage, analyse le solde de volume et le flux signé imprimé pour chaque limite de liquide à chaque liste imprimée (les formats classiques `THERE IS n LIQUID BOUNDARIES` et TELEMAC v9 `NUMBER OF LIQUID BOUNDARIES:` listing sont reconnus), et écrit dans le répertoire de simulation:

* `extracted-fluxes.csv` - la série chronologique du volume dans le domaine et du flux à travers chaque limite liquide;
* `flux-convergence.png` - un tracé des magnitudes du flux au cours du temps de simulation (facultatif, `plotting=True`).

The function returns the extracted series as a `pandas.DataFrame` indexed by simulation time; the working directory of the calling process is not modified. The implementation can be inspected in [flux_analyst.py on GitHub](https://github.com/hydro-informatics/pythomac/blob/main/pythomac/flux_analyst.py), and the complete API documentation is available at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io).

Pour appliquer la fonction, copiez le code suivant dans un nouveau script Python appelé, par exemple, `example_flux_convergence.py`, situé dans le répertoire où la simulation stable2d a été effectuée (ou [téléchargez exemple flux convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py)):

```python
# example_flux_convergence.py

from pathlib import Path
from pythomac import extract_fluxes

simulation_dir = str(Path(__file__).parents[1])
telemac_cas = "steady2d.cas"

fluxes_df = extract_fluxes(
    model_directory=simulation_dir,
    cas_name=telemac_cas,
    plotting=True
)
```

```{admonition} Errors? Verify the simulation directory.
:class: error

Une déclaration `print(simulation_dir)` dans le bloc de code ci-dessus indique si le chemin attribué résout dans le répertoire qui contient les fichiers de direction et `.sortie`. Ajustez `simulation_dir` si le script réside à un niveau différent par rapport à la simulation.
```

Exécutez le script Python depuis un terminal (ou Anaconda Prompt) dans le répertoire de simulation :

```
python example_flux_convergence.py
```

Le script place dans le dossier de simulation :

* le fichier CSV [extracted-fluxes.csv (télécharger)](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/extracted_fluxes.csv); et
* la courbe de convergence des flux (*flux-convergence.png*) à travers les limites du modèle (voir {numref}`Fig. %s <steady-flux-convergence>`), ce qui indique qualitativement que les flux ont approché la convergence après environ 6000-7000 étapes.

```{figure} ../../img/telemac/flux-convergence.png
:alt: python telemac flux discharge convergence pythomac
:name: steady-flux-convergence

Les magnitudes de flux à travers les deux limites de liquide de la simulation stable à sec Telemac2d au cours du temps simulé, produite avec la fonction pythomac.extract fluxes().
```

(tm-calculate-convergence)=
## Identifier la convergence

Pour déterminer si et quand les flux limites convergent, le déséquilibre relatif des flux est évalué à chaque heure d'impression $t$ comme suit:

```{math}
:label: error_rate
\varepsilon_{t} = \frac{\left| |Q_{i,t}| - |Q_{j,t}| \right|}{|Q_{j,t}|}
```

où $Q_{i,t}$ et $Q_{j,t}$ = les flux sortants et entrants franchissent les limites du modèle à l'heure $t$, respectivement. Les magnitudes de flux $|\cdot|$ sont nécessaires parce que TELEMAC signale les flux limites avec une convention de signe (flux positif, flux négatif); le bilan massique correspond donc à $|Q_{i,t}| = |Q_{j,t}|$, de sorte que $\varepsilon_{t} \to 0$ à la convergence, et la normalisation par l'afflux $|Q_{j,t}|$ rendes $\varepsilon_{t}$ sans dimension. Dans une simulation stable et régulière, le rapport des déséquilibres de flux consécutifs approche une constante de convergence $c_{\varepsilon}$ égale à l'unité avec un temps croissant:

```{math}
:label: error_lim
\lim_{t\to \infty} \frac{\varepsilon_{t+1}}{\varepsilon^{\iota}_{t}} = c_{\varepsilon}
```

La combinaison du taux de convergence (ou ordre) $\iota$ et de la constante de convergence $c_{\varepsilon}$ indique:

* convergence linéaire si $\iota$ = 1 ** et** $c_{\varepsilon} \in ]0, 1[$;
* convergence lente *sublinéaire* si $\iota$ = 1 ** et** $c_{\varepsilon}$ = 1;
* rapide *convergence superlinéaire* si $\iota$ > 1 **et** $c_{\varepsilon} \in ]0, 1]$; et
* divergence si $\iota$ = 1 ** et** $c_{\varepsilon}$ > 1, **ou** $\iota$ < 1.

````{aside} Calculate $\varepsilon_{t+1}$

$\varepsilon_{t+1}$ (`epsilon_t1`) est obtenu à partir de $\varepsilon_{t}$ (`epsilon_t0`) en déplaçant la série par un élément :

```python
epsilon_t0 = epsilon[:-1]  # cut off last element
epsilon_t1 = epsilon[1:]   # cut off element zero
```
````

Le moment où une simulation stable peut être considérée comme ayant atteint un état stable est identifié par le début de la convergence sublinéaire ($\iota$ = 1 et $c_{\varepsilon}$ = 1); c'est-à-dire le moment $t$ au-delà duquel chaque étape supplémentaire $t+1$ améliore la précision du modèle seulement de façon insignifiante (le terme *insignificative* est quantifié dans le {ref}`section below <tm-target-conv>`). Dans l'hypothèse où le modèle converge sous une forme ou une autre, régler $c_{\varepsilon}$ = 1 rendement $\iota(t)$ en fonction de $\varepsilon_{t}$ et $\varepsilon_{t+1}$:

\début{align}
\label{estimation convergence}
\frac{\varepsilon {t+1}}{\varepsilon^{\iota(t)}} {t}} &=c {\varepsilon} & \Leftrightarrow \\
\iota(t) &= \frac{1}{c {\varepsilon}} \cdot \log {\varepsilon {t}}\varepsilon {t+1} & \overbrace{\Longleftrightarrow}^{c {\varepsilon} = 1}\\
\iota(t) &= \log {\varepsilon {t}}\varepsilon {t+1} &
\end{align}

These relations are implemented in the `pythomac.calculate_convergence()` function, which returns a `pandas.DataFrame` with the columns `"Relative imbalance"` ($\varepsilon_{t+1}$, Equation {eq}`error_rate`) and `"Convergence rate"` ($\iota(t)$), indexed by simulation time. Its core reads:

```python
import numpy as np
import pandas as pd


def calculate_convergence(series_1, series_2, conv_constant=1.):
    # relative flux imbalance epsilon_t = ||Q_in| - |Q_out|| / |Q_in|; the magnitudes |.|
    #   are needed because Telemac reports outflow negative, so that balance -> epsilon -> 0
    epsilon = np.abs(np.abs(series_1) - np.abs(series_2)) / np.abs(series_1)
    # derive epsilon at t and t+1
    epsilon_t0 = epsilon[:-1]  # cut off last element
    epsilon_t1 = epsilon[1:]   # cut off element zero
    # return the relative imbalance and the convergence rate iota as a pandas DataFrame
    return pd.DataFrame({
        "Relative imbalance": epsilon_t1,
        "Convergence rate": np.emath.logn(epsilon_t0, epsilon_t1) / conv_constant,
    })
```

````{admonition} This function is available in pythomac
:class: tip

```python
from pythomac import calculate_convergence
```

L'implémentation emballée accepte en outre `cas_timestep` (l'espacement d'impression dans les secondes de simulation, utilisé pour l'échelle de l'index) et `plot_dir` (si fourni, un graphique `convergence-rate.png` est écrit à ce répertoire).
````

Pour calculer $\iota(t)$ (nom variable Python: `iota_t`) avec la fonction ci-dessus, modifier le *exemple flux convergence.py* script Python comme suit:

```python
# example_flux_convergence.py

# ...
# add to header:
from pythomac import calculate_convergence

# calculate fluxes_df (see above code block)
fluxes_df = [...]

# back-calculate the printout spacing (in simulation seconds) from the flux index
timestep_in_cas = int(max(fluxes_df.index.values) / (len(fluxes_df.index.values) - 1))

# calculate iota (t) with the calculate_convergence function
iota_t = calculate_convergence(
    series_1=fluxes_df["Fluxes Boundary 1"][1:],  # remove first zero-entry
    series_2=fluxes_df["Fluxes Boundary 2"][1:],  # remove first zero-entry
    cas_timestep=timestep_in_cas,
    plot_dir=simulation_dir,
)
```

Le taux de convergence résultant $\iota(t)$ est tracé à {numref}`Fig. %s <tm-convergence-rate>` pour le {ref}`steady 2d tutorial <telemac2d-steady>` avec les périodes d'impression modifiées de `50` secondes et un temps de simulation total de `10000` secondes.

```{figure} ../../img/telemac/convergence-rate.png
:alt: convergence rate fluxes telemac boundaries
:name: tm-convergence-rate

Le taux de convergence $\iota$ en fonction des 10000 étapes de la simulation 2d.
```

(tm-target-conv)=
## Temps de simulation optimal dérivé

Pour économiser le temps de calcul, l'étape dans laquelle les flux d'entrée et de sortie ont convergé présente un intérêt pratique. Les flux tracés dans {numref}`Fig. %s <steady-flux-convergence>` et le taux de convergence dans {numref}`Fig. %s <tm-convergence-rate>` suggèrent qualitativement que la simulation s'est stabilisée après environ 6000 secondes (étapes de temps). L'extrémité locale dans les deux chiffres près de 4000 étapes dans le temps marque l'interaction des fronts mouillants se propageant à partir des limites amont et aval (voir le {ref}`animation in the steady 2d tutorial <telemac-flow-convergence-gif>`); la convergence monotonique se fixe seulement par la suite.

Parce qu'un jugement purement visuel de convergence est subjectif, un critère objectif est adopté : la longueur optimale de simulation est le plus petit temps $t$ au-delà duquel le déséquilibre relatif du flux $\varepsilon_{t}$ (Equation {eq}`error_rate`) reste en permanence en dessous d'une tolérance cible $\varepsilon_{tar}$. Les tolérances de $\varepsilon_{tar}$ = 10$^{-4}$ sont généralement acceptables pour les essais d'étalonnage préliminaires, alors que la validation et les essais d'initialisation à chaud justifient des valeurs plus petites (10$^{-6}$ ou moins). Comme l'illustre {numref}`Fig. %s <tm-convergence-rate>`, le déséquilibre peut tomber temporairement sous la tolérance et remonter à nouveau (ici près de 4000 pas de temps, lorsque le front en amont franchit la limite en aval); seul le dernier passage permanent est pertinent. L'implémentation algorithmique détecte donc la dernière fois à laquelle $\varepsilon_{t} \geq \varepsilon_{tar}$ et désigne l'impression subséquente comme temps de convergence. Ce critère est implémenté à `pythomac.get_convergence_time()`, qui retourne l'index d'impression du passage à niveau permanent, ou `numpy.nan` (avec un avertissement) si la tolérance n'est jamais maintenue. Modifier le script *exemple flux convergence.py* comme suit:

```python
# example_flux_convergence.py

# ...
# add to header:
from pythomac import get_convergence_time

# calculate fluxes_df and iota_t (see above code blocks)
fluxes_df = [...]
iota_t = [...]

# identify the printout index from which the relative flux imbalance stays
# permanently below the target tolerance (epsilon_tar)
convergence_time_iteration = get_convergence_time(
    relative_imbalance=iota_t["Relative imbalance"],
    convergence_precision=1.0E-4
)

if not str(convergence_time_iteration).lower() == "nan":
    print("The simulation converged after {0} simulation seconds ({1}th printout).".format(
            str(timestep_in_cas * convergence_time_iteration), str(convergence_time_iteration)))
```

```  
The simulation converged after 6000 simulation seconds (120th printout).
```

````{admonition} Full example script
:class: tip

A complete implementation, including the retrieval of the `timestep_in_cas` variable and the export of the convergence table to `convergence-rate.csv`, is provided in [example_flux_convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py), with documentation at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io/en/latest/convergence.html).
````

Avec le temps de convergence établi, le mot clé `NUMBER OF TIME STEPS` dans le fichier de pilotage `.cas` peut être réduit en conséquence, par exemple:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 6000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

```{admonition} Variable time steps require a duration-based criterion
:class: note

Si le fichier de direction active `VARIABLE TIME-STEP : YES` (une étape adaptative contrôlée par Nombre de Courant), le nombre d'étapes de temps n'est pas connu a priori et `NUMBER OF TIME STEPS` ne lie pas le temps simulé; l'exécution est alors plafonnée par `DURATION`, et le temps de convergence identifié ci-dessus doit être interprété en secondes de simulation plutôt qu'en étapes de temps.
```

## Dépannage des instabilités et des divergences

Si une simulation régulière ne parvient pas à obtenir des flux stables, ou si les flux divergent, vérifiez que toutes les limites sont bien définies selon la section des projecteurs sur {ref}`boundary conditions <tm-foc-bc>`, et consultez le workflow dans la section sur {ref}`mass conservation <tm-foc-mass>`.
