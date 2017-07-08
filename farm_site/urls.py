from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'dashboard/members', views.members, name='members'),
    url(r'dashboard/signups', views.signups, name='signups'),
    url(r'dashboard/locations', views.locations, name='locations'),
    url(r'dashboard', views.dashboard, name='dashboard')
]
