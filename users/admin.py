from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    fieldsets = (
        ('Informações do usuário', {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'cpf_cnpj', 'birthday')}),
        ('Tipos de usuário', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Permissões', {'fields': ('groups',)}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Criação de usuário', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'cpf_cnpj', 'birthday')}
         ),
    )
    list_display = ['first_name', 'last_name', 'cpf_cnpj', 'email']
    search_fields = ['first_name', 'last_name', 'cpf_cnpj', 'email']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
