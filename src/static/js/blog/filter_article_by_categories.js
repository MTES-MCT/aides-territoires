$(document).ready(function () {

    var URL_FRAGMENT_REGEX = new RegExp("^[0-9a-z-_/]+$");

    $('#select').on('change', function () {
        let url_fragment = $(this).val();
        if (url_fragment.match(URL_FRAGMENT_REGEX)) {
            window.location.replace(url_fragment);
        }
        return false;
    });
})