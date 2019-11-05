(function (exports) {

    /**
     * Enable the subvention related fields toggling.
     *
     * Note: if some subvention related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleSubventionFields = function(form, div) {

        var checkbox = form.find('input[value=grant]');
        var checked = checkbox.prop('checked');
        var hasErrors = div.find('p.error').length > 0;

        if (checked || hasErrors) {
            div.addClass('collapse show');
        } else {
            div.addClass('collapse');
        }

        if (!hasErrors) {
            form.on('change', function() {
                var collapse = checkbox.prop('checked') ? 'show' : 'hide';
                div.collapse(collapse);
            });
        }
    };

})(this);

$(document).ready(function () {

    // Only display subvention related fields when the `subvention`
    // checkbox is checked.
    var aidEditForm = $('form.main-form');
    var subventionFieldsDiv = $('div#subvention-fields');
    toggleSubventionFields(aidEditForm, subventionFieldsDiv);
});