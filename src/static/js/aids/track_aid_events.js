(function (exports) {
    'use strict';

    /**
     * Hide some piece of information until some button is clicked.
     * This is required to track user engagement.
     */
    exports.enableCTA = function(dataDiv, revealBtn, aid_slug) {

        revealBtn.click(function() {
            dataDiv.removeClass('fake-collapse', { duration: 500 });

            // Use the global Matomo tracker
            if (_paq) {
                _paq.push(['trackEvent', 'Fiche aide', 'Voir contacts', aid_slug]);
            }
            revealBtn.remove();
        });
    };

    exports.trackOutclicks = function(links, aid_slug) {
        links.click(function(evt) {
            if (_paq) {
                _paq.push(['trackEvent', 'Fiche aide', 'Voir lien du porteur', aid_slug, this.href]);
            }
        });
    }

})(this);

$(document).ready(function () {
    var dataDiv = $('div#going-further');
    var revealBtn = $('button#going-further-reveal-button');

    // Track clicks on "Going further" button
    enableCTA(dataDiv, revealBtn, AID_SLUG);

    // Track clicks on outlinks
    var links = dataDiv.find('a');
    trackOutclicks(links, AID_SLUG);
});
