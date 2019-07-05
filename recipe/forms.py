from django import forms
from .models import Recipe, Ingredient, IngredientQuantity

##Take another look at these forms; write more efficiently

class SearchForm(forms.Form):
    def search(self, query):
        query = query.split()
        recipes = Recipe.objects.all()
        ingredients = Ingredient.objects.all()
        results = []

        for recipe in recipes:
            for item in query:
                if item.lower() in self.clean(recipe.title):
                    if recipe not in results:
                        results.append(recipe)

        for ingredient in ingredients:
            for item in query:
                if item.lower() in self.clean(ingredient.name):
                    for entry in Recipe.objects.filter(ingredients__name=ingredient.name):
                        if entry not in results:
                            results.append(entry)

        return results

    def clean(self, word):
        return word.lower().split()


class AddDeleteForm(forms.Form):
    def add_or_delete(self, user, pk):
        recipe = Recipe.objects.get(pk=pk)

        if Recipe.objects.filter(users=user, pk=pk).exists():
            recipe.users.remove(user)
        else:
            recipe.users.add(user)
