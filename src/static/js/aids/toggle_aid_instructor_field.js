(function (exports, catalog) {

    /**
     * Add a button to toggle the "Instuctors" field.
     *
     * Note: we must not hide the field if there's a value in it.
     */
    exports.toggleInstructorField = function(form, div) {

        var hasErrors = div.find('p.error').length > 0;
        var hasValues = div.find('select').val().length > 0;

        if (!(hasValues || hasErrors)) {
            var revealBtn = $('<button class="btn btn-primary mb-3 fr-btn" />');
            revealBtn.html('<span class="fas fa-plus"></span> ' + catalog.add_instructor_label);
            revealBtn.insertBefore(div);

            div.addClass('collapse');

            revealBtn.click(function() {
                div.collapse('show');
                revealBtn.remove();
            });

            div.collapse('hide');
        }
    };

})(this, catalog);

$(document).ready(function () {

    var aidEditForm = $('form.main-form');
    var instructorDiv = $('#instructor-fields');
    toggleInstructorField(aidEditForm, instructorDiv);
});
