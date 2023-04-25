let tooltip = $('#tooltip');
tooltip.css({
    'display': "none",
    'top': 0,
    'left': 0,
});
$('body').append(tooltip);


let get_department_data = function(selected_path) {
    // Retrieves the data from the selected path and an array of objects
    // that was passed through JSON
    let department_code = selected_path.attr('data-num');
    let department_data = departments_data.find(d => d.code === department_code);
    if (department_data) {
        return department_data;
    } else {
        return {}
    }
};

$('#france-map .land').hover(function(e) {
    // Shows a description on hover
    let selected_path = $( this );
    let data = get_department_data(selected_path);

    let titleText = "";
    if ("code" in data) {
        titleText = `${data.name} : ${data.backers_count} porteurs`;
    } else {
        titleText = "Impossible de trouver les données pour ce département.";
    }

    tooltip.html(titleText);
    tooltip.css({
      'top': e.clientY + $(window).scrollTop(),
      'left': e.clientX,
      'display': 'block'
     });
    $('body').append(tooltip);
}, function() {
    // Hide description when the cursor exits the land
    tooltip.css({
      'display': 'none'
     });
});

$('#france-map .land').click(function() {
    // Goes to the selected department entry on click
    let selected_path = $( this );
    let data = get_department_data(selected_path);
    if ("code" in data) {
        let new_url = window.location.origin + "/cartographie/" + data.code + '-' + data.slug + '/';
        window.location = new_url; 
    }
});