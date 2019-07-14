from django import forms
from django.forms import ModelMultipleChoiceField
from .models import Recipe, Ingredient, IngredientQuantity
from django_select2.forms import Select2MultipleWidget, ModelSelect2MultipleWidget

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


## figure out a way to use ModelSelect2MultipleWidget(queryset=Recipe.objects.all(), search_fields=['title_icontains']) - not working
## arbitrarily used Recipe.objects.all() and Recipe.objects.none() as defaults; but this form is used for both recipe and ingredients
## can I rename items so that it changes between recipes and ingredients depending on path?
class EditSelect2Form(forms.Form):
    items = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget, queryset=Recipe.objects.all())

    def __init__(self, qs=Recipe.objects.none(), *args, **kwargs):
        super(EditSelect2Form, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = qs
