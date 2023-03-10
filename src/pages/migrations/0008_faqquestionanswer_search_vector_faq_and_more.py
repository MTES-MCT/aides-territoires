# Generated by Django 4.1.5 on 2023-03-07 09:29

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0007_faqcategory_faqquestionanswer"),
    ]

    operations = [
        migrations.AddField(
            model_name="faqquestionanswer",
            name="search_vector_faq",
            field=django.contrib.postgres.search.SearchVectorField(
                null=True, verbose_name="Search vector FAQ"
            ),
        ),
        migrations.AddIndex(
            model_name="faqquestionanswer",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector_faq"], name="pages_faqqu_search__e8ffa7_gin"
            ),
        ),
    ]
