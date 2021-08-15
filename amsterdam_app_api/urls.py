from django.urls import path
from amsterdam_app_api import views


""" Base path: /api/v1
"""

urlpatterns = [
    # Projects
    path('projects', views.projects),
    path('projects/ingest', views.ingest_projects),
    path('project/details', views.project_details),

    # Image
    path('image', views.image)
]
