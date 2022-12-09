# Contribuer à Aides-territoires

## Installation

Une documentation détaillée de l'installation en local est disponible sur [ONBOARDING.md](./ONBOARDING.md).

```
git clone https://github.com/MTES-MCT/aides-territoires
cd aides-territoires
```

## Tests

Pour faire tourner les tests :

```
cd src && make test
```

Note : certains tests utilisent [Selenium](https://selenium-python.readthedocs.io/index.html)
qui dépend de [geckodriver](https://firefox-source-docs.mozilla.org/testing/geckodriver/geckodriver/).

Pour les faire tourner, il conviendra donc d'en télécharger
[la dernière version](https://github.com/mozilla/geckodriver/releases) pour
l'intégrer dans son `$PATH`.

GeckoDriver s'attend à trouver Firefox installé.

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

En staging et en production, les variables d'environments sont spécifiées directement sur Scalingo.

## CSS, Sass et compression

### Maintenir le code HTML propre

Le projet utilise [Le Système de Design de l'Etat](https://gouvfr.atlassian.net/wiki/spaces/DB/overview) pour faciliter le développement, proposer un rendu homogène. 

Les intervenant·es sur le code sont donc *prié·es d'utiliser autant que possible les classes
spécifiques au Système de Design de l'Etat dans le HTML.

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

 * Installer [la version native de Sassc](https://github.com/sass/sassc) et pas
   la version en pure js (sous ubuntu: `sudo apt-get install sassc`);
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

_Note : les traductions ont été abandonnées et sont progressivement supprimées._

Ce project utilise le système de traduction de Django :
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

Nous utilisons `pep8`, `flake8` et `black`

Pour vérifier son code, on peut intégrer le linter adapté à
son IDE et aussi faire ceci :

    make checkstyle

## Déploiement

### Variables d'environnement

En staging et en production, les variables d'environments sont spécifiées directement sur Scalingo.

### Envoi d'email

Les emails transactionnels sont envoyés via SendingBlue.
Pour les environnements de Staging, il existe un mécanisme qui permet de n'envoyer les emails qu'à une liste restreinte d'adresses.
Cette "Whitelist" est définie dans les `settings`.
Pour connaître le fonctionnement historique de ce filtrage : https://github.com/MTES-MCT/aides-territoires/pull/399

En local vous avez la possibilité de visualiser les emails dont le template n'est pas hébergé sur SendinBlue depuis votre shell. Pour ce faire la variable `EMAIL_BACKEND` doit être définie avec `django.core.mail.backends.console.EmailBackend` dans votre fichier `.env.local`

### Fichiers media

Nous utilisons un service d'« Object Storage » compatible avec l'API S3 pour le stockage de tous les fichiers medias.

### Double authentification

Pour mettre en place la double authentification, il faut mettre ceci dans le
fichier `.env` ou dans les variables d'environnement Scalingo :

    ADMIN_OTP_ENABLED=True

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

Le site est actuellement hébergé sur Scalingo. Cf. la documentation d'infogérance.

Note : demander l'accès au moment de l'*onboarding*.
