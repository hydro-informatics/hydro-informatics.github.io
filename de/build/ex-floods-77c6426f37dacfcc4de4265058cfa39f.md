---
description: Python-Übung für Flutfrequenzanalyse und Rücklaufzeitberechnung mit Pandas, die Überschreitungswahrscheinlichkeit und Wiederauftretensintervalle für hydrologische Entladungsdaten abdeckt.
---

(ex-floods)=
# Überflutungszeiten

```{admonition} Goals
Benutzerdefinierte Module und Funktionen in einem Skript laden. Open comma-Typ begrenzte Dateien und manipulieren Dateien mit {ref}`pandas`.
```

```{admonition} Requirements
:class: attention
Python Bibliotheken: {ref}`pandas` und *matplotlib*. Verstehen Sie die Datenverarbeitung mit {ref}`pandas`.
```

Bereiten Sie sich durch Klonen des Übungs-Repository:

```
git clone https://github.com/Ecohydraulics/Exercise-FloodReturn.git
```

```{figure} ../img/hw-aibling.jpg
:alt: floods Mangfall Bad Aibling Hochwasser
:name: flood-image

Flut am Mangfall River in Bayern (Quelle: KSS 2020).
```

## Terminologie
Die Flutfrequenzanalyse verwendet eine Reihe von Entladungsdaten (z.B. von einer Messstation) und wertet die Auftretenswahrscheinlichkeit einer bestimmten Entladung aus. So definiert die Ereigniswahrscheinlichkeit die Häufigkeit einer Entladung, die aus zwei Gründen wichtig ist:

1. ** Sicherheit**: Viele Rechtsrahmen verwenden ein **-Recurrence-Intervall** (d.h. eine Retourendauer oder Häufigkeit in Einheiten von Jahren), um Sicherheitsniveaus zu definieren, die Gebäude und Infrastruktur erfüllen müssen.
1. **Ecohydraulik*: Insbesondere in trockenen Gebieten ist es wichtig zu wissen, wie lange bestimmte Entladungen unter bestimmten Ebenen liegen, wo viele aquatische Lebensräume nicht tief genug, zu heiß oder vom Hauptkanal getrennt sein können. Daher wollen wir die **-Exceedance-Wahrscheinlichkeit** einer gegebenen Entladung kennen.

Die Beziehung zwischen der Überschreitungswahrscheinlichkeit und dem Wiederauftretensintervall ergibt sich aus der Definition beider Begriffe:
* Die **-Exceedance Wahrscheinlichkeit** ist die Wahrscheinlichkeit eines Ereignisses einer bestimmten Größe (in m$^3$/s oder CFS) oder höher.
* Das **-Recurrence-Intervall** ist die Inverse der Überschreitungswahrscheinlichkeit und drückt die durchschnittliche Rücklaufzeit eines Ereignisses bestimmter Größe in Zeiteinheiten aus.

Das Berechnungskonzept der Rückgabeperiode macht zwei elementare Annahmen. Zunächst wird angenommen, dass die einzelnen Strömungsereignisse einen stationären Peak aufweisen. Zweitens wird die statistische Unabhängigkeit einzelner Ereignisse angenommen. Die Annahme der statistischen Unabhängigkeit bedeutet, dass in diesem Jahr eine 100-jährige Flut mit der gleichen Wahrscheinlichkeit wie im nächsten Jahr auftritt, unabhängig davon, ob in diesem Jahr tatsächlich eine 100-jährige Flut aufgetreten ist. So beträgt die Wahrscheinlichkeit einer 100-jährigen Überschwemmung für jedes Jahr 1/100 (oder 1/50 für eine 50-jährige Überschwemmung usw.).

## Die Wahrscheinlichkeit einer 100-jährigen Überschwemmung in 100 Jahren beträgt 63 %

