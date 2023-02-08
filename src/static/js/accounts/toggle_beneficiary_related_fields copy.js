(function (exports) {

    /**
     * Enable the beneficiary_role & benficiary_function fields toggling.
     *
     * Note: if some related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleBeneficiaryFields = function(form, div) {

        var select = form.find('select#id_organization_type option[value="commune"]');
        var selected = select.prop('selected');
        var hasErrors = div.find('p.error').length > 0;

        if (selected || hasErrors) {
            div.addClass('fr-collapse--expanded');
        } else {
            div.removeClass('fr-collapse--expanded');
        }
    };

})(this);

$(document).ready(function () {

    // Only display subvention related fields when the `subvention`
    // checkbox is checked.
    var registerForm = $('form#register-form');
    var beneficiaryFieldsDiv = $('div#beneficiary-fields-collapse');

    toggleBeneficiaryFields(registerForm, beneficiaryFieldsDiv);

    registerForm.on('change', function() {
        toggleBeneficiaryFields(registerForm, beneficiaryFieldsDiv);
    });
});
