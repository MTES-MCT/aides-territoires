# Generated by Django 2.2.9 on 2020-01-20 10:00

from django.db import migrations


def import_bookmarks(apps, schema_editor):
    Alert = apps.get_model("alerts", "Alert")
    Bookmark = apps.get_model("bookmarks", "Bookmark")

    alerts = []
    bookmarks = Bookmark.objects.filter(send_email_alert=True).select_related("owner")
    for bookmark in bookmarks:
        alerts.append(
            Alert(
                email=bookmark.owner.email,
                querystring=bookmark.querystring,
                title=bookmark.title,
                alert_frequency=bookmark.alert_frequency,
                validated=True,
                date_validated=bookmark.date_created,
                latest_alert_date=bookmark.latest_alert_date,
                date_created=bookmark.date_created,
                date_updated=bookmark.date_updated,
            )
        )
    Alert.objects.bulk_create(alerts)


class Migration(migrations.Migration):

    dependencies = [
        ("alerts", "0002_auto_20200117_1116"),
        ("bookmarks", "0007_auto_20191115_1448"),
    ]

    operations = [
        migrations.RunPython(import_bookmarks),
    ]
