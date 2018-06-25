# AIDES-TERRITOIRES

`Identifiez en quelques clics toutes les aides disponibles sur votre territoire pour vos projets d'aménagement durable.`

Il s'agit d'un mono-repository qui contient 3 projets :

- **site** : le site vitrine visible https://www.aides-territoires.beta.gouv.fr/ , généré statiquement par Next.js (React avec rendu serveur pour le SEO)
- **react-app** : l'application de recherche d'aides, qui est disponible sur https://recherche.aides-territoires.beta.gouv.fr/
- server : https://api.aides-territoires.beta.gouv.fr/ le serveur node fournissant les webservices / API en GraphQL consommés par la recherche de **react-app**

## Getting started

```
git clone https://github.com/MTES-MCT/aides-territoires
cd aides-territoires
```

### server : installer les webservices GraphQL

#### pré-requis

Node js ^8.9.3 est requis.

#### installation

Attention : le serveur dépend, pour la dev ou pour la prod, d'un fichier .env
qui contient des variables secrètes pour des services externes, ni la dev ni la prod ne peuvent tourner correctement sans ce fichier.

```sh
cd server
yarn install
# configurer les variables d'environnement : copier coller le fichier
# d'exemple et renseigner les variables secrètes
cp .env.example .env
# lancer le serveur de dev
yarn dev
# le serveur écoute sur http://localhost:8100/
```

#### mettre en production

Pour lancer serveur de production, utiliser "yarn start".
En coulisse, il lance pm2 qui va lancer un process node par CPU disponible et
faire un load-balancing entre ces différents process

```sh
cd server
yarn install
yarn start
```

### react-app : installer l'application React de recherche

```sh
cd react-app
yarn install
yarn dev
# le serveur écoute sur http://localhost:3000/
```

Les composants réutilisables sont dans le storybook

```sh
yarn storybook
# se rendre sur http://localhost:9009/ pour voir le storybook
```

#### mettre en production

```sh
cd react-app
yarn install
yarn build
```

Le code compilé se retrouve dans le dossier **build**
Ce répertoire peut ensuite être déployé et servi par le serveur http de votre choix

### site : installer le site vitrine

Le site est généré statiquement par Next.js (du React exporter en html pour le SEO )

#### pré-requis

Node js ^8.9.3 est requis.

#### installation

```sh
cd site
# yarn est utilisé comment gestionnaire de paquet
npm install yarn -g
yarn install
yarn dev
```

#### mettre en production

Générer le site statique dans un dossier "out"

```sh
cd site
yarn install
yarn export
```

Le code compilé se retrouve dans le dossier **out**
Ce répertoire peut ensuite être déployé et servi par le serveur http de votre choix
