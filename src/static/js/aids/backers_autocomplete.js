let backersAutocomplete = new SlimSelect({
    select: '#id_backers',
    settings: {
        placeholderText: 'Tous les porteurs d’aide',
        searchPlaceholder: 'Rechercher',
        searchingText: 'Recherche…',
        maxValuesShown: 1,
        maxValuesMessage: '{number} valeurs choisies',
        allowDeselect: true
    },
    events: {
        search: (search, currentData) => {
            return new Promise((resolve, reject) => {
                if (search.length < 3) {
                    return reject('Tapez au moins 3 caractères')
                }
                console.log(search)

                let queryPath = '/api/backers/?has_published_financed_aids: true&q=' + search

                fetch(queryPath, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }).then((response) => response.json()).then((data) => {
                    // Take the data and create an array of options
                    // excluding any that are already selected in currentData
                    const options = data.results
                        .map((entry) => {
                            return {
                                text: entry.text,
                                value: entry.id
                            }
                        })
                    console.log(options)
                    resolve(options)
                })
            })
        }
    }
})