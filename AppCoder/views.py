from django.shortcuts import redirect, render
from AppCoder.models import Curso,Profesor
from .forms import CursoFormulario, ProfesorFormulario
from django.http import HttpResponse
# Create your views here.

def inicio(request):
    return render(request,'AppCoder/inicio.html')

def cursos(request):
    return render(request,'AppCoder/cursos.html')

def profesores(request):
    return render(request,'AppCoder/profesores.html')

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
        respuesta = f'No se encontro la camada:{request.GET["camada"]}'
          
    return HttpResponse(respuesta)