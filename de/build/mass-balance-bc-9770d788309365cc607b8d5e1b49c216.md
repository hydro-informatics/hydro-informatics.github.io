---
description: Detaillierte Anleitung zur Grenzkonditionierungs- und Massenkonvergenzanalyse in TELEMAC, die Froude-Zahlen, Flussanalyse und Workflows für robuste massenkonservative Flussmodellierung abdeckt.
---

(foc-mass-bc)=
# Grenzen und Massenkonvergenz

Die Erhaltung von Masse und Definition von Randbedingungen gehen Hand in Hand, da überbestimmte oder falsch eingeschränkte Flüssigkeitsgrenzen unsymmetrische Wasser- oder Sedimentmassen oder andere rechnerische Probleme wie überkritische Strömungen (aus hoch {term}`Froude numbers <Froude number>`) resultieren. Dieses Kapitel sieht unter der Haube der Randbedingungen, wie sie die Massenbilanz, die Flusskonvergenzanalyse beeinflussen und was getan werden kann, um ein robustes, massenkonservatives numerisches Telemac-Modell zu erhalten. Ein **voller Workflow für robuste Modellierung wird unter der {ref}`end of this chapter <tm-foc-mass-workflow>`** angeboten.

