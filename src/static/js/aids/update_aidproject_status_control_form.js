$(document).ready(function () {
	// Disallow user to checked "aid_denied" and "aid_obtained" checkboxes for a same aidproject object

	let dialogBoxesBtn = $('button[id^="aidproject-status-modal-btn-"]');

    dialogBoxesBtn.each(function(index) {
		$(this).on('click', function() {
			let aidproject_id = $(this).attr("id").split("aidproject-status-modal-btn-")[1]
			let aid_paid_checkbox = $("input[type='checkbox']#id_aid_paid--" + aidproject_id)
			let aid_obtained_checkbox = $("input[type='checkbox']#id_aid_obtained--" + aidproject_id)
			let aid_denied_checkbox = $("input[type='checkbox']#id_aid_denied--" + aidproject_id)
			let aid_requested_checkbox = $("input[type='checkbox']#id_aid_requested--" + aidproject_id)
			aid_requested_checkbox.change(function() {
				if (aid_requested_checkbox.is(":not(:checked)")) {
					aid_paid_checkbox.prop("checked", false);
					aid_obtained_checkbox.prop("checked", false);
					aid_denied_checkbox.prop("checked", false);
				}
			})
			aid_obtained_checkbox.change(function() {
				if (aid_obtained_checkbox.is(":checked")) {
					aid_requested_checkbox.prop("checked", true);
					aid_denied_checkbox.prop("checked", false);
				}
				if (aid_obtained_checkbox.is(":not(:checked)")) {
					aid_paid_checkbox.prop("checked", false);
					aid_requested_checkbox.prop("checked", false);
				}
			})
			aid_paid_checkbox.change(function() {
				if (aid_paid_checkbox.is(":checked")) {
					aid_denied_checkbox.prop("checked", false);
					aid_obtained_checkbox.prop("checked", true);
					aid_requested_checkbox.prop("checked", true);
				}
				if (aid_paid_checkbox.is(":not(:checked)")) {
					aid_obtained_checkbox.prop("checked", false);
					aid_requested_checkbox.prop("checked", false);
				}
			})
			aid_denied_checkbox.change(function() {
				if (aid_denied_checkbox.is(":checked")) {
					aid_requested_checkbox.prop("checked", true);
					aid_obtained_checkbox.prop("checked", false);
					aid_paid_checkbox.prop("checked", false);
				}
				if (aid_denied_checkbox.is(":not(:checked)")) {
					aid_requested_checkbox.prop("checked", false);
				}
			})
		})	
	})
});
