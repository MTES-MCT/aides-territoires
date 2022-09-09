(function (exports) {
    'use strict';

    /**
     * Hide some piece of information until some button is clicked.
     * This is required to track user engagement.
     */
    exports.originUrlCTA = function(OriginUrlBtn, aid_slug) {

        OriginUrlBtn.click(function() {

            // Send an event to our stats DB
            var statsData = JSON.stringify({
                aid: AID_ID,
                querystring: CURRENT_SEARCH
            });
            $.ajax({
                type: 'POST',
                url: `/api/stats/aid-originurl-click-events/`,
                contentType: 'application/json',
                headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
                dataType: 'json',
                data: statsData
            })

            // Send an event to Matomo
            if (_paq) {
                _paq.push(['trackEvent', 'Fiche aide', 'Clic lien vers le descriptif complet', aid_slug]);
            }
        });
    };

    exports.applicationUrlCTA = function(ApplicationUrlBtn, aid_slug) {

        ApplicationUrlBtn.click(function() {

            // Send an event to our stats DB
            var statsData = JSON.stringify({
                aid: AID_ID,
                querystring: CURRENT_SEARCH
            });
            $.ajax({
                type: 'POST',
                url: `/api/stats/aid-applicationurl-click-events/`,
                contentType: 'application/json',
                headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
                dataType: 'json',
                data: statsData
            })

            // Send an event to Matomo
            if (_paq) {
                _paq.push(['trackEvent', 'Fiche aide', 'Clic lien candidater', aid_slug]);
            }
        });
    };

    exports.trackOutclicks = function(links, aid_slug) {
        links.click(function(evt) {
            // Send an event to Matomo
            if (_paq) {
                _paq.push(['trackEvent', 'Fiche aide', 'Voir lien du porteur', aid_slug, this.href]);
            }
        });
    }

})(this);

$(document).ready(function () {
    var dataDiv = $('div#contact');
    var OriginUrlBtn = $('a#origin_url_btn');
    var ApplicationUrlBtn = $('a#application_url_btn');

    // Track clicks on "application_url" & "origin_url" buttons
    originUrlCTA(OriginUrlBtn, AID_SLUG);
    applicationUrlCTA(ApplicationUrlBtn, AID_SLUG);

    // Track clicks on outlinks
    var links = dataDiv.find('a');
    trackOutclicks(links, AID_SLUG);
});
