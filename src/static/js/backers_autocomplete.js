/**
 * Handle the code related to the financer and instructor fields.
 *  - create the autocomplete fields using select2
 */

$(document).ready(function () {

    $('select#id_financers').select2({
        placeholder: catalog.financers_placeholder,
        language: 'fr',
        minimumInputLength: 2,
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
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

    $('select#id_instructors').select2({
        placeholder: catalog.instructors_placeholder,
        language: 'fr',
        minimumInputLength: 2,
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
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
