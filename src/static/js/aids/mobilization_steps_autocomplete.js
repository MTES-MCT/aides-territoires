$(document).ready(function () {
    $('select#id_mobilization_step').select2({
        placeholder: "Toutes les étapes",
        theme: "select2-dsfr select2-dsfr-checkboxes",
        dropdownAutoWidth: true,
        width: "auto",
        closeOnSelect: false,
        selectionAdapter: $.fn.select2.amd.require("NumberOfSelectedSelectionAdapter"),
        templateSelection: (data) => {
            return format_number_of_selected(data)
        },
    })
});
