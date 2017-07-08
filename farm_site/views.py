from django.shortcuts import render, render, get_object_or_404, redirect
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
    current_signups = Signup.objects.filter(season_id=1).order_by("member")
    return render(request, 'farm_site/members.html', {'signups': current_signups})

def locations(request):
    locations = Location.objects.filter(current=True)
    return render(request, 'farm_site/locations.html', {'locations': locations})

def signups(request):
    signups = Signup.objects.all
    return render(request, 'farm_site/signups.html', {'signups': signups})
