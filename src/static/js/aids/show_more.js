// Hide pagination's div and display #show_more button instead
$('#show_more').removeClass('d-none')
$('.pagination').addClass('d-none')

// Catch and serialize research form  
next_url = $(".form-body").serialize()

// Catch next_page and last_page url 
next_page = $(".next")[0].href
last_page = $(".last")[0].href

// On click on #show_more button display new results on the same page. 
$("#show_more_btn").on("click", function(e){
    e.preventDefault();
    next_page = $(".next")[0].href
    last_page = $(".last")[0].href
    $.ajax({
        type: "GET",
        url: $(".next")[0].href,
        cache: false,
        success: function(html){
            html_parsed = $.parseHTML(html)
            $('.aids').append($(html_parsed).find(".aids > .col"))
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }  
    });
    console.log(next_url)
    console.log(next_page)
    console.log(last_page)
})
