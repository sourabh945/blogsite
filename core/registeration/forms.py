"""
    This files holdes the forms that we are using for the registerations and login 
"""

from django import forms

class signup_form(forms.Form):

    email = forms.EmailField(
        max_length=126,
        label='Enter your email',
        required=True
    )

    username = forms.CharField(
        max_length=126,
        label='Enter a username for you',
        required=True,
    )

    name = forms.CharField(
        max_length=126,
        label='Enter your name',
        required=True,
    )

    password = forms.CharField(
        label='Enter a password for you',
        required=True,
        widget=forms.PasswordInput,
    )

    confirmpassword = forms.CharField(
        label='Confirm your password',
        required=True,
        widget=forms.PasswordInput,
    )


class login_form(forms.Form):

    username_or_email = forms.CharField(
        max_length=126,
        label='Enter your email or username',
        required=True,
    )

    password = forms.CharField(
        label='Enter your password',
        required=True,
        widget=forms.PasswordInput,
    )
    

class verification_regen_form(forms.Form):

    email_or_username = forms.CharField(
        max_length=126,
        label='Enter your email or username',
        required=True,
    )