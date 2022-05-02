$(document).ready(function () {
    $('select#id_programs').select2({
        placeholder: catalog.programs_placeholder,
        language: 'fr',
        theme: "select2-dsfr",
        dropdownAutoWidth : true,
        width: "auto",
    });
    $(".select2-container").addClass("fr-select-group");
    $(".select2-selection").addClass("fr-select");
});
