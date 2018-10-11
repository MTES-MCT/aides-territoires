/**
 * Define features for the bookmark modal.
 */
(function (exports) {

    exports.copyUrlToClipboard = function (event) {
        event.preventDefault();

        var window = exports;
        var url = window.document.location;

    };

})(this);

$(document).ready(function () {
    var clipboardBtn = $('button#clipboard-btn');
    clipboardBtn.click(copyUrlToClipboard);
});