$(document).ready(function () {
    $('select#id_targeted_audiences').select2({
        placeholder: catalog.autocomplete_placeholder,
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth : true,
        width: "auto",
    });
});
