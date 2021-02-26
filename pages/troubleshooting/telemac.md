---
title: Debugging TELEMAC
tags: [telemac, troubleshooting]
keywords: basement, numerical modelling
sidebar: mydoc_sidebar
permalink: dbg_tm.html
folder: troubleshooting
---

Since its early development, *TELEMAC* has become a robust an reliable tool for the numerically modelling of open surface flows. Yet there are a few little challenges and this page provides some answers (under development).

## Traceback errors

If a simulation crashes and it is not clear why, debugging with [*gdb*](http://www.gdbtutorial.com) is a good option. To do so, first install *gdb*:

```
sudo apt install gdb
```

Then launch the steering file in debugging mode as follows:

```
telemac2d.py -w tmp simulation_file.cas --split
telemac2d.py -w tmp simulation_file.cas -x
cd tmp
gdb ./out_telemac2d
```

In *gdb* tap:

```
(gdb) run
```

To end *gdb* tap:
 
 ```
(gdb) quit
```

This approach also works with *Telemac3d* (and other modules).
 
 ## Errors in steering (CAS) file
 
 * make sure to use `:` rather than `=`
 * place all model files in the same folder and only use file names without the directories of files
 