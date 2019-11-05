(function (exports) {

    exports.toggleSubventionFields = function(form, div) {

        var checkbox = form.find('input[value=grant]');
        var checked = checkbox.prop('checked');

        if (checked) {
            div.addClass('collapse show');
        } else {
            div.addClass('collapse');
        }

        form.on('change', function() {
            var collapse = checkbox.prop('checked') ? 'show' : 'hide';
            div.collapse(collapse);
        });
    };

})(this);

$(document).ready(function () {
    // Prevent status update when edit form was modified
    // to prevent data loss.
    var aidEditForm = $('form.main-form');
    var subventionFieldsDiv = $('div#subvention-fields');

    toggleSubventionFields(aidEditForm, subventionFieldsDiv);
});