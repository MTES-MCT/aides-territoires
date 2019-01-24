$(document).ready(function () {

    $('#id_aid_types').select2({
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
        placeholder: catalog.aid_types_placeholder,
    });
    $('#id_mobilization_step').select2({
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
        placeholder: catalog.mobilization_steps_placeholder,
    });
    $('#id_destinations').select2({
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
        placeholder: catalog.destinations_placeholder,
    });
    $('#id_scale').select2({
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
        placeholder: catalog.scale_placeholder,
    });
});