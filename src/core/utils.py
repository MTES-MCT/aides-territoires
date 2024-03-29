import requests
import unicodedata
import operator

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.postgres.search import SearchQuery
from django.core.files.storage import FileSystemStorage
from django.views.generic import RedirectView


def reupload_files(model, fieldname):
    """Reupload some media files to s3.

    Returns a migration method.
    """
    app, model_name = model.split(".")
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
    nfkd_form = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def remove_forbidden_chars(input_str):
    """
    Remove forbidden characters that can cause error 500
    when present in free text searches
    - For now, only the null character is managed
    """
    return input_str.replace("\x00", "")


def parse_query(raw_query):
    """Process a raw query and returns a `SearchQuery`.

    In Postgres, you converts a search query into a `tsquery` object
    that is matched against a `tsvector` object.

    The main method to get a `tsquery` is to use
    the function `plainto_tsquery` that is designed to transform
    unformatted text and generates a `tsquery` with tokens separated by
    `AND`. That is the default function used by Django when you create
    a `SearchQuery` object.

    If you want to create a `ts_query` with other boolean operators, you
    have two main solutions:
        - use the `to_tsquery` method that is not made to handle raw data
        - create several `ts_query` objects and combine them using
        boolean operators.

    This is the second solution we are using.

    By default, terms are made mandatory.
    Terms with a comma in between are optional.
    """
    all_terms = filter(None, raw_query.lower().split(","))
    all_terms = list(all_terms)
    all_terms = [term.strip(" ") for term in all_terms]

    next_operator = operator.or_
    invert = False
    query = None

    for term in all_terms:
        if len(term.split(" ")) > 1:
            list_sub_term = term.split(" ")
            sub_query = None
            for sub_term in list_sub_term:
                next_operator = operator.and_
                if sub_query is None:
                    sub_query = SearchQuery(
                        sub_term, config="french_unaccent", invert=invert
                    )
                else:
                    sub_query = next_operator(
                        sub_query,
                        SearchQuery(sub_term, config="french_unaccent", invert=invert),
                    )
            if query is None:
                query = sub_query
            else:
                next_operator = operator.or_
                query = next_operator(query, sub_query)
        else:
            if query is None:
                query = SearchQuery(term, config="french_unaccent", invert=invert)
            else:
                query = next_operator(
                    query, SearchQuery(term, config="french_unaccent", invert=invert)
                )

        next_operator = operator.or_
        invert = False

    return query


def get_base_url():
    site = Site.objects.get_current()
    if "localhost" in site.domain:
        scheme = "http"
    else:
        scheme = "https"
    base_url = f"{scheme}://{site.domain}"
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
    if "aides-territoires" in host:
        return host.split(".")[0]
    return host


def is_subdomain(subdomain):
    """
    Check if string is subdomain
    """
    if subdomain and subdomain != "aides-territoires":
        return True
    return False


def build_host_with_subdomain(host, subdomain):
    """
    Build domain with subdomain
    """
    if is_subdomain(subdomain):
        if subdomain == "francemobilites":
            return "aides.francemobilites.fr"
        else:
            return f"{subdomain}.{host}"
    return host


def get_stored_file_url(file_name: str, folder: str = "resources") -> str:
    """
    Returns the URL of a file on our storage bucket
    """
    cloud_root = getattr(settings, "AWS_S3_ENDPOINT_URL", "")
    bucket_name = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "")

    return f"{cloud_root}/{bucket_name}/{folder}/{file_name}"


def download_file_to_tmp(distant_file_name: str, local_file_name: str) -> str:
    """
    Download a file from the bucket and store it in /tmp
    Useful for a big CSV file.

    Restricted to files already on the bucket in order to limit
    the risks associated to downloading a file to the /tmp folder
    """
    file_url = get_stored_file_url(distant_file_name)
    local_folder = "tmp"
    local_path = f"/{local_folder}/{local_file_name}"

    response = requests.get(file_url)

    with open(local_path, "wb") as f:
        f.write(response.content)

    return local_path


class RedirectAidDetailView(RedirectView):
    """
    We are using this view as a temporary fix.
    Some links have been sent to users using the
    wrong aid detail URL - it was an issue with
    translations.
    """

    permanent = False
    redirect_url = "/aides/{slug}/"

    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs.get("slug")
        return self.redirect_url.format(slug=slug)
