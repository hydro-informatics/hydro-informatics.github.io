---
description: Lineare Klassifikationsgrundsätze mit dem Perceptron-Algorithmus und Margen-Klassifikatoren mit Regularisierung für maschinelle Lernanwendungen in der Wasserressourcentechnik.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearclassification)=
# Lineare Klassifizierung

In diesem Abschnitt werden wir die Grundlagen der linearen Klassifizierung durch einen einfachen ML-Algorithmus, den Perceptron. Darüber hinaus werden wir die Konzepte hinter dem Perceptron-Algorithmus erweitern, indem wir Aspekte der *Regularisierung* berücksichtigen, um einen Margen-Linear-Klassifikator aufzubauen.

```{admonition} Requirements
:class: warning
* Sie sind mit maschinellen Lernbedingungen vertraut. Wir empfehlen, unsere [Einführung an ML](https://hydro-informatics.com/datascience/machinelearning.html) zu lesen, um die Nomenklatur, die wir auf der ganzen Website verwenden, kennenzulernen.
* Sie kennen grundlegende lineare Algebra-Konzepte (wie ein Punktprodukt, Vektor-Projektionen, Ebenen, Eigenvektoren und Eigenwerte). Bitte beachten Sie die Videos von [3Blue1Brown](https://youtu.be/kjBOesZCoqc) für eine entsprechende Revision, falls erforderlich.
* Grundkenntnisse in Python und Array Computing mit NumPy.
```


## Hyperplane

Angenommen, wir möchten positive und negative Objekte aus dem Trainingssatz unten (Abbildung links) klassifizieren:

```{figure} ../img/datascience/decision-boundary.png
:alt: decisionbound
:name: cloud-points-ml

Trainingsset von Punkten mit binären Labels (+1, -1) und zweidimensionalen $(x_1, x_2)$ Features. Die Entscheidungsgrenze (graue Linie) wird durch den Parametervektor $\theta$, der der Entscheidungsgrenze normal ist, und den Offsetparameter $\theta_0$, der die Daten linear trennt, definiert.
```

Der vorstehende Datensatz wird als linear trennbar angesehen, da er mindestens eine lineare Entscheidungsgrenze zur korrekten Aufteilung des gesamten Datensatzes aufweist. Zum Beispiel könnten wir eine Entscheidungsgrenze wie die graue Linie oben passieren (Abbildung rechts)


Da die Merkmale $(x_1, x_2) \in \mathbb{R}^2 $, d.h. der Merkmalssatz zum zweidimensionalen Raum gehört, stellt die Entscheidungsgrenze eine Linie dar. Wenn wir mit einer Reihe von Features im dreidimensionalen Raum $(x_1, x_2, x_3)$ umgehen, wäre die Entscheidungsgrenze ein Flugzeug. In analoger Weise, wenn unser Feature-Set in einem höheren Raum wäre, würde die Entscheidungsgrenze eine *Hyperplane* bilden.


Ein Hyperplan mit $d$-Dimensionen wird üblicherweise durch den flugzeugnormalen Vektor $\theta \in \mathbb{R}^d$ und Offset (scalar) Parameter $\theta_0$ bezeichnet. Im obigen Beispiel würden wir das Hyperplan (oder die Entscheidungsgrenze) definieren als:

  $$
	\theta \cdot X + \theta_0 =0 \equiv \begin{bmatrix} \theta_1 & \theta_2 \end{bmatrix} \cdot \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} + \theta_0 = 0
  $$


```{note}
Beachten Sie, dass $\theta$ die Orientierung (Slope oder Neigung) der Grenze steuert, während $\theta_0$ den Standort (oder Offset oder Bias) der Grenze steuert. Wenn also $\theta_0 = 0$, dann kreuzt die Entscheidungsgrenze den Ursprung. $\theta_0$ wird auch oft als *bias term* bezeichnet.
```
 
