$(document).ready(function () {

    $('select#id_text').select2({
        placeholder: catalog.text_placeholder,
        allowClear: true,
        tags: true,
        language: 'fr',
        selectOnClose: true,
        minimumInputLength: 1,
        ajax: {
            url: catalog.text_url,
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
});
