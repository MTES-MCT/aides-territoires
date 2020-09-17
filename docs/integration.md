# Intégration du site en Iframe

Il est possible d'intégrer le moteur de recherche d'Aides-territoires sur votre propre site dans une iframe.

## Tutoriel d'intégration

Pour ce faire :

 1. rendez-vous sur [le moteur de recherche d'Aides-territoires](https://aides-territoires.beta.gouv.fr/aides/) ;
 1. sélectionnez les filtres de recherche tels que vous souhaitez les voir apparaître sur votre site ;
 1. copiez l'url complète de la recherche ;
 1. créez une page dédiée sur votre site ;
 1. embarquez le code suivant à l'emplacement approprié, en remplaçant l'url (balise `src`) par celle que vous avez copié précédemment ;
 1. donnez une valeur non-nulle à la variable `integration`.

```html
<iframe
    style="width: 100%; border: 0; height: 1600px;"
    name="Aides-territoires"
    src="https://aides-territoires.beta.gouv.fr/aides/?integration=integration&perimeter=70960-guyane">
</iframe>
```

## Considérations techniques

Le moteur de recherche d'Aides-territoires dispose d'une conception adaptative (*responsive design*).

Cela signifie que la largeur du moteur s'adaptera à la largeur de l'iframe telle que vous la définirez.