Unser Klassifikator$h(x, \theta, \theta_0)$ ist damit gleich $sign(\theta \cdot X + \theta_0)$, wo$\theta \in \mathbb{R}^2 $ und $\theta_0 \in \mathbb{R}$. Rufen Sie die Vorzeichenfunktion, auch als Vorzeichenfunktion bekannt, ist eine mathematische Funktion, die das Vorzeichen oder die Richtung einer realen Zahl zurückgibt. Das heißt, wenn die Eingangszahl positiv, negativ oder 0 ist, kehrt die Vorzeichenfunktion +1, -1 bzw. 0 zurück.
 
 
`````{admonition} Exercise 1
:class: tip
Versuchen Sie, zu beantworten, ob das Paar der folgenden Trainingsbeispiele linear trennbar sind. Welche sind durch den Ursprung linear trennbar?

````{figure} ../img/datascience/exercise-decision-bound.png
:alt: ex-decision-bound
:name: exercise-db

Übung 1 auf linear trennbaren Paar von Beispielen.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 1.
:header-rows: 1
:name: tab-ml-ex1-solution

* - Datensatz
  - eine
  - B.
  - c)
  - dgl.
* - Linear trennbar (LS)?
  - Ja.
  - Nein
  - Ja.
  - Nein
* - LS durch Herkunft?
  - Nein
  - Nein
  - Ja.
  - Nein

```
````
`````

## Perceptron-Algorithmus

Im Perceptron-Algorithmus initialisieren wir typischerweise $\theta$ als Null (Nullvektor) und schleifen durch das Paar von Trainingsbeispielen. Bei jeder Iteration werden wir überprüfen, ob der Klassifikator einen Fehler macht, dieses Trainingsbeispiel (i-th Beispiel) einzustufen, und wenn ja, dann aktualisieren wir die Parameter von $\theta$.


Assume that $\theta_0 =0$ for simplicity (the decision boundary must pass through the origin). Our perceptron classifier will make a mistake ``if`` $y^{(i)}(\theta \cdot x^{(i)}) \leq 0$. We will then update our $\theta$ to no longer misclassify that training example. The way to do this is by adding $y^{(i)}x^{(i)}$ to the previous $\theta$. Thus, the update would look like:

  $$
	\theta = \theta + y^{(i)}x^{(i)}
  $$


````{admonition} Exercise 2: Understanding the perceptron update
:class: tip
Versuchen Sie zu verstehen, warum dieses Update nützlich ist. Hinweis: Ersetzen Sie den Ausdruck für die Aktualisierungen $\theta$ in der ``if``Check.

```{admonition} Solution
:class: dropdown

Substituiert den Ausdruck für den aktualisierten $\theta$, um zu überprüfen, ob der Klassifikator in diesem Beispiel noch einen Fehler macht:

  $$
	y^{(i)}(\theta + y^{(i)}x^{(i)})x^{(i)}
  $$
  
Wir initialisieren $\theta$ als Null, so wird der Ausdruck vereinfacht auf:
 
  $$
    y^{(i)}(y^{(i)}x^{(i)})x^{(i)}
  $$
  
Da jedes Etikett selbst gleich einer ist (beide $1 * 1$ und $-1 * -1$ gleich 1), wird der Ausdruck folgendermaßen:

  $$
    x^{(i)}x^{(i)} = \| x^{(i)} \|^2 > 0 
  $$
  
Dies bedeutet, dass der Ausdruck $y^{(i)}(\theta \cdot x^{(i)}) > 0$ (kein Fehler) So wurde $\theta$ so aktualisiert, dass es das i-th-Beispiel nicht mehr missklassifiziert.
```
````


Wir haben in den Händen eine Reihe von verschiedenen Trainingsbeispielen, die das Potenzial haben, unseren Klassifikator in viele Richtungen zu nudeln/zu aktualisieren. So ist es möglich und sogar erwartet, dass die letzten Trainingsbeispiele Updates verursachen, die frühere, erste Updates überschreiben werden. Dies führt dazu, dass frühere Beispiele nicht mehr korrekt klassifiziert werden. Aus diesem Grund müssen wir durch das gesamte Trainingsset mehrere $T$-Zeiten schleifen, um sicherzustellen, dass alle Beispiele korrekt klassifiziert werden. Solche Iterationen können sowohl in Reihenfolge als auch zufällig aus den Trainingsbeispielen ausgewählt werden.

Wir können den Algorithmus wie folgt kodieren:

```python
import numpy as np


