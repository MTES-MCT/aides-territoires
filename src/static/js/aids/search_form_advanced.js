$(document).ready(function () {

    const moreOptionsToggle = $("#search-form-more-options");
    const extraFields = $(".search-form-extra-field");


    moreOptionsToggle.on('click', function () {
        extraFields.show()
    });
});
