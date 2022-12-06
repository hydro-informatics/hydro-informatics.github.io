(ex-floods)=
# Flood Return Periods

```{admonition} Goals
Load custom modules and functions in a script. Open comma-type delimited files and manipulate files with {ref}`pandas`.
```

```{admonition} Requirements
:class: attention
Python libraries: {ref}`pandas` and *matplotlib*. Understand data handling with {ref}`pandas`.
```

Get ready by cloning the exercise repository:

```
git clone https://github.com/Ecohydraulics/Exercise-FloodReturn.git
```

```{figure} ../img/hw-aibling.jpg
:alt: floods Mangfall Bad Aibling Hochwasser
:name: flood-image

Flood at the Mangfall River in Bavaria (source: KSS 2020).
```

## Terminology
Flood frequency analysis uses a series of discharge data (e.g., from a gauging station) and evaluates the occurrence probability of a particular discharge. Thus, the occurrence probability defines the frequency of a discharge, which is important for two reasons:

1. **Flood safety**: Many legal frames use a **recurrence interval** (i.e., a return period or frequency in units of years) to define safety levels that buildings and infrastructure must meet.
1. **Ecohydraulics**: In arid areas, in particular, it is important to know how long certain discharges are below certain levels, where many aquatic habitats may not be deep enough, too hot, or disconnected from the main channel. Therefore, we want to know the **exceedance probability** of a given discharge.

The relationship between the exceedance probability and the recurrence interval results from the definition of both terms:
* The **exceedance probability** is the likelihood of an event of a certain magnitude (in m$^3$/s or CFS) or higher.
* The **recurrence interval** is the inverse of the exceedance probability and expresses the average return period of an event of a certain magnitude in units of time.

The calculation concept of the return period makes two elementary assumptions. First, it is assumed that the individual flow events have a stationary peak. Second, statistical independence of individual events is assumed. The assumption of statistical independence means that this year a 100-year flood occurs with the same probability as next year, regardless of whether or not a 100-year flood actually occurred this year. Thus, for any given year, the probability of a 100-year flood occurring is 1/100 (or 1/50 for a 50-year flood and so on).

## The Probability of a 100-year Flood Occurring in 100 Years is 63%

As engineers we often want to know how likely it is that a 100-year flood will occur within the next 2, 5, 10, ... or 100 years (i.e., what are the likely costs of flood damage associated with a 100-year flood?). The answer to that question is *"the opposite likelihood of no 100-year flood occurring in the next 2, 5, or 10 years"*. Mathematically that means the annual occurrence probability $Pr$ of an event with a recurrence interval $T=100$ years over an observation period of $\Delta t \in [2, 5, 10, 100]$ years is:

$Pr(T=100, \Delta t=2, 5, 10, 100) = (1 - (1-1/T)^{\Delta t})$

{numref}`Table %s <tab-pr-floods>` shows solutions to the probability $Pr(T, \Delta t)$ function for observation periods $\Delta t$ of 2, 5, 10, and 100 years, as well as recurrence intervals $T$ of 10, 50, and 100 years.

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
  - 40.95%
  - 65.13%
  - 100.00%

* - $T$ = 50
  - 3.96%
  - 9.61%
  - 18.29%
  - 86.74%

* - $T$ = 100
  - 1.99%
  - 4.90%
  - 9.56%
  - 63.40%
```

Visit the [*USGS* water science school](https://www.usgs.gov/special-topic/water-science-school/science/100-year-flood?qt-science_center_objects=0#qt-science_center_objects) to learn more about flood (and drought) recurrence interval.

## Get Discharge Data

### Discharge Data Sources

Flow data can be retrieved from gauging stations. In Germany, the ["Gewässerkundliches Jahrbuch"](http://www.dgj.de/) provides a compound overview of statistic data from gauging stations. Note that many gauging stations are, as in many other countries, too, managed by state authorities and only a small share of data is available from federal institutions. For example, gauge data for Baden-Württemberg are available at the State Institute for the Environment, Survey and Nature Conservation's (LUBW) [geo portal](https://hvz.lubw.baden-wuerttemberg.de/). The following list provides more sources for discharge data around the globe.

* The [Bundesanstalt für Gewässerkunde *BfG*](https://www.bafg.de) runs the [Global Runoff Data Centre *GRDC*](https://www.bafg.de/GRDC/EN/Home/homepage_node.html) for the World Meteorological Organization *WMO* to provide river discharge data worldwide. The *GRDC*'s download platform is available in the form of an [interactive web-GIS](https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser#dataDownload/Home). To get the data, go to their [download interface](https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser#dataDownload/Stations), select the desired station, switch to *Table* view (third row in the top left of the window), check the station, click **download**, and fill the form to send the request. You will receive an email with a download link for the requested data (wait a couple of minutes before clicking on the link - the preparation may take more time than the email).
* Flow datasets from alpine and midland rivers are provided by the Swiss Federal Office for the Environment's [hydrological data platform](https://www.hydrodaten.admin.ch/) (for long-term observations, a form has to be filled out here, too).
* In the United States, the National Oceanic and Atmospheric Administration *NOAA* provides discharge data from the past and forecasts for watersheds in North America. For example, the [California Nevada River Forecast Center](https://www.cnrfc.noaa.gov/) provides flow forecasts for the South-Western United States, and historic data can be accessed from the [California Data Exchange Center *CDEC*](http://cdec.water.ca.gov/).
* A general *US*-borne interface for loading flow data and statistics comes with the [`hydrofunctions` *Python* library](https://hydrofunctions.readthedocs.io/) provided by the United States Geological Survey *USGS*. This library enables to directly get gauge data and statistics based on a stream gauge ID. For example `output = hydrofunctions.peaks("01541200")`
   * To install `hydrofunctions` in a {ref}`conda <conda-env>` environment, type `conda install -c conda-forge hydrofunctions` in {ref}`Anaconda Prompt <install-pckg>`.
   * Example usage:

```
import hydrofunctions as hf
hf.draw_map()` # only runs in JupyterLab
```

