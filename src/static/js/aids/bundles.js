/**
 * Define features for the bundle modal.
 */
(function (exports, catalog) {

    var window = exports;

    exports.bundleAid = function (event) {
        event.preventDefault();

        var $bundleForm = $(this);
        var $submitButton = $bundleForm.find('button[type=submit]');
        var formAction = $bundleForm.attr('action');
        var data = $bundleForm.serialize();

        var onSendSuccess = function () {
            $submitButton.html(catalog.bundle_success);
            $bundleForm.slideUp('fast', function() {
                $('<div class="success"></div>')
                .html(catalog.bundle_success)
                .insertAfter($bundleForm)
                .hide()
                .slideDown('fast');
            });
        };

        var onSendError = function () {
            $submitButton.html(catalog.bundle_error);
        };

        bundleXHR = $.ajax({
            method: 'post',
            url: formAction,
            data: data,
            beforeSend: function () {
                $submitButton.attr('disabled', 'disabled');
                $submitButton.html(catalog.bundle_waiting);
            },
            success: onSendSuccess,
            error: onSendError,
            complete: function() {
            }
        });
    };

})(this, catalog);

$(document).ready(function () {
    var bundleForm = $('#bundle-form');
    bundleForm.on('submit', bundleAid);
});