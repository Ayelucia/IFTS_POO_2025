from .models import Perro, UsuarioAdoptante
from django.db.models import Q

class SistemaAdopcion:
    def cargar_perro(self, datos_form):
        perro = datos_form.save()
        return perro

    def eliminar_perro(self, perro_id):
        try:
            Perro.objects.get(id=perro_id).delete()
            return True
        except Perro.DoesNotExist:
            return False

    def registrar_usuario(self, datos_form):
        usuario = datos_form.save()
        return usuario

    def postular_perro(self, perro_id):
        try:
            perro = Perro.objects.get(id=perro_id)
            if perro.estado == 'disponible':
                perro.estado = 'reservado'
                perro.save()
                return f"Perro {perro.nombre} reservado correctamente."
            else:
                return f"El perro {perro.nombre} no está disponible."
        except Perro.DoesNotExist:
            return "Perro no encontrado."

    def confirmar_adopcion(self, perro_id):
        try:
            perro = Perro.objects.get(id=perro_id)
            if perro.estado == 'reservado':
                perro.estado = 'adoptado'
                perro.save()
                usuario = UsuarioAdoptante.objects.last()
                if usuario:
                    usuario.historial_adopciones.add(perro)
                    return f"{usuario.nombre} adoptó a {perro.nombre}."
                return f"{perro.nombre} adoptado (sin usuario)."
            return "No se puede confirmar adopción."
        except Perro.DoesNotExist:
            return "Perro no encontrado."

    def sugerir_perros(self):
        usuario = UsuarioAdoptante.objects.last()
        if not usuario:
            return [], None
        sugerencias = Perro.objects.filter(estado='disponible').filter(
            Q(raza__iexact=usuario.preferencia_raza) |
            Q(tamaño__iexact=usuario.preferencia_tamaño)
        )
        if usuario.preferencia_edad:
            sugerencias = sugerencias.filter(edad__lte=usuario.preferencia_edad)
        return sugerencias, usuario

    def listar_por_estado(self, estado):
        return Perro.objects.filter(estado=estado)

    def listar_por_usuario(self, dni):
        try:
            usuario = UsuarioAdoptante.objects.get(dni=dni)
            return usuario.historial_adopciones.all()
        except UsuarioAdoptante.DoesNotExist:
            return []
