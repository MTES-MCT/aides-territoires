/**
 * Dynamic search engine definition.
 *
 * Every time the search filter form is changed, fetch new results immediately.
 */
(function (exports, catalog) {
    // When the search filter form is used, we dynamically fetch new
    // results and display them on the spot. We also update the url,
    // so the current search remains bookmarkable.
    var resultsDiv = $('div#search-results');
    var resultsUrl = catalog.search_url;
    var searchXHR = undefined;
    var pendingRequest = false;

    var markRequestAsPending = function() {
        pendingRequest = true;
        resultsDiv.addClass('loading');
    };

    var markRequestAsCompleted = function() {
        pendingRequest = false;
        resultsDiv.removeClass('loading');
    };

    var displaySearchResults = function(results) {
        resultsDiv.html(results)
    };

    var updateUrl = function(searchParams) {
        var newUrl = '?' + searchParams;
        history.replaceState(null, null, newUrl);
    };

    exports.updateSearchResults = function (event) {
        var $form = $(this);
        var searchParams = $form.serialize();

        // If a pending request exists, abort it before we start a new one
        if (pendingRequest && searchXHR) {
            searchXHR.abort();
        }

        searchXHR = $.ajax({
            url: resultsUrl,
            data: searchParams,
            dataType: 'html',
            beforeSend: function () {
                markRequestAsPending();
            }
        }).done(function (results) {
            displaySearchResults(results);
            updateUrl(searchParams);
        }).always(function () {
            markRequestAsCompleted();
        });
    };

})(this, catalog);

$(document).ready(function () {
    $('div#search-engine form').on('change submit keyup', updateSearchResults);

    // Since we use js to dynamically fetch new results, it's better
    // to hide the useless submit button. We do it using js, so
    // the search feature remains fully working when js is not available.
    $('div#search-engine button[type=submit]').hide();
});