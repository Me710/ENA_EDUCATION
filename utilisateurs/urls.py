from django.urls import path
from .views import accueil, user_login, user_logout,register
from django.contrib import admin
from django.urls import path, include 
from django.views.generic import TemplateView

urlpatterns = [
	path('', accueil, name="accueil"),
	path('register', register, name="register"),
	path('login', user_login, name="login"),
	path('logout', user_logout, name="logout"),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]