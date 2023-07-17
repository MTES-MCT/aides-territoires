(function (exports) {

    /**
     * Enable the engineering related fields toggling.
     *
     * Note: if some engineering related fields have errors (because the form
     * was submitted before), we always display them so the error message
     * will never be hidden.
     */
    exports.toggleSupportTypeFields = function(form, div) {

        var engineeringInputs = [
            "strategic_engineering",
            "diagnostic_engineering",
            "AMOA_engineering",
            "MOE_engineering",
            "financial_engineering",
            "administrative_engineering",
            "legal_and_regulatory_engineering",
            "formation_engineering",
        ]
        
        engineeringInputs.forEach(element => {
            var checkbox = form.find(`input[value=${element}]`);
            var checked = checkbox.prop('checked');
            var hasErrors = div.find('p.error').length > 0;
            
            if (checked || hasErrors) {
                div.addClass('fr-collapse--expanded');
            }

        });

        var engineeringchecked = $('#id_aid_types_1 > .fr-checkbox-group > input:checked').length;
        if (engineeringchecked < 1){
            div.removeClass('fr-collapse--expanded');
        };
    };
})(this);

$(document).ready(function () {

    // Only display engineering aid_type related fields when at least one `engineering`
    // checkbox is checked.
    var aidEditForm = $('form.main-form');
    var supportTypeFieldsDiv = $('div#support-type-fields-collapse');

    toggleSupportTypeFields(aidEditForm, supportTypeFieldsDiv);

    aidEditForm.on('change', function() {
        toggleSupportTypeFields(aidEditForm, supportTypeFieldsDiv);
    });
});
