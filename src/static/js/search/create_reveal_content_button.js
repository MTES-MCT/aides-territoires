(function (exports, catalog) {
    'use strict';

    /**
     * Hide secondary content and create a button to reveal it.
     */
    exports.enableRevealButton = function(content) {
        content.addClass('collapse');

        var button = $('<button />');
        button.attr('type', 'button');
        button.addClass('btn btn-primary');
        button.html(catalog.show_me_more);

        button.insertBefore(content);

        button.click(function() {
            content.collapse('show');
            button.remove();
        });
    };

}(this, catalog));

$(document).ready(function() {
    var content = $('#more-content');
    if (content) {
        enableRevealButton(content);
    }
});
