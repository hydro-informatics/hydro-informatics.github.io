---
description: Leitfaden zur Wahl von wahrnehmbar-uniform und colorblind-freundlichen Farbkarten in Matplotlib und cmocean für wissenschaftliche Datenvisualisierung, ersetzt irreführende Regenbogen-Jet-Paletten.
---

(friendly-colors)=
# Perceptually-Uniform, Colorblind-Friendly Colormaps

## Regenbogen/Jet vermeiden

* **Nicht wahrnehmbar gleichmäßig:** gleiche numerische Schritte sehen nicht aus wie gleiche visuelle Schritte; nicht-monotonische Helligkeit führt falsche "Zähle" ein, die Interpretation irreführen können.
* ** Probleme der Erreichbarkeit: ** Regenbogen-Palette bilden deutliche Farbtöne, die viele Zuschauer mit Farbsichtmangel (ca. 1 bei 12 Männern) nicht zuverlässig unterscheiden können.
* **Context Switching:** abrupte Farbsprünge machen Lesegradienten und subtile Trends härter, insbesondere wenn sie auf Projektoren gedruckt oder betrachtet werden.

## Was stattdessen zu verwenden

Wählen Sie Farbkarten für *uniform wahrgenommene Änderung* (in der Regel monotone Helligkeit) und *CVD Robustheit*:

* **Sequential (low > high):** e.g., Matplotlib's `viridis`, `magma`, `plasma`, `inferno`; cmocean's domain-aware sequences (e.g., `cmo.thermal` for temperature, `cmo.haline` for salinity).
* **Diverging (midpoint emphasis):** use when values deviate around a meaningful center (0, climatology, etc.). Examples: Matplotlib's `seismic`-style but *perceptually tuned* options like `coolwarm` (still imperfect) or cmocean's `balance`, `delta`, `curl`, which are engineered for symmetry and lightness control.
* **Cyclic (wrap-around variables):** for phase/aspect (0°≡360°). Use cyclic maps such as cmocean's `phase`.
* **Categorical (discrete classes):** use distinct, desaturated palettes with good lightness separation; avoid "rainbow" categories for quantitative data.

## Wählen Sie die richtige Karte für Ihre Daten

* **Monotonic Daten:* sequentiell.
**Signierte Anomalien um eine Referenz: ** divergiert mit einem klar definierten, *perzeptuell zentralen* Mittelpunkt.
* ** Winkel/Ausrichtung:* zyklisch, so dass die Endpunkte übereinstimmen.
* ** Dynamische Reichweite:** sorgen dafür, dass die Leichtigkeitsrampe den Bereich überspannt, in dem Ihr Publikum Diskriminierung braucht (Sie können den Farbbereich bei Bedarf trimmen/clipen).
* **Background:** Wählen Sie eine Karte aus, deren Helligkeit mit dem Abbildungshintergrund kontrast (dunkle Karten auf dunklen Hintergründen obskurieren niedrige Werte).

## Schnelle Rezepte

### Matplotlib + cmocean

Installieren Sie cmocean (Matplotlib-Port):

```
pip install cmocean
```

Setzen Sie einen globalen Standard und ein Diagramm:

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

Mehr cmocean info: [matplotlib.org/cmocean](https://matplotlib.org/cmocean/)

### Fabio Crameri's cm Werkzeuge

[Fabio Crameri](https://www.fabiocrameri.ch) developed a sophisticated toolset for scientific color maps that are universally readable by color-vision deficient and color-blind individuals, and when printed in black and white. For background information, refer to {cite:t}`crameri2020misuse` ([direct link](https://www.nature.com/articles/s41467-020-19160-7)) and Fabio Crameri's [EGU blogpost](https://blogs.egu.eu/divisions/gd/2017/08/23/the-rainbow-colour-map). The Python package `cmcrameri` is hosted at [https://pypi.org/project/cmcrameri ](https://pypi.org/project/cmcrameri).

Hier ist eine schnelle Möglichkeit, die cmcrameri wissenschaftlichen Farbkarten in Python zu verwenden:

1. Installieren

```bash
pip install cmcrameri
```

2. Grundnutzung mit Matplotlib

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

Alle Farbkarten sind unter `cmcrameri.cm.<name>` erhältlich.

3. Reversierte und kategorische Varianten

```python
plt.imshow(Z, cmap=cm.batlow_r)
```

Kategorische (diskrete) Versionen verwenden einen "S"-Suffix, beispielsweise `cm.batlowS`.

4. Schnell verfügbare Karten durchsuchen

```python
from cmcrameri import show_cmaps
show_cmaps()
```

Dies zeigt alle installierten cmcrameri-Farbkarten in der Python-Sitzung.

5. Gute Voreinstellungen und Tipps
* Folgedaten: Start mit `batlow` oder `oslo`.
* Diverging data centre on zero: versuchen Sie `vik` oder `broc`.

Diese Paletten sind so konzipiert, dass sie wahrnehmbar bestellt und fair sind und für viele Formen von Farbvisionsmangel lesbar bleiben.

6. Einen projektweiten Standard festlegen (optional)

```python
import matplotlib as mpl
import cmcrameri.cm as cm
mpl.rcParams["image.cmap"] = cm.batlow
```

Matplotlib akzeptiert ein Colormap-Objekt für `image.cmap`. Siehe Matplotlib's colormap docs für allgemeines Verhalten. ([Matplotlib][4])

Verwenden Sie `cm.<name>`, fügen Sie `_r` für reversed, `S` für kategorisch und `show_cmaps()` zu erkunden.



## Zahlen farbblind-safe (Linux + GNOME)

Eine praktische Möglichkeit, *simulieren* häufige Farb-Vision Mängel direkt auf Ihrem Bildschirm ist die GNOME Shell Erweiterung **Colorblind Filter**. Es gilt Echtzeit-Filter, so können Sie vorhersehen, wie Ihre Grundstücke unter Deuteranopia, Protanopia, Tritanopia, etc. aussehen.

* Erweiterung: [G-dH/gnome-colorblind-filters](https://github.com/G-dH/gnome-colorblind-filters)
* Workflow: erzeugen Sie Ihre Plots > toggle the relevant filter > anpassen Farbkarte/Bereich/Linien-Stile, bis die Figur lesbar bleibt.

## Best-Practice Checkliste

* Benutzen Sie * * * * augenscheinlich einheitliche ** Karten mit ** monotoner Helligkeit** für quantitative Gradienten.
* Match **map type** to **data type** (sequential/diverging/cyclic).
* Stellen Sie sicher ** kontrastreich* und lesbar **colorbar Zecken/labels*; setzen Sie aussagekräftige Grenzen (`vmin/vmax`, zentrierte divergierende Skalen).
* Verifizieren Sie ** Zugänglichkeit** mit CVD-Simulation; verlassen Sie sich nicht allein auf die Farbe -add Konturen, Annotationen oder unterschiedliche Linienstilen, wo hilfreich.
* Seien Sie konsistent über Panels und Publikationen; dokumentieren Sie die Farbkarte Wahl in Beschriftungen (z.B. "cmocean 'balance'").


