from bs4 import BeautifulSoup
import pytest

from django.core import management
from django.urls import reverse
from django.utils.text import slugify
from aids.factories import AidFactory

from backers.factories import BackerFactory

pytestmark = pytest.mark.django_db


def test_map_view_is_complete(client, perimeters, aids):
    BackerFactory(financed_aids=[aids[0], aids[1]])
    BackerFactory(financed_aids=[aids[2], aids[3]])

    management.call_command("count_by_department")

    # force launching the task first
    url = reverse("map_view")
    res = client.get(url)
    assert res.status_code == 200

    assert "map-svg" in res.content.decode()
    assert "2 porteurs" in res.content.decode()


def test_department_view_is_complete(client, perimeters, aids):
    BackerFactory(financed_aids=[aids[0], aids[1]], perimeter=perimeters["herault"])
    BackerFactory(financed_aids=[aids[2], aids[3]], perimeter=perimeters["herault"])

    # force launching the task first
    management.call_command("count_by_department")

    herault = perimeters["herault"]
    url = reverse(
        "department_view", kwargs={"code": herault.code, "slug": slugify(herault.name)}
    )
    res = client.get(url)

    assert res.status_code == 200

    assert "Top 10 des 2 porteurs par nombre d’aides :" in res.content.decode()


def test_department_view_has_detailed_data_for_engineering_aids(client, perimeters):

    normandie = perimeters["normandie"]
    aid_1 = AidFactory(aid_types=["technical_engineering"], perimeter=normandie)
    aid_2 = AidFactory(aid_types=["financial_engineering"], perimeter=normandie)
    aid_3 = AidFactory(aid_types=["financial_engineering"], perimeter=normandie)
    BackerFactory(
        name="Porteur 1", financed_aids=[aid_1, aid_2, aid_3], perimeter=normandie
    )

    # force launching the task first
    management.call_command("count_by_department")

    normandie = perimeters["normandie"]
    url = reverse(
        "department_view",
        kwargs={"code": normandie.code, "slug": slugify(normandie.name)},
    )
    res = client.get(f"{url}?aid_type=technical_group")

    print(res.content.decode())
    assert res.status_code == 200

    soup = BeautifulSoup(res.content.decode(), "html.parser")

    table = soup.find_all("table")[0]

    row = table.find_all("tr")[1]

    assert [a.string.strip() for a in row.find_all("a")] == [
        "Porteur 1",
        "3",
        "1",
        "2",
        "0",
    ]
