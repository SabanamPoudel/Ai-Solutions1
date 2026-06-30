from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # Public pages
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('articles/', views.articles, name='articles'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('case-studies/', views.case_studies, name='case_studies'),

    # Authentication
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # AJAX actions
    path('ajax/enquiry/<int:pk>/status/', views.update_enquiry_status, name='update_enquiry_status'),
    path('ajax/enquiry/<int:pk>/delete/', views.delete_enquiry, name='delete_enquiry'),
    path('ajax/feedback/<int:pk>/status/', views.update_feedback_status, name='update_feedback_status'),
    path('ajax/feedback/<int:pk>/delete/', views.delete_feedback, name='delete_feedback'),
    path('ajax/article/<int:pk>/toggle/', views.toggle_article_status, name='toggle_article'),
    path('ajax/event/<int:pk>/toggle/', views.toggle_event_status, name='toggle_event'),
    path('ajax/chatbot/<int:pk>/save/', views.save_chatbot_response, name='save_chatbot'),
    path('ajax/chatbot/add/', views.add_chatbot_response, name='add_chatbot'),
    path('ajax/chatbot/<int:pk>/delete/', views.delete_chatbot_response, name='delete_chatbot'),
    path('ajax/article/add/', views.add_article, name='add_article'),
    path('ajax/article/<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('ajax/article/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('ajax/event/add/', views.add_event, name='add_event'),
    path('ajax/event/<int:pk>/edit/', views.edit_event, name='edit_event'),
    path('ajax/event/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('ajax/service/add/', views.add_service, name='add_service'),
    path('ajax/service/<int:pk>/edit/', views.edit_service, name='edit_service'),
    path('ajax/service/<int:pk>/delete/', views.delete_service, name='delete_service'),
    path('ajax/chatbot/query/', views.chatbot_query, name='chatbot_query'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
