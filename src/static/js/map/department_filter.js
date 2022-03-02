department_filter = function (return_page) {

  /* go to the map for the selected department */
  $( "#select-department" ).change(function() {
      window.location = window.location.origin + "/cartographie/" + $( this ).val() + return_page;
  });

  /* use the org filter */
  $( "#select-organization" ).change(function() {
      let page_url = window.location.href.split('?')[0];
      let audience = $( this ).val();
      if (audience) {
          window.location = page_url + "?target_audience=" + $( this ).val();
      } else {
          window.location = page_url;
      }
  });

  /* use the aid_type filter */
  $( "#select-aid-type" ).change(function() {
    let page_url = window.location.href.split('?')[0];
    let audience = $( this ).val();
    if (audience) {
        window.location = page_url + "?aid_type=" + $( this ).val();
    } else {
        window.location = page_url;
    }
});
}
