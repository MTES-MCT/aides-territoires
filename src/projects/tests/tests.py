import pytest

from django.urls import reverse

from accounts.factories import UserFactory
from organizations.factories import OrganizationFactory
from projects.factories import ProjectFactory
from projects.models import Project

pytestmark = pytest.mark.django_db


def test_public_project_status_by_default_is_reviewable(client, perimeters):
    organization = OrganizationFactory()
    organization.organization_type = ["commune"]
    organization.zip_code = 34080
    organization.city_name = "Montpellier"
    organization.perimeter = perimeters["montpellier"]
    organization.save()

    user = UserFactory(
        email="public@project.creator", beneficiary_organization=organization
    )

    client.force_login(user)
    create_project_url = reverse("project_create_view")
    res = client.post(
        create_project_url,
        {
            "name": "a public project",
            "description": "this is a public description",
            "private_description": "very private notes",
            "project_types_suggestion": "this a suggested project type",
            "is_public": True,
        },
    )

    assert res.status_code == 302
    project = Project.objects.first()
    assert project.is_public is True
    assert project.status == Project.STATUS.reviewable
    projects_list_page = reverse("project_list_view")
    res = client.get(projects_list_page, follow=True)
    assert "Votre nouveau projet a été créé" in res.content.decode()


def test_project_type_or_project_types_suggestion_fields_is_needed_to_make_a_project_public(
    client, perimeters
):
    organization = OrganizationFactory()
    organization.organization_type = ["commune"]
    organization.zip_code = 34080
    organization.city_name = "Montpellier"
    organization.perimeter = perimeters["montpellier"]
    organization.save()

    user = UserFactory(
        email="public@project.creator", beneficiary_organization=organization
    )

    client.force_login(user)
    create_project_url = reverse("project_create_view")
    res = client.post(
        create_project_url,
        {
            "name": "a public project",
            "description": "this is a public description",
            "private_description": "very private notes",
            "is_public": True,
        },
    )

    assert res.status_code == 200
    Project.objects.count() == 0
    assert (
        "Merci de remplir au moins un des champs parmi &#x27;Types de projet&#x27;"
        in res.content.decode()
    )


def test_only_published_public_projects_are_displayed(client):
    project = ProjectFactory(status=Project.STATUS.draft, is_public=False)
    url = reverse("public_project_detail_view", args=[project.pk, project.slug])
    res = client.get(url)
    assert res.status_code == 403

    project.is_public = True
    project.status = Project.STATUS.reviewable
    project.save()
    res = client.get(url)
    assert res.status_code == 403

    project.status = Project.STATUS.published
    project.save()
    res = client.get(url)
    assert res.status_code == 200


def test_anonymous_user_cant_access_public_project_complete_informations(client):
    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
        description="a public description",
    )
    url = reverse("public_project_detail_view", args=[project.pk, project.slug])
    res = client.get(url)
    assert res.status_code == 200
    assert project.description not in res.content.decode()


def test_authenticated_user_can_access_public_project_complete_informations(
    client, user
):
    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
        description="a public description",
    )
    url = reverse("public_project_detail_view", args=[project.pk, project.slug])
    client.force_login(user)
    res = client.get(url)
    assert res.status_code == 200
    assert project.description in res.content.decode()


def test_authenticated_user_can_add_public_project_to_favorite(client):
    public_project_organization = OrganizationFactory()
    user_organization = OrganizationFactory()
    user_organization.organization_type = ["commune"]
    user_organization.save()
    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
        description="a public description",
    )
    project.organizations.add(public_project_organization)
    project.save()
    user = UserFactory(
        email="public@project.creator", beneficiary_organization=user_organization
    )

    client.force_login(user)

    add_project_to_favorite_url = reverse(
        "add_project_to_favorite_view", args=[user_organization.pk]
    )
    res = client.post(add_project_to_favorite_url, {"favorite_projects": project.pk})

    assert res.status_code == 302
    public_project_page = reverse(
        "public_project_detail_view", args=[project.pk, project.slug]
    )
    res = client.get(public_project_page, follow=True)
    assert (
        f"Le projet «{project.name}» a bien été ajouté à vos projets favoris"
        in res.content.decode()
    )
