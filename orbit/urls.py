from django.urls import path
from . import views

app_name = 'orbits'

urlpatterns = [
    path('', views.orbit_list, name='orbit_list'),
    path('create/', views.orbit_create, name='orbit_create'),
    path('<slug:slug>/', views.orbit_detail, name='orbit_detail'),
    path('<slug:slug>/edit/', views.orbit_update, name='orbit_update'),
    path('<slug:slug>/delete/', views.orbit_delete, name='orbit_delete'),
    path('<slug:slug>/activate/', views.orbit_activate, name='orbit_activate'),
    path('<slug:slug>/deactivate/', views.orbit_deactivate, name='orbit_deactivate'),
    path('<slug:slug>/archive/', views.orbit_archive, name='orbit_archive'),
]
