$(document).ready(function () {
    $("select#id_categories").select2({
        placeholder: "Saisissez quelques caractères pour des suggestions.",
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "auto",
    });
});
