$(document).ready(function () {
    $('select#id_targeted_audiences').select2({
        placeholder: "Toutes les structures",
        theme: "select2-dsfr select2-dsfr-checkboxes",
        dropdownAutoWidth: true,
        width: "100%",
        closeOnSelect: false,
        selectionAdapter: $.fn.select2.amd.require("NumberOfSelectedSelectionAdapter"),
        templateSelection: (data) => {
            return format_number_of_selected(data)
        },
        dropdownAdapter: $.fn.select2.amd.require("DropdownWithSearchAdapter")
    })
});
