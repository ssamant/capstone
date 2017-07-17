from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^csa$', views.csa, name='csa'),
    url(r'^restaurants$', views.restaurants, name='restaurants'),
    url(r'^dashboard/members$', views.members, name='members'),
    url(r'^dashboard/members/(?P<member_id>\d+)$', views.member_info, name='member_info'),
    url(r'dashboard/signups', views.signups, name='signups'),
    url(r'dashboard/locations', views.locations, name='locations'),
    url(r'dashboard', views.dashboard, name='dashboard'),
    url(r'^newsletter$', views.newsletter, name='newsletter'),

    url(r'^signup_member$', views.signup_member, name='signup_member'),
    url(r'^signup_csa$', views.signup_csa, name='signup_csa'),
    url(r'^signup_success$', views.signup_success, name='signup_success'),
    url(r'^signup_done$', views.signup_done, name='signup_done'),
    
    url(r'^active$', views.active_signups, name='active_signups')
]
