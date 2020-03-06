/**
 * A very simple plugin to display a char counter for input texts.
 *
 * This is very quick and dirty, but it's for internal usage only.
 */
(function ($) {
    'use strict';

    var updateCharCounter = function (input, counter, maxlength) {
        var inputLength = input.val().length;
        var counterInfo = '(' + inputLength + ' / ' + maxlength + ')';
        counter.html(counterInfo);

        if (inputLength > maxlength) {
            input.addClass('is-invalid');
            counter.addClass('out-of-range');
        } else {
            input.removeClass('is-invalid');
            counter.removeClass('out-of-range');
        }
    };

    $.fn.softmaxlength = function () {

        this.each(function () {
            var input = $(this);
            var maxlength = input.attr('maxlength');
            var inputId = input.attr('id');
            var label = $('label[for=' + inputId + ']');

            label.addClass('softmaxlength');

            // Create the counter element that will display remaining chars
            var counter = $('<span class="softmaxlength-counter"></span>');
            counter.appendTo(label);

            // Removes hard maxlength value
            // This ensures the browser won't prevent pasting data longer
            // than the `maxlength` value.
            input.attr('maxlength', '');

            // Display the counter everytime the input is changed
            updateCharCounter(input, counter, maxlength);
            input.on('input', function () {
                updateCharCounter(input, counter, maxlength);
            });
        });

        return this;
    };
})($ || django.jQuery);
