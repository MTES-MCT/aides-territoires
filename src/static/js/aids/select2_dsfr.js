// Fix the autocomplete forms for the dsfr
$(document).ready(function () {
  $(".select2-container").addClass("fr-select-group");
  $(".select2-selection--multiple").addClass("fr-select");
  $(".select2-selection--single").addClass("fr-select");
});

// Fix the bug on select2 not able to focus correctly with jQuery 3.6
$(document).on('select2:open', function (e) {
  let searchField = document.querySelector(`[aria-controls="select2-${e.target.id}-results"]`);
  if (searchField) {
    searchField.focus()
  }
});