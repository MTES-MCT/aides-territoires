(function ($) {
    'use strict';

    $(document).ready(function () {
        $('form #id_name').softmaxlength();
        $('form #id_short_title').softmaxlength();
    });
}($ || django.jQuery));