# Algorithm always starting to loop from x1
def perceptron(X, y, theta, t_times):
    n_mistakes = 0

    # Initialize list to show the progress (updates) of theta
    progress_theta = []

    # Initialize an array with same size as the total number of examples to count how many mistake are made at each training example
    explicit_mistakes = np.zeros(shape=y.shape[0])

    # Loop through the training set T times
    for t in t_times:

        # Loop through the training examples in order
        for index, x in enumerate(X):

            # Check if the algorithm makes a mistake in the i-th (or index-th) example
            if y[index] * np.dot(theta, x) <= 0:
                # Update theta to no longer misclassify the i-th example
                theta = theta + y[index] * x

                # Save the update theta
                progress_theta.append(theta)

                # Update total number of mistakes
                n_mistakes += 1

                # Update total number of mistakes at the i-th training example
                explicit_mistakes[index] += 1
    print('The perceptron did {} mistakes until convergence'.format(n_mistakes))
    return progress_theta, n_mistakes, explicit_mistakes


if __name__ == '__main__':
    X = np.array([[-1, -1], [1, 0], [-1, 1.5]])
    # X = np.array([[-1, -1], [1, 0], [-1, 10]])

    y = np.array([1, -1, 1])

    t_times = range(0, 100)

    theta = np.array([-1, -1])

    a, b, c = perceptron(X, y, theta, t_times)
```

## Margengrenzen und Scharnierverlust

Wie Sie vielleicht bemerkt haben, bietet der Perceptron-Algorithmus keinen Regularisierungsbegriff. Das Ziel war einfach, jede Entscheidungsgrenze zu finden, die die Daten richtig teilen kann. Hier werden wir das Konzept von *hinge loss* und *margin Grenzen* einführen, um das Problem des Lernens einer Entscheidungsgrenze in ein Optimierungsproblem unter Berücksichtigung der Regularisierung zu transformieren.

### Motivation hinter Margengrenzen

Schauen wir uns unseren bisher vorgestellten Trainingsdatensatz an (Abbildung unten). Jede Entscheidungsgrenze innerhalb der gestrichelten Graulinien teilt die Trainingsbeispiele richtig auf. Intuitiv möchten wir jedoch eine Entscheidungsgrenze bevorzugen, die die Abstände zwischen der Entscheidungsgrenze und den Trainingspunkten maximieren kann. Der Grund dafür ist, dass es wahrscheinlich ist, dass die Punkte, die wir zukünftig klassifizieren möchten, statistische Geräusche haben, so dass eine zu nahe an den Ausbildungsbeispielen liegende Entscheidungsgrenze eher eine geringfügig veränderte (noisier) Versionen der Ausbildungsbeispiele falsch einstufen kann. Ein Klassifikator, der eine relativ höhere Marge zwischen der Entscheidungsgrenze und den Beispielen hält, wird hingegen bei der Klassifizierung künftiger, nicht gesicherter Daten wahrscheinlich erfolgreicher sein.

```{figure} ../img/datascience/margin-bound.png
:alt: marginbound
:name: margin-bound

