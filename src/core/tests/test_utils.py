from core.utils import get_site_from_host, is_subdomain, build_host_with_subdomain


def test_get_site_from_host():
    host_testset = [
        # ('given-host', 'expected-subdomain')
        ("aides-territoires.local:8000", "aides-territoires"),
        ("aides-territoires.beta.gouv.fr", "aides-territoires"),
        ("aides-territoires.osc-fr1.scalingo.io", "aides-territoires"),
        ("francemobilites.aides-territoires.beta.gouv.fr", "francemobilites"),  # noqa
        ("staging.aides-territoires.beta.gouv.fr", "staging"),
        ("staging.aides-territoires.osc-fr1.scalingo.io", "staging"),
        (
            "aides-territoires-pr123.osc-fr1.scalingo.io",
            "aides-territoires-pr123",
        ),  # noqa
        ("aides.francemobilites.fr", "francemobilites"),
        ("", ""),
    ]
    for host in host_testset:
        assert get_site_from_host(host[0]) == host[1]


def test_is_subdomain():
    subdomain_testset = [
        ("", False),
        ("aides-territoires", False),
        ("francemobilites", True),
        ("staging", True),
        ("test", True),
    ]
    for subdomain in subdomain_testset:
        assert is_subdomain(subdomain[0]) == subdomain[1]


def test_build_host_with_subdomain():
    host_testset = [
        # ('given-host', 'expected-subdomain')
        (
            "aides-territoires.local:8000",
            "aides-territoires",
            "aides-territoires.local:8000",
        ),  # noqa
        (
            "aides-territoires.beta.gouv.fr",
            "aides-territoires",
            "aides-territoires.beta.gouv.fr",
        ),  # noqa
        (
            "aides-territoires.beta.gouv.fr",
            "",
            "aides-territoires.beta.gouv.fr",
        ),  # noqa
        (
            "aides-territoires.osc-fr1.scalingo.io",
            "aides-territoires",
            "aides-territoires.osc-fr1.scalingo.io",
        ),  # noqa
        (
            "aides-territoires.beta.gouv.fr",
            "francemobilites",
            "aides.francemobilites.fr",
        ),  # noqa
        (
            "aides-territoires.beta.gouv.fr",
            "staging",
            "staging.aides-territoires.beta.gouv.fr",
        ),  # noqa
        (
            "aides-territoires.osc-fr1.scalingo.io",
            "staging",
            "staging.aides-territoires.osc-fr1.scalingo.io",
        ),  # noqa
        (
            "osc-fr1.scalingo.io",
            "aides-territoires-pr123",
            "aides-territoires-pr123.osc-fr1.scalingo.io",
        ),  # noqa
    ]
    for host in host_testset:
        assert build_host_with_subdomain(host[0], host[1]) == host[2]
