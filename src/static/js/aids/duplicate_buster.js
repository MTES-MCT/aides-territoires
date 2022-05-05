/**
 * Script to detect duplicate aids.
 * Where? Admin aid detail form & App aid create/edit form
 * How? On the 'origin_url' field
 * When? once the form is initialized, and everytime the form is changed
 */
(function (exports, $) {
    'use strict';

    const MAX_RESULTS = 5;  // Don't display more duplicate
    const API_ENDPOINT = '/api/aids/?version=1.1&drafts=True&internal=True';

    // Create divs to hold the error message
    const topErrorDiv = $('<div class="inline-error"></div>');
    const inlineErrorDiv = $('<div class="inline-error"></div>');

    var aidForm, nameField, slugField, originUrlField;

    var DuplicateBuster = function (form) {
        aidForm = form;
        nameField = $('#id_name');
        slugField = $('#id_slug');
        originUrlField = $('#id_origin_url');
    };
    exports.DuplicateBuster = DuplicateBuster;

    DuplicateBuster.prototype.init = function () {
        initializeErrorDom();
        aidForm.on('change', warnForDuplicates);

        // Check duplicate when the form is first displayed
        warnForDuplicates();
    };

    // Insert the message holding div into the dom
    var initializeErrorDom = function () {
        topErrorDiv.insertAfter(nameField);
        inlineErrorDiv.insertAfter(originUrlField);
    };

    // Generate a link to a single duplicate aid
    var formatSingleDuplicate = function (data) {
        var url;
        var currentPath = $(location).attr('pathname');

        if (currentPath.startsWith('/admin/')) {
            url = '/admin/aids/aid/' + data['id'] + '/change/';
        } else {
            url = '/aides/' + data['slug'] + '/';
        }

        var a = $('<a/>');
        a.attr('href', url);
        a.html(data['name']);

        var li = $('<li/>');
        li.append(a);
        return li;
    };

    /**
     * Create a warning message with links to the related aids.
     */
    var displayWarningMessage = function (apiData) {
        var messageDiv = $('<div class="fr-alert fr-alert--error fr-mt-2w" />');
        var messageP = $('<p class="fr-alert__title">Attention ! Nous avons trouvé des aides qui ressemblent à des doublons.</p>');

        var currentSlug = slugField.val();
        var count = apiData['count'];
        var maxResults = Math.min(count, MAX_RESULTS);
        var duplicates = apiData['results']
            .filter(function (result) {
                return result['slug'] != currentSlug;
            })
            .slice(0, maxResults)
            .map(formatSingleDuplicate);

        var messageUl = $('<ul/>');
        messageUl.append(duplicates);

        messageDiv.append(messageP);
        messageDiv.append(messageUl);

        return messageDiv;
    };

    /**
     * Create a query to fetch for duplicates.
     * Note : if we don't have enough data, just return null.
     */
    var buildSearchForDuplicateQuery = function () {
        var origin_url = originUrlField.val();

        var query;
        if (origin_url) {
            query = API_ENDPOINT + '&origin_url=' + encodeURIComponent(origin_url);
        } else {
            query = null;
        }

        return query;
    };

    /**
     * Call the API to find aid that might be duplicates from the current one.
     */
    var fetchDuplicates = function () {
        var query = buildSearchForDuplicateQuery();
        if (query === null) {
            // If we can't call the api, just return an empty result set
            return new Promise(function () { return { count: 0, results: [] }; });
        }

        return $.getJSON(query);
    };

    /**
     * Hide or display a warning message depending on the duplicates found
     */
    var hideOrShowMessage = function (duplicates) {
        var count = duplicates['count'];
        var results = duplicates['results'];
        var currentSlug = slugField.val();

        // Be careful as to not count the current aid as a duplicate of itself
        if (count == 0 || count == 1 && results[0]['slug'] == currentSlug) {
            topErrorDiv.html('');
            inlineErrorDiv.html('');
        } else {
            var msg = displayWarningMessage(duplicates);
            topErrorDiv.html(msg);
            inlineErrorDiv.html(msg.clone());
        }
    };

    /**
     * Display an error message if we find aids that might be duplicate.
     */
    var warnForDuplicates = function () {
        var duplicates = fetchDuplicates();
        duplicates.then(hideOrShowMessage);
    };

}(this, $ || django.jQuery));

(function ($) {
    $(document).ready(function () {
        var aidForm = $('#aid_form').length ? $('#aid_form') : $('#aid-edit-form');
        var buster = new DuplicateBuster(aidForm);
        buster.init();
    });
})($ || django.jQuery);
