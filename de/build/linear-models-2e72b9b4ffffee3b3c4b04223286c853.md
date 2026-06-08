---
description: Einführung in lineare statistische Modelle zur Vorhersage und Erläuterung von hydrologischen Variablen, die einfache und mehrfache lineare Regression und deren Annahmen abdecken.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearmodels)=

# Lineare Modelle

Linearmodelle sind eine Klasse von statistischen Modellen, die eine lineare Beziehung zwischen einer abhängigen Variablen und einer oder mehreren unabhängigen Variablen aufbauen wollen. Diese Modelle gehen davon aus, dass der Zusammenhang zwischen den Größen durch eine Gerade in einem mehrdimensionalen Raum dargestellt werden kann.

Bei einem einfachen linearen Regressionsmodell gibt es nur eine unabhängige Variable, während bei mehreren linearen Regressionsmodellen mehrere unabhängige Variablen vorhanden sind. Die abhängige Variable, auch die Zielvariable oder Antwortvariable genannt, ist die Variable, die wir anhand der unabhängigen Variablen vorhersagen oder erklären möchten.

Linearmodelle haben mehrere Vorteile. Sie sind relativ einfach zu verstehen und zu interpretieren, und sie geben Einblicke in die Zusammenhänge zwischen Variablen. Zusätzlich sind lineare Modelle rechnerisch effizient und können auf große Datensätze angewendet werden. Lineare Modelle nehmen jedoch einen linearen Zusammenhang zwischen Variablen ein, der in allen Fällen nicht wahr ist. Wir werden dies im Detail im Abschnitt über Struktur- und Schätzfehler in {ref}`linearregression` behandeln. Wenn also die Beziehung nicht linear ist, können alternative Modellierungstechniken sinnvoller sein.