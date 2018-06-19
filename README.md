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

### react-app : installer l'application React de recherche

```sh
cd react-app
yarn install
# lancer le serveur de dev
yarn dev
# le serveur écoute sur http://localhost:3000/
```

Les composants réutilisables sont dans le storybook

```sh
yarn storybook
# se rendre sur http://localhost:9009/ pour voir le storybook
```

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

#### Générer le site statique dans un dossier "out"

```sh
# à la racine du répertoire:
yarn export
# le code html est alors généré dans le dossier "out".
# il suffit de servir ces fichiers avec le serveur http de votre choix
```
