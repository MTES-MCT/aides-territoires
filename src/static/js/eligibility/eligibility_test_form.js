/**
 * Handles the aid alert creation form.
 */
(function (exports, catalog) {
    'use strict';

    const SUBMIT_BUTTON_TEXT = 'Vérifier mon éligibilité';
    const SUCCESS_MESSAGE = '✔️ Vous êtes éligible !';
    const FAILURE_MESSAGE = 'Vous n\'êtes malheureusement pas éligible.';

    var eligibilityTestIntroduction = $('div#eligibility-test-introduction');
    var eligibilityTestForm = $('form#eligibility-test-form');
    var eligibilityTestResults = $('div#eligibility-test-results');
    var eligibilityTestResultMessage = $('p#eligibility-test-result-message');
    var eligibilityTestConclusion = $('div#eligibility-test-conclusion');

    var submitButton = $('<button>', { type: 'submit', text: SUBMIT_BUTTON_TEXT });

    var ANSWER_CHOICES = ['a', 'b', 'c', 'd'];

    /**
     * API call to fetch the eligibility test details & questions
     */
    exports.fetchEligibilityTestData = function (event) {
        $.ajax({
            type: 'GET',
            url: `/api/eligibility/${AID_ELIGIBILITY_TEST_ID}/`,
            beforeSend: function () {
                $('#spinner').removeClass("d-none");
            },
            success: function(data) {
                $('#spinner').addClass("d-none");
                // form-group for each question
                buildEligibilityTestForm(data);
            },
        })
    }

    /**
     * Use jquery to build the eligibility test form
     */
    exports.buildEligibilityTestForm = function (eligibilityTestJson) {
        // update the test introduction & conclusion
        eligibilityTestIntroduction.html(eligibilityTestJson.introduction); // .attr('class', 'info')
        // build the test form
        eligibilityTestJson.questions.forEach((question, index) => {
            var questionTitle = $(`<h6><span class="badge badge-primary">${index + 1}</span>&nbsp;&nbsp;${question.text}</h6>`);
            var questionFormGroup = $('<div>', { class: 'form-group fr-form-group required' });
            // inline radio for each question's answer_choice
            ANSWER_CHOICES.forEach((answerChoice, answerIndex) => {
                var answerChoiceKey = `answer_choice_${answerChoice}`;
                if (question[answerChoiceKey]) {
                    var formCheck = $('<div>', { class: 'form-check fr-radio-group' });
                    var formCheckLabel = $('<label>', { class: 'form-check-label fr-label', for: `answer-${question.id}-${answerIndex + 1}`, text: question[answerChoiceKey] });
                    formCheck.append($('<input>', { class: 'form-check-input', type: 'radio', id: `answer-${question.id}-${answerIndex + 1}`, name: question.id, value: answerChoice, required: true }));
                    formCheck.append(formCheckLabel);
                    questionFormGroup.append(formCheck);
                }
            })
            eligibilityTestForm.append(questionTitle);
            eligibilityTestForm.append(questionFormGroup);
        })
        // add the submit button
        eligibilityTestForm.append(submitButton);
        submitButton.addClass("fr-btn fr-my-5w");
        eligibilityTestForm.off('submit').on('submit', { eligibilityTestJson: eligibilityTestJson }, showEligibilityTestResults);
    }
    
    /**
     * Check if the test is successful or not.
     * Display the corresponding message.
     */
    exports.showEligibilityTestResults = function (event) {
        // avoid page refresh
        event.preventDefault();
        // get form data
        var formData = eligibilityTestForm.serializeArray();
        // now we can disable the form
        eligibilityTestForm.find('input').prop("disabled", true);
        submitButton.remove();
        // prepare the results & stats
        var results = true;
        var statsData = [];
        eligibilityTestResults.show();
        
        formData.forEach((answer, index) => {
            // answer = { name: '<question id>', value: '<answer choice letter>' }
            var questionId = parseInt(answer.name);
            var question = event.data.eligibilityTestJson.questions.find(q => q.id === questionId);
            var answerSuccess = question.answer_correct === answer.value;
            // update results if answerSuccess is false
            results = !answerSuccess ?  answerSuccess : results;
            // build stats answer object
            statsData.push({
                'id': question.id,
                'text': question.text,
                'answer': question[`answer_choice_${answer.value}`],
                'answer_correct': question.answer_correct
            })
        });

        // send results
        sendEligibilityTestData(statsData, results);

        // show results
        if (results) {
            eligibilityTestResultMessage.attr('class', 'success').text(SUCCESS_MESSAGE);
            eligibilityTestConclusion.html(event.data.eligibilityTestJson.conclusion_success); // .attr('class', 'info')
        } else {
            eligibilityTestResultMessage.attr('class', 'warning').text(FAILURE_MESSAGE);
            eligibilityTestConclusion.html(event.data.eligibilityTestJson.conclusion_failure); // .attr('class', 'info')
        }
        eligibilityTestConclusion.append(event.data.eligibilityTestJson.conclusion);
    }

    exports.sendEligibilityTestData = function(statsData, results) {
        var statsData = JSON.stringify({
            aid: AID_ID,
            eligibility_test: AID_ELIGIBILITY_TEST_ID,
            answer_success: results,
            answer_details: statsData,
            querystring: CURRENT_SEARCH
        });

        $.ajax({
            type: 'POST',
            url: `/api/stats/aid-eligibility-test-events/`,
            contentType: 'application/json',
            headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value },
            dataType: 'json',
            data: statsData
        })
    }

    exports.resetEligibilityTest = function (event) {
        eligibilityTestForm.empty();
        eligibilityTestResults.hide();

        if (event.data && event.data.eligibilityTestJson) {
            buildEligibilityTestForm(event.data.eligibilityTestJson);
        } else {
            fetchEligibilityTestData();
        }
    }

})(this, catalog);

$(document).ready(function () {
    $('#aid-eligibility-test-modal-btn').on('click', resetEligibilityTest);
});
