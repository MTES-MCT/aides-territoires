// Load the aid preview page in an iframe in modal
$(document).ready(function () {
    "use strict";

    $('#aid-preview-modal').on('show.bs.modal', function () {
        var content = $(this).find('div.content');
        var iframe = $('<iframe />');
        iframe.attr('src', '{{ aid.get_absolute_url }}?integration=integration');
        content.html(iframe);
    });
});
