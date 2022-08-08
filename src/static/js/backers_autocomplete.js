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
        theme: "select2-dsfr",
        dropdownAutoWidth : true,
        width: "auto",
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
        theme: "select2-dsfr",
        dropdownAutoWidth : true,
        width: "auto",
    });
    $(".select2-container").addClass("fr-select-group");
    $(".select2-selection").addClass("fr-select");
});