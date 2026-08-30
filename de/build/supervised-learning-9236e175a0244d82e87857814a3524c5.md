---
description: Überwachte Machine-Learning-Konzepte für Wasserressourcenanwendungen, die Perceptron, SVM, Entscheidungsbäume, neuronale Netze, Trainings- / Testaufteilungen und Hypothesenraumoptimierung abdecken.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(supervisedlearning)=

# Beaufsichtigtes Lernen

Bestehende ML-Algorithmen sind vielfältig und ihre Anwendbarkeit hängt von der zu erlernenden Zielaufgabe (oder *Mapping*) ab. Perceptron, Support Vector Machine, Pegasos, Decision Trees, Random Forests, Neural Networks sind Beispiele für ML-Algorithmen, die einem *überwachten Lernansatz folgen, der im Mittelpunkt dieses Abschnitts steht. Dieser Abschnitt hat folgende Ziele:

* Das Gesamtkonzept des maschinellen Lernens verstehen
* Verstehen Sie Elemente des überwachten Lernens

## Elemente des überwachten Lernens

Beim überwachten Lernen erhalten wir Beispiele (d.h. Messungen) zusammen mit der Ziellösung (d.h. Labels), von denen wir möchten, dass das ML-Modell lernt, wie man sie abbildet. Im Gegensatz dazu werden uns bei unüberwachten Lernproblemen Beispiele gegeben, aber wir kennen die Ziellösung oder *labels * nicht. Ein typisches Beispiel für ein unüberwachtes Lernproblem ist das Clustering.

### Schulung und Tests
Ziel eines ML-Algorithmus nach einem überwachten Lernansatz ist es, anhand von *Training*-Beispielen herauszufinden, wie die Ziellösung reproduziert werden kann. Ein ML-Modell ist also eine Funktion, die die Ziellösung aus dem Parametersatz der Beispiele abbildet. Wir beginnen mit der Hypothese einer Reihe von möglichen Mappern (oder Funktionen), die eine Reihe von Parametern (oder *Features*) als Argumente / Eingabe verwenden, um die Ziellösungen zu erhalten. Den *Hypotheseraum* definieren wir somit als die Menge möglicher Modelle (Klassifikatoren, Regressoren). Der Algorithmus automatisiert dann den Prozess des Findens der besten *Modellparameter * (d.h. des besten Modells), die mit den Beispiel-Label-Paaren übereinstimmen. Dies geschieht durch die Optimierung des Modells an den Händen eines Trainingsdatensatzes ($S$).

Das Ziel unserer Maschine ist es, eine In-to-Output-Regel zu finden, die durch eine mathematische Funktion $F(x)$ notiert wird, so dass:

  $$
	F(x) \rightarrow y
  $$
  
Dabei sind $x$ unsere Attribute, auch bekannt als *features*, $y$ sind die Datensatz-Labels, die Zielwerte, die wir abbilden wollen.

Our task is to find the best hypothesis (or best model) $h_{best}$ among the set of hypotheses $\mathcal{H}$. We do this by updating our hypothesis every time we loop through a selected number of training examples, thus computing an improved hypothesis $h_{t+1}$ from our current hypothesis $h_t$. Intuitively, if $h_t$ misclassifies a particular training pair $(x_i, y_i) \in S $(training dataset), then we would like $h_{t+1}$ to be like $h_t$ but nudged toward accurately classifying $(x_i, y_i)$. To make $h_t$ less bad on a training example $(x_i, y_i)$, we will nudge $h_t$ in a tiny bit along the negative of the derivative of the optimization function ($\nabla C_t$). Such optimization method is called Gradient Descent (GD), because we use the gradient of the optimization function to update our hypothesis toward a better version. 

So würde das Update aussehen:

  $$
	\vec{h_{t+1}} = \vec{h_t} - \eta_t \cdot \nabla C_t 
  $$

Dabei ist $\eta_t$ die sogenannte *Lernrate*.

Beachten Sie, dass die Hypothese (Modell) hier ein Vektor von Modellparametern ist (nicht zu verwechseln mit Merkmalen), die für einige *ML-Algorithmen * auch als Gewichte bezeichnet werden.

### Optimierungsfunktion: Verlust- und Regularisierungsbegriffe

The process of improving our hypothesis (or model) consists of an optimization problem, where we wish to minimize an optimization function ($C$). Intuitively, we would like to minimize discrepancies between predicted and actual values of $y$. These discrepancies are expressed in terms of a *loss function* that quantifies how well our model performed at a given example pair. At the same time, we do not wish that our model minimizes so much the loss function, and thus is so fitted to the training data, to the point that it is not applicable to a brand new dataset anymore. For this reason, we introduce a regularization term that aims at minimizing the complexity of the model. Finally, our optimization function would be:


  $$
	C(h_t) = \sum_{i}^{n} Loss_i + Regularizer 
  $$
  
	
wobei $n$ die Anzahl der Trainingsbeispiele ist.

Es gibt einige Gründe, warum wir unser Modell nicht an den Trainingsdatensatz anpassen möchten. Erstens kann unser Trainingsdatensatz statistisches Rauschen enthalten, das wir mit unserem Klassifikator nicht erfassen möchten. Die folgende Abbildung veranschaulicht das Konzept:

![Overfitting in ML](https://elitedatascience.com/wp-content/uploads/2017/09/Overfitting-Data-Points.png)

In der Abbildung sehen wir deutlich, dass die grüne Linie zu den Trainingsdatenpunkten, die durch zwei Klassen (blaue und rote Punkte) gekennzeichnet sind, überpasst ist. Die schwarze Linie ist wahrscheinlich eine zufriedenstellende Entscheidungsgrenze, um die roten und blauen Punkte zu teilen.

Der zweite Grund, warum wir unser Modell nicht überarbeiten wollen, ist, dass unser Ziel im Herzen der Probleme des maschinellen Lernens darin besteht, ein Modell, das aus einem Trainingsdatensatz gelernt wurde, auf die Weltdaten anwenden zu können. Daher wünschen wir, dass unser Modell * verallgemeinert * oder richtig anwendet, was gelernt wurde, um einen breiteren, unsichtbaren Datensatz. Um zu überprüfen, ob unser Modell gut funktioniert, reicht es nicht aus, den Trainingsfehler zu minimieren. Wir müssen die gelernten Parameter an einem unsichtbaren Datensatz, dem sogenannten Testing Dataset, testen.


```{admonition} Keep in mind
:class: tip

Es ist unwahrscheinlich, dass unser Modell bessere Ergebnisse beim Testen liefert als in den Trainingsdaten, aber es gibt ein ideales Szenario, das wir erreichen wollen, das heißt, sowohl den Trainings- als auch den Testfehler zu minimieren. Wir werden dieses Thema im Abschnitt über *Cross-Validierung * behandeln.
```


### Klassifizierung und Regression

Im weiteren Sinne kann ein ML-Modell trainiert werden, um zu lernen, wie man Kategorien oder kontinuierliche Werte vorhersagt. In diesen beiden Ansätzen werden wir die obigen Konzepte verwenden, um einen *Klassifikator* bzw. einen *Regressor* zu erstellen. Der Hauptunterschied liegt in der Art und Weise, wie wir den * Trainingsfehler * oder * Verlust * berechnen. In den nächsten Abschnitten werden wir beide Probleme aus einer Perspektive des überwachten Lernens behandeln.