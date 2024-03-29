(function (exports) {
    /**
     * Pre-fill the organization_name value depending on certain variables
     * and hide it in some case
     */
    exports.preFillOrganizationName = function (form) {

        let organizationType = form.find("#id_organization_type option:selected").val();

        let organizationNameField = $("#id_name");
        let organizationNameDiv = form.find("#form-group-name");

        if (form.attr('id') == "register-form") {
            organizationNameField = $("#id_organization_name")
            organizationNameDiv = form.find("#form-group-organization_name");
        }


        let perimeterNameValue = $("#id_perimeter").find('option:selected').text().split(' (')[0];

        // Check if the field has errors. Do not hide it if is the case
        let hasErrors = organizationNameDiv.find('p.error').length > 0;

        if (organizationType == "private_person") {
            let full_name = "";
            // Set organization name to user name for private persons
            if (form.attr('id') == "register-form") {
                let first_name = form.find("#id_first_name").val();
                let last_name = form.find("#id_last_name").val();
                full_name = first_name + " " + last_name;
            } else {
                full_name = $('.at-username').first().text()
            }

            organizationNameField.val(full_name);

            if (!hasErrors) {
                organizationNameDiv.addClass('fr-collapse');
            }
        } else if (["commune", "department", "region", "epci"].includes(organizationType)) {
            // Set organization name relative to perimeter name for collectivities
            let organizationName = perimeterNameValue;

            if (organizationType == "commune") {
                organizationName = "Mairie de " + perimeterNameValue
            } else if (organizationType == "region") {
                organizationName = "Région " + perimeterNameValue
            }

            if (perimeterNameValue) {
                organizationNameField.val(organizationName);
            } else {
                organizationNameField.val("");
            }
            organizationNameDiv.removeClass('fr-collapse');
        } else {
            organizationNameDiv.removeClass('fr-collapse');
        }
    }
})(this);

$(document).ready(function () {
    /* Only call the preFillOrganizationName() function if
     - the name field is empty
     - one of the fields used to determine it is changed
    */
    let organizationForm = $('#register-form, #create-organization-form, #update-organization-form');
    let organizationNameField = $("#id_name");

    if (organizationNameField == "") {
        preFillOrganizationName(organizationForm);
    }

    organizationForm.find(":input").on('change', function () {
        let fieldID = $(this).attr('id');

        if (["id_organization_type", "id_perimeter", "id_intercommunality_type"].includes(fieldID)) {
            preFillOrganizationName(organizationForm);
        }

    });
});
