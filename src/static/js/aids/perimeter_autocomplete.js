$(document).ready(function () {
    $('select#id_perimeter').select2({
        placeholder: catalog.perimeter_placeholder,
        ajax: {
            url: catalog.perimeter_url,
            dataType: 'json',
            delay: 100,
        },
        theme: 'bootstrap4',
        width: '',
    });
});