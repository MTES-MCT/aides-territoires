$(document).ready(function () {

    $('select#id_project_types').select2({
        placeholder: "Sélectionnez un type de projet",
        language: {
            inputTooShort: function () { return "Sélectionnez un type de projet"; },
        },
        minimumInputLength: 0,
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
        dropdownAutoWidth: true,
        width: "auto",
    });
});