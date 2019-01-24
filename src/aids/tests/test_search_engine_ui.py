import time

from django.urls import reverse

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from aids.factories import AidFactory


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


def test_search_filters_are_displayed(live_server, browser):
    """Seach filters button must appear when loading the page."""

    search_url = reverse('search_view')
    search_params = '?text=my_search_query&aid_types=grant&aid_types=loan'
    browser.get(live_server + search_url + search_params)
    assert 'Toutes les aides' in browser.title
    buttons = browser.find_elements_by_css_selector('div#filters button')
    assert len(buttons) == 3


def test_updating_the_form_displays_filters(live_server, browser):
    """Search filters buttons are dynamically displayed."""

    search_url = reverse('search_view')
    browser.get(live_server + search_url)
    assert 'Toutes les aides' in browser.title

    buttons = browser.find_elements_by_css_selector('div#filters button')
    assert len(buttons) == 0

    search_input = browser.find_element_by_id('id_text')
    search_input.send_keys('Gloubiboulga')

    buttons = browser.find_elements_by_css_selector('div#filters button')
    assert len(buttons) == 1

    button_content = buttons[0].get_attribute('innerHTML')
    assert 'Gloubiboulga' in button_content


def test_clicking_a_filter_removes_the_search_criteria(live_server, browser):
    """Clicking on a filter buttons removes the search filter."""

    search_url = reverse('search_view')
    search_params = '?text=Gloubiboulga'
    browser.get(live_server + search_url + search_params)
    assert 'text=Gloubiboulga' in browser.current_url

    buttons = browser.find_elements_by_css_selector('div#filters button')
    assert len(buttons) == 1
    assert buttons[0].is_displayed()
    assert 'Gloubiboulga' in buttons[0].get_attribute('innerHTML')

    buttons[0].click()
    time.sleep(0.5)

    assert 'text=Gloubiboulga' not in browser.current_url

    buttons = browser.find_elements_by_css_selector('div#filters button')
    assert len(buttons) == 0


def test_updating_the_form_performs_a_new_search(live_server, browser):
    """Search form dynamically updates search results."""

    AidFactory(name='Gloubiboulga')
    AidFactory(name='Schtroumpf')

    search_url = reverse('search_view')
    browser.get(live_server + search_url)

    results = browser.find_elements_by_css_selector('div.aid h1')
    assert len(results) == 2

    search_input = browser.find_element_by_id('id_text')
    search_input.send_keys('Gloubiboulga')
    time.sleep(1)
    results = browser.find_elements_by_css_selector('div.aid h1')
    assert len(results) == 1
    assert 'Gloubiboulga' in results[0].get_attribute('innerHTML')

    search_input.clear()
    search_input.send_keys('Schtroumpf')
    time.sleep(1)
    results = browser.find_elements_by_css_selector('div.aid h1')
    assert len(results) == 1
    assert 'Schtroumpf' in results[0].get_attribute('innerHTML')
