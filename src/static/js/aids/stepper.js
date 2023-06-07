(function (exports) {

    /**
     *  Toggle the active button on the stepper
     */
    exports.toggleActiveStepperButton = function (stepperButtons, activeButton) {
        stepperButtons.each(function () {
            if ($(this).attr("href") == activeButton) {
                $(this).removeClass("fr-btn--secondary")
                $(this).attr("aria-current", true)
            } else {
                $(this).addClass("fr-btn--secondary")
                $(this).removeAttr("aria-current")
            }
        })
    };

})(this);


$(document).ready(function () {
    // Update the stepper when clicking on one of the buttons
    let stepperButtons = $('#nav-form a:not(.fr-btn--tertiary-no-outline)');

    stepperButtons.on("click", function () {
        let clickedButtonTarget = $(this).attr("href")
        toggleActiveStepperButton(stepperButtons, clickedButtonTarget)
    });

    let $sections = $('.at-fields-section')

    $(window).on("scroll", function () {
        let currentPosition = $(this).scrollTop();
        $sections.each(function () {
            let sectionTop = $(this).offset().top - 100; // offsetting a bit to account for the sticky stepper
            let sectionBottom = sectionTop + $(this).outerHeight();
            let sectionTitle = $(this).find('.at-stepper--section-title');

            if (currentPosition >= sectionTop && currentPosition < sectionBottom) {
                let topSectionID = "#" + $(sectionTitle).attr('id');
                toggleActiveStepperButton(stepperButtons, topSectionID)
                return false; // Exit the loop once the current section is found
            }
        });
    })
});
