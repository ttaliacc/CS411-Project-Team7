from django.db import models

# Create your models here.





class FavoriteMovies(models.Model):
    id = models.IntegerField(primary_key=True)
    adult = models.BooleanField(default=False)
    backdrop_path = models.CharField(max_length=255, null=True, blank=True)
    homepage = models.CharField(max_length=255, null=True, blank=True)
    movie_id = models.CharField(max_length=255, null=True, blank=True)
    original_language = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    popularity = models.FloatField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    video = models.BooleanField(default=False)
    vote_average = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
