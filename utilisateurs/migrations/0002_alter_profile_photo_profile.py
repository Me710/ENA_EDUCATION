# Generated by Django 4.1 on 2023-02-01 23:59

from django.db import migrations, models
import utilisateurs.models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo_profile',
            field=models.ImageField(blank=True, upload_to=utilisateurs.models.renommer_image),
        ),
    ]