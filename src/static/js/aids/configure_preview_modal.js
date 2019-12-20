// Load the aid preview page in an iframe in modal
$(document).ready(function () {
    "use strict";

    $('#aid-preview-modal').on('show.bs.modal', function (event) {
        var previewBtn = $(event.relatedTarget);
        var previewUrl = previewBtn.data('preview-url');
        var content = $(this).find('div.content');
        var iframe = $('<iframe />');
        iframe.attr('src', previewUrl);
        content.html(iframe);
    });
});
