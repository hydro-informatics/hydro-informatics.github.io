---
description: Lineare Regression zur Vorhersage kontinuierlicher Variablen in der Wasserressourcentechnik, die Modellparameter, Gradientenabstieg, Regularisierung und strukturelle versus Schätzungsfehler abdeckt.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearregression)=
# Lineare Regression

In diesem Abschnitt werden wir die Konzepte der linearen ML-Algorithmen weiter untersuchen, aber jetzt wird sich unsere Aufgabe darauf konzentrieren, Antworten in Bezug auf kontinuierliche Werte vorherzusagen, anstatt diskrete Klassen, wie wir es in der linearen Klassifizierung getan haben. Unter Berücksichtigung der in der [Einführung in ML](https://hydro-informatics.com/datascience/machinelearning.html)] erwähnten ML-Anwendung möchten wir nun möglicherweise * wie viel * die Menge einer in Wasser gelösten chemischen Substanz ist, und nicht nur, ob sie gelöst ist oder nicht (binäre Klassifizierung).

```{admonition} Requirements
:class: warning
* Sie kennen Begriffe des maschinellen Lernens. Wir empfehlen, den Abschnitt [Einführung in ML](https://hydro-informatics.com/datascience/machinelearning.html)] zu lesen, um sich mit der Nomenklatur vertraut zu machen, die wir auf der gesamten Website verwenden.
* Sie kennen grundlegende lineare Algebra-Konzepte (wie ein Punktprodukt, Vektorprojektionen, Ebenen, Eigenvektoren und Eigenwerte). Bitte beachten Sie die Videos von [3Blue1Brown](https://youtu.be/kjBOesZCoqc) für eine geeignete Überarbeitung, falls erforderlich].
* Grundkenntnisse in Differentialrechnung (Ableitung durch die Kettenregel, Gradienten).
```

Die lineare Regression konzentriert sich auf die Modellierung der Beziehung zwischen Eingangsvariablen (Features) und einer kontinuierlichen Zielvariablen. Sie geht von einem linearen Zusammenhang zwischen den Eingangsmerkmalen und der Zielgröße aus.

```{note}
Eine lineare Beziehung ist jede Beziehung zwischen zwei Variablen, die einer Linie im Koordinatenraum folgt. Im Gegensatz dazu beinhalten nichtlineare Beziehungen eine Nichtproportionalität zwischen Ein- und Ausgängen, die sich auf Schwellenwerte, Schleifen oder eine Funktion beziehen kann, die nicht der Gleichung einer Linie folgt ($y = a \cdot x + b$).
```

Hier ist es wieder unser Ziel, die am besten passende Linie (oder Hyperebene in höheren Dimensionen) zu finden, die den Unterschied zwischen vorhergesagten und tatsächlichen Zielwerten minimiert. Zu diesem Zweck werden wir Folgendes abdecken:

* Kriterium der kleinsten Quadrate zur Quantifizierung des Trainingsfehlers in der linearen Regression
* Der stochastische Gradientenabstieg (SDG) Algorithmus, der im Trainingsprozess eines linearen Regressionsmodells verwendet wird
* Der Regularisierungsterm für lineare Regression
* Fehlerquellen bei der linearen Regression


## Empirische Risikominimierung (ERM)

### Zielfunktion

Wie wir in der [Einführung in ML](https://hydro-informatics.com/datascience/machinelearning.html)] gesehen haben, ist das Ziel von ML, die Zielfunktion zu minimieren, indem die Parameter des Modells durch Techniken (dh Optimierungsalgorithmen) wie Gradientenabstieg angepasst werden.

Eine der objektiven Funktionen, die wir bei der linearen Regression verwenden können, ist *Empirisches Risiko ($R$)*. Wir drücken das empirische Risiko in Form eines Verlustmaßes aus, das nur die Abweichung zwischen Modellvorhersagen und den Zielwerten (oder Labels) unseres Trainingsdatensatzes widerspiegelt und somit keine Regularisierung berücksichtigt. Ziel der empirischen Risikominimierung ($R$) ist es, ein Modell zu finden, das die Diskrepanz zwischen Vorhersagen und Beobachtungen der Trainingsdaten minimiert, wobei davon ausgegangen wird, dass es sich gut auf unsichtbare Daten verallgemeinert. So können wir $R$ wie folgt definieren:

  $$
	R(\theta) = \frac{1}{n} \sum_{t=1}^n Loss(y^{(t)}-\theta \cdot x^{(t)})
  $$
where $n$ is the number of training examples, $(x^{(t)}, y^{(t)})$ is the $t$-th training example (feature vector and label, respectively), and $Loss$ is a generic loss function. Note that $\cdot§ denotes a dot product.


```{important}
Beachten Sie auch, dass wir in unserer Definition des empirischen Risikos ($R$) den Bias-Begriff ($\theta_0$) aus Gründen der Einfachheit ignorieren.
```

One common way to express deviations between predictions and observations on the training data is to compute the squared error, $(y^{(t)}-\theta \cdot x^{(t)})^2$, which yields the ordinary least squares (OLS) objective function:

  $$
	R(\theta) = \frac{1}{n} \sum_{t=1}^n (y^{(t)}-\theta \cdot x^{(t)})^2/2
  $$

```{note}
Das Quadratieren von Abweichungen zwischen Modellvorhersagen und Labelwerten als Verlustfunktion ist eine gängige Praxis, um Optimierungsprobleme aufgrund ihrer Einfachheit, Differenzierbarkeit und ihres konvexen Verhaltens zu lösen. Wenn die Abweichungen im Durchschnitt groß sind, wird die quadrierte Fehlerfunktion unser Modell stark bestrafen.
```

```{admonition} Know more
:class: seealso, dropdown

Die Quadratur der Abweichungen zwischen Modellvorhersagen und Labelwerten, die als Verlustfunktion verwendet werden können, ist bei Optimierungsproblemen aus mehreren Gründen üblich:
* Einfachheit: Die Quadratur der Abweichungen vereinfacht die mathematische Formulierung der Verlustfunktion. Es eliminiert die Notwendigkeit, die Richtung der Abweichung (positiv oder negativ) zu berücksichtigen und stellt sicher, dass alle Abweichungen positiv zum Verlust beitragen. Darüber hinaus behält die Quadratur die schönen mathematischen Eigenschaften bei, die für die Optimierung erforderlich sind, wie z. B. differenzierbar und konvex.
* Betonung großer Fehler: Die Quadratur der Abweichungen verstärkt die Auswirkungen größerer Fehler im Vergleich zu kleineren Fehlern. Durch die Quadrierung der Abweichungen werden durch die Verlustfunktion signifikante Abweichungen stärker benachteiligt, was bei vielen Anwendungen wünschenswert sein kann. Diese Betonung großer Fehler kann dazu führen, dass sich der Optimierungsprozess auf die Reduzierung von Ausreißern und die Verbesserung der Gesamtgenauigkeit konzentriert.
* Differenzierbarkeit: Die Quadratur der Abweichungen macht die Verlustfunktion differenzierbar, was für Optimierungsalgorithmen, die auf Gradienten zur Aktualisierung der Modellparameter angewiesen sind, von entscheidender Bedeutung ist. Die Fähigkeit, Derivate zu berechnen, ermöglicht eine effiziente Optimierung mit Gradienten-basierten Methoden wie Gradientenabstieg oder stochastische Gradientenabstieg. Diese Methoden passen die Modellparameter iterativ in die Richtung an, die den Verlust minimiert.
* Konvexität: Quadratverlust ist eine konvexe Funktion, was bedeutet, dass es ein einziges globales Minimum hat. Convexity vereinfacht den Optimierungsprozess, da es garantiert, dass die Verlustfunktion eine einzigartige Lösung hat und Optimierungsalgorithmen zuverlässig zu dieser Lösung konvergieren können. Nicht-konvexe Verlustfunktionen können mehrere lokale Minima haben, was die Optimierung schwieriger machen kann.

```


### Lernalgorithmus

Now, we will use the stochastic gradient descent (SDG) algorithm to update our model $\theta$. Recall that we do this by adjusting the model parameters $\theta$ with the gradient of our objective function, i.e., empirical risk, evaluated at each training example. Thus, we nudge $\theta$ towards the direction opposite to the gradient $\nabla_\theta R(\theta)$. Note that the function $R$ above, defined with the squared error as loss function, is differentiable everywhere. We compute the gradient of the empirical risk, which yields:

  $$
	\nabla_\theta R(\theta) = -(y^{(t)}-\theta \cdot x^{(t)}) \cdot x^{(t)}
  $$

Daher können wir unseren Lernalgorithmus wie folgt zusammenfassen:

1. Initialisieren $\theta = 0$
2. Zufällig auswählen $t = {1, ..., n}$
3. Update $\theta$, so that:
	
	$$
		\theta = \theta - \eta (- (y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}) \\
		\therefore \theta = \theta + \eta (y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}
	$$
	where $\eta$ is the learning rate.


Beachten Sie, dass dieser Lernalgorithmus dem für den Fall der linearen Klassifikation sehr ähnlich ist.

````{admonition} Exercise 1: Difference between learning algorithms for regression and classification
:class: tip
There is one major difference between this learning algorithm and the one we covered for training a linear classifier. Can you spot it? Hint: Look carefully to how the update of $\theta$ for linear regression works. 


```{admonition} Solution
:class: dropdown
The learning algorithm for linear regression will be adjusting $\theta$ at every step where there was some discrepancy ($y^{(t)}-\theta \cdot x^{(t)} \neq 0$). Thus, we are not concerned whether there is a mistake or not, which we checked with an ``if`` clause in {ref}`linearclassification`, but are rather looking for *how much* was the discrepancy.
If the prediction and the correct value deviate a lot, then the algorithm will make sure to correct $\theta$ more strongly and, if the discrepancies are small, the algorithm will be correcting less.

```
````


## Regularisierung: Ridge-Regression

### Zielfunktion

Bisher hat sich unser Optimierungsproblem für das Training eines linearen Regressionsmodells nur auf die Minimierung des Trainingsfehlers (empirische Risikominimierung oder ERM) konzentriert. Ein Regularisierungsbegriff ist jedoch in den meisten Fällen entscheidend, da unser Modell sonst nicht für andere Datensätze verallgemeinern kann (zusätzlich zum Trainingsdatensatz in den Händen). Daher werden wir nun einen Regularisierungsterm in unsere Zielfunktion einführen, der nun ein *ridge Regression * Problem darstellt. Die Ridge-Regression führt einen Regularisierungsbegriff ein, der oft als "Gridge-Strafe" oder "L2-Strafe" für die Objektivfunktion der gewöhnlichen kleinsten Quadrate (OLS) bezeichnet wird. Dieser Strafbegriff ($\frac{1}{2} \| \theta \|^2$) steuert die Komplexität des Modells, indem er $\theta$ (d.h. Regressionskoeffizienten) gegen Null schrumpft. Daher ist die Objektivfunktion $J(\theta)$ für die Gratregression:

  $$
	J(\theta) = \frac{\lambda}{2} \| \theta \|^2 + R(\theta) 
  $$

wobei $\lambda$ der Regularisierungsparameter ist, den wir in {ref}`linearclassification` behandelt haben.

### Lernalgorithmus

Wie bei der Methode der empirischen Risikominimierung (ERM) können wir auch den stochastischen Gradientenabstiegsalgorithmus bei der Gratregression anwenden, nur jetzt müssen wir den Gradienten der neuen Zielfunktion ($\nabla_\theta J(\theta)$) nehmen und ihn verwenden, um $\theta$ bei jeder Iteration durch den Trainingsdatensatz zu aktualisieren.

Let's first expand all terms of $J(\theta)$:

  $$
	J (\theta)= \frac{\lambda}{2} \| \theta \|^2 + R (\theta) = \frac{\lambda}{2} \| \theta \|^2 + \frac{1}{n} \sum_{t=1}^n \frac{(y^{(t)}- \theta \cdot x^{(t)})^2}{2}  
  $$
  
	
Der Gradient kann jetzt berechnet werden als:

  $$
	\nabla_\theta J(\theta) = \lambda \theta - (y^{(t)}- \theta \cdot x^{(t)}) x^{(t)}
  $$
	
Daher können wir unseren Lernalgorithmus wie folgt zusammenfassen:

1. Initialisieren $\theta = 0$
2. Zufällig auswählen $t = {1, ..., n}$
3. Update $\theta$, so that:
	
	$$
		\theta = \theta - \eta (\lambda \theta - (y^{(t)} - \theta \cdot x^{(t)}) x^{(t)}) \\
	$$
	where $\eta$ is the learning rate.
	
	
````{admonition} Exercise 2: Simplify and understand the expression of the update of $\theta$ for ridge regression
:class: tip

Try to simplify the expression above that updates the value of $\theta$ at each iteration. Hint: You will end up with a sum of two terms. What is each of these terms trying to achieve during the optimization?

```{admonition} Solution
:class: dropdown
Vereinfachen des Update-Ausdrucks ergibt:

  $$
	\theta = (1 - \eta \lambda) \theta + \eta (y^{(t)} - \theta \cdot x^{(t)}) x^{(t)}
  $$

The second term of the expression, $(y^{(t)}-\theta \cdot x^{(t)}) x^{(t)}$, is exactly what we had seen before in ERM (before we added regularization). The first term, $(1-\eta \lambda)$, is trying to keep $\theta$ as close as possible to zero, since both $\lambda$ (regularization term) and $\eta$ (learning rate) are positive numbers. Thus, the second term is correcting our model parameters $\theta$ towards minimizing the training loss, whereas the first term tries to keep $\theta$ as small as possible.
```
````

Note that by adding a regularization term to our objective function, we are now concerned with finding an optimal model that, rather than fitting the training data perfectly, it is able to generalize to other datasets as well. We do so because we believe that the model should not be adjusted to every single piece of weak evidence or noise contained in the training dataset. Instead, we introduce the regularization parameter $\lambda$, which avoids that $\theta$ changes except for when the evidence is strong enough to worth an increase of $\theta$. As the value of $\lambda$ increases, so does the training error, but with the hope that our model will generalize better, yielding a lower test error.

## Strukturelle vs. Schätzungsfehler

Bei der Auswahl eines ML-Algorithmus machen wir bestimmte Annahmen über die Beziehung zwischen den Features und den Labels. Bei linearer Regression wird angenommen, dass die Beziehung zwischen den Merkmalen und den Etiketten durch eine lineare Gleichung dargestellt werden kann. Wenn diese Annahme verletzt wird, z. B. wenn die wahre Beziehung nichtlinear ist, hat unser Modell einen hohen * Strukturfehler *, da es die zugrunde liegenden Muster in den Daten nicht genau erfassen kann. Strukturfehler umfassen also die Einschränkungen oder Annahmen des gewählten Modells und stellen den irreduziblen Fehler dar, der unabhängig von der Menge der Trainingsdaten nicht beseitigt werden kann. *Schätzfehler* hingegen ergibt sich aus der Endlichkeit der Trainingsdaten und der daraus resultierenden Unfähigkeit unseres Modells, aus diesen Daten zu passen oder zu verallgemeinern. Schätzungsfehler können auftreten, wenn die verfügbaren Trainingsdaten begrenzt sind oder die wahre zugrunde liegende Verteilung des Problems nicht ausreichend darstellen. In solchen Fällen kann das Modell Schwierigkeiten haben, die wahren Muster und Beziehungen in den Daten zu erfassen, was zu höheren Schätzungsfehlern führt.

`````{admonition} Exercise 3: Sources of error in linear regression
:class: tip
Welche der folgenden Abbildungen zeigt Struktur- bzw. Schätzfehler besser? Die blauen Punkte bezeichnen den Trainingsdatensatz und die orange Linie das lineare Regressionsmodell.

````{figure} ../img/datascience/struc-vs-estimation-error.jpg
:alt: strucure versus estimation error
:name: truc-vs-est-errors

Beispiele für Struktur- und Schätzfehler.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 3.
:header-rows: 1
:name: tab-ml-ex1-solutionx
* - Grundstück
  - a
  - b
* - Fehlerart
  - Struktur
  - Schätzung
```

````
`````

 
 
 
 
 