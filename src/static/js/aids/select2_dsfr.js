// This file uses the `jQuery` prefix instead of `$`
// so that it also works in the Django Admin

// Fix the autocomplete forms for the dsfr
jQuery(document).ready(function () {
  jQuery(".select2-container").addClass("fr-select-group");
  jQuery(".select2-selection--multiple").addClass("fr-select");
  jQuery(".select2-selection--single").addClass("fr-select");
});

// Fix the bug on select2 not able to focus correctly with jQuery 3.6
jQuery(document).on('select2:open', function (e) {
  let searchField = document.querySelector(`[aria-controls="select2-${e.target.id}-results"]`);
  if (searchField) {
    searchField.focus()
  }
});