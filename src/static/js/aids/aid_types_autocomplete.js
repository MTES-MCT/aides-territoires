$(document).ready(function () {
    $('select#id_aid_type').select2({
        placeholder: "Toutes les natures d’aide",
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "100%",
    })
        .on('select2:close', show_number_of_selected)
        .each(show_number_of_selected);
});
