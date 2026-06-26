---
description: TELEMAC Modelloptimierungsleitfaden für rechnergestützte Geschwindigkeitsverbesserungen, physikalische Korrektheitskalibrierung, Massenerhaltung und maschinelle lerngestützte Modellveredelung.
---

(telemac-opti)=
# Optimierung

Eine numerische Modellkalibrierung sollte ein rechnerisch funktionsfähiges und physikalisch mindestens ein vernünftig genaues Modell liefern. Die Modellkalibrierung wurde bereits im {ref}`results analysis section <tm2d-post-export>` des stetigen Telemac2d-Tutorials erfasst. Dieses Kapitel bietet zunächst mehr Tipps, um die körperliche Korrektheit eines Modells zu erhöhen, insbesondere in Bezug auf die Erhaltung der Masse, die manchmal in Telemac herausfordern kann. Darüber hinaus werden fortschrittliche Kalibriermethoden vorgestellt, die überwachtes maschinelles Lernen zur Verbesserung der physikalischen Modellgenauigkeit verwenden.

```{admonition} Goals and requirements
Dieses Tutorial erklärt, wie ein Telemac-Modell durch die Verbesserung seiner Rechenstabilität und der physikalischen Korrektheit verfeinert werden kann. So ist es nach der Einrichtung eines Telemac-Modells relevant, wie es für einen einfachen Fall in der {ref}`steady 2d chapter <telemac2d-steady>` erläutert wird.

```


## Berechnungszeit

Einige der Keywords in der TELEMAC-Lenkung (`*.cas`)-Datei beeinflussen die Rechengeschwindigkeit.

* Nutzen Sie die {ref}`ACCURACY and MAXIMUM ITERATION <tm2d-accuracy>` Keywords, um schnellere Konvergenz zu erzielen.
* Deaktivieren Sie `TIDAL FLATS`, obwohl das Deaktivieren {ref}`tidal flats <tm2d-tidal>` nicht empfohlen werden kann, physikalisch sinnvolle und stabile Modelle zu liefern.
* Bei der Nutzung des GMRES-Resolvers (`SOLVER : 7`) kann die Variation der {ref}`solver options <tm2d-solver-pars>` dazu beitragen, die Gesamtberechnungszeit zu reduzieren.
* Achten Sie darauf, den Standard `MATRIX STORAGE : 3`keyword zu verwenden.
* Verwenden Sie eine frühere Simulation (z.B. mit einem gröberen Mesh), um das Modell mit den `COMPUTATION CONTINUED : YES` und `PREVIOUS COMPUTATION FILE : *.slf` Keywords einzuleiten (siehe Abschnitt 4.1.3 in der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf)).

Darüber hinaus bietet Telemac2d eine Möglichkeit, eine Simulation (Schritt) zu stoppen, wenn Flussmittel stabilisieren. Um diese Funktion zu aktivieren, fügen Sie den folgenden Block in der Steuerungsdatei (`*.cas`) hinzu:

```
/ steady state stop criteria in steering.cas
STOP IF A STEADY STATE IS REACHED : YES / default is NO
STOP CRITERIA : 1.E-3;1.E-3;1.E-3 / use list of three values - defaults are 1.E-4
```

Die Stop-Kriterien sind jedoch für nicht stationäre Ströme nicht funktionsfähig (z.B. {cite:t}`von_karman_mechanische_1930`wirbel Straße stromabwärts von Brückenpiern). Lesen Sie mehr über die Konvergenzkriterien in der [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) (Abschnitt 5.1).

```{admonition} More recommendations are in the user manual
:class: tip

Die [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) bietet weitere Empfehlungen für Rechenzeit, Stabilität und Modelloptimierung, einschließlich des Netzes, in Abschnitt 16.
```

## Stabilität und körperliche Korrektheit


### Genauigkeit

Wenn die Genauigkeits-Keywords unangemessen definiert sind, kann TELEMAC die Simulation nicht beenden können. In diesem Fall stellen Sie sicher, die Genauigkeits-Keywords zu kommentieren und lassen Sie TELEMAC seine Standardwerte verwenden:

```fortran
/ SOLVER ACCURACY : 1.E-4
/ ACCURACY FOR DIFFUSION OF TRACERS : 1.E-4
/ ACCURACY OF K : 1.E-6
/ ACCURACY OF EPSILON : 1.E-6
/ ACCURACY OF SPALART-ALLMARAS : 1.E-6
```

