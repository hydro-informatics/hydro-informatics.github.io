# Debugging Virtual Machines

## Error message: Hardware acceleration not available

This error pop-up message may be raised by *VirtualBox* (or other hypervisors) because of a setting in the BIOS of the host system. To fix the error:

* Reboot the computer.
* Enter the boot menu during start-up: At the very beginning of the system start, typically press the `F2` or `DEL` key. Depending on the computer, other keys might apply (e.g., `F12` - watch the screen for information on how to access `Setup`).
* The boot manager opens. Use the arrow keys to navigate to the `Advanced settings`, hit enter, and go to `CPU Configuration`.
* In the `CPU Configuration`, go to `Secure Virtual Machine`. If there is a `[Disabled]` flag, hit the enter key to switch to `[Enabled]`.
* Press `Esc`, go to `Exit` > `Save changes and exit` (or just hit the `F10` key). Confirm. The system will reboot now.
* Back in *Windows* re-run *VirtualBox* and start a VM. The error message should no longer appear.


## Graphical User Interfaces crashing

Using *OpenGL* with virtual machines on *VirtualBox* is still in an experimental phase and may fails, in particular with *nvidia* graphic cards. To install *nvidia* drivers, enable *non-free* packages and install *nvidia-detect* to retrieve a suitable driver:

 * Open `etc/apt/sources.list` and change the `buster`repository definition (example for server in Germany):
    + original: `deb http://ftp.de.debian.org/debian/ buster main`
    + to: `deb-src http://ftp.de.debian.org/debian/ buster main non-free`
* In *Terminal* update repositories and install `nvidia-detect`

```
sudo apt update
sudo apt -y install nvidia-detect
```

Then, install the *nvidia* driver (or whatever the previous command recommended):

```
sudo apt install nvidia-driver
```

Reboot Debian to finalize:

```
systemctl reboot
```
