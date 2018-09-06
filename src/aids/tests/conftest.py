"""Global fixtures for tests."""

import pytest

from accounts.factories import UserFactory
from backers.factories import BackerFactory


@pytest.fixture
def user():
    """Generates a valid and active user."""

    user = UserFactory()
    return user


@pytest.fixture
def backer():
    """Generates a valid Backer."""

    backer = BackerFactory()
    return backer
