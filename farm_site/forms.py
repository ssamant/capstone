from django import forms
from .models import Signup, Member, Location



class CreateMember(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'phone', 'street_address', 'city', 'zipcode', 'state')


class CreateSignup(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('box', 'eggs', 'location', 'payment')
