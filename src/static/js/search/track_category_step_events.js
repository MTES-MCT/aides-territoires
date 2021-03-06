(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (form, stepName) {
        form.submit(function () {
            try {
                var allCategories = $(this).find('input[type=checkbox]');

                var inputs = $(this).find(':checked').map(function () {
                    return $(this).val().trim();
                });
                var allInputs = inputs.toArray().reduce(function (acc, value) {
                    var accumulated;
                    if (acc == '') {
                        accumulated = value;
                    } else {
                        accumulated = acc + "|" + value;
                    }
                    return accumulated;
                }, '');
                if (_paq) {
                    _paq.push(['trackEvent', 'Recherche', stepName, allInputs, allCategories.length]);
                }
            } catch (e) {
                console.log(e);
            }
        });
    }

})(this);

$(document).ready(function () {
    var SEARCH_STEP = 'Étape 4 – Sous-thématiques';

    var searchForm = $('form#categories');
    trackSearchEvent(searchForm, SEARCH_STEP);
});
