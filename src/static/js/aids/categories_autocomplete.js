$(document).ready(function () {
  $("select#id_categories").select2({
    placeholder: "Saisissez quelques caractères pour des suggestions.",
    language: "fr",
    theme: "select2-dsfr",
    dropdownAutoWidth: true,
    width: "auto",
  }).on('select2:close', function (evt) {
    let uldiv = $(this).siblings('span.select2').find('ul')
    let count = $(this).select2('data').length
    if (count == 0) {
      uldiv.html("")
    }
    else {
      uldiv.html("<li>" + count + " sélectionnées</li>")
    }
  });
});
