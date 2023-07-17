$(document).ready(function () {
	// Disallow user to checked "direct" and "indirect" support_type checkboxes

	$(this).on('click', function() {
		let support_type_direct_checkbox = $("input[type='checkbox']#id_support_type_0")
		let support_type_indirect_checkbox = $("input[type='checkbox']#id_support_type_1")
		
		support_type_direct_checkbox.change(function() {
			if (support_type_direct_checkbox.is(":checked")) {
				support_type_indirect_checkbox.prop("checked", false);
			}
		})

		support_type_indirect_checkbox.change(function() {
			if (support_type_indirect_checkbox.is(":checked")) {
				support_type_direct_checkbox.prop("checked", false);
			}
		})
	})	
})
