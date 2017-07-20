from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    #general
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^csa$', views.csa, name='csa'),
    url(r'^restaurants$', views.restaurants, name='restaurants'),
    url(r'^newsletter$', views.newsletter, name='newsletter'),

    #csa signup
    url(r'^signup_member$', views.signup_member, name='signup_member'),
    url(r'^signup_csa$', views.signup_csa, name='signup_csa'),
    url(r'^signup_success$', views.signup_success, name='signup_success'),
    url(r'^signup_done$', views.signup_done, name='signup_done'),

    #farmers
    url(r'dashboard$', views.dashboard, name='dashboard'),
    url(r'dashboard/members$', views.members, name='members'),
    url(r'dashboard/members/(?P<member_id>\d+)$', views.member_info, name='member_info'),
    url(r'dashboard/signups$', views.signups, name='signups'),
    url(r'dashboard/locations$', views.locations, name='locations'),
    url(r'dashboard/active$', views.active_signups, name='active_signups'),

    #csa members with login
    url(r'^csa/(?P<member_id>\d+)$', views.csa_member_info, name='csa_member_info'),

    #authentication
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls)
]
