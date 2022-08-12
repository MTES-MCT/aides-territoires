# Onboarding tech

## Montage de l'environnement de travail

Afin d'avoir un environnement de travail le plus proche possible de la production,
il est recommandé d'utiliser une machine virtuelle LXC qui contiendra l'intégralité
du projet.

Ladite machine pourra être créée automatiquement grâce a un script, et provisionnée
grâce à la même recette Ansible que celle utilisée pour le déploiement en
production.

Note : un setup alternatif (sans machine virtuelle) est documenté [ici](https://github.com/MTES-MCT/aides-territoires/wiki/Installation-de-l'environment-en-local).

### Prérequis

 * un OS unix à jour ;
 * une [installation de LXD fonctionnelle](https://linuxcontainers.org/lxd/getting-started-cli/).
 * git ;
 * ansible (2.7.7 minimum) ;

### Création de la machine de dev locale

Créer un répertoire de travail et cloner le projet git :

    git clone https://github.com/MTES-MCT/aides-territoires

Se déplacer dans le répertoire de déploiement et exécuter le script d'installation :

    cd aides-territoires/deployment
    ./local_vm_creation.sh

…qui effectue les actions suivantes :

- Test de la présence d'une clé publique
  - Si elle n'existe pas la générer avec la commande *ssh-keygen -t rsa* puis relancer le script
  - Si il en existe une ou plusieurs saisir le nom de la clé à utiliser (si la saisie est incorrecte le script s'interrompt)
- Création et mise à jour de la machine virtuelle LXC.
- Configuration de l'accès root ssh par clé rsa.
- Installation de python.
- Mise en place d'un répertoire partagé permettant la prise en compte du code modifié dans le répertoire de travail local.

Si tout s'est bien passé vous devez avoir une machine virtuelle presque fonctionnelle.

### Configuration de la machine hôte

Il reste quelques manipulations à effectuer qui sont expliquées à la fin du script.

Ajout d'une entrée dans le fichier `/etc/hosts`.

    <ip de la machine> aides-territoires.local

Modification du fichier `~/.ssh/config`.

    Host aides.local
        User root
        Port 22
        Hostname aides-territoires.local
        ForwardAgent yes

Création du fichier `.env.local` dans le répertoire *aides-territoires/src/*

    cp ../src/.env.example ../src/.env.local

Déploiement de l'application à l'aide d'ansible.

    ansible-playbook -i hosts -l local site.yml

Une fois ces étapes réalisées, votre version de dev sera accessible à l'adresse :

https://aides-territoires.local/

En vous connectant à cette adresse, vous accéderez à Nginx en frontal, dans une
configuration très similaire à ce qui existe en recette et production.

### Serveur de développement

Afin de bénéficier des fonctionnalités proposées par le serveur de développement de django, il faut effectuer quelques opérations manuelles, à répéter à chaque
démarrage de la VM :

    ssh aides.local
    supervisorctl stop aides
    su - aides
    source ~/.virtualenvs/aides/bin/activate
    cd aides/src
    python manage.py runserver 0.0.0.0:8000

La version de dev du site sera alors accessible à cette adresse :

http://aides-territoires.local:8000/

Il sera nécessaire de mettre à jour la base de données à partir d'un dump récent.

### Serveur de développement pour les minisites (pages personnalisées)

Dans le fichier .env.local il est nécessaire d'ajouter comme ALLOWED_HOSTS :

    francemobilites.aides-territoires.local

Le serveur peut ensuite être démarré avec la commande :

    ./manage.py runserver 0:8000 --settings minisites.settings.local

La version dev du minisite sera alors accessible à cette adresse :

http://francemobilites.aides-territoires.local:8000/

### Lancement des tests

Pour lancer les tests depuis la machine virtuelle il est nécessaire que l'utilisateur `postgres` donne l'autorisation à l'utilisateur `aides` de créer une base de données :

    su - postgres
    psql alter user aides createdb

Il faut aussi installer l'extension pg_trgm :

    psql -d template1 -c 'CREATE EXTENSION IF NOT EXISTS pg_trgm;' -U postgres
    psql -d template1 -c 'CREATE EXTENSION IF NOT EXISTS unaccent;' -U postgres
    psql -d template1 -c 'CREATE EXTENSION IF NOT EXISTS btree_gin;' -U postgres
    psql -d template1 -c 'CREATE TEXT SEARCH CONFIGURATION french_unaccent( COPY = french ); ALTER TEXT SEARCH CONFIGURATION french_unaccent ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;' -U postgres

En suivant l'utilisateur `aides` peut lancer les tests :

    su - aides
    cd aides/src
    make test
