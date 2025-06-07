from django import forms
from .models.usuario import Profile,User
from .models.categoria_producto import Categoria
from .models.producto import Producto
from .models.inventario import Inventario
from .models.cliente import Cliente
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm

# Registro de usuarios
class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg'})
    )

    role = forms.ChoiceField(
        choices=Profile.ROLES,  # 📌 Se usa directamente del modelo
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg'})
        self.fields['password2'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # 📌 Asigna el rol seleccionado directamente al usuario
            Profile.objects.create(user=user, role=self.cleaned_data['role'])
        return user


# Perfil del usuario|
class ProfileForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white',
            'type': 'text',
            'placeholder': 'Leonardo'
        })
    )

    apellido = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white',
            'type': 'text',
            'placeholder': 'Díaz'
        })
    )

    telefono = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white',
            'type': 'tel',
            'placeholder': '3125563387'
        })
    )

    class Meta:
        model = Profile
        fields = ['nombre', 'apellido', 'telefono']






# Login de usuarios
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg', 'placeholder': '••••••••'})
        
        




# Categoria productos
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'id': 'nombre',
                'name': 'nombre',
                'placeholder': 'Ej. Laptop HP 15',
                'required': True,
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg '
                         'focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                         'dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white'
            }),
            'descripcion': forms.Textarea(attrs={
                'id': 'descripcion',
                'name': 'descripcion',
                'placeholder': 'Descripción detallada de la Categoria...',
                'required': True,
                'rows': 3,
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg '
                         'focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
                         'dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white'
            }),
        }
  
# Productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Ej. Laptop HP 15',
                'id': 'nombre',
            }),
            'categoria': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'id': 'categoria',
            }),
            'precio': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Ej. 499.99',
                'id': 'precio',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Descripción detallada del producto...',
                'id': 'descripcion',
            }),
        }
        
# Inventario
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg ' +
                         'focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 ' +
                         'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg ' +
                         'focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 ' +
                         'dark:border-gray-500 dark:placeholder-gray-400 dark:text-white',
                'placeholder': 'Ej. 10'
            }),
        }
        

# Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'nombre', 'apellido', 'correo', 'celular']