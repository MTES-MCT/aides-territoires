(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (form, stepName) {
        form.submit(function () {
            try {
                var project = $(this).find(':checked').map(function () {
                    return $(this).val().trim();
                });
                if (_paq) {
                    _paq.push(['trackEvent', 'Recherche', stepName, project]);
                }
            } catch (e) {
                console.log(e);
            }
        });
    }

})(this);

$(document).ready(function () {
    var SEARCH_STEP = 'Étape 5 – Projets';

    var searchForm = $('form#project');
    trackSearchEvent(searchForm, SEARCH_STEP);
});
