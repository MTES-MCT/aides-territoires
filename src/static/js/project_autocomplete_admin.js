django.jQuery(document).ready(function () {

    django.jQuery('select#id_projects').select2({
        language: 'fr',
        minimumInputLength: 3,
        ajax: {
            url: '/api/projects/',
            dataType: 'json',
            delay: 100,
            data: function (params) {
                var query = {
                  q: params.term,
                  is_published: true,
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
        width: '80%',
    });
});