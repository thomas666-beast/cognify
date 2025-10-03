from django import forms
from .models import Orbit

class OrbitForm(forms.ModelForm):
    class Meta:
        model = Orbit
        fields = ['name', 'description', 'status', 'order', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter orbit name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter orbit description...',
                'rows': 4
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'height: 45px;'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., fa-globe, bi-orbit'
            }),
        }
        help_texts = {
            'name': 'Required. 3-100 characters. Letters, numbers, spaces, hyphens, underscores, and dots only.',
            'color': 'Click to choose a color or enter hex code manually.',
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if Orbit.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("An orbit with this name already exists.")
        return name
