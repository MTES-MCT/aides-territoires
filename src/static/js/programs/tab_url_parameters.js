$(document).ready(function () {
    // update url parameter when user click on a program-tab
    
	let tabBtns = $('article#program button[id^="tabpanel-"]');
    
    tabBtns.each(function(index) {
		$(this).on('click', function() {
			let tabBtnId = $(this).attr("id").split("tabpanel-")[1]
            window.history.pushState({}, '', '?tab=' + tabBtnId);
        })
	})	
})
