$(document).ready(function () {
    'use strict';

    if (!$) {
        $ = django.jQuery;
    }
    $('form input#id_name').softmaxlength();
});