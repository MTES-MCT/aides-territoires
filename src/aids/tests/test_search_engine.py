"""Test methods for the search engine view."""

import pytest
from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone

from aids.factories import AidFactory
from programs.factories import ProgramFactory
from keywords.factories import SynonymListFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def aids(perimeters):
    aids = [
        AidFactory(perimeter=perimeters["europe"]),
        *AidFactory.create_batch(2, perimeter=perimeters["france"]),
        *AidFactory.create_batch(3, perimeter=perimeters["occitanie"]),
        *AidFactory.create_batch(4, perimeter=perimeters["herault"]),
        *AidFactory.create_batch(5, perimeter=perimeters["montpellier"]),
        *AidFactory.create_batch(6, perimeter=perimeters["vic"]),
        *AidFactory.create_batch(7, perimeter=perimeters["aveyron"]),
        *AidFactory.create_batch(8, perimeter=perimeters["rodez"]),
        *AidFactory.create_batch(9, perimeter=perimeters["normandie"]),
        *AidFactory.create_batch(10, perimeter=perimeters["eure"]),
        *AidFactory.create_batch(11, perimeter=perimeters["st-cyr"]),
        *AidFactory.create_batch(12, perimeter=perimeters["adour-garonne"]),
        *AidFactory.create_batch(13, perimeter=perimeters["rhone-mediterannee"]),
        *AidFactory.create_batch(14, perimeter=perimeters["fort-de-france"]),
        *AidFactory.create_batch(15, perimeter=perimeters["outre-mer"]),
    ]
    return aids


def test_search_engine_view(client):
    """Test that the url is publicly accessible."""

    url = reverse("search_view")
    res = client.get(url)
    assert res.status_code == 200


def test_only_published_aids_are_listed(client):
    """Test that unpublished aids are not shown."""

    AidFactory.create_batch(3)
    url = reverse("search_view")
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 3

    # Let's create some non published aids, to check that the list
    # of objects passed to the context does not change
    AidFactory.create_batch(5, status="draft")
    AidFactory.create_batch(7, status="reviewable")
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 3

    # Let's add some more published aids, to check that the limit does not
    # come from pagination parameters
    AidFactory.create_batch(11)
    url = reverse("search_view")
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 14


def test_deleted_aids_are_not_listed(client):
    """Deleted aids must be excluded from all queries by default."""

    AidFactory(status="deleted")
    url = reverse("search_view")
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 0


def test_generic_aid_is_listed(client, perimeters):
    generic = AidFactory(perimeter=perimeters["france"], is_generic=True)
    AidFactory(generic_aid=generic, perimeter=perimeters["occitanie"])
    url = reverse("search_view")
    res = client.get(url)
    assert res.status_code == 200
    assert generic in res.context["aids"]


def test_generic_aid_is_not_listed_if_local_aid_is_expired(client, perimeters):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    generic = AidFactory(perimeter=perimeters["france"], is_generic=True)
    local = AidFactory(
        generic_aid=generic,
        perimeter=perimeters["occitanie"],
        submission_deadline=yesterday,
    )
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["occitanie"].pk})
    assert res.status_code == 200
    assert generic not in res.context["aids"]
    assert local not in res.context["aids"]

    res = client.get(url)
    assert res.status_code == 200
    assert generic in res.context["aids"]
    assert local not in res.context["aids"]


def test_local_aid_is_listed(client, perimeters):
    generic = AidFactory(perimeter=perimeters["france"], is_generic=True)
    local = AidFactory(generic_aid=generic, perimeter=perimeters["occitanie"])
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["occitanie"].pk})
    assert res.status_code == 200
    assert local in res.context["aids"]


def test_standard_aid_is_listed(client, perimeters):
    standard = AidFactory(perimeter=perimeters["occitanie"])
    url = reverse("search_view")
    res = client.get(url)
    assert res.status_code == 200
    assert standard in res.context["aids"]


def test_get_generic_search_perimeter_is_wider(client, perimeters):
    generic = AidFactory(perimeter=perimeters["france"], is_generic=True)
    local = AidFactory(generic_aid=generic, perimeter=perimeters["occitanie"])
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["europe"].pk})
    assert res.status_code == 200
    # Searching on a wider perimeter: europe is wider than occitanie.
    # We expect to see the generic aid, not it's local version.
    assert generic in res.context["aids"]
    assert local not in res.context["aids"]


def test_has_generic_if_search_perimeter_matches(client, perimeters):
    generic = AidFactory(perimeter=perimeters["france"], is_generic=True)
    local = AidFactory(generic_aid=generic, perimeter=perimeters["occitanie"])
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["france"].pk})
    assert res.status_code == 200
    # Searching on matching perimeter: france.
    # We expect to see the generic aid, not it's local version.
    assert generic in res.context["aids"]
    assert local not in res.context["aids"]


