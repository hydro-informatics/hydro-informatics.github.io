---
description: Nichtlineare Klassifizierung mit Kernel-Methoden und Support Vector Machines (SVM) im maschinellen Lernen, die Feature-Transformation und Kernel-Tricks für komplexe Entscheidungsgrenzen abdeckt.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(nonlinearclassification)=
# Kerne
 
In this section, we will cover fundamental concepts of non-linear classification by introducing the concept of kernels. First, let us recall what we have seen so far in our section about {ref}`linearclassification`. In linear classification, our task consisted of classifying data points through a hyperplane that could linearly separate the dataset in the features coordinate space. For instance, in a 3d feature space, thus a feature vector such as $(x_1, x_2, x_3) \in \mathbb{R}^3 $, recall that our data is considered linearly separable if there is at least one plane (not line) who can split the points. Unlike linear classification, which assumes a linear relationship between input features and class labels, non-linear classification algorithms use various techniques to capture complex patterns and decision boundaries in the data. In particular, we will look at how we can transform our data into a new coordinate space of higher dimension through *kernels*, which help us turning the non-linear problem into a linear one.
 
Kernel ermöglichen es uns, Daten in einen höherdimensionalen Merkmalsraum zu transformieren, in dem eine lineare Trennung möglich wird. Ein Beispiel für einen ML-Algorithmus, der auf Kernel angewiesen ist, um komplexe Muster und Entscheidungsgrenzen in den Daten zu finden, ist Support Vector Machine (SVM).


```{note}
Andere nichtlineare Klassifizierungsalgorithmen umfassen Entscheidungsbäume, zufällige Wälder, k-nächste Nachbarn (KNN) und neuronale Netze. Diese Algorithmen verwenden verschiedene Techniken, die sich von der Kernelisierung unterscheiden, um nichtlineare Beziehungen zwischen Eingabemerkmalen und Klassenetiketten zu modellieren und zu erfassen, so dass sie komplexe Klassifizierungsaufgaben bewältigen können.
```

## Merkmalstransformation

We will now see how feature transformation works through a 1d example, that is, we have one feature $x \in \mathbb{R}$. The figure below illustrates the training points ($n=3$).

Beachten Sie aus der Abbildung, dass der Datensatz nicht linear trennbar ist, zumindest nicht im angegebenen Merkmalsraum in 1 Dimension. Um dieses Problem in ein lineares Problem zu verwandeln, können wir eine Merkmalstransformation ($\phi (x)$) durchführen, um nach einer Entscheidungsgrenze in einem höherdimensionalen Raum zu suchen. Beachten Sie in diesem Beispiel, dass wir das 1D-Feature in einen neuen 2D-Feature-Vektor umwandeln können, wobei die zusätzliche Dimension als eine Art neues Feature angesehen werden kann.

  $$
    x \to \Phi(x) = [\Phi_1 \; \; \; \Phi_2] = [x \; \; \; x^2]
  $$

`````{tab-set}
````{tab-item} Original feature space 
```{figure} ../img/datascience/feat-transform-1.JPG
:height: 400px
:alt: initial problem before feature transformation
:name: feat-transform-1

1: Trainingsdaten im ersten Feature Space.
```
````

````{tab-item} New feature space
```{figure} ../img/datascience/feat-transform-2.JPG
:height: 400px
:alt: problem after feature transformation
:name: feat-transform-2
:class: with-shadow

2: Trainingsdatensatz im neuen Feature Space $\Phi(x)$.
```
````

````{tab-item} Decision boundary in the new feature space
```{figure} ../img/datascience/feat-transform-3.JPG
:height: 400px
:alt: decision boundary linearly separating the dataset in the new feature space
:name: feat-transform-3

3: Trainingsdatensatz und Entscheidungsgrenze im neuen Feature Space $\Phi(x)$
```
````
`````

By performing feature transformation as illustrated in the step 2: training dataset in the new feature space $\Phi(x)$ (see figure above), we can find a classifier $h(x, \theta, \theta_o)$ with a decision boundary defined by $\theta$ and the offset parameter $\theta_0$:

  $$
    h (x, \theta, \theta_0) = sign(\theta \cdot \Phi(x) + \theta_0)\\
	\therefore h (x, \theta, \theta_0) = sign(\theta_1 x + \theta_2 x^2 + \theta_0)
  $$


`````{admonition} Exercise 1: Feature transformation with kernels
:class: tip
The figure below shows a dataset that is not linearly separable in the original feature space $x = [x_1, x_2]$. Can you think of a kernel function to create a higher-dimensional feature space where there is a decision boundary solvable through linear classification?

````{figure} ../img/datascience/exercise-1-kernels.jpg
:height: 400px
:alt: ex-kernels-1
:name: exercise-kernels-1

Übung 1 zu Kernel
````

````{admonition} Hint
:class: dropdown, important
Hint: The points are clearly separable by a circumference in the original feature space $x \in \mathbb{R}^2$. Now try to draw a kernelized feature space $\Phi \in \mathbb{R}^3$.
````

````{admonition} Solution
:class: dropdown

Wir fangen an, dieses Problem zu lösen, indem wir uns an die Gleichung eines Umfangs erinnern, der nicht im Ursprung zentriert ist:

  $$
    (x_1+a)^2+(x_2+b)^2 = c
  $$
Erweiterung der obigen Gleichung erhalten wir:

  $$
    x_1^2 + 2 a x_1 + a^2 + x_2^2 + 2 b x_2 + b^2 -c = 0 \\
  $$
  
Die Begriffe $a$, $b$ und $c$ sind Konstanten, so dass wir die Gleichung vereinfachen können:

  $$
    2 a x_1 + 2 b x_2 + x_1^2 + x_2^2 + C = 0 \\
  $$
Wobei $C = (a^2 + b^2 - c)$.

Note that the above equation denotes our non-linear decision boundary in the original feature space $x \in \mathbb{R}^2$ and thus should equal the expression $\theta \cdot \Phi(x) +\theta_0$:

  $$
    \theta \cdot \Phi(x) + \theta_0 = x_1^2 + 2 a x_1 + x_2^2 + 2 b x_2  + C
  $$
  
which means that $\theta_0 = C$, $\Phi(x) = [x_1 \;\; x_2 \;\; x_1^2 \;\; x_2^2]$, and thus we can also find $\theta$ in terms of the circumference parameters:

  $$
    \theta = [2a \;\; 2b \;\; 1 \;\; 1]
  $$

````
`````

## Mehr kommt bald...



