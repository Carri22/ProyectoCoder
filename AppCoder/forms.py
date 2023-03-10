from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Avatar


class CursoFormulario(forms.Form):
    nombre = forms.CharField()
    camada = forms.IntegerField()

class ProfesorFormulario(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    email = forms.EmailField()
    profesion = forms.CharField()

#Clase para crear un formulario de registro
class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = None
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Repita la contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        help_texts = {k:'' for k in fields}
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('password2')
        if password and confirm_password and password != confirm_password:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return confirm_password
    
    


#Clase para crear un formulario de registro
class UserEditForm(forms.Form):

    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput)
    email = forms.EmailField()
    first_name=forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    # password = forms.CharField(label="Contraseña" ,widget=forms.PasswordInput)
    # password2 = forms.CharField(label="Repita la contraseña",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        help_texts = {k:'' for k in fields}

#Formulario para avatar
class AvatarFormulario(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = '__all__'
        exclude = ['user']
