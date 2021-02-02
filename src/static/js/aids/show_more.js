$('#show_more').removeClass('d-none')
$('.pagination').addClass('d-none')
next_url = $(".form-body").serialize()

$("#show_more_btn").on("click", function(){
    $.ajax({
        type: "GET",
        url: next_url,
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
})

