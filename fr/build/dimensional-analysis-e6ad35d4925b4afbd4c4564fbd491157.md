---
description: Introduction à l'analyse des données et à l'analyse dimensionnelle pour l'ingénierie des ressources en eau, y compris les types de données, les configurations expérimentales et les méthodes traditionnelles d'élaboration des idées.
---

(about-data)=
# A propos de l'analyse des données

Traditionnellement, l'analyse dimensionnelle a été utilisée pour tirer des enseignements de différentes configurations expérimentales et environnements d'enquête. Ce chapitre approfondit brièvement le type de données et explique les données traditionnelles avec une analyse dimensionnelle.

## Nature des données

```{admonition} Under construction - incomplete instructions
:class: warning
Nous différencions les données sous la forme de représentations nominales, ordinales, d'intervalles et de rapports (cf. MA Negreiros chpt 2.1.1).
```


## Analyse dimensionnelle

Cette section présente la théorie de l'échelle selon {cite:t}`barenblatt_dimensional_1987`, {cite:t}`barenblatt_scaling_1996`, et {cite:t}`yalin71`.

### Description du modèle mathématique

L'hydrodynamique de la rivière peut être exprimée par une expression simplifiée de la dimension {term}`Navier-Stokes equations` pour les fluides incompressibles, en supposant une distribution de pression hydrostatique {cite:p}`kundu_fluid_2008, graf_hydraulique_2011`. Il en résulte les équations d'eau peu profonde de Saint-Venant utilisées dans certains modèles d'ordinateur hydraulique (p. ex. HEC-RAS ou BASEMENT1D {cite:p}`us_army_corps_of_engineeers_hydrologic_2016, vaw_laboratory_2017`. Cette équation d'eau peu profonde se compose de cinq termes {cite:p}`jansen_scale_1994`:

$$
	\overbrace{\frac{1}{g} \frac{\partial u}{\partial t}}^{I}  +  \overbrace{\frac{u}{g} \frac{\partial u}{\partial x}}^{II}  +  \overbrace{\frac{\partial h}{\partial x}}^{III}  +  \overbrace{\frac{\partial z}{\partial x}}^{IV}   =  \overbrace{-\frac{u\left| u \right|}{C^2 h}}^{V = S_e}
$$

Les cinq termes peuvent être reliés séparément les uns aux autres pour la dérivation des facteurs d'échelle$\lambda$. Ainsi, l'équation des échelles des termes I et II se traduit par {cite:p}`de_vries_river_1993`:

$$
	\frac{\lambda_u}{\lambda_t} = \frac{\lambda_u^2}{\lambda_l} \Longrightarrow \lambda_l = \lambda_u \cdot \lambda_t
$$


où
* $\lambda_u$ $\equiv$ échelle de vitesse et
* $\lambda_t$ & $\equiv$ & échelle de temps.

Postulant que l'échelle de gravité $\lambda_g$ est l'unité, la comparaison des échelles des termes II et V donne les résultats suivants :

$$
	\frac{\lambda_u^2}{\lambda_l} = \frac{\lambda_u^2}{\lambda_C^2 \cdot \lambda_h} \Longrightarrow \lambda_C^2 = \sqrt{\frac{\lambda_l}{\lambda_h}}
$$


where $\lambda_C$ $\equiv$ Ch\'ezy roughness scale.

### Concepts de Similitude

La similarité du nombre de Froude dans un modèle à échelles et un prototype est obtenue sur la base de la condition Froude, qui résulte de l'équivalence des échelles des termes II et III dans l'équation ci-dessus {cite:p}`de_vries_river_1993`:

$$
	\frac{\lambda_u^2}{\lambda_l} = \frac{\lambda_h}{\lambda_l} \Longrightarrow \lambda_u = \sqrt{\lambda_h}.
$$

La similarité du transport des sédiments est particulièrement intéressante dans cette étude et exige que les échelles de {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` $\tau_{*}$ et de {term}`bed load transport intensity <Bedload>` $\Phi_b$ soient unies (i.e., $\lambda_{\tau_*}$=1 et $\lambda_{\Phi}$=1 {cite:p}`de_vries_river_1993`).

En ce qui concerne la vitesse de cisaillement $u_*$ = $\sqrt{\tau/\rho_f}$ = $\sqrt{\tau_*(s-1)gD}$ et l'exigence de $\lambda_{\tau_*}$=1, la similitude du transport des sédiments est donnée lorsque {cite:p}`jansen_scale_1994`:

$$
	\lambda_u^2 \approx \lambda_s \cdot \lambda_{D}
$$


où
* $\lambda_s$ $\equiv$ échelle de densité relative des sédiments
* $\lambda_{D}$ $\equiv$ échelle du diamètre du grain.


La similitude du transport unitaire des sédiments (c.-à-d. par unité de largeur) peut être vérifiée sur la base de l'échelle $\lambda_{q_b}$, qui est dérivée de l'échelle {term}`Exner equation`:

$$
	\frac{\partial z}{\partial t} = -\frac{1}{1-\zeta} \cdot \frac{\partial q_s}{\partial x}
$$

En ce qui concerne les considérations relatives à l'échelle ci-dessus, $\lambda_{q_b}$ est dérivé comme suit:

$$
	\frac{\lambda_l}{\lambda_t} = \frac{\lambda_{q_b}}{\lambda_l} \Rightarrow \lambda_{q_b} =\frac{\lambda_l^2}{\lambda_t} = \lambda_l^{3/2}
$$

$\lambda_{q_b}$ refers to volumetric fluxes. The scale of the mass flow rate $\lambda_{\dot{q}_b}$ can be computed by multiplying the above equation by the sediment density $\rho_s$. Postulating the density scale of $\lambda_{s}$=1, the mass flow rate scale is also $\lambda_{\dot{q}_b}= \lambda_l^{3/2}$.
The boundary conditions imposed by the feasibility of the laboratory experiments entail that the densities of the sediment in nature and in the model are similar (i.e., $\lambda_s$=1). Thus, the Froude similarity ($\lambda_u = \sqrt{\lambda_h}$) and the similarity of sediment transport ($\lambda_u = \sqrt{\lambda_{D}}$) require that $\lambda_{D}$=$\lambda_h$ (i.e., the same geometric scales apply to the grain diameter as well as to the water depth) {cite:p}`jansen_scale_1994`. This condition can be considered as fulfilled in this study, as of coarse sediments in the shape of gravel are used for the experiments.
