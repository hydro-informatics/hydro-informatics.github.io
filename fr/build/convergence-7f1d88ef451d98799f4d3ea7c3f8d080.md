---
description: Analyse quantitative de convergence pour les simulations TELEMAC utilisant la sortie du bilan massique et le Python, couvrant le diagnostic du flux et la vérification cumulative du débit pour des modèles de rivière fiables.
---

(tm-convergence)=
# Convergence (Quantitative)

````{admonition} Requirements
:class: important, dropdown

* Remplissez le {ref}`Telemac steady 2d tutorial <telemac2d-steady>` (ou similaire).
* Les mots-clés `MASS-BALANCE : YES` et/ou `PRINTING CUMULATED FLOWRATES : YES` doivent avoir été utilisés dans le fichier de direction (`.cas`) pour imprimer des flux de masse au-delà des limites de liquide dans le terminal.
* La simulation de Telemac doit avoir été lancée avec le drapeau `s` (plus de détails ci-dessous):

```fortran
telemac2d.py [STUDY-NAME].cas -s
```

* Une installation de Python avec le `numpy`, `pandas`, et `matplotlib` bibliothèques ({ref}`see the Python installation guide <install-python>`), même si `flusstools` n'est pas nécessaire.

**Tous les fichiers de simulation requis pour ce tutoriel peuvent être téléchargés à partir du dépôt [hydro-informatique/télémac sur GitHub](https://github.com/hydro-informatics/telemac/tree/main/steady2d-tutorial) (voir détails ci-dessous).**
````

```{admonition} Goals & purpose
:class: note

Ce tutoriel décrit la vérification de la convergence des flux pour optimiser le nombre requis de temps de simulation (`NUMBER OF TIME STEPS`) d'un **steady** Simulation Telemac. Une telle analyse de convergence est recommandée avant d'utiliser des résultats de simulation stables pour lancer une simulation {ref}`unsteady <chpt-unsteady>` ou {ref}`morphodynamic (sediment transport) <gaia-basics>`. Cependant, les scripts ci-dessous peuvent aussi servir à comparer les temps de déplacement des vagues d'inondation qui vont d'une limite en amont à une limite en aval.

Si vous cherchez des solutions pour corriger un modèle non convergent, veuillez vous référer à {ref}`spotlight chapter on mass conservation <tm-foc-mass>` et assurez-vous que {ref}`liquid boundaries are well defined <tm-foc-bc>`.
```

Ce chapitre utilise les fichiers de simulation de {ref}`Telemac steady 2d tutorial <telemac2d-steady>`, mais avec une définition légèrement différente des délais et des périodes d'impression:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 10000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

En outre, la simulation a été recourue avec le drapeau `-s`, qui enregistre l'état de simulation dans un fichier appelé similaire à `[FILE-NAME].cas_YEAR-MM-DD-HHhMMminSSs.sortie`.

```fortran
telemac2d.py steady2d-conv.cas -s
```

Les fichiers de direction `.cas` et `.sortie` peuvent être téléchargés à partir des dépôts hydro-informatiques.com :

* [télécharger stable2d-conv.cas](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas)
* [téléchargez stable2d-conv.cas 2023-07-26-18h41min26s.sortie](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/steady2d-conv.cas_2023-07-26-18h41min26s.sortie)

(tm-flux-convergence)=
## Extraire et vérifier les données Flux

```{admonition} Alternative: use control sections

Cette section présente l'analyse de convergence de flux (flux) directement depuis l'enregistrement de messages Telemac avec Python. Sinon, les flux peuvent être extraits par {ref}`defining control sections (read more in the unsteady tutorial <tm-control-sections>`.
```

Les modèles de carnets de notes Telemac jupyter (*HOMETEL/notebooks/* > *data manip/extraction/*.ipynb* ou *workshops/exo fluxes.ipynb*) fournissent des indications pour extraire les données des résultats de simulation, qui peuvent être ajustées dans un cadre généralement applicable pour observer la convergence de masse aux limites en fonction de la définition `NUMBER OF TIME STEPS`. Cependant, les modèles de cahiers ne fonctionnent pas de façon simple, c'est pourquoi les paragraphes suivants décrivent un tweak Python simple et minimaliste appelé [pythomac](https://pythomac.readthedocs.io), développé par hydro-informatics.com. Il y a trois options pour travailler avec nos codes, et tous ont besoin d'avoir une installation de Python avec le `numpy`, `pandas`, et `matplotlib` bibliothèques ({ref}`see the Python installation guide <install-python>`):

`````{tab-set}
````{tab-item} pip-install pythomac

Pip-installer le paquet *pythomac*:

```
pip install pythomac
```
````

````{tab-item} clone pythomac

Cloner le dépôt *pythomac* de [GitHub](https://github.com/hydro-informatics/pythomac):

```
git clone https://github.com/hydro-informatics/pythomac.git
```

Copiez-collez le dossier `pythomac/pythomac/` dans votre répertoire de simulation. Autrement dit, assurez-vous que le script Python `/HOME/pythomac/extract_fluxes.py` (entre autres) est correctement situé, à côté de `/HOME/your-simulation-dir/steady2d.cas`.
````

````{tab-item} download pythomac as zip

Téléchargez une archive zippée du dépôt *pythomac* depuis [GitHub (cliquez ici à droite > enregistrer sous...)](https://github.com/hydro-informatics/pythomac/archive/refs/heads/main.zip). Ouvrez l'archive zip > ouvrir `pythomac-main`, et extraire le contenu du dossier `pythomac` (i.e., `pythomac-main/pythomac/`) à côté de votre répertoire de simulation. Autrement dit, assurez-vous que le script Python `/HOME/pythomac/extract_fluxes.py` (entre autres) est correctement situé, à côté de `/HOME/your-simulation-dir/steady2d.cas`.
````
`````

````{admonition} Expand to see the code in the extract_fluxes.py Python script:
:class: tip, dropdown
:name: python-extract-fluxes-telemac

```python
""" Extract data from a Telemac simulation that has already been running.
The codes are inspired by the following jupyter notebook:
    HOMETEL/notebooks/data_manip/extraction/output_file_extraction.ipynb
 which uses the following example case:
    /examples/telemac2d/bump/t2d_bump_FE.cas
"""

# retrieve file paths - this script must be stored in the directory where the simulation lives
import sys
import os
# data processing
import pandas as pd
import numpy as np
# plotting
import matplotlib
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
# Telemac stuff
from parser_output import get_latest_output_files
from parser_output import OutputFileData


def extract_fluxes(
        model_directory="",
        cas_name="steady2d.cas",
        plotting=True
):
    """This function writes a .csv file and an x-y plot of fluxes across the boundaries of a Telemac2d model. It auto-
        matically place the .csv and .png plot files into the simulation directory (i.e., where the .cas file is).

    Notes:
        * The Telemac simulation must have been running with the '-s' flag (``telemac2d.py my.cas -s``).
        * Make sure to activate the .cas keyword ``PRINTING CUMULATED FLOWRATES : YES``
        * This script skips volume errors (search tags are not implemented).
        * Read more about this script at
            https://hydro-informatics.com/numerics/telemac/telemac2d-steady.html#verify-steady-tm2d

    :param str model_directory: the file directory where the simulation lives
    :param str cas_name: name of the .cas steering file (without directory)
    :param bool plotting: default (True) will place a figure called flux-convergence.png in the simulation directory
    :return pandas.DataFrame: time series of fluxes across boundaries (if Error int: -1)
    """

    # assign cas file name in the folder
    file_name = get_latest_output_files(
        os.path.join(model_directory,  # os.path.dirname(os.path.realpath(__file__))
                     cas_name
                     )
        )

    # go to working directory
    try:
        os.chdir(model_directory)
    except Exception as problem:
        print("ERROR: the provided directory {0} does not exist:\n{1}".format(str(model_directory), str(problem)))
        return -1

    try:
        out_file = OutputFileData(file_name[0])
    except Exception as e:
        print("CAS name: " + str(os.path.join(os.path.dirname(os.path.realpath(__file__)), cas_name)))
        print("ERROR in file {0}:\n{1}".format(str(file_name), str(e)))
        print("Recall: the simulation must run with the -s flags")
        return -1

    print("Found study with name: {}".format(out_file.get_name_of_study()))
    print("The simulation took: {} seconds".format(out_file.get_exec_time()))

    # extract total volume, fluxes, and volume error
    out_fluxes = out_file.get_value_history_output("voltotal;volfluxes;volerror")
    out_fluxes_dict = {}
    for e in out_fluxes:
        try:
            # differentiate between Time and Flux series with nested lists
            if not isinstance(e[0], tuple):
                out_fluxes_dict.update({e[0]: np.array(e[1])})
            else:
                for sub_e in e:
                    try:
                        if "volume" in str(sub_e[0]).lower():
                            # go here if ('Volumes (m3/s)', [volume(t)])
                            out_fluxes_dict.update({sub_e[0]: np.array(sub_e[1])})
                        if "fluxes" in str(sub_e[0]).lower():
                            for bound_i, bound_e in enumerate(sub_e[1]):
                                out_fluxes_dict.update({
                                    "Fluxes {}".format(str(bound_e)): np.array(sub_e[2][bound_i])
                                })
                    except Exception as problem:
                        print("ERROR in intended VOLUME tuple " + str(sub_e[0]) + ":\n" + str(problem))
        except Exception as problem:
            print("ERROR in " + str(e[0]) + ":\n" + str(problem))
            print("WARNING: Flux series seem empty. Verify:")
            print("         - did you run telemac2d.py sim.cas with the -s flag?")
            print("         - did your define all required VARIABLES FOR GRAPHIC PRINTOUTS (U,V,S,B,Q,F,H)?")

    try:
        df = pd.DataFrame.from_dict(out_fluxes_dict)
        df.set_index(list(df)[0], inplace=True)
    except Exception as problem:
        print("ERROR: could not convert dict to DataFrame because:\n" + str(problem))
        return -1

    export_fn = "extracted_fluxes.csv"
    print("* Exporting to {}".format(str(os.path.join(model_directory, export_fn))))
    df.to_csv(os.path.join(model_directory, export_fn))

    if plotting:
        font = {'size': 9}
        matplotlib.rc('font', **font)
        fig = plt.figure(figsize=(6, 3), dpi=400)
        axes = fig.add_subplot()
        colors = plt.cm.Blues(np.linspace(0, 1, len(df.columns)))
        markers = ("x", "o", "s", "+", "1", "D", "*", "CARETDOWN", "3", "^", "p", "2")
        for i, y in enumerate(list(df)):
            if "flux" in str(y).lower():
                axes.plot(df.index.values, df[y].abs(), color=colors[i], markersize=2, marker=markers[i], markerfacecolor='none',
                          markeredgecolor=colors[i], linestyle='-', linewidth=1.0, alpha=0.6, label=y)
        axes.set_xlim((np.nanmin(df.index.values), np.nanmax(df.index.values)))
        axes.set_ylim(bottom=0)
        axes.set_xlabel("Time (s)")
        axes.set_ylabel("Fluxes (m$^3$/s)")
        axes.legend(loc="best", facecolor="white", edgecolor="gray", framealpha=0.5)
        fig.tight_layout()
        fig.savefig(os.path.join(model_directory, "flux-convergence.png"))
        print("* Saved plot as " + str(os.path.join(model_directory, "flux-convergence.png")))
    return df
```
````

Detailed instructions for using the `extract_fluxes()` function through pythomac and its dependencies (`numpy`, `pandas`, and `matplotlib`) can be found at [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io).

Pour utiliser les fonctions définies dans `pythomac`, copiez le code suivant dans un nouveau script Python appelé, par exemple, `example_flux_convergence.py` dans le répertoire où la simulation stable2d à l'initialisation sèche a été exécutée (ou [téléchargez exemple flux convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py)):


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

```{admonition} Got errors? Verify that the simulation directories are correct.
:class: error

L'ajout d'une ligne simple `print(simulation_dir)` dans le bloc de code ci-dessus pourrait aider à vérifier la justesse des répertoires. Autrement dit, le code Python devrait être capable d'affiner la simulation.
```

Exécutez le script Python depuis Terminal (ou Anaconda Prompt) comme suit (assurez-vous à `cd` dans le répertoire de simulation):

```
python example_flux_convergence.py
```

Le script sera placé dans le dossier de simulation :

* un fichier CSV appelé [extracted fluxes.csv (télécharger)](https://github.com/hydro-informatics/telemac/raw/main/steady2d-tutorial/extracted_fluxes.csv), et
* un tracé des convergences de flux (*flux-convergence.png*) à travers les limites du modèle (voir {numref}`Fig. %s <steady-flux-convergence>`) montrant qualitativement que les flux ont atteint la convergence après environ 6000-7000 pas de temps.

```{figure} ../../img/telemac/flux-convergence.png
:alt: python telemac flux discharge convergence pythomac
:name: steady-flux-convergence

La courbe de convergence du flux franchit les deux limites de la simulation stabilisée à sec Telemac2d avec un temps total de simulation de quelques secondes, créée avec la fonction pythomac.extract fluxes().
```

(tm-calculate-convergence)=
## Identifier la convergence

Pour tester si et quand les flux convergent, nous suivons le déséquilibre relatif des flux pour chaque étape de temps $t$ comme:

```{math}
:label: error_rate
\varepsilon {t} = \frac{\left=Q {i,t}
```

où $Q_{i,t}$ et $Q_{j,t}$ sont les flux sortants et entrants au-delà des limites du modèle à timestep $t$, respectivement. Les magnitudes de flux $|\cdot|$ sont utilisées parce que Telemac signale les flux limites avec un signe (flux positif, flux négatif); le bilan massique correspond alors à $|Q_{i,t}| = |Q_{j,t}|$, de sorte que $\varepsilon_{t} \to 0$ à la convergence, et la normalisation par l'afflux $|Q_{j,t}|$ rend $\varepsilon_{t}$ sans dimension. Dans une simulation stable et régulière, le rapport des déséquilibres de flux consécutifs devrait converger vers une constante de convergence $c_{\varepsilon}$ égale à l'unité avec un temps croissant:

```{math}
:label: error_lim
\lim {t\to \infty} \frac{\varepsilon {t+1}}{\varepsilon^{\iota} {t}} = c {\varepsilon}
```

La combinaison du taux de convergence (ou ordre) $\iota$, et la constante de convergence $c_{\varepsilon}$ indiquent:

* convergence linéaire si $\iota$ = 1 ** et** $c_{\varepsilon} \in ]0, 1[$
* lent * sublinéaire * convergence si $\iota$ = 1 ** et** $c_{\varepsilon}$ = 1
* rapide * superlinéaire * convergence si $\iota$ > 1 ** et** $c_{\varepsilon} \in ]0, 1]$
* convergence des divergences si $\iota$ = 1 **et** $c_{\varepsilon}$ > 1; **ou** $\iota$ < 1

````{aside} Calculate $\varepsilon_{t+1}$

Pour calculer $\varepsilon_{t+1}$ (`epsilon_t1`) à partir de $\varepsilon_{t}$ (`epsilon_t0`), il suffit de rouler $\varepsilon_{t}$ par un élément dans Python :

```python
epsilon_t0 = epsilon[:-1]  # cut off last element
epsilon_t1 = epsilon[1:]   # cut off element zero
```
````

Pour déterminer le moment où une simulation régulière peut être considérée comme ayant atteint un état stable, nous voulons observer quand $\iota$ = 1 et $c_{\varepsilon}$ = 1 indiquent une convergence sublinéaire. C'est-à-dire, nous cherchons le timestep $t$ au-dessus duquel chaque timestep supplémentaire $t+1$ n'améliore que de façon insignifiante la précision du modèle (lire davantage sur le terme *insignificative* dans le {ref}`below section <tm-target-conv>`). Ainsi, en supposant que les convergences du modèle sous quelque forme que ce soit, nous pouvons définir $c_{\varepsilon}$ = 1 pour calculer $\iota (t)$ en fonction de $\varepsilon_{t}$ et $\varepsilon_{t+1}$:

\début{align}
\label{estimation convergence}
\frac{\varepsilon {t+1}}{\varepsilon^{\iota(t)}} {t}} &=c {\varepsilon} & \Leftrightarrow \\
\iota(t) &= \frac{1}{c {\varepsilon}} \cdot \log {\varepsilon {t}\varepsilon {t+1}} & \overbrace{\Longleftrightarrow}^{c {\varepsilon} = 1}\\
\iota(t) &= \log {\varepsilon {t}\varepsilon {t+1}} &
\end{align}

Cette équation peut être mise en œuvre dans une fonction Python comme suit:


```python
import numpy as np
import pandas as pd


def calculate_convergence(Q_in, Q_out, conv_constant=1.):
    # relative flux imbalance epsilon_t = ||Q_in| - |Q_out|| / |Q_in|; the magnitudes |.|
    #   are needed because Telemac reports outflow negative, so that balance -> epsilon -> 0
    epsilon = np.abs(np.abs(Q_in) - np.abs(Q_out)) / np.abs(Q_in)
    # derive epsilon at t and t+1
    epsilon_t0 = epsilon[:-1]  # cut off last element
    epsilon_t1 = epsilon[1:]   # cut off element zero
    # return the relative imbalance and the convergence rate iota as a pandas DataFrame
    return pd.DataFrame({
        "Relative imbalance": epsilon_t1,
        "Convergence rate": np.emath.logn(epsilon_t0, epsilon_t1) / conv_constant,
    })
```

````{admonition} Also this function is available in pythomac
:class: tip

```python
from pythomac import calculate_convergence
```
````

Pour calculer $\iota (t)$ (nom variable Python : `iota_t`) avec la fonction ci-dessus, modifier le *exemple flux convergence.py* script Python :

```python
# example_flux_convergence.py

# ...
# add to header (alternatively copy-paste the above function into this script):
from pythomac import calculate_convergence

# calculate fluxes_df (see above code block)
fluxes_df = [...]

# calculate iota (t) with the calculate_convergence function
iota_t = calculate_convergence(
    fluxes_df["Fluxes Boundary 1"][1:],  # remove first zero-entry
    fluxes_df["Fluxes Boundary 2"][1:],  # remove first zero-entry
)
```

Le taux de convergence résultant $\iota (t)$ est tracé à {numref}`Fig. %s <tm-convergence-rate>` pour le {ref}`steady 2d tutorial <telemac2d-steady>`, avec les périodes d'impression modifiées de `50` secondes et un temps de simulation total de `10000` secondes.

```{figure} ../../img/telemac/convergence-rate.png
:alt: convergence rate fluxes telemac boundaries
:name: tm-convergence-rate

Le taux de convergence $\iota$ en tant que fonction 10000 temps de simulation de la simulation stable 2d.
```

(tm-target-conv)=
## Temps de simulation optimal dérivé

Pour économiser du temps informatique, nous nous intéressons à l'étape de convergence des flux entrants et sortants. Les flux tracés dans {numref}`Fig. %s <steady-flux-convergence>`, et le taux de convergence dans {numref}`Fig. %s <tm-convergence-rate>` qualitativement suggèrent que la simulation était stable après environ 6000 secondes (temps pas). Les bosses dans les deux chiffres après 4000 pas de temps indiquent bien la « rencontre » des « ondes » de flux provenant des limites amont et aval (voir {ref}`animation in the steady 2d tutorial <telemac-flow-convergence-gif>`). Ce n'est qu'après que la convergence a commencé.

La définition du moment de la convergence peut être subjective. Pour économiser du temps informatique, nous cherchons le plus petit temps $t$ au-delà duquel le déséquilibre relatif du flux $\varepsilon_{t}$ (Equation {eq}`error_rate`) reste en permanence en dessous d'une tolérance cible $\varepsilon_{tar}$. Les tolérances de $\varepsilon_{tar}$ = 10$^{-4}$ sont généralement acceptables pour les essais d'étalonnage préliminaires, tandis que la validation et les essais d'initialisation à chaud justifient des valeurs plus faibles (10$^{-6}$ ou moins). Comme l'illustre {numref}`Fig. %s <tm-convergence-rate>`, le déséquilibre peut tomber brièvement sous la tolérance et remonter après environ 4000 pas de temps, lorsque l'onde en amont roule sur la limite en aval; seul le dernier passage permanent compte. Par conséquent, nous voulons une implémentation algorithmique qui détecte la dernière étape à laquelle $\varepsilon_{t} \geq \varepsilon_{tar}$ et prend la prochaine comme temps de convergence. À cette fin, nous pouvons ajouter à la *exemple flux convergence.py* script Python le code suivant:

```python
# example_flux_convergence.py

# ...

# calculate fluxes_df (see above code block)
fluxes_df = [...]

# calculate iota_t with calculate_convergence (also returns a "Relative imbalance" column)
iota_t = [...]

# define a desired target tolerance (epsilon_tar) for the relative flux imbalance
target_convergence_precision = 1.0E-4

# get the relative flux imbalance epsilon_t (Delta_Q) from calculate_convergence
relative_imbalance = iota_t["Relative imbalance"].to_numpy()

# find the index of the last element that still exceeds the target tolerance and add +1
#   (i.e., the first element from which the imbalance stays permanently below the tolerance)
below_tolerance = relative_imbalance < target_convergence_precision
idx = np.flatnonzero(~below_tolerance)[-1] + 1

# print the timestep at which the desired convergence was achieved to the console
printout_period_in_cas = 50  # the printout period defined in the cas file
print("The simulation converged after {0} simulation seconds ({1}th printout).".format(
        str(printout_period_in_cas * idx), str(idx)))
```

```  
The simulation converged after 6000 simulation seconds (120th printout).
```

````{admonition} Bolster your code
:class: tip

The code for calculating the timestep at which a target convergence level was achieved is also implemented in the `get_convergence_time()` function in `pythomac`:

```python
from pythomac import get_convergence_time
```

A full implementation with also a convenient way for retrieving the `printout_period_in_cas` variable can be found in [this version of example_flux_convergence.py](https://github.com/hydro-informatics/pythomac/blob/main/example_flux_convergence.py) with documentation on [https://pythomac.readthedocs.io](https://pythomac.readthedocs.io/en/latest/convergence.html).
````

Maintenant que vous savez que votre simulation Telemac converge de manière satisfaisante, vous pouvez réduire le paramètre `NUMBER OF TIME STEPS` dans le fichier de pilotage `.cas`, par exemple:

```fortran
/ steady2d-conv.cas
TIME STEP : 1.
NUMBER OF TIME STEPS : 6000
GRAPHIC PRINTOUT PERIOD : 50
LISTING PRINTOUT PERIOD : 50
```

## Dépannage des instabilités et des divergences

Si une simulation régulière n'atteint jamais la stabilité des flux ou même la divergence des flux, assurez-vous que toutes les limites sont bien définies selon la section des projecteurs sur {ref}`boundary conditions <tm-foc-bc>`, et regardez le flux de travail dans la section suivante sur {ref}`mass conservation <tm-foc-mass>`.
