(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (buttons, stepName) {
        buttons.click(function () {
            try {
                var audience = $(this).html().trim();
                if (_paq) {
                    _paq.push(['trackEvent', 'Recherche', stepName, audience]);
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
    var SEARCH_STEP = 'Étape 1 – Structure';

    var audienceButtons = $('form#audience button[type=submit]');
    trackSearchEvent(audienceButtons, SEARCH_STEP);

    var skipBtn = $('div.navigation-links a.next-btn');
    trackSkipEvent(skipBtn, SEARCH_STEP);
});
