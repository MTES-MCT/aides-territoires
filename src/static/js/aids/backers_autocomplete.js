let backersAutocomplete = new SlimSelect({
    select: '#id_backers',
    settings: {
        placeholderText: 'Tous les porteurs d’aide',
        searchPlaceholder: 'Rechercher',
        searchingText: 'Recherche…',
        searchText: 'Tapez quelques caractères',
        maxValuesShown: 1,
        maxValuesMessage: '{number} valeurs choisies',
        allowDeselect: true
    },
    events: {
        search: (search, currentData) => {
            return new Promise((resolve, reject) => {
                if (search.length < 2) {
                    return reject('Tapez au moins 2 caractères')
                }

                let apiUrl = '/api/backers/?has_published_financed_aids=true&q=' + search
                fetch(apiUrl)
                    .then((response) => response.json())
                    .then((data) => {
                        const options = data.results
                            .map((entry) => {
                                return {
                                    text: entry.text,
                                    value: entry.id
                                }
                            })
                        console.log(options);
                        resolve(options)
                    })
                    .catch((error) => {
                        console.error(error);
                    })
            })
        }
    },
})