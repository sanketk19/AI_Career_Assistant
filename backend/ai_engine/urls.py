
from django.urls import path
from . import views

urlpatterns = [

    path('chat/', views.ai_chat, name='ai_chat'),

    path(
        'resume-analysis/',
        views.resume_analysis,
        name='resume_analysis'
    ),

    path(
        'career-roadmap/',
        views.career_roadmap,
        name='career_roadmap'
    ),

    path(
        'chat-history/',
        views.chat_history,
        name='chat_history'
    ),

    path(
        'delete-chat-history/',
        views.delete_chat_history,
        name='delete_chat_history'
    ),

]
