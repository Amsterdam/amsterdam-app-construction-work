from django.urls import path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from amsterdam_app_api import views_generic
from amsterdam_app_api import views_iprox_projects
from amsterdam_app_api import views_iprox_news
from amsterdam_app_api import views_ingest
from amsterdam_app_api import views_mobile_devices
from amsterdam_app_api import views_messages
from amsterdam_app_api import views_project_manager


schema_view = get_schema_view(
   openapi.Info(
      title="Amsterdam APP Backend API",
      default_version='v1',
      description="API backend server for Amsterdam App."
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

""" Base path: /api/v1
"""

urlpatterns = [
    # Swagger (drf-yasg framework)
    url(r'^apidocs$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Project(s)
    path('projects', views_iprox_projects.projects),
    path('project/details', views_iprox_projects.project_details),
    path('project/news', views_iprox_news.news),

    # Ingestion
    path('ingest', views_ingest.ingest_projects),

    # Image & Assets
    path('image', views_generic.image),
    path('asset', views_generic.asset),

    # Mobile devices (used for CRUD devices for push-notifications)
    path('notification/registration/device', views_mobile_devices.crud),

    # Project Manager (used to CRUD a project manager for notifications)
    path('notification/registration/project-manager', views_project_manager.crud),

    # Warning message
    path('notification/messages/warning/create', views_messages.warning_message_post),
    path('notification/messages/warning/get', views_messages.warning_message_get),

    # Push notification
    path('notification/messages/push/send', views_messages.push_notification_post),
    path('notification/messages/push/get', views_messages.push_notification_get)
]
