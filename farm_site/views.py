from django.shortcuts import render

def index(request):
    return render(request, 'farm_site/index.html', {})
