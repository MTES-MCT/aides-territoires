
# Intégration de l'équipe « *onboarding* »

Afin d'avoir un environnement de travail le plus proche possible de la production,
il est recommandé d'utiliser une machine virtuelle LXC qui contiendra l'intégralité
du projet. 
Ladite machine pourra être configurée automatiquement grâce a un script de déploiement qui génére la machine virtuelle LXC et la configure.
Ce script exécute aussi le même script de déploiement que ceux utilisés pour la recette et la production.

## Prérequis 
Le script de déploiement à été réalisé sur une machine fonctionnant sous Ubuntu 18.04 possédant les paquets suivants :

 - lxd
 - git
 - ansible 2.7.7 (minimum)
 
 ## Déploiement
 - Créer un répertoire de travail et cloner le projet git : (*git clone https://github.com/MTES-MCT/aides-territoires*)
 - Se rendre de le répertoire aides-territoires/deployment  (*cd aides-territoires/deployment*)
 - Exécuter le script d'installation : *./local_vm_creation.sh* qui effectue les actions suivantes :
	 - Test de la présence d'une clé publique
		 - Si elle n'existe pas la générer avec la commande *ssh-keygen -t rsa* puis relancer le script
		 - Si il en existe une ou plusieurs saisir le nom de la clé à utiliser (si la saisie est incorrecte le script s'interrompt)
	 - Création et mise à jour de la machine virtuelle LXC.
	 - Configuration de l'accès root ssh par clé rsa.
	 - Installation de python.
	 - Mise en place d'un répertoire partagé permettant la prise en compte du code modifié dans le répertoire de travail local.
 
 Si tout s'est bien passé vous devez avoir une machine virtuelle presque fonctionnelle.
 
 Il reste quelques manipulations à effectuer qui sont expliquées à la fin du script.
 - Sur la machine hôte :
	 - Modification du fichier ~/.ssh/config
     - Création du fichier *.env.local* dans le répertoire *aides-territoires/src/*
	 - Déploiement de l'application à l'aide d'ansible (*ansible-playbook -i hosts -l local -vvv site.yml*)
	
 - Sur la machine virtuelle :
	 - Démarrer l'environnement virtuel Python
	 - Installer les packages python nécessaires

 Il serra aussi nécessaire de mettre à jour la base de donnée à partir d'un dump récent.  