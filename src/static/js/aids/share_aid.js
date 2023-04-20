$(document).ready(function () {

    $("#clipboard-btn").on("click", function () {

        input_url = $("#currentUrl")

        input_url.focus();
        input_url.select();
        document.execCommand("copy");
    })


    let facebook_btn = document.getElementById("fr-btn--facebook");

    facebook_btn.addEventListener(
        "click", function () {
            window.open(
                this.href,
                'Partager sur Facebook - ouvre une nouvelle fenêtre',
                'toolbar=no,location=yes,status=no,menubar=no,scrollbars=yes,resizable=yes,width=600,height=450'
            );
            event.preventDefault();
        }
    );

    let twitter_btn = document.getElementById("fr-btn--twitter");

    twitter_btn.addEventListener(
        "click", function () {
            window.open(
                this.href,
                'Partager sur Twitter - ouvre une nouvelle fenêtre',
                'toolbar=no,location=yes,status=no,menubar=no,scrollbars=yes,resizable=yes,width=600,height=420'
            );
            event.preventDefault();
        }
    );

    let linkedin_btn = document.getElementById("fr-btn--linkedin");

    linkedin_btn.addEventListener(
        "click", function () {
            window.open(
                this.href,
                'Partager sur LinkedIn - ouvre une nouvelle fenêtre',
                'toolbar=no,location=yes,status=no,menubar=no,scrollbars=yes,resizable=yes,width=550,height=550'
            );
            event.preventDefault();
        }
    );

})
