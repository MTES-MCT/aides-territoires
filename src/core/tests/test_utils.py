from core.utils import get_subdomain_from_host


def test_get_subdomain_from_host():
    host_testset = [
        # (host, subdomain)
        ('aides-territoires.local:8000', 'aides-territoires'),
        ('aides-territoires.beta.gouv.fr', 'aides-territoires'),
        ('francemobilities.aides-territoires.beta.gouv.fr', 'francemobilities'),  # noqa
        ('staging.aides-territoires.beta.gouv.fr', 'staging'),
        ('aides.francemobilities.fr', 'aides.francemobilities.fr'),
        ('', ''),
    ]
    for host in host_testset:
        assert get_subdomain_from_host(host[0]) == host[1]
