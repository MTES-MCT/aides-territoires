import time

from django.urls import reverse

from aids.factories import AidFactory


def test_duplicate_buster(client, live_server, browser, contributor):

    client.force_login(contributor)
    cookie = client.cookies['sessionid']
    browser.get(live_server.url)
    browser.add_cookie({
        'name': 'sessionid',
        'value': cookie.value,
        'secure': False,
        'path': '/'})

    AidFactory(
        name='Schtroumpf',
        status='published',
        recurrence='ongoing',
        author=contributor,
        origin_url='https://example.com/schtroumpf/')

    aid = AidFactory(
        name='Gloubiboulga',
        status='published',
        recurrence='ongoing',
        author=contributor,
        origin_url='https://example.com/schtroumpf/')

    edit_url = reverse('aid_edit_view', args=[aid.slug])
    browser.get(live_server + edit_url)

    time.sleep(2)
    # browser.save_screenshot('/tmp/django.png')

    errors = browser.find_elements_by_css_selector('div.duplicate-error')
    assert len(errors) == 2
    assert 'Schtroumpf' in errors[0].get_attribute('innerHTML')
