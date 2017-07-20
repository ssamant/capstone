from django import template

register = template.Library()

@register.filter
def is_farmer(user):
    return user.groups.filter(name='Farmer').exists()

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)
