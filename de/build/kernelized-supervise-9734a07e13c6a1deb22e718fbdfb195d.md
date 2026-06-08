---
description: Nichtlineare Klassifikation mit Kernel-Methoden und Support Vector Machines (SVM) im maschinellen Lernen, Abdeckung von Features Transformation und Kerneltricks für komplexe Entscheidungsgrenzen.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(nonlinearclassification)=
# Kernmaterial
 
In diesem Abschnitt werden wir grundlegende Konzepte der nichtlinearen Klassifizierung durch die Einführung des Konzepts von Kerneln abdecken. Lassen Sie uns zunächst daran erinnern, was wir bisher in unserem Abschnitt über {ref}`linearclassification` gesehen haben. In der linearen Klassifikation bestand unsere Aufgabe darin, Datenpunkte durch ein Hyperplan zu klassifizieren, das den Datensatz in den Merkmalen den Koordinatenraum linear trennen könnte. Zum Beispiel in einem 3d-Funktionsraum, also einem Merkmalsvektor wie $(x_1, x_2, x_3) \in \mathbb{R}^3 $, erinnern Sie daran, dass unsere Daten als linear trennbar angesehen werden, wenn es mindestens eine Ebene (nicht Zeile), die die Punkte teilen kann. Im Gegensatz zur linearen Klassifizierung, die eine lineare Beziehung zwischen Eingabemerkmalen und Klassenetiketten einnimmt, verwenden nichtlineare Klassifizierungsalgorithmen verschiedene Techniken, um komplexe Muster und Entscheidungsgrenzen in den Daten zu erfassen. Insbesondere werden wir uns anschauen, wie wir unsere Daten durch *Kernels* in einen neuen Koordinatenraum höherer Dimension transformieren können, der uns dabei hilft, das nichtlineare Problem in einen linearen zu verwandeln.
 
Kernels ermöglichen es uns, Daten in einen überdimensionalen Funktionsraum zu transformieren, in dem eine lineare Trennung möglich wird. Ein Beispiel für den ML-Algorithmus, der auf Kernel basiert, um komplexe Muster und Entscheidungsgrenzen in den Daten zu finden, ist Support Vector Machine (SVM).


```{note}
Andere nichtlineare Klassifizierungsalgorithmen umfassen Entscheidungsbäume, zufällige Wälder, k-nächste Nachbarn (KN), und neuronale Netzwerke. Diese Algorithmen verwenden unterschiedliche Techniken von der Kernelisierung bis zur Modellierung und Erfassung nichtlinearer Zusammenhänge zwischen Eingabemerkmalen und Klassenetiketten, so dass sie komplexe Klassifizierungsaufgaben bewältigen können.
```

## Eigenschaften

Wir werden nun sehen, wie Feature-Transformation über ein Beispiel funktioniert, d.h. wir haben eine Funktion $x \in \mathbb{R}$. Die nachstehende Abbildung zeigt die Ausbildungspunkte ($n=3$).

Beachten Sie aus der Figur, dass der Datensatz nicht linear trennbar ist, zumindest nicht in dem angegebenen Merkmalsraum in 1 Dimension. Um dieses Problem zu einem linearen Problem zu machen, können wir eine Feature-Transformation ($\phi (x)$) durchführen, um eine Entscheidungsgrenze in einem überdimensionalen Raum zu suchen. In diesem speziellen Beispiel sei darauf hingewiesen, dass wir das 1d-Feature in einen neuen 2d-Featurevektor transformieren können, wo die zusätzliche Dimension als eine Art neues Feature angesehen werden kann.

  $$
    x \to \Phi(x) = [\Phi_1 \; \; \; \Phi_2] = [x \; \; \; x^2]
  $$

`````{tab-set}
````{tab-item} Original feature space 
```{figure} ../img/datascience/feat-transform-1.JPG
:height: 400px
:alt: initial problem before feature transformation
:name: feat-transform-1

