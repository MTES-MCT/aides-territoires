(function (exports) {
    "use strict";

    exports.trackSearchEvent = function (form, stepName) {
        form.submit(function () {
            try {

                var inputs = $(this).find('input[type=checkbox]:checked').map(function () {
                    return $(this).val().trim();
                });
                var allCategories = inputs.toArray().reduce(function (acc, value) {
                    var accumulated;
                    if (acc == '') {
                        accumulated = value;
                    } else {
                        accumulated = acc + "|" + value;
                    }
                    return accumulated;
                }, '');

                var audience = $('#id_targeted_audiences option:selected:visible').text();
                var perimeter = $(this).find('[name=perimeter]').select2('data')[0].text;
                var key_word = $(this).find('input#id_text').val();
                var eventName = audience + ';' + perimeter + ';' + key_word + ';' + allCategories;
                if (eventName == ";;;") {
                    eventName = "Recherche vide"
                }

                if (_paq) {
                    _paq.push(['trackEvent', 'Recherche', stepName, eventName]);
                }
            } catch (e) {
                console.log(e);
            }
        })
    }
})(this);

$(document).ready(function () {
    var SEARCH_STEP = 'Trouver des aides';

    var searchForm = $('form#general_search_form');
    trackSearchEvent(searchForm, SEARCH_STEP);
});