from django.contrib.auth.models import User
from django import forms
import re


NAME_RE = re.compile(r'^[a-zA-z]+$')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class SettingsForm(forms.Form):
    first_name = forms.CharField(label='Change first name', required=False)
    last_name = forms.CharField(label='Change last name', required=False)
    image = forms.ImageField(label='Change profile picture', required=False)

    def clean_name(self, field):
        data = self.cleaned_data.get(field)

        if data and not NAME_RE.match(data):
            raise forms.ValidationError('Name can contain only letters.')

        return data

    def clean_first_name(self):
        return self.clean_name('first_name')

    def clean_last_name(self):
        return self.clean_name('last_name')

    def clean_image(self):
        data = self.cleaned_data['image']

        if data and data._size > 5242880:
            raise forms.ValidationError('Maximum size is 5MB.')

        return data