### Variable Zeitstufen und CFL-Zahl Zustand

Unstabile Simulationen können auftreten, wenn die Bedingung {term}`CFL` unzureichend erfüllt ist. Um sicherzustellen, dass die {term}`CFL`-Bedingung respektiert wird, aktivieren Sie die variable Zeitschrittberechnung und verwenden Sie das **DESIRED COURANT NUMBER** Keyword (Standardwert `1`), z.B.:

```fortran
TIME STEP : 5
VARIABLE TIME-STEP : YES
DURATION : 5000
DESIRED COURANT NUMBER : 0.9
```

Beachten Sie, dass der **TIME STEP** noch benötigt wird, da der **GRAPHISCHE PRINTOUT PERIOD** ein Vielfaches des definierten **TIME STEP** ist.

```{admonition} Use the DURATION keyword
Eine variable Zeitschrittberechnung kann ewig laufen. Die Zuordnung des **DURATION** Schlüsselworts vermeidet solche ewigen Abläufe.
```

### Implizit
Um die Modellstabilität zu erhöhen, ändern Sie die folgenden Variablen oder stellen Sie sicher, dass sich die Variablen in der *CAS*-Datei befinden:

* `IMPLICITATION FOR DEPTH` ist zwischen `0.5` und `0.6`.
* `IMPLICITATION FOR VELOCITIES` ist zwischen `0.5` und `0.6`.
* `IMPLICITATION FOR DIFFUSION` sollte `1.` oder kleiner sein.

### Oberflächenschwingungen (Wiggles)
Wenn an der Wasseroberfläche physikalisch nicht-meaningful Gradienten oder Oszillationen auftreten oder die Bathymetrie steile Steigungen aufweist, können folgende Keyword-Einstellungen helfen:

* `FREE SURFACE GRADIENT` - Standardmäßig ist `1.0`, aber es kann auf `0.1` reduziert werden, um Stabilität zu erreichen (jeweils beginnen Sie mit inkremental ab, wie ein Wert von `0.9`).
* `DISCRETIZATIONS IN SPACE : 12;11` - verwendet quasi-bubble Raumdiskretisierung mit 4-node Dreiecke für Geschwindigkeit.

### Restmasse Fehler
Um Restmassenfehler zu reduzieren, verwenden Sie in der Lenkdatei:

```fortran
CONTINUITY CORRECTION : YES
```

### Diversity

Um Divergenzprobleme zu begrenzen, verwenden Sie die Schlüsselwörter `CONTROL OF LIMITS` und `LIMIT VALUES`. Das `LIMIT VALUES`-Keyword ist eine Liste von 8 Integern für minimale und maximale Werte für H, U, V und T (Tracers). Die Implementierung in der Lenkdatei sieht so aus:

```fortran
CONTROL OF LIMITS : YES / default is NO
LIMIT VALUES : -1000;9000;-1000;1000;-1000;1000;-1000;1000 / default mins and max for H, U, V, tracer
```

### Tidal Flats

Das Benetzen und Trocknen von Gitterzellen, beispielsweise bei einer Simulation von Staus oder Fluthydrographen, kann zur Modellinstabilität führen. Während der Abschnitt {ref}`tm2d-tidal` im Telemac2d-Live-Modelling-Tutorial physikalisch und rechnerisch aussagekräftige Keyword-Optionskombinationen vorschlägt, empfiehlt Abschnitt 16.5 im [Telemac2d manual](https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/blob/v9.0.0/documentation/telemac2d/user/telemac2d_user_9.0.pdf) die Verwendung der folgenden Einstellungen in der Lenkdatei als konservative Entscheidungen aus dem BAW-Wesel-Beispiel.

```fortran
VELOCITY PROFILES : 4;0
TURBULENCE MODEL : 1
VELOCITY DIFFUSIVITY : 2.
TIDAL FLATS : YES
OPTION FOR THE TREATMENT OF TIDAL FLATS : 1
TREATMENT OF NEGATIVE DEPTHS : 2
FREE SURFACE GRADIENT COMPATIBILITY : 0.9
H CLIPPING : NO
TYPE OF ADVECTION : 1;5
SUPG OPTION : 0;0
TREATMENT OF THE LINEAR SYSTEM : 2
SOLVER : 2
PRECONDITIONING : 2
SOLVER ACCURACY : 1.E-5
CONTINUITY CORRECTION : YES
```

