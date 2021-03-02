from django.core.files.storage import FileSystemStorage


def reupload_files(model, fieldname):
    """Reupload some media files to s3.

    Returns a migration method.
    """
    app, model_name = model.split('.')
    fs_storage = FileSystemStorage()

    def do_reupload_files(apps, *args):
        Model = apps.get_model(app, model_name)
        for item in Model.objects.all():
            filename = getattr(item, fieldname).name
            if filename and fs_storage.exists(filename):
                field_file = fs_storage.open(filename)
                setattr(item, fieldname, field_file)
                item.save()

    return do_reupload_files


def get_subdomain_from_host(host):
    """
    Cleanup host field
    aides-territoires.beta.gouv.fr --> aides-territoires
    staging.aides-territoires.beta.gouv.fr --> staging
    francemobilities.aides-territoires.beta.gouv.fr --> francemobilities
    aides.francemobilities.fr --> aides.francemobilities.fr
    """
    # site = Site.objects.get_current()
    if 'aides-territoires' in host:
        return host.split('.')[0]
    return host
