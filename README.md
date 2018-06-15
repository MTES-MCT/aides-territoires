# AIDES-TERRITOIRES

`Identifiez en quelques clics toutes les aides disponibles sur votre territoire pour vos projets d'aménagement durable.`

Il s'agit d'un mono-repository qui contient 3 projets :

- site : le site vitrine visible https://www.aides-territoires.beta.gouv.fr/ , généré statiquement par Next.js (React avec rendu serveur pour le SEO)
- react-app : l'application de recherche d'aides, qui est disponible sur https://recherche.aides-territoires.beta.gouv.fr/
- server : https://api.aides-territoires.beta.gouv.fr/ le serveur node fournissant ls webservices / API en GraphQL consommées par la recherche de react-app

Chaque répertoire dispose de son propre README concernant l'installation et le déploiement.

## Getting started

```
git clone git@github.com:MTES-MCT/aides-territoires.git
```

Installer les serveur GraphQL

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

installer l'application React de recherche

```sh
cd react-app
yarn install
# lancer le serveur de dev
yarn dev
# le serveur écoute sur http://localhost:3000/
```

## Support Navigateur

Firefox : >= 40
