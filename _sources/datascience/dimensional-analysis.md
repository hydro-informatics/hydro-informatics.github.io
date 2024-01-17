(about-data)=
# About Data Analysis

Traditionally, dimensional analysis were used to derive insights from different experimental setups and survey environments. This chapter briefly digs into the type of data and explains traditional data insights with dimensional analysis. 

## The Nature of Data

```{admonition} Under construction - incomplete instructions
:class: warning
We differentiate between data in the form of nominal, ordinal, interval, and ratio representations (cf. MA Negreiros chpt 2.1.1).
```


## Dimensional Analysis

This section introduces the scaling theory according to {cite:t}`barenblatt_dimensional_1987`, {cite:t}`barenblatt_scaling_1996`, and {cite:t}`yalin71`.

### Mathematical Model Description

River hydrodynamics can be expressed by a simplified expression of the one-dimensional {term}`Navier-Stokes equations` for incompressible fluids, assuming hydrostatic pressure distribution {cite:p}`kundu_fluid_2008, graf_hydraulique_2011`). This results in the Saint-Venant shallow water equations as used in some hydraulic computer models (e.g., HEC-RAS or BASEMENT1D {cite:p}`us_army_corps_of_engineeers_hydrologic_2016, vaw_laboratory_2017`. This shallow water equation consists of five terms {cite:p}`jansen_scale_1994`:

$$
	\overbrace{\frac{1}{g} \frac{\partial u}{\partial t}}^{I}  +  \overbrace{\frac{u}{g} \frac{\partial u}{\partial x}}^{II}  +  \overbrace{\frac{\partial h}{\partial x}}^{III}  +  \overbrace{\frac{\partial z}{\partial x}}^{IV}   =  \overbrace{-\frac{u\left| u \right|}{C^2 h}}^{V = S_e}
$$

The five terms can be related separately to each other for the derivation of scale factors$\lambda$. Thus, equating the scales of the terms I and II results in {cite:p}`de_vries_river_1993`:

$$
	\frac{\lambda_u}{\lambda_t} = \frac{\lambda_u^2}{\lambda_l} \Longrightarrow \lambda_l = \lambda_u \cdot \lambda_t
$$


where
* $\lambda_u$ $\equiv$ velocity scale and
* $\lambda_t$ & $\equiv$ & time scale.

Postulating that the gravity scale $\lambda_g$ is unity, the comparison of the scales of terms II and V results in:

$$
	\frac{\lambda_u^2}{\lambda_l} = \frac{\lambda_u^2}{\lambda_C^2 \cdot \lambda_h} \Longrightarrow \lambda_C^2 = \sqrt{\frac{\lambda_l}{\lambda_h}}
$$


where $\lambda_C$ $\equiv$ Ch\'ezy roughness scale.

### Similitude Concepts

The similarity of the Froude number in a scaled model and a prototype is achieved based on the Froude condition, which results from equating the scales of terms II and III in the above equation {cite:p}`de_vries_river_1993`:

$$
	\frac{\lambda_u^2}{\lambda_l} = \frac{\lambda_h}{\lambda_l} \Longrightarrow \lambda_u = \sqrt{\lambda_h}.
$$

The similarity of sediment transport is of particular interest in this study and requires that the scales of the {term}`dimensionless bed shear stress <Dimensionless bed shear stress>` $\tau_{*}$ and of the {term}`bed load transport intensity <Bedload>` $\Phi_b$ are unity (i.e., $\lambda_{\tau_*}$=1 and $\lambda_{\Phi}$=1 {cite:p}`de_vries_river_1993`).

With respect to the shear velocity $u_*$ = $\sqrt{\tau/\rho_f}$ = $\sqrt{\tau_*(s-1)gD}$ and the requirement of $\lambda_{\tau_*}$=1, the similarity of sediment transport is given when {cite:p}`jansen_scale_1994`:

$$
	\lambda_u^2 \approx \lambda_s \cdot \lambda_{D}
$$


where
* $\lambda_s$ $\equiv$ scale of relative sediment density
* $\lambda_{D}$ $\equiv$ scale of grain diameter.


The similarity of unitary sediment transport (i.e., per unit width) can be verified based on the scale $\lambda_{q_b}$, which is derived from the {term}`Exner equation`:

$$
	\frac{\partial z}{\partial t} = -\frac{1}{1-\zeta} \cdot \frac{\partial q_s}{\partial x}
$$

With respect to the scale considerations above, $\lambda_{q_b}$ is derived as:

$$
	\frac{\lambda_l}{\lambda_t} = \frac{\lambda_{q_b}}{\lambda_l} \Rightarrow \lambda_{q_b} =\frac{\lambda_l^2}{\lambda_t} = \lambda_l^{3/2}
$$

$\lambda_{q_b}$ refers to volumetric fluxes. The scale of the mass flow rate $\lambda_{\dot{q}_b}$ can be computed by multiplying the above equation by the sediment density $\rho_s$. Postulating the density scale of $\lambda_{s}$=1, the mass flow rate scale is also $\lambda_{\dot{q}_b}= \lambda_l^{3/2}$.
The boundary conditions imposed by the feasibility of the laboratory experiments entail that the densities of the sediment in nature and in the model are similar (i.e., $\lambda_s$=1). Thus, the Froude similarity ($\lambda_u = \sqrt{\lambda_h}$) and the similarity of sediment transport ($\lambda_u = \sqrt{\lambda_{D}}$) require that $\lambda_{D}$=$\lambda_h$ (i.e., the same geometric scales apply to the grain diameter as well as to the water depth) {cite:p}`jansen_scale_1994`. This condition can be considered as fulfilled in this study, as of coarse sediments in the shape of gravel are used for the experiments.
