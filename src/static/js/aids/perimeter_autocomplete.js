$(document).ready(function () {
    $('select#id_perimeter').select2({
        placeholder: catalog.perimeter_placeholder,
        language: 'fr',
        minimumInputLength: 1,
        language: {
            inputTooShort: function() { return ''; },
        },
        ajax: {
            url: catalog.perimeter_url,
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
