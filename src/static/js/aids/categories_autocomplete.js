$(document).ready(function () {
    $("#id_categories").select2({
        placeholder: "Toutes les sous-thématiques",
        theme: "select2-dsfr select2-dsfr-checkboxes",
        dropdownAutoWidth: true,
        width: "auto",

        closeOnSelect: false,
        selectionAdapter: $.fn.select2.amd.require("NumberOfSelectedSelectionAdapter"),
        templateSelection: (data) => {
            return format_number_of_selected(data)
        },
        dropdownAdapter: $.fn.select2.amd.require("DropdownWithSearchAdapter")
    })
});
