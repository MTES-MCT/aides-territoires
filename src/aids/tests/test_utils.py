import pytest
from datetime import datetime

from aids.utils import generate_clone_title

clone_tests = [
    ("Aid title", "[Copie 10h42] Aid title"),
    ("[Copie 10h20] Aid title", "[Copie 10h42] Aid title"),
    ("[Copie] Aid title", "[Copie 10h42] Aid title"),
    ("[Portnawak] Aid title", "[Copie 10h42] [Portnawak] Aid title"),
]


@pytest.mark.parametrize("title,clone_title", clone_tests)
def test_generate_clone_title(title, clone_title):

    test_timestamp = datetime(year=2020, month=1, day=1, hour=10, minute=42)
    assert generate_clone_title(title, now=test_timestamp) == clone_title
