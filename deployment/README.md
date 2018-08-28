# Recettes de déploiement Ansible

Ce répertoire contient un [jeu de recettes Ansible
complet](https://www.ansible.com/) permettant de déployer le projet
AIdes-Territoires en une seule commande sur un serveur.


## Démarrage rapide

Utiliser `./hosts.example` comme point de départ pour configurer [l'inventaire
Ansible](http://docs.ansible.com/ansible/intro_inventory.html). Il est possible
d'éditer le fichier `/etc/ansible/hosts` ou de créer un fichier local à
référencer à chaque fois avec l'option `-i`.

Il est également important de s'assurer que sa clé ssh a bien été envoyée sur
le serveur.

Pour déployer en production:

    ansible-playbook -i hosts site.yml


## Playbooks

Le répertoire est structuré en respectant les [Bonnes pratiques
Ansible](http://docs.ansible.com/ansible/playbooks_best_practices.html).

Le fichier de recette principal est `site.yml`. Lancer cette recette va
entièrement configurer un serveur et installer le projet dessus. Le seul
pré-requis est d'avoir un accès ssh à l'utilisateur root sur le serveur.


## Configuration de production

Les paramètres de production ne peuvent être embarquées dans le dépôt git. Pour
cette raison, les valeurs sensibles doivent être embarqués dans un fichier
`.env.production` placé à la racine de projet Django. Ce fichier sera
automatiquement copié par le script de déploiement.


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

Pour ce faire, il suffit de définir [des variables de groupes
spécifiques](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html).

Créer `/etc/ansible/group_vars/<group>.yml`, et configurer la variable
`project_version` qui peut prendre pour valeur une branche, un tag ou un nom de
commit git.


## Configuration locale

### SSH Config

Voici un exemple de fichier `~/.ssh/config`:

    # Physical host
    Host myserver
        HostName myserver.com
        User root

    # The production instance on a LXC virtual machine and a public ip
    Host www.myserver.com
        HostName 1.2.3.4
        User root
        ForwardAgent yes

    # The staging instance on a LXC virtual machine and a local ip only
    Host staging.myserver.com
        User root
        ProxyCommand ssh myserver nc lxc_staging_machine_name 22
        ForwardAgent yes