## Load Data with *pandas*
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

Did everything work? Verify the loaded `data_series` with `print(data_series.head())`


If your CSV file has special characters (e.g. <sup>3</sup>), you may need to use the optional keyword argument `encoding="latin1"` because some special characters cannot be recognized with the standard `utf-8` encoding.

### Plot the Data

Plotting data is not the focus of this exercise and for this reason, there is a ready-to-use function available in the `plot_discharge.py` script. Make sure that the `plot_discharge.py` is in the same directory as the above `discharge_analysis.py` *Python* script (recall how to load {ref}`sec-pypckg`). Use the `plot_discharge` function in `plot_discharge.py` as follows:

```python
from plot_discharge import plot_discharge
plot_discharge(df.index, df["Q (CMS)"], title="Daily Flows 1826 - 2016")
```

On a side note, `plot_discharge` uses the {ref}`matplotlib` library.


## Construct Series of Annual Maximum Discharge
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

Optionally, plot the annual maxima with:
```python
plot_discharge(annual_max_df["year"], annual_max_df["Q (CMS)"], title="Annual Flows 1826 - 2016")
```

```{note}
Resampling does not preserve the original recording dates of discharges.
```


## Calculate Exceedance Probability and Recurrence Intervals

The exceedance probability $Pr$ of a particular event within the observation period is:

$$
Pr(i) = (N - i + 1) / (N + 1)
$$

where
* $N$ is the total number of observation years, and
* $i$ is the *rank* of the event.

To rank the events, we first need to sort the maximum annual discharge data frame (`annual_max_df`) by the smallest to largest discharge value (rather than in time):

```python
annual_max_df_sorted = annual_max_df.sort_values(by="Q (CMS)")
```

Then, we derive the number of observations $N$ (`n = annual_max_df_sorted.shape[0]`) and add a `"rank"` column, in which we simply enumerate the rows using the `range` method.

```python
n = annual_max_df_sorted.shape[0]
annual_max_df_sorted.insert(0, "rank", range(1, 1 + n)
```

Now, we have all ingredients to calculate the probability of every event with the above shown $Pr(rank=i)$-formula.<br>

```python
annual_max_df_sorted["pr"] = (n - annual_max_df_sorted["rank"] + 1) / (n + 1)
```

Recall, the recurrence interval (here: return period in years) is the inverse of the exceedance probability and we can add it to the data frame with:

```python
annual_max_df_sorted["return-period"] = 1 / annual_max_df_sorted["pr"]
```

Check the resulting highest discharge and its return period:

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


## Outside the Box

The here shown method is only an interpolation. For extrapolating return periods beyond the length of the observation period (e.g., for extreme events such as a 1000-year flood), a prediction model is necessary (e.g., Gumbel distributed-extrapolation).

After all, there is already software that calculates return periods, freely available at the U.S. Army Corps of Engineers Hydrologic Engineering Center (*HEC*) {cite:p}`us_army_corps_of_engineeers_hydrologic_2016`: [HEC-SPP](https://www.hec.usace.army.mil/software/hec-ssp/). HEC-SPP enables the calculation of flow event frequencies and return periods according to US standards. So if you are not working in or for the United States, you still may want to have your code ready. Moreover, *HEC-SPP* requires pre-processing of discharge data (i.e., it only works with annual maxima).


```{admonition} Homework
Use the formulae in the our [Gumble-template workbook](https://github.com/Ecohydraulics/Exercise-FloodReturn/raw/main/flow-data/flood-statistics-gumble-template.xlsx) to implement the Gumbel distribution for extrapolating a 200, 500, and 1000-years flood. Interpolations discharges of 2, 5, 10, 20, and 50-year flow events. *Use loops and functions!*
```
