(function($) {
    'use strict';

    $(function() {
        $('select#id_tags').djangoAdminSelect2({
            minimumInputLength: 2,
            ajax: {
                url: '/api/tags/',
                dataType: 'json',
                delay: 100,
            },
            tags: true,
            theme: 'admin-autocomplete',
            tokenSeparators: [','],
        });
    });
}(django.jQuery));
