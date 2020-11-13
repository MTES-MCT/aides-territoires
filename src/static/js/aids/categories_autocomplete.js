$(document).ready(function () {
    $('select#id_categories').select2({
        placeholder: catalog.autocomplete_placeholder,
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
    });
    updateAvailableCategories();
    $(document).on('change', 'select#id_themes', function() {
        updateAvailableCategories();
    });
});

function updateAvailableCategories() {
    const themesSelected = $('select#id_themes').select2('data').map(function(theme) { return theme.text.toLowerCase() });
    const categoryOptions = $('select#id_categories option');
    if (themesSelected.length) {
        categoryOptions.each(function() {
            const categoryTheme = $(this)[0].label.split(' > ')[0].toLowerCase();
            // disable categories not in the theme selection
            if (themesSelected.indexOf(categoryTheme) === -1) {
                console.log($(this))
                $(this).attr('disabled', 'disabled');
            } else {
                $(this).removeAttr('disabled');
            }
        });
    }
};
