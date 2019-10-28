/**
 * Handles the aid bookmark creation form.
 */
(function (exports, catalog) {
    'use strict';

    /**
     * See https://www.quirksmode.org/js/cookies.html
     */
    var readCookie = function (name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }

    /**
     * Prepend current search parameters to the form data.
     *
     * The "alert creation form" does not actually holds the fields
     * for the current search. Hence, we have to append the search fields
     * (that are held in a different form) to the currently posted data.
     *
     * The easiest way to get that data is to get it from the cookie that
     * is updated everytime a search is performed.
     */
    exports.onBookmarkFormSubmit = function (event) {
        var searchCookieName = catalog.SEARCH_COOKIE_NAME;
        var cookieValue = readCookie(searchCookieName);
        var input = $('<input />');
        input.attr('type', 'hidden');
        input.attr('name', 'querystring');
        input.attr('value', cookieValue);
        input.appendTo(this);
        return true;
    };

})(this, catalog);

$(document).ready(function () {
    $('form#bookmark-form').on('submit', onBookmarkFormSubmit);
});