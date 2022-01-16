# _Challenge 2_

Voici la branche Challenge2 du groupe Rouge

## _Pré-Requis_

L'exécution de notre code nécessite l'utilisation d'un fichier .weights contenant les résultats de l'aprentissage de notre réseau de neurones. 
Celui-ci dépassant la taille maximale autorisée, il faut le télécharger sous le lien suivant : https://drive.google.com/file/d/1k9ex3AmuKGmZoxvqDPVgwVyrhr3TGt6z/view?usp=sharing
Ce fichier est à placer dans grp-rouge/vision/

De plus,  le fichier [detectbottle.py](https://github.com/hugovanhille/LARM-Groupe_Rouge/blob/challenge2/grp-rouge/scripts/detectbottle.py) contient deux paramètre associés à des chemins locaux à définir. Merci de modifier ces deux chemins présents ligne 17 du fichier detectbottle (remplacer /home/altreon par /home/username/)

## _Composition_

Notre objectif était de trouver des bouteilles Nuka Cherry dans l'espace de jeu et de les marquer dans la carte

Cette branche contient ce fichier README ainsi que le package grp-rouge

Notre stratégie de vision se base sur un réseau de neurones en deep learning entrainé à partir d'une centaines d'images de bouteilles oranges et noires sur un réseau préentrainé de YOLO. 
Ce réseau de neurones fonctionne parfaitement lors des test ou on lui donne u jeu d'images à analyser

Dans le répertoire scripts, on retrouve  2 fichiers python.
- Le fichier [detectbottle.py](https://github.com/hugovanhille/LARM-Groupe_Rouge/blob/challenge2/grp-rouge/scripts/detectbottle.py) permet d'analyser les images obtenu par la caméra pour détecter des bouteilles. Nous avons choisis d'analyser une image toute les 1,5s afin de ne pas surcharger l'éxecution.
 Une fois une bouteille détecté, on récupère sa position grace à la caméra 3D, et on envoie l'information sur un topic qui sera récupére par le fichier python suivant.
- Le deuxième ([markbottle.py](https://github.com/hugovanhille/LARM-Groupe_Rouge/blob/challenge2/grp-rouge/scripts/markbottle.py)) s'occupe d'afficher les marqueurs des bouteilles sur Rviz.

Dans le répertoire launch il y a le fichier launch NAME qui permet de lancer la simulation du robot
Lacommande à éxecuter est la suivante :
```bash 
roslaunch grp-rouge challenge2.launch 
```

Ensuite, le répertoire vision contient l'ensemble des fichiers utiles au bon fonctionnement de notre réseau de neurones (résultats de l'apprentissages et autres informations indispensables à son exécution).

Finalement, le dossier rviz  permet de lançer rviz dans les bonnes configurations.
