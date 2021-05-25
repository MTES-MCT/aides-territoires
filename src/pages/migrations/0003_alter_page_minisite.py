# Generated by Django 3.2 on 2021-05-04 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0024_reupload_files'),
        ('pages', '0002_page_minisite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='minisite',
            field=models.ForeignKey(blank=True, help_text='Optional, link this page to a minisite.', null=True, on_delete=django.db.models.deletion.PROTECT, to='search.searchpage', verbose_name='Minisite'),
        ),
    ]
