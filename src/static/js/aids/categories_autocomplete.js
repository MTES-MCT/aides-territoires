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

    let BACKERS_MAP = $('#department-search-form').length
    let searchParams = new URLSearchParams(window.location.search)

    if (BACKERS_MAP && searchParams.has('aid_category')) {
        let categories = searchParams.get('aid_category').split(',')
        $('#id_categories').val(categories)
        $('#id_categories').trigger('change')
    }

});
