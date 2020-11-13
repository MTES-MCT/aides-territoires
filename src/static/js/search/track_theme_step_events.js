(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (form, stepName) {
        form.submit(function () {
            try {
                var inputs = $(this).find(':checked').map(function (counter, checkbox) {
                    var input = form.find('input[id='+ checkbox.id + '][name=themes].custom-control-input');
                    return input.val().trim();
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
                    _paq.push(['trackEvent', 'Recherche', stepName, allInputs]);
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
