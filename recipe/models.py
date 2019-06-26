from django.conf import settings
from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ##ingredients = models.ManyToManyField(Ingredients) ##NEED TO LOOK AT THIS AGAIN
    instructions = models.TextField()

    def __str__(self):
        return self.title
