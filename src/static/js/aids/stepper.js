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
    let stepperButtons = $('#nav-form a');

    stepperButtons.on("click", function () {
        let clickedButtonTarget = $(this).attr("href")
        toggleActiveStepperButton(stepperButtons, clickedButtonTarget)
    });

    let $sectionTitles = $('.at-stepper--section-title');

    $(window).on("scroll", function () {
        let topSectionID = "#" + $sectionTitles.filter((i, el) => $(el).offset().top > ($(window).scrollTop() - 300)).first().prop('id')
        toggleActiveStepperButton(stepperButtons, topSectionID)
    })
});
