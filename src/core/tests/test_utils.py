from core.utils import get_subdomain_from_host


def test_get_subdomain_from_host():
    host_testset = [
        # ('given-host', 'expected-subdomain')
        ('aides-territoires.local:8000', 'aides-territoires'),
        ('aides-territoires.beta.gouv.fr', 'aides-territoires'),
        ('aides-territoires.osc-fr1.scalingo.io', 'aides-territoires'),
        ('francemobilities.aides-territoires.beta.gouv.fr', 'francemobilities'),  # noqa
        ('staging.aides-territoires.beta.gouv.fr', 'staging'),
        ('staging.aides-territoires.osc-fr1.scalingo.io', 'staging'),
        ('aides-territoires-pr123.osc-fr1.scalingo.io', 'aides-territoires-pr123'),  # noqa
        ('aides.francemobilities.fr', 'aides.francemobilities.fr'),
        ('', ''),
    ]
    for host in host_testset:
        assert get_subdomain_from_host(host[0]) == host[1]
