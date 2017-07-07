from django.shortcuts import render
from .models import Member

def index(request):
    return render(request, 'farm_site/index.html', {})

def members(request):
    members = Member.objects.all
    return render(request, 'farm_site/members.html', {'members': members})


    
