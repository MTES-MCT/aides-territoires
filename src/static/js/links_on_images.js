$(document).ready(function () {
    // We don't want the visual "after effect" on images links.
    let linksForImages = $("a:has(img)")
    linksForImages.addClass('at-link-blank__none')
});
