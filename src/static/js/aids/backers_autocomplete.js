$(document).ready(function () {
    $('select#id_backers').select2({
        placeholder: "Tous les porteurs d’aide",
        minimumInputLength: 3,
        language: {
            inputTooShort: function () { return "Saisissez quelques caractères pour des suggestions."; },
        },
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
            data: function (params) {
                let query = {
                    q: params.term,
                    has_published_financed_aids: true,
                    page: params.page || 1
                }
                return query;
            },
            processResults: function (data, params) {
                params.page = params.page || 1;

                return {
                    results: data.results,
                    pagination: {
                        more: data.next != null
                    }
                };
            }
        },
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "auto",
    })
        .on('select2:close', show_number_of_selected)
        .each(show_number_of_selected);
});
