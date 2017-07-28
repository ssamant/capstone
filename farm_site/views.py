from django.shortcuts import render, render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from .models import Member, Location, Signup, Season, User
from .forms import CreateMember, CreateSignup, CreateUser, SignupPaid, EditLocation, ContactForm
from .tables import SignupTable
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import modelformset_factory
import logging
from django.conf import settings

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

def find_us(request):
    key = settings.GOOGLE_MAPS_KEY
    print(key)
    return render(request, 'farm_site/find_us.html', {'key':key})

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


@login_required
# @login_required(redirect_field_name='returning_member')
def signup_returning_member(request):
    member = Member.objects.get(id=request.user.member_id)
    if member.signup_set.filter(season__current_season=True).exists():
        #check if user has a signup for this season
        return redirect('signup_error')
    else:
        form = CreateMember(instance=member)
        return render(request, 'farm_site/signup_member.html', {'form': form})


def signup_csa(request):
    key = settings.GOOGLE_MAPS_KEY
    member = get_object_or_404(Member, pk=request.session['member_id'])
    if request.method == "POST":
        form = CreateSignup(request.POST)
        if form.is_valid():
            signup = form.save(commit=False)
            signup.member = member
            signup.season = Season.objects.get(current_season=True)
            signup.created_date = timezone.now()
            signup.save()
            request.session['signup_id'] = signup.id
            return redirect('signup_success')
    else:
        form = CreateSignup()
    return render(request, 'farm_site/signup_csa.html', {'form': form, 'key': key})

def signup_error(request):
    signup = request.user.member.signup_set.get(season__current_season=True)
    return render(request, 'farm_site/signup_error.html', {'signup': signup})

def signup_success(request):
    #need to get member object to put in User
    signup = get_object_or_404(Signup, pk=request.session['signup_id'])
    total = 0
    if (signup.box == "regular"):
        total += 570
    else:
        total += 715
    if (signup.eggs == "dozen"):
        total+= 180
    elif (signup.eggs == "half-dozen"):
        total+= 105
    if request.user.is_authenticated:
        return render(request, 'farm_site/signup_success.html', {'signup': signup,'total' : total })
    else:
        if request.method == "POST":
            form = CreateUser(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                member = get_object_or_404(Member, pk=request.session['member_id'])
                user = User.objects.create(email=email, member=member )
                if password:
                    user.set_password(password)
                else:
                    user.set_unusable_password()
                user.save()
                group = Group.objects.get(name='Member')
                user.groups.add(group)
                request.session['user_email'] = user.email
                return redirect('signup_done')
        else:
            form = CreateUser(initial={'email':signup.member.email})
    return render(request, 'farm_site/signup_success.html', {'signup': signup, 'form': form, 'total': total})

def signup_done(request):
    email = request.session['user_email']
    return render(request, 'farm_site/signup_done.html', {'email' : email})



@login_required
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
                return redirect('csa_member_info', member_id=member.id)
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

@login_required
@user_passes_test(is_farmer, login_url='index')
def dashboard(request):
    now = timezone.now()
    earlier = now - timezone.timedelta(days=3)
    new_signups = Signup.objects.filter(created_date__range=(earlier,now))
    new_signups.order_by('-created_date')
    return render(request, 'farm_site/dashboard.html', {'new_signups': new_signups})

@login_required
@user_passes_test(is_farmer, login_url='index')
def members(request):
    current_signups = Signup.objects.filter(Q(season__current_season=True), Q(paid=True)).order_by("member__last_name")
    current_year = Season.objects.get(current_season=True).year

    return render(request, 'farm_site/members.html', {'signups': current_signups, 'current_year': current_year})

@login_required
@user_passes_test(is_farmer, login_url='index')
def member_info(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    signups = member.signup_set.all()
    current_signup = member.current_signup

    return render(request, 'farm_site/member_info.html', { 'member': member, 'signups': signups, 'current_signup': current_signup })

@login_required
@user_passes_test(is_farmer, login_url='index')
def locations(request):
    current_year = Season.objects.get(current_season=True).year
    locations = Location.objects.filter(current=True).order_by("name")
    return render(request, 'farm_site/locations.html', {'locations': locations, 'current_year': current_year})


@login_required
@user_passes_test(is_farmer, login_url='index')
def newsletter(request):
    return render(request, 'farm_site/newsletter.html', {})

@login_required
@user_passes_test(is_farmer, login_url='index')
def active_signups(request):
    SignupPaidFormSet = modelformset_factory(Signup, form = SignupPaid)
    active = Signup.objects.filter(Q(season__current_season=True), Q(paid=False))
    print("HELLO")
    if request.method == "POST":
        formset = SignupPaidFormSet(request.POST)
        print("method = Post")

        if (formset.is_valid()):
            print(formset.as_table())
            for form in formset:
                print(form.cleaned_data)
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

@login_required
@user_passes_test(is_farmer, login_url='index')
def all_seasons(request, season_id, location_id, member_id):
    print("*****")
    print(season_id, location_id, member_id)
    print((season_id=="0" and location_id=="0" and member_id=="0"))
    if (season_id=="0" and location_id=="0" and member_id=="0"):
        signups = Signup.objects.all().order_by('season', 'location', 'member__last_name')
        selection = "All"
    elif location_id=="0" and member_id=="0":
        signups = Signup.objects.filter(season_id=season_id).order_by('location', 'member__last_name')
        selection = Season.objects.get(id=season_id)
    elif member_id=="0":
        signups = Signup.objects.filter(location_id=location_id).order_by('season', 'member__last_name')
        selection = Location.objects.get(id=location_id)
    else:
        signups = Signup.objects.filter(member_id=member_id).order_by('season')
        selection = Member.objects.get(id=member_id)

    seasons = Season.objects.all()
    locations = Location.objects.all().order_by('name')
    members = Member.objects.all().order_by('last_name')
    return render(request, 'farm_site/all_seasons.html', {'signups': signups, 'seasons': seasons, 'locations':locations, 'members':members, 'selection':selection})


@login_required
@user_passes_test(is_farmer, login_url='index')
def email(request):
    return render(request, 'farm_site/email.html', {})
