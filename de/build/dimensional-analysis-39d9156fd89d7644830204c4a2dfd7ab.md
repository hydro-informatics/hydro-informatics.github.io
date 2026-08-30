---
description: Einführung in die Datenanalyse und Dimensionsanalyse für die Wasserressourcentechnik, die Datentypen, experimentelle Setups und traditionelle Methoden zur Ableitung von Erkenntnissen umfasst.
---

(about-data)=
# Über Datenanalyse

Traditionell wurden dimensionale Analysen verwendet, um Erkenntnisse aus verschiedenen experimentellen Setups und Umfrageumgebungen abzuleiten. Dieses Kapitel befasst sich kurz mit der Art der Daten und erklärt traditionelle Dateneinblicke mit dimensionaler Analyse.

## Die Art der Daten

```{admonition} Under construction - incomplete instructions
:class: warning
Wir unterscheiden zwischen Daten in Form von nominalen, ordinalen, Intervall- und Verhältnisdarstellungen (vgl. MA Negreiros chpt 2.1.1).
```


## Dimensionsanalyse

Dieser Abschnitt stellt die Skalierungstheorie gemäß {cite:t}`barenblatt_dimensional_1987`, {cite:t}`barenblatt_scaling_1996` und {cite:t}`yalin71` vor.

### Beschreibung des mathematischen Modells

River hydrodynamics can be expressed by a simplified expression of the one-dimensional {term}`Navier-Stokes-Gleichungen <Navier-Stokes equations>` for incompressible fluids, assuming hydrostatic pressure distribution {cite:p}`kundu_fluid_2008, graf_hydraulique_2011`). This results in the Saint-Venant shallow water equations as used in some hydraulic computer models (e.g., HEC-RAS or BASEMENT1D {cite:p}`us_army_corps_of_engineeers_hydrologic_2016, vaw_laboratory_2017`. This shallow water equation consists of five terms {cite:p}`jansen_scale_1994`:

$$
	\overbrace{\frac{1}{g} \frac{\partial u}{\partial t}}^{I}  +  \overbrace{\frac{u}{g} \frac{\partial u}{\partial x}}^{II}  +  \overbrace{\frac{\partial h}{\partial x}}^{III}  +  \overbrace{\frac{\partial z}{\partial x}}^{IV}   =  \overbrace{-\frac{u\left| u \right|}{C^2 h}}^{V = S_e}
$$

The five terms can be related separately to each other for the derivation of scale factors$\lambda$. Thus, equating the scales of the terms I and II results in {cite:p}`de_vries_river_1993`:

$$
	\frac{\lambda_u}{\lambda_t} = \frac{\lambda_u^2}{\lambda_l} \Longrightarrow \lambda_l = \lambda_u \cdot \lambda_t
$$


wo
* $\lambda_u$ $\equiv$ velocity scale and
* $\lambda_t$ & $\equiv$ & Zeitskala.

Postulating that the gravity scale $\lambda_g$ is unity, the comparison of the scales of terms II and V results in:

$$
	\frac{\lambda_u^2}{\lambda_l} = \frac{\lambda_u^2}{\lambda_C^2 \cdot \lambda_h} \Longrightarrow \lambda_C^2 = \sqrt{\frac{\lambda_l}{\lambda_h}}
$$


Wobei $\lambda_C$ $\equiv$ Ch\'ezy Rauheit Skala.

### Similitude-Konzepte

The similarity of the Froude number in a scaled model and a prototype is achieved based on the Froude condition, which results from equating the scales of terms II and III in the above equation {cite:p}`de_vries_river_1993`:

$$
	\frac{\lambda_u^2}{\lambda_l} = \frac{\lambda_h}{\lambda_l} \Longrightarrow \lambda_u = \sqrt{\lambda_h}.
$$

The similarity of sediment transport is of particular interest in this study and requires that the scales of the {term}`Dimensionslose Schubspannung <Dimensionless bed shear stress>` $\tau_{*}$ and of the {term}`bed load transport intensity <Bedload>` $\Phi_b$ are unity (i.e., $\lambda_{\tau_*}$=1 and $\lambda_{\Phi}$=1 {cite:p}`de_vries_river_1993`).

In Bezug auf die Schergeschwindigkeit $u_*$ = $\sqrt{\tau/\rho_f}$ = $\sqrt{\tau_*(s-1)gD}$ und die Anforderung von $\lambda_{\tau_*}$=1 ist die Ähnlichkeit des Sedimenttransports gegeben, wenn {cite:p}`jansen_scale_1994`:

$$
	\lambda_u^2 \approx \lambda_s \cdot \lambda_{D}
$$


wo
* $\lambda_s$ $\equiv$ scale of relative sediment density
* $\lambda_{D}$ $\equiv$ scale of grain diameter.


Die Ähnlichkeit des einheitlichen Sedimenttransports (d.h. pro Einheitsbreite) kann anhand der Skala $\lambda_{q_b}$ verifiziert werden, die von {term}`Exner-Gleichung <Exner equation>` abgeleitet wird:

$$
	\frac{\partial z}{\partial t} = -\frac{1}{1-\zeta} \cdot \frac{\partial q_s}{\partial x}
$$

With respect to the scale considerations above, $\lambda_{q_b}$ is derived as:

$$
	\frac{\lambda_l}{\lambda_t} = \frac{\lambda_{q_b}}{\lambda_l} \Rightarrow \lambda_{q_b} =\frac{\lambda_l^2}{\lambda_t} = \lambda_l^{3/2}
$$

$\lambda_{q_b}$ refers to volumetric fluxes. The scale of the mass flow rate $\lambda_{\dot{q}_b}$ can be computed by multiplying the above equation by the sediment density $\rho_s$. Postulating the density scale of $\lambda_{s}$=1, the mass flow rate scale is also $\lambda_{\dot{q}_b}= \lambda_l^{3/2}$.
The boundary conditions imposed by the feasibility of the laboratory experiments entail that the densities of the sediment in nature and in the model are similar (i.e., $\lambda_s$=1). Thus, the Froude similarity ($\lambda_u = \sqrt{\lambda_h}$) and the similarity of sediment transport ($\lambda_u = \sqrt{\lambda_{D}}$) require that $\lambda_{D}$=$\lambda_h$ (i.e., the same geometric scales apply to the grain diameter as well as to the water depth) {cite:p}`jansen_scale_1994`. This condition can be considered as fulfilled in this study, as of coarse sediments in the shape of gravel are used for the experiments.
