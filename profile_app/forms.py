from django import forms
from profile_app.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'gender', 'age']

        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female')], attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
        }

