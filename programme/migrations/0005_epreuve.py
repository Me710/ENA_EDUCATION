# Generated by Django 4.1.6 on 2023-06-17 21:52

from django.db import migrations, models
import django.db.models.deletion
import programme.models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0004_rename_niveau_lesson_categorie_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Epreuve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epreuve_id', models.CharField(max_length=40, unique=True)),
                ('nom', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('ecole', models.CharField(max_length=40)),
                ('niveau', models.PositiveIntegerField()),
                ('annee', models.PositiveIntegerField()),
                ('description', models.TextField(max_length=500)),
                ('miniature', models.ImageField(blank=True, upload_to=programme.models.generate_image)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='PDF', verbose_name='Epreuve en pdf')),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epreuve', to='programme.categories')),
            ],
        ),
    ]
