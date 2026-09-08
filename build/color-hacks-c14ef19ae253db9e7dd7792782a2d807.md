---
description: Guide to choosing perceptually-uniform and colorblind-friendly colormaps in Matplotlib and cmocean for scientific data visualization, replacing misleading rainbow/jet palettes.
---

(friendly-colors)=
# Perceptually-Uniform, Colorblind-Friendly Colormaps

## Avoid rainbow/jet

* **Not perceptually uniform:** equal numeric steps don't look like equal visual steps; non-monotonic lightness introduces false "edges" that can mislead interpretation.
* **Accessibility issues:** rainbow palettes map distinct hues that many viewers with color-vision deficiencies (approx. 1 in 12 men) cannot reliably differentiate.
* **Context switching:** abrupt hue jumps make reading gradients and subtle trends harder, especially when printed or viewed on projectors.

## What to use instead

Choose colormaps designed for *uniform perceived change* (usually monotonic lightness) and *CVD robustness*:

* **Sequential (low > high):** e.g., Matplotlib's `viridis`, `magma`, `plasma`, `inferno`; cmocean's domain-aware sequences (e.g., `cmo.thermal` for temperature, `cmo.haline` for salinity).
* **Diverging (midpoint emphasis):** use when values deviate around a meaningful center (0, climatology, etc.). Examples: Matplotlib's `seismic`-style but *perceptually tuned* options like `coolwarm` (still imperfect) or cmocean's `balance`, `delta`, `curl`, which are engineered for symmetry and lightness control.
* **Cyclic (wrap-around variables):** for phase/aspect (0°≡360°). Use cyclic maps such as cmocean's `phase`.
* **Categorical (discrete classes):** use distinct, desaturated palettes with good lightness separation; avoid "rainbow" categories for quantitative data.

## Picking the right map for your data

* **Monotonic data:** sequential.
* **Signed anomalies around a reference:** diverging with a clearly defined, *perceptually central* midpoint.
* **Angles/orientations:** cyclic so the endpoints match.
* **Dynamic range:** ensure the lightness ramp spans the range where your audience needs discrimination (you can trim/clip the colormap range if needed).
* **Background:** pick a map whose lightness contrasts with the figure background (dark maps on dark backgrounds obscure low values).

## Quick recipes

### Matplotlib + cmocean

Install cmocean (Matplotlib port):

```
pip install cmocean
```

Set a global default and plot:

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

More cmocean info: [matplotlib.org/cmocean](https://matplotlib.org/cmocean/)

### Fabio Crameri's cm tools

[Fabio Crameri](https://www.fabiocrameri.ch) developed a sophisticated toolset for scientific color maps that are universally readable by color-vision deficient and color-blind individuals, and when printed in black and white. For background information, refer to {cite:t}`crameri2020misuse` ([direct link](https://www.nature.com/articles/s41467-020-19160-7)) and Fabio Crameri's [EGU blogpost](https://blogs.egu.eu/divisions/gd/2017/08/23/the-rainbow-colour-map). The Python package `cmcrameri` is hosted at [https://pypi.org/project/cmcrameri ](https://pypi.org/project/cmcrameri).

Here is a quick way to use the cmcrameri scientific colormaps in Python:

1. Install

```bash
pip install cmcrameri
```

2. Basic usage with Matplotlib

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

All colormaps are available under `cmcrameri.cm.<name>`.

3. Reversed and categorical variants

```python
plt.imshow(Z, cmap=cm.batlow_r)
```

Categorical (discrete) versions use an "S" suffix, for example `cm.batlowS`.

4. Quickly browse available maps

```python
from cmcrameri import show_cmaps
show_cmaps()
```

This displays all installed cmcrameri colormaps in the Python session.

5. Good defaults and tips
   * Sequential data: start with `batlow` or `oslo`.
   * Diverging data centered on zero: try `vik` or `broc`.

These palettes are designed to be perceptually ordered and fair, and to remain readable for many forms of color-vision deficiency.

6. Set a project-wide default (optional)

```python
import matplotlib as mpl
import cmcrameri.cm as cm
mpl.rcParams["image.cmap"] = cm.batlow
```

Matplotlib accepts a Colormap object for `image.cmap`. See Matplotlib’s colormap docs for general behavior. ([Matplotlib][4])

Use `cm.<name>`, add `_r` for reversed, `S` for categorical, and `show_cmaps()` to explore.



## Make figures colorblind-safe (Linux + GNOME)

A handy way to *simulate* common color-vision deficiencies directly on your screen is the GNOME Shell extension **Colorblind Filters**. It applies real-time filters so you can preview how your plots look under Deuteranopia, Protanopia, Tritanopia, etc.

* Extension: [G-dH/gnome-colorblind-filters](https://github.com/G-dH/gnome-colorblind-filters)
* Workflow: generate your plots > toggle the relevant filter > adjust colormap/range/line styles until the figure remains readable.

## Best-practice checklist

* Use **perceptually uniform** maps with **monotonic lightness** for quantitative gradients.
* Match **map type** to **data type** (sequential/diverging/cyclic).
* Ensure **contrast** and legible **colorbar ticks/labels**; set meaningful limits (`vmin/vmax`, centered diverging scales).
* Verify **accessibility** with CVD simulation; don't rely on color alone—add contours, annotations, or varying line styles where helpful.
* Be consistent across panels and publications; document the colormap choice in captions (e.g., "cmocean 'balance'").


