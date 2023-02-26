from django.shortcuts import redirect, render
from AppCoder.models import Curso,Profesor
from .forms import CursoFormulario, ProfesorFormulario, MyUserCreationForm,UserEditForm,AvatarFormulario
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
#Importaciones para el login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from  django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
#Importaciones para el mixins
from django.contrib.auth.mixins import LoginRequiredMixin
#Importaciones para los decoradores 
from django.contrib.auth.decorators import login_required




# Create your views here. 


#CRUD DE CURSO
class CursoList(LoginRequiredMixin,ListView):
    model = Curso
    template_name = 'AppCoder/cursos-list.html'

class CursoDetalle(DetailView):
    model = Curso
    template_name = 'AppCoder/curso-detalle.html'

class CursoCreate(LoginRequiredMixin, CreateView):
    model = Curso
    template_name = 'AppCoder/curso-nuevo.html'
    success_url = reverse_lazy('inicio')
    fields = ['nombre','camada']

class CursoUpdate(LoginRequiredMixin, UpdateView):
    model = Curso
    template_name = 'AppCoder/curso-nuevo.html'
    success_url = reverse_lazy('inicio')
    fields = ['nombre','camada']

class CursoDelete(LoginRequiredMixin,DeleteView):
    model = Curso
    template_name = 'AppCoder/curso-eliminar.html'
    success_url = reverse_lazy('inicio')


def inicio(request):
    return render(request,'AppCoder/inicio.html')

def cursos(request):
    mis_cursos = Curso.objects.all()

    if request.method == "POST":
        #Aqui recibiremos toda la informacion enviada mediante el formulario
        mi_formulario = CursoFormulario(request.POST)

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            curso = Curso(nombre = informacion['nombre'],camada=informacion['camada'])
            curso.save()

            nuevo_curso = {'nombre':informacion['nombre'],'camada':informacion['camada']}

            return render(request, 'AppCoder/cursos.html',{'formulario_curso': mi_formulario,
                                                           'nuevo_curso':nuevo_curso,
                                                           'mis_cursos':mis_cursos})

    else:
        mi_formulario = CursoFormulario()

    return render(request, 'AppCoder/cursos.html',{'formulario_curso':mi_formulario, 'mis_cursos':mis_cursos})

def profesores(request):
    return render(request,'AppCoder/profesores.html')

@login_required
def estudiantes(request):
    return render(request,'AppCoder/estudiantes.html')

def entregables(request):
    return render(request,'AppCoder/entregables.html')

def curso_formulario(request):
    
    # if request.method == "POST":
    #     curso = Curso(nombre=request.POST['curso'],camada=request.POST['camada'])
    #     curso.save()
    #     return redirect('inicio')
    
    #Aqui recibiremos toda la informacion enviada mediante el formulario
    if request.method == 'POST':
        mi_formulario = CursoFormulario(request.POST)
        
        #Validamos que los datos correspondan a los esperados
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            curso=Curso(nombre=informacion['nombre'],camada=informacion['camada'])
            curso.save()
            return redirect('inicio')
    else:
        #Inicializamos un formulario vacio para construir el HTML
        mi_formulario = CursoFormulario()

    return render(request, 'AppCoder/curso-formulario.html',{'formulario_curso': mi_formulario})

def profesor_formulario(request):
    
    #Aqui recibiremos toda la informacion enviada mediante el formulario
    if request.method == 'POST':
        mi_formulario = ProfesorFormulario(request.POST)
        
        #Validamos que los datos correspondan a los esperados
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            profesor=Profesor(
                nombre=informacion['nombre'],
                apellido=informacion['apellido'],
                email=informacion['email'],
                profesion=informacion['profesion'],
                )
            profesor.save()
            return redirect('inicio')
    else:
        #Inicializamos un formulario vacio para construir el HTML
        mi_formulario = ProfesorFormulario()
        
    return render(request, 'AppCoder/profesor-formulario.html',{'formulario_profesor': mi_formulario})

def busqueda_camada(request):
    return render(request, 'AppCoder/busqueda-camada.html')

def buscar(request):
    if request.GET["camada"]:
        camada = request.GET["camada"]
        cursos = Curso.objects.filter(camada__icontains=camada)

        return render(request, 'AppCoder/resultado-busqueda.html',{'cursos': cursos, 'camada':camada})
    
    else:
        respuesta = f'No se encontro la camada'
          
    # return HttpResponse(respuesta)
    return render(request, "AppCoder/resultado-busqueda.html", {"respuesta": respuesta})

