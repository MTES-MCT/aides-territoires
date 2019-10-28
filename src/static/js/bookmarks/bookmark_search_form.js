/**
 * Handles the aid bookmark creation form.
 */
(function (exports, catalog) {
    'use strict';

    var searchForm = $('form#search-form');

    var queryField = $('form#search-form input#id_text');
    var perimeterField = $('form#search-form select#id_perimeter');
    var bookmarkNameField = $('form#bookmark-form input#id_title');

    /**
     * Prepend current search parameters to the form data.
     *
     * The "alert creation form" does not actually holds the fields
     * for the current search. Hence, we have to append the search fields
     * (that are held in a different form) to the currently posted data.
     */
    exports.onBookmarkFormSubmit = function (event) {
        var querystring = searchForm.serialize();
        var input = $('<input />');
        input.attr('type', 'hidden');
        input.attr('name', 'querystring');
        input.attr('value', querystring);
        input.appendTo(this);
        return true;
    };


    /**
     * Prefill the "alert title" field upon aid modal opening.
     */
    exports.onModalShow = function (event) {
        var nameSuggestion;

        var query = queryField.val();
        var perimeter = perimeterField.children('option:selected').text();
        var perimeterName = perimeter.split(' (')[0];


        if (query !== '' && perimeterName !== '') {
            nameSuggestion = perimeterName + ' — ' + query;
        } else {
            nameSuggestion = perimeterName + ' ' + query;
        }

        bookmarkNameField.val(nameSuggestion.trim());
    };

})(this, catalog);

$(document).ready(function () {
    $('form#bookmark-form').on('submit', onBookmarkFormSubmit);
    $('div#bookmark-search-modal').on('show.bs.modal', onModalShow);
});