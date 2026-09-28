---
description: Python-Übungen für die Hochwasserfrequenzanalyse und die Berechnung der Rückkehrzeit unter Verwendung von Pandas, die Überschreitungswahrscheinlichkeit und Rezidivintervalle für hydrologische Ableitungsdaten abdecken.
---

(ex-floods)=
# Hochwasserrückkehrzeiten

```{admonition} Goals
Load custom modules and functions in a script. Open comma-type delimited files and manipulate files with {ref}`pandas`.
```

```{admonition} Requirements
:class: attention
Python-Bibliotheken: {ref}`pandas` und *matplotlib*. Verstehen Sie die Datenverarbeitung mit {ref}`pandas`.
```

Machen Sie sich bereit, indem Sie das Übungsrepository klonen:

```
git clone https://github.com/Ecohydraulics/Exercise-FloodReturn.git
```

```{figure} ../img/hw-aibling.jpg
:alt: floods Mangfall Bad Aibling Hochwasser
:name: flood-image

Überschwemmung am Mangfall in Bayern (Quelle: KSS 2020).
```

## Terminologie
Die Hochwasserfrequenzanalyse verwendet eine Reihe von Entladungsdaten (z. B. von einer Messstation) und wertet die Eintrittswahrscheinlichkeit einer bestimmten Entladung aus. Die Ereigniswahrscheinlichkeit definiert somit die Häufigkeit einer Entladung, was aus zwei Gründen wichtig ist:

1. **Überwassersicherheit**: Viele rechtliche Rahmen verwenden ein **wiederkehrendes Intervall ** (dh eine Rückkehrzeit oder Häufigkeit in Einheiten von Jahren), um Sicherheitsniveaus zu definieren, die Gebäude und Infrastruktur erfüllen müssen.
1. **Ökohydraulik**: Insbesondere in trockenen Gebieten ist es wichtig zu wissen, wie lange bestimmte Ableitungen unter bestimmten Werten liegen, wo viele aquatische Lebensräume möglicherweise nicht tief genug, zu heiß oder vom Hauptkanal getrennt sind. Daher möchten wir die **Überschreitungswahrscheinlichkeit** einer bestimmten Entlastung wissen.

Die Beziehung zwischen der Überschreitungswahrscheinlichkeit und dem Rezidivintervall ergibt sich aus der Definition beider Begriffe:
* Die **Überschreitungswahrscheinlichkeit** ist die Wahrscheinlichkeit eines Ereignisses einer bestimmten Größenordnung (in m$^3$/s oder CFS) oder höher.
* Das **Rezidivintervall** ist die Umkehrung der Überschreitungswahrscheinlichkeit und drückt die durchschnittliche Rückgabedauer eines Ereignisses einer bestimmten Größe in Zeiteinheiten aus.

Das Berechnungskonzept der Renditeperiode macht zwei elementare Annahmen. Zunächst wird angenommen, dass die einzelnen Strömungsereignisse einen stationären Peak aufweisen. Zweitens wird die statistische Unabhängigkeit einzelner Ereignisse angenommen. Die Annahme der statistischen Unabhängigkeit bedeutet, dass in diesem Jahr eine 100-jährige Flut mit der gleichen Wahrscheinlichkeit auftritt wie im nächsten Jahr, unabhängig davon, ob in diesem Jahr tatsächlich eine 100-jährige Flut aufgetreten ist oder nicht. Für jedes gegebene Jahr beträgt die Wahrscheinlichkeit, dass eine 100-jährige Flut auftritt, 1/100 (oder 1/50 für eine 50-jährige Flut und so weiter).

## Die Wahrscheinlichkeit einer 100-jährigen Flut, die in 100 Jahren auftritt, beträgt 63%

As engineers we often want to know how likely it is that a 100-year flood will occur within the next 2, 5, 10, ... or 100 years (i.e., what are the likely costs of flood damage associated with a 100-year flood?). The answer to that question is *"the opposite likelihood of no 100-year flood occurring in the next 2, 5, or 10 years"*. Mathematically that means the annual occurrence probability $Pr$ of an event with a recurrence interval $T=100$ years over an observation period of $\Delta t \in [2, 5, 10, 100]$ years is:

$Pr(T=100, \Delta t=2, 5, 10, 100) = (1 - (1-1/T)^{\Delta t})$

