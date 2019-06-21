/**
 * Dynamic features for bookmarks.
 */
(function (exports, catalog) {
    'use strict';

    var updateBookmark = function(form) {
        var action = form.attr('action');
        var data = form.serialize();
        $.ajax({
            url: action,
            data: data,
            method: 'POST',
            success: function(response) {
                // Let's just do nothing here.
            },
            error: function(response) {
            },
        });
    };

    /**
     * Intercept the form POST action and converts the request into ajax
     */
    exports.onCheckboxChange = function (event) {

        event.preventDefault();
        var checkbox = $(event.target);
        var form = checkbox.parents('form');
        updateBookmark(form);
    };

})(this, catalog);

$(document).ready(function () {
    $('form.update-form input[type=checkbox]').on('change', onCheckboxChange);
});