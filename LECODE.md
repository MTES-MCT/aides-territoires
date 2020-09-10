# Le dépôt Aides-territoires

Cette documentation s'adresse aux personnes qui veulent comprendre comment est
architecturé le projet, et comprendre comment fonctionne le code de manière
globale.

## Les rôles utilisateurs

Au niveau du développement, Aides-territoires s'adresse principalement à trois
types d'utilisateurs (personas) :

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
