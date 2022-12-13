$(document).ready(function () {
    // Reset the selects when the "back" button is clicked
    $("select").each(function () {
        $(this).val($(this).find('option[selected]').val());
    });
})

const SANE_ID_REGEX = /^[0-9a-z-_]*$/;

function department_filter(return_page) {
    /* go to the map for the selected department */
    $("#select-department").change(function () {
        let department = $(this).val();
        if (department.match(SANE_ID_REGEX)) {
            let new_url = window.location.origin + "/cartographie/" + department + return_page;
            window.location.href = new_url + window.location.search;
        } else {
            console.log("Invalid department id");
        }
    });

    /* use the org filter */
    $("#select-organization").change(function () {
        let audience = $(this).val();
        if (audience.match(SANE_ID_REGEX)) {
            set_param_value("target_audience", audience);
        } else {
            console.log("Invalid target audience id");
        }
    });

    /* use the aid_type filter */
    $("#select-aid-type").change(function () {
        let aid_type = $(this).val();
        if (aid_type.match(SANE_ID_REGEX)) {
            set_param_value("aid_type", aid_type);
        } else {
            console.log("Invalid aid type id");
        }
    });
};

$('#map-back-button a').on('click', function (e) {
    e.preventDefault();
    window.history.back();
});