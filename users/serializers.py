from rest_framework.serializers import ModelSerializer
from .models import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'cpf_cnpj', 'birthday', 'email']
