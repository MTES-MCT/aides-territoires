(function (exports) {
    "use strict";

    exports.trackAlertValidation = function(form, alert_title) {
        form.submit(function() {
            if (_paq) {
                _paq.push(['trackEvent', 'Alert email', 'Alerte créée', alert_title]);
            }
        });
    }

})(this);

$(document).ready(function () {
    // Track alert validation
    var form = $('for#validation-form');
    trackAlertValidation(form, ALERT_TITLE)
});
