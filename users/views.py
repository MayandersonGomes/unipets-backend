from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from .models import UserProfile
from .serializers import UserProfileSerializer
from .filters import FilterUserProfileViewSet


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [FilterUserProfileViewSet]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super(UserProfileViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            with transaction.atomic():
                username = data['username']
                email = data['email']
                cpf_cnpj = data['cpf_cnpj']

                if self.queryset.filter(username=username).exists():
                    return Response(
                        {'message': 'Já existe um usuário com o username informado!'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif self.queryset.filter(email=email).exists():
                    return Response(
                        {'message': 'Já existe um usuário com o email informado!'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                elif self.queryset.filter(cpf_cnpj=cpf_cnpj).exists():
                    return Response(
                        {'message': 'Já existe um usuário com o cpj/cnpj informado!'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                user = UserProfile.objects.create(
                    username=username, name=data['name'], birthday=data['birthday'],
                    email=email, cpf_cnpj=cpf_cnpj, is_active=False
                )
                user.set_password(data['password'])
                user.save()

                return Response(
                    {
                        'message': 'Cadastro concluído com sucesso. Por favor, verifique seu email para ativar sua conta!'
                    }, status=status.HTTP_201_CREATED
                )

        except Exception:
            return Response({'message': 'Houve um erro ao finalizar seu cadastro!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
