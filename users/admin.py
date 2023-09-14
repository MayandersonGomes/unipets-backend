from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    fieldsets = (
        ('Informações do usuário', {'fields': ('username', 'password', 'name', 'email', 'cpf_cnpj', 'birthday')}),
        ('Tipos de usuário', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Permissões', {'fields': ('groups',)}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Criação de usuário', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'email', 'cpf_cnpj', 'birthday')}
         ),
    )
    list_display = ['name', 'cpf_cnpj', 'email']
    search_fields = ['name', 'cpf_cnpj', 'email']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
