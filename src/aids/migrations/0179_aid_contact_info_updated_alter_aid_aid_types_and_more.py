# Generated by Django 4.2.1 on 2023-06-12 15:19

import core.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("geofr", "0045_financialdata"),
        ("eligibility", "0004_eligibilitytest_conclusions"),
        ("backers", "0015_backer_perimeter"),
        ("aids", "0178_alter_aid_application_url_alter_aid_origin_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="aid",
            name="contact_info_updated",
            field=models.BooleanField(
                default=False,
                help_text="Cette aide est en attente d’une revue des données                 de contact",
                verbose_name="En attente de revue des données de contact mises à jour",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="aid_types",
            field=core.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("grant", "Subvention"),
                        ("loan", "Prêt"),
                        ("recoverable_advance", "Avance récupérable"),
                        ("cee", "Certificat d'économie d'énergie (CEE)"),
                        ("technical_engineering", "Ingénierie technique"),
                        ("financial_engineering", "Ingénierie financière"),
                        ("legal_engineering", "Ingénierie Juridique / administrative"),
                        ("other", "Autre aide financière"),
                    ],
                    max_length=32,
                ),
                blank=True,
                help_text="Précisez le ou les types de l’aide.",
                null=True,
                size=None,
                verbose_name="Types d’aide",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="amendment_author_email",
            field=models.EmailField(
                blank=True,
                max_length=254,
                null=True,
                verbose_name="E-mail de l’auteur de l’amendement",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="amendment_author_name",
            field=models.CharField(
                blank=True, max_length=256, verbose_name="Auteur de l’amendement"
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="amendment_author_org",
            field=models.CharField(
                blank=True,
                max_length=255,
                verbose_name="Structure de l’auteur de l’amendement",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="author_notification",
            field=models.BooleanField(
                default=True,
                help_text="Un email doit-il être envoyé à l’auteur de cette aide         au moment de sa publication\xa0?",
                verbose_name="Envoyer un email à l’auteur de l’aide ?",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="description",
            field=models.TextField(
                verbose_name="Description complète de l’aide et de ses objectifs"
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="destinations",
            field=core.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("supply", "Dépenses de fonctionnement"),
                        ("investment", "Dépenses d’investissement"),
                    ],
                    max_length=32,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="Types de dépenses / actions couvertes",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="eligibility_test",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="aids",
                to="eligibility.eligibilitytest",
                verbose_name="Test d’éligibilité",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="european_aid",
            field=models.CharField(
                choices=[
                    ("sectorial", "Sectorielle"),
                    ("organizational", "Structurelle"),
                ],
                default=None,
                help_text="Précisez si l’aide européenne est structurelle ou sectorielle",
                max_length=32,
                null=True,
                verbose_name="Aide européenne ?",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="financers",
            field=models.ManyToManyField(
                related_name="financed_aids",
                through="aids.AidFinancer",
                to="backers.backer",
                verbose_name="Porteurs d’aides",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="import_data_url",
            field=models.URLField(
                blank=True,
                null=True,
                verbose_name="URL d’origine de la donnée importée",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="import_uniqueid",
            field=models.CharField(
                blank=True,
                max_length=200,
                null=True,
                unique=True,
                verbose_name="Identifiant d’import unique",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="import_updated",
            field=models.BooleanField(
                default=False,
                help_text="Cette aide est en attente d’une revue des mises à jour         proposées par l’outil d’import",
                verbose_name="En attente de revue des données importées mises à jour",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="is_call_for_project",
            field=models.BooleanField(
                null=True, verbose_name="Appel à projet / Manifestation d’intérêt"
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="is_charged",
            field=models.BooleanField(
                default=False,
                help_text="Ne pas cocher pour les aides sous adhésion et ajouter la mention         «\xa0*sous adhésion\xa0» dans les critères d’éligibilité.",
                verbose_name="Aide Payante",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="mobilization_steps",
            field=core.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("preop", "Réflexion / conception"),
                        ("op", "Mise en œuvre / réalisation"),
                        ("postop", "Usage / valorisation"),
                    ],
                    default="preop",
                    max_length=32,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="État d’avancement du projet pour bénéficier du dispositif",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="name",
            field=models.CharField(
                help_text="Le titre doit commencer par un verbe à l’infinitif pour que l’objectif de l’aide soit explicite vis-à-vis de ses bénéficiaires.",
                max_length=180,
                verbose_name="Nom",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="perimeter",
            field=models.ForeignKey(
                blank=True,
                help_text="Sur quel périmètre l’aide est-elle diffusée\xa0?",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="geofr.perimeter",
                verbose_name="Périmètre",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="recoverable_advance_amount",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Montant de l’avance récupérable"
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="recurrence",
            field=models.CharField(
                blank=True,
                choices=[
                    ("oneoff", "Ponctuelle"),
                    ("ongoing", "Permanente"),
                    ("recurring", "Récurrente"),
                ],
                help_text="L’aide est-elle ponctuelle, permanente, ou récurrente\xa0?",
                max_length=16,
                verbose_name="Récurrence",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="slug",
            field=models.SlugField(
                blank=True,
                help_text="Laisser vide pour autoremplir.",
                verbose_name="Fragment d’URL",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="start_date",
            field=models.DateField(
                blank=True,
                help_text="À quelle date l’aide est-elle ouverte aux candidatures\xa0?",
                null=True,
                verbose_name="Date d’ouverture",
            ),
        ),
        migrations.AlterField(
            model_name="aid",
            name="targeted_audiences",
            field=core.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("commune", "Communes"),
                        ("epci", "Intercommunalités / Pays"),
                        ("department", "Départements"),
                        ("region", "Régions"),
                        ("special", "Collectivités d'outre-mer à statuts particuliers"),
                        ("association", "Associations"),
                        ("private_person", "Particuliers"),
                        ("farmer", "Agriculteurs"),
                        ("private_sector", "Entreprises privées"),
                        (
                            "public_cies",
                            "Entreprises publiques locales (Sem, Spl, SemOp)",
                        ),
                        (
                            "public_org",
                            "Établissements publics (écoles, bibliothèques…) / Services de l'État",
                        ),
                        ("researcher", "Recherche"),
                    ],
                    max_length=32,
                ),
                blank=True,
                null=True,
                size=None,
                verbose_name="Bénéficiaires de l’aide",
            ),
        ),
        migrations.AlterField(
            model_name="aidproject",
            name="date_obtained",
            field=models.DateTimeField(
                blank=True,
                help_text="Date à laquelle cette aide a été obtenue par le porteur du projet",
                null=True,
                verbose_name="Date de l’obtention",
            ),
        ),
        migrations.AlterField(
            model_name="aidproject",
            name="date_paid",
            field=models.DateTimeField(
                blank=True,
                help_text="Date à laquelle cette aide a été reçue par le porteur du projet",
                null=True,
                verbose_name="Date de la réception de l’aide",
            ),
        ),
        migrations.AlterField(
            model_name="suggestedaidproject",
            name="date_associated",
            field=models.DateTimeField(
                blank=True,
                help_text="Date à laquelle cette aide a été acceptée par le porteur du projet",
                null=True,
                verbose_name="Date d’association",
            ),
        ),
    ]
