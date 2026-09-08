---
description: Überwachte künstliche neuronale Netze für wissenschaftliche Computer, die die Ausbreitung von Vorwärts- und Rückwärtsbewegungen, Gewichtsoptimierung und scikit-learn-Implementierungen für Vorhersagen von Wasserressourcen abdecken.
---

```{admonition} Contributor
:class: tip
This chapter is being written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(neuralnetworks)=
# Neuronale Netze (überwacht)


Der Trainingsprozess von künstlichen neuronalen Netzen besteht nicht nur darin, die besten Merkmalsdarstellungen für unsere Daten zu finden, sondern auch die Modellparameter (Gewichte) zu einer korrekten Klassifizierung zu optimieren.

[Scikit-learn reference](https://scikit-learn.org/stable/modules/neural_networks_supervised.html).]

## Vorwärtsausbreitung


Vorwärtsausbreitung ist der Prozess, der ...

Wir addieren den Output der vorherigen Schicht multipliziert mit dem Gewicht jedes Drahtes. Backpropagation funktioniert, indem die partiellen Ableitungen der Kostenfunktion in Bezug auf jedes Gewicht oder Bias-Begriffe verwendet werden, um Signalaktualisierungen von der Ausgabeschicht zur Eingabeschicht (also rückwärts) zu übertragen.
