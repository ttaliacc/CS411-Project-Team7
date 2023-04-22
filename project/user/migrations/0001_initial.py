# Generated by Django 4.0.7 on 2023-04-18 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('adult', models.BooleanField(default=False)),
                ('backdrop_path', models.CharField(blank=True, max_length=255, null=True)),
                ('homepage', models.CharField(blank=True, max_length=255, null=True)),
                ('imdb_id', models.CharField(blank=True, max_length=255, null=True)),
                ('original_language', models.CharField(max_length=255)),
                ('original_title', models.CharField(max_length=255)),
                ('overview', models.TextField()),
                ('popularity', models.FloatField(blank=True, null=True)),
                ('poster_path', models.CharField(blank=True, max_length=255, null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('title', models.CharField(max_length=255)),
                ('video', models.BooleanField(default=False)),
                ('vote_average', models.FloatField(blank=True, null=True)),
                ('vote_count', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]