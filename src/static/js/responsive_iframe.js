$(document).ready(function () {
    // Making the iframe responsive if not already present
    if (!$("iframe").parents('.at-responsive-video').length) {
        $("iframe").wrap("<div class='at-responsive-video'></div>");
    }
});
