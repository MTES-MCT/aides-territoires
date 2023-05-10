(function (exports) {

    /**
     * Enable the short title field toggling.
     *
     * For now, the short title field is only ever used for France Relance
     * related aids.
     *
     */
    exports.toggleShortTitleField = function (form, div) {

        div.addClass('at-display__none');

        let checkbox = $("#id_in_france_relance");
        let checked = checkbox.prop("value") === "True";
        let hasErrors = div.find('p.error').length > 0;

        console.log(checkbox, checked)

        if (checked || hasErrors) {
            div.removeClass('at-display__none');
            console.log("here")
        } else {
            div.addClass('at-display__none');
            console.log("there")
        }
    };

})(this);

$(document).ready(function () {

    // Only display the short title field when "France Relance" is
    // selected.
    let aidEditForm = $('form.main-form');
    let shortTitleDiv = $('div#form-group-short_title');

    toggleShortTitleField(aidEditForm, shortTitleDiv);
    aidEditForm.on('change', function () {
        toggleShortTitleField(aidEditForm, shortTitleDiv);
    });
});
