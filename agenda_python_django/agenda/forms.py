# https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms.extras.widgets import SelectDateWidget
from .models import AddEvent


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    email = forms.EmailField(max_length=254,
        help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', )


class CreateEventForm(forms.ModelForm):
    data_intratii = forms.DateField(widget=SelectDateWidget(years=range(2000, 2020)))

    class Meta:
        model = AddEvent
        fields = ['data_intratii', 'tags',
                  'vizibilitate', 'title', 'text', ]
