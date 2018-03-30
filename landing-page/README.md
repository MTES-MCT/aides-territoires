# aides territoires - landing page

Code pour http://www.aides-territoires.beta.gouv.fr
Le site est propulsé par Next.js ( Application React universelle ).

## pré-requis

Node js ^8.9.3 est requis.

## installation

```sh
# yarn est utilisé comment gestionnaire de paquet
npm install yarn -g
# pm2 est utilisé pour la gestion des process node
npm install pm2 -g
# install all packages
yarn install
# creer le fichier de config de l'app pour l'environnement local
# ce fichier n'est pas versionné
cp env.config.example.js env.config.gs
```

## compiler le code et servir sur le port 3000

```sh
# compilation
yarn build
# servir (utilise pm2)
yarn start
```

## en cas de souci : rédémarrer le process node

Attention, cela coupe le serveur le temps du rédémarrage !

```
yarn restart
```

## Mettre en production

### déployer

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

### exemple de configuration nginx

```
# se connecter au serveur node
upstream www.aides-territoires.beta.gouv.fr {
    server localhost:3000;
}

server {
  gzip on;
	listen 80;
	listen [::]:80;
	server_name www.aides-territoires.beta.gouv.fr;
	location / {
		proxy_pass http://www.aides-territoires.beta.gouv.fr;
	}
}
```
