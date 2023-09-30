from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import UserProfileSerializer
from .filters import FilterUserProfileViewSet
from rest_framework.authtoken.models import Token


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [FilterUserProfileViewSet]

    def get_permissions(self):
        if self.action in ['create', 'auth']:
            return [AllowAny()]
        return super(UserProfileViewSet, self).get_permissions()

    def create(self, request):
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
    
    @action(methods=['POST'], detail=False)
    def auth(self, request):
        data = request.data
        try:
            user = authenticate(request, username=data['email'], password=data['password'])
            if user and user.is_active:
                token = Token.objects.get_or_create(user=user)
                serializer = self.serializer_class(user)
                return Response({'message': 'Login realizado com sucesso!', 'token': token[0].key, 'user': serializer.data}, status=status.HTTP_200_OK)
            if UserProfile.objects.filter(email=data['email'], is_active=False).exists():
                return Response({'message': 'Por favor, confirme seu email para ativar seu usuário!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': 'Email e/ou senha inválidos!'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            return Response({'message': 'Erro ao realizar login!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)