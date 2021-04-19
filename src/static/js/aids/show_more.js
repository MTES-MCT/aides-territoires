(function (exports, catalog) {

    exports.Pagination = function(current_page, last_page) {
        this.current_page = current_page;
        this.last_page = last_page;
    };

    exports.Pagination.prototype.backToResults = function () {

        // Here we want to allow user to go back to the previous results page
        // But only if the user research is the same 

        // get form params
        url = new URL(this.current_page);
        searchParams = url.searchParams

        // We check if the search params extracted from url in localStorage
        // are identiqual to actual search (except page parameter)
        // If so, we use the value of current_page from localStorage to display previous page of results
        // else clear the localStorage and return
        url_LS = new URL(localStorage.getItem('current_page_LS'))
        searchParams_LS = url_LS.searchParams
        searchParams.delete("page")
        searchParams_LS.delete("page")

        if (searchParams_LS.toString() == searchParams.toString()) {
            url = new URL(localStorage.getItem('current_page_LS'))
            searchParams = url.searchParams
        } else {
            localStorage.clear();
            return
        }

        page_number = searchParams.get("page")

        // if page_number is > 1
        // we want to display all page between page 1 and the page_number
        if (page_number > 1 ) {
            previous_page_number = 2
            do {
                searchParams.set('page', previous_page_number)

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
                previous_page_number = (parseInt(previous_page_number) + 1).toString()
                if(this.current_page == this.last_page) {
                    $('#show_more').addClass('d-none')
                }
            }
            while (previous_page_number <= page_number)
        }
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
        localStorage.setItem('current_page_LS', new_url)
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

    // If current_page in sessionStorage
    // We try to display previous results
    if (localStorage.getItem('current_page_LS')) {
        pagination.backToResults();
    }
});