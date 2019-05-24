$(document).ready(function () {

    $('#id_scale').select2({
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
        placeholder: catalog.scale_placeholder,
    });

    $('#id_targeted_audiances').select2({
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
        placeholder: catalog.targeted_audiances_placeholder,
    });
});