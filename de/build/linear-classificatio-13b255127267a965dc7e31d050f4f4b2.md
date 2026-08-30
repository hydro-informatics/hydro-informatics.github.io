---
description: Lineare Klassifikationsgrundlagen mit dem Perceptron-Algorithmus und Margin-Klassifikatoren mit Regularisierung für maschinelle Lernanwendungen in der Wasserressourcentechnik.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearclassification)=
# Lineare Klassifizierung

In diesem Abschnitt werden wir die Grundlagen der linearen Klassifizierung durch einen einfachen ML-Algorithmus, das Perceptron, behandeln. Darüber hinaus werden wir die Konzepte hinter dem Perceptron-Algorithmus erweitern, indem wir Aspekte der *Regularisierung * berücksichtigen, um einen linearen Margin-Klassifikator zu erstellen.

```{admonition} Requirements
:class: warning
* Sie kennen Begriffe des maschinellen Lernens. Wir empfehlen, unseren [Einführung in ML](https://hydro-informatics.com/datascience/machinelearning.html)] Abschnitt zu lesen, um sich mit der Nomenklatur vertraut zu machen, die wir auf der gesamten Website verwenden.
* Sie kennen grundlegende lineare Algebra-Konzepte (wie ein Punktprodukt, Vektorprojektionen, Ebenen, Eigenvektoren und Eigenwerte). Bitte beachten Sie die Videos von [3Blue1Brown](https://youtu.be/kjBOesZCoqc) für eine geeignete Überarbeitung, falls erforderlich].
* Grundkenntnisse in Python und Array Computing mit NumPy.
```


## Hyperflugzeuge

Angenommen, wir möchten positive und negative Objekte aus dem Trainingssatz unten klassifizieren (Abbildung links):

```{figure} ../img/datascience/decision-boundary.png
:alt: decisionbound
:name: cloud-points-ml

Training set of points with binary labels (+1, -1) and two-dimensional $(x_1, x_2)$ features. The decision boundary (grey line) is defined by the parameter vector $\theta$, which is normal to the decision boundary, and offset parameter $\theta_0$ that linearly separates the data.
```

Der obige Datensatz wird als linear trennbar angesehen, da er mindestens eine lineare Entscheidungsgrenze existiert, die in der Lage ist, den gesamten Datensatz korrekt aufzuteilen. Zum Beispiel könnten wir eine Entscheidungsgrenze wie die graue Linie oben (Abbildung rechts) überschreiten.


In this case, since the features $(x_1, x_2) \in \mathbb{R}^2 $, that is, the feature set belongs to the two-dimensional space, the decision boundary constitutes a line. If we were dealing with a set of features in the three-dimensional space $(x_1, x_2, x_3)$, the decision boundary would be a plane. Analogously, if our feature set were in a higher-dimensional space, the decision boundary would constitute a *hyperplane*.


A hyperplane with $d$ dimensions is conventionally denoted by the vector normal to the plane, $\theta \in \mathbb{R}^d$, and offset (scalar) parameter $\theta_0$. In the example above, we would define the hyperplane (or decision boundary) as:

  $$
	\theta \cdot X + \theta_0 =0 \equiv \begin{bmatrix} \theta_1 & \theta_2 \end{bmatrix} \cdot \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} + \theta_0 = 0
  $$


```{note}
 Note that $\theta$ controls the orientation (slope, or inclination) of the boundary, whereas $\theta_0$ controls the location (or offset, or bias) of the boundary. Thus, if $\theta_0 = 0$, then the decision boundary crosses the origin. $\theta_0$ is also often called the *bias term*.
```
 
Unser Klassifikator $h(x, \theta, \theta_0)$ ist somit gleich $sign(\theta \cdot X + \theta_0)$, wobei $\theta \in \mathbb{R}^2 $ und $\theta_0 \in \mathbb{R}$. Erinnern Sie sich an die Zeichenfunktion, auch bekannt als Signum-Funktion, ist eine mathematische Funktion, die das Zeichen oder die Richtung einer reellen Zahl zurückgibt. Das heißt, wenn die Eingabenummer positiv, negativ oder 0 ist, gibt die Vorzeichenfunktion +1, -1 bzw. 0 zurück.
 
 
`````{admonition} Exercise 1
:class: tip
Versuchen Sie zu beantworten, ob das Paar von Trainingsbeispielen unten linear trennbar ist. Welche sind linear durch den Ursprung trennbar?

````{figure} ../img/datascience/exercise-decision-bound.png
:alt: ex-decision-bound
:name: exercise-db

Übung 1 über linear trennbare Beispiele.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 1.
:header-rows: 1
:name: tab-ml-ex1-solution

* - Datensatz
  - a
  - b
  - c
  - d
* - Linear trennbar (LS)?
  - Ja
  - Nein
  - Ja
  - Nein
* - LS durch Herkunft?
  - Nein
  - Nein
  - Ja
  - Nein

```
````
`````

## Perceptron-Algorithmus

In the perceptron algorithm, we typically initialize $\theta$ as zero (zero vector) and loop through the pair of training examples. At every iteration, we will check if the classifier makes a mistake classifying that training example (i-th example), and if so, then we update the parameters of $\theta$. 


Assume that $\theta_0 =0$ for simplicity (the decision boundary must pass through the origin). Our perceptron classifier will make a mistake ``if`` $y^{(i)}(\theta \cdot x^{(i)}) \leq 0$. We will then update our $\theta$ to no longer misclassify that training example. The way to do this is by adding $y^{(i)}x^{(i)}$ to the previous $\theta$. Thus, the update would look like:

  $$
	\theta = \theta + y^{(i)}x^{(i)}
  $$


````{admonition} Exercise 2: Understanding the perceptron update
:class: tip
Versuchen Sie zu verstehen, warum dieses Update nützlich ist. Tipp: Ersetzen Sie den Ausdruck für die Updates $\theta$ im ``if`` Check.

```{admonition} Solution
:class: dropdown

