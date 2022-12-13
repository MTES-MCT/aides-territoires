$(document).ready(function () {

    const URL_FRAGMENT_REGEX = /^[0-9a-z-_/]+$/;

    $('#select').on('change', function () {
        let url_fragment = $(this).val();
        if (url_fragment.match(URL_FRAGMENT_REGEX)) {
            window.location.href = url_fragment;
        } else {
            console.log("Invalid URL fragment");
        }
        return false;
    });
})