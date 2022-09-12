# Generated by Django 3.2.15 on 2022-09-12 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='acquisition_channel',
            field=models.CharField(blank=True, choices=[('webinar', 'Webinaire'), ('animator', 'Animateur local'), ('trade_press', 'Presse spécialisée'), ('word_of_mouth', 'Bouche-à-oreille'), ('invited', 'Invitation à collaborer'), ('other', 'Autre')], help_text="Comment l'utilisateur a-t-il connu Aides-territoires?", max_length=32, null=True, verbose_name="Canal d'acquisition"),
        ),
        migrations.AddField(
            model_name='user',
            name='acquisition_channel_comment',
            field=models.CharField(blank=True, help_text="Comment l'utilisateur a-t-il connu Aides-territoires (champ libre)?", max_length=1000, null=True, verbose_name="Commentaire Canal d'acquisition"),
        ),
    ]
