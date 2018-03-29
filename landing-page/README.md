# aides territoires - landing page

Code pour http://www.aides-territoires.beta.gouv.fr

## installation

Le site est propulsé par Next.js (React avec SSR).
Il faut donc avoir _node js_ d'installé.

_Yarn_ est utilisé comment gestionnaire de paquet

_pm2_ est utilisé pour la gestion des process node

```sh
npm install yarn -g
npm install pm2 -g
```

## compiler le code et servir sur le port 3000

```sh
# compilation
yarn build
# servir (utilise pm2)
yarn start
```

# Mettre en production

sur le serveur :

```sh
# s'assurer que le répertoire est clean
git checkout .
# récupérer les dernières modif
git pull --rebase
# compiler le code
yarn build
# démarrer le process node.
# Inutile si le process node est déjà démarré.
yarn start
```
