from django.shortcuts import render, render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from .models import Member, Location, Signup, Season
from .forms import CreateMember, CreateSignup, CreateUser, SignupPaid, EditLocation, ContactForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
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

def contact(request):
    return render(request, 'farm_site/contact.html', {})

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


@login_required(redirect_field_name='returning_member')
def signup_returning_member(request):
    member = Member.objects.get(id=request.user.member_id)
    if request.method == 'POST':
        form = CreateMember(request.POST, instance=member)
        if form.is_valid():
            member = form.save()
            request.session['member_id'] = member.id
            return redirect('signup_csa')
    else:
        form = CreateMember(instance=member)
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
    if request.user.is_authenticated:
        return render(request, 'farm_site/signup_success.html', {'signup': signup })
    else:
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
                request.session['user_email'] = user.email
                return redirect('signup_done')
        else:
            form = CreateUser(initial={'email':signup.member.email})
    return render(request, 'farm_site/signup_success.html', {'signup': signup, 'form': form})

def signup_done(request):
    email = request.session['user_email']
    return render(request, 'farm_site/signup_done.html', {'email' : email})



@login_required(redirect_field_name='csa')
def csa_member_info(request, member_id):
    if str(request.user.member_id) == member_id:
        member = get_object_or_404(Member, pk=member_id)
        return render(request, 'farm_site/csa_member_info.html', {'member': member})
    else:
        messages.warning(request, 'Sorry: you are not authorized to view that page')
        return redirect('index')

def csa_member_edit(request, member_id):
    if str(request.user.member_id) == member_id:
        member = get_object_or_404(Member, pk=member_id)
        if request.method == "POST":
            form = CreateMember(request.POST, instance=member)
            print(form)
            if form.is_valid():
                member = form.save()
                messages.success(request, 'Your member information has been updated')
                return redirect('farm_site/csa_member_info.html')
        else:
            form = CreateMember(instance=member)
            return render(request, 'farm_site/csa_member_edit.html', {'form': form})
    else:
        messages.warning(request, 'Sorry: you are not authorized to view that page')
        return redirect('index')

def edit_location(request, member_id):
    if str(request.user.member_id) == member_id:
        member = get_object_or_404(Member, pk=member_id)
        signup = member.current_signup()
        if request.method == "POST":
            form = EditLocation(request.POST, instance=signup)
            if form.is_valid():
                print(form.cleaned_data["location"])
                signup.location = Location.objects.get(name=form.cleaned_data["location"])
                signup.save()
                messages.success(request, 'Your pickup location has been updated')
                return redirect('csa_member_info', member_id=member_id)
        else:
            form = EditLocation(instance=signup)
            return render(request, 'farm_site/edit_location.html', { 'form' : form })
    else:
        messages.warning(request, 'Sorry: you are not authorized to view that page')
        return redirect('index')

# farmers views
def is_farmer(user):
    return user.groups.filter(name='Farmer').exists()

@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
def dashboard(request):
    return render(request, 'farm_site/dashboard.html', {})

@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
def members(request):
    current_signups = Signup.objects.filter(Q(season__current_season=True), Q(paid=True)).order_by("member__last_name")
    current_year = Season.objects.get(current_season=True).year

    return render(request, 'farm_site/members.html', {'signups': current_signups, 'current_year': current_year})

@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
def member_info(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    signups = member.signup_set.all()
    current_signup = member.current_signup

    return render(request, 'farm_site/member_info.html', { 'member': member, 'signups': signups, 'current_signup': current_signup })

@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
def locations(request):
    current_year = Season.objects.get(current_season=True).year
    locations = Location.objects.filter(current=True).order_by("name")
    return render(request, 'farm_site/locations.html', {'locations': locations, 'current_year': current_year})


@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
def newsletter(request):
    return render(request, 'farm_site/newsletter.html', {})

@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
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
                        formset = SignupPaidFormSet(queryset=active)
                        signups = zip(active,formset)
                        messages.success(request, 'Signups marked as paid')
                        return render(request, 'farm_site/active_signups.html', {'signups': signups, 'formset': formset})


    #once paid signups have been processed, clear the form and re-render page
    #include a message?
    formset = SignupPaidFormSet(queryset=active)
    signups = zip(active,formset)
    return render(request, 'farm_site/active_signups.html', {'signups': signups, 'formset': formset})

@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
def all_seasons(request):
    signups = Signup.objects.all()
    seasons = Season.objects.all()
    locations = Location.objects.all()
    return render(request, 'farm_site/all_seasons.html', {'signups': signups, 'seasons': seasons, 'locations':locations})


@login_required(redirect_field_name='index')
@user_passes_test(is_farmer, login_url='index')
def email(request):
    return render(request, 'farm_site/email.html', {})
