/**
 * Define features for the bookmark modal.
 */
(function (exports, catalog) {

    var window = exports;

    exports.fillCurrentUrlField = function (event) {
        var currentUrl = window.document.location;
        var input = event.data.clipboardInput;

        input.attr('value', currentUrl);
    };

    exports.copyUrlToClipboard = function (event) {
        event.preventDefault();

        var navigator = window.navigator;
        var document = window.document;
        var $input = event.data.clipboardInput;
        var $copyBtn = $(event.currentTarget);
        var currentUrl = $input.attr('value');

        $input.focus();
        $input.select();

        var onCopyToClipboardSuccess = function () {
            $copyBtn.tooltip({
                placement: 'bottom',
                title: catalog.copy_to_clipboard_success,
            }).tooltip('show');
        };

        var onCopyToClipboardError = function () {
            $copyBtn.tooltip({
                placement: 'bottom',
                title: catalog.copy_to_clipboard_error,
            }).tooltip('show');
        };

        if (navigator.clipboard) {
            navigator.clipboard.writeText(currentUrl).then(onCopyToClipboardSuccess, onCopyToClipboardError);
        } else {
            if (document.execCommand('copy')) {
                onCopyToClipboardSuccess();
            } else {
                onCopyToClipboardError();
            }
        }
    };

    exports.receiveResults = function (event) {
        event.preventDefault();

        var $receiveForm = $(this);
        var $submitButton = $receiveForm.find('button[type=submit]');
        var formAction = $receiveForm.attr('action');
        var queryString = window.location.search.substring(1);
        var $csrfTokenField = $receiveForm.find('input[name=csrfmiddlewaretoken]');
        var token = $csrfTokenField.attr('value');
        var fullQueryString = queryString + '&csrfmiddlewaretoken=' + token;

        var onSendSuccess = function () {
            $submitButton.tooltip({
                placement: 'bottom',
                title: catalog.send_by_email_success
            }).tooltip('show');
        };

        var onSendError = function () {
            $submitButton.tooltip({
                placement: 'bottom',
                title: catalog.send_by_email_error
            }).tooltip('show');
        };

        searchXHR = $.ajax({
            method: 'post',
            url: formAction,
            data: fullQueryString,
            beforeSend: function () {
                $submitButton.attr('disabled', 'disabled');
                $submitButton.html(catalog.send_by_email_message);
            },
            success: onSendSuccess,
            error: onSendError,
            complete: function() {
                $submitButton.html(catalog.send_by_email_done);
            }
        });
    };

})(this, catalog);

$(document).ready(function () {
    // Setup the "copy to clipboard feature"
    var clipboardBtn = $('button#clipboard-btn');
    var clipboardModal = $('div#bookmark-modal');
    var clipboardInput = clipboardModal.find('input[name=current-url]');
    clipboardModal.on('show.bs.modal', { clipboardInput: clipboardInput }, fillCurrentUrlField);
    clipboardBtn.on('click', { clipboardInput: clipboardInput }, copyUrlToClipboard);

    // Setup the "receive by email" feature
    var receiveForm = $('form#send-results-by-email-form');
    receiveForm.on('submit', receiveResults);
});