from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpf_cnpj', 'email']
    search_fields = ['name', 'cpf_cnpj', 'email']
