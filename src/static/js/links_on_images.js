$(document).ready(function() {
    $(document).ready(function() {
        // We don't want the visual "after effect" on images links.
        let linksForImages = $("a:has(img)")
        for (link of linksForImages) {
            link.classList.add("no-after")
        }
    });    
});
