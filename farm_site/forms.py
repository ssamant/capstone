from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Signup, Member, Location, User



class CreateMember(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('email', 'first_name', 'last_name',  'phone', 'street_address', 'city', 'state', 'zipcode')


class CreateSignup(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('box', 'eggs', 'location', 'payment')


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
