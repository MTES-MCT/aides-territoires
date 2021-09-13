(function (exports) {
    "use strict";

    exports.trackResultsAlertButtonClick = function(alert_link, source) {
        alert_link.click(function(evt) {
            if (_paq) {
                _paq.push(['trackEvent', 'Alerte bouton', source]);
            }
        });
    }
})(this);

$(document).ready(function () {
    // Track clicks on alert button above the search form
    var resultsFormAlertButton = $('button#save-alert-btn');
    if (resultsFormAlertButton) {
        trackResultsAlertButtonClick(resultsFormAlertButton, 'Alerte bouton click (résultats > cartouche)');
    }

    // Track clicks on alert button in the aid results (alert block)
    var resultsBlockAlertButton = $('button#save-alert-results-block-btn');
    if (resultsBlockAlertButton) {
        trackResultsAlertButtonClick(resultsBlockAlertButton, 'Alerte bouton click (résultats > encart)');
    }

    // Track clicks on alert button in the aid detail (alert block)
    var resultsBlockAlertButton = $('button#save-alert-detail-block-btn');
    if (resultsBlockAlertButton) {
        trackResultsAlertButtonClick(resultsBlockAlertButton, 'Alerte bouton click (fiche aide)');
    }
});
