(function (exports, catalog) {

    exports.Pagination = function(current_page, last_page) {
        this.current_page = current_page;
        this.last_page = last_page;
    };

    exports.Pagination.prototype.showMoreResults = function () {

        // get form params
        url = new URL(this.current_page);
        searchParams = url.searchParams

        // new value of "page" is set to "next_page_number"
        page_number = searchParams.get("page")

        if (page_number !== null) {
            next_page_number = (parseInt(page_number) + 1).toString()
        } else {
            page_number = 1
            next_page_number = (parseInt(page_number) + 1).toString()
        }

        searchParams.set('page', next_page_number)

        // change the search property of the main url
        url.search = searchParams.toString();

        // the new url string
        var new_url = url.toString();

        if(this.current_page !== this.last_page) {
            $("#show_more_btn").attr("disabled", true);
            searchXHR = $.ajax({
                type: "GET",
                url: new_url,
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
                    $("#show_more_btn").attr("disabled", false);
                },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
        } else {
            $('#show_more').addClass('d-none')
        }
        this.current_page = new_url
        if(this.current_page == this.last_page) {
            $('#show_more').addClass('d-none')
        }
    };

})(this, catalog);

$(document).ready(function () {

    // Hide pagination's div and display #show_more button instead
    $('#show_more').removeClass('d-none')
    $('#pagination ul.pagination').addClass('d-none')
    $('#spinner').addClass("d-none");

    // get current_page & last_page url
    var pagination = new Pagination(window.location.href, $(".last")[0].href);

    // On click on #show_more button display new results on the same page. 
    $("#show_more_btn").on("click", pagination.showMoreResults.bind(pagination));
});