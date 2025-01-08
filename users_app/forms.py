from profile_app.models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age'
        }),
        label="Age")
    
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Gender",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label="Password",
    )
     
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        label="Confirm Password",
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(list(e.messages))

        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'age', 'gender', 'password')

class UserProfileInfoForm(forms.Form):
    class Meta:
        model = Profile
        fields = ('profile_pic')
