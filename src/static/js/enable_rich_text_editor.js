(function ($) {
    'use strict';

    $(document).ready(function () {

        $('textarea.textarea-wysiwyg').trumbowyg({
            lang: 'fr',
            btnsDef: {
                image: {
                    dropdown: ['insertImage', 'upload'],
                    ico: 'insertImage'
                }
            },
            btns: [
                ['viewHTML'],
                ['undo', 'redo'],
                ['formatting'],
                ['strong', 'em'],
                ['link'],
                ['image'],
                ['unorderedList', 'orderedList'],
                ['removeformat'],
                ['fullscreen']
            ],
            minimalLinks: true,
            removeformatPasted: true,
            svgPath: '/static/trumbowyg/dist/ui/icons.svg',
            plugins: {
                upload: {
                    serverPath: '/upload/',
                    fileFieldName: 'image',
                    urlPropertyName: 'url'
                }
            }
        });
    });
}($ || django.jQuery));
