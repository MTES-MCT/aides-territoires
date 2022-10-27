$(document).ready(function () {
    $('select#id_targeted_audiences').select2({
        placeholder: "Saisissez quelques caractères pour des suggestions.",
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "auto",
    });
});
