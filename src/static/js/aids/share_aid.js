$(document).ready(function () {

    $("#clipboard-btn").on("click", function(){
        
        input_url = $("#currentUrl")
        
        input_url.focus();
        input_url.select();
        document.execCommand("copy");
    })

})
