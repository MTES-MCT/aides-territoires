(function (exports) {
    "use strict";

    exports.SavePromotionDisplayEvent = function (promotionLink) {

        promotionLink.each(function () {
            // Send an event to our stats DB
            let statsData = JSON.stringify({
                promotion: this.id,
                querystring: CURRENT_SEARCH
            });
            $.ajax({
                type: 'POST',
                url: `/api/stats/promotion-display-events/`,
                contentType: 'application/json',
                headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
                dataType: 'json',
                data: statsData
            })

        });
    };

    exports.SavePromotionClickEvent = function (promotionLink) {

        promotionLink.click(function () {
            // Send an event to our stats DB
            let statsData = JSON.stringify({
                promotion: this.id,
                querystring: CURRENT_SEARCH
            });
            $.ajax({
                type: 'POST',
                url: `/api/stats/promotion-click-events/`,
                contentType: 'application/json',
                headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
                dataType: 'json',
                data: statsData
            })

        });
    };

    exports.trackSearchEvent = function (perimeter, categories, nbResults, stepName) {
        try {
            let allCategories = categories.reduce(function (acc, value) {
                let accumulated;
                if (acc == '') {
                    accumulated = value;
                } else {
                    accumulated = acc + "|" + value;
                }
                return accumulated;
            }, '');

            let eventName;
            if (perimeter) {
                eventName = perimeter + ' > ' + allCategories;
            } else {
                eventName = allCategories;
            }

            if (_paq) {
                _paq.push(['trackEvent', 'Recherche', stepName, eventName, nbResults]);
            }
        } catch (e) {
            console.log(e);
        }
    }

})(this);

$(document).ready(function () {
    let SEARCH_STEP = 'Étape 5 – Résultats';
    trackSearchEvent(PERIMETER, CATEGORIES, NB_RESULTS, SEARCH_STEP);

    // Track clicks on #promotion-block-link button
    let promotionLink = $('#promotion-block-link>a');
    SavePromotionDisplayEvent(promotionLink);
    SavePromotionClickEvent(promotionLink);
});
