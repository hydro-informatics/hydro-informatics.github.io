---
description: Einführung in maschinelles Lernen für die Wasserressourcenforschung, die überwachtes und unüberwachtes Lernen, ML-Algorithmen, Modelltraining und Anwendungen in Hydrologie und Flussökosystemen umfasst.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(machinelearning)=
# Einleitung

Machine Learning (ML) ist wohl eines der prominentesten Werkzeuge in der Datenwissenschaft, um die Wasserressourcenforschung voranzutreiben. ML-Modelle sind in der Lage, komplexe zugrunde liegende Beziehungen eines Systems zu erlernen und finden somit ihre Anwendungen in verschiedenen Wasserressourcenthemen: von Flussökosystemen bis zur Wasserversorgung. Wir werden eine Vielzahl von Lernalgorithmen und Methoden zur Optimierung von ML-Modellen abdecken, so dass sie auf unsichtbare Daten verallgemeinern können, die im Prinzip überwachte und unbeaufsichtigte Lerntechniken umfassen.

## Das Ziel von Machine Learning

Machine Learning zielt darauf ab, komplexe Beziehungen aus Erfahrung (d.h. Daten) rechnerisch zu lernen. *Computational Learning* ist ein Teilbereich der künstlichen Intelligenz (KI), der sich auf die Entwicklung von Modellen konzentriert, die es Computern ermöglichen, zu lernen und Vorhersagen oder Entscheidungen zu treffen, ohne explizit programmiert zu werden. Es beinhaltet das Entwerfen und Implementieren mathematischer und statistischer Modelle, die Daten automatisch analysieren, Muster identifizieren und fundierte Entscheidungen oder Vorhersagen basierend auf den beobachteten Daten treffen können. Diese Aufgabe kann beispielsweise die Vorhersage oder Modellierung komplexer Phänomene sein. Beachten Sie, dass sich die Vorhersage hier nicht nur auf die Zukunft bezieht, sondern auf jedes nicht identifizierte Ereignis. Zum Beispiel können wir vorhersagen, ob eine chemische Substanz in Wasser unter einer Reihe von Umweltbedingungen gelöst wird oder war oder ist.

Im Gegensatz zum populären Denken gibt es ML-Algorithmen seit mehreren Jahrzehnten. Sie wurden jedoch erst in den letzten zehn Jahren stark beachtet, als Einschränkungen der Rechenleistung kein Hindernis mehr für die Anwendung von ML * Algorithmen * für die Erstellung hilfreicher * ML-Modelle * waren. Wir beziehen uns auf *Algorithmen* als Basisbefehle, die ein Modell *anweisen, wie man aus Daten lernt*, während ein *ML-Modell* das Ergebnis (dh das gelernte Programm) des Lernens der Zielaufgabe aus dem ausgewählten Regelsatz (*ML-Algorithmus*) und Beispielen (dh Daten) ist.

## Arten des maschinellen Lernens

In diesem Abschnitt haben wir uns hauptsächlich mit grundlegenden Elementen des überwachten Lernens befasst, aber beachten Sie, dass es mehrere andere Arten von ML-Problemen gibt. Einige davon sind:
* Unüberwachtes Lernen: Wir geben kein korrektes Verhalten an (z. B. Etiketten). Hier haben wir einige Beobachtungen, aber die Aufgabe selbst ist nicht gut definiert.
* Semi-überwachtes Lernen: Wir können einige Teile unseres Modells mit einigen Etiketten angeben, aber andere Teile müssen ohne explizite Ziele gelernt werden. Zum Beispiel können wir unüberwachtes Lernen verwenden, um Cluster zu erhalten, die Merkmale für ein überwachtes Lernproblem definieren.
* Aktives Lernen: Der Algorithmus selbst kann nach zusätzlichen, nützlichen Beispielen fragen. Lernen Sie zum Beispiel, nur Beispiele auszuwählen, die tatsächlich zum Lernen benötigt werden.
* Transfer Learning: Wenn eine Methode für ein individuelles Szenario trainiert wird und Sie sie in einem anderen Szenario verwenden möchten. Dies bedeutet: Wie kann man das nutzen, was von A on B gelernt wurde?
* Verstärkungslernen: Das Modell ist darauf trainiert, zu handeln, anstatt nur vorherzusagen, und der Algorithmus selbst verwendet Ergebnisse seiner experimentierten Handlungen als Feedback oder *Verstärkung*, um ein optimiertes Ergebnis von Aktionen zu erzielen (z. B. ein Roboter, der laufen lernt).

(data-science)=
## Unterschied zwischen Machine Learning und Data Science

Der konzeptionelle Unterschied zwischen Data Science und Machine Learning lässt sich ähnlich dem Konzept von Rechtecken und Quadraten in der Geometrie vorstellen, wobei Data Science *Rechtecken * und Machine Learning * Quadraten * entspricht. Sowohl Data Science als auch Machine Learning befassen sich mit Programmierung (z. B. in Python, R oder SQL), Statistiken und Datenmodellierung. Data Science umfasst auch Datenvisualisierung und Datenwrangling.

```{admonition} Recommended course
:class: tip

Denken Sie daran, nach Materialien zu suchen und unabhängig für Ihr optimales Lernen zu lernen. Zum Beispiel empfehlen wir dringend den umfassenden [Maschinenlernkurs](https://www.edx.org/course/machine-learning-with-python-from-linear-models-to), angeboten von MITx, der Online-Lerninitiative des Massachusetts Institute of Technology].
```

