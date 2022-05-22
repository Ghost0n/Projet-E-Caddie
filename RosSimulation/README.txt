Matériel: VM
OS: Ubuntu 20.04.4 LTS
Version ROS: noetic 1.15.14
Langage: Python version 3.8.10
Dépendence du code: rospy

************************************************Consigne de de lancement********************************************

Il faut exécuter les commandes suivantes dans le terminal:

- $ cd "path/to/RosProject"     		Pour changer le répertoire courant vers le répertoire RosProject
- $ source devel/setup.bash			Nécessaire pour chaque terminal avant utiliser ROS
- $ catkin_make					Pour s'assurer de l'intégrité du code
- $ roslaunch mpriority simulation.launch 	Le fichier .launch s'occupe de lancer tous les noeuds implémentés

S'il y a un problème d'exécution il faut s'assurer que tous les fichiers " *.py " 
dans " RosProject/src/mpriority/scripts " ont tous la permission d'exécution.
Sinon il faut les ajouter avec $ chmod +x nom_de_fichier.py 

************************************************Consigne d'utilisation***********************************************

La simulation est constituée par 3 caisses pour le moment pour des raisons de test.
Au début, le numéro de caisse faisant l'appel est demandé. (un entier entre 1 et 3 est exigé, tapez 99 si vous voulez quitter l'appel de caisse)
On observe ensuite l'algorithme de priorité qui donne l'ordre à l'e_caddie de s'y rendre,
Et l'e_caddie se met à se déplacer jusqu'à arriver à sa destination.
