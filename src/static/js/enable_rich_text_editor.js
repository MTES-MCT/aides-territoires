(function ($) {
    'use strict';
    $(document).ready(function () {
        trumbowygConfig.btns.push(['image'])  // An admin can add images
        $('textarea.textarea-wysiwyg').trumbowyg(trumbowygConfig);
    });
}($ || django.jQuery));