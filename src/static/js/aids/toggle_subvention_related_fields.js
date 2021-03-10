(function (exports) {

    /**
     * Enable the financial related fields toggling.
     *
     * Note: if some financial related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleFinancialFields = function(form, div, inputvalue) {

        div.addClass('collapse');

        var checkbox = form.find('input[value=' + inputvalue + ']');
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

    // Only display related fields when the main field (subvention, loan,
    // recoverable_advance or other) checkbox is checked.
    var aidEditForm = $('form.main-form');

    var subventionFieldsDiv = $('div#subvention-fields');
    var loanFieldsDiv = $('div#loan-field');
    var recoverableAdvanceFieldDiv = $('div#recoverable-advance-field');
    var otherFinancialAidFieldDiv = $('div#other-financial-aid-field');

    toggleFinancialFields(aidEditForm, subventionFieldsDiv, 'grant');
    aidEditForm.on('change', function() {
        toggleFinancialFields(aidEditForm, subventionFieldsDiv, 'grant');
    });

    toggleFinancialFields(aidEditForm, loanFieldsDiv, 'loan');
    aidEditForm.on('change', function() {
        toggleFinancialFields(aidEditForm, loanFieldsDiv, 'loan');
    });

    toggleFinancialFields(aidEditForm, recoverableAdvanceFieldDiv, 'recoverable_advance');
    aidEditForm.on('change', function() {
        toggleFinancialFields(aidEditForm, recoverableAdvanceFieldDiv, 'recoverable_advance');
    });

    toggleFinancialFields(aidEditForm, otherFinancialAidFieldDiv, 'other');
    aidEditForm.on('change', function() {
        toggleFinancialFields(aidEditForm, otherFinancialAidFieldDiv, 'other');
    });
});
