from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UploadPDFForm(forms.Form):
    file = forms.FileField(label='Seleccionar PDF')

    def clean_file(self):
        f = self.cleaned_data['file']
        content_type = f.content_type
        name = f.name.lower()
        if content_type != 'application/pdf' and not name.endswith('.pdf'):
            raise forms.ValidationError('El archivo debe ser un PDF.')
        return f


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
