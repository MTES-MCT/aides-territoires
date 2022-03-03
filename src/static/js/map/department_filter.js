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
        let new_url = window.location.origin + "/cartographie/" + $(this).val() + return_page;
        window.location.replace(new_url + window.location.search);
    });

    /* use the org filter */
    $("#select-organization").change(function () {
        let audience = $(this).val();
        set_param_value("target_audience", audience);
    });

    /* use the aid_type filter */
    $("#select-aid-type").change(function () {
        let aid_type = $(this).val();
        set_param_value("aid_type", aid_type);
    });
};