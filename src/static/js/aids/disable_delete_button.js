$(document).ready(function () {
    // Disable deletion button until confirmation checkbox was checked
    var deleteBtn = $('form#delete-form button[type=submit]');
    var confirmCb = $('form#delete-form input[type=checkbox]');

    deleteBtn.prop('disabled', true);
    confirmCb.on('click', function() {
        deleteBtn.prop('disabled', !confirmCb.prop('checked'));
    });
});
