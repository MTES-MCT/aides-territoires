$(document).ready(function () {
    $('select#id_programs').select2({
        placeholder: catalog.programs_placeholder,
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth : true,
        width: "100%",
    });
});
