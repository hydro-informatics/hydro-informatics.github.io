---
description: Lineare Regression zur Vorhersage kontinuierlicher Variablen in der Wasserressourcen-Engineering, Abdeckung von Modellparametern, Gradientenabstieg, Regularisierung und strukturellen Versus-Schätzfehlern.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearregression)=
# Lineare Regression

In diesem Abschnitt werden wir die Konzepte von linearen ML-Algorithmen weiter erforschen, aber jetzt wird unsere Aufgabe sich auf die Vorhersage von Antworten in Bezug auf kontinuierliche Werte konzentrieren, anstatt diskrete Klassen, wie wir es in der linearen Klassifizierung taten. Unter der in der [Einleitung an ML](https://hydro-informatics.com/datascience/machinelearning.html) z.B. genannten ML-Anwendung wollen wir nun vorhersagen *wieviel* ist die Menge einer in Wasser gelösten chemischen Substanz, anstatt nur, wenn sie gelöst oder nicht (binäre Klassifikation).

```{admonition} Requirements
:class: warning
* Sie sind mit maschinellen Lernbedingungen vertraut. Wir empfehlen, die [Einführung an ML](https://hydro-informatics.com/datascience/machinelearning.html) zu lesen, um die von uns verwendete Nomenklatur über die gesamte Website zu kennen.
* Sie kennen grundlegende lineare Algebra-Konzepte (z.B. ein Punktprodukt, Vektorprojektionen, Ebenen, Eigenvektoren und Eigenwerte). Bitte verweisen Sie auf die Videos von [3Blue1Brown](https://youtu.be/kjBOesZCoqc), falls erforderlich, für eine entsprechende Überarbeitung.
* Grundkenntnisse in der Differentialrechnung (Derivation durch die Kettenregel, Gradienten).
```

Die lineare Regression konzentriert sich auf die Modellierung der Beziehung zwischen Eingangsgrößen (Features) und einer kontinuierlichen Zielgröße. Er nimmt einen linearen Zusammenhang zwischen den Eingangsmerkmalen und der Zielgröße an.

```{note}
Ein linearer Zusammenhang ist jede Beziehung zwischen zwei Größen, die einer Zeile im Koordinatenraum folgt. Dagegen sind nichtlineare Zusammenhänge nichtproportional zwischen Eingängen und Ausgängen, die mit Schwellen, Schleifen oder einer Funktion verbunden sein können, die nicht der Gleichung einer Zeile folgt ($y = a \cdot x + b$).
```

Hier ist unser Ziel wieder, die am besten passende Linie (oder Hyperplane in höheren Dimensionen) zu finden, die den Unterschied zwischen vorhergesagten und tatsächlichen Zielwerten minimiert. Zu diesem Zweck werden wir abdecken:

* Das kleinste Quadratkriterium zur Quantifizierung des Trainingsfehlers bei linearer Regression
* Der stochastische Gradientenabstieg (SDG) Algorithmus, der beim Training eines linearen Regressionsmodells verwendet wird
* Der Regularisierungsbegriff für lineare Regression
* Die Fehlerquellen bei linearer Regression


## Empirische Risikominimierung (ERM)

### Zielfunktion

Wie wir in der [Einführung an ML](https://hydro-informatics.com/datascience/machinelearning.html)] gesehen haben, besteht das Ziel von ML darin, die Zielfunktion durch Anpassung der Parameter des Modells durch Techniken (d.h. Optimierungsalgorithmen) wie Gradientenabstieg zu minimieren.

Eine der objektiven Funktionen, die wir bei der linearen Regression nutzen können, ist *Empirisches Risiko ($R$)*. Wir drücken das empirische Risiko in Bezug auf eine Verlustmaßnahme aus, die nur die Abweichung zwischen Modellvorhersagungen und den Zielwerten (oder Etiketten) unseres Trainingsdatensatzes widerspiegelt und somit keine Regularisierung berücksichtigt. Ziel der empirischen Risikominimierung ($R$) (ERM) ist es, ein Modell zu finden, das die Diskrepanz zwischen Vorhersagen und Beobachtungen auf den Trainingsdaten minimiert, mit der Annahme, dass es sich gut auf ungesehene Daten verallgemeinern wird. So können wir $R$ folgendermaßen definieren:

  $$
	R(\theta) = \frac{1}{n} \sum_{t=1}^n Loss(y^{(t)}-\theta \cdot x^{(t)})
  $$
$n$ ist die Anzahl der Ausbildungsbeispiele, $(x^{(t)}, y^{(t)})$ ist das $t$-th-Training Beispiel (Feature-Vektor bzw. Etikett) und $Loss$ ist eine generische Verlustfunktion. Beachten Sie, dass $\cdot§ ein Punktprodukt bedeutet.


```{important}
Beachten Sie auch, dass wir in unserer Definition des empirischen Risikos ($R$) oben den Vorurteilsbegriff ($\theta_0$) für Einfachheit ignorieren.
```

Eine häufige Möglichkeit, Abweichungen zwischen Vorhersagen und Beobachtungen zu den Trainingsdaten auszudrücken, besteht darin, den quadratischen Fehler $(y^{(t)}-\theta \cdot x^{(t)})^2$ zu berechnen, der die gewöhnlichesten Quadrate (OLS)-Zielfunktion ergibt:

  $$
	R(\theta) = \frac{1}{n} \sum_{t=1}^n (y^{(t)}-\theta \cdot x^{(t)})^2/2
  $$

```{note}
Die Streichung von Abweichungen zwischen Modellvorhersagungen und Etikettenwerten als Verlustfunktion ist eine häufige Praxis, um Optimierungsprobleme aufgrund ihrer Einfachheit, Differenzierbarkeit und konvexem Verhalten zu lösen. Wenn die Abweichungen im Durchschnitt groß sind, wird die quadratische Fehlerfunktion unser Modell stark penalisieren.
```

```{admonition} Know more
:class: seealso, dropdown

Aus mehreren Gründen ist es üblich, die Abweichungen zwischen Modellvorhersagungen und Etikettenwerten zur Verwendung als Verlustfunktion bei Optimierungsproblemen zu streichen:
* Einfachheit: Die Ausscheidung der Abweichungen vereinfacht die mathematische Formulierung der Verlustfunktion. Es entfällt die Notwendigkeit, die Richtung der Abweichung (positive oder negative) zu berücksichtigen und sicherzustellen, dass alle Abweichungen positiv zum Verlust beitragen. Zusätzlich bewahrt Squaring die schönen mathematischen Eigenschaften, die für die Optimierung erforderlich sind, wie differenzierbar und konvex.
* Betonung großer Fehler: Die Streichung der Abweichungen verstärkt die Auswirkungen größerer Fehler im Vergleich zu kleineren Fehlern. Durch die Squrierung der Abweichungen penalisiert die Verlustfunktion signifikante Abweichungen stärker, was in vielen Anwendungen wünschenswert sein kann. Dieser Schwerpunkt auf großen Fehlern kann den Optimierungsprozess zur Reduzierung von Ausreißern und zur Verbesserung der Gesamtgenauigkeit führen.
* Differenzierbarkeit: Durch die Streichung der Abweichungen wird die Verlustfunktion differenzierbar, was für Optimierungsalgorithmen, die auf Gradienten zur Aktualisierung der Modellparameter vertrauen, entscheidend ist. Die Fähigkeit, Derivate zu berechnen, ermöglicht eine effiziente Optimierung mit gradientenbasierten Methoden wie Gradientenabstieg oder stochastische Gradientenabstieg. Diese Methoden passen die Modellparameter iterativ in die Richtung, die den Verlust minimiert.
* Konvexität: Squared Verlust ist eine konvexe Funktion, d.h. es hat ein einziges globales Minimum. Die Konvexität vereinfacht den Optimierungsprozess, da sie gewährleistet, dass die Verlustfunktion eine einzigartige Lösung hat und Optimierungsalgorithmen zuverlässig mit dieser Lösung zusammenkommen können. Nicht-Convex-Verlustfunktionen können mehrere lokale Minima haben, die die Optimierung anspruchsvoller machen können.

```


### Lernalgorithmus

Nun verwenden wir den stochastischen Gradientenabstieg (SDG)-Algorithmus, um unser Modell $\theta$ zu aktualisieren. Beachten Sie, dass wir dies tun, indem wir die Modellparameter $\theta$ mit dem Gradienten unserer Zielfunktion, d.h. empirisches Risiko, an jedem Trainingsbeispiel ausgewertet. So kreuzen wir $\theta$ in Richtung der Richtung gegenüber dem Gradienten $\nabla_\theta R(\theta)$. Beachten Sie, dass die Funktion $R$ oben, definiert mit dem quadratischen Fehler als Verlustfunktion, überall differenzierbar ist. Wir berechnen den Gradienten des empirischen Risikos, das ergibt:

  $$
	\nabla_\theta R(\theta) = -(y^{(t)}-\theta \cdot x^{(t)}) \cdot x^{(t)}
  $$

So können wir unseren Lernalgorithmus als:

1. Initialisieren $\theta = 0$
2. Randomly wählen $t = {1, ..., n}$
3. Update $\theta$, so dass:
	
	$$
		\theta = \theta - \eta (- (y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}) \\
		\therefore \theta = \theta + \eta (y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}
	$$
wo $\eta$ die Lernrate ist.


Beachten Sie, dass dieser Lernalgorithmus demjenigen für den Fall der linearen Klassifizierung sehr ähnlich ist.

````{admonition} Exercise 1: Difference between learning algorithms for regression and classification
:class: tip
Es gibt einen großen Unterschied zwischen diesem Lernalgorithmus und dem, den wir für die Ausbildung eines linearen Klassifikators abgedeckt. Kannst du es sehen? Hinweis: Achten Sie darauf, wie das Update von $\theta$ für lineare Regression funktioniert.


```{admonition} Solution
:class: dropdown
Der Lernalgorithmus für lineare Regression wird $\theta$ an jedem Schritt anpassen, an dem es einige Diskrepanzen gab ($y^{(t)}-\theta \cdot x^{(t)} \neq 0$). So geht es uns nicht darum, ob es einen Fehler gibt oder nicht, den wir mit einer ``if``-Klausel in {ref}`linearclassification` überprüft haben, sondern eher nach *wieviel* war die Diskrepanz.
Wenn die Vorhersage und der korrekte Wert viel abweichen, wird der Algorithmus dafür sorgen, $\theta$ stärker zu korrigieren und, wenn die Diskrepanzen klein sind, wird der Algorithmus weniger korrigieren.

```
````


## Reglementierung: Ridge Regression

### Zielfunktion

Bisher hat sich unser Optimierungsproblem für die Ausbildung eines linearen Regressionsmodells nur auf die Minimierung des Trainingsfehlers (Empirische Risikominimierung oder ERM) konzentriert. Allerdings ist in den meisten Fällen ein regulärer Begriff von entscheidender Bedeutung, sonst kann unser Modell nicht für andere Datensätze verallgemeinern (neben dem Trainingsdatensatz in den Händen). Daher werden wir jetzt einen Regelbegriff für unsere Zielfunktion einführen, der nun ein *Kühlregression*-Problem darstellt. Ridge Regression führt einen regulären Begriff ein, oft die "Kühle Strafe" oder "L2 Strafe" auf die gewöhnliche am wenigsten Quadrate (OLS) objektive Funktion genannt. Dieser Straftermin ($\frac{1}{2} \| \theta \|^2$) steuert die Komplexität des Modells durch Schrumpfung $\theta$ (d.h. Regressionskoeffizienten) auf Null. So ist die Zielfunktion $J(\theta)$ für die Regression des Grats:

  $$
	J(\theta) = \frac{\lambda}{2} \| \theta \|^2 + R(\theta) 
  $$

wobei $\lambda$ der Regelparameter ist, den wir in der {ref}`linearclassification` erfasst haben.

### Lernalgorithmus

Wie wir in der Empirical Risk Minimization (ERM) Methode taten, können wir auch den stochastischen Gradienten-Abstiegsalgorithmus in der Gratregression anwenden, nur jetzt müssen wir den Gradienten der neuen Zielfunktion ($\nabla_\theta J(\theta)$) nehmen und es verwenden, um $\theta$ an jeder Iteration über den Trainingsdatensatz zu aktualisieren.

Erweitern wir zunächst alle Bedingungen von $J(\theta)$:

  $$
	J (\theta)= \frac{\lambda}{2} \| \theta \|^2 + R (\theta) = \frac{\lambda}{2} \| \theta \|^2 + \frac{1}{n} \sum_{t=1}^n \frac{(y^{(t)}- \theta \cdot x^{(t)})^2}{2}  
  $$
  
	
Der Gradient kann nun als:

  $$
	\nabla_\theta J(\theta) = \lambda \theta - (y^{(t)}- \theta \cdot x^{(t)}) x^{(t)}
  $$
	
So können wir unseren Lernalgorithmus als:

1. Initialisieren $\theta = 0$
2. Randomly wählen $t = {1, ..., n}$
3. Update $\theta$, so dass:
	
	$$
		\theta = \theta - \eta (\lambda \theta - (y^{(t)} - \theta \cdot x^{(t)}) x^{(t)}) \\
	$$
wo $\eta$ die Lernrate ist.
	
	
````{admonition} Exercise 2: Simplify and understand the expression of the update of $\theta$ for ridge regression
:class: tip

Versuchen Sie, den Ausdruck oben zu vereinfachen, dass den Wert von $\theta$ an jeder Iteration aktualisiert. Hinweis: Sie werden mit einer Summe von zwei Begriffen enden. Was versucht jeder dieser Begriffe während der Optimierung zu erreichen?

```{admonition} Solution
:class: dropdown
Vereinfachung der Update-Ausdruckserträge:

  $$
	\theta = (1 - \eta \lambda) \theta + \eta (y^{(t)} - \theta \cdot x^{(t)}) x^{(t)}
  $$

Die zweite Ausdrucksperiode, $(y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}$, ist genau das, was wir zuvor in der WKM gesehen hatten (vor wir die Regulierung hinzugefügt haben). Der erste Begriff, $(1-\eta \lambda)$, versucht, $\theta$ so nah wie möglich zu Null zu halten, da sowohl $\lambda$ (Regularisierungsterm) als auch $\eta$ (Lernrate) positive Zahlen sind. So korrigiert der zweite Begriff unsere Modellparameter $\theta$ zur Minimierung des Trainingsverlustes, während der erste Begriff versucht, $\theta$ möglichst klein zu halten.
```
````

Beachten Sie, dass wir durch die Hinzufügung eines Regelbegriffs zu unserer Zielfunktion nun ein optimales Modell finden, das es anstatt die Trainingsdaten perfekt anzupassen, auch auf andere Datensätze verallgemeinert werden kann. Wir tun dies, weil wir glauben, dass das Modell nicht auf jedes einzelne Stück von schwachen Beweisen oder Geräuschen im Trainingsdatensatz angepasst werden sollte. Stattdessen stellen wir den Regularisierungsparameter $\lambda$ ein, der verhindert, dass $\theta$ ändert, außer wenn der Nachweis stark genug ist, um einen Anstieg von $\theta$ zu werten. Mit steigendem Wert von $\lambda$ erhöht sich auch der Trainingsfehler, aber mit der Hoffnung, dass unser Modell besser verallgemeinert und einen geringeren Testfehler ergibt.

## Struktur gegen Schätzfehler

Bei der Auswahl eines ML-Algorithmus machen wir bestimmte Annahmen über die Beziehung zwischen den Merkmalen und den Etiketten. Bei linearer Regression wird davon ausgegangen, dass der Zusammenhang zwischen den Merkmalen und den Etiketten durch eine lineare Gleichung dargestellt werden kann. Wenn diese Annahme verletzt wird, wie wenn die wahre Beziehung nicht linear ist, dann wird unser Modell einen hohen *Strukturfehler* haben, weil es die zugrunde liegenden Muster in den Daten nicht genau erfassen kann. Somit umfasst der strukturelle Fehler die Einschränkungen oder Annahmen des gewählten Modells, und er stellt den irreduzierbaren Fehler dar, der unabhängig von der Menge der Trainingsdaten nicht beseitigt werden kann. *Schätzungsfehler* hingegen ergibt sich aus der endlichen Natur der Trainingsdaten und der daraus resultierenden Unfähigkeit unseres Modells, aus diesen Daten zu passen oder zu verallgemeinern. Schätzungsfehler können auftreten, wenn die verfügbaren Trainingsdaten begrenzt sind oder die tatsächlich zugrunde liegende Verteilung des Problems nicht ausreichend darstellt. In solchen Fällen kann das Modell kämpfen, um die wahren Muster und Zusammenhänge in den Daten zu erfassen, was zu höheren Schätzungsfehlern führt.

`````{admonition} Exercise 3: Sources of error in linear regression
:class: tip
Welche der nachfolgenden Figuren zeigt Struktur- bzw. Schätzfehler besser? Die blauen Punkte bezeichnen den Trainingsdatensatz und die orange Linie das lineare Regressionsmodell.

````{figure} ../img/datascience/struc-vs-estimation-error.jpg
:alt: strucure versus estimation error
:name: truc-vs-est-errors

Beispiel für Struktur- und Schätzfehler.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 3.
:header-rows: 1
:name: tab-ml-ex1-solutionx
* - Plot
- a
- b
* - Fehlertyp
- Struktur
- Schätzung
```

````
`````

 
 
 
 
 