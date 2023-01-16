import pytest
import tablib

from programs.factories import ProgramFactory
from pages.models import FaqCategory, FaqQuestionAnswer
from pages.resources import FaqQuestionAnswerResource

pytestmark = pytest.mark.django_db


def test_can_import_faq_question_answer_with_unexistent_faq_category(client):

    resource = FaqQuestionAnswerResource()

    ProgramFactory(name="Fonds vert")
    faq_question_answer = FaqQuestionAnswer.objects.all()
    faq_category = FaqCategory.objects.all()

    assert faq_question_answer.count() == 0
    assert faq_category.count() == 0

    dataset = tablib.Dataset(headers=["faq_category", "question", "answer", "program"])
    row = [
        "Principes généraux",
        "La grande question sur la vie, l'univers et le reste",
        "42",
        "Fonds vert",
    ]
    dataset.append(row)

    resource.import_data(dataset, raise_errors=True)

    assert faq_question_answer.count() == 1
    assert faq_category.count() == 1

    new_faq_question_answer_object = FaqQuestionAnswer.objects.first()

    assert (
        new_faq_question_answer_object.question
        == "La grande question sur la vie, l'univers et le reste"
    )
    assert new_faq_question_answer_object.answer == "42"
    assert new_faq_question_answer_object.program.name == "Fonds vert"
    assert new_faq_question_answer_object.faq_category.name == "Principes généraux"
