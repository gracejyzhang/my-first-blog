from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Ingredient, IngredientQuantity, Instruction
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import AddDeleteForm, SearchForm

# Create your views here.

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = Ingredient.objects.filter(recipes__title=recipe.title)
    ingredient_quantity = IngredientQuantity.objects.filter(recipe__title=recipe.title)
    instructions = Instruction.objects.filter(recipe__title=recipe.title).order_by('number')

    if request.method == "POST" and request.user.is_authenticated:
        AddDeleteForm(request.POST).add_or_delete(request.user, pk)

    return render(request, 'recipe/recipe_detail.html', {'recipe': recipe, 'ingredients': ingredients, 'instructions': instructions, 'ingredient_quantity': ingredient_quantity})

def search(request):
    results = SearchForm(request.GET).search(request.GET['q'])
    return render(request, 'recipe/results.html', {'results': results})

def saved_recipes(request):
    recipes = Recipe.objects.filter(users=request.user)
    return render(request, 'saved_recipes/saved_recipes.html', {'recipes': recipes})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('recipe_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})



