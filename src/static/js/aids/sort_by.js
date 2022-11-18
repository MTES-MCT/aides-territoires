// Manage the "sort by" button outside of the form on the aid search result page"
$("#order-by").change(function () {
    let allowed_values = ["relevance", "publication_date", "submission_deadline"]
    let sort_key = $(this).val();
    if ($.inArray(sort_key, allowed_values) == 0) {
        // Remove the parameter from the URL in the default case
        set_param_value("order_by", "");
    } else if ($.inArray(sort_key, allowed_values)) {
        set_param_value("order_by", sort_key);
    } else {
        console.log("Invalid sorting value");
    }
});