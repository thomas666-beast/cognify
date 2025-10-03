from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('create/', views.topic_create, name='topic_create'),
    path('<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('<slug:slug>/edit/', views.topic_update, name='topic_update'),
    path('<slug:slug>/delete/', views.topic_delete, name='topic_delete'),
    path('<slug:slug>/activate/', views.topic_activate, name='topic_activate'),
    path('<slug:slug>/deactivate/', views.topic_deactivate, name='topic_deactivate'),

    # Question URLs
    path('<slug:topic_slug>/questions/add/', views.question_create, name='question_create'),
    path('<slug:topic_slug>/questions/<int:question_id>/', views.question_detail, name='question_detail'),
    path('<slug:topic_slug>/questions/<int:question_id>/edit/', views.question_update, name='question_update'),
    path('<slug:topic_slug>/questions/<int:question_id>/delete/', views.question_delete, name='question_delete'),

    # Answer URLs
    path('<slug:topic_slug>/questions/<int:question_id>/answers/add/', views.answer_create, name='answer_create'),
    path('<slug:topic_slug>/questions/<int:question_id>/answers/<int:answer_id>/edit/', views.answer_update,
         name='answer_update'),
    path('<slug:topic_slug>/questions/<int:question_id>/answers/<int:answer_id>/delete/', views.answer_delete,
         name='answer_delete'),
]
