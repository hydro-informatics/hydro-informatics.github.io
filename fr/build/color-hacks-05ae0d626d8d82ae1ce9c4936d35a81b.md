---
description: Guide de choix perceptually-uniforme et coloraved-friendly colormaps dans Matplotlib et cmocean pour la visualisation des données scientifiques, remplaçant les palettes trompeuses arc-en-ciel/jet.
---

(friendly-colors)=
# Perceptually-Uniform, coloravedly-friendly Colormaps

## Éviter l'arc-en-ciel/projet

* **Pas d'uniformité perceptible :** les étapes numériques égales ne ressemblent pas à des étapes visuelles égales ; la légèreté non-monotonique introduit de faux « bords » qui peuvent induire en erreur l'interprétation.
* **Questions d'accessibilité:** palettes arc-en-ciel cartographient des teintes distinctes que de nombreux téléspectateurs avec des déficiences de vision couleur (environ 1 homme sur 12) ne peuvent pas différencier de façon fiable.
* **Changement de contexte :** les sauts brusques rendent les gradients de lecture et les tendances subtiles plus difficiles, surtout lorsqu'ils sont imprimés ou consultés sur des projecteurs.

## À utiliser à la place

Choisissez des cartes de couleur conçues pour *changement perçu uniforme* (habituellement la légèreté monotonique) et *la robustesse CVD*:

