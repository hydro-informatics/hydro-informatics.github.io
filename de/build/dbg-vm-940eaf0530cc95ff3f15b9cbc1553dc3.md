---
description: Beheben Sie häufige VirtualBox- und virtuelle Maschinenfehler, einschließlich Hardwarebeschleunigungsproblemen und OpenGL-Abstürzen mit NVIDIA-Grafikkarten unter Debian Linux.
---

# Debugging virtueller Maschinen

## Fehlermeldung: Hardwarebeschleunigung nicht verfügbar

Diese Fehler-Popup-Nachricht kann von *VirtualBox* (oder anderen Hypervisoren) aufgrund einer Einstellung im BIOS des Hostsystems ausgelöst werden. Um den Fehler zu beheben:

* Den Computer neu starten.
* Enter the boot menu during start-up: At the very beginning of the system start, typically press the `F2` or `DEL` key. Depending on the computer, other keys might apply (e.g., `F12` - watch the screen for information on how to access `Setup`).
* The boot manager opens. Use the arrow keys to navigate to the `Advanced settings`, hit enter, and go to `CPU Configuration`.
* In the `CPU Configuration`, go to `Secure Virtual Machine`. If there is a `[Disabled]` flag, hit the enter key to switch to `[Enabled]`.
* Drücken Sie `Esc`, gehen Sie zu `Exit` > `Save changes and exit` (oder drücken Sie einfach die `F10`-Taste). Bestätigung. Das System wird jetzt neu gestartet.
* Zurück in *Windows * führen Sie *VirtualBox * erneut aus und starten Sie eine VM. Die Fehlermeldung sollte nicht mehr angezeigt werden.


## Grafische Benutzeroberflächen abstürzen

Die Verwendung von *OpenGL* mit virtuellen Maschinen auf *VirtualBox* befindet sich noch in einer experimentellen Phase und kann insbesondere mit *nvidia* Grafikkarten fehlschlagen. Um *nvidia*-Treiber zu installieren, *non-free*-Pakete zu aktivieren und *nvidia-detect* zu installieren, um einen geeigneten Treiber abzurufen:

 * Öffnen Sie `etc/apt/sources.list` und ändern Sie die `buster`repository-Definition (Beispiel für Server in Deutschland):
    + Original: `deb http://ftp.de.debian.org/debian/ buster main`
    + an: `deb-src http://ftp.de.debian.org/debian/ buster main non-free`
* In *Terminal* Repositorien aktualisieren und `nvidia-detect` installieren

```
sudo apt update
sudo apt -y install nvidia-detect
```

Installieren Sie dann den Treiber *nvidia* (oder was auch immer der vorherige Befehl empfohlen hat):

```
sudo apt install nvidia-driver
```

Debian neu starten, um abzuschließen:

```
systemctl reboot
```
