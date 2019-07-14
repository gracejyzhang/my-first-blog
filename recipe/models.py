from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, related_name='ingredients')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.ManyToManyField('Ingredient', through='IngredientQuantity', related_name='recipes') #'Ingredient', related_name='recipes' ##NEED TO LOOK AT THIS AGAIN
    users = models.ManyToManyField(User, related_name='recipes')

    def __str__(self):
        return self.title


class IngredientQuantity(models.Model):
    quantity = models.CharField(max_length=50)
    recipe = models.ForeignKey('Recipe', related_name='recipe', on_delete=models.SET_NULL, null=True)
    ingredient = models.ForeignKey('Ingredient', related_name='ingredient_quantity', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.quantity


class Instruction(models.Model):
    number = models.IntegerField()
    text = models.CharField(max_length=500)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
