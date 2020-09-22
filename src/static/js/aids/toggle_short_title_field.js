(function (exports) {

    /**
     * Enable the short title field toggling.
     *
     * For now, the short title field is only ever used for France Relance
     * related aids.
     *
     */
    exports.toggleShortTitleField = function(form, div) {

        div.addClass('collapse');

        var checkbox = form.find('input[name=in_france_relance]');
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

    // Only display the short title field whan "France Relance" is
    // selected.
    var aidEditForm = $('form.main-form');
    var shortTitleDiv = $('div#form-group-short_title');

    toggleShortTitleField(aidEditForm, shortTitleDiv);
    aidEditForm.on('change', function() {
        toggleShortTitleField(aidEditForm, shortTitleDiv);
    });
});
