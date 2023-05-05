let categoriesAutocomplete = new SlimSelect({
    select: '#id_categories',
    settings: {
        placeholderText: 'Toutes les thématiques',
        searchPlaceholder: 'Rechercher',
        searchingText: 'Recherche…',
        maxValuesShown: 1,
        maxValuesMessage: '{number} valeurs choisies',
        allowDeselect: true
    },
})