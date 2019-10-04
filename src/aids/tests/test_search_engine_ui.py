import time
from datetime import timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from django.urls import reverse
from django.utils import timezone

from aids.factories import AidFactory


def test_aid_detail_shows_link_to_previous_search(live_server, browser):
    aid = AidFactory(name='Gloubiboulga')
    AidFactory(name='Schtroumpf')

    search_url = reverse('search_view')
    browser.get(live_server + search_url)

    results = browser.find_elements_by_css_selector('section.aid h1')
    assert len(results) == 2

    search_input = browser.find_element_by_id('id_text')
    search_input.send_keys('Gloubiboulga')

    submit_btn = browser.find_element_by_css_selector(
        'section#search-engine form button.search-btn')
    submit_btn.click()
    time.sleep(1)

    results = browser.find_elements_by_css_selector('section.aid h1')
    assert len(results) == 1

    browser.get(live_server + aid.get_absolute_url())
    breadcrumbs = browser.find_elements_by_css_selector('ol.breadcrumb')
    assert 'text=Gloubiboulga' in breadcrumbs[0].get_attribute('innerHTML')


def test_sorting_field(live_server, browser):
    """Test the dynamic sorting field."""

    yesterday = timezone.now() - timedelta(days=1)
    AidFactory(name='Gloubiboulga', date_published=yesterday)
    AidFactory(name='Schtroumpf')

    search_url = reverse('search_view')
    browser.get(live_server + search_url)
    results = browser.find_elements_by_css_selector('section.aid h1')

    assert len(results) == 2
    assert 'Gloubiboulga' in results[0].get_attribute('innerHTML')

    sort_input = browser.find_element_by_id('sorting-btn')
    input_content = sort_input.get_attribute('innerHTML')
    assert 'pertinence' in input_content

    sort_input.click()
    WebDriverWait(browser, 20) \
        .until(EC.element_to_be_clickable(
            (By.ID, "sort-publication-date"))) \
        .click()

    time.sleep(0.5)

    assert 'order_by=publication_date' in browser.current_url

    sorted_results = browser.find_elements_by_css_selector('section.aid h1')
    assert len(sorted_results) == 2
    assert 'Schtroumpf' in sorted_results[0].get_attribute('innerHTML')
