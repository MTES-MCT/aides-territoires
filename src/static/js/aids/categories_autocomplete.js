$(document).ready(function () {
    $('select#id_categories').select2({
        placeholder: catalog.autocomplete_placeholder,
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
    });
});
