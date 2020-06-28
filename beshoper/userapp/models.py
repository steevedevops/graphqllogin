from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
    documento = models.CharField(max_length=50, null=True, blank=True)
    fotoperfil = models.CharField(max_length=100, null=True, blank=True)
    fotoportada = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(blank=False, null=False, default=False, verbose_name='Verificado')
    datacriado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s - %s - %s' % (self.email, self.documento, self.fotoportada, self.datacriado)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'