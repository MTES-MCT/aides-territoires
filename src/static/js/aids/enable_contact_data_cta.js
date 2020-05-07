(function (exports, catalog) {
    "use strict";

    /**
     * Hide some piece of information until some button is clicked.
     *
     * This is required to track user engagement.
     */
    exports.enableCTA = function(div, btnLabel) {
        div.addClass('collapse');

        var revealBtn = $('<button type="button" class="cta-btn"></button>');
        revealBtn.html(btnLabel);
        revealBtn.insertBefore(div);

        revealBtn.click(function() {
            div.collapse('show');
            revealBtn.remove();
        });
    };


})(this, catalog);

$(document).ready(function () {
    var dataDiv = $('#going-further');
    enableCTA(dataDiv, catalog.going_further_cta_label);
});
