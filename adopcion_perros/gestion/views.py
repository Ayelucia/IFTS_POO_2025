from django.shortcuts import render, redirect, get_object_or_404
#from .models import PerroAdulto, PerroJoven
from django.db.models import Q
from .forms import PerroForm, UsuarioForm
from .models import Perro, UsuarioAdoptante
from .sistema import SistemaAdopcion

sistema = SistemaAdopcion()

def inicio(request):
    return render(request, 'gestion/inicio.html')

def listar_perros(request):
    estado = request.GET.get('estado')
    dni = request.GET.get('dni')

    perros = Perro.objects.all()

    if estado:
        perros = perros.filter(estado=estado)

    if dni:
        try:
            usuario = UsuarioAdoptante.objects.get(dni=dni)
            perros = usuario.historial_adopciones.all()
        except UsuarioAdoptante.DoesNotExist:
            perros = Perro.objects.none()

    return render(request, 'gestion/listado_perros.html', {'perros': perros})

def registrar_perro(request):
    if request.method == 'POST':
        form = PerroForm(request.POST)
        if form.is_valid():
            sistema.cargar_perro(form)
            return redirect('listar_perros')
    else:
        form = PerroForm()
    return render(request, 'gestion/registro_perro.html', {'form': form})

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            sistema.registrar_usuario(form)
            return redirect('inicio')
    else:
        form = UsuarioForm()
    return render(request, 'gestion/registro_usuario.html', {'form': form})

def postular_adopcion(request, perro_id):
    mensaje = sistema.postular_perro(perro_id)
    return render(request, 'gestion/mensaje.html', {'mensaje': mensaje})

def confirmar_adopcion(request, perro_id):
    mensaje = sistema.confirmar_adopcion(perro_id)
    return render(request, 'gestion/mensaje.html', {'mensaje': mensaje})

def sugerir_perros(request):
    usuarios = UsuarioAdoptante.objects.all().order_by('nombre')  #todos los usuarios
    usuario_id = request.GET.get('usuario_id')

    if usuario_id:
        usuario = get_object_or_404(UsuarioAdoptante, id=usuario_id)
    else:
        usuario = UsuarioAdoptante.objects.last()  #último usuario 

    if not usuario:
        return render(request, 'gestion/mensaje.html', {'mensaje': 'No hay usuarios registrados.'})

    edad_preferida = usuario.preferencia_edad
    if edad_preferida is not None:
        rango_min = max(edad_preferida - 3, 0)
        rango_max = edad_preferida + 3

        sugerencias = Perro.objects.filter(
            estado='disponible',
            edad__gte=rango_min,
            edad__lte=rango_max
        ).filter(
            Q(raza__iexact=usuario.preferencia_raza) |
            Q(tamaño__iexact=usuario.preferencia_tamaño)
        )
    else:
        sugerencias = Perro.objects.filter(
            estado='disponible'
        ).filter(
            Q(raza__iexact=usuario.preferencia_raza) |
            Q(tamaño__iexact=usuario.preferencia_tamaño)
        )

    context = {
        'usuario': usuario,
        'usuarios': usuarios,
        'sugerencias': sugerencias,
    }
    return render(request, 'gestion/sugerencias.html', context)