(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (form, stepName) {
        form.submit(function () {
            try {
                var labels = $(this).find(':checked').map(function (counter, checkbox) {
                    var label = form.find('label[for=' + checkbox.id + '].custom-control-label');
                    return label.text().trim();
                });
                var allLabels = labels.toArray().reduce(function (acc, value) {
                    return acc + "|" + value;
                }, '');
                if (_paq) {
                    _paq.push(['trackEvent', 'Recherche', stepName, allLabels]);
                }
            } catch (e) {
                console.log(e);
            }
        });
    }

    exports.trackSkipEvent = function (link, stepName) {
        link.click(function () {
            try {
                if (_paq) {
                    _paq.push(['trackEvent', 'Recherche', stepName, 'Passée']);
                }
            } catch (e) {
                console.log(e);
            }
        });
    }


})(this);

$(document).ready(function () {
    var SEARCH_STEP = 'Étape 3 – Thématiques';

    var searchForm = $('form#theme');
    trackSearchEvent(searchForm, SEARCH_STEP);

    var skipBtn = $('div.navigation-links a.next-btn');
    trackSkipEvent(skipBtn, SEARCH_STEP);
});
