from django.shortcuts import render
from .models import Member
from .models import Location
from .models import Signup

def index(request):
    return render(request, 'farm_site/index.html', {})

def members(request):
    members = Member.objects.all
    return render(request, 'farm_site/members.html', {'members': members})


def dashboard(request):
    return render(request, 'farm_site/dashboard.html', {})


def locations(request):
    locations = Location.objects.filter(current=True)
    return render(request, 'farm_site/locations.html', {'locations': locations})

def signups(request):
    signups = Signup.objects.all
    return render(request, 'farm_site/signups.html', {'signups': signups})
