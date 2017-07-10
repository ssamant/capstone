from django import forms

from .models import Signup
from .models import Member

class SignupForm(forms.ModelForm):

    class Meta:
        model = Signup
        fields = ('box', 'eggs', 'member', 'location')
