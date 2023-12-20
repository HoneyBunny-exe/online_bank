"""
URL configuration for online_bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main_app.views import RegistrationAPIView, AuthorizationAPIView, UpdateJWTAPIView, ChangeAuthAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("main_app.api_urls")),
    path('auth/registration/', RegistrationAPIView.as_view()),
    path('auth/', AuthorizationAPIView.as_view()),
    path('auth/update_api_tokens/', UpdateJWTAPIView.as_view()),
    path('auth/change_auth/', ChangeAuthAPIView.as_view()),
]

admin.site.site_header = 'Wordskills Bank'
