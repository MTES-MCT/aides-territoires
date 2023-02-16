(function (exports) {
    /**
     * Pre-fill the organization_name value depending on certain variables
     * and hide it in some case
     */
    exports.preFillOrganizationName = function (form) {
        let organizationType = form.find("#id_organization_type option:selected").val();
        let organizationNameField = $("#id_organization_name")
        let organizationNameDiv = form.find("#form-group-organization_name");
        let perimeterNameValue = $("#id_perimeter").find('option:selected').text().split(' (')[0];

        // Check if the field has errors. Do not hide it if is the case
        let hasErrors = organizationNameDiv.find('p.error').length > 0;

        if (organizationType == "private_person") {
            // Set organization name to user name for private persons
            let first_name = form.find("#id_first_name").val();
            let last_name = form.find("#id_last_name").val();
            let full_name = first_name + " " + last_name;
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
        } else {
            organizationNameDiv.removeClass('fr-collapse');
        }
    }
})(this);

$(document).ready(function () {
    let registerForm = $('#register-form');

    registerForm.on('change', function () {
        preFillOrganizationName(registerForm);
    });
});
