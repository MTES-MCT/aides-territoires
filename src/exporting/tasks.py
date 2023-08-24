from django.core import files
from django.core.files.base import ContentFile
from django.utils import timezone, dateformat

from core.celery import app

from aids.models import Aid, AidProject
from aids.resources import AidResource, AidProjectResource
from accounts.models import User
from accounts.resources import UserResource
from exporting.models import DataExport
from projects.models import Project, ValidatedProject
from projects.resources import ProjectResource, ValidatedProjectResource
from aids.services.export import export_related_projects


def export_aids(aids_id_list, author_id, file_format):
    queryset = Aid.objects.filter(id__in=aids_id_list)
    exported_data = AidResource().export(queryset)
    if file_format == "csv":
        file_content = ContentFile(exported_data.csv.encode())
    if file_format == "xlsx":
        file_content = ContentFile(exported_data.xlsx)
    file_name = "export-aides-"
    file_name += dateformat.format(timezone.now(), "Y-m-d_H-i-s")
    file_name += f".{file_format}"
    file_object = files.File(file_content, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    file_content.close()


def export_aidprojects(aidprojects_id_list, author_id, file_format):
    queryset = AidProject.objects.filter(id__in=aidprojects_id_list)
    exported_data = AidProjectResource().export(queryset)
    if file_format == "csv":
        file_content = ContentFile(exported_data.csv.encode())
    if file_format == "xlsx":
        file_content = ContentFile(exported_data.xlsx)
    file_name = "export-aides-"
    file_name += dateformat.format(timezone.now(), "Y-m-d_H-i-s")
    file_name += f".{file_format}"
    file_object = files.File(file_content, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    file_content.close()


@app.task
def export_aids_as_csv(aids_id_list, author_id):
    export_aids(aids_id_list, author_id, file_format="csv")


@app.task
def export_aids_as_xlsx(aids_id_list, author_id):
    export_aids(aids_id_list, author_id, file_format="xlsx")


@app.task
def export_related_projects_as_xlsx(aid_id, user_id):
    return export_related_projects(aid_id, user_id)


@app.task
def export_aidprojects_as_csv(aidprojects_id_list, author_id):
    export_aidprojects(aidprojects_id_list, author_id, file_format="csv")


@app.task
def export_aidprojects_as_xlsx(aidprojects_id_list, author_id):
    export_aidprojects(aidprojects_id_list, author_id, file_format="xlsx")


def export_projects(validated_projects_id_list, author_id, file_format):
    queryset = Project.objects.filter(id__in=validated_projects_id_list)
    exported_data = ProjectResource().export(queryset)
    if file_format == "csv":
        file_content = ContentFile(exported_data.csv.encode())
    if file_format == "xlsx":
        file_content = ContentFile(exported_data.xlsx)
    file_name = "export-projets-"
    file_name += dateformat.format(timezone.now(), "Y-m-d_H-i-s")
    file_name += f".{file_format}"
    file_object = files.File(file_content, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    file_content.close()


@app.task
def export_projects_as_csv(projects_id_list, author_id):
    export_projects(projects_id_list, author_id, file_format="csv")


@app.task
def export_projects_as_xlsx(projects_id_list, author_id):
    export_projects(projects_id_list, author_id, file_format="xlsx")


def export_validated_projects(validated_projects_id_list, author_id, file_format):
    queryset = ValidatedProject.objects.filter(id__in=validated_projects_id_list)
    exported_data = ValidatedProjectResource().export(queryset)
    if file_format == "csv":
        file_content = ContentFile(exported_data.csv.encode())
    if file_format == "xlsx":
        file_content = ContentFile(exported_data.xlsx)
    file_name = "export-projets-subventionnes-"
    file_name += dateformat.format(timezone.now(), "Y-m-d_H-i-s")
    file_name += f".{file_format}"
    file_object = files.File(file_content, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    file_content.close()


@app.task
def export_validated_projects_as_csv(validated_projects_id_list, author_id):
    export_validated_projects(validated_projects_id_list, author_id, file_format="csv")


@app.task
def export_validated_projects_as_xlsx(validated_projects_id_list, author_id):
    export_validated_projects(validated_projects_id_list, author_id, file_format="xlsx")


def export_users(users_id_list, author_id, file_format):
    queryset = User.objects.filter(id__in=users_id_list)
    exported_data = UserResource().export(queryset)
    if file_format == "csv":
        file_content = ContentFile(exported_data.csv.encode())
    if file_format == "xlsx":
        file_content = ContentFile(exported_data.xlsx)
    file_name = "export-utilisateurs-"
    file_name += dateformat.format(timezone.now(), "Y-m-d_H-i-s")
    file_name += f".{file_format}"
    file_object = files.File(file_content, name=file_name)
    DataExport.objects.create(
        author_id=author_id,
        exported_file=file_object,
    )
    file_object.close()
    file_content.close()


@app.task
def export_users_as_csv(users_id_list, author_id):
    export_users(users_id_list, author_id, file_format="csv")


@app.task
def export_users_as_xlsx(users_id_list, author_id):
    export_users(users_id_list, author_id, file_format="xlsx")
