/**
 * Handles the aid bookmark creation form.
 */
(function (exports, catalog) {
    'use strict';

    var searchForm = $('form#search-form');

    var queryField = $('form#search-form input#id_text');
    var perimeterField = $('form#search-form select#id_perimeter');
    var bookmarkNameField = $('form#bookmark-form input#id_title');
    var sendAlertField = $('form#bookmark-form input#id_send_email_alert');
    var frequencyField = $('form#bookmark-form select#id_alert_frequency');


    /**
     * Prepend current search parameters to the form data.
     *
     * The "alert creation form" does not actually holds the fields
     * for the current search. Hence, we have to append the search fields
     * (that are held in a different form) to the currently posted data.
     */
    exports.appendQuerystringToForm = function (event) {
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
    exports.prefillAlertNameField = function (event) {
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

    exports.focusTitleField = function (event) {
        bookmarkNameField.focus();
    };

    /**
     * Hide the "alert frequency" field.
     *
     * It will only get displayed when the "send alert" checkbox is checked.
     */
    exports.hideFrequencyField = function (event) {
        if (sendAlertField.length > 0) {
            var formGroup = frequencyField.parent('div.form-group');
            formGroup.addClass('collapse');
        }
    };

    /**
     * Toggles the "alert frequency" field depending on the "send alert"
     * field current value.
     */
    exports.updateAlertFrequencyVisibility = function (event) {
        if (sendAlertField.length > 0) {
            var collapse = sendAlertField.prop('checked') ? 'show' : 'hide';
            var formGroup = frequencyField.parent('div.form-group');
            formGroup.collapse(collapse);
        }
    };

})(this, catalog);

$(document).ready(function () {
    $('div#bookmark-search-modal').on('show.bs.modal', prefillAlertNameField);
    $('div#bookmark-search-modal').on('show.bs.modal', hideFrequencyField);
    $('div#bookmark-search-modal').on('shown.bs.modal', focusTitleField);
    $('form#bookmark-form').on('change', updateAlertFrequencyVisibility);
    $('form#bookmark-form').on('submit', appendQuerystringToForm);
});