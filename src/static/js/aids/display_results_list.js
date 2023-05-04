$(document).ready(function () {

    let display_mode = sessionStorage.getItem('display_mode');

    let displayAsList = function () {
        $('#btn-results-card').addClass('fr-btn--secondary')
        $('#btn-results-list').removeClass('fr-btn--secondary')
        $('#aids-as-list').removeClass('at-display__none')
        $('#aids-as-card').addClass('at-display__none')
        $('#btn-results-list').html('<span class="ri-list-check"></span> Affichage en liste')
        $('#btn-results-card').html('<span class="ri-function-line"></span>')
        $('#btn-results-list').attr("aria-pressed", true)
        $('#btn-results-card').removeAttr("aria-pressed")

    };

    let displayAsCard = function () {
        $('#btn-results-card').removeClass('fr-btn--secondary')
        $('#btn-results-list').addClass('fr-btn--secondary')
        $('#aids-as-list').addClass('at-display__none')
        $('#aids-as-card').removeClass('at-display__none')
        $('#btn-results-list').html('<span class="ri-list-check"></span>')
        $('#btn-results-card').html('<span class="ri-function-line"></span> Affichage en cartes')
        $('#btn-results-list').removeAttr("aria-pressed")
        $('#btn-results-card').attr("aria-pressed", true)
    };

    if (display_mode == 'list') {
        displayAsList();
    } else if (display_mode == 'card') {
        displayAsCard();
    }

    $('#btn-results-list').on('click', function () {
        displayAsList();
        sessionStorage.setItem('display_mode', 'list');
    })

    $('#btn-results-card').on('click', function () {
        displayAsCard();
        sessionStorage.setItem('display_mode', 'card');
    })

});