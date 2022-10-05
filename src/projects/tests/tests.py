import pytest

from django.urls import reverse

from accounts.factories import UserFactory
from organizations.factories import CommuneOrganizationFactory
from projects.factories import ProjectFactory
from projects.models import Project
from aids.factories import AidFactory, SuggestedAidProjectFactory
from aids.models import SuggestedAidProject

pytestmark = pytest.mark.django_db


def test_public_project_status_by_default_is_reviewable(client, perimeters):
    organization = CommuneOrganizationFactory()
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
    assert Project.objects.count() == 1
    project = Project.objects.first()
    assert project.is_public is True
    assert project.status == Project.STATUS.reviewable
    projects_list_page = reverse("project_list_view")
    res = client.get(projects_list_page, follow=True)
    assert "Votre nouveau projet a été créé" in res.content.decode()


def test_project_type_or_project_types_suggestion_fields_is_needed_to_make_a_project_public(
    client, perimeters
):
    organization = CommuneOrganizationFactory()
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
    assert Project.objects.count() == 0
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
    )
    url = reverse("public_project_detail_view", args=[project.pk, project.slug])
    client.force_login(user)
    res = client.get(url)
    assert res.status_code == 200
    assert project.description in res.content.decode()


def test_authenticated_user_can_add_public_project_to_favorite(client):
    public_project_organization = CommuneOrganizationFactory()
    user_organization = CommuneOrganizationFactory()
    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
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


def test_project_owner_can_associate_suggested_aid_to_project(client):
    user = UserFactory(email="public@project.creator")
    user_organization = CommuneOrganizationFactory()
    user_organization.beneficiaries.add(user.pk)
    user_organization.save()
    user.beneficiary_organization = user_organization
    user.save()
    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
    )
    project.organizations.add(user_organization.pk)
    project.save()
    aid = AidFactory()
    suggested_aid = SuggestedAidProjectFactory()
    suggested_aid.creator = user
    suggested_aid.project = project
    suggested_aid.aid = aid
    suggested_aid.save()

    client.force_login(user)

    aid_match_project_url = reverse("aid_match_project_view", args=[aid.slug])
    res = client.post(
        aid_match_project_url,
        {"projects": [project.pk], "_page": "suggested_aid"},
    )

    assert res.status_code == 302
    detail_project_page = reverse(
        "project_detail_view", args=[project.pk, project.slug]
    )
    assert project in aid.projects.all()
    suggested_aid.refresh_from_db()
    assert suggested_aid.is_associated is True
    res = client.get(detail_project_page, follow=True)
    assert "L’aide a bien été associée au projet" in res.content.decode()


def test_project_owner_can_reject_a_suggested_aid(client):
    user = UserFactory(email="public@project.creator")
    user_organization = CommuneOrganizationFactory()
    user_organization.beneficiaries.add(user.pk)
    user_organization.save()
    user.beneficiary_organization = user_organization
    user.save()
    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
    )
    project.organizations.add(user_organization.pk)
    project.save()
    aid = AidFactory()
    suggested_aid = SuggestedAidProjectFactory()
    suggested_aid.creator = user
    suggested_aid.project = project
    suggested_aid.aid = aid
    suggested_aid.save()

    client.force_login(user)

    reject_suggested_aid_url = reverse("reject_suggested_aid_view", args=[aid.slug])
    res = client.post(
        reject_suggested_aid_url,
        {"project-pk": [project.pk]},
    )

    assert res.status_code == 302
    detail_project_page = reverse(
        "project_detail_view", args=[project.pk, project.slug]
    )
    assert project not in aid.projects.all()
    suggested_aid.refresh_from_db()
    assert suggested_aid.is_rejected is True
    res = client.get(detail_project_page, follow=True)
    assert (
        "L’aide a bien été supprimée de la liste des aides suggérées pour votre projet."
        in res.content.decode()
    )


def test_authenticated_user_can_suggest_aid_with_url(client):
    user = UserFactory(email="friendly@user.test")
    user_organization = CommuneOrganizationFactory()
    user_organization.beneficiaries.add(user.pk)
    user_organization.save()
    user.beneficiary_organization = user_organization
    user.save()

    project_owner = UserFactory(email="project@owner.test")
    project_owner_organization = CommuneOrganizationFactory()
    project_owner_organization.beneficiaries.add(project_owner.pk)
    project_owner_organization.save()
    project_owner.beneficiary_organization = project_owner_organization
    project_owner.save()

    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
    )
    project.organizations.add(user_organization.pk)
    project.organization_favorite.add(project_owner_organization.pk)
    project.save()

    aid = AidFactory()
    aid_url = f"https://aides-territoires.beta.gouv.fr{aid.get_absolute_url()}"

    client.force_login(user)

    suggested_aid_url = reverse("suggest_aid_view")
    res = client.post(
        suggested_aid_url,
        {
            "project": [project.pk],
            "aid": aid_url,
            "origin_page": "public_project_page",
        },
    )

    assert res.status_code == 302
    public_project_detail_page = reverse(
        "public_project_detail_view", args=[project.pk, project.slug]
    )
    assert SuggestedAidProject.objects.count() == 1
    assert SuggestedAidProject.objects.first().aid == aid
    assert SuggestedAidProject.objects.first().project == project
    res = client.get(public_project_detail_page, follow=True)
    assert "Merci! L’aide a bien été suggérée!" in res.content.decode()


def test_authenticated_user_can_suggest_aid_from_aid_detail_page(client):
    user = UserFactory(email="friendly@user.test")
    user_organization = CommuneOrganizationFactory()
    user_organization.beneficiaries.add(user.pk)
    user_organization.save()
    user.beneficiary_organization = user_organization
    user.save()

    project_owner = UserFactory(email="project@owner.test")
    project_owner_organization = CommuneOrganizationFactory()
    project_owner_organization.beneficiaries.add(project_owner.pk)
    project_owner_organization.save()
    project_owner.beneficiary_organization = project_owner_organization
    project_owner.save()

    project = ProjectFactory(
        status=Project.STATUS.published,
        is_public=True,
    )
    project.organizations.add(user_organization.pk)
    project.organization_favorite.add(project_owner_organization.pk)
    project.save()

    aid = AidFactory()

    client.force_login(user)

    suggested_aid_url = reverse("suggest_aid_view")
    res = client.post(
        suggested_aid_url,
        {
            "project": [project.pk],
            "aid": aid.slug,
            "origin_page": "aid_detail_page",
        },
    )

    assert res.status_code == 302
    aid_detail_page = reverse("aid_detail_view", args=[aid.slug])
    assert SuggestedAidProject.objects.count() == 1
    assert SuggestedAidProject.objects.first().aid == aid
    assert SuggestedAidProject.objects.first().project == project
    res = client.get(aid_detail_page, follow=True)
    assert "Merci! L’aide a bien été suggérée!" in res.content.decode()
