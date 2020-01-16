import pytest
from django.core.management import call_command

from aids.factories import AidFactory
from alerts.factories import BookmarkFactory

pytestmark = pytest.mark.django_db


def test_command_with_no_bookmarks(user, mailoutbox):
    call_command('send_bookmarks_alerts')
    assert len(mailoutbox) == 0


def test_command_with_a_bookmark_but_no_aids(user, mailoutbox):
    BookmarkFactory(owner=user, querystring='text=test')
    call_command('send_bookmarks_alerts')
    assert len(mailoutbox) == 0


def test_command_with_a_bookmark_but_no_matching_aids(user, mailoutbox):
    BookmarkFactory(owner=user, querystring='text=test')
    AidFactory.create_batch(5, name='Gloubiboulga')
    call_command('send_bookmarks_alerts')
    assert len(mailoutbox) == 0


def test_command_with_matching_aids(user, mailoutbox):
    BookmarkFactory(owner=user, querystring='text=test')
    AidFactory.create_batch(5, name='test')
    call_command('send_bookmarks_alerts')
    assert len(mailoutbox) == 1
    assert list(mailoutbox[0].to) == [user.email]


def test_command_with_disabled_email_setting(user, mailoutbox):
    BookmarkFactory(
        owner=user,
        send_email_alert=False,
        querystring='text=test')
    AidFactory.create_batch(5, name='test')
    call_command('send_bookmarks_alerts')
    assert len(mailoutbox) == 0


def test_command_output_format(user, mailoutbox):
    BookmarkFactory(
        owner=user,
        title='Gloubiboukmark',
        querystring='text=test')
    AidFactory.create(name='Test 1')
    AidFactory.create(name='Test 2')
    AidFactory.create(name='Test 3')
    AidFactory.create(name='Test 4')
    call_command('send_bookmarks_alerts')

    content = mailoutbox[0].body
    assert 'Gloubiboukmark' in content
    assert 'Test 1' in content
    assert 'Test 2' in content
    assert 'Test 3' in content

    # Only the first three aids are in the mail
    assert 'Test 4' not in content
    assert 'encore d\'autres aides disponibles !' in content
