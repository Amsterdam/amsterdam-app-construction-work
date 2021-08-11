from django.urls import path
from amsterdam_app_api import views


""" Base path: /api
"""

urlpatterns = [
    path('projects/', views.projects),
    path('projects/ingest', views.ingest_projects),
    path('project/details', views.project_details)
]
