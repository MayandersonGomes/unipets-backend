from django.contrib import admin
from django.urls import path, include
from .routers import router

admin.site.site_header = 'Unipets - Administração'
admin.site.index_title = 'Administração'
admin.site.site_title = 'Unipets'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
