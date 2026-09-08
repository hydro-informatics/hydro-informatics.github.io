---
description: Leitfaden zur Auswahl perzeptuell einheitlicher und farbenblindfreundlicher Colormaps in Matplotlib und cmocean für die wissenschaftliche Datenvisualisierung, die irreführende Regenbogen- / Jetpaletten ersetzen.
---

(friendly-colors)=
# Perzeptuell einheitliche, farbenblinde Colormaps

## Regenbogen/Jet vermeiden

* ** Nicht perzeptuell einheitlich: gleiche numerische Schritte sehen nicht wie gleiche visuelle Schritte aus; nicht-monotonische Leichtigkeit führt falsche "Ränder" ein, die die Interpretation irreführen können.
* ** Zugänglichkeitsprobleme: ** Regenbogenpaletten zeichnen verschiedene Farbtöne ab, die viele Zuschauer mit Farbsehschwächen (ca. 1 von 12 Männern) nicht zuverlässig unterscheiden können.
* **Kontextwechsel: abrupte Farbsprünge machen Leseverläufe und subtile Trends schwieriger, insbesondere wenn sie auf Projektoren gedruckt oder angesehen werden.

## Was stattdessen zu verwenden ist

Wählen Sie Colormaps, die für * gleichmäßig wahrgenommene Veränderung * (normalerweise monotone Leichtigkeit) und *CVD-Robustheit * konzipiert sind:

* **Sequentiell (niedrig > hoch): ** z.B. Matplotlibs `viridis`, `magma`, `plasma`, `inferno`; cmoceans domänenbewusste Sequenzen (z.B. `cmo.thermal` für Temperatur, `cmo.haline` für Salzgehalt).
* **Verschieden (Hervorhebung des Mittelpunkts):** Verwenden Sie, wenn Werte um ein sinnvolles Zentrum (0, Klimatologie usw.) abweichen. Beispiele: Matplotlibs `seismic`-Stil, aber *wahrnehmungsmäßig abgestimmte* Optionen wie `coolwarm` (immer noch unvollkommen) oder cmoceans `balance`, `delta`, `curl`, die für Symmetrie und Leichtigkeitskontrolle entwickelt wurden.
* **Cyclic (wrap-around variables):** for phase/aspect (0°≡360°). Use cyclic maps such as cmocean's `phase`.
* **Kategorisch (diskrete Klassen):** Verwenden Sie verschiedene, desaturierte Paletten mit guter Leichtigkeitstrennung; vermeiden Sie "Regenbogen" -Kategorien für quantitative Daten.

## Die richtige Karte für Ihre Daten auswählen

* **Monotische Daten:** sequentiell.
* **Signierte Anomalien um eine Referenz:** divergierend mit einem klar definierten, *wahrnehmungsmäßig zentralen* Mittelpunkt.
* **Winkel/Orientierungen:** zyklisch, so dass die Endpunkte übereinstimmen.
* **Dynamischer Bereich:** Stellen Sie sicher, dass die Leichtigkeitsrampe den Bereich abdeckt, in dem Ihre Zielgruppe diskriminiert werden muss (Sie können den Colormap-Bereich bei Bedarf trimmen/clippen).
* **Hintergrund:** Wählen Sie eine Karte, deren Helligkeit mit dem Figurenhintergrund kontrastiert (dunkle Karten auf dunklen Hintergründen verdecken niedrige Werte).

## Schnelle Rezepte

### Matplotlib + cmocean

Installieren Sie cmocean (Matplotlib Port):

```
pip install cmocean
```

Setzen Sie einen globalen Standard und Plot:

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

Weitere cmocean Infos: [matplotlib.org/cmocean](https://matplotlib.org/cmocean/)]

### Fabio Crameris cm Werkzeuge

[Fabio Crameri](https://www.fabiocrameri.ch) developed a sophisticated toolset for scientific color maps that are universally readable by color-vision deficient and color-blind individuals, and when printed in black and white. For background information, refer to {cite:t}`crameri2020misuse` ([direct link](https://www.nature.com/articles/s41467-020-19160-7)) and Fabio Crameri's [EGU blogpost](https://blogs.egu.eu/divisions/gd/2017/08/23/the-rainbow-colour-map). The Python package `cmcrameri` is hosted at [https://pypi.org/project/cmcrameri ](https://pypi.org/project/cmcrameri).

Hier ist eine schnelle Möglichkeit, die cmcrameri wissenschaftlichen Colormaps in Python zu verwenden:

1. Installieren

```bash
pip install cmcrameri
```

2. Grundlegende Nutzung mit Matplotlib

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

3. Umgekehrte und kategorische Varianten

```python
plt.imshow(Z, cmap=cm.batlow_r)
```

Categorical (discrete) versions use an "S" suffix, for example `cm.batlowS`.

4. Schnell durchsuchen verfügbare Karten

```python
from cmcrameri import show_cmaps
show_cmaps()
```

Dies zeigt alle installierten cmcrameri Colormaps in der Python-Sitzung an.

5. Gute Defaults und Tipps
   * Sequenzielle Daten: Beginnen Sie mit `batlow` oder `oslo`.
   * Diverging data centered on zero: try `vik` or `broc`.

Diese Paletten sind so konzipiert, dass sie perzeptuell geordnet und fair sind und für viele Formen von Farbmangel lesbar bleiben.

6. Setzen Sie einen projektweiten Standard (optional)

```python
import matplotlib as mpl
import cmcrameri.cm as cm
mpl.rcParams["image.cmap"] = cm.batlow
```

Matplotlib akzeptiert ein Colormap-Objekt für `image.cmap`. Siehe Matplotlibs Colormap-Dokumente für allgemeines Verhalten. ([Matplotlib][4])

Verwenden Sie `cm.<name>`, fügen Sie `_r` für umgekehrt, `S` für kategorisch und `show_cmaps()` zum Erkunden hinzu.



## Stellen Sie Figuren farbenblind sicher (Linux + GNOME)

Eine praktische Möglichkeit, häufige Farbsichtmängel direkt auf Ihrem Bildschirm zu simulieren, ist die GNOME Shell-Erweiterung **Farbblindfilter **. Es wendet Echtzeitfilter an, so dass Sie eine Vorschau erhalten können, wie Ihre Plots unter Deuteranopia, Protanopia, Tritanopia usw. aussehen.

* Erweiterung: [G-dH/gnome-colorblind-filters](https://github.com/G-dH/gnome-colorblind-filters)]
* Workflow: Erzeugen Sie Ihre Plots > Umschalten des relevanten Filters > Anpassen der Colormap / Range / Line-Stile, bis die Figur lesbar bleibt.

## Best Practice Checkliste

* Verwenden Sie **wahrnehmungsmäßig einheitliche ** Karten mit **monotonischer Leichtigkeit ** für quantitative Gradienten.
* Match **map type** to **data type** (sequenziell/divergierend/zyklisch).
* Stellen Sie sicher **Kontrast ** und lesbare **Farbbalken Ticks / Labels **; Setzen Sie sinnvolle Grenzen (`vmin/vmax`, zentrierte divergierende Skalen).
* Überprüfen Sie die Zugänglichkeit mit CVD-Simulation; Verlassen Sie sich nicht nur auf Farbe - fügen Sie Konturen, Anmerkungen oder unterschiedliche Linienstile hinzu, wenn dies hilfreich ist.
* Seien Sie konsistent in allen Panels und Publikationen; dokumentieren Sie die Colormap-Auswahl in Beschriftungen (z. B. "cmocean 'balance'").


