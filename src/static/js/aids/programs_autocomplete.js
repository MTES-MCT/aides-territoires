$(document).ready(function () {
    $('select#id_programs').select2({
        placeholder: catalog.programs_placeholder,
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
    });
});
