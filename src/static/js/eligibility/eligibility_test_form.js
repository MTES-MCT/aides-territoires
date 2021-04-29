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
            var questionFormGroup = $('<div>', { class: 'form-group required' });
            // inline radio for each question's answer_choice
            ANSWER_CHOICES.forEach((answerChoice, answerIndex) => {
                var answerChoiceKey = `answer_choice_${answerChoice}`;
                if (question[answerChoiceKey]) {
                    var formCheck = $('<div>', { class: 'form-check' });
                    var formCheckLabel = $('<label>', { class: 'form-check-label', for: `answer-${question.id}-${answerIndex + 1}`, text: question[answerChoiceKey] });
                    formCheckLabel.prepend($('<input>', { class: 'form-check-input', type: 'radio', id: `answer-${question.id}-${answerIndex + 1}`, name: question.id, value: answerChoice, required: true }));
                    formCheck.append(formCheckLabel);
                    questionFormGroup.append(formCheck);
                }
            })
            eligibilityTestForm.append(questionTitle);
            eligibilityTestForm.append(questionFormGroup);
        })
        // add the submit button
        eligibilityTestForm.append(submitButton);
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
        // prepare the results
        var results = true;
        eligibilityTestResults.show();
        
        formData.forEach(answer => {
            // get questionId from the answer 'name' key
            var questionId = parseInt(answer.name);
            // check if the answer is correct
            var answerSuccess = event.data.eligibilityTestJson.questions.find(q => q.id === questionId).answer_correct === answer.value;
            // update results if answerSuccess is false
            results = !answerSuccess ? answerSuccess : results;
        });
    
        // show result message & conclusion
        if (results) {
            eligibilityTestResultMessage.attr('class', 'success').text(SUCCESS_MESSAGE);
            eligibilityTestConclusion.html(event.data.eligibilityTestJson.conclusion_success); // .attr('class', 'info')
        } else {
            eligibilityTestResultMessage.attr('class', 'warning').text(FAILURE_MESSAGE);
            eligibilityTestConclusion.html(event.data.eligibilityTestJson.conclusion_failure); // .attr('class', 'info')
        }
        eligibilityTestConclusion.append(event.data.eligibilityTestJson.conclusion);
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
    $('div#aid-eligibility-test-modal').on('show.bs.modal', resetEligibilityTest);
});
