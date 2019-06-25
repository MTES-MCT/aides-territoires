"""Global fixtures for tests."""

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from accounts.factories import UserFactory, ContributorFactory
from backers.factories import BackerFactory
from geofr.factories import PerimeterFactory


@pytest.fixture
def user():
    """Generates a valid and active user."""

    user = UserFactory()
    return user


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def contributor():
    """Generates a valid and active contributor."""

    user = ContributorFactory()
    return user


@pytest.fixture
def backer():
    """Generates a valid Backer."""

    backer = BackerFactory()
    return backer


@pytest.fixture
def perimeter():
    """Generates a valid Perimetes."""

    perimeter = PerimeterFactory()
    return perimeter


@pytest.fixture(scope="module")
def browser():
    opts = Options()
    opts.headless = True
    browser = webdriver.Firefox(options=opts)
    browser.implicitly_wait(1)
    browser.set_window_position(0, 0)
    browser.set_window_size(1200, 800)

    # This is equivalent to a `tearDown`.
    # Sometimes, I admire Python's elegancy so much!
    yield browser
    browser.quit()
