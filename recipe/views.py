from django.shortcuts import render, get_object_or_404
from .models import Recipe, Ingredient, IngredientQuantity, Instruction

# Create your views here.

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = Ingredient.objects.filter(recipes__title=recipe.title)
    instructions = Instruction.objects.filter(recipe__title=recipe.title).order_by('number')
    return render(request, 'recipe/recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients, 'instructions': instructions})

def search(request):
    data = request.GET['q']
    data = data.split()
    recipes = Recipe.objects.all()
    ingredients = Ingredient.objects.all()
    results = []
    for recipe in recipes:
        for item in data:
            if item.lower() == recipe.title.lower():
                if recipe not in results:
                    results.append(recipe)
    for ingredient in ingredients:
        for item in data:
            if item.lower() == ingredient.name:
                for entry in Recipe.objects.filter(ingredients__name=ingredient.name):
                    if entry not in results:
                        results.append(entry)
    return render(request, 'recipe/results.html', {'results': results})