Trainingsset von Punkten mit binären Etiketten (+1, -1) im zweidimensionalen Spielraum $(x_1, x_2)$. Jede Entscheidungsgrenze innerhalb der gestrichelten Graulinien kann die Daten richtig teilen.
```

### Optimierungsproblem
Erinnern Sie sich, dass unser Ziel ist, einen linearen Klassifikator zu finden, der die Entfernungen zwischen der Entscheidungsgrenze und den Trainingspunkten (margin linear Klassifikator) maximiert, aber auch den Trainingsfehler minimiert. Dies stellt also ein Optimierungsproblem dar, das diesen beiden Faktoren entgegenwirken muss, die wir als:

* Die Margen (Abstände zwischen der Entscheidungsgrenze und den Trainingspunkten) sollten maximiert werden.
* Der Trainingsfehler sollte minimiert werden. Wir werden dies im Sinne von *Hintergrundverlust* ausdrücken.


### Margengrenzen
Zuvor sahen wir, dass die Gleichung, die eine Entscheidungsgrenze definiert, $\theta \cdot X + \theta_0 =0$ genügt.

```{note}
Beachten Sie, dass laut $\theta \cdot X + \theta_0 =0$ jeder Punkt, der genau am Flugzeug lebt, falsch eingestuft werden würde.
```

Wir können jetzt parallele Margengrenzen definieren (gestrichelt in der vorherigen Abbildung) als:

  $$
	\theta \cdot X + \theta_0 = \pm 1
  $$

Beachten Sie, dass wir die Grenzen so definieren können, weil wir einen Grad an Freiheit in unserer Definition der Entscheidungsgrenze haben, nämlich die Größe des normalen Vektors $\| \theta \|$. Das ist, unabhängig vom Wert $\| \theta \|$, unsere Entscheidungsgrenze bleibt unverändert.


Rufen Sie das Problem der Berechnung der [kleinsten Entfernung eines Punktes an eine plan](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane). Diese Entfernung ist:

  $$
	\frac{\theta \cdot x^{(i)} + \theta_0 }{\| \theta \|}
  $$

Wir können nun den unterschriebenen Abstand zwischen der Entscheidungsgrenze und dem i-ten Beispiel berechnen:

  $$
	\gamma_i (\theta, \theta_0) = \frac{\theta \cdot x^{(i)} + \theta_0 }{\| \theta \|}
  $$

Somit ist der Abstand zwischen den Randgrenzen und der Entscheidungsgrenze:

  $$
	\gamma_i (\theta, \theta_0) = \frac{1}{\| \theta \|}
  $$


### Hinfälliger Verlust

Bisher wissen wir, dass $sign(\theta \cdot x^{(i)} + \theta_0 )$ das i-te Beispiel klassifiziert. Der Weg zu wissen, ob die Klassifikation mit dem Label einverstanden ist, indem es von $y^{(i)}$ multipliziert. Wir können diese Vereinbarung auch in einer leicht modifizierten Version mit dem Scharnierverlust ausdrücken:

  $$
	Loss_h(z)= \begin{cases} = 0 \;\; \mbox{if} \;\; z \geq 1 \\ =1-z \;\; \mbox{if} \;\;< 1\end{cases}
  $$

wobei $z$ die Vereinbarung ist (bezeichnete Entfernung von der Entscheidungsgrenze) $y^{(i)}(\theta \cdot x^{(i)}+\theta_0)$.

Die Abbildung unten zeigt, wie der Scharnierverlust entlang der z-Achse (Abstand von Grenze) funktioniert, wie in [dieses ResearchGate Publikation](https://www.researchgate.net/publication/341468721):

<img src="../img/datascience/hinge-loss.png" alt="hinge-loss-function" class="bg-primary mb-1" width="400px">


### Zielfunktion

So können wir jetzt eine objektive Funktion schaffen, die (1) den durchschnittlichen Scharnierverlust über die Trainingsbeispiele minimiert und (2) maximiert $\frac{1}{\| \theta \|}$. Expression (2) kann auch auf eine Minimierung $\frac{1}{2}\| \theta \|^2$ zu reformieren. So definieren wir die Zielfunktion als:

  $$
	C(\theta, \theta_0) = \frac{1}{n}\sum_{i=1}^n Loss_h(y^{(i)}(\theta \cdot x^{(i)}+\theta_0)) + \frac{\lambda}{2} \| \theta \|^2
  $$
  
wobei $\lambda$ der Regelparameter ist, der die Bedeutung der Minimierung des Regelungsterms $\frac{\lambda}{2}\| \theta \|^2$ zu den Kosten für die Einbindung von mehr Verlusten (Erhöhung der Verlustdauer) ausgleicht. Je kleiner der Wert von $\lambda$ ist, desto mehr betonen wir, den durchschnittlichen Verlust zu minimieren.

```{note}
Bei der Optimierung ist das Ziel in der Regel, die Zielfunktion zu minimieren, und dies ist auch die etablierte Konvention in ML, obwohl Maximierung auch in bestimmten Fällen ein gültiges Ziel sein kann.
```


 
`````{admonition} Exercise 3: Understanding the influence of $\lambda$
:class: tip
Versuchen Sie, den Einfluss des $\lambda$ Parameters auf die Randgrenzen und die Entscheidungsgrenze piktorial zu verstehen. Welche der nachstehenden Felder mit optimierten Randgrenzen entsprechen am ehesten einem $\lambda = 1, 10, \mbox{and} \;1000$

````{figure} ../img/datascience/exercise-lambda.png
:alt: lambdainfluence
:name: lambda-influence

Wirkung des Regelparameters $\lambda$ auf die Optimierungslösung.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 3.
:header-rows: 1
:name: tab-ml-ex1-solution3

* - Grundstück
  - eine
  - B.
  - c)
* - Lambda Wert
  - 1
  - 10.
  - ANHANG

```
````
`````
 
 
 
 
 