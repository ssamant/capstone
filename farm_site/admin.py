from django.contrib import admin
from .models import User, Member, Location, Season, Signup



admin.site.register(User)
admin.site.register(Location)
admin.site.register(Season)
admin.site.register(Signup)
admin.site.register(Member)
