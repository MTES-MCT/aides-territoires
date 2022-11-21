$(document).ready(function () {
    $('select#id_destinations').select2({
        placeholder: "Tous les types de dépense",
        language: "fr",
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "100%",
    })
        .on('select2:close', show_number_of_selected)
        .each(show_number_of_selected);
});
