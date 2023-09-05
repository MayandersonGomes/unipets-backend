from rest_framework import routers
from users.views import UserProfileViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'users', UserProfileViewSet, basename='users')