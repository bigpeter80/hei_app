from django.db import models
from django.conf import settings
from django.utils import timezone

class ClienteQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(eliminado=False)

class ClienteManager(models.Manager):
    def get_queryset(self):
        return ClienteQuerySet(self.model, using=self._db).activos()
    
class Cliente(models.Model):
    dni = models.CharField(max_length=20, unique=True, error_messages={'unique': "Ya existe un cliente con este DNI."})
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True, error_messages={'unique': "Ya existe un cliente con este email."})

    eliminado = models.BooleanField(default=False)
    modificado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='clientes_modificados'
    )
    fecha_modificacion = models.DateTimeField(auto_now=True)

    objects = ClienteManager()  # Por defecto, solo clientes no eliminados
    all_objects = models.Manager()  # Para acceder a todos, incluso los eliminados

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni}"
