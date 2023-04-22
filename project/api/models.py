from django.db import models

# Create your models here.

class Genre(models.Model):
    gid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class StreamInfo(models.Model):
    display_name = models.CharField(max_length=255, null=True,blank=True)
    sid = models.CharField(max_length=255, default=0,null=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    icon = models.CharField(max_length=255,null=True,blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    adult = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    belongs_to_collection = models.CharField(max_length=255, null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    homepage = models.CharField(max_length=255, null=True, blank=True)
    imdb_id = models.CharField(max_length=255, null=True, blank=True)
    original_language = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    revenue = models.IntegerField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    tagline = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title