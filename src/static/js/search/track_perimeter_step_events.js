(function (exports) {
    "use strict";

    exports.trackSearchEvent = function(form, stepName) {
        form.submit(function() {
            var perimeter = $(this).find('[name=perimeter]').select2('data')[0].text;
            if (_paq) {
                _paq.push(['trackEvent', 'Recherche', stepName, perimeter]);
            }
        });
    }

    exports.trackSkipEvent = function(link, stepName) {
        link.click(function() {
            if (_paq) {
                _paq.push(['trackEvent', 'Recherche', stepName, 'Passée']);
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
