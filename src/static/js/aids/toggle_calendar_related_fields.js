(function (exports) {

    /**
     * Enable the calendar related fields toggling.
     *
     * For ongoing aids, calendar fields (opening date, closing date, etc.)
     * don't make any sense. So we will only display them when the current
     * `recurrence` field value maks sense.
     */
    exports.toggleCalendarFields = function(form, div) {

        var recurrence = form.find('select[name=recurrence]');
        var isOngoing = recurrence.val() == 'ongoing';
        var isEmpty = recurrence.val() == '';
        var hasErrors = div.find('p.error').length > 0;
        if ((isEmpty || isOngoing) && !hasErrors) {
            div.removeClass('fr-collapse--expanded');
        } else {
            div.addClass('fr-collapse--expanded');
        }
    };

})(this);

$(document).ready(function () {

    var aidEditForm = $('form.main-form');
    var calendarFieldsDiv = $('div#calendar-fields-collapse');
    toggleCalendarFields(aidEditForm, calendarFieldsDiv);
    aidEditForm.on('change', function() {
        toggleCalendarFields(aidEditForm, calendarFieldsDiv);
    });
});
