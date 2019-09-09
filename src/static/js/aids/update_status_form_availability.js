(function (exports) {

    // block the status edition button if some data was modified
    exports.checkStatusUpdateAvailability = function(aidEditForm, aidStatusBtn) {

        var initialData = aidEditForm.serialize();

        aidEditForm.on('change', function() {
            var newData = aidEditForm.serialize();
            aidStatusBtn.prop('disabled', initialData != newData);
        });
    };

})(this);

$(document).ready(function () {
    // Prevent status update when edit form was modified
    // to prevent data loss.
    var aidEditForm = $('form.main-form');
    var aidStatusBtn = $('form#unpublish-form button[type=submit]');

    checkStatusUpdateAvailability(aidEditForm, aidStatusBtn);
});