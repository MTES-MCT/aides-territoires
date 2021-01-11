(function ($) {
    'use strict';

    const MAX_RESULTS = 5;  // Don't display more duplicate

    const API_ENDPOINT = '/api/aids/?version=1.1&drafts=True';

    var form = $('form#aid_form');
    var urlField = $('#id_origin_url');

    // Create a div to hold the error message
    var errorDiv = $('<div class="inline-error"></div>');

    // Insert the message holding div into the dom
    var initializeErrorDom = function() {
        errorDiv.insertAfter('input#id_origin_url');
    };

    // Generate a link to a single duplicate aid
    var formatSingleDuplicate = function(data) {
        var a = $('<a/>');
        var url = '/admin/aids/aid/' + data['id'] + '/change/';
        a.attr('href', url);
        a.html(data['name']);

        var li = $('<li/>');
        li.append(a);
        return li;
    };

    /**
     * Create a warning message with links to the related aids.
     */
    var displayWarningMessage = function(apiData) {
        var messageDiv = $('<div class="errornote" />');

        var messageP = $('<p>Attention ! Nous avons trouvé des aides qui ressemblent à des doublons.</p>');

        var count = apiData['count'];
        var maxResults = Math.min(count, MAX_RESULTS);
        var duplicates = apiData['results']
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
    var buildSearchForDuplicateQuery = function() {
        var origin_url = $('#id_origin_url').val();

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
    var fetchDuplicates = function() {
        var query = buildSearchForDuplicateQuery();
        if (query === null) {
            // If we can't call the api, just return an empty result set
            return new Promise(function() { return {count: 0, results: []}; });
        }

        return $.getJSON(query);
    };

    /**
     * Hide or display a warning message depending on the duplicates found
     */
    var hideOrShowMessage = function(duplicates) {
        var count = duplicates['count'];
        var results = duplicates['results'];
        var currentSlug = $('#id_slug').val();

        // Be careful as to not count the current aid as a duplicate of itself
        if (count == 0 || count == 1 && results[0]['slug'] == currentSlug) {
            errorDiv.html('');
        } else {
            var msg = displayWarningMessage(duplicates);
            errorDiv.html(msg);
        }
    };

    /**
     * Display an error message if we find aids that might be duplicate.
     */
    var warnForDuplicates = function() {
        var duplicates = fetchDuplicates();
        duplicates.then(hideOrShowMessage);
    };

    $(document).ready(function () {
        var aidEditForm = $('form#aid_form');

        initializeErrorDom();
        aidEditForm.on('change', warnForDuplicates);

    });
}($ || django.jQuery));
