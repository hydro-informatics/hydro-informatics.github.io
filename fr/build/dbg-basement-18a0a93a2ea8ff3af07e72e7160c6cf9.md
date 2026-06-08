---
description: Solutions aux erreurs de modèles numériques de base communes, y compris les problèmes d'importation de sortie XDMF et les problèmes de répertoire de simulation dans le post-traitement QGIS.
---

# Base de débogage

Depuis ses débuts, *BASEMENT* est devenu un outil fiable pour la modélisation numérique des rivières. Pourtant, il y a quelques défis et cette page fournit quelques réponses (en cours d'élaboration).

(dbg-bm-xdmf)=
## Importation d'outils de sortie de modèle XDMF


### Erreur XDMF des versions erronées

Selon l'environnement du système, l'en-tête de `results.xmdf` peut ne pas être lisible pour QGIS. Les deux onglets ci-dessous montrent les lignes d'en-tête incorrectes et correctes. Pour résoudre le problème, ouvrez `results.xmdf` dans un éditeur de texte (par exemple, {ref}`Notepad++ <npp>` sur Windows), remplacez le mauvais par l'en-tête correct, et enregistrez le correctif `results.xmdf`.

`````{tab-set}
````{tab-item} Wrong header
```html
<?xml version="1.0"?>
<Xdmf Version="3.0">
```
````

````{tab-item} Correct header
```html
<?xml version="1.0" ?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="2.0">
```
````
`````

### Erreur XDMF des mauvais répertoires de simulation
Le `results.xdmf` contient des données géospatiales explicites (p. ex., vitesse du débit et profondeur de l'eau), qui peuvent théoriquement être importées directement dans *QGIS* avec le plugin *Crayfish* (en savoir plus dans la section {ref}`BASEMENT post-processing <qgis-imp-steps>`). Cependant, il y a un petit problème : QGIS peut s'écraser à cause d'un répertoire invalide. Pour le réparer :

1. Ouvrir `results.xdmf` dans un éditeur de texte (par exemple, {ref}`Notepad++ <npp>` sous Windows).
1. Utilisez l'outil de recherche et de remplacement (`CTRL` + `H` touches dans Notepad++) pour supprimer les chemins de fichiers avant `results_aux.h5`.
* Recherchez la chaîne `results_aux.h5` et identifiez le chemin écrit devant elle (par exemple, `C:\temp\`).
* Trouver et remplacer ce chemin utilisateur, par exemple : `Find` = `C:\temp\results_aux.h5` et `Replace with` = `results_aux.h5`.
1. Après avoir supprimé toutes les occurrences de chemin dans le document, enregistrer et fermer `results.xdmf`.


Cette question est également abordée dans le [Forum des utilisateurs de BASEMENT](http://people.ee.ethz.ch/~basement/forum/viewtopic.php?id=5261)].
