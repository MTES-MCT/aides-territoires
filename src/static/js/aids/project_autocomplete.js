$(document).ready(function () {

    $('select#id_projects').select2({
        placeholder: catalog.project_placeholder,
        language: 'fr',
        minimumInputLength: 3,
        language: {
            inputTooShort: function() {
                $('.select2-search__field').on('input', function() {
                    $('input#id_text').val($('.select2-search__field').val());
                }) 
                return catalog.autocomplete_placeholder; 
            },
        },
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

                  if (data.results.length === 0) {
                    $("#other_project_box").removeClass("d-none");
                  } 
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
