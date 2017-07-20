from django import template

register = template.Library()

@register.filter
def is_farmer(user):
    return user.groups.filter(name='Farmer').exists()
