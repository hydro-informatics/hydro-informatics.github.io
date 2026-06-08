---
description: Einführung in das maschinelle Lernen für die Wasserressourcenforschung, die beaufsichtigtes und ununterbrochenes Lernen, ML-Algorithmen, Modellbildung und Anwendungen in der Hydrologie und Flussökosysteme abdeckt.
---

```{admonition} Contributor
:class: tip
This chapter was written and developed by [Beatriz Negreiros](https://beatriznegreiros.com/) <img src="../img/authors/beatriz.jpg" alt="Beatriz Negreiros" width="50" height="50">
```

(machinelearning)=
# Einleitung

Machine Learning (ML) ist wahrscheinlich eines der prominentesten Tools in der Datenwissenschaft, um die Wasserressourcenforschung voranzutreiben. ML-Modelle sind in der Lage, komplexe zugrunde liegende Zusammenhänge eines Systems zu erlernen und finden so ihre Anwendungen in verschiedenen Wasserressourcenthemen: von Flussökosystemen bis zur Wasserversorgung. Wir werden eine Vielzahl von Lernalgorithmen und -methoden abdecken, um ML-Modelle zu optimieren, damit sie sich auf ungesehene Daten verallgemeinern können, die im Prinzip überwachte und nicht überwachte Lerntechniken beinhalten.

## Das Ziel des maschinellen Lernens

Machine Learning zielt darauf ab, komplexe Zusammenhänge aus Erfahrung (d.h. Daten) rechnerisch zu erlernen. *Computational learning* ist ein Unterfeld künstlicher Intelligenz (KI), das sich auf die Entwicklung von Modellen konzentriert, die es Computern ermöglichen, Vorhersagen oder Entscheidungen zu lernen und zu treffen, ohne explizit programmiert zu werden. Es umfasst die Gestaltung und Umsetzung mathematischer und statistischer Modelle, die automatisch Daten analysieren, Muster identifizieren und fundierte Entscheidungen oder Vorhersagen basierend auf den beobachteten Daten treffen können. Diese Aufgabe kann beispielsweise die Vorhersage oder Modellierung komplexer Phänomene sein. Beachten Sie, dass die Vorhersage hier nicht nur auf die Zukunft, sondern auf ein nicht identifiziertes Ereignis verweist. So können wir z.B. vorhersagen, ob eine chemische Substanz bei einer Reihe von Umweltbedingungen in Wasser gelöst oder gelöst wird.

Im Gegensatz zum populären Denken sind ML-Algorithmen seit mehreren Jahrzehnten da. Sie wurden jedoch erst in den letzten zehn Jahren stark geachtet, als Einschränkungen in der Rechenleistung nicht mehr ein Hindernis für die Anwendung von ML *algorithmen* für die Bereitstellung hilfreicher *ML-Modelle* waren. Wir beziehen uns auf *Algorithmen* als Basiszeilen-Befehle, die ein Modell *how aus Daten zu lernen* anweisen, während ein *ML-Modell* das Ergebnis (d.h. das gelernte Programm) des Lernens der Zielaufgabe aus der ausgewählten Regelreihe (*ML-Algorithmus*) und Beispiele (d.h. Daten) ist.

## Arten des maschinellen Lernens

In diesem Abschnitt beschäftigten wir uns hauptsächlich mit grundlegenden Elementen des überwachten Lernens, aber beachten Sie, dass es mehrere andere Arten von ML-Problemen gibt. Einige davon sind:
* Unsupervised learning: Wir geben kein korrektes Verhalten (d.h. Labels) an. Hier haben wir einige Beobachtungen, aber die Aufgabe selbst ist nicht klar definiert.
* Semi-supervised learning: Wir können einige Teile unseres Modells mit einigen Labels angeben, aber andere Teile müssen ohne explizite Ziele gelernt werden. So können wir z.B. ununterbrochenes Lernen nutzen, um Cluster zu erhalten, die Funktionen zu einem überwachten Lernproblem definieren.
* Aktives Lernen: Der Algorithmus selbst kann nach weiteren, nützlichen Beispielen fragen. Lernen Sie zum Beispiel nur Beispiele auszuwählen, die für das Lernen tatsächlich benötigt werden.
* Transfer-Lernen: Wenn eine Methode für ein individuelles Szenario trainiert wird und Sie es in einem anderen Szenario verwenden möchten. Dies bedeutet: Wie man von dem Gebrauch macht, was von A auf B gelernt wurde?
* Verstärkungslernen: Das Modell ist ausgebildet, um zu handeln, anstatt nur vorherzusagen, und der Algorithmus selbst nutzt Ergebnisse aus seinen experimentierten Handlungen als Feedback oder * Verstärkung*, um ein optimiertes Ergebnis von Handlungen zu erreichen (z.B. ein Roboter lernen zu gehen).

(data-science)=
## Der Unterschied zwischen maschinellem Lernen und Datenwissenschaft

Der konzeptionelle Unterschied zwischen Datenwissenschaft und maschinellem Lernen kann sich ähnlich dem Konzept von Rechtecken und Quadraten in der Geometrie vorstellen, wo die Datenwissenschaft mit *Rectangles* und maschinelles Lernen mit *quares* korrespondiert. Sowohl Datenwissenschaft als auch maschinelles Lernen beschäftigen sich mit der Programmierung (z.B. in Python, R oder SQL), Statistik und Datenmodellierung. Die Datenwissenschaft umfasst zudem die Datenvisualisierung und Datenknüpfung.

```{admonition} Recommended course
:class: tip

Denken Sie daran, nach Materialien zu suchen und studieren unabhängig für Ihr optimales Lernen. Zum Beispiel empfehlen wir den umfassenden [Maschinenlernkurs](https://www.edx.org/course/machine-learning-with-python-from-linear-models-to), der von MITx angeboten wird, die Online-Lerninitiative des Massachusetts Institute of Technology.
```

