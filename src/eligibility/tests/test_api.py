import json
import pytest
from django.urls import reverse

from eligibility.factories import EligibilityTestFactory, EligibilityQuestionFactory


pytestmark = pytest.mark.django_db


# def test_api_list_does_not_exist(client):
#     res = client.get(reverse('eligibility-list'))
#     assert res.status_code == 404


def test_api(client):
    eligibility_test_1 = EligibilityTestFactory(name="Test 1")
    eligibility_test_2 = EligibilityTestFactory(name="Test 2")
    eligibility_question_1 = EligibilityQuestionFactory(text="Question 1")
    eligibility_question_2 = EligibilityQuestionFactory(text="Question 2")
    eligibility_test_2.questions.add(
        eligibility_question_1, through_defaults={"order": 2}
    )
    eligibility_test_2.questions.add(
        eligibility_question_2, through_defaults={"order": 1}
    )

    res = client.get(reverse("eligibility-detail", args=[eligibility_test_1.id]))
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["name"] == eligibility_test_1.name
    assert len(content["questions"]) == 0

    res = client.get(reverse("eligibility-detail", args=[eligibility_test_2.id]))
    assert res.status_code == 200
    content = json.loads(res.content.decode())
    assert content["name"] == eligibility_test_2.name
    assert len(content["questions"]) == 2
    # questions should be sorted by order
    assert content["questions"][0]["id"] == eligibility_question_2.id
    assert content["questions"][0]["order"] == 1
