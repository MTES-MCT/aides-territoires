(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (form, stepName) {
        form.submit(function () {

            // We use a try/catch block because we don't want to block
            // the form submission in case anything in the event logging process
            // breaks.
            try {
                var perimeter = $(this).find('[name=perimeter]').select2('data')[0].text;
                if (_paq) {
                    _paq.push(['trackEvent', 'Recherche', stepName, perimeter]);
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
    var SEARCH_STEP = 'Étape 2 – Territoire';

    var searchForm = $('form#perimeter');
    trackSearchEvent(searchForm, SEARCH_STEP);

    var skipBtn = $('div.navigation-links a.next-btn');
    trackSkipEvent(skipBtn, SEARCH_STEP);
});
