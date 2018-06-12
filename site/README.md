# aides territoires - landing page

Code pour http://www.aides-territoires.beta.gouv.fr
Le site est généré statiquement par Next.js

## pré-requis

Node js ^8.9.3 est requis.

## installation

```sh
# yarn est utilisé comment gestionnaire de paquet
npm install yarn -g
yarn install
```

## développer

```sh
yarn dev
```

### Générer le site statique

sur le serveur cible :

```sh
# à la racine du répertoire:
yarn export
# le code html est alors généré dans le dossier "out".
# il suffit de servir ces fichiers avec un serveur http
```

### exemple de configuration nginx
