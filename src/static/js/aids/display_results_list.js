$(document).ready(function () {

    let display_mode = sessionStorage.getItem('display_mode');

    let displayOnList = function () {
        $('#btn-results-card').addClass('fr-btn--secondary')
        $('#btn-results-list').removeClass('fr-btn--secondary')
        $('#aid_in_list').removeClass('at-display__none')
        $('#aid_in_card').addClass('at-display__none')
    };

    let displayOnCard = function () {
        $('#btn-results-card').removeClass('fr-btn--secondary')
        $('#btn-results-list').addClass('fr-btn--secondary')
        $('#aid_in_list').addClass('at-display__none')
        $('#aid_in_card').removeClass('at-display__none')
    };

    if(display_mode == 'list') {
        displayOnList();
    } else if(display_mode == 'card') {
        displayOnCard();
    }

    $('#btn-results-list').on('click', function() {
        displayOnList();
        sessionStorage.setItem('display_mode', 'list');
    })

    $('#btn-results-card').on('click', function() {
        displayOnCard();
        sessionStorage.setItem('display_mode', 'card');
    })

});