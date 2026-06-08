---
description: Fehlerbehebung gemeinsamer numerischer Modellierungsprobleme einschließlich Mesh-Qualitätsrichtlinien, dreieckige und rechteckige Mesh-Best Practices und Stabilitätsspitzen für CFD-Simulationen.
---

# Numerische Modelle

Die Einrichtung eines in kommerziellen oder nichtkommerziellen Codes implementierten numerischen Modells kann eine Menge Kopfschmerzen verursachen. Diese Seite enthält einige Grundprinzipien, um Probleme mit numerischen Modellen zu vermeiden.



## Mesh Generation und Qualität

Die Hinweise zum Meshing werden aus [Olsen (1999)](http://folk.ntnu.no/nilsol/cfd/class2.pdf) und [Olsen (2012)](http://folk.ntnu.no/nilsol/tvm4155/flures6.pdf).

Allgemeines:

* Mesh-Übergang: Zellen sollten nicht kleiner oder größer als 50 % bzw. 200% der Größe benachbarter Zellen sein.
* Präfer dreieckige Maschen über rechteckige Maschen (computationseffizienz).


Dreieckige Maschen:

* Vermeiden Sie breite oder spitze Dreiecke (optimal: gleichseitige Dreiecke). Ein Innenwinkel sollte nicht kleiner als 22° sein.

Rechteckige Maschen:

* Alle Innenwinkel sollten in der Nähe von 90° liegen.