def test_get_local_if_search_perimeter_is_smaller(client, perimeters):
    generic = AidFactory(perimeter=perimeters["france"], is_generic=True)
    local = AidFactory(generic_aid=generic, perimeter=perimeters["occitanie"])
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["herault"].pk})
    assert res.status_code == 200
    # Searching on a small perimeter: herault is smaller than occitanie.
    # We expect to see the local aid, not it's generic version.
    assert generic not in res.context["aids"]
    assert local in res.context["aids"]


def test_get_local_aid_if_search_perimeter_matches(client, perimeters):
    generic = AidFactory(perimeter=perimeters["france"], is_generic=True)
    local = AidFactory(generic_aid=generic, perimeter=perimeters["occitanie"])
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["occitanie"].pk})
    assert res.status_code == 200
    # Searching on a matching perimeter: occitanie.
    # We expect to see the local aid, not it's generic version.
    assert generic not in res.context["aids"]
    assert local in res.context["aids"]


def test_expired_aids_are_not_listed(client):

    url = reverse("search_view")

    AidFactory.create_batch(2)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 2

    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    AidFactory.create_batch(3, submission_deadline=tomorrow)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 5

    AidFactory.create_batch(5, submission_deadline=today)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 10

    AidFactory.create_batch(7, submission_deadline=yesterday)
    res = client.get(url)
    assert res.status_code == 200
    assert len(res.context["aids"]) == 10


def test_search_european_aids(client, perimeters, aids):
    """Display ALL the aids."""
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["europe"].pk})
    assert res.context["paginator"].count == 120


def test_search_french_aids(client, perimeters, aids):
    """Display ALL the aids again."""
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["france"].pk})
    assert res.context["paginator"].count == 120


def test_search_aids_form_occitanie(client, perimeters, aids):
    """Only display aids in Occitanie and above."""
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["occitanie"].pk})
    assert res.context["paginator"].count == 36


def test_search_aids_from_herault(client, perimeters, aids):
    """Only display aids in Hérault and above."""
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["herault"].pk})
    assert res.context["paginator"].count == 21


def test_search_aids_from_montpellier(client, perimeters, aids):
    """Only display aids in Hérault and above."""
    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["montpellier"].pk})
    assert res.context["paginator"].count == 28


def test_search_aids_from_rhone_mediterannee_basin(client, perimeters, aids):
    """Only display aids in the selected basin."""

    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["rhone-mediterannee"].pk})
    assert res.context["paginator"].count == 27


def test_search_aids_from_adour_garonne_basin(client, perimeters, aids):
    """Only display aids in the selected basin."""

    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["adour-garonne"].pk})
    assert res.context["paginator"].count == 23


def test_search_overseas_aids(client, perimeters, aids):
    """Only display overseas aids."""

    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["outre-mer"].pk})
    assert res.context["paginator"].count == 32


def test_search_mainland_aids(client, perimeters, aids):
    """Only display mainland aids."""

    url = reverse("search_view")
    res = client.get(url, data={"perimeter": perimeters["métropole"].pk})
    assert res.context["paginator"].count == 91


def test_full_text_search(client, perimeters):
    """Full text search return valid results."""

    AidFactory(perimeter=perimeters["europe"], name="Mon Aide à Tester sur l'écologie")
    url = reverse("search_view")

    # Words are correctly stemmed and lexemed
    res = client.get(url, data={"text": "aide"})
    assert res.context["paginator"].count == 1

    # Plurals are taken into account
    res = client.get(url, data={"text": "aides"})
    assert res.context["paginator"].count == 1

    # Verbs are too
    res = client.get(url, data={"text": "test"})
    assert res.context["paginator"].count == 1

    # Accents are not taken into account
    res = client.get(url, data={"text": "écologie"})
    assert res.context["paginator"].count == 1

    # Irrelevant results are not returned
    res = client.get(url, data={"text": "gloubiboulga"})
    assert res.context["paginator"].count == 0


def test_full_text_results_ordering(client, perimeters):
    """Title terms have more weight."""

    europe = perimeters["europe"]
    AidFactory(perimeter=europe, name="Pomme", description="Poire")
    AidFactory(perimeter=europe, name="Poire", description="Pomme")
    url = reverse("search_view")

    res = client.get(url, data={"text": "pomme"})
    assert res.context["paginator"].count == 2
    assert res.context["aids"][0].name == "Pomme"
    assert res.context["aids"][1].name == "Poire"

    res = client.get(url, data={"text": "poire"})
    assert res.context["paginator"].count == 2
    assert res.context["aids"][0].name == "Poire"
    assert res.context["aids"][1].name == "Pomme"


def test_full_text_advanced_syntax(client, perimeters):
    AidFactory(
        perimeter=perimeters["europe"],
        name="Dépollution des rejets urbains par temps de pluie",
    )
    url = reverse("search_view")

    # Searching with several terms find the document
    res = client.get(url, data={"text": "dépollution temps pluie"})
    assert res.context["paginator"].count == 1

    # Search terms use OR when a comma is present
    res = client.get(url, data={"text": "dépollution temps, soleil"})
    assert res.context["paginator"].count == 1

    res = client.get(url, data={"text": "soleil, dépollution temps"})
    assert res.context["paginator"].count == 1


