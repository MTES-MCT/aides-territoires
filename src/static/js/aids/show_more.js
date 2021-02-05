$(document).ready(function () {

    // Hide pagination's div and display #show_more button instead
    $('#show_more').removeClass('d-none')
    $('.pagination').addClass('d-none')

    // On click on #show_more button display new results on the same page. 
    $("#show_more_btn").on("click", function(e){
        e.preventDefault();
        next_url = $(".form-body").serialize()
        next_page = $(".next")[0].href
        last_page = $(".last")[0].href

        if(next_page !== last_page) {
            searchXHR = $.ajax({
                type: "GET",
                url: next_page,
                cache: false,
                success: function(html){
                    html_parsed = $.parseHTML(html)
                    $('.aids').append($(html_parsed).find(".aids > .col"))
                },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })        
        } else {
            $('#show_more').removeClass('d-none')
        }
        console.log(next_page)
        console.log(last_page)
    })
});