1: Trainingsdaten im ersten Funktionsraum.
```
````

````{tab-item} New feature space
```{figure} ../img/datascience/feat-transform-2.JPG
:height: 400px
:alt: problem after feature transformation
:name: feat-transform-2
:class: with-shadow

2: Trainingsdatensatz im neuen Feature-Bereich $\Phi(x)$.
```
````

````{tab-item} Decision boundary in the new feature space
```{figure} ../img/datascience/feat-transform-3.JPG
:height: 400px
:alt: decision boundary linearly separating the dataset in the new feature space
:name: feat-transform-3

3: Trainingsdatensatz und Entscheidungsgrenzen im neuen Feature-Bereich $\Phi(x)$
```
````
`````

Durch die Ausführung der Feature-Transformation, wie in Schritt 2: Trainingsdatensatz im neuen Feature-Bereich $\Phi(x)$ (siehe Abbildung oben) dargestellt, finden wir einen Klassifikator $h(x, \theta, \theta_o)$ mit einer Entscheidungsgrenze von $\theta$ und den Offset-Parameter $\theta_0$:

  $$
    h (x, \theta, \theta_0) = sign(\theta \cdot \Phi(x) + \theta_0)\\
	\therefore h (x, \theta, \theta_0) = sign(\theta_1 x + \theta_2 x^2 + \theta_0)
  $$


`````{admonition} Exercise 1: Feature transformation with kernels
:class: tip
Die folgende Abbildung zeigt einen Datensatz, der im Original-Featureraum $x = [x_1, x_2]$ nicht linear trennbar ist. Können Sie an eine Kernelfunktion denken, um einen überdimensionalen Funktionsraum zu schaffen, in dem eine Entscheidungsgrenze durch lineare Klassifikation auflösbar ist?

````{figure} ../img/datascience/exercise-1-kernels.jpg
:height: 400px
:alt: ex-kernels-1
:name: exercise-kernels-1

Übung 1 auf Kernel
````

````{admonition} Hint
:class: dropdown, important
Hinweis: Die Punkte sind durch einen Umfang im Original-Funktionsraum $x \in \mathbb{R}^2$ deutlich trennbar. Jetzt versuchen Sie, einen Kernelized-Funktionsraum $\Phi \in \mathbb{R}^3$ zu zeichnen.
````

````{admonition} Solution
:class: dropdown

Wir beginnen, dieses Problem zu lösen, indem wir die Gleichung eines nicht im Ursprung zentrierten Umfangs erinnern:

  $$
    (x_1+a)^2+(x_2+b)^2 = c
  $$
Erweitern der obigen Gleichung erhalten wir:

  $$
    x_1^2 + 2 a x_1 + a^2 + x_2^2 + 2 b x_2 + b^2 -c = 0 \\
  $$
  
Die Begriffe $a$, $b$ und $c$ sind Konstanten, so können wir die Gleichung vereinfachen:

  $$
    2 a x_1 + 2 b x_2 + x_1^2 + x_2^2 + C = 0 \\
  $$
wo $C = (a^2 + b^2 - c)$.

Beachten Sie, dass die obige Gleichung unsere nichtlineare Entscheidungsgrenze im Original-Featureraum $x \in \mathbb{R}^2$ bedeutet und somit den Ausdruck $\theta \cdot \Phi(x) +\theta_0$:

  $$
    \theta \cdot \Phi(x) + \theta_0 = x_1^2 + 2 a x_1 + x_2^2 + 2 b x_2  + C
  $$
  
Das bedeutet, dass $\theta_0 = C$, $\Phi(x) = [x_1 \;\; x_2 \;\; x_1^2 \;\; x_2^2]$, und so finden wir auch $\theta$ in Bezug auf die Umfangparameter:

  $$
    \theta = [2a \;\; 2b \;\; 1 \;\; 1]
  $$

````
`````

## Mehr kommen bald...



