from django.urls import path
from .views import * 

urlpatterns = [
    # 
    # path('cursos/',cursos, name="cursos"),
    # path('profesores/',profesores, name="profesores"),
    # path('estudiantes/',estudiantes, name="estudiantes"),
    # path('entregables/',entregables, name="entregables"),
    # path('curso-formulario/',curso_formulario,name="curso-formulario"),
    # path('profesor-formulario/',profesor_formulario,name="profesor-formulario"),
    # path('busqueda-camada/',busqueda_camada,name="busqueda-camada"),
    # path('buscar/',buscar,name="buscar"),
    # path('leer-profesores/',leer_profesores,name="leer-profesores"),
    # path('eliminar-profesor/<profesor_id>',eliminar_profesor,name="eliminar-profesor"),
    # path('editar-profesor/<profesor_id>',editar_profesor,name="editar-profesor"),

    path('',CursoList.as_view(), name="inicio"), #Esta es nuestra primer vista
    path('detalle/<pk>',CursoDetalle.as_view(),name="detalle"),
    path('nuevo/',CursoCreate.as_view(),name="nuevo"), 
    path('editar/<pk>',CursoUpdate.as_view(),name="editar"),
    path('eliminar/<pk>',CursoDelete.as_view(),name="eliminar"),

]
