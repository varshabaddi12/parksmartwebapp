from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/<int:slot_id>/', views.booking, name='booking'),
    path('ticket/<int:booking_id>/', views.ticket, name='ticket'),
]