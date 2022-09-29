const fetchMayorData = function (perimeter_id) {
    // Retrieves the data about mayors and fills the proper fields
    $.ajax({
        type: 'GET',
        url: '/api/perimeters/data/?perimeter_id=' + perimeter_id,
        dataType: 'json',
        success: function (data) {
            $.each(data.results, function (i) {
                let entry = data.results[i];
                if (entry.prop === "mairie_email") {
                    $("#id_email").val(entry.value);
                }

                if ($("#id_beneficiary_function").val() == "mayor") {
                    $("#id_beneficiary_role").val("Maire");
                    if (entry.prop === "mayor_first_name") {
                        $("#id_first_name").val(entry.value);
                    }

                    if (entry.prop === "mayor_last_name") {
                        $("#id_last_name").val(entry.value);
                    }
                }
            });
        },
    })
}

$(document).ready(function () {

    /***
     * Listen to changes on the initial form.
     * Using a proxy because a event listener on select tags apparently ignores
     * the select2-powered ones.
     */

    let initialForm = new Proxy({
        beneficiary_function: null,
        perimeter: null,
    }, {
        set: function (target, property, value) {
            target[property] = value;

            if (target["beneficiary_function"] && target["perimeter"]) {
                fetchMayorData(target["perimeter"]);
                $("#registration-full").show('fast');
            }
        }
    });

    initialForm.beneficiary_function = $("#id_beneficiary_function").val();
    $("#id_beneficiary_function").change(function () {
        initialForm.beneficiary_function = $(this).val();
    });

    if ($("#id_perimeter").val()) {
        initialForm.perimeter = $("#id_perimeter").val().split('-')[0];
    }
    $("#id_perimeter").change(function () {
        let perimeter_slug = $(this).val();
        let perimeter_id = perimeter_slug.split('-')[0];

        initialForm.perimeter = perimeter_id;

        let perimeter_name = $(this).find('option:selected').text();
        $("#id_organization_name").val("Commune de " + perimeter_name.split(' (')[0]);
    });

    // Set the source from URL
    let searchParams = new URLSearchParams(window.location.search);
    if (searchParams.has('source')) {
        let source = searchParams.get('source');
        console.log("source: " + source);
        $("#id_acquisition_channel_comment").val(source);
    }

});