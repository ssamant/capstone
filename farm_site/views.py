from django.shortcuts import render, render, get_object_or_404, redirect
from django.utils import timezone
from .models import Member
from .models import Location
from .models import Signup
from .models import Season

# general views
def index(request):
    return render(request, 'farm_site/index.html', {})

def about(request):
    return render(request, 'farm_site/about.html', {})

def csa(request):
    return render(request, 'farm_site/csa.html', {})

def restaurants(request):
    return render(request, 'farm_site/restaurants.html', {})

# csa member views


# farmers views
def dashboard(request):
    return render(request, 'farm_site/dashboard.html', {})


def members(request):
    current_signups = Signup.objects.filter(season__current_season=True).order_by("member__last_name")
    current_year = Season.objects.get(current_season=True).year

    return render(request, 'farm_site/members.html', {'signups': current_signups, 'current_year': current_year})

def member_info(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    signups = member.signup_set.all()
    try:
        current_signup = member.signup_set.get(season__current_season=True)
    except Signup.DoesNotExist:
        current_signup = None

    return render(request, 'farm_site/member_info.html', { 'member': member, 'signups': signups, 'current_signup': current_signup })

def locations(request):
    locations = Location.objects.filter(current=True).order_by("name")
    current_year = Season.objects.get(current_season=True).year
    return render(request, 'farm_site/locations.html', {'locations': locations, 'current_year': current_year})

def signups(request):
    signups = Signup.objects.all
    return render(request, 'farm_site/signups.html', {'signups': signups})

def newsletter(request):
    return render(request, 'farm_site/newsletter.html', {})
