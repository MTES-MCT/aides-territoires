(function (exports) {
    'use strict';

    exports.registerFromNextPageWarningCTA = function (registerFromNextPageWarningButton) {

        registerFromNextPageWarningButton.click(function () {

            // Send an event to our stats DB
            let statsData = JSON.stringify({
                querystring: CURRENT_SEARCH
            });
            $.ajax({
                type: 'POST',
                url: `/api/stats/account-register-from-nextpagewarning-click-events/`,
                contentType: 'application/json',
                headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
                dataType: 'json',
                data: statsData
            })

            // Send an event to Matomo
            if (_paq) {
                _paq.push(['trackEvent', 'Compte Utilisateur', 'Clic sur le bouton Register-from-Next-Page-Warning']);
            }
        });
    };

})(this);

$(document).ready(function () {
    let registerFromNextPageWarningButton = $('a#register-from-next-page-warning');

    // Track clicks on the button
    registerFromNextPageWarningCTA(registerFromNextPageWarningButton);
});
