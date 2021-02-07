(function (exports, catalog) {

    exports.showMoreResults = function (event) {
        event.preventDefault();

        next_url = $("#search-form").serialize()
        next_page = $(".next")[0].href
        last_page = $(".last")[0].href

        if(next_page !== last_page) {
            searchXHR = $.ajax({
                type: "GET",
                url: next_page,
                cache: false,
                beforeSend: function () {
                    $('#show_more_text').addClass('d-none')
                    $('#spinner').removeClass("d-none");
                },
                success: function(html){
                    html_parsed = $.parseHTML(html)
                    $('.aids').append($(html_parsed).find(".aids > .col"))
                    $('#spinner').addClass("d-none");
                    $('#show_more_text').removeClass('d-none')
                },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
        } else {
            $('#show_more').removeClass('d-none')
        }
    };

})(this, catalog);

$(document).ready(function () {

    // Hide pagination's div and display #show_more button instead
    $('#show_more').removeClass('d-none')
    $('.pagination').addClass('d-none')
    $('#spinner').addClass("d-none");

    // On click on #show_more button display new results on the same page. 
    $("#show_more_btn").on("click", showMoreResults);
});
