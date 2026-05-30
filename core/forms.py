from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Injeta o visual do Bootstrap em todos os campos gerados
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control mb-2'