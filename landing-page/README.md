# aides territoires - landing page

## installation

```
npm i yarn
```

## build and serve

build landing page and start to server on port 3000

```
cd landing-page
yarn build
yarn start
```

start landing page on port 3000

```
cd server
yarn start
```

# Deploy

```sh
# faire un build sur le serveur local
# le fichier "build" est versionné pour permettre de tester en local
# avant de le déployer
yarn build
yarn start

# si tout est ok, plus qu'à récupérer le code sur le serveur de prod
# on clean les éventuelles modifs qui empecherait un rebase correct :
git checkout .
# on récupère notre code
git pull --rebase
# installer les paquets qui aurait pu être installées entre temps
yarn install
```
