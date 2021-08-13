# Aides-territoires

[![Build Status](https://travis-ci.com/MTES-MCT/aides-territoires.svg?branch=master)](https://travis-ci.com/MTES-MCT/aides-territoires)

**Identifiez en quelques clics toutes les aides disponibles sur votre territoire
pour vos projets d'aménagement durable.**

Dépôt de code de la startup d'état **Aides-territoires** incubée à la Fabrique Numérique du MTES-MCT.

Ce `README` s'adresse plutôt aux intervenant·es techniques sur le projet.
Pour plus d'infos en tant qu'utilisateur·ice du produit ou de l'API, vous pouvez consulter les liens suivants :

- [Site web](https://aides-territoires.beta.gouv.fr/)
- [Documentation technique de l'API](https://aides-territoires.beta.gouv.fr/data/)

## Les rôles utilisateurs

Aides-territoires s'adresse principalement à trois types d'utilisateurs (personas) :

 - les **chercheurs d'aides** ;
 - les **porteurs d'aides** ;
 - les **admins**.

### Chercheurs d'aides

Les chercheurs d'aides sont les principaux « clients » du service offert par
Aides-territoires. Il s'agit des personnes qui utilisent le site pour
trouver des aides pour leurs projets.

Les chercheurs d'aides peuvent accéder aux fonctionnalités suivantes :

  - utiliser le moteur de recherche pour trouver des aides pertinentes ;
  - créer des alertes pour recevoir par email de nouveaux résultats
    correspondant à une recherche donnée ;
  - suggérer des modifications sur une fiche d'aide.

Les chercheurs d'aides sont des utilisateurs anonymes et n'ont pas besoin de
créer de compte.

### Porteurs d'aides

Les porteurs d'aides sont les personnes ou organisations qui publient des
aides sur Aides-territoires.

Les porteurs d'aides doivent créer un compte et remplir leur profil pour être
identifiés comme tels.

Les porteurs d'aides ont accès aux fonctionnalités suivantes :

  - accès à une interface de contribution (édition / publication d'aides) ;

 ### Admins

Les admins sont les membres d'Aides-territoires qui ont accès à l'interface
d'admin Django, et peuvent administrer les différentes données.

  - éditer les aides ;
  - saisir de nouvelles aides ;
  - publier ou dépublier les aides ;
  - accepter les suggestions de modifications sur les aides ;
  - créer des « minisites », des pages de recherche personnalisées ;
  - administrer les différentes données (catégories, etc.)

## Fonctionnalités principales

La liste des « gros morceaux » ou fonctionnalités principales à connaître :

  - création, édition, publication d'aides ;
  - recherche d'aides en 4 étapes ;
  - présentation du résultat des aides et filtre rapide ;
  - moteur de recherche avancé « plus de critères » ;
  - critère « périmètre » dans la recherche ;
  - possibilité d'amender une aide ;
  - interface de comparaison entre l'aide et ses amendements ;
  - création de « minisites » ;
  - scripts de mise à jour des périmètres

## Architecture et organisation du projet

Le projet est structuré comme un projet Django classique, découpé en applications.

L'utilité de chaque application est décrite dans son fichier `__init__.py`.

Certaines données de projet sont accessible depuis une API. L'API est en lecture seule.

Retrouvez plus d'informations sur les pages suivantes :

  - en savoir plus sur le code et comment contribuer ? [CONTRIBUTING.md](./ONBOARDING.md)
  - installer l'environment en local ? [ONBOARDING.md](./ONBOARDING.md)

## Une question ?

Un formulaire de contact est disponible [ici](https://aides-territoires.beta.gouv.fr/contact/).

Si le sujet est purement technique, vous pouvez aussi créer une _Issue_.
