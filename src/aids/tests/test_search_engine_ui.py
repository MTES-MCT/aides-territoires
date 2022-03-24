import time

from django.urls import reverse

from aids.factories import AidFactory
from selenium.webdriver.common.by import By

def test_aid_detail_shows_link_to_previous_search(live_server, browser):
    aid = AidFactory(name='Gloubiboulga')
    AidFactory(name='Schtroumpf')

    search_url = reverse('search_view')
    browser.get(live_server + search_url)

    results = browser.find_elements(By.CSS_SELECTOR, 'article.aid h1')
    assert len(results) == 2

    search_input = browser.find_element_by_id('id_text')
    search_input.send_keys('Gloubiboulga')

    submit_btn = browser.find_element_by_css_selector(
        'section#search-engine form button.search-btn')
    submit_btn.click()
    time.sleep(1)

    results = browser.find_elements_by_css_selector('article.aid h1')
    assert len(results) == 1

    browser.get(live_server + aid.get_absolute_url())
    breadcrumbs = browser.find_elements_by_css_selector('ol.breadcrumb')
    assert 'text=Gloubiboulga' in breadcrumbs[0].get_attribute('innerHTML')
