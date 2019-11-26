$(document).ready(function() {
    $('select#id_financers').select2({
        placeholder: catalog.financers_placeholder,
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
        },
        theme: 'bootstrap4',
        width: '',
    });
    $('select#id_instructors').select2({
        placeholder: catalog.instructors_placeholder,
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
        },
        theme: 'bootstrap4',
        width: '',
    });
});
