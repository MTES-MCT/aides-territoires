/**
 * Define features for the bookmark modal.
 */
(function (exports, catalog) {

    var window = exports;

    exports.bookmarkAid = function (event) {
        event.preventDefault();

        var $bookmarkForm = $(this);
        var $submitButton = $bookmarkForm.find('button[type=submit]');
        var formAction = $bookmarkForm.attr('action');
        var data = $bookmarkForm.serialize();

        var onSendSuccess = function () {
            $submitButton.html(catalog.bookmark_success);
        };

        var onSendError = function () {
            $submitButton.html(catalog.bookmark_error);
        };

        bookmarkXHR = $.ajax({
            method: 'post',
            url: formAction,
            data: data,
            beforeSend: function () {
                $submitButton.attr('disabled', 'disabled');
                $submitButton.html(catalog.bookmark_waiting);
            },
            success: onSendSuccess,
            error: onSendError,
            complete: function() {
            }
        });
    };

})(this, catalog);

$(document).ready(function () {
    var bookmarkForm = $('#bookmark-form');
    bookmarkForm.on('submit', bookmarkAid);
});