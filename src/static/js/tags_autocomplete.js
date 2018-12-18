$(document).ready(function() {
    $('select#id_tags').select2({
        placeholder: catalog.tags_placeholder,
        minimumInputLength: 2,
        ajax: {
            url: '/api/tags/',
            dataType: 'json',
            delay: 100,
        },
        tags: true,
        theme: 'bootstrap4',
        width: '',
        tokenSeparators: [','],
    });
});
