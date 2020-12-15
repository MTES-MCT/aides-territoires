import re

from django.utils import timezone


# The regex to detect existing title prefixes for duplicate aids
CLONE_PREFIX_RE = r'^\[Copie( \d{2}h\d{2})?\] '
#                   ^                           | Starts with...
#                    \[Copie               \]   | the string "[Copie] "...
#                           (            )?     | containing an optional...
#                             \d{2}h\d{2}       | H:M timestamp


def generate_clone_title(aid_title, now=None):
    """Return a suitable name for a duplicate aid.

    >>> generate_clone_name('Aid title')
    [Copie 10h04] Aid title]

    >>> generate_clone_name('[Copie 10h04] Aid title')
    [Copie 10h05] Aid title]
    """
    now = now or timezone.now()

    title_without_prefix = re.sub(CLONE_PREFIX_RE, r'', aid_title)
    new_title = f'[Copie {now:%Hh%M}] {title_without_prefix}'
    return new_title
