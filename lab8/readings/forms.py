from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TemperatureReading, UserProfile


class TemperatureReadingForm(forms.ModelForm):
    class Meta:
        model = TemperatureReading
        fields = ['sensor', 'temperature', 'timestamp', 'note']
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, label='Роль')
    organization = forms.CharField(max_length=200, required=False, label='Организация')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                organization=self.cleaned_data.get('organization', ''),
                phone=self.cleaned_data.get('phone', '')
            )
        return user