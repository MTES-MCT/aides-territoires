# AIDES-TERRITOIRES

[![Build Status](https://travis-ci.com/MTES-MCT/aides-territoires.svg?branch=master)](https://travis-ci.com/MTES-MCT/aides-territoires)

Identifiez en quelques clics toutes les aides disponibles sur votre territoire
pour vos projets d'aménagement durable.

Dépôt du projet Aides-territoires : https://aides-territoires.beta.gouv.fr/


## Démarrage

```
git clone https://github.com/MTES-MCT/aides-territoires
cd aides-territoires
```


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
