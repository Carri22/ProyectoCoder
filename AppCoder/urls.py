from django.urls import path
from .views import * 

urlpatterns = [
    path('',inicio), #Esta es nuestra primer vista
    path('cursos/',cursos),
    path('profesores/',profesores),
    path('estudiantes/',estudiantes),
    path('entregables/',entregables),

]