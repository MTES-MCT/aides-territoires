(function (exports, _paq) {
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
            if (_paq) {
                _paq.push(['trackEvent', 'Fiche aide', 'Voir contacts', aid_slug]);
            }
            revealBtn.remove();
        });
    };


})(this, _paq);

$(document).ready(function () {
    var dataDiv = $('#going-further');
    enableCTA(dataDiv, catalog.going_further_cta_label, AID_SLUG);
});
