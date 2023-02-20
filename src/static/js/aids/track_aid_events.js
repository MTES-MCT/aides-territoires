(function (exports) {
    'use strict';

    /**
     * Hide some piece of information until some button is clicked.
     * This is required to track user engagement.
     */
    exports.originUrlCTA = function(OriginUrlBtn, aid_slug) {

        OriginUrlBtn.click(function() {

            // Send an event to our stats DB
            let statsData = JSON.stringify({
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

    exports.applicationUrlCTA = function(ApplicationUrlBtn, aid_slug, prepopulate_application_url=None, organization=None, ds_folder_url=None, ds_folder_id=None, ds_folder_number=None) {

        ApplicationUrlBtn.click(function() {

            // Send an event to our stats DB
            let statsData = JSON.stringify({
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

            // if application_url is a link to a prepopulate Démarches-Simplifiées folder
            // create a AidCreateDSFolderEvent
            if(PREPOPULATE_APPLICATION_URL) {
                let statsData2 = JSON.stringify({
                    aid: AID_ID,
                    organization:ORGANIZATION,
                    ds_folder_url:DS_FOLDER_URL,
                    ds_folder_id:DS_FOLDER_ID,
                    ds_folder_number:DS_FOLDER_NUMBER,
                });
                $.ajax({
                    type: 'POST',
                    url: `/api/stats/aid-create-ds-folder-events/`,
                    contentType: 'application/json',
                    headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
                    dataType: 'json',
                    data: statsData2
                })
                if (_paq) {
                    _paq.push(['trackEvent', 'Fiche aide', 'Clic lien vers le dossier Démarches-Simplifiées prérempli', aid_slug]);
                }
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
    let dataDiv = $('div#contact');
    let OriginUrlBtn = $('a#origin_url_btn');
    let ApplicationUrlBtn = $('a#application_url_btn');

    // Track clicks on "application_url" & "origin_url" buttons
    originUrlCTA(OriginUrlBtn, AID_SLUG);
    applicationUrlCTA(ApplicationUrlBtn, AID_SLUG, PREPOPULATE_APPLICATION_URL, ORGANIZATION, DS_FOLDER_URL, DS_FOLDER_ID, DS_FOLDER_NUMBER);

    // Track clicks on outlinks
    let links = dataDiv.find('a');
    trackOutclicks(links, AID_SLUG);
});
