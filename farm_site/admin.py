from django.contrib import admin
from .models import Member
from .models import Location
from .models import Season
from .models import Signup


admin.site.register(Member)
admin.site.register(Location)
admin.site.register(Season)
admin.site.register(Signup)
