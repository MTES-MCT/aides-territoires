(function (exports) {
    // Update the "exclusion from search" status of a backer for the current user
    exports.toggleExcludeBacker = function () {
        let backerId = $(this).attr('data-at-backer-id');
        let isChecked = $(this).prop('checked');

        $.post(
            '/partenaires/masquer/' + backerId + '/',
            {
                'excluded': isChecked ? 1 : 0,
                'csrfmiddlewaretoken': csrf_token
            },
            function (data) {
                let nb_p = $("#nb-excluded-backers");

                if (data.nb_excluded == 0) {
                    nb_p.html("Tous les porteurs sont affichés.")
                }
                else if (data.nb_excluded == 1) {
                    nb_p.html(data.nb_excluded + ' porteur masqué.')
                }
                else {
                    nb_p.html(data.nb_excluded + ' porteurs masqués.')
                }
            },
        );
    };
})(this);
$(document).ready(function () {
    const backerToggles = $('#at-backer-toggles .fr-toggle__input');
    backerToggles.on('click', toggleExcludeBacker);
});
