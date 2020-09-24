---
title: Debugging Virtual Machines
tags: [telemac, troubleshooting, vm]
keywords: telemac, virtual, machine, virtualbox
sidebar: mydoc_sidebar
permalink: dbg_vm.html
folder: troubleshooting
---

### Error message: Hardware acceleration not available

This error pop-up message may be raised by *VirtualBox* (or other hypervisors) because of a setting in the BIOS of the host system. To fix the error:

* Reboot the computer.
* Enter the boot menu during start-up: At the very beginning of the system start, typically press the `F2` or `DEL` key. Depending on the computer, other keys might apply (e.g., `F12` - watch the screen for information on how to access `Setup`).
* The boot manager opens. Use the arrow keys to navigate to the `Advanced settings`, hit enter, and go to `CPU Configuration`.
* In the `CPU Configuration`, go to `Secure Virtual Machine`. If there is a `[Disabled]` flag, hit the enter key to switch to `[Enabled]`.
* Press `Esc`, go to `Exit` > `Save changes and exit` (or just hit the `F10` key). Confirm. The system will reboot now.
* Back in *Windows* re-run *VirtualBox* and start a VM. The error message should no longer appear.
