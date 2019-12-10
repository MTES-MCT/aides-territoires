/**
 * Handle the code related to the financer and instructor fields.
 *  - create the autocomplete fields using select2
 *  - handle the "suggestion" fields
 */

(function (exports) {
    'use strict';

    /**
     * Hide the backer suggestion field using bootstrap's collapse mechanism
     */
    exports.hideSuggestionField = function (field) {
        var field = $('#form-group-' + field);
        var input = field.find('input');

        // Note: don't hide the field if it actually holds a value
        if (input.val() === '') {
            field.addClass('collapse');
        }
    };

    /**
     * Prepares an event listener to show and set focus to the suggestion field
     */
    exports.showSuggestionField = function (backerFieldName, suggestionFieldName) {
        var select2Field = $('#id_' + backerFieldName);
        var suggestionFieldFormGroup = $('#form-group-' + suggestionFieldName);
        var suggestionField = $('#id_' + suggestionFieldName);

        // This function will be called when the suggestion button is clicked
        return function () {
            select2Field.select2('close');
            suggestionFieldFormGroup.collapse('show');
            suggestionField.focus();
        }
    }

}(this));

$(document).ready(function () {

    hideSuggestionField('financer_suggestion');
    hideSuggestionField('instructor_suggestion');

    $('select#id_financers').select2({
        placeholder: catalog.financers_placeholder,
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
        },
        theme: 'bootstrap4',
        width: '',
        language: {
            noResults: function (term) {
                var btn = $('<button />')
                    .addClass('btn')
                    .addClass('btn-link')
                    .on('click', showSuggestionField('financers', 'financer_suggestion'))
                    .html(catalog.suggest_backer_button);

                var text = $('<span />')
                    .html(catalog.no_backers_found);

                return text.append(btn);
            },
        },
    });
    $('select#id_instructors').select2({
        placeholder: catalog.instructors_placeholder,
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
        },
        theme: 'bootstrap4',
        width: '',
        language: {
            noResults: function (term) {
                var btn = $('<button />')
                    .addClass('btn')
                    .addClass('btn-link')
                    .on('click', showSuggestionField('instructors', 'instructor_suggestion'))
                    .html(catalog.suggest_backer_button);

                var text = $('<span />')
                    .html(catalog.no_backers_found);

                return text.append(btn);
            },
        },
    });
});
