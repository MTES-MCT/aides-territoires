# Aides-territoires

**Identifiez en quelques clics toutes les aides disponibles sur votre territoire pour vos projets d'aménagement durable.**

Dépôt de code de la startup d'état **Aides-territoires** incubée à la Fabrique Numérique du MTES-MCT.

Ce `README` s'adresse plutôt aux intervenant·es techniques sur le projet.
Pour plus d'infos en tant qu'utilisateur·ice du produit ou de l'API, vous pouvez consulter les liens suivants :

- [Site web](https://aides-territoires.beta.gouv.fr/)
- [Documentation technique de l'API](https://aides-territoires.beta.gouv.fr/data/)

## Les rôles utilisateurs

Aides-territoires s'adresse principalement à trois types d'utilisateurs (personas) :

 - les **chercheurs d'aides**
 - les **porteurs d'aides**
 - les **admins**.

### Chercheurs d'aides

Les chercheurs d'aides sont les principaux « clients » du service offert par
Aides-territoires. Il s'agit des personnes qui utilisent le site pour
trouver des aides pour leurs projets.

Les chercheurs d'aides peuvent accéder aux fonctionnalités suivantes :

  - utiliser le moteur de recherche pour trouver des aides pertinentes
  - créer des alertes pour recevoir par email de nouveaux résultats
    correspondant à une recherche donnée
  - suggérer des modifications sur une fiche d'aide.

Les chercheurs d'aides sont des utilisateurs anonymes et n'ont pas besoin de
créer de compte.

### Porteurs d'aides

Les porteurs d'aides sont les personnes ou organisations qui publient des
aides sur Aides-territoires.

Les porteurs d'aides doivent créer un compte et remplir leur profil pour être
identifiés comme tels.

Les porteurs d'aides ont accès aux fonctionnalités suivantes :

  - une interface de contribution (édition / publication d'aides)

 ### Admins

Les admins sont les membres d'Aides-territoires qui ont accès à l'interface
d'admin Django, et peuvent administrer les différentes données.

  - éditer les aides
  - saisir de nouvelles aides
  - publier ou dépublier les aides
  - accepter les suggestions de modifications sur les aides
  - créer des « minisites », des pages de recherche personnalisées
  - administrer les différentes données (catégories, etc.)

## Fonctionnalités principales

La liste des « gros morceaux » ou fonctionnalités principales à connaître :

  - création, édition, publication d'aides
  - recherche d'aides (avec filtres par type de bénéficiaire, périmètre, mots clés ou thématique)
  - présentation du résultat des aides et filtre rapide
  - moteur de recherche avancé « plus de critères »
  - création de « portails »
  - création et gestion de projets
  - publication de projets et suggestion d'aides pour des projets publics
  - création d'alertes à partir d'une recherche
  - test d'éligibilité sur certaines aides
  - import d'aides par Excel, CSV ou API
  - une API pour récupérer les données d'Aides-territoires

## Aspects techniques

### Architecture

Le produit est développé en Django (Python).
Il est structuré comme un projet Django classique, découpé en applications.

La base de données utilisée est PostgreSQL.
Redis nous sert aussi à accélérer les requêtes (caching), il sert aussi de broker pour les tâches de fond (Celery),
et pour compter les tentatives infructueuses de connexion (Defender).

Certaines données de projet sont accessible depuis une API. L'API est en lecture seule.

L'interface utilise des templates HTML, avec le système de design de l'État et un peu de Javascript via jQuery.

### Le code

Pour en savoir plus sur le code et comment contribuer : [CONTRIBUTING.md](./CONTRIBUTING.md)

Les étapes pour installer l'environment en local : [ONBOARDING.md](./ONBOARDING.md)

### Infrastructure

L'application est hébergée chez [Scalingo](https://scalingo.com/fr).

Les fichiers statiques (images, documents) sont chez [Scaleway](https://www.scaleway.com/fr/).

### Outillage

- [Github](https://github.com/) pour l'hébergement du code et l'intégration continue
- [Sentry](https://sentry.io) pour le reporting des erreurs
- [Brevo](https://www.brevo.com/fr/) pour l'envoi d'emails
- [AlwaysData](https://www.alwaysdata.com/fr/) pour la gestion des DNS
- [Metabase](https://www.metabase.com/) pour l'analyse et la visualisation des données
- [Matomo](https://fr.matomo.org/) pour l'analyse du traffic web
- [Updown](https://updown.io/) pour la page de statuts et les alertes

### Monitoring

[Statut du service](https://updown.io/tqz4?locale=fr)

## Une question ?

Un formulaire de contact est disponible [ici](https://aides-territoires.beta.gouv.fr/contact/).

Si le sujet est purement technique, vous pouvez aussi créer une _Issue_.
