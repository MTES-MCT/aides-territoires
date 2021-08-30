$(document).ready(function () {

    $("#select_path").on("change", function(){
        $('#create_project').attr('action', this.options[this.selectedIndex].value)
        $('#id_aids_associated option[value="' + AID_ID + '"]').prop('selected', true);
    })
    return false

})
