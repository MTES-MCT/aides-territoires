(function ($) {
    'use strict';

    const MAX_RESULTS = 5;  // Don't display more duplicate

    // Create a div to hold the error message
    var errorDiv = $('<div id="duplicate-message"></div>');

    // Insert the message holding div into the dom
    var initializeErrorDom = function() {
        errorDiv.insertBefore('form#aid_form > div');
    };

    // Generate a link to a single duplicate aid
    var formatSingleDuplicate = function(data) {
        var a = $('<a/>');
        a.attr('href', data['url']);
        a.html(data['name']);

        var li = $('<li/>');
        li.append(a);
        return li;
    };

    /**
     * Create a warning message with links to the related aids.
     */
    var createWarningMessage = function(apiData) {
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
     * Display an error message if we find aids that might be duplicate.
     */
    var warnForDuplicates = function(form) {
        var query = '/api/aids/?version=1.1&text=Réduire';
        $.getJSON(query, function(data) {

            var count = data['count'];
            if (count == 0) {
                errorDiv.html('');
            } else {
                var msg = createWarningMessage(data);
                errorDiv.html(msg);
            }
        });
    };

    $(document).ready(function () {
        var aidEditForm = $('form#aid_form');

        initializeErrorDom();
        aidEditForm.on('change', warnForDuplicates);

    });
}($ || django.jQuery));
