$(document).ready(function () {

    function count_categories_checked() {

        $(".fr-accordion__btn span").html("");

        var categories_checked = {},
            category;
    
        $('#categories input:checkbox:checked').each(function(i, el) {
            category = $(el).data('theme');
            if (categories_checked.hasOwnProperty(category)) {
                categories_checked[category] += 1;
            }
            else {
                categories_checked[category] = 1;
            }
        });

        for(var key in categories_checked){
            if (categories_checked[key] > 0) {
                $(".fr-accordion__btn[data-theme='" + key + "'] span").html("(" + categories_checked[key] + ")");
            } else {
                $(".fr-accordion__btn[data-theme='" + key + "'] span").html("");
            }
        }
    }

    $("#categories .all-categories-btn").click(function(){
        var id_theme = $(this).data("theme");
        if ($(this).data("selected") == false) {
            $("input:checkbox[data-theme='" + id_theme + "']").prop('checked', true)
            $(this).data("selected", true);
            $(this).html("Désélectionner toutes les sous-thématiques");
            count_categories_checked()
        } else {
            $("input:checkbox[data-theme='" + id_theme + "']").prop('checked', false);
            $(this).data("selected", false);
            $(this).html("Sélectionner toutes les sous-thématiques");
            count_categories_checked()
        }
    });

    $("#categories input:checkbox").change(function() {
        count_categories_checked()
    })

});