* **Séquentiel (faible > élevé):** p.ex., Matplotlib's `viridis`, `magma`, `plasma`, `inferno`; les séquences du domaine-aware (p.ex., `cmo.thermal` pour la température, `cmo.haline` pour la salinité).
* **Divergence (accent sur le point médian):** utiliser lorsque les valeurs s'écartent autour d'un centre significatif (0, climatologie, etc.). Exemples : Matplotlib's `seismic`-style mais *perceptually accorded* options comme `coolwarm` (toujours imparfaite) ou cmocean's `balance`, `delta`, `curl`, qui sont conçus pour le contrôle de la symétrie et de la légèreté.
* **Cyclique (variables d'arrondi):** pour phase/aspect (0°) 360°. Utiliser des cartes cycliques telles que `phase`.
* **Categorical (classes discrètes):** utiliser des palettes distinctes et désaturées avec une bonne séparation de la légèreté; éviter les catégories "rainbow" pour les données quantitatives.

## Choisir la bonne carte pour vos données

* **Données monotoniques:** séquentielle.
* **Anomalies de l'ordre d'une référence :** divergent d'un point médian clairement défini, *perceptuellement central*.
* ** Angles/orientations:** cycliques de sorte que les paramètres correspondent.
* ** Gamme dynamique :** s'assurer que la rampe de légèreté couvre la gamme où votre public a besoin de discrimination (vous pouvez couper/cliper la gamme colormap si nécessaire).
* **Contexte :** choisir une carte dont la légèreté contraste avec le fond de la figure (des cartes sombres sur des fonds sombres masquent des valeurs basses).

## Recettes rapides

### Matplotlib + cmocéan

Installer le port de Matplotlib:

```
pip install cmocean
```

Définir une valeur par défaut globale et un graphique :

```python
import matplotlib.pyplot as plt
import numpy as np
import cmocean

# Set a perceptually-uniform default
plt.rcParams["image.cmap"] = "viridis"

# Example data
x = np.linspace(-3, 3, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)
Z = np.hypot(X, Y)

# Sequential (distance field)
plt.imshow(Z, origin="lower", cmap=cmocean.cm.thermal)
plt.colorbar(label="Temperature-like quantity")
plt.title("Sequential, perceptually-uniform")
plt.show()

# Diverging (positive/negative anomaly)
Z_anom = np.sin(X) * np.cos(Y)
plt.imshow(Z_anom, origin="lower", cmap=cmocean.cm.balance, vmin=-1, vmax=1)
plt.colorbar(label="Anomaly")
plt.title("Diverging around 0")
plt.show()

# Cyclic (phase)
Z_phase = np.angle(np.exp(1j*(X)))
plt.imshow(Z_phase, origin="lower", cmap=cmocean.cm.phase)
plt.colorbar(label="Phase [rad]")
plt.title("Cyclic for wrap-around variables")
plt.show()
```

Pour plus d'informations sur les cmocéaniques : [matplotlib.org/cmocean](https://matplotlib.org/cmocean/)

### Outils en cm de Fabio Crameri

[Fabio Crameri](https://www.fabiocrameri.ch) developed a sophisticated toolset for scientific color maps that are universally readable by color-vision deficient and color-blind individuals, and when printed in black and white. For background information, refer to {cite:t}`crameri2020misuse` ([direct link](https://www.nature.com/articles/s41467-020-19160-7)) and Fabio Crameri's [EGU blogpost](https://blogs.egu.eu/divisions/gd/2017/08/23/the-rainbow-colour-map). The Python package `cmcrameri` is hosted at [https://pypi.org/project/cmcrameri ](https://pypi.org/project/cmcrameri).

Voici un moyen rapide d'utiliser les colormaps scientifiques cmcrameri en Python:

1. Installer

```bash
pip install cmcrameri
```

2. Utilisation de base avec Matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np
import cmcrameri.cm as cm

x = np.linspace(-3, 3, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)
Z = np.hypot(X, Y)

plt.imshow(Z, cmap=cm.batlow, origin="lower")
plt.colorbar(label="value")
plt.title("cmcrameri: batlow")
plt.tight_layout()
plt.show()
```

Toutes les couleurs sont disponibles sous `cmcrameri.cm.<name>`.

3. Variantes inversées et catégoriques

```python
plt.imshow(Z, cmap=cm.batlow_r)
```

Les versions catégoriques (discretes) utilisent un suffixe « S », par exemple `cm.batlowS`.

4. Parcourez rapidement les cartes disponibles

```python
from cmcrameri import show_cmaps
show_cmaps()
```

Ceci affiche toutes les cartes de couleurs de cmcrameri installées dans la session Python.

5. Bons par défaut et conseils
   * Données séquentielles : commencez par `batlow` ou `oslo`.
   * Divergence des données centrée sur zéro : essayez `vik` ou `broc`.

Ces palettes sont conçues pour être perceptuellement ordonnées et équitables, et pour rester lisibles pour de nombreuses formes de déficience color-vision.

6. Définir un projet par défaut (facultatif)

```python
import matplotlib as mpl
import cmcrameri.cm as cm
mpl.rcParams["image.cmap"] = cm.batlow
```

Matplotlib accepte un objet Colormap pour `image.cmap`. Voir les documents de matplotlib pour le comportement général. ([Matplotlib][4])

Utilisez `cm.<name>`, ajoutez `_r` pour inverser, `S` pour classer, et `show_cmaps()` pour explorer.



## Faites des figures en aveugle (Linux + GNOME)

Une façon pratique de *simuler* les déficiences communes de la vision couleur directement sur votre écran est l'extension GNOME Shell ** Filtres en aveugle**. Il applique des filtres en temps réel afin que vous puissiez prévisualiser comment vos parcelles semblent sous Deuteranopia, Protanopia, Tritanopia, etc.

* Extension : [G-dH/gnome-colorave-filters](https://github.com/G-dH/gnome-colorblind-filters)
* Workflow: générer vos placettes > basculer le filtre pertinent > ajuster les styles colormap/range/line jusqu'à ce que la figure reste lisible.

## Liste de contrôle des meilleures pratiques

* Utiliser des cartes **perceptuellement uniformes** avec une légèreté **monotonique** pour les gradients quantitatifs.
* Correspondance **type de carte** à **type de données** (séquentiel/divergence/cyclique).
* S'assurer que **contrast** et lisible **colorbar tic/labels**; fixer des limites significatives (`vmin/vmax`, échelles de divergence centrées).
* Vérifier **accessibilité** avec simulation CVD; ne pas compter sur la couleur seule — ajouter des contours, des annotations, ou des styles de lignes variables lorsque utile.
* Être cohérents entre les panneaux et les publications; documenter le choix colormap dans les légendes (p. ex., « équilibre » des cmocéens).


