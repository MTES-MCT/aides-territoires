(function ($) {
    'use strict';
    $(document).ready(function () {
        // An admin can add images, justify text.
        trumbowygConfig.btns.push(['image']);
        trumbowygConfig.btns.push([
            'justifyLeft',
            'justifyCenter',
        ]);
        $('textarea.textarea-wysiwyg').trumbowyg(trumbowygConfig);
    });
}($ || django.jQuery));