Substituting the expression for the updated $\theta$ to check if the classifier still makes a mistake in that example:

  $$
	y^{(i)}(\theta + y^{(i)}x^{(i)})x^{(i)}
  $$
  
We initialize $\theta$ as zero, thus the expression is simplified to:
 
  $$
    y^{(i)}(y^{(i)}x^{(i)})x^{(i)}
  $$
  
Since any label time itself is equal to one (both $1 * 1$ and $-1 * -1$ equal 1), the expression turns into:

  $$
    x^{(i)}x^{(i)} = \| x^{(i)} \|^2 > 0 
  $$
  
This means that that the expression $y^{(i)}(\theta \cdot x^{(i)}) > 0$ (no mistake). Thus, $\theta$ was updated so that it doesn't misclassify the i-th example anymore.
```
````


We have in hands a set of different training examples which have the potential to nudge/update our classifier in many directions. Thus, it is possible and even expected that the last training examples cause updates that will overwrite earlier, initial updates. This will result that earlier examples will no longer be correctly classified. For this reason, we need to loop through the whole training set multiple $T$ times to ensure that all examples are correctly classified. Such iterations can be performed both in order or randomly selected from the training examples. 

Wir können den Algorithmus wie folgt codieren:

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

## Margin-Grenzen und Scharnierverlust

Wie Sie vielleicht bemerkt haben, verfügt der Perceptron-Algorithmus über keinen Regularisierungsbegriff. Das Ziel war einfach, eine Entscheidungsgrenze zu finden, die die Daten korrekt aufteilen kann. Hier werden wir das Konzept von *Hindernisverlust * und *Margengrenzen * vorstellen, um das Problem des Erlernens einer Entscheidungsgrenze in ein Optimierungsproblem unter Berücksichtigung der Regularisierung zu verwandeln.

### Motivation hinter Margengrenzen

Werfen wir einen Blick auf unseren zuvor vorgestellten Trainingsdatensatz (Abbildung unten). Jede Entscheidungsgrenze innerhalb der gestrichelten grauen Linien teilt die Trainingsbeispiele korrekt auf. Wir möchten jedoch intuitiv eine Entscheidungsgrenze bevorzugen, die die Abstände zwischen der Entscheidungsgrenze und den Trainingspunkten maximieren kann. Der Grund dafür ist, dass die Punkte, die wir in Zukunft klassifizieren möchten, wahrscheinlich ein statistisches Rauschen haben, so dass eine Entscheidungsgrenze, die zu nahe an den Trainingsbeispielen liegt, eher leicht veränderte (lautere) Versionen der Trainingsbeispiele falsch klassifiziert. Im Gegensatz dazu wird ein Klassifikator, der eine relativ höhere Marge zwischen der Entscheidungsgrenze und den Beispielen hat, wahrscheinlich erfolgreicher bei der Klassifizierung zukünftiger, unsichtbarer Daten sein.

```{figure} ../img/datascience/margin-bound.png
:alt: marginbound
:name: margin-bound

