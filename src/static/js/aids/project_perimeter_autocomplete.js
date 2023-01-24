$(document).ready(function () {
    // hide "custom" perimeters in the user part of the website
    let RESTRICT_TO_VISIBLE_PERIMETERS = $('#project_perimeter').length || $('#perimeter').length || $('#search-form').length || $('#advanced-search-form').length || $('#register-page').length || $('#register-commune-page').length;
    let RESTRICT_TO_NON_OBSOLETE_PERIMETERS = $('#project_perimeter').length || $('#perimeter').length || $('#search-form').length || $('#advanced-search-form').length || $('#register-page').length || $('#register-commune-page').length;

    // Filter on scale on certain forms
    let scale = null;
    let RESTRICT_TO_COMMUNES = $('#register-commune-page').length
    if (RESTRICT_TO_COMMUNES) {
        scale = 'commune';
    }

    // Set the placeholder message
    let placeholder_message = "Tapez les premiers caractères"

    if ($('#search-form').length || $('#advanced-search-form').length) {
        placeholder_message = "Tous les territoires"
    }

    $('select#id_project_perimeter').select2({
        placeholder: placeholder_message,
        allowClear: true,
        minimumInputLength: 1,
        language: {
            inputTooShort: function () { return ''; },
        },
        ajax: {
            url: catalog.perimeter_url,
            dataType: 'json',
            delay: 100,
            data: function (params) {
                let query = {
                    q: params.term,
                    is_visible_to_users: RESTRICT_TO_VISIBLE_PERIMETERS ? true : false,
                    is_non_obsolete: RESTRICT_TO_NON_OBSOLETE_PERIMETERS ? true : false,
                }
                if (scale) {
                    query.scale = scale;
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
            },
        },
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "auto",
    });
});