def leer_profesores(request):
    profesores = Profesor.objects.all()

    contexto = {'profesores':profesores}

    return render(request, 'AppCoder/leer-profesores.html',contexto)

def eliminar_profesor(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)
    profesor.delete()

    #Vuelvo al menu de profesores
    profesores = Profesor.objects.all()
    contexto = {'profesores':profesores}

    return render(request,'AppCoder/leer-profesores.html',contexto)

def editar_profesor(request,profesor_id):

    #Guarda al objeto profesor con el id pasado por paramertro y lo guarda en la variable profesor
    profesor = Profesor.objects.get(id=profesor_id)
    
    if request.method == "POST":
        mi_formulario = ProfesorFormulario(request.POST)

        #Validamos que los datos correspondan a los esperados
        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            
            profesor.nombre=informacion['nombre']
            profesor.apellido=informacion['apellido']
            profesor.email=informacion['email']
            profesor.profesion=informacion['profesion']
                
            #Actualiza el profesor con los nuevos datos
            profesor.save()

            profesores=Profesor.objects.all()
            contexto = {'profesores': profesores}

            #Regresa a la vista leer-profesores
            return render(request, 'AppCoder/leer-profesores.html',contexto)

    else:
        mi_formulario = ProfesorFormulario(initial={'nombre':profesor.nombre,
                                                    'apellido':profesor.apellido,
                                                    'email':profesor.email,
                                                    'profesion':profesor.profesion})

        profesores=Profesor.objects.all()
        contexto={"mi_formulario":mi_formulario,"profesor_id":profesor_id,"profesores":profesores}
            
    return render(request,'AppCoder/leer-profesores.html', contexto)


#Vistas del login
def login_request(request):
    form = AuthenticationForm()

    if request.method == "POST":
        #Creacion del formulario con los datos resividos desde la vista
        form = AuthenticationForm(request, data=request.POST)

        #Validar si los datos del formulario sean validaos
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contraseña = form.cleaned_data.get('password')

            user = authenticate(username = usuario, password=contraseña)

            if user is not None:
                login(request, user)
                contexto = {'mensaje': f'Bienvenido {usuario}'}
                return render(request, 'AppCoder/inicio.html', contexto)
            else:
                contexto = {'mensaje': f'El usuario no existe','form': form}
                return render(request, 'AppCoder/login.html', contexto)
            
        else:
            contexto = {'mensaje': f'Los datos del formulario son erroneos','form': form}
            return render(request, 'AppCoder/login.html', contexto)
        
    contexto = {'form':form}
    return render(request, 'AppCoder/login.html',contexto)

def register(request):
    
    if request.method == "POST":
        
        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('login')
    else:
        form = MyUserCreationForm()
    return render(request, 'AppCoder/registro.html', {'form': form})

# def registro(request):
#     if request.method == 'POST':
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.save()
#             return redirect('login')
#     else:
#         form = MyUserCreationForm()
#     return render(request, 'AppCoder/registro.html', {'form': form})

@login_required
def editar_perfil(request):
    usuario = User.objects.get(username=request.user)

    if request.method == 'POST':
        mi_formulario = UserEditForm(request.POST)

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data

            usuario.username = informacion["username"]
            usuario.email = informacion["email"]
            # usuario.password = informacion["password"]
            # usuario.password2 = informacion["password2"]
            usuario.last_name = informacion["last_name"]
            usuario.first_name = informacion["first_name"]

            usuario.save()
            return redirect('/')

    else:        
        mi_formulario = UserEditForm(initial={"username":usuario.username,
                                            "email":usuario.email,
                                            "last_name":usuario.last_name,
                                            "first_name":usuario.first_name})
        contexto = {'mi_formulario': mi_formulario}
        return render(request,'AppCoder/editar-perfil.html',contexto)

@login_required
def agregar_avatar(request):
    avatar = request.user.avatar
    mi_formulario = AvatarFormulario(instance=avatar)

    if request.method == 'POST':
        mi_formulario = AvatarFormulario(request.POST, request.FILES, instance=avatar)
        if mi_formulario.is_valid():
            mi_formulario.save()
            return redirect('/')
    else:
        return render(request, 'AppCoder/agregar-avatar.html',{'mi_formulario':mi_formulario})