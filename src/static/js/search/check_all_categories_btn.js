$(document).ready(function () {

    $(".CheckAll").click(function(){
        var id_theme = $(this).data("theme");
        if ($(this).data("selected") == false) {
            $("input:checkbox[data-theme='" + id_theme + "']").prop('checked', true)
            $(this).data("selected", true);
            $(this).html("Désélectionner toutes les sous-thématiques");
        } else {
            $("input:checkbox[data-theme='" + id_theme + "']").prop('checked', false);
            $(this).data("selected", false);
            $(this).html("Sélectionner toutes les sous-thématiques");
        }

    });
});
