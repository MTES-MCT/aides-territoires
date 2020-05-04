$(document).ready(function () {

    $('select#id_backers').select2({
        placeholder: catalog.financers_placeholder,
        language: 'fr',
        minimumInputLength: 3,
        language: {
            inputTooShort: function() { return catalog.autocomplete_placeholder; },
        },
        ajax: {
            url: '/api/backers/',
            dataType: 'json',
            delay: 100,
            data: function (params) {
                var query = {
                  q: params.term,
                  page: params.page || 1
                }
                return query;
              },
              processResults: function (data, params) {
                  params.page = params.page || 1;

                  return {
                      results: data.results,
                      pagination: {
                          more: data.next != null
                      }
                  };
              }
        },
        theme: 'bootstrap4',
        width: '',
    });
});
