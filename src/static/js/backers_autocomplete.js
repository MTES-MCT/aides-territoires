$(document).ready(function() {
    $('select#id_financers').select2({
        placeholder: catalog.backers_placeholder,
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
        },
        theme: 'bootstrap4',
        width: '',
    });
});