def test_synonym_search(client, perimeters):
    AidFactory(
        perimeter=perimeters["france"],
        name="Aménager une piste cyclable le long des saules",
    )
    AidFactory(perimeter=perimeters["france"], name="Acheter un vélo pour flamber")
    AidFactory(
        perimeter=perimeters["france"],
        name="Construire un atelier de réparation pour vélos",
    )
    AidFactory(
        perimeter=perimeters["france"], name="Organiser un tour de France sur autoroute"
    )
    url = reverse("search_view")

    synonym_list = SynonymListFactory(
        name="Voie douce",
        keywords_list="voie douce, vélo, vélos, liaisons douces, bmx, piste cyclable",
    )

    # Searching with a synonym-list find the aids and exclude irrelevant results
    res = client.get(url, data={"text": synonym_list.id_slug})
    assert res.context["paginator"].count == 3


def test_the_call_for_project_only_filter(client, perimeters, aids):

    for aid in aids[:5]:
        aid.is_call_for_project = True
        aid.save()

    url = reverse("search_view")
    res = client.get(url, data={"call_for_projects_only": "Oui"})
    assert res.context["paginator"].count == 5


def test_program_filter(client, perimeters, aids):
    """Test that results can be filtered by aid programs."""

    program = ProgramFactory()
    aids[0].programs.set([program])
    url = reverse("search_view")
    res = client.get(url, data={"programs": program.slug})
    assert res.context["paginator"].count == 1


def test_submission_deadline_ordering(client, perimeters):
    """Test that results can be sorted by approaching deadline."""

    AidFactory(
        name="Approaching aid",
        perimeter=perimeters["europe"],
        submission_deadline=timezone.now() + timedelta(days=5),
    )
    AidFactory(
        name="Plenty of time aid",
        perimeter=perimeters["france"],
        submission_deadline=timezone.now() + timedelta(days=150),
    )

    url = reverse("search_view")

    res = client.get(url)
    assert res.context["paginator"].count == 2
    assert res.context["aids"][0].name == "Plenty of time aid"
    assert res.context["aids"][1].name == "Approaching aid"

    res = client.get(url, data={"order_by": "submission_deadline"})
    assert res.context["paginator"].count == 2
    assert res.context["aids"][0].name == "Approaching aid"
    assert res.context["aids"][1].name == "Plenty of time aid"


def test_the_france_relance_boolean_filter(client, perimeters):
    AidFactory(
        name="Aide France Relance 1",
        perimeter=perimeters["europe"],
        in_france_relance=True,
    )
    AidFactory(
        name="Aide France Relance 2",
        perimeter=perimeters["europe"],
        in_france_relance=True,
    )
    AidFactory(
        name="Aide France Relance 3",
        perimeter=perimeters["europe"],
        in_france_relance=True,
    )
    AidFactory(
        name="Aide diverse 4", perimeter=perimeters["europe"], in_france_relance=False
    )
    AidFactory(
        name="Aide diverse 5", perimeter=perimeters["europe"], in_france_relance=False
    )

    url = reverse("search_view")
    res = client.get(url)
    assert res.context["paginator"].count == 5

    # This filter is used to select FrRel aids
    res = client.get(url, data={"in_france_relance": "true"})
    assert res.context["paginator"].count == 3
    assert res.context["aids"][0].name == "Aide France Relance 1"
    assert res.context["aids"][1].name == "Aide France Relance 2"
    assert res.context["aids"][2].name == "Aide France Relance 3"

    # Any false value disables the filter
    res = client.get(url, data={"in_france_relance": "false"})
    assert res.context["paginator"].count == 5


def test_aids_can_be_filterd_by_published_after(client, perimeters):
    AidFactory(
        name="Aide A",
        perimeter=perimeters["europe"],
        date_published=timezone.make_aware(datetime(2020, 9, 3)),
    )
    AidFactory(
        name="Aide B",
        perimeter=perimeters["europe"],
        date_published=timezone.make_aware(datetime(2020, 9, 2)),
    )
    AidFactory(
        name="Aide C",
        perimeter=perimeters["europe"],
        date_published=timezone.make_aware(datetime(2019, 1, 1)),
    )

    url = reverse("search_view")
    res = client.get(url)
    assert res.context["paginator"].count == 3

    # This filter is used to select aids published after the latest_alert_date
    res = client.get(url, data={"published_after": "2020-09-03"})
    assert res.context["paginator"].count == 1
    assert res.context["aids"][0].name == "Aide A"

    res = client.get(url, data={"published_after": "2020-09-01"})
    assert res.context["paginator"].count == 2
    assert res.context["aids"][0].name == "Aide A"
    assert res.context["aids"][1].name == "Aide B"

    # If published_after filter doesn't match any aids there isn't any result
    res = client.get(url, data={"published_after": "2020-09-04"})
    assert res.context["paginator"].count == 0
