from django import template
from ..models import Recipe

register = template.Library()

@register.filter(name='get_quantity')
def get_quantity(queryset, search):
    for element in queryset:
        if element.ingredient == search:
            return element

#returns boolean
@register.filter(name='check_list')
def check_list(user, pk):
    if Recipe.objects.filter(users=user, pk=pk).exists():
        return "Delete"
    else:
        return "Add"
