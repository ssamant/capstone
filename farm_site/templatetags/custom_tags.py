from django import template

register = template.Library()

@register.filter
def is_farmer(user):
    return user.groups.filter(name='Farmer').exists()


@register.filter
def by_season(signups, season_id):
    return signups.filter(season=season_id)
