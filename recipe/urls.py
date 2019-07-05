from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search, name='search'),
    path('saved/', views.saved_recipes, name='saved_recipes'),
]
