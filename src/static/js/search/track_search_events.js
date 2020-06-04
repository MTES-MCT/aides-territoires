(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (perimeter, categories, nbResults, stepName) {
        try {
            var allCategories = categories.reduce(function (acc, value) {
                var accumulated;
                if (acc == '') {
                    accumulated = value;
                } else {
                    accumulated = acc + "|" + value;
                }
                return accumulated;
            }, '');

            var eventName;
            if (perimeter) {
                eventName = perimeter + ' > ' + allCategories;
            } else {
                eventName = allCategories;
            }

            console.log(stepName, eventName, nbResults);
            if (_paq) {
                _paq.push(['trackEvent', 'Recherche', stepName, eventName, nbResults]);
            }
        } catch (e) {
            console.log(e);
        }
    }

})(this);

$(document).ready(function () {
    var SEARCH_STEP = 'Étape 5 – Résultats';
    trackSearchEvent(PERIMETER, CATEGORIES, NB_RESULTS, SEARCH_STEP);
});
