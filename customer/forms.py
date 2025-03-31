from django import forms

class LoginForm(forms.Form):
    login_input = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
