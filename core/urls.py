from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cdb/', views.create_drop_box, name="cdb"),
]