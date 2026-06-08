---
description: Correction des erreurs courantes de VirtualBox et de la machine virtuelle, y compris les problèmes d'accélération matérielle et les pannes OpenGL avec les cartes graphiques NVIDIA sur Debian Linux.
---

# Déboguer des machines virtuelles

## Message d'erreur : Accélération matérielle non disponible

Ce message pop-up d'erreur peut être soulevé par *VirtualBox* (ou d'autres hyperviseurs) en raison d'un réglage dans le BIOS du système hôte. Pour corriger l'erreur :

* Redémarrez l'ordinateur.
* Saisissez le menu de démarrage pendant le démarrage : Au tout début du système, appuyez généralement sur la touche `F2` ou `DEL`. Selon l'ordinateur, d'autres clés peuvent s'appliquer (par exemple, `F12` - regardez l'écran pour savoir comment accéder à `Setup`).
* Le gestionnaire de démarrage s'ouvre. Utilisez les touches fléchées pour naviguer à `Advanced settings`, appuyez sur Entrée et allez à `CPU Configuration`.
* Dans le `CPU Configuration`, allez à `Secure Virtual Machine`. S'il y a un drapeau `[Disabled]`, appuyez sur la touche Entrée pour passer à `[Enabled]`.
* Appuyez sur `Esc`, allez à `Exit` > `Save changes and exit` (ou appuyez simplement sur la touche `F10`). Confirmez. Le système va redémarrer.
* Retour dans *Windows* re-lancer *VirtualBox* et démarrer un VM. Le message d'erreur ne devrait plus apparaître.


## Interfaces utilisateur graphiques plantage

L'utilisation de *OpenGL* avec des machines virtuelles sur *VirtualBox* est encore en phase expérimentale et peut échouer, en particulier avec les cartes graphiques *nvidia*. Pour installer les pilotes *nvidia*, activez les paquets *non-free* et installez *nvidia-detect* pour récupérer un pilote approprié:

 * Ouvrez `etc/apt/sources.list` et changez la définition `buster`repositoire (exemple pour le serveur en Allemagne):
    + original : `deb http://ftp.de.debian.org/debian/ buster main`
    + À : `deb-src http://ftp.de.debian.org/debian/ buster main non-free`
* Dans *Terminal* mettre à jour les dépôts et installer `nvidia-detect`

```
sudo apt update
sudo apt -y install nvidia-detect
```

Ensuite, installez le pilote *nvidia* (ou quelle que soit la commande précédente recommandée):

```
sudo apt install nvidia-driver
```

Redémarrer Debian pour finaliser :

```
systemctl reboot
```
