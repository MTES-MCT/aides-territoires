# Generated by Django 4.2.1 on 2023-06-27 08:14

import backers.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("backers", "0015_backer_perimeter"),
    ]

    operations = [
        migrations.CreateModel(
            name="BackerCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, max_length=256, verbose_name="Nom"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Laissez vide pour autoremplir",
                        verbose_name="Fragment d’URL",
                    ),
                ),
                ("order", models.PositiveIntegerField(default=1, verbose_name="Rang")),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Date de création",
                    ),
                ),
            ],
            options={
                "verbose_name": "Catégorie de porteurs",
                "verbose_name_plural": "Catégories de porteurs",
                "ordering": ["order"],
            },
        ),
        migrations.AlterModelOptions(
            name="backer",
            options={"verbose_name": "Porteur", "verbose_name_plural": "Porteurs"},
        ),
        migrations.AlterModelOptions(
            name="backergroup",
            options={
                "verbose_name": "Groupe de porteurs",
                "verbose_name_plural": "Groupes de porteurs",
            },
        ),
        migrations.AlterField(
            model_name="backer",
            name="date_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Date de création"
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="description",
            field=models.TextField(
                blank=True,
                default="",
                verbose_name="Description complète du porteur d’aides",
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="external_link",
            field=models.URLField(
                blank=True,
                help_text="L’URL externe vers laquelle renvoie un clic sur le logo du porteur",
                null=True,
                verbose_name="Lien externe",
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="backers",
                to="backers.backergroup",
                verbose_name="Groupe de porteurs",
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="is_corporate",
            field=models.BooleanField(
                default=False, verbose_name="Porteur d’aides privé\xa0?"
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="is_spotlighted",
            field=models.BooleanField(
                default=False,
                help_text="Si le porteur est mis en avant, son logo apparaît sur la page d’accueil",
                verbose_name="Le porteur est-il mis en avant ?",
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="logo",
            field=models.FileField(
                blank=True,
                help_text="Évitez les fichiers trop lourds. Préférez les fichiers SVG.",
                null=True,
                upload_to=backers.models.logo_upload_to,
                verbose_name="Logo du porteur",
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="meta_description",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Sera affichée dans les SERPs. À garder < 120 caractères.",
                max_length=256,
                verbose_name="Description (balise meta)",
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="meta_title",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Le titre qui sera affiché dans les SERPs. Il est recommandé de le garder < \n        60 caractères.\n        Laissez vide pour réutiliser le nom du porteur d’aides.",
                max_length=180,
                verbose_name="Titre (balise meta)",
            ),
        ),
        migrations.AlterField(
            model_name="backer",
            name="name",
            field=models.CharField(db_index=True, max_length=256, verbose_name="Nom"),
        ),
        migrations.AlterField(
            model_name="backer",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Laissez vide pour autoremplir",
                verbose_name="Fragment d’URL",
            ),
        ),
        migrations.AlterField(
            model_name="backergroup",
            name="date_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Date de création"
            ),
        ),
        migrations.AlterField(
            model_name="backergroup",
            name="name",
            field=models.CharField(db_index=True, max_length=256, verbose_name="Nom"),
        ),
        migrations.AlterField(
            model_name="backergroup",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Laissez vide pour autoremplir",
                verbose_name="Fragment d’URL",
            ),
        ),
        migrations.CreateModel(
            name="BackerSubCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, max_length=256, verbose_name="Nom"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Laissez vide pour autoremplir",
                        verbose_name="Fragment d'url",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Date de création",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="backer_subcategories",
                        to="backers.backercategory",
                        verbose_name="Catégorie de porteurs",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sous-Catégorie de porteurs",
                "verbose_name_plural": "Sous-Catégories de porteurs",
            },
        ),
        migrations.AddField(
            model_name="backergroup",
            name="subcategory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="backer_group",
                to="backers.backersubcategory",
                verbose_name="Sous-Catégorie de porteurs",
            ),
        ),
    ]
