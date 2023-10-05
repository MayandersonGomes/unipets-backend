from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'cpf_cnpj', 'birthday', 'email', 'password']

