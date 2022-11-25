$(document).ready(function () {
    $("select#id_categories").select2({
        placeholder: "Toutes les thématiques",
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "auto",
    })
        .on('select2:close', show_number_of_selected)
        .each(show_number_of_selected);
});
