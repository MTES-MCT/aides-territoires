$(document).ready(function () {
    // Disable submit button until at least one enabled checkbox was checked
    let submitBtn = $('form#suggest-aid-modal-form button[type=submit]');
    let checkboxesEnabled = $("#form-group-favorite-projects input[type='checkbox']:not(:disabled)");

    submitBtn.prop('disabled', true);
    checkboxesEnabled.each(function(index) {
    	$(this).on('click', function() {
			if($(".fr-form-group input[type='checkbox']:checked:not(:disabled)").length) {
    			submitBtn.prop('disabled', false);
			} else {
    			submitBtn.prop('disabled', true);
			}
		})
    });
});
