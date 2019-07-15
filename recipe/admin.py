from django.contrib import admin
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Instruction, IngredientQuantity, Tag


# Register your models here.

class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity

class InstructionInline(admin.TabularInline):
    model = Instruction

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientQuantityInline,]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Instruction)
admin.site.register(IngredientQuantity)
admin.site.register(Tag)

