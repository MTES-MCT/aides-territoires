(function ($) {
    'use strict';

    $(document).ready(function () {
        $('form #id_title').softmaxlength();
        $('form #id_slug').softmaxlength();
        $('form #id_meta_title').softmaxlength();
        $('form #id_meta_description').softmaxlength();
    });
}($ || django.jQuery));
