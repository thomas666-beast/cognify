from django import forms
from .models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['nickname', 'firstname', 'lastname', 'position', 'email', 'bio', 'is_active']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unique nickname...'
            }),
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name...'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name...'
            }),
            'position': forms.Select(attrs={
                'class': 'form-select'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address...'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself...',
                'rows': 4
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        help_texts = {
            'nickname': 'Required. 3-120 characters. Letters, numbers, and @/./+/-/_ only.',
            'email': 'Optional. Must be unique if provided.',
        }

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname'].strip()
        if Participant.objects.filter(nickname=nickname).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A participant with this nickname already exists.")
        return nickname

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and Participant.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A participant with this email already exists.")
        return email
