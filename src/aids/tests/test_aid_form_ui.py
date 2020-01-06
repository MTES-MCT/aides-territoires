# The following test has been working unreliably and costed too much to
# maintain. Hence, I decided it was the less worse of two evils to disable it.
# def test_calendar_fields_only_show_when_required(client, live_server,
#                                                  browser, contributor):
#     """Calendar fields are only displayed when they are needed."""

#     client.force_login(contributor)
#     cookie = client.cookies['sessionid']
#     browser.get(live_server.url)
#     browser.add_cookie({
#         'name': 'sessionid',
#         'value': cookie.value,
#         'secure': False,
#         'path': '/'})

#     aid = AidFactory(name='Gloubiboulga', recurrence='', author=contributor)
#     edit_url = reverse('aid_edit_view', args=[aid.slug])

#     browser.get(live_server + edit_url)
#     browser.implicitly_wait(1)
#     calendar_fields = browser.find_element_by_id('calendar-fields')
#     assert not calendar_fields.is_displayed()

#     recurrence_field = Select(browser.find_element_by_id('id_recurrence'))
#     recurrence_field.select_by_value('oneoff')
#     browser.implicitly_wait(1)
#     assert calendar_fields.is_displayed()

#     recurrence_field.select_by_value('ongoing')
#     browser.implicitly_wait(1)
#     assert not calendar_fields.is_displayed()

#     recurrence_field.select_by_value('recurring')
#     browser.implicitly_wait(1)
#     assert calendar_fields.is_displayed()

#     recurrence_field.select_by_value('')
#     browser.implicitly_wait(1)
#     assert not calendar_fields.is_displayed()
