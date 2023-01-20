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
            let new_url = window.location.origin + "/projets/projets-subventionnés/résultats/?department_search=true&project_perimeter=" + department;
            window.location.href = new_url + window.location.search;
        } else {
            console.log("Invalid department id");
        }
    });
};

$('#map-back-button a').on('click', function (e) {
    e.preventDefault();
    window.history.back();
});