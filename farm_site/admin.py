from django.contrib import admin
from .models import Member
from .models import Location
from .models import Season


admin.site.register(Member)
admin.site.register(Location)
admin.site.register(Season)
