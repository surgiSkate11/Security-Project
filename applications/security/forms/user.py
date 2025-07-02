from django import forms
from applications.security.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
             'is_active', 'is_staff', 'is_superuser'
        ]
        widgets = {
            'icon': forms.TextInput(attrs={'placeholder': 'fa-solid fa-user'}),
            'order': forms.NumberInput(attrs={'min': 0}),
        }