---
description: Einführung in lineare statistische Modelle zur Vorhersage und Erklärung hydrologischer Variablen, die einfache und multiple lineare Regression und deren Annahmen abdecken.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(linearmodels)=

# Lineare Modelle

Lineare Modelle sind eine Klasse von statistischen Modellen, die darauf abzielen, eine lineare Beziehung zwischen einer abhängigen Variablen und einer oder mehreren unabhängigen Variablen herzustellen. Diese Modelle gehen davon aus, dass die Beziehung zwischen den Variablen durch eine Gerade in einem mehrdimensionalen Raum dargestellt werden kann.

In einem einfachen linearen Regressionsmodell gibt es nur eine unabhängige Variable, während es in mehreren linearen Regressionsmodellen mehrere unabhängige Variablen gibt. Die abhängige Variable, auch Zielvariable oder Antwortvariable genannt, ist die Variable, die wir basierend auf den unabhängigen Variablen vorhersagen oder erklären möchten.

Linear models have several advantages. They are relatively simple to understand and interpret, and they provide insights into the relationships between variables. Additionally, linear models are computationally efficient and can be applied to large datasets. However, linear models assume a linear relationship between variables, which may not hold true in all cases. We will cover this in detail in the section about structural and estimation errors in {ref}`linearregression`. Thus, if the relationship is nonlinear, alternative modeling techniques may be more appropriate.