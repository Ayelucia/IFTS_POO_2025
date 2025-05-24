from django.db import models

# herencia
class Animal(models.Model):
    nombre = models.CharField(max_length=100)

    def descripcion(self):
        return f"{self.nombre} es un perro."

    class Meta:
        abstract = True

# polimorfismo 
class PerroAdulto(Animal):
    raza = models.CharField(max_length=100)

    def descripcion(self):
        return f"{self.nombre} es un perro adulto de raza {self.raza}."

    def __str__(self):
        return f"{self.nombre} (Adulto)"

class PerroJoven(Animal):
    raza = models.CharField(max_length=100)

    def descripcion(self):
        return f"{self.nombre} es un perro joven de raza {self.raza}."

    def __str__(self):
        return f"{self.nombre} (Joven)"


class Perro(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('reservado', 'Reservado'),
        ('adoptado', 'Adoptado'),
    ]

    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField()
    tamaño = models.CharField(max_length=50)
    peso = models.FloatField()
    estado_salud = models.CharField(max_length=100)
    vacunado = models.BooleanField(default=False)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='disponible')
    temperamento = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.save()

    def __str__(self):
        return f"{self.nombre} (ID: {self.id})"

# composición/(historial de perros adoptados)
class UsuarioAdoptante(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    preferencia_raza = models.CharField(max_length=100, blank=True)
    preferencia_tamaño = models.CharField(max_length=50, blank=True)
    preferencia_edad = models.IntegerField(null=True, blank=True)
    historial_adopciones = models.ManyToManyField(Perro, blank=True)

    def __str__(self):
        return self.nombre
