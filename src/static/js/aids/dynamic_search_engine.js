/**
 * Dynamic search engine definition.
 *
 * Every time the search filter form is changed, fetch new results immediately.
 */
(function (exports, catalog) {
    'use strict';

    // When the search filter form is used, we dynamically fetch new
    // results and display them on the spot. We also update the url,
    // so the current search remains bookmarkable.
    var resultsDiv = $('div#search-results');
    var resultsUrl = catalog.search_url;
    var searchXHR = undefined;
    var pendingRequest = false;
    var searchForm = $('div#search-engine form');
    var filtersDiv = $('div#filters');

    var markRequestAsPending = function () {
        pendingRequest = true;
        resultsDiv.addClass('loading');
    };

    var markRequestAsCompleted = function () {
        pendingRequest = false;
        resultsDiv.removeClass('loading');
    };

    var displaySearchResults = function (results) {
        resultsDiv.html(results)
    };

    var updateUrl = function (searchParams) {
        var newUrl = '?' + searchParams;
        history.replaceState(null, null, newUrl);
    };

    var updateSearchResults = function (event) {
        var searchParams = searchForm.serialize();

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

    var filterButton = function (fieldName, fieldLabel, fieldValue, fieldText) {
        return `
            <button data-field="${fieldName}" data-value="${fieldValue}">
                ${fieldLabel} : ${fieldText}
                <i class="fas fa-times"></i>
            </button>
        `
    };

    var renderSearchFilters = function (event) {
        filtersDiv.html('');
        var filterButtons = [];

        var textFields = searchForm.find('input[type=text], input[type=date]');
        for (var i = 0; i < textFields.length; i++) {
            var field = $(textFields[i]);
            var label = field.attr('name');
            var value = field.val();
            if (value !== '') {
                var buttonHtml = filterButton(label, label, value, value);
                filterButtons.push(buttonHtml);
            }
        }

        var selectFields = searchForm.find('select');
        for (var i = 0; i < selectFields.length; i++) {
            var field = $(selectFields[i]);
            var label = field.attr('name');
            var values = field.select2('data');

            for (var j = 0; j < values.length; j++) {
                var value = values[j].id;
                var text = values[j].text;

                if (value !== '') {
                    var buttonHtml = filterButton(label, label, value, text);
                    filterButtons.push(buttonHtml);
                }
            }
        }

        var checkboxFields = searchForm.find('input[type=checkbox]');
        for (var i = 0; i < checkboxFields.length; i++) {
            var field = $(checkboxFields[i]);
            if (field.is(':checked')) {
                var label = field.attr('name');
                var value = field.val();
                if (value !== '') {
                    var buttonHtml = filterButton(label, label, value, value);
                    filterButtons.push(buttonHtml);
                }
            }
        }

        for (var i = 0; i < filterButtons.length; i++) {
            filtersDiv.append(filterButtons[i]);
        }
    };

    exports.renderSearchFilters = renderSearchFilters;

    exports.renderSearch = function (event) {
        updateSearchResults(event);
        renderSearchFilters(event);
    };

    exports.clearFilter = function (event) {
        var button = $(this);
        var filterFieldName = button.data('field');
        var filterFieldValue = button.data('value');
        var field = searchForm.find(`input[name=${filterFieldName}], select[name=${filterFieldName}]`);
        var currentValue = field.val();

        if (Array.isArray(currentValue)) {
            var filteredValue = currentValue.filter(function(elt) {
                return elt != filterFieldValue;
            });
            field.val(filteredValue);
        } else {
            field.val('');
        }

        field.trigger('change');
        renderSearch();
    };

})(this, catalog);

$(document).ready(function () {
    $('div#search-engine form').on('change submit', renderSearch);
    $('div#search-engine form').on('keyup', 'input[type=text]', renderSearch);
    $('div#filters').on('click', 'button', clearFilter);
    renderSearchFilters();

    // Since we use js to dynamically fetch new results, it's better
    // to hide the useless submit button. We do it using js, so
    // the search feature remains fully working when js is not available.
    $('div#search-engine button[type=submit]').hide();
});