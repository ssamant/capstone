from django import forms
from django.forms import ModelForm, Textarea, ModelChoiceField
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

class EditLocation(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('location',)

class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class SignupPaid(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('paid',)
        # widgets = {
        #     'member': forms.widgets.Select(attrs={'readonly': True, 'disabled':True}, to_field_name="first_name"),
        # }

        # name = forms.TextInput(attrs={'size': 10, 'title': 'Your name',})

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
