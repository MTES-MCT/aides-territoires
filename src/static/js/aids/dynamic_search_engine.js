/**
 * Dynamic search engine definition.
 *
 * Every time the search filter form is changed, fetch new results immediately.
 *
 * When the search filter form is used, we dynamically fetch new
 * results and display them on the spot. We also update the url,
 * so the current search remains bookmarkable at all time.
 *
 * At last, we save the current search params in a cookie, so we can display
 * the correct "Go back to your search" link in the aid detail page.
 */
(function (exports, catalog) {
    'use strict';

    var resultsDiv = $('div#search-results');
    var resultsUrl = catalog.search_url;
    var searchXHR = undefined;
    var searchForm = $('div#search-engine form');
    var orderField = $('div#search-engine select#id_order_by');

    var state = {
        pendingRequest: false,
        searchParams: searchForm.serialize(),
    }

    var fetchNewResults = function () {
        // If a pending request exists, abort it before we start a new one
        if (state['pendingRequest'] && searchXHR) {
            searchXHR.abort();
        }

        // Fetch results using ajax
        searchXHR = $.ajax({
            url: resultsUrl,
            data: state['searchParams'],
            dataType: 'html',
            beforeSend: function () {
                state['pendingRequest'] = true;
                renderPendingState();
            }
        }).always(function (results) {
            state['pendingRequest'] = false;
            renderState(results);
        });
    };

    var renderState = function (results) {
        renderResults(results);
        renderUrl();
        renderPendingState();
        renderSessionCookie();
    }

    /**
     * Update the UI to show whether the request is pending or completed.
     */
    var renderPendingState = function () {
        var isPending = state['pendingRequest'];
        if (isPending) {
            resultsDiv.addClass('loading');
        } else {
            resultsDiv.removeClass('loading');
        }
    }

    /**
     * Inserts the results from the search api inside the dom.
     * Since the api returns html, this is pretty straightforward.
     */
    var renderResults = function (results) {
        resultsDiv.html(results)
    };

    /**
     * Updathe the url with the new search parameters, and reflects that
     * in the browser's history.
     */
    var renderUrl = function () {
        var newUrl = '?' + state['searchParams'];
        history.replaceState(null, null, newUrl);
    };

    /**
     * Saves the current search in a cookie for later retrieval.
     */
    exports.renderSessionCookie = function() {
        var searchUrl = state['searchParams'];
        document.cookie = catalog.SEARCH_COOKIE_NAME + '=' + searchUrl;
    };

    var updateSearch = function () {
        var newSearchParams = searchForm.serialize();
        if (state['searchParams'] != newSearchParams) {
            state['searchParams'] = newSearchParams;
            fetchNewResults();
        }
    };

    var updateSort = function(sortCriteria) {
        orderField.val(sortCriteria);
    };

    /**
     * Updating the search form triggers a new search query.
     */
    exports.onFormSubmit = function (event) {

        // if the "save bookmark" button was clicked, the form submission
        // must proceed without interruption
        var activeElement = document.activeElement;
        if (activeElement) {
            var formaction = activeElement.getAttribute('formaction');
            if (formaction) {
                return;
            }
        }

        event.preventDefault();
        updateSearch();
    };

    exports.onSortCriteraSelected = function() {
        var a = $(this);
        var sortCriteria = a.data('sort');
        updateSort(sortCriteria);
        updateSearch();
    };

    /**
     * Converts the "order by" field into an hidden input.
     *
     * By default, we add a select field to let the user choose a specific
     * results ordering.
     *
     * But since we will handle ordering dynamically with a specific dynamic
     * widget, we convert the "order_by" select field into a hidden input.
     *
     * We make this conversion in javascript, so the ordering field remains
     * functional when javascript is disabled.
     */
    exports.hideOrderField = function() {
        var hiddenOrderField = $('<input type="hidden" name="order_by" id="id_order_by" />');
        var enclosingDiv = orderField.parent('div');
        enclosingDiv.replaceWith(hiddenOrderField);
        orderField = hiddenOrderField;
    };

})(this, catalog);

$(document).ready(function () {
    $('div#search-engine form').on('submit', onFormSubmit);
    $('div#search-results').on('click', 'div#sorting-menu a', onSortCriteraSelected);

    renderSessionCookie();
    hideOrderField();
});