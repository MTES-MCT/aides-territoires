(function (exports) {
    "use strict";

    /**
     * Hide some piece of information until some button is clicked.
     *
     * This is required to track user engagement.
     */
    exports.enableCTA = function(div, btnLabel, aid_slug) {
        div.addClass('collapse');

        var revealBtn = $('<button type="button" class="cta-btn"></button>');
        revealBtn.html(btnLabel);
        revealBtn.insertBefore(div);

        revealBtn.click(function() {
            div.collapse('show');

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
    // Track clicks on "Going further" button
    var dataDiv = $('#going-further');
    enableCTA(dataDiv, catalog.going_further_cta_label, AID_SLUG);

    // Track clicks on outlinks
    var links = dataDiv.find('a');
    trackOutclicks(links, AID_SLUG)
});
