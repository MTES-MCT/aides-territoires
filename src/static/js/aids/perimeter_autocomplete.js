$(document).ready(function () {

    // hide "custom" perimeters in the user part of the website
    var RESTRICT_TO_VISIBLE_PERIMETERS = $('#perimeter').length || $('#search-form').length || $('#advanced-search-form').length || $('#general_search_form').length;
    var RESTRICT_TO_NON_OBSOLETE_PERIMETERS = $('#perimeter').length || $('#search-form').length || $('#advanced-search-form').length || $('#general_search_form').length;

    $('select#id_perimeter').select2({
        placeholder: catalog.perimeter_placeholder,
        allowClear: true,
        language: 'fr',
        minimumInputLength: 1,
        language: {
            inputTooShort: function () { return ''; },
        },
        ajax: {
            url: catalog.perimeter_url,
            dataType: 'json',
            delay: 100,
            data: function (params) {
                var query = {
                    q: params.term,
                    is_visible_to_users: RESTRICT_TO_VISIBLE_PERIMETERS ? true : false,
                    is_non_obsolete: RESTRICT_TO_NON_OBSOLETE_PERIMETERS ? true : false,
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
        theme: 'bootstrap4',
        width: '',
    });
});
