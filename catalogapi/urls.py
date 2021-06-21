from django.urls import path
from . import views

urlpatterns = [
    path('simpleapi', views.simpleapi, name='simple_api'),
    path('login', views.login, name='login_api'),
    path('borrowedbooks', views.borrowedbooks, name='borrowedbooks_api'),
]