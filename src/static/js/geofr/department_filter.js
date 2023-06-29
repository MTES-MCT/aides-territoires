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
            let new_url = ""
            if ($("#backers-by-departement").length) {
                new_url = window.location.origin + "/cartographie/" + department + return_page;
            } else {
                new_url = window.location.origin + "/cartographie/" + department + "/porteurs" + return_page;
            }
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

    /* use the perimeter_scale filter */
    $("#select-perimeter-scale").change(function () {
        let perimeter_scale = $(this).val();
        if (perimeter_scale.match(SANE_ID_REGEX)) {
            set_param_value("perimeter_scale", perimeter_scale);
        } else {
            console.log("Invalid perimeter scale");
        }
    });

    /* use the backer_category filter */
    $("#select-backer-category").change(function () {
        let backer_category = $(this).val();
        if (backer_category.match(SANE_ID_REGEX)) {
            set_param_value("backer_category", backer_category);
        } else {
            console.log("Invalid backer category");
        }
    });

    /* use the aid_category filter */
    $("#id_categories").change(function () {
        let aid_category = $(this).val();
        set_param_value("aid_category", aid_category);
    });
};
