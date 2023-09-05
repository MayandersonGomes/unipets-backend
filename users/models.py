from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    name = models.CharField('Nome', max_length=30)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=14, unique=True)
    birthday = models.DateField('Data de nascimento')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'cpf_cnpj', 'birthday']

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
