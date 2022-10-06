$(document).ready(function () {

    $('select#id_project_types').select2({
        placeholder: catalog.project_types_placeholder,
        language: {
            inputTooShort: function() { return catalog.project_types_placeholder; },
        },
        minimumInputLength: 3,
        ajax: {
            url: catalog.project_types_url,
            dataType: 'json',
            delay: 100,
            data: function (params) {
                let query = {
                    q: params.term,
                }
                return query;
            },
            processResults: function (data, params) {
                params.page = params.page || 1;

                return {
                    results: data,
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
});