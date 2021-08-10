# Aides-territoires

[![Build Status](https://travis-ci.com/MTES-MCT/aides-territoires.svg?branch=master)](https://travis-ci.com/MTES-MCT/aides-territoires)

Dépôt du projet
[Aides-territoires.beta.gouv.fr](https://aides-territoires.beta.gouv.fr/).

Identifiez en quelques clics toutes les aides disponibles sur votre territoire
pour vos projets d'aménagement durable.

Ce document s'adresse aux intervenant·es techniques sur le projet
Aides-territoires. Pour plus d'infos en tant qu'utilisateur·ice, se reporter
[directement au site](https://aides-territoires.beta.gouv.fr/).

## Présentation du code

Vous pouvez accéder à une grossière [documentation des briques générales qui
constituent le code d'Aides-territoires](LECODE.md).

## Intégration de l'équipe « *onboarding* »

- Pour se parler sur Slack : https://aides-territoires.slack.com/
- Pour s'organiser sur Trello : https://trello.com/b/5ldc900w/aides-territoires-planification

Demandez votre inscription à la liste de diffusion tech pour recevoir les
e-mails destinés à l'équipe (alertes Sentry, erreurs Django, etc.).

## Démarrage

Les développeur·euses qui intègrent le projet et doivent
monter un environnement de développement local pourront [consulter la documentation
spécifique](./ONBOARDING.md).

```
git clone https://github.com/MTES-MCT/aides-territoires
cd aides-territoires
```

## Tests

Pour faire tourner les tests:

```
cd src && make test
```

À noter : certains tests utilisent [Selenium](https://selenium-python.readthedocs.io/index.html)
qui dépend de [geckodriver](https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/).

Pour les faire tourner, il conviendra donc d'en télécharger
[la dernière version](https://github.com/mozilla/geckodriver/releases) pour
l'intégrer dans son `$PATH`.

GeckoDriver s'attend à trouver firefox installé.

    # Firefox on debian
    apt-get update
    apt-get purge firefox-esr

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
        <a class="navbar-brand" href="…">Aides-territoires</a>
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
        <a class="homelink" href="…">Aides-territoires</a>
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


## Utilisation de Redis

Nous utilisons Redis en production :

- Comme backend de cache pour Django
- Comme broker pour Celery

En locale et pour les Review Apps, il n'y a généralement pas besoin
d'utiliser Redis.


## Traduction : À propos des fichiers `.po` et `.mo`

Ce project utilise le système de tranduction de Django :
Le texte dans le code est en anglais et la traduction qui
s'affiche sur le site en Français, se trouve dans le fichier
`.po` du dossier `locales`.

https://docs.djangoproject.com/en/dev/topics/i18n/translation/

Pour générer la traduction dans le fichier `.po` :

    make makemessages


Django utilise une version compilée du fichier `.po`, c'est le
fichier `.mo` que l'on obtient avec :

    python manage.py compilemessages


En production, ce fichier est généré automatiquement lors du
déploiement. Il n'est donc pas inclus dans le code github.

## Linter de code / Code Style

Nous utilisons `pep8` et `flake8`.

Pour vérifier son code, on peut intégrer le linter adapté à
son IDE et aussi faire ceci :

    make checkstyle


## Déploiement


### Variables d'environnement

Afin de rendre disponible les variables d'environnement dans les playbooks
ansible, nous utilisons le fichier `.env.ansible`.


    # Pour créer le fichier env:
    cp .env.ansible.example .env.ansible

Ce fichier est chargé grâce au script `ansible-playbook-dotenv.sh` qui est
lui-même appelé dans le script `deploy.py`.


### Slack webhook

Ansible lance une notification après le déploiement. Pour cela,
il faut installer ceci:

    ansible-galaxy collection install community.general


### Envoi d'email

Les emails transactionnels sont envoyés via SendingBlue.
Pour les environnements de Staging, il un mécanisme qui permet de
n'envoyer les emails qu'à une liste restreinte d'adresses.
Cette "Whitelist" est définie dans les `settings`.Pour connaître le fonctionnement historique de ce filtrage : https://github.com/MTES-MCT/aides-territoires/pull/399


### Fichiers media

Nous utilisons un service d'« Object Storage » compatible avec l'API S3 pour le stockage de tous les fichiers medias.


### Double authentification

Pour mettre en place la double authentification, il faut mettre ceci dans le
fichier `.env` ou dans les variable d'environnement Scalingo :

    ADMIN_OTP_ENABLE=True

Ceci va activer une double authentification pour l'accès au site d'admin :
mot de passe et jeton d'authentification.
Le jeton d'authentification peut-être obtenu via une application mobile comme
Google Authenticator ou Authy.

Lors de la première utilisation et avant d'activer la double authentification,
il faudra faire en sorte qu'un premier utilisateur admin puisse se connecter.
Pour cela, il faudra penser à créer un `Device` pour cet utilisateur initial,
avec le QR code associé qu'il faudra scanner avec l'application mobile.

Pour plus de détail : https://django-otp-official.readthedocs.io/en/stable/overview.html

### Mise en production

Le site est actuellement hébergé sur Scalingo. Cf. la documentation
d'infogérance.

Note : demander l'accès au moment de l'*onboarding*.
