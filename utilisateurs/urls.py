from django.urls import path
from .views import *
from django.contrib import admin
from django.urls import path, include 
from django.views.generic import TemplateView

app_name = ""

urlpatterns = [
	path('', accueil, name="accueil"),
    path('about/', apropos, name="about"),
	path('register', register, name="register"),
	path('login', user_login, name="login"),
	path('logout', user_logout, name="logout"),
    path('/myprofil', myprofil, name="myprofil"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]

#path('bibliotheques', bibliotheques, name="bibliotheques"),