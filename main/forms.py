from django import forms
from main.models import User, WorkSpace, Channel


class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']


class WorkSpaceForm(forms.ModelForm):
    class Meta:
        model = WorkSpace
        exclude = ('created_by', 'created_on', )


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        exclude = ('workspace', 'created_by', 'created_on', )