$(document).ready(function () {
    'use strict';

    if (!$) {
        $ = django.jQuery;
    }
    $('form #id_name').softmaxlength();
});