Als Ingenieure wollen wir oft wissen, wie wahrscheinlich es ist, dass eine 100-jährige Flut innerhalb der nächsten 2, 5, 10, ... oder 100 Jahre auftreten wird (d.h. was sind die wahrscheinlichen Kosten für Flutschäden im Zusammenhang mit einer 100-jährigen Flut?). Die Antwort auf diese Frage ist *"die entgegengesetzte Wahrscheinlichkeit, dass in den nächsten 2, 5 oder 10 Jahren keine 100-jährige Flut auftritt"*. Mathematisch bedeutet das die jährliche Eintrittswahrscheinlichkeit $Pr$ einer Veranstaltung mit einem Wiederauftretensintervall $T=100$Jahre über einen Beobachtungszeitraum von $\Delta t \in [2, 5, 10, 100]$Jahre:

$Pr(T=100, \Delta t=2, 5, 10, 100) = (1 - (1-1/T)^{\Delta t})$

{numref}`Table %s <tab-pr-floods>` zeigt Lösungen zur Wahrscheinlichkeit $Pr(T, \Delta t)$Funktion für Beobachtungsperioden $\Delta t$ von 2, 5, 10 und 100 Jahren sowie Rekursionsintervalle $T$ von 10, 50 und 100 Jahren.

```{list-table} Solutions to the probability function $Pr(T, \Delta t)$ for selected observation periods $\Delta t$.
:header-rows: 1
:name: tab-pr-floods

* - $Pr(T, \Delta t)$
  - $\Delta t$ = 2
  - $\Delta t$ = 5
  - $\Delta t$ = 10
  - $\Delta t$ = 100

* - $T$ = 10
  - 19.00%
  - 40,95%
  - 65.13%
  - 100.00%

* - $T$ = 50
  - 3,96%
  - 9.61%
  - 18.29%
  - 86.74 %

* - $T$ = 100
  - 1,9 %
  - 4,90%
  - 9.56%
  - 63,40%
```

