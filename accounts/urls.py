from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_page, name='home_page'),

    # HOME
    path('home-register/', views.home_register, name='home_register'),
    path('home-login/', views.home_login, name='home_login'),
    path('home-dashboard/', views.home_dashboard, name='home_dashboard'),

    # DONAR
    path('donar-register/', views.donor_register, name='donar_register'),
    path('donar-login/', views.donor_login, name='donar_login'),
    path('donar-dashboard/', views.donar_dashboard, name='donar_dashboard'),

    # ⭐ THIS LINE MUST EXIST
    path('create-donation/', views.create_donation, name='create_donation'),
]