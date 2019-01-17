# Aides-territoires

[![Build Status](https://travis-ci.com/MTES-MCT/aides-territoires.svg?branch=master)](https://travis-ci.com/MTES-MCT/aides-territoires)

Dépôt du projet
[Aides-territoires.beta.gouv.fr](https://aides-territoires.beta.gouv.fr/).

Identifiez en quelques clics toutes les aides disponibles sur votre territoire
pour vos projets d'aménagement durable.

Ce document s'adresse aux intervenant·es techniques sur le projet
Aides-territoires. Pour plus d'infos en tant qu'utilisateur·ice, se reporter
[directement au site](https://aides-territoires.beta.gouv.fr/).

## Intégration de l'équipe « *onboarding* »

Les développeur·euses qui intègrent le projet et doivent
monter un environnement de développement local pourront [consulter la documentation
spécifique](./ONBOARDING.md).

## Démarrage

```
git clone https://github.com/MTES-MCT/aides-territoires
cd aides-territoires
```


## Définition du fini

Avant chaque mise en production, les intervenant·es sont prié·es de [passer
cette liste en revue](./DOD.md).


## Gestion des dépendances avec Pipenv

Le projet utilise [Pipenv pour gérer les dépendances de paquets
Python](https://pipenv.readthedocs.io/en/latest/) et produire des *builds*
déterministes.

Pour installer les dépendances du projet :

    pipenv install --dev

Pour installer un nouveau paquet et l'ajouter aux dépendances :

    pipenv install <paquet>

Pour un paquet ne servant que pour le développement, e.g *debug-toolbar* :

    pipenv install --dev <paquet>


## Configuration locale, production

Le projet utilise [django-environ](http://django-environ.readthedocs.io/) pour
gérer les settings des différents environnements ne pouvant être embarquées
dans le dépôt git.

Typiquement :

 * configuration locale spécifique à chaque intervenant·e sur le projet, e.g
   paramètres de connexion à la base de données ;
 * configuration de production.

Pour surcharger la configuration locale de développement, il est possible de
créer un fichier `.env.local` à la racine du projet Django. Cf. [le fichier
.env.example](./src/.env.example) pour l'exemple. Ce fichier est facultatif car
des paramètres par défaut sont définis.

En revanche, pour un déploiement en production, la définition d'un fichier
`.env.production` est *obligatoire*.


## CSS, Sass et compression

### Maintenir le code HTML propre

Le projet utilise [Bootstrap](http://getbootstrap.com/) pour faciliter le
développement et proposer un rendu homogène. Toutefois, c'est la version Sass
du framework css qui est utiliséee, afin d'éviter de pourrir le code HTML de
classes non-sémantiques.

Les intervenant·es sur le code sont donc *prié·es de ne pas utiliser de classes
spécifiques à Bootstrap dans le HTML*, mais d'utiliser des classes et ids
sémantiques.

Incorrect : 

```html
<nav class="navbar navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="…">Aides-Territoires</a>
        <ul class="navbar-nav mr-auto">
            <li class="nav-item"><a class="nav-link" href="…">Lien</a></li>
        </ul>
        <span class="text-right navbar-text">Beta</span>
    </div>
</nav>
```

Correct :

```html
<nav id="main-navbar">
    <div class="container">
        <a class="homelink" href="…">Aides-Territoires</a>
        <ul class="homenav">
            <li><a href="…">Lien</a></li>
        </ul>
        <span>Beta</span>
    </div>
</nav>
```

```css
nav#main-navbar {
    @extend .navbar;
    @extend .navbar-dark;
    @extend .bg-dark;

    .homelink {
        @extend .navbar-brand;
    }

    ul.homenav {
        @extend .navbar-nav;
        @extend .mr-auto;

        li {
            @extend .nav-item;

            a {
                @extend .nav-link;
            }
        }
    }

    span {
        @extend .text-right;
        @extend .navbar-text;
    }
}
```

### Utilisation de django-compressor

Le projet utilise
[django-compressor](https://django-compressor.readthedocs.io/), une application
qui permet de gérer la `pipeline` de compression des fichiers statiques.

[Django-compressor propose plusieurs modes de
déploiement](https://django-compressor.readthedocs.io/en/latest/scenarios/) :

 1) la compilation / compression se fait manuellement une fois pour toute ;
 2) la compilation / compression se fait automatiquement à chaque requête.

Le premier mode de fonctionnement est adapté à un déploiement en production. Le
second dans un environnement de développement.

Il faut noter que le second mode peut significativement dégrader les
performances et ralentir le travail. Pour améliorer les performances, deux
possibilités :

 * Installer [la version native de Sass](http://sass-lang.com/install) et pas
   la version en pure js ;
 * Désactiver en local la compression par requête dans le fichier `.env.local`.

```
COMPRESS_OFFLINE=False
```

Il faudra alors manuellement lancer la compression en cas de besoin.

    python manage.py compress


## Déploiement

Le déploiement se fait avec
[Ansible](https://docs.ansible.com/ansible/latest/index.html) et ne nécessite
qu'une commande.

À la racine du dépôt git:

```
ansible-playbook deployment/site.yml
```

[Plus de détails dans le répertoire
spécifique.](deployment/)
