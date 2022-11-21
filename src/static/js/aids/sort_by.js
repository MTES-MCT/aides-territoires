// Manage the "sort by" button outside of the form on the aid search result page"
$("#order-by").change(function () {
    let sort_key = $(this).val();
    if (sort_key == "relevance") {
        // Remove the parameter from the URL in the default case
        set_param_value("order_by", "");
    } else if (["publication_date", "-publication_date", "submission_deadline"].indexOf(sort_key) >= 0) {
        set_param_value("order_by", sort_key);
    } else {
        console.log("Invalid sorting value");
    }
});