Trainingssatz von Punkten mit binären Labels (+1, -1) im zweidimensionalen Feature Space $(x_1, x_2)$. Jede Entscheidungsgrenze innerhalb der gestrichelten grauen Linien kann die Daten korrekt aufteilen.
```

### Optimierungsproblem
Denken Sie daran, dass es unser Ziel ist, einen linearen Klassifikator zu finden, der die Abstände zwischen der Entscheidungsgrenze und den Trainingspunkten maximiert (margin linearer Klassifikator), aber auch den Trainingsfehler minimiert. Dies stellt somit ein Optimierungsproblem dar, das diese beiden Faktoren ausgleichen muss, die wir als Folgendes angeben können:

* Die Margen (Abstände zwischen der Entscheidungsgrenze und den Trainingspunkten) sollten maximiert werden.
* Der Trainingsfehler sollte minimiert werden. Wir werden dies als *Hindernisverlust * ausdrücken.


### Grenzgrenzen
Previously, we saw that the equation defining a decision boundary satisfies $\theta \cdot X + \theta_0 =0$. 

```{note}
Note that according to $\theta \cdot X + \theta_0 =0$, any point living exactly at the plane would be misclassified. 
```

Wir können nun parallele Randgrenzen (gestrichelte Linie in der vorherigen Abbildung) als definieren:

  $$
	\theta \cdot X + \theta_0 = \pm 1
  $$

Note that we can define the boundaries like this because we have a degree of freedom in our definition of the decision boundary, namely, the magnitude of the normal vector $\| \theta \|$. That is, regardless of the value $\| \theta \|$, our decision boundary remains unaltered.


Erinnern Sie sich an das Problem der Berechnung der [kleinste Abstand eines Punktes zu einem Flugzeug](https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_plane)]. Dieser Abstand beträgt:

  $$
	\frac{\theta \cdot x^{(i)} + \theta_0 }{\| \theta \|}
  $$

Wir können nun den signierten Abstand zwischen der Entscheidungsgrenze und dem i-ten Beispiel berechnen als:

  $$
	\gamma_i (\theta, \theta_0) = \frac{\theta \cdot x^{(i)} + \theta_0 }{\| \theta \|}
  $$

Der Abstand zwischen den Randgrenzen und der Entscheidungsgrenze beträgt somit:

  $$
	\gamma_i (\theta, \theta_0) = \frac{1}{\| \theta \|}
  $$


### Gelenkverlust

We so far know that $sign(\theta \cdot x^{(i)} + \theta_0 )$ will classify the i-th example. The way to know if the classification agrees with the label is by multiplying it by $y^{(i)}$. We can express this agreement also in a slightly modified version, using the hinge loss:

  $$
	Loss_h(z)= \begin{cases} = 0 \;\; \mbox{if} \;\; z \geq 1 \\ =1-z \;\; \mbox{if} \;\;< 1\end{cases}
  $$

Dabei ist $z$ die Vereinbarung (signierte Entfernung von der Entscheidungsgrenze) $y^{(i)}(\theta \cdot x^{(i)}+\theta_0)$.

Die folgende Abbildung zeigt, wie der Scharnierverlust entlang der z-Achse (Abstand von der Grenze) funktioniert, wie in [dieser ResearchGate-Publikation](https://www.researchgate.net/publication/341468721)] gezeigt:

<img src="../img/datascience/hinge-loss.png" alt="hinge-loss-function" class="bg-primary mb-1" width="400px">


### Zielfunktion

So now we can create an objective function that (1) minimizes the average hinge loss over the training examples, and (2) maximizes $\frac{1}{\| \theta \|}$. Expression (2) can be also reformulated towards minimizing $\frac{1}{2}\| \theta \|^2$. Thus we define the objective function as:

  $$
	C(\theta, \theta_0) = \frac{1}{n}\sum_{i=1}^n Loss_h(y^{(i)}(\theta \cdot x^{(i)}+\theta_0)) + \frac{\lambda}{2} \| \theta \|^2
  $$
  
where $\lambda$ is the regularization parameter that balances the importance of minimizing the regularization term $\frac{\lambda}{2}\| \theta \|^2$ at the cost of incurring more losses (increasing the loss term). Vice versa, the smaller the value of $\lambda$, the more emphasis we will give to minimizing average loss.

```{note}
Bei der Optimierung besteht das Ziel typischerweise darin, die Zielfunktion zu minimieren, und dies ist auch die etablierte Konvention in ML, obwohl das Maximieren in bestimmten Fällen auch ein gültiges Ziel sein kann.
```


 
`````{admonition} Exercise 3: Understanding the influence of $\lambda$
:class: tip
Try to understand pictorially the influence of the $\lambda$ parameter on the margin boundaries and decision boundary. Which of the plots showing optimized margin boundaries below are most likely to correspond to a $\lambda = 1, 10, \mbox{and} \;1000$

````{figure} ../img/datascience/exercise-lambda.png
:alt: lambdainfluence
:name: lambda-influence

Auswirkung des Regularisierungsparameters $\lambda$ auf die Optimierungslösung.
````

````{admonition} Solution
:class: dropdown

```{list-table} Solution to the Machine Learning Exercise 3.
:header-rows: 1
:name: tab-ml-ex1-solution3

* - Grundstück
  - a
  - b
  - c
* - Lambdawert
  - 1
  - 10
  - 1000 Tonnen

```
````
`````
 
 
 
 
 