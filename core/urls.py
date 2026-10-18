from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cdb/', views.create_drop_box, name="cdb"),
    path('rdb/', views.retrive_drop_box, name="rdb"),
    path('pin/', views.create_drop, name="create_drop"),
    path('drop/', views.retrive_drop, name="retrive_drop"),
    path('destroy/', views.destroy_drop, name="destroy_drop"),
]