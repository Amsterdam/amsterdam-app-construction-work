from django.urls import path
from amsterdam_app_api import views


urlpatterns = [
    path('api/projects/', views.all_projects),
    path('api/projects/ingest', views.ingest_all_projects)
]
