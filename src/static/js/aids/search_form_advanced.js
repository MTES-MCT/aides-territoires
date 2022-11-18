$(document).ready(function () {
    // Allows to show/hide the extra search fields
    const moreOptionsToggle = $("#search-form-more-options");
    const extraFields = $(".search-form-extra-fields");

    const moreOptionsText = {
        expand: moreOptionsToggle.html(), // Get the default value from the actual template
        contract: '<span class="fr-icon-subtract-line" aria-hidden="true"></span> Masquer les critères avancés',
    }

    moreOptionsToggle.on('click', function (event) {
        event.preventDefault();
        if (moreOptionsToggle.html() == moreOptionsText.expand) {
            extraFields.slideDown("fast");
            moreOptionsToggle.html(moreOptionsText.contract);
        } else {
            extraFields.slideUp("fast");
            moreOptionsToggle.html(moreOptionsText.expand);
        }
    });
});
