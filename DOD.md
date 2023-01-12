# Définition du fini

Ce document liste les éléments à vérifier afin de déclarer qu'une
fonctionnalité est terminée et peut être déployée.

  - [ ] La *feature* est couverte par des tests automatisés
    - [ ] L'ensemble des tests passent sans erreurs
  - [ ] Tous les éléments présents dans le code sont en anglais
  - [ ] Tous les éléments textuels s'affichent en français
  - [ ] Si des modèles ont été modifiés, l'API est-elle toujours fonctionnelle ?
  - [ ] L'application est conforme au [RGAA v4.1](https://accessibilite.numerique.gouv.fr/) 
    - [ ] Les éléments de contenus non-textuels sont assortis d'équivalents textuels
    - [ ] Les éléments sont visuellement perceptibles, notamment en utilisant des contrastes suffisants et en ne communiquant pas d'information uniquement par la couleur
    - [ ] Le balisage sémantique est correctement utilisé (e.g utiliser résumé pour les tableaux, les bonnes balises pour indiquer les colonnes d'entêtes, etc.)
    - [ ] L'application est utilisable au clavier
    - [ ] L'information est présentée de manière cohérente et structurée, en utilisant un balisage sémantiques (hx, sections, nav, etc.)
    - [ ] L'application reste utilisable avec un agrandissement de police de 200%
    - [ ] Les formulaires sont correctement balisés (utilisation de labels, intitulés des boutons explicites)
  - [ ] La navigation est facilitée (fil d'Ariane, contenus faciles à trouver, pas d'imbrication trop profondes des pages, etc.)
  - [ ] L'application est conforme au RGPD
    - [ ] Les données personnelles collectées sont pertinentes et nécessaires au fonctionnement du service
    - [ ] Les données sont collectées après recueil d'un consentement explicite de l'usager·e
    - [ ] L'usager·e est informé·e de l'utilisation qui sera faite des données collectées
    - [ ] L'usager·e dispose d'un moyen de consulter / rectifier / supprimer ses données
    - [ ] L'application ne génère pas de requête http vers un autre domaine (trackers)
