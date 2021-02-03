(function (exports) {
    "use strict";

    exports.trackAlertValidation = function(form, alert_title) {
        form.submit(function() {
            if (_paq) {
                _paq.push(['trackEvent', 'Alerte email', 'Alerte créée', alert_title]);
            }
        });
    }

    exports.trackAlertDeletion = function(form, alert_title) {
        form.submit(function() {
            if (_paq) {
                _paq.push(['trackEvent', 'Alerte email', 'Alerte supprimée', alert_title]);
            }
        });
    }
})(this);

$(document).ready(function () {
    // Track alert validation
    var validateForm = $('form#validation-form');
    if (validateForm) {
        trackAlertValidation(validateForm, ALERT_TITLE);
    }

    var deleteForm = $('form#delete-form');
    if (deleteForm) {
        trackAlertDeletion(deleteForm, ALERT_TITLE);
    }
});
