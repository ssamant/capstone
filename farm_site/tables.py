import django_tables2 as tables
from .models import Signup


class SignupTable(tables.Table):
    class Meta:

        model = Signup
        attrs = {'class': 'table',
            'th' : {
                '_ordering': {
                    'orderable': 'sortable', # Instead of `orderable`
                    'ascending': 'ascend',   # Instead of `asc`
                    'descending': 'descend'  # Instead of `desc`
                }
            }}
        sequence = ('season', 'location', 'member', 'box')
        exclude = ('id', 'paid', 'eggs', 'payment')
