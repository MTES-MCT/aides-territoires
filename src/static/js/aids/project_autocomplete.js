$(document).ready(function () {

    $('select#id_projects').select2({
        placeholder: catalog.project_placeholder,
        language: 'fr',
        minimumInputLength: 3,
        language: {
            inputTooShort: function() {
                // If the user enter a value in the autocomplete field input but
                // doesn't select an option we want to use the value to fill
                // the #id_text input and pursue the research with the text filter. 
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

    // If user select a project in the list we erase the value of #id_text input
    // to search with the project filter instead of the text filter 
    $('select#id_projects').on('select2:selecting', function() {
        $('input#id_text').val('');
    })
});
