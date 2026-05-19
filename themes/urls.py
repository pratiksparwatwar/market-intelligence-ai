from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('themes/', views.theme_list, name='theme_list'),
    path('themes/<int:pk>/', views.theme_detail, name='theme_detail'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('api/fetch-news/', views.trigger_fetch_news, name='fetch_news'),
    path('api/generate-themes/', views.trigger_generate_themes, name='generate_themes'),
    path('api/clear-data/', views.trigger_clear_data, name='clear_data'),
]
