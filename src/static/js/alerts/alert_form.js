/**
 * Handles the aid alert creation form.
 */
(function (exports, catalog) {
    'use strict';

    var searchForm = $('form#search-form');

    var queryField = $('form#search-form input#id_text');
    var perimeterField = $('form#search-form select#id_perimeter');
    var alertNameField = $('form#alert-form input#id_title');
    var emailField = $('form#alert-form input#id_email');

    var EMPTY_SEARCH = "integration=&text=&apply_before=&&order_by=";


    /**
     * Prepend current search parameters to the form data.
     *
     * The "alert creation form" does not actually holds the fields
     * for the current search. Hence, we have to append the search fields
     * (that are held in a different form) to the currently posted data.
     */
    exports.appendQuerystringToForm = function (event) {
        var querystring = searchForm.serialize();
        // if in aid detail, searchForm is empty. Use CURRENT_SEARCH instead
        if (!querystring && (typeof CURRENT_SEARCH !== "undefined")) {
            // var querystring = CURRENT_SEARCH.split("&")
            //                                 .filter(e => /^(?!.*(order_by|action)).*$/i.test(e))
            //                                 .join("&");
            querystring = CURRENT_SEARCH || EMPTY_SEARCH;
        }
        var input = $('<input />');
        input.attr('type', 'hidden');
        input.attr('name', 'querystring');
        input.attr('value', querystring);
        input.appendTo(this);
        return true;
    };

    exports.appendSourceToForm = function (event) {
        var source = 'aides-territoires';
        var pathname = window.location.pathname;

        // if in search page, use SEARCH_PAGE_SLUG instead
        if (typeof SEARCH_PAGE_SLUG !== "undefined") {
            source = SEARCH_PAGE_SLUG;
        }
        // if in search page without subdomain enabled,
        // use the search_page slug in the path instead
        else if (pathname.includes('/portails/')) {
            source = pathname.split("/");
            source = source[2]
        }

        var input = $('<input />');
        input.attr('type', 'hidden');
        input.attr('name', 'source');
        input.attr('value', source);
        input.appendTo(this);
        return true;
    };

    /**
     * Prefill the "alert title" field upon aid modal opening.
     */
    exports.prefillAlertNameField = function (event) {
        var nameSuggestion;

        var query = queryField.val() || '';
        var perimeter = perimeterField.children('option:selected').text();
        var perimeterName = perimeter.split(' (')[0];

        if (query !== '' && perimeterName !== '') {
            nameSuggestion = perimeterName + ' — ' + query;
        } else {
            nameSuggestion = perimeterName + ' ' + query;
        }

        alertNameField.val(nameSuggestion.trim());
    };

    exports.focusForm = function (event) {
        emailField.focus();
    };

})(this, catalog);

$(document).ready(function () {
    $('div#alert-search-modal').on('show.bs.modal', prefillAlertNameField);
    $('div#alert-search-modal').on('shown.bs.modal', focusForm);
    $('form#alert-form').on('submit', appendQuerystringToForm);
    $('form#alert-form').on('submit', appendSourceToForm);
});
