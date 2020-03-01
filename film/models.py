from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=200, null=False)
    director = models.CharField(max_length=200, null=False)
    release_date = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.name
