(function (exports) {
    'use strict';

    exports.sendAidMatchingProjectData = function(match_result) {
            var statsData = JSON.stringify({
                aid: AID_ID,
                project: PROJECT_ID,
                is_matching: match_result,
                querystring: CURRENT_SEARCH
            });

            $.ajax({
                type: 'POST',
                url: `/api/stats/aid-match-project-events/`,
                contentType: 'application/json',
                headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
                dataType: 'json',
                data: statsData
            })
        }

})(this);

$(document).ready(function () {
    $("#no_match_project_btn").on('click', function() {
        sendAidMatchingProjectData(false);
    });
    $("#match_project_btn").on('click', function() {
        sendAidMatchingProjectData(true);
    });
});
