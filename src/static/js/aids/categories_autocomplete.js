$(document).ready(function () {
    $("select#id_categories").select2({
        placeholder: catalog.autocomplete_placeholder,
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth : true,
        width: "auto",
    });
});
