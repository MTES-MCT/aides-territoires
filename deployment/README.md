# Recettes de déploiement Ansible

Ce répertoire contient un [jeu de recettes Ansible
complet](https://www.ansible.com/) permettant de déployer le projet
Aides-Territoires en une seule commande sur les serveurs de staging et
production.


## Démarrage rapide

Utiliser le fichier [hosts](./hosts) comme point de départ pour configurer
[l'inventaire Ansible](http://docs.ansible.com/ansible/intro_inventory.html).
Il est possible de copier ce fichier vers `/etc/ansible/hosts` ou de le
référencer systématiquement avec l'option `-i`.

Il est également important de s'assurer que sa clé ssh a bien été envoyée sur
le serveur.

Pour mettre à jour tous les environnements :

    ansible-playbook -i hosts site.yml

Pour déployer en recette uniquement :

    ansible-playbook -i hosts -l stage site.yml


## Playbooks

Le répertoire est structuré en respectant les [bonnes pratiques
Ansible](http://docs.ansible.com/ansible/playbooks_best_practices.html).

Le fichier de recette principal est `site.yml`. Lancer cette recette va
entièrement configurer tous les serveurs listés dans l'inventaire Ansible et
installer le projet dessus. Le seul pré-requis est d'avoir un accès ssh à
l'utilisateur root sur le serveur, et que Python soit installé sur la machine
destination.


## Configuration des environnements

Certains paramètres de configuration (clés d'accès aux apis, mots de passe,
etc.) ne peuvent être embarquées dans le dépôt git. Pour cette raison, les
valeurs sensibles doivent être embarqués dans un fichier `.env.quelquechose`
placé à [la racine du projet Django](../src/). Ce fichier sera automatiquement
copié par le script de déploiement.

Par ailleurs, les variables spécifiques au déploiement sont configurées dans le
répertoire [group_vars](./group_vars/).


## Déploiement rapide

En exécutant le livre de recette principal `site.yml`, Ansible va exécuter
toutes les étapes de déploiement, y compris les tâches de configuration du
serveur, ce qui peut prendre un certain temps.

Dans le cas de livraisons fréquentes, il est possible de n'exécuter que les
dernières tâches, i.e mise à jour de la base de code, installation des paquets,
migrations de la base de données, recompilation des fichiers css, etc.

    ansible-playbook -i hosts site.yml --start-at-task="Build"


## Différentes versions pour différents environnements

Il est souvent d'usage d'effectuer des livraisons de versions différentes sur
différents environnements, par exemple pour faire tourner la branche `master`
sur le serveur de recette mais un tag spécifique sur le serveur de production.

Pour ce faire, nous utilisons [les variables de groupes
spécifiques](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html).

Cf. la variable `project_version` du [répertoire group_vars](./group_vars/).


## Configuration locale

Le [fichier d'inventaire "hosts"](./hosts) dans le dépôt ne contient pas de
noms de domaines. Pour le faire fonctionner tel quel, il est possible de
définir des alias ssh.

### SSH Config

Voici un exemple de fichier `~/.ssh/config`:

    # Physical host
    Host myserver
        HostName myserver.com
        User root

    # The staging instance on a LXC virtual machine and a public ip
    Host aides.stage
        User root
        Port 22
        HostName 51.15.144.197
        ForwardAgent yes

    # The production instance on a LXC virtual machine and a public ip
    Host aides.prod
        User root
        Port 22
        HostName 62.4.14.127
        ForwardAgent yes
