/**
 * Define features for the bookmark modal.
 */
(function (exports, catalog) {

    exports.fillCurrentUrlField = function (event) {
        var window = exports;
        var currentUrl = window.document.location;
        var input = event.data.clipboardInput;

        input.attr('value', currentUrl);
    };

    exports.copyUrlToClipboard = function (event) {
        event.preventDefault();

        var window = exports;
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

})(this, catalog);

$(document).ready(function () {
    var clipboardBtn = $('button#clipboard-btn');
    var clipboardModal = $('div#bookmark-modal');
    var clipboardInput = clipboardModal.find('input[name=current-url]');

    clipboardModal.on('show.bs.modal', { clipboardInput: clipboardInput }, fillCurrentUrlField);
    clipboardBtn.on('click', { clipboardInput: clipboardInput }, copyUrlToClipboard);
});