{numref}`Table %s <tab-pr-floods>` zeigt Lösungen für die Wahrscheinlichkeitsfunktion $Pr(T, \Delta t)$ für Beobachtungszeiträume $\Delta t$ von 2, 5, 10 und 100 Jahren sowie Rezidivintervalle $T$ von 10, 50 und 100 Jahren.

```{list-table} Solutions to the probability function $Pr(T, \Delta t)$ for selected observation periods $\Delta t$.
:header-rows: 1
:name: tab-pr-floods

* - $Pr(T, \Delta t)$
  - $\Delta t$=2
  - $\Delta t$=5
  - $\Delta t$=10
  - $\Delta t$=100

* - $T$=10
  - 19,00 %
  - 40,95%
  - 65,13%
  - 100,00 %

* - $T$=50
  - 3,96%
  - 9,61%
  - 18,29%
  - 86,74%

* - $T$=100
  - 1,99 %
  - 4,90 %
  - 9,56%
  - 63,40 %
```

Besuchen Sie die [*USGS* Wasserwissenschaftsschule](https://www.usgs.gov/special-topic/water-science-school/science/100-year-flood?qt-science_center_objects=0#qt-science_center_objects), um mehr über das Wiederauftreten von Überschwemmungen (und Dürren) zu erfahren.

## Entladedaten erhalten

### Entladedatenquellen

Flussdaten können von Messstationen abgerufen werden. In Deutschland bietet das [Gewässerkundliches Jahrbuch]](http://www.dgj.de/) einen zusammengesetzten Überblick über statistische Daten von Messstationen. Beachten Sie, dass viele Messstationen, wie auch in vielen anderen Ländern, von staatlichen Behörden verwaltet werden und nur ein kleiner Teil der Daten von Bundesinstitutionen verfügbar ist. Zum Beispiel sind Messdaten für Baden-Württemberg beim Landesinstitut für Umwelt, Erhebung und Naturschutz (LUBW) verfügbar [geo portal](https://hvz.lubw.baden-wuerttemberg.de/)]. Die folgende Liste enthält weitere Quellen für Entladungsdaten rund um den Globus.

* Die [Bundesanstalt für Gewässerkunde *BfG*](https://www.bafg.de) betreibt das [Global Runoff Data Centre *GRDC*](https://www.bafg.de/GRDC/EN/Home/homepage_node.html)] für die Weltorganisation für Meteorologie *WMO*, um weltweit Flussabflussdaten bereitzustellen. Die Download-Plattform der *GRDC* ist in Form eines [interaktiven web-GIS](https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser#dataDownload/Home)] verfügbar. Um die Daten zu erhalten, gehen Sie zu ihrer [Download interface](https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser#dataDownload/Stations), wählen Sie die gewünschte Station aus, wechseln Sie zur *Tabellen*-Ansicht (dritte Zeile oben links im Fenster), überprüfen Sie die Station, klicken Sie auf **Download** und füllen Sie das Formular aus, um die Anfrage zu senden. Sie erhalten eine E-Mail mit einem Download-Link für die angeforderten Daten (warten Sie einige Minuten, bevor Sie auf den Link klicken - die Vorbereitung kann mehr Zeit in Anspruch nehmen als die E-Mail).
* Flussdatensätze von alpinen und mittleren Flüssen werden vom Schweizerischen Bundesamt für Umwelt zur Verfügung gestellt [hydrologische Datenplattform](https://www.hydrodaten.admin.ch/) (für Langzeitbeobachtungen muss auch hier ein Formular ausgefüllt werden).
* In den Vereinigten Staaten liefert die National Oceanic and Atmospheric Administration * NOAA* Ableitungsdaten aus der Vergangenheit und Prognosen für Wassereinzugsgebiete in Nordamerika. Zum Beispiel bietet das [California Nevada River Forecast Center](https://www.cnrfc.noaa.gov/)] Flussprognosen für den Südwesten der Vereinigten Staaten, und historische Daten können über das [California Data Exchange Center *CDEC*](http://cdec.water.ca.gov/)] abgerufen werden.
* Eine allgemeine *US*-Schnittstelle zum Laden von Flussdaten und Statistiken ist mit der [`hydrofunctions` *Python* library](https://hydrofunctions.readthedocs.io/), die vom United States Geological Survey *USGS* bereitgestellt wird, ausgestattet.] Diese Bibliothek ermöglicht es, direkt Messdaten und Statistiken basierend auf einer Stream-Messe-ID abzurufen. Zum Beispiel `output = hydrofunctions.peaks("01541200")`
   * Um `hydrofunctions` in einer {ref}`conda <conda-env>` Umgebung zu installieren, geben Sie `conda install -c conda-forge hydrofunctions` in {ref}`Anaconda Prompt <install-pckg>` ein.
   * Anwendungsbeispiel:

```
import hydrofunctions as hf
hf.draw_map()` # only runs in JupyterLab
```

## Daten laden mit *pandas*
Create a new *Python* file (e.g., `discharge_analysis.py`) and import *pandas* as `pd` at the beginning. Read the provided flow data series file `"daily-flow-series.csv"` with `pd.read_csv`.
The header (column names) is in row 36, but we do not use the column names from the *csv* file and overwrite them with the `names` argument (`"Date"` and `"Q (CMS)"` (for Cubic Meters per Second)). Alternatively, we could use the `skiprows` argument to indicate where the data content starts in the file.
With `sep=";"`, we indicate that columns are separated by a semicolon. The `usecols=[0, 2]` argument specifies that we only want to read columns 0 (date) and 2 (discharge) because the information content of column 1 (time) is not relevant for daily discharge. The `parse_dates=[0]` argument lets *pandas* know that column 0 contains date-formatted values. Alternatively, we could use a `dtype={"Date": ... }` dictionary to specify the data formats of columns. However, using `dtype` would require importing `datetime` and induce unnecessary complexity. In addition, the `index_col` argument defines the column indices, which need to have a date format for the later analyses. In addition, use the optional keyword argument `encoding="latin1"` because the provided data file contains some special characters that cannot be recognized with the standard `utf-8` encoding.

```python
import pandas as pd
df = pd.read_csv("flow-data/daily-flow-series.csv",
                 header=36,
                 sep=";",
                 names=["Date", "Q (CMS)"],
                 usecols=[0, 2],
                 parse_dates=[0],
                 index_col="Date")
```

Hat alles funktioniert? Überprüfen Sie das geladene `data_series` mit `print(data_series.head())`


If your CSV file has special characters (e.g. <sup>3</sup>), you may need to use the optional keyword argument `encoding="latin1"` because some special characters cannot be recognized with the standard `utf-8` encoding.

### Zeichnen der Daten

Plotting data is not the focus of this exercise and for this reason, there is a ready-to-use function available in the `plot_discharge.py` script. Make sure that the `plot_discharge.py` is in the same directory as the above `discharge_analysis.py` *Python* script (recall how to load {ref}`sec-pypckg`). Use the `plot_discharge` function in `plot_discharge.py` as follows:

```python
from plot_discharge import plot_discharge
plot_discharge(df.index, df["Q (CMS)"], title="Daily Flows 1826 - 2016")
```

On a side note, `plot_discharge` uses the {ref}`matplotlib` library.


## Baureihe der jährlichen maximalen Entlastung
Flood event recurrence intervals result from statistics of the annual maximum discharge. Therefore, use [*pandas*' resample](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html) function to find annual maximum values. The resample function requires the definition of a `DateTimeIndex`, which we already implemented by using the `index_col` argument when we loaded the data. The first (and only required) argument for the `resample` function is the rule defining the length of the time frame to which re-sampling applies. Here, we use `"A"` for annual statistics. For using bi-annual or 5-year periods, we could use the rule `"5A"`. More rules can be found at the [*pandas* docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases).
In addition, we use the argument `kind=period`, because we are only interested in the year in which the discharge occurred. Finally, we apply `.max()` to run *maximum* statistics on the data frame. Since the re-sampled dataframe is again a dataframe, all dataframe methods can also be applied to it. That is, instead of `max()` we can as well use `min()`, `sum()`, `median()`, `mean()` and so on ([see pandas dataframe methods](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)).

```python
annual_max_df = df.resample(rule="A", kind="period").max()
```

Because we use `kind="period"`, the row indices of `annual_max_df` correspond to time periods of years. For instance, the row index `1826` corresponds to the period `1826-01-01` through `1826-12-31`. However, we need integer numbers of years rather than periods for the calculation of return periods. To get integer formats of years, we transfer the year of each period into a new column of the data frame and reset the row indices. Resetting the row indices to default integer indices through (`drop=True`) is not absolutely necessary, but serves the physical correctness of the data frame. The argument `inplace=True` replaces the indices inside `annual_max_df` (otherwise, we needed to write `annual_max_df = annual_max_df.reset_index(drop=True)`).

```python
annual_max_df["year"] = annual_max_df.index.year
annual_max_df.reset_index(inplace=True, drop=True)
print(annual_max_df.head()
```

Optional zeichnen Sie die jährlichen Maxima mit:
```python
plot_discharge(annual_max_df["year"], annual_max_df["Q (CMS)"], title="Annual Flows 1826 - 2016")
```

```{note}
Bei der Neubeprobung werden die ursprünglichen Aufzeichnungsdaten der Einleitungen nicht beibehalten.
```


## Überschreitungswahrscheinlichkeit und Wiederholungsintervalle berechnen

Die Überschreitungswahrscheinlichkeit $Pr$ eines bestimmten Ereignisses innerhalb des Beobachtungszeitraums ist:

$$
Pr(i) = (N - i + 1) / (N + 1)
$$

wo
* $N$ ist die Gesamtzahl der Beobachtungsjahre und
* $i$ ist der *Rank* der Veranstaltung.

Um die Ereignisse einzuordnen, müssen wir zuerst den maximalen jährlichen Entladedatenrahmen (`annual_max_df`) nach dem kleinsten bis größten Entladewert (und nicht nach der Zeit) sortieren:

```python
annual_max_df_sorted = annual_max_df.sort_values(by="Q (CMS)")
```

Then, we derive the number of observations $N$ (`n = annual_max_df_sorted.shape[0]`) and add a `"rank"` column, in which we simply enumerate the rows using the `range` method.

```python
n = annual_max_df_sorted.shape[0]
annual_max_df_sorted.insert(0, "rank", range(1, 1 + n)
```

Jetzt haben wir alle Zutaten, um die Wahrscheinlichkeit jedes Ereignisses mit den oben gezeigten $Pr(rank=i)$-formula.<br> zu berechnen.

```python
annual_max_df_sorted["pr"] = (n - annual_max_df_sorted["rank"] + 1) / (n + 1)
```

Das Rezidivintervall (hier: Rückgabezeit in Jahren) ist die Umkehrung der Überschreitungswahrscheinlichkeit und wir können es dem Datenrahmen hinzufügen mit:

```python
annual_max_df_sorted["return-period"] = 1 / annual_max_df_sorted["pr"]
```

Überprüfen Sie die resultierende höchste Entladung und ihre Rückgabefrist:

```python
print(annual_max_df_sorted.tail()
```

Plot the resulting probability and return curves with the plot functions provided in the `plot_result.py` *Python* script:

```python
plot_q_freq(annual_max_df_sorted)
plot_q_return_period(annual_max_df_sorted)
```

```{admonition} Variable name consistency
:class: attention
The plot functions only work correctly if the probability column is named $Pr$, the return period column is named $return-period$, and the discharge column is named $Q (CMS)$ (otherwise, consider renaming the data frame column header names or modifying the plot functions).
```


## Außerhalb der Box

Das hier gezeigte Verfahren ist lediglich eine Interpolation. Für die Extrapolation von Rückkehrperioden über die Länge des Beobachtungszeitraums hinaus (z. B. für Extremereignisse wie eine 1000-jährige Flut) ist ein Vorhersagemodell erforderlich (z. B. Gumbel-Extrapolation).

Schließlich gibt es bereits Software, die Rückgabezeiten berechnet, frei verfügbar im U.S. Army Corps of Engineers Hydrologic Engineering Center (*HEC*) {cite:p}`us_army_corps_of_engineeers_hydrologic_2016`: [HEC-SPP](https://www.hec.usace.army.mil/software/hec-ssp/)]. HEC-SPP ermöglicht die Berechnung von Flow-Event-Frequenzen und Rückkehrperioden nach US-Standards. Wenn sie also nicht in oder für die vereinigten staaten arbeiten, möchten sie vielleicht immer noch ihren code bereit haben. Darüber hinaus erfordert *HEC-SPP* eine Vorverarbeitung der Entladedaten (d.h. es funktioniert nur mit jährlichen Maxima).


```{admonition} Homework
Verwenden Sie die Formeln in unserem [Gumble-template workbook](https://github.com/Ecohydraulics/Exercise-FloodReturn/raw/main/flow-data/flood-statistics-gumble-template.xlsx)], um die Gumbel-Verteilung für die Extrapolation einer 200-, 500- und 1000-jährigen Flut zu implementieren. Interpolationen entladen 2, 5, 10, 20 und 50-jährige Flussereignisse. *Verwenden Sie Schleifen und Funktionen!*
```
