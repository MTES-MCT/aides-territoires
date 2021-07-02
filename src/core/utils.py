import unicodedata

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.storage import FileSystemStorage
from django.views.generic import RedirectView


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


def remove_accents(input_str):
    """Remove accents from a string.

    Shamelessly stolen from SO.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def get_base_url():
    site = Site.objects.get_current()
    scheme = 'https'
    base_url = '{scheme}://{domain}'.format(
        scheme=scheme,
        domain=site.domain)
    return base_url


def get_site_from_host(host):
    """
    Return the string bit that identify a site.
    This can be the subdomain or a minisite slug.
    aides-territoires.beta.gouv.fr --> aides-territoires
    staging.aides-territoires.beta.gouv.fr --> staging
    francemobilites.aides-territoires.beta.gouv.fr --> francemobilites
    aides.francemobilites.fr --> francemobilites  # Using the mapping
    """
    for minisite_host, minisite_slug in settings.MAP_DNS_TO_MINISITES:
        # If we detect that a mapping is defined for the incoming
        # DNS host, then we get the minisite slug from that mapping.
        if minisite_host in host:
            return minisite_slug
    if 'aides-territoires' in host:
        return host.split('.')[0]
    return host


def is_subdomain(subdomain):
    """
    Check if string is subdomain
    """
    if subdomain and subdomain != 'aides-territoires':
        return True
    return False


def build_host_with_subdomain(host, subdomain):
    """
    Build domain with subdomain
    """
    if is_subdomain(subdomain):
        return f'{subdomain}.{host}'
    return host


class RedirectAidDetailView(RedirectView):
    """
    We are using this view as a temporary fix.
    Some links have been sent to users using the
    wrong aid detail URL - it was an issue with
    translations.
    """
    permanent = False
    redirect_url = '/aides/{slug}/'

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.get('slug')
        return self.redirect_url.format(slug=slug)
