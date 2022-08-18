$(document).ready(function () {

    var newOption = new Option("lali", false, false);
    $('select#id_text').append(newOption).trigger('change');

    $('select#id_text').select2({
        placeholder: catalog.text_placeholder,
        allowClear: true,
        tags: true,
        language: 'fr',
        selectOnClose: true,
        minimumInputLength: 1,
        selectOnBlur: true,
        language: {
            inputTooShort: function () { return ''; },
        },
        ajax: {
            url: catalog.text_url,
            dataType: 'json',
            delay: 100,
            data: function (params) {
                var query = {
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
