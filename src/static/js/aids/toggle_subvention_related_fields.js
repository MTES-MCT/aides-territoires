(function (exports) {

    /**
     * Enable the subvention related fields toggling.
     *
     * Note: if some subvention related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleSubventionFields = function(form, div) {

        div.addClass('collapse');

        var checkbox = form.find('input[value=grant]');
        var checked = checkbox.prop('checked');
        var hasErrors = div.find('p.error').length > 0;

        if (checked || hasErrors) {
            div.collapse('show');
        } else {
            div.collapse('hide');
        }
    };

})(this);

$(document).ready(function () {

    // Only display subvention related fields when the `subvention`
    // checkbox is checked.
    var aidEditForm = $('form.main-form');
    var subventionFieldsDiv = $('div#subvention-fields');
    toggleSubventionFields(aidEditForm, subventionFieldsDiv);
    aidEditForm.on('change', function() {
        toggleSubventionFields(aidEditForm, subventionFieldsDiv);
    });
});