Besuchen Sie die [*USGS* Wasserwissenschaftsschule](https://www.usgs.gov/special-topic/water-science-school/science/100-year-flood?qt-science_center_objects=0#qt-science_center_objects), um mehr über Flut (und Dürre)-Rekurs zu erfahren.

## Löschen von Daten

### Datenquellen deaktivieren

Durchflussdaten können von Messstationen abgerufen werden. In Deutschland bietet das ["Gewässerkundliches Jahrbuch"](http://www.dgj.de/) eine Übersicht über statistische Daten von gauging Stationen. Beachten Sie, dass viele Messstellen, wie auch in vielen anderen Ländern, von staatlichen Behörden verwaltet werden und nur ein kleiner Datenanteil von Bundeseinrichtungen zur Verfügung steht. Zum Beispiel sind Lehrdaten für Baden-Württemberg am Staatlichen Institut für Umwelt, Umwelt und Naturschutz (LUBW) verfügbar [geo portal](https://hvz.lubw.baden-wuerttemberg.de/). Die folgende Liste enthält mehr Quellen für die Datenerhebung auf der ganzen Welt.

* Die [Bundesanstalt für Gewässerkunde *BfG*](https://www.bafg.de) betreibt das [Global Runoff Data Centre *GRDC*](https://www.bafg.de/GRDC/EN/Home/homepage_node.html) für die Weltorganisation für Meteorologie *WMO* zur Bereitstellung von Flussabflussdaten weltweit. Die Download-Plattform von *GRDC* ist in Form einer [interaktiven web-GIS](https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser#dataDownload/Home). Um die Daten zu erhalten, gehen Sie an ihre [download interface](https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser#dataDownload/Stations), wählen Sie die gewünschte Station, wechseln Sie auf *Table*-Ansicht (dritte Zeile oben links im Fenster), überprüfen Sie die Station, klicken Sie **download*** und füllen Sie das Formular aus, um die Anfrage zu senden. Sie erhalten eine E-Mail mit einem Download-Link für die gewünschten Daten (warten Sie ein paar Minuten, bevor Sie auf den Link klicken - die Vorbereitung kann mehr Zeit als die E-Mail nehmen).
* Flussdatensätze aus alpinen und mittleren Flüssen werden vom Bundesamt für Umwelt [hydrologische Datenplattform](https://www.hydrodaten.admin.ch/) (für langfristige Beobachtungen muss auch hier ein Formular ausgefüllt werden).
* In den Vereinigten Staaten liefert die National Oceanic and Atmospheric Administration *NOAA* Entladungsdaten aus der Vergangenheit und Prognosen für Wassersheds in Nordamerika. Zum Beispiel bietet das [California Nevada River Forecast Center](https://www.cnrfc.noaa.gov/) Flussprognosen für die südwestlichen Vereinigten Staaten, und historische Daten können vom [California Data Exchange Center *CDEC*](http://cdec.water.ca.gov/).
* Eine allgemeine *US*-gestützte Schnittstelle zum Laden von Flussdaten und Statistiken enthält die [`hydrofunctions` *Python* library](https://hydrofunctions.readthedocs.io/) der United States Geological Survey *USGS*. Diese Bibliothek ermöglicht es, Messdaten und Statistiken auf Basis einer Stream-ID direkt zu erhalten. Zum Beispiel `output = hydrofunctions.peaks("01541200")`
   * Um `hydrofunctions` in einer {ref}`conda <conda-env>`-Umgebung zu installieren, geben Sie bitte `conda install -c conda-forge hydrofunctions` in {ref}`Anaconda Prompt <install-pckg>` ein.
   * Beispielnutzung:

```
import hydrofunctions as hf
hf.draw_map()` # only runs in JupyterLab
```

## Daten laden mit *pandas*
Erstellen Sie eine neue *Python*-Datei (z.B. `discharge_analysis.py`) und importieren Sie *pandas* als `pd` zu Beginn. Lesen Sie die bereitgestellte Datenreihendatei `"daily-flow-series.csv"` mit `pd.read_csv`.
Der Header (Spaltennamen) befindet sich in Zeile 36, aber wir verwenden nicht die Spaltennamen aus der *csv*-Datei und überschreiben sie mit dem `names`Argument (`"Date"` und `"Q (CMS)"` (für Cubic Meters per Second)). Alternativ könnten wir das Argument `skiprows` verwenden, um anzuzeigen, wo der Dateninhalt in der Datei beginnt.
Mit `sep=";"` geben wir an, dass Spalten durch ein Semikolon getrennt werden. Das `usecols=[0, 2]`-Argument gibt an, dass wir nur die Spalten 0 (Datum) und 2 (Entladung) lesen wollen, da der Informationsinhalt der Spalte 1 (Zeit) für die tägliche Entladung nicht relevant ist. Das `parse_dates=[0]`Argument lässt *pandas* wissen, dass Spalte 0 datenformatierte Werte enthält. Alternativ können wir ein `dtype={"Date": ... }` Wörterbuch verwenden, um die Datenformate der Spalten anzugeben. Die Nutzung von `dtype` erfordert jedoch den Import von `datetime` und induziert unnötige Komplexität. Darüber hinaus definiert das `index_col` Argument die Spaltenindizes, die ein Datumsformat für die späteren Analysen haben müssen. Darüber hinaus verwenden Sie das optionale Keyword-Argument `encoding="latin1"`, da die bereitgestellte Datendatei einige Sonderzeichen enthält, die mit der Standard-`utf-8` encoding nicht erkannt werden können.

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

Hat alles funktioniert? Überprüfen Sie die geladenen `data_series` mit `print(data_series.head())`


Wenn Ihre CSV-Datei besondere Zeichen hat (z.B. <sup>3</sup>) müssen Sie das optionale Keyword-Argument `encoding="latin1"` verwenden, da einige Sonderzeichen nicht mit der Standard `utf-8` encoding erkannt werden können.

### Geben Sie die Daten

Die Plotting-Daten stehen nicht im Mittelpunkt dieser Übung, weshalb im Skript `plot_discharge.py` eine gebrauchsfertige Funktion zur Verfügung steht. Stellen Sie sicher, dass die `plot_discharge.py` im gleichen Verzeichnis wie das oben genannte `discharge_analysis.py` *Python*-Skript steht (wie man {ref}`sec-pypckg` lädt). Verwenden Sie die `plot_discharge`-Funktion in `plot_discharge.py` wie folgt:

```python
from plot_discharge import plot_discharge
plot_discharge(df.index, df["Q (CMS)"], title="Daily Flows 1826 - 2016")
```

`plot_discharge` verwendet die Bibliothek {ref}`matplotlib`.


## Baureihe der jährlichen maximalen Entladung
Die Wiederholungsintervalle der Flutereignisse ergeben sich aus Statistiken der jährlichen Höchstentladung. Verwenden Sie daher die Funktion resample](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html), um jährliche Höchstwerte zu finden. Die Resample-Funktion erfordert die Definition einer `DateTimeIndex`, die wir bereits mit dem `index_col` Argument implementiert haben, wenn wir die Daten geladen haben. Das erste (und nur erforderliche) Argument für die `resample`-Funktion ist die Regel, die die Länge des Zeitrahmens definiert, auf den eine erneute Probenahme Anwendung findet. Hier verwenden wir `"A"` für Jahresstatistiken. Für die Nutzung von zwei- oder 5-Jahres-Zeiträumen können wir die Regel `"5A"` verwenden. Weitere Regeln finden Sie unter der [*pandas* docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases).
Darüber hinaus verwenden wir das Argument `kind=period`, denn wir sind nur an dem Jahr interessiert, in dem die Entlastung stattgefunden hat. Schließlich wenden wir `.max()` an, um *maximum* Statistiken über den Datenrahmen auszuführen. Da der wieder abgetastete Datenrahmen wiederum ein Datenrahmen ist, können auch alle Dataframe-Methoden darauf angewendet werden. Das heißt, statt `max()` können wir auch `min()`, `sum()`, `median()`, `mean()` und so weiter ([siehe pandas dataframe Methoden](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html)) verwenden.

```python
annual_max_df = df.resample(rule="A", kind="period").max()
```

Da wir `kind="period"` verwenden, entsprechen die Zeilenindizes von `annual_max_df` den Zeiträumen von Jahren. So entspricht der Zeilenindex `1826` dem Zeitraum `1826-01-01` durch`1826-12-31`. Wir brauchen jedoch ganzzahlige Zahlen von Jahren und nicht Perioden für die Berechnung von Rückgabeperioden. Um ganzzahlige Formate von Jahren zu erhalten, übertragen wir das Jahr jeder Periode in eine neue Spalte des Datenrahmens und setzen die Zeilenindizes zurück. Das Zurücksetzen der Zeilenindizes auf Standard-Indizes durch (`drop=True`) ist nicht unbedingt erforderlich, sondern dient der physikalischen Korrektheit des Datenrahmens. Das Argument `inplace=True` ersetzt die Indizes innerhalb `annual_max_df` (anders müssen wir `annual_max_df = annual_max_df.reset_index(drop=True)` schreiben).

```python
annual_max_df["year"] = annual_max_df.index.year
annual_max_df.reset_index(inplace=True, drop=True)
print(annual_max_df.head()
```

Optional die jährlichen Maxima mit:
```python
plot_discharge(annual_max_df["year"], annual_max_df["Q (CMS)"], title="Annual Flows 1826 - 2016")
```

```{note}
Das Reampling bewahrt nicht die ursprünglichen Aufnahmetermine der Entladungen.
```


## Berechnen von Exceedance Probability und Recurrence Intervals

Die Überschreitungswahrscheinlichkeit $Pr$ eines bestimmten Ereignisses innerhalb des Beobachtungszeitraums ist:

$$
Pr(i) = (N - i + 1) / (N + 1)
$$

wenn
* $N$ ist die Gesamtzahl der Beobachtungsjahre und
* $i$ ist der *rank* der Veranstaltung.

Um die Ereignisse zu ordnen, müssen wir zunächst den maximalen jährlichen Entladungsdatenrahmen (`annual_max_df`) um den kleinsten bis größten Entladewert (anstatt rechtzeitig) sortieren:

```python
annual_max_df_sorted = annual_max_df.sort_values(by="Q (CMS)")
```

Dann leiten wir die Anzahl der Beobachtungen $N$ (`n = annual_max_df_sorted.shape[0]`) ab und fügen eine `"rank"` Spalte hinzu, in der wir einfach die Zeilen mit der `range`-Methode auszählen.

```python
n = annual_max_df_sorted.shape[0]
annual_max_df_sorted.insert(0, "rank", range(1, 1 + n)
```

Jetzt haben wir alle Zutaten, um die Wahrscheinlichkeit jeder Veranstaltung zu berechnen, mit der oben angegebenen $Pr(rank=i)$-formula.<br>

```python
annual_max_df_sorted["pr"] = (n - annual_max_df_sorted["rank"] + 1) / (n + 1)
```

Recall, das Wiederholungsintervall (hier: Rückkehrzeit in Jahren) ist das Invers der Überschreitungswahrscheinlichkeit und wir können es in den Datenrahmen mit:

```python
annual_max_df_sorted["return-period"] = 1 / annual_max_df_sorted["pr"]
```

Prüfen Sie die resultierende höchste Entladung und ihre Rückgabezeit:

```python
print(annual_max_df_sorted.tail()
```

Geben Sie die resultierende Wahrscheinlichkeit und Rückgabekurven mit den im Skript `plot_result.py` *Python* bereitgestellten Plotfunktionen aus:

```python
plot_q_freq(annual_max_df_sorted)
plot_q_return_period(annual_max_df_sorted)
```

```{admonition} Variable name consistency
:class: attention
Die Handlungsfunktionen funktionieren nur richtig, wenn die Wahrscheinlichkeitsspalte $Pr$ benannt ist, die Rückgabeperiodenspalte $return-period$ benannt ist und die Entladungsspalte $Q (CMS)$ benannt ist (anders erwägen Sie die Umbenennung der Datenrahmenspalten-Headernamen oder die Änderung der Plotfunktionen).
```


## Außerhalb der Box

Das hier dargestellte Verfahren ist nur eine Interpolation. Für die Extrapolation von Rückführungszeiten über die Länge des Beobachtungszeitraums (z.B. für Extremereignisse wie eine 1000-jährige Flut) ist ein Prädiktionsmodell erforderlich (z.B. Gumbel verteilte Extrapolation).

Schließlich gibt es bereits Software, die Rückgabefristen berechnet, frei verfügbar im U.S. Army Corps of Engineers Hydrologic Engineering Center (*HEC*) {cite:p}`us_army_corps_of_engineeers_hydrologic_2016`: [HEC-SPP](https://www.hec.usace.army.mil/software/hec-ssp/). HEC-SPP ermöglicht die Berechnung von Flussereignisfrequenzen und Rücklaufperioden nach US-Standards. Wenn Sie also nicht in oder für die Vereinigten Staaten arbeiten, können Sie immer noch Ihren Code bereit haben. Darüber hinaus erfordert *HEC-SPP* eine Vorverarbeitung von Entladungsdaten (d.h. es funktioniert nur mit jährlichen Maxima).


```{admonition} Homework
Verwenden Sie die Formeln in unserem [Gumble-template workbook](https://github.com/Ecohydraulics/Exercise-FloodReturn/raw/main/flow-data/flood-statistics-gumble-template.xlsx), um die Gumbel-Distribution zur Extrapolation einer 200-, 500- und 1000-jährigen Flut umzusetzen. Interpolationsentladungen von 2, 5, 10, 20 und 50-Jahresdurchflussereignissen. *Verwenden Sie Schleifen und Funktionen!*
```
