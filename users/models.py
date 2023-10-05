import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=14, unique=True)
    birthday = models.DateField('Data de nascimento')
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'cpf_cnpj', 'birthday', 'password']

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
