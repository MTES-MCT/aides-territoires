/**
 * Dynamic search engine definition.
 *
 * Every time the search filter form is changed, fetch new results immediately.
 *
 * When the search filter form is used, we dynamically fetch new
 * results and display them on the spot. We also update the url,
 * so the current search remains bookmarkable at all time.
 */
(function (exports, catalog) {
    'use strict';

    var resultsDiv = $('div#search-results');
    var resultsUrl = catalog.search_url;
    var searchXHR = undefined;
    var searchForm = $('div#search-engine form');
    var filtersDiv = $('div#search-engine div#filters');

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
        renderFilterButtons();
        renderPendingState();
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
     * Returns the html code of a single filter button.
     */
    var filterButton = function (fieldName, fieldLabel, fieldValue, fieldText) {
        // Using template stings was nice. Too bad IE11 does not support them.
        return '<button data-field="' +
            fieldName +
            '" data-value="' +
            fieldValue +
            '">' +
            fieldLabel + ': ' + fieldText +
            ' <i class="fas fa-times"></i></button> ';
    };

    /**
     * Display all the buttons that visually represents all the filters that
     * were selected to refine the search query.
     *
     * Several filter buttons can be rendered for a single field, e.g for
     * select multiple fields.
     */
    exports.renderFilterButtons = function (event) {
        var filterButtons = [];

        var textFields = searchForm.find('input[type=text], input[type=date]');
        for (var i = 0; i < textFields.length; i++) {
            var field = $(textFields[i]);
            var name = field.attr('name');
            var label = field.siblings('label');
            var value = field.val();
            if (value !== '') {
                var buttonHtml = filterButton(name, label.html(), value, value);
                filterButtons.push(buttonHtml);
            }
        }

        var selectFields = searchForm.find('select');
        for (var i = 0; i < selectFields.length; i++) {
            var field = $(selectFields[i]);
            var name = field.attr('name');
            var label = field.siblings('label');
            var values = field.select2('data');

            for (var j = 0; j < values.length; j++) {
                var value = values[j].id;
                var text = values[j].text;

                if (value !== '') {
                    var buttonHtml = filterButton(name, label.html(), value, text);
                    filterButtons.push(buttonHtml);
                }
            }
        }

        var checkboxFields = searchForm.find('input[type=checkbox]');
        for (var i = 0; i < checkboxFields.length; i++) {
            var field = $(checkboxFields[i]);
            if (field.is(':checked')) {
                var name = field.attr('name');
                var label = field.siblings('label');
                var value = field.val();
                if (value !== '') {
                    var buttonHtml = filterButton(name, label.html(), value, value);
                    filterButtons.push(buttonHtml);
                }
            }
        }

        var allFilters = '';
        for (var i = 0; i < filterButtons.length; i++) {
            allFilters += filterButtons[i];
        }
        filtersDiv.html(allFilters);
    };

    /**
     * Removes a single filter criteria.
     */
    var clearSingleFilter = function (button) {
        var filterFieldName = button.data('field');
        var filterFieldValue = button.data('value');
        var fieldSelector = 'input[name=' + filterFieldName + '], select[name=' + filterFieldName + ']';
        var field = searchForm.find(fieldSelector);
        var currentValue = field.val();

        // The filter can be for a single value field (input[type=text], checkbox, etc.)
        // or it can be a single value for a multiple choice field, which is
        // rendered with selecte2.
        if (Array.isArray(currentValue)) {
            var filteredValue = currentValue.filter(function (elt) {
                return elt != filterFieldValue;
            });
            field.val(filteredValue);
        } else if (field.prop('checked')) {
            field.prop('checked', false);
        } else {
            field.val('');
        }

        // Here, we are telling select2 to update the rendering of the field.
        field.trigger('change');
    };

    var updateSearch = function () {
        state['searchParams'] = searchForm.serialize();
        fetchNewResults();
    }

    /**
     * Updating the search form triggers a new search query.
     */
    exports.onSearchFormChanged = function () {
        updateSearch();
    };

    /**
     * Removing a search filter triggers a new search query.
     */
    exports.onSearchFilterRemoved = function () {
        var button = $(this);
        clearSingleFilter(button);
        updateSearch();
    }

})(this, catalog);

$(document).ready(function () {
    $('div#search-engine form').on('change submit', onSearchFormChanged);
    $('div#search-engine form').on('keyup', 'input[type=text]', onSearchFormChanged);
    $('div#filters').on('click', 'button', onSearchFilterRemoved);
    renderFilterButtons();

    // Since we use js to dynamically fetch new results, it's better
    // to hide the useless submit button. We do it using js, so
    // the search feature remains fully working when js is not available.
    $('div#search-engine button[type=submit]').hide();
});