````{admonition} How to find the Wesel example
:class: tip

Dieses Beispiel wird typischerweise im folgenden Verzeichnis installiert:

```
/telemac/v9.0.0/examples/telemac2d/wesel/
```
````


### Diskretierungsschema

Die Standardeinstellung von `DISCRETIZATIONS IN SPACE : 11;11` gibt eine lineare Diskretisierung für Geschwindigkeit und Wassertiefe zu, die rechnerisch schnell, aber potentiell instabil ist (weiterlesen Sie im Abschnitt unter {ref}`general Telemac2d parameters <tm2d-numerical>`). Um Stabilitätsprobleme im Zusammenhang mit dem Diskretierungsschema zu überwinden, beachten Sie unter `DISCRETIZATIONS IN SPACE : 12;11`. Darüber hinaus kann die Einstellung `FREE SURFACE GRADIENT COMPATIBILITY : 0.01` (d.h. in der Nähe von Null) bei der Fehlerbehebung von Stabilitätsproblemen im Zusammenhang mit der Diskretierung von Geschwindigkeit und Tiefe helfen.


### Höchste Iterationen
*Dieser Abschnitt wird von [Federica Scolari](https://www.iws.uni-stuttgart.de/institut/team/Scolari/)*.

Eine Simulation kann im *Terminal* `EXCEEDING MAXIMUM ITERATIONS` Warnungen drucken:

```fortran
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  0.7234532E-01
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
GRACJG (BIEF) : EXCEEDING MAXIMUM ITERATIONS:    50 RELATIVE PRECISION:  NaN
```

`EXCEEDING MAXIMUM ITERATIONS`warnungen können auftreten, wenn Sie **SCHEME FÜR ADVECTION VON [...]* Keywords mit den Werten `3`,`4`,`5`,`13` oder `14` verwenden. Der Grund ist, dass diese Systeme {term}`CFL` Bedingungen von weniger als 1 durch die Auslösung iterativer, adaptiver Timestepping liefern. Um `EXCEEDING MAXIMUM ITERATIONS`warnungen zu beheben, versuchen Sie die folgenden Optionen:

*	Verringern Sie den Zeitschritt allmählich.
*	Verringern Sie die Genauigkeit der Lösung (z.B. von `1.E-8` an `1.E-6`).
* Verwenden Sie andere Werte für `SCHEME FOR ADVECTION OF [...]`.
*	Erhöhen Sie den Schlüsselwortwert `MAXIMUM NUMBER OF ITERATIONS FOR SOLVER`, überschreiten Sie jedoch nicht `200`.
*	Ändern Sie den Typ `VELOCITY PROFILE` (lesen Sie die Anweisungen dieses eBooks für {ref}`2d <tm2d-bounds>` oder {ref}`3d  <tm3d-slf-boundaries>`).
*	Kaltstart (d.h. {ref}`defining initial conditions with the INITIAL CONDITIONS keyword in the steering file <tm2d-init-dry>`) darf nicht konvergieren. Daher auch
    -	die `PRESCRIBED FLOWRATES`(oder in {ref}`liquid boundary file <tm2d-liq-file>`) schrittweise zu erhöhen oder
    -	{ref}`create an initial conditions Selafin file <bk-create-slf>`, eine Wassertiefe an den Einlaufknoten zuzuordnen.


## Bayesische Kalibrierung

```{admonition} Requirements
Seien Sie bequem mit {ref}`supervised learning concepts (read on hydro-informatics.com) <supervisedlearning>` und vertraut mit dem erforderlichen Vokabular.

```


```{admonition} This section is under construction

Bis wir die Zeit gefunden haben, die Bayesische Kalibrierung mit der üblichen hydro-informatics.com Qualität zu beschreiben, laden wir Sie ein, sich unsere Open-Access-Publikation zur Kopplung von Telemac mit Surrogate-Modellen für Bayesian-Optimierungen: {cite:t}`mouris_stability_2023`. Weitere Informationen finden Sie auch unter {cite:t}`schwindt_bayesian_2023`, {cite:t}`mohammadi_bayesian_2018` und {cite:t}`oladyshkin_bayesian3_2020`.

```

