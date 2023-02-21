import pytest

from django.urls import reverse
from keywords.models import SynonymList

from programs.factories import ProgramFactory
from keywords.factories import SynonymListFactory
from aids.factories import AidFactory

pytestmark = pytest.mark.django_db


def test_only_aids_from_program_selected_are_displayed_in_detail_page(client):
    program_selected = ProgramFactory()
    program_selected.name = "Fonds vert"
    program_selected.save()

    other_program = ProgramFactory()
    other_program.name = "Petites villes de demain"
    other_program.save()

    first_aid = AidFactory()
    first_aid.programs.add(program_selected)
    second_aid = AidFactory()
    second_aid.programs.add(program_selected)
    third_aid = AidFactory()
    third_aid.programs.add(other_program)

    program_detail_url = reverse("program_detail", args=[program_selected.slug])
    res = client.get(program_detail_url)
    assert "2 aides liées au programme" in res.content.decode()
    assert first_aid.name in res.content.decode()
    assert second_aid.name in res.content.decode()
    assert third_aid.name not in res.content.decode()


def test_user_can_filter_aids_displayed_in_program_detail_page(client, perimeters):
    program_selected = ProgramFactory()
    program_selected.name = "Fonds vert"
    program_selected.save()

    first_aid = AidFactory(perimeter=perimeters["normandie"])
    first_aid.programs.add(program_selected)
    first_aid.save()
    second_aid = AidFactory(
        name="Créer une statue à Champignac-en-Cambrousse",
        perimeter=perimeters["montpellier"],
    )
    second_aid.programs.add(program_selected)
    second_aid.save()
    third_aid = AidFactory(
        name="Aide non-pertinente",
        description="Description",
        eligibility="Eligibility",
        perimeter=perimeters["montpellier"],
    )
    third_aid.programs.add(program_selected)
    third_aid.save()

    SynonymListFactory(
        name="spirou",
        keywords_list="Champignac-en-Cambrousse",
    )

    program_detail_url = reverse("program_detail", args=[program_selected.slug])

    res = client.get(program_detail_url)
    assert res.status_code == 200
    assert "3 aides liées au programme" in res.content.decode()
    assert first_aid.name in res.content.decode()
    assert second_aid.name in res.content.decode()
    assert third_aid.name in res.content.decode()

    res = client.get(program_detail_url, data={"perimeter": perimeters["normandie"].pk})
    assert res.status_code == 200
    assert "1 aide liée au programme" in res.content.decode()
    assert first_aid.name in res.content.decode()
    assert second_aid.name not in res.content.decode()
    assert third_aid.name not in res.content.decode()

    res = client.get(
        program_detail_url,
        data={"perimeter": perimeters["montpellier"].pk, "text": "1-synonyms-spirou"},
    )
    assert res.status_code == 200
    print(res.content.decode())
    print(SynonymList.objects.all().values("name", "id", "slug"))
    print(second_aid.__dict__)
    print(third_aid.__dict__)
    assert "1 aide liée au programme" in res.content.decode()
    assert first_aid.name not in res.content.decode()
    assert second_aid.name in res.content.decode()
    assert third_aid.name not in res.content.decode()
