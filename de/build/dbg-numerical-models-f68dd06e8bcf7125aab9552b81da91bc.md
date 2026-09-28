---
description: Behebung gemeinsamer numerischer Modellierungsprobleme, einschließlich Mesh-Qualitätsrichtlinien, dreieckigen und rechteckigen Mesh-Best Practices und Stabilitätstipps für CFD-Simulationen.
---

# Numerische Modelle

Die Einrichtung eines numerischen Modells, das in kommerziellen oder nicht-kommerziellen Codes implementiert ist, kann viel Kopfzerbrechen verursachen. Diese Seite enthält einige grundlegende Prinzipien, um Probleme mit numerischen Modellen zu vermeiden.



## Mesh Generation und Qualität

Die Hinweise zum Meshing sind aus [Olsen (1999)](http://folk.ntnu.no/nilsol/cfd/class2.pdf) und [Olsen (2012)](http://folk.ntnu.no/nilsol/tvm4155/flures6.pdf) extrahiert.

Allgemein:

* Mesh-Übergang: Zellen sollten nicht kleiner oder größer als 50% bzw. 200% der Größe benachbarter Zellen sein.
* Dreieckmaschen gegenüber rechteckigen Maschen bevorzugen (Rechenleistung).


Dreieckmaschen:

* Vermeiden Sie breite oder spitzwinklige Dreiecke (optimal: gleichseitige Dreiecke). Kein Innenwinkel sollte kleiner als 22° sein.

Rechteckmaschen:

* Alle Innenwinkel sollten nahe bei 90° liegen.
