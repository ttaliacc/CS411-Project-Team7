# Generated by Django 4.0.7 on 2023-04-23 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdb',
            field=models.URLField(blank=True, max_length=128),
        ),
    ]