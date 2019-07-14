from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Ingredient, IngredientQuantity, Instruction
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import AddDeleteForm, SearchForm, EditSelect2Form

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

def inventory(request):
    ingredients = Ingredient.objects.filter(users=request.user)
    return render(request, 'inventory/inventory.html', {'ingredients': ingredients})

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

def edit(request):
    if 'saved/' in request.path:
        qs = Recipe.objects.all()
        order = 'title'
    elif 'inventory/' in request.path:
        qs = Ingredient.objects.all()
        order = 'name'

    if request.method == 'POST':
        if 'Delete' in request.POST:
            form_delete = EditSelect2Form(qs.filter(users=request.user), request.POST)
            if form_delete.is_valid():
                for pk in request.POST.getlist('items'):
                    item = qs.get(pk=pk)
                    item.users.remove(request.user)
            form_add = EditSelect2Form(qs.exclude(users=request.user).order_by(order))

        elif 'Add' in request.POST:
            form_add = EditSelect2Form(qs.exclude(users=request.user), request.POST)
            if form_add.is_valid():
                for pk in request.POST.getlist('items'):
                    item = qs.get(pk=pk)
                    item.users.add(request.user)
            form_delete = EditSelect2Form(qs.filter(users=request.user).order_by(order))

    else:
        form_delete = EditSelect2Form(qs.filter(users=request.user).order_by(order))
        form_add = EditSelect2Form(qs.exclude(users=request.user).order_by(order))

    return render(request, 'edit.html', {'form_delete': form_delete, 'form_add': form_add})


