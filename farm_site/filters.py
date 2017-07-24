import django_filters
from .models import Signup


class SignupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Singup
        fields = ['season__year', 'location__name']
