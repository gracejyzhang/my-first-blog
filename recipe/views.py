from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipe/recipe_detail.html', {'recipe': recipe})
