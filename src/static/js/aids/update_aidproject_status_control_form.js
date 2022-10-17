$(document).ready(function () {
	// Disallow user to checked "aid_denied" and "aid_obtained" checkboxes for a same aidproject object

	let dialogBoxesBtn = $('button[id^="aidproject-status-modal-btn-"]');

    dialogBoxesBtn.each(function(index) {
		$(this).on('click', function() {
			aidproject_id = $(this).attr("id").split("aidproject-status-modal-btn-")[1]
			let aid_obtained_checkbox = $("input[type='checkbox']#id_aid_obtained--" + aidproject_id)
			let aid_denied_checkbox = $("input[type='checkbox']#id_aid_denied--" + aidproject_id)
			aid_obtained_checkbox.change(function() {
				if (aid_obtained_checkbox.is(":checked")) {
					aid_denied_checkbox.prop("checked", false);
				}
			})
			aid_denied_checkbox.change(function() {
				if (aid_denied_checkbox.is(":checked")) {
					aid_obtained_checkbox.prop("checked", false);
				}
			})
		})	
	})
});
