/**
 * Dynamic search engine definition.
 *
 * Every time the search filter form is changed, fetch new results immediately.
 */
(function (exports, catalog) {
    // When the search filter form is used, we dynamically fetch new
    // results and display them on the spot. We also update the url,
    // so the current search remains bookmarkable.
    var results_div = $('div#search-results');
    var results_url = catalog.search_url;
    var searchXHR = undefined;
    var pendingRequest = false;

    exports.renderSearchResults = function (event) {
        var $form = $(this);
        var search_parameters = $form.serialize();

        // If a pending request exists, abort it before we start a new one
        if (pendingRequest && searchXHR) {
            searchXHR.abort();
        }

        searchXHR = $.ajax({
            url: results_url,
            data: search_parameters,
            dataType: 'html',
            beforeSend: function () {
                pendingRequest = true;
                results_div.addClass('loading');
            }
        }).done(function (result) {
            results_div.html(result)

            var new_url = '?' + search_parameters;
            history.replaceState(null, null, new_url);
        }).always(function () {
            pendingRequest = false;
            results_div.removeClass('loading');
        });
    };

})(this, catalog);

$(document).ready(function () {
    $('div#search-engine form').on('change submit keyup', renderSearchResults);

    // Since we use js to dynamically fetch new results, it's better
    // to hide the useless submit button. We do it using js, so
    // the search feature remains fully working when js is not available.
    $('div#search-engine button[type=submit]').hide();
});