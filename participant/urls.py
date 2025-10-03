from django.urls import path
from . import views

app_name = 'participants'

urlpatterns = [
    path('', views.participant_list, name='participant_list'),
    path('create/', views.participant_create, name='participant_create'),
    path('<uuid:pk>/', views.participant_detail, name='participant_detail'),
    path('<uuid:pk>/edit/', views.participant_update, name='participant_update'),
    path('<uuid:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('<uuid:pk>/activate/', views.participant_activate, name='participant_activate'),
    path('<uuid:pk>/deactivate/', views.participant_deactivate, name='participant_deactivate'),
]
