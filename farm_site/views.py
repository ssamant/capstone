from django.shortcuts import render, render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from .models import Member, Location, Signup, Season
from .forms import CreateMember, CreateSignup, CreateUser, SignupPaid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.forms import modelformset_factory
import logging

# general views
def index(request):
    return render(request, 'farm_site/index.html', {})

def about(request):
    return render(request, 'farm_site/about.html', {})

def csa(request):
    return render(request, 'farm_site/csa.html', {})

def restaurants(request):
    return render(request, 'farm_site/restaurants.html', {})

#sign up for a csa
def signup_member(request):
    if request.method == 'POST':
        form = CreateMember(request.POST)
        if form.is_valid():
            member = form.save()
            request.session['member_id'] = member.id
            return redirect('signup_csa')
            # add else to check if user is logged in
    else:
        form = CreateMember()
    return render(request, 'farm_site/signup_member.html', {'form': form})


def signup_csa(request):
    member = get_object_or_404(Member, pk=request.session['member_id'])
    if request.method == "POST":
        form = CreateSignup(request.POST)
        if form.is_valid():
            signup = form.save(commit=False)
            signup.member = member
            signup.season = Season.objects.get(current_season=True)
            signup.save()
            request.session['signup_id'] = signup.id
            return redirect('signup_success')
    else:
        form = CreateSignup()
    return render(request, 'farm_site/signup_csa.html', {'form': form})

def signup_success(request):
    #need to get member object to put in User
    signup = get_object_or_404(Signup, pk=request.session['signup_id'])
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            member = get_object_or_404(Member, pk=request.session['member_id'])
            user.member = member
            # check if user.save() would work instead
            user = form.save()
            group = Group.objects.get(name='Member')
            user.groups.add(group)
            return redirect('signup_done')
    else:
        form = CreateUser(initial={'email':signup.member.email})
    return render(request, 'farm_site/signup_success.html', {'signup': signup, 'form': form})

def signup_done(request):
    return render(request, 'farm_site/signup_done.html', {})


# csa member views
def csa_member_info(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    return render(request, 'farm_site/csa_member_info.html', {'member': member})

# farmers views
def dashboard(request):
    return render(request, 'farm_site/dashboard.html', {})

def members(request):
    current_signups = Signup.objects.filter(Q(season__current_season=True), Q(paid=True)).order_by("member__last_name")
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
    current_year = Season.objects.get(current_season=True).year
    locations = Location.objects.filter(current=True).order_by("name")
    return render(request, 'farm_site/locations.html', {'locations': locations, 'current_year': current_year})

def signups(request):
    signups = Signup.objects.all
    return render(request, 'farm_site/signups.html', {'signups': signups})

def newsletter(request):
    return render(request, 'farm_site/newsletter.html', {})

def active_signups(request):
    SignupPaidFormSet = modelformset_factory(Signup, form = SignupPaid)
    active = Signup.objects.filter(Q(season__current_season=True), Q(paid=False))
    print("HELLO")
    if request.method == "POST":
        formset = SignupPaidFormSet(request.POST)
        print("method = Post")

        if (formset.is_valid()):
            for form in formset:
                if form.is_valid() and not form.empty_permitted:
                    print("*****Form****")
                    print(form.cleaned_data["paid"])
                    if form.cleaned_data["paid"]:
                        print("*****Checked*****")
                        print(form.cleaned_data["id"])
                        signup = get_object_or_404(Signup, pk=form.instance.pk)
                        signup.paid = True
                        signup.save()


    #once paid signups have been processed, clear the form and re-render page
    #include a message?
    formset = SignupPaidFormSet(queryset=active)
    signups = zip(active,formset)
    return render(request, 'farm_site/active_signups.html', {'signups': signups, 'formset': formset})
