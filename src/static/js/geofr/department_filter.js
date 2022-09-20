$(document).ready(function () {
    // Reset the selects when the "back" button is clicked
    $("select").each(function () {
        $(this).val($(this).find('option[selected]').val());
    });
})

var SANE_ID_REGEX = new RegExp("^[0-9a-z-_]+$");

set_param_value = function (param, value) {
    /* update or remove a GET parameter from the current URL */
    if ('URLSearchParams' in window) {
        let searchParams = new URLSearchParams(window.location.search);
        if (value) {
            searchParams.set(param, value);
        } else {
            searchParams.delete(param);
        }
        window.location.search = searchParams.toString();
    }
};

department_filter = function (return_page) {
    /* go to the map for the selected department */
    $("#select-department").change(function () {
        let department = $(this).val();
        if (department.match(SANE_ID_REGEX)) {
            let new_url = window.location.origin + "/cartographie/" + department + return_page;
            window.location.replace(new_url + window.location.search);
        } else {
            console.log("invalid id");
        }
    });

    /* use the org filter */
    $("#select-organization").change(function () {
        let audience = $(this).val();
        if (audience.match(SANE_ID_REGEX)) {
            set_param_value("target_audience", audience);
        } else {
            console.log("invalid id");
        }
    });

    /* use the aid_type filter */
    $("#select-aid-type").change(function () {
        let aid_type = $(this).val();
        if (aid_type.match(SANE_ID_REGEX)) {
            set_param_value("aid_type", aid_type);
        } else {
            console.log("invalid id");
        }
    });
};

$('#map-back-button a').on('click', function (e) {
    e.preventDefault();
    window.history.back();
});