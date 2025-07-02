from django import forms
from applications.doctor.models import Patient
import re

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'dni',
            'birth_date',
            'gender',
            'phone',
            'email',
            'address',
            'blood_type',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombres'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos'
            }),
            'dni': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cédula'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Fecha de nacimiento'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección'
            }),
            'blood_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    # Validar que la cédula tenga solo números y 10 o 13 dígitos
    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit() or len(dni) not in [10, 13]:
            raise forms.ValidationError("La cédula debe tener 10 o 13 dígitos numéricos.")
        return dni

    # Validar que el email sea único y tenga formato correcto
    def clean_email(self):
        email = self.cleaned_data['email']
        if Patient.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un paciente con este correo electrónico.")
        return email

    # Validar que el teléfono tenga solo números y al menos 7 dígitos
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^\d{7,}$', phone):
            raise forms.ValidationError("El teléfono debe tener al menos 7 dígitos numéricos.")
        return phone