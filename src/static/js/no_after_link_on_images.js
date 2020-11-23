$(document).ready(function() {
    $(document).ready(function() {
        let linksForImages = $("a:has(img)")
        for (link of linksForImages) {
            link.classList.add("no-after")
        }
    });    
});
