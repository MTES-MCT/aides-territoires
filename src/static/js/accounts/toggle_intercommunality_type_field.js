(function (exports) {

    /**
     * Enable the intercommunality_type field toggling.
     *
     * Note: if some related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleIntercommunalityTypeField = function (form, div) {
        let select = form.find('#id_organization_type option[value="epci"]');
        let selected = select.prop('selected');
        let hasErrors = div.find('p.error').length > 0;

        if (selected || hasErrors) {
            div.addClass('fr-collapse--expanded fr-mb-3w at-required--label');
        } else {
            div.removeClass('fr-collapse--expanded fr-mb-3w at-required--label');
        }
    };

})(this);

$(document).ready(function () {

    // Only display subvention related fields when the `subvention`
    // checkbox is checked.
    let form = $('#register-form, #create-organization-form, #update-organization-form');
    let intercommunalityTypeFieldDiv = $('#intercommunality-type-field-collapse');

    toggleIntercommunalityTypeField(form, intercommunalityTypeFieldDiv);

    form.on('change', function () {
        toggleIntercommunalityTypeField(form, intercommunalityTypeFieldDiv);
    });
});
