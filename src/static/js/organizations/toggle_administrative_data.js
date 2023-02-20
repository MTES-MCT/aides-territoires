(function (exports) {

    /**
     * Enable the organization-administrative-data field group toggling.
     *
     * Note: if some related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleorganizationAdministrativeDataDiv = function (form, div) {
        let select = form.find('#id_organization_type option[value="private_person"]');
        let selected = select.prop('selected');
        let hasErrors = div.find('p.error').length > 0;

        if (selected || hasErrors) {
            div.addClass('fr-collapse');
        } else {
            div.removeClass('fr-collapse');
        }
    };

})(this);

$(document).ready(function () {

    // Hide administrative data fields group when the user is a 
    // private person

    let form = $('#update-organization-form');
    let organizationAdministrativeDataDiv = $('#organization-administrative-data');

    toggleorganizationAdministrativeDataDiv(form, organizationAdministrativeDataDiv);

    form.on('change', function () {
        toggleorganizationAdministrativeDataDiv(form, organizationAdministrativeDataDiv);
    });
});
