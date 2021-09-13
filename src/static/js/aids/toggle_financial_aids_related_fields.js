(function (exports) {

    /**
     * Enable the subvention related fields toggling.
     *
     * Note: if some subvention related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleLoanFields = function(form, div) {

        var checkbox = form.find('input[value=loan]');
        var checked = checkbox.prop('checked');
        var hasErrors = div.find('p.error').length > 0;

        if (checked || hasErrors) {
            div.addClass('fr-collapse--expanded');
        } else {
            div.removeClass('fr-collapse--expanded');
        }
    };

        /**
     * Enable the subvention related fields toggling.
     *
     * Note: if some subvention related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
         exports.toggleAdvanceFields = function(form, div) {
    
            var checkbox = form.find('input[value=recoverable_advance]');
            var checked = checkbox.prop('checked');
            var hasErrors = div.find('p.error').length > 0;
    
            if (checked || hasErrors) {
                div.addClass('fr-collapse--expanded');
            } else {
                div.removeClass('fr-collapse--expanded');
            }
        };

        
        /**
     * Enable the subvention related fields toggling.
     *
     * Note: if some subvention related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
         exports.toggleOtherFinancialAidFields = function(form, div) {
    
            var checkbox = form.find('input[value=other]');
            var checked = checkbox.prop('checked');
            var hasErrors = div.find('p.error').length > 0;
    
            if (checked || hasErrors) {
                div.addClass('fr-collapse--expanded');
            } else {
                div.removeClass('fr-collapse--expanded');
            }
        };

        
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
                div.addClass('fr-collapse--expanded');
            } else {
                div.removeClass('fr-collapse--expanded');
            }
        };    

})(this);

$(document).ready(function () {

    // Only display subvention related fields when the `subvention`
    // checkbox is checked.
    var aidEditForm = $('form.main-form');
    var loanFieldsDiv = $('div#loan-fields-collapse');
    var advanceFieldsDiv = $('div#recoverable-advance-fields-collapse');
    var otherFinancialAidFieldsDiv = $('div#other-financial-aid-fields-collapse');
    var subventionFieldsDiv = $('div#subvention-fields-collapse');

    toggleLoanFields(aidEditForm, loanFieldsDiv);
    toggleAdvanceFields(aidEditForm, advanceFieldsDiv);
    toggleOtherFinancialAidFields(aidEditForm, otherFinancialAidFieldsDiv);
    toggleSubventionFields(aidEditForm, subventionFieldsDiv);

    aidEditForm.on('change', function() {
        toggleLoanFields(aidEditForm, loanFieldsDiv);
        toggleAdvanceFields(aidEditForm, advanceFieldsDiv);
        toggleOtherFinancialAidFields(aidEditForm, otherFinancialAidFieldsDiv);
        toggleSubventionFields(aidEditForm, subventionFieldsDiv);
    });
});
