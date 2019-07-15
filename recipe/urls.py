from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search, name='search'),
    path('saved/', views.saved_recipes, name='saved_recipes'),
    path('saved/edit/', views.edit, name='edit_list'),
    path('select2/', include('django_select2.urls')),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/edit/', views.edit, name='edit_inventory'),
    path('shopping_list/', views.shopping_list, name='shopping_list'),
    path('recipe/add/', views.add_recipe, name='add_recipe')
]
