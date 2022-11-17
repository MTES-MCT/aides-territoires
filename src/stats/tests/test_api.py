import pytest
import json

from django.urls import reverse

from stats.models import AidContactClickEvent, AidEligibilityTestEvent
from aids.factories import AidFactory
from eligibility.factories import EligibilityTestFactory, EligibilityQuestionFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def contact_api_url():
    return reverse("aid-contact-click-events-list")


@pytest.fixture
def project_api_url():
    return reverse("aid-match-project-events-list")


@pytest.fixture
def eligibility_api_url():
    return reverse("aid-eligibility-test-events-list")


def test_aid_contact_click_events_api(client, contact_api_url):
    aid = AidFactory()
    assert AidContactClickEvent.objects.count() == 0

    # querystring should be passed
    data = {
        "aid": aid.id,
        # 'querystring': ''
    }
    client.post(contact_api_url, data=data)
    assert AidContactClickEvent.objects.count() == 0

    # querystring can be empty
    data = {"aid": aid.id, "querystring": ""}
    client.post(contact_api_url, data=data)
    assert AidContactClickEvent.objects.count() == 1

    # querystring will be cleaned
    data = {"aid": aid.id, "querystring": "perimeter=&aid_type=financial"}
    client.post(contact_api_url, data=data)
    assert AidContactClickEvent.objects.count() == 2
    event = AidContactClickEvent.objects.last()
    assert event.querystring == "aid_type=financial"


def test_aid_eligibility_test_events_api(client, eligibility_api_url):
    aid = AidFactory()
    eligibility_test = EligibilityTestFactory(name="Test")
    eligibility_question_1 = EligibilityQuestionFactory(text="Question 1")
    eligibility_question_2 = EligibilityQuestionFactory(text="Question 2")
    eligibility_test.questions.add(
        eligibility_question_1, through_defaults={"order": 1}
    )
    eligibility_test.questions.add(
        eligibility_question_2, through_defaults={"order": 2}
    )
    assert AidEligibilityTestEvent.objects.count() == 0

    # querystring should be passed
    data = {
        "aid": aid.id,
        "eligibility_test": eligibility_test.id,
        # 'querystring': ''
    }
    client.post(eligibility_api_url, data=data)
    assert AidEligibilityTestEvent.objects.count() == 0

    # answer_success will default to False if not passed
    data = {
        "aid": aid.id,
        "eligibility_test": eligibility_test.id,
        "querystring": "text=coucou",
    }
    client.post(eligibility_api_url, data=data)
    assert AidEligibilityTestEvent.objects.count() == 1
    event = AidEligibilityTestEvent.objects.last()
    assert event.answer_success is False
    assert not event.answer_details

    # answer_details stores a JSON
    data = {
        "aid": aid.id,
        "eligibility_test": eligibility_test.id,
        "answer_success": True,  # 'true' also works
        "querystring": "text=coucou",
        "answer_details": json.dumps(
            [
                {
                    "id": eligibility_question_1.id,
                    "text": eligibility_question_1.text,
                    "answer": "une réponse",
                    "answer_correct": eligibility_question_1.answer_correct,
                },
                {
                    "id": eligibility_question_2.id,
                    "text": eligibility_question_2.text,
                    "answer": "une autre réponse",
                    "answer_correct": eligibility_question_2.answer_correct,
                },
            ]
        ),
    }
    client.post(eligibility_api_url, data=data)
    assert AidEligibilityTestEvent.objects.count() == 2
    event = AidEligibilityTestEvent.objects.last()
    assert event.answer_success is True
    assert len(event.answer_details) == 2
    assert event.answer_details[0]["id"] == eligibility_question_1.id

    # querystring can be empty
    data = {
        "aid": aid.id,
        "eligibility_test": eligibility_test.id,
        "answer_success": True,
        "querystring": "",
    }
    client.post(eligibility_api_url, data=data)
    assert AidEligibilityTestEvent.objects.count() == 3
    event = AidEligibilityTestEvent.objects.last()
    assert event.answer_success is True

    # querystring will be cleaned
    data = {
        "aid": aid.id,
        "eligibility_test": eligibility_test.id,
        "answer_success": True,
        "querystring": "perimeter=&aid_type=financial",
    }
    client.post(eligibility_api_url, data=data)
    assert AidEligibilityTestEvent.objects.count() == 4
    event = AidEligibilityTestEvent.objects.last()
    assert event.querystring == "aid_type=financial"
