(chpt-unsteady)=
# Unsteady 2d Simulation

## Under construction. Expected release in the next 12 months.

Thank you for your patience.

(prepro-unsteady)=
### Define unsteady flow boundaries

In addition, users can define a liquid boundary conditions file (*qsl*) to define time-dependent boundary conditions (e.g., discharge, water depth, flow velocity or tracers).
The name format of the boundary conditions file can be modified in the steering file with:

```
/steering.cas
BOUNDARY CONDITIONS FILE : 'bc_channel.cli'
LIQUID BOUNDARIES FILE   : 'bc_unsteady.qsl'
```

Example for a liquid boundary conditions file:
```
# bc_unsteady.qsl
# Time-dependent inflow (discharge Q(2) and outflow (depth SL(1)
T           Q(1)     SL(2)
s           m3/s     m
0.            0.     5.0
500.        100.     5.0
5000.       150.     5.0
```

### Stage-discharge (or WSE-Q) Relationship

Define a stage-discharge file (*ASCII* format) to use a stage (water surface elevation *WSE*) - discharge relationship for boundary conditions. Such files typically apply to the downstream boundary of a model at control sections (e.g., a free overflow weir). To use a stage-discharge file, define the following keyword in the steering file:

```
/steering.cas
STAGE-DISCHARGE CURVES FILE : YES
```
