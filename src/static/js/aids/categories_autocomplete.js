/**
 * Define features for the bookmark modal.
 */
(function (exports, catalog) {

    exports.updateAvailableCategories = function () {
        const themeNamesSelected = $('select#id_themes').select2('data').map(function(theme) { return theme.text.toLowerCase(); });
        const categoriesSelected = $('select#id_categories').select2('data');
        const categoryOptions = $('select#id_categories option');
        if (themeNamesSelected.length) {
            // enable categories in the theme section
            // disable categories not in the theme selection
            categoryOptions.each(function() {
                const categoryOption = $(this)[0].label.split(' > ')[0].toLowerCase();
                if (themeNamesSelected.indexOf(categoryOption) === -1) {
                    $(this).attr('disabled', 'disabled');
                } else {
                    $(this).removeAttr('disabled');
                }
            });
            // remove selected categories not belonging to selected themes
            const categoryNamesSelectedRemaining = categoriesSelected
                .filter(function(categorySelected) {
                    return themeNamesSelected.indexOf(categorySelected.text.split(' > ')[0].toLowerCase()) !== -1
                })
                .map(function(categoryRemaining) { return categoryRemaining.id });
            $('select#id_categories').val(categoryNamesSelectedRemaining).trigger('change');
            // set default placeholder
            if (!categoryNamesSelectedRemaining.length) {
                $('div#form-group-categories').find("input").attr("placeholder", catalog.autocomplete_placeholder);
            }
        } else {
            // disable all categories
            categoryOptions.each(function() {
                $(this).attr('disabled', 'disabled');
            });
            // remove all selected categories
            $('select#id_categories').val(null).trigger('change');
            // set custom placeholder
            $('div#form-group-categories').find("input").attr("placeholder", catalog.categories_blank_themes_placeholder);
        }
    };

})(this, catalog);


$(document).ready(function () {
    $('select#id_categories').select2({
        placeholder: catalog.autocomplete_placeholder,
        language: 'fr',
        theme: 'bootstrap4',
        width: '',
    });
    // init if themes filter
    if ($('select#id_themes')) {
        updateAvailableCategories();
        // track themes changes
        $(document).on('change', 'select#id_themes', function() {
            updateAvailableCategories();
        });
    }
});

