(function (exports, catalog) {
    'use strict';

    /**
     * Hide secondary content and create a button to reveal it.
     */
    exports.enableRevealButton = function(content) {
        content.addClass('collapse');

        var button = $('<button />');
        button.attr('type', 'button');
        button.addClass('btn btn-primary mt-2');
        button.html(catalog.show_me_more);

        button.insertAfter(content);

        button.click(function() {
            if (content.hasClass('show')) {
                button.html(catalog.show_me_more);
            } else {
                button.html(catalog.show_me_less);
            }

            content.collapse('toggle');
        });
    };

}(this, catalog));

$(document).ready(function() {
    var content = $('#more-content');
    if (content) {
        enableRevealButton(content);
    }
});
