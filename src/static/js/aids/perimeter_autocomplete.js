$(document).ready(function () {
    // hide "custom" perimeters in the user part of the website
    let RESTRICT_TO_VISIBLE_PERIMETERS = $('#perimeter').length || $('#project_perimeter').length || $('#search-form').length || $('#advanced-search-form').length || $('#register-page').length || $('#register-commune-page').length;
    let RESTRICT_TO_NON_OBSOLETE_PERIMETERS = $('#perimeter').length || $('#search-form').length || $('#advanced-search-form').length || $('#register-page').length || $('#register-commune-page').length;

    // Filter on scale on certain forms
    let scale = null;
    let RESTRICT_TO_COMMUNES = $('#register-commune-page').length;
    let RESTRICT_DYNAMICALLY = $('#register-page').length;

    if (RESTRICT_TO_COMMUNES) {
        scale = 'commune';
    } else if (RESTRICT_DYNAMICALLY) {
        $("#id_organization_type").on("change", function () {
            let organizationType = $("#id_organization_type option:selected").val();
            let perimeterField = $("#id_perimeter")

            switch (organizationType) {
                case "commune": {
                    scale = 'commune';
                    perimeterField.val(null).trigger('change'); // unselect current value
                    break;
                }
                case "epci": {
                    scale = 'epci,adhoc';
                    perimeterField.val(null).trigger('change');
                    break;
                }
                case "department": {
                    scale = 'department';
                    perimeterField.val(null).trigger('change');
                    break;
                }
                case "region": {
                    scale = 'region';
                    perimeterField.val(null).trigger('change');
                    break;
                }
                default:
                    scale = null;
            };
        });
    }

    // Set the placeholder message
    let placeholder_message = "Tapez les premiers caractères"

    if ($('#search-form').length || $('#advanced-search-form').length) {
        placeholder_message = "Tous les territoires"
    }

    $('#id_perimeter').select2({
        placeholder: placeholder_message,
        allowClear: true,
        minimumInputLength: 1,
        language: {
            inputTooShort: function () { return ''; },
        },
        ajax: {
            url: catalog.perimeter_url,
            dataType: 'json',
            delay: 100,
            data: function (params) {
                let query = {
                    q: params.term,
                    is_visible_to_users: RESTRICT_TO_VISIBLE_PERIMETERS ? true : false,
                    is_non_obsolete: RESTRICT_TO_NON_OBSOLETE_PERIMETERS ? true : false,
                }
                if (scale) {
                    query.scale = scale;
                }
                return query;
            },
            processResults: function (data, params) {
                params.page = params.page || 1;

                return {
                    results: data.results,
                    pagination: {
                        more: data.next != null
                    }
                };
            },
        },
        theme: "select2-dsfr",
        dropdownAutoWidth: true,
        width: "auto",